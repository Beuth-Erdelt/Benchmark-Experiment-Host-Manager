# Plan: flexible and reliable result comparison (dbmsbenchmarker + bexhoma)

Status: **proposal**, nothing implemented. Written 2026-10-30 after the TPC-H and TPC-DS
cross-DBMS comparison at SF=3 (experiments 1793305221, 1793360424, 1793379736).

Touches **two repositories**: `DBMS-Benchmarker` (the comparison itself) and
`Benchmark-Experiment-Host-Manager` (bexhoma: query configs, summary, tests, contracts, docs).

## 1. Problem

How dbmsbenchmarker compares result sets today (read from the code, commit 65879ee):

| Stage | Where | What it does |
|-------|-------|--------------|
| Normalise per run | `benchmarker.py` `singleResult` (407-514) | cells to `str().strip()`; with `sorted: True` numbers are rounded to `datatransfer.precision` and rows sorted; the stored pickle is the rounded, sorted result |
| Repeat runs | `benchmarker.py` 1505, 1541 | exact list equality inside one process |
| Across connections | `tools.py` `merge_partial_results` (1764-1927) | first connection is the reference; both sides rounded to **2 decimals (hard-coded)**, sorted, compared with `pd.concat([df1, df2, df2]).drop_duplicates(keep=False)` |

Defects observed in our runs:

1. **Lossy storage.** Rounding happens before storing (TPC-DS: 0 decimals), so the raw values cannot be
   re-evaluated later.
2. **False alarms at rounding boundaries** (25.4999 vs 25.5; Q1, Q12, Q75) and **blindness below the precision**.
3. **Duplicate blindness.** `drop_duplicates(keep=False)` ignores row multiplicities; a row present twice on one
   side and absent on the other is not found.
4. **Order is never checked** (stage 1 and the merge sort), so a wrong `ORDER BY` is invisible; only the `LIMIT`
   boundary shows it.
5. **First connection is the reference.** A failed or odd first connection flags every other one.
6. **Column titles must match** (ClickHouse `D1.D_WEEK_SEQ` vs `D_WEEK_SEQ` flagged Q72 for four systems).
7. **`''` vs NULL, `None`/`nan`/`\N`** are different strings.
8. **No diagnosis.** The result is 0/1 per query and connection; no hint which rows, which columns, why.
9. **The bexhoma contract understates the check** (see section 7).

## 2. Comparison levels

The verdict per query and connection is the **highest level reached**.

| Level | Meaning |
|-------|---------|
| L0 | same shape: row count and column count |
| L1a | same multiset after canonicalization, exact (a real `Counter`, not `drop_duplicates`) |
| L1b | same multiset, numbers within a tolerance |
| L2k | same sequence of the `ORDER BY` key values; rows with equal keys may permute (tie groups) |
| L2s | same strict row-by-row sequence |
| L3 | byte-identical serialization of the raw result (same engine only: regressions, repeat runs) |

`ORDER BY … LIMIT n` queries get a **tie-aware boundary** rule: rows whose key equals the last key at the cut
may differ; any other difference is a mismatch.

Canonicalization (pluggable, per query):

- strings: strip, optional right-trim of CHAR padding, optional case folding
- NULL: unify `None`, `NULL`, `\N`, `nan`; `null_equals_empty` off by default (a difference is reported as
  *explained*, e.g. "NULL vs empty string")
- numbers: `1e5` = `100000`, `-0.0` = `0`; tolerance mode `{abs, rel}` instead of rounding
- dates and timestamps: `1998-01-01` = `1998-01-01 00:00:00`
- booleans
- column names: strip table qualifier, case-insensitive; match by position or by name

Tolerance is not transitive, so it cannot be applied by hashing rounded values. Group rows by their
non-numeric columns first, then compare the numeric columns with `isclose` inside each group.

## 3. Configuration

New optional `comparison` block per query, with defaults at the top level of the queries config:

```python
'comparison': {
    'level': 'L1b',
    'numeric': {'mode': 'tolerance', 'abs': 0.01, 'rel': 1e-6},
    'strings': {'strip': True, 'rtrim_char': True, 'case_sensitive': True},
    'nulls':   {'null_equals_empty': False},
    'columns': {'match': 'position', 'strip_qualifier': True, 'case_insensitive': True},
    'order_by': [0, 1, 3],        # key columns for L2k, written by the query config builder
    'reference': 'majority',      # 'first' | 'majority' | '<connection>' | 'golden'
}
```

Backward compatibility: without the block, `datatransfer.compare: 'result'` + `precision` + `sorted` behave as
today (L1a with the configured precision). `hash` and `size` stay as they are.

## 4. dbmsbenchmarker changes

| File | Change |
|------|--------|
| new `dbmsbenchmarker/compare.py` | `canonicalize(rows, spec)`, `compare(a, b, spec) -> CompareResult(level, details)` |
| `benchmarker.py` `singleResult` | store raw stripped values and column names; sorting stays optional for storage; keep the in-run check but call `compare` |
| `tools.py` `merge_partial_results` | replace first-connection logic: equivalence classes (connections with identical canonical result), reference by policy, failed connections excluded; write the level and a details dict to the protocol |
| `inspector.py` | `getDifference12` kept for old result folders |
| `evaluator.py`, `layout.py` | `get_total_warnings` keeps its 0/1 shape for compatibility; new `get_comparison_levels`; dashboard heatmap shows levels |
| `docs/`, `tests/` | document the options; unit tests (section 8) |

Details per query and connection: rows only on each side (count and up to N examples), per-column mismatch
counts with maximum absolute and relative difference, and a hint for known causes (`''` vs NULL, column title,
rounding boundary, tie at the `LIMIT` cut, NULL ordering).

## 5. bexhoma changes

| Where | Change |
|-------|--------|
| `bexhoma/benchmarks/tpch.py`, `tpcds.py`, `ssb.py` (`tpcc.py`) | write the `comparison` block into the generated queries config; set `order_by` from the query definition |
| `experiments/*/queries-*.config` | the `datatransfer` blocks (`precision`, `sorted`, `compare`) stay valid; add `comparison` defaults |
| `bexhoma/evaluators/dbmsbenchmarker.py` | read the level matrix next to `get_total_warnings`; test "SQL warnings (result mismatch)" is derived from the required level |
| `bexhoma/collectors/dbmsbenchmarker.py`, `experiments/base.py` (3677-3820), `benchmarks/base.py` (883), `report_writer.py` | summary section "Warnings (result mismatch)" becomes a level matrix; keep the old table while the version transition lasts |
| CLI (`tpch.py`, `tpcds.py`, `ssb.py`) | `-xcl/--xcompare-level` (and tolerance) as `-x` options per the existing convention |
| benchmarker image | the benchmarker container must contain the new dbmsbenchmarker; pin the version in `requirements` and the image build |
| `contracts/contract_result.yml`, `contract_catalog.yml` | see section 7 |
| docs | `Queries-TPC-H.md` and `Queries-TPC-DS.md` section "How the results are compared"; `AgentReport.md` if the summary changes |

## 6. Phases

1. **Core and tests.** `compare.py` with canonicalization, levels L0 to L2s, unit tests from the cases in section
   8; store raw values; keep the old behavior as default. Offline tool that re-evaluates an existing result folder.
2. **Merge and report.** Equivalence classes, reference policy, details in the protocol, level matrix in the
   dbmsbenchmarker summary and in bexhoma.
3. **bexhoma integration.** Query config builders, CLI options, contract and docs, image.
4. **Golden results.** Optional expected result (TPC answer sets at SF=1) as a reference.
5. **Order keys.** `order_by` written by the query config builders; L2k enabled for queries with `ORDER BY`.

Phase 1 alone already makes the existing SF=3 result folders re-evaluable once they store raw values (new runs).

## 7. Contract finding (needs a decision)

`contracts/contract_result.yml` (`no_sql_warnings`, line 172, and the limitation on line 278) says the check
compares result sets "only inside one driver process" and passes vacuously at numRun=1 because bexhoma uses one
pod per connection. The runs in this session show something different: the merged protocol **does** flag
cross-connection mismatches (for example Q36 and Q20 in TPC-DS experiment 1793360424, TPC-H Q11 in 1793305221),
produced by `merge_partial_results` over the connection subfolders of one experiment code. The contract text
appears outdated and should be verified and corrected, with a version bump (`result_contract_version` is
"1.12.0", == `report_writer.SCHEMA_VERSION`), independent of this plan.

## 8. Test cases (from observed problems)

- ClickHouse `''` vs NULL (TPC-DS Q18, Q67)
- qualified column title `D1.D_WEEK_SEQ` (Q72)
- rounding boundary: average 25.4998 vs 25.50 (TPC-H Q1 on MonetDB, TPC-DS Q12)
- ±1 on a rounded sum (Q75)
- duplicate rows on one side only
- NULL ordering at a `LIMIT` cut (Q74, Q76, Q99, Q56)
- tie at the `LIMIT` cut
- empty vs grand-total row of a `ROLLUP` over an empty input (Q27, Q36 before the TN change)
- failed first connection (ClickHouseCluster) must not flag the others
- old result folders (rounded pickles) still compare as before

## 9. Risks and open questions

- **Size.** Large result sets: hash first, run the tolerance matching only on rows that did not hash equal.
- **Pickle size and format.** Raw storage is larger; old folders must keep working (feature-detect).
- **Order keys.** Parsing `ORDER BY` out of SQL is brittle; the query config builder should declare them.
- **Tolerance defaults.** Too loose hides real errors, too tight brings back the false alarms; start with
  `abs 0.01, rel 1e-6` and check against the stored SF=3 results.
- **Two repositories.** Version coupling: bexhoma passes the new config block, an old benchmarker image ignores it
  (must not fail); decide the minimum dbmsbenchmarker version.
- **Scope of L3.** Only meaningful within one engine; decide whether it is worth exposing.
