

## Interpretation

**What came back:** The experiment that ran (code `1787175665`) is the **forced-execution side only** — `duckdb_force_execution: true`, TPC-H SF1, 16 CPU / 64 GiB, 1 and 8 concurrent streams, all 22 queries, 2 repeats, 3 repetitions. It is the first of the two sequential experiments you designed.

**Is it trustworthy? Yes.** All 7 validity checks passed (`report/index.md`, `overall_status: passed 7 / failed 0`): no SUT container restarts, no SQL errors, no SQL warnings, no 0/NaN in the headline metrics, and the workflow ran as planned. So the forced-side numbers are sound and quotable.

**Forced-side numbers** (`report/index.md`, Key Metrics, 3 repetitions):

| Streams | Geo Times [s] | Throughput@Size |
|---|---|---|
| 1 | 0.51 / 0.56 / 0.58 | 2933.33 / 2400.00 / 2329.41 |
| 8 | 0.83 / 0.82 / 0.83 | 12930.61 / 13200.00 / 12672.00 |

**What it does *not* answer — and this is the key finding:** Your question is a **comparison** (force vs. default), and only one side of that comparison exists. The follow-up experiment with `duckdb_force_execution: false` has **not been run**. `list_results()` shows `1787175665` is the newest finished experiment; because experiment codes are monotonically increasing, a follow-up would need a *greater* code, and none exists. So:

- **Overall recommendation (force vs. default): unresolved.** I cannot tell you whether to force or leave routing at default, because the default-routing baseline has not been measured. The forced side alone tells you how fast forced execution is, but not whether it beats cost-based routing.
- **Consistency across query shapes: unresolved.** A per-query-shape verdict needs per-query latency/throughput for *both* modes. The forced side ran all 22 queries cleanly (no errors/warnings, no 0/NaN), so its per-query detail is complete in `report/execution.md` — but there is no forced=false per-query data to compare it against, so no query can yet be shown to favor the opposite mode.

**What the hypothesis got right / wrong:** The design was correct — it used two sequential experiments with a single `PgDuckDB` entry each (never two same-named entries in one experiment), and the forced side executed exactly as specified. The hypothesis's premise (that the two sides must be compared overall and per query shape) is sound; it is simply that the second half of the comparison is still missing.

**What's missing to settle the question:** the `duckdb_force_execution: false` follow-up (identical design) must be run and its report produced. Once it exists, the forced side's Geo Times / Throughput@Size can be compared against the default side overall and per query shape to yield the recommendation and identify any queries that favor the opposite mode.



Submitted.

**Experiment code: `1787179264`**

**What the run will settle:** This is the cost-based-routing baseline (`duckdb_force_execution: false`) — the missing second half of the two-experiment comparison. It is byte-for-byte identical to the completed forced-side run (`1787175665`) except for the single knob override, so the two runs are directly comparable:

- **Overall recommendation (force vs. default):** compare Geo Times and Throughput@Size at 1 and 8 streams against the forced side (0.51/0.56/0.58 s and 2933/2400/2329 Q/h at 1 stream; 0.83/0.82/0.83 s and 12931/13200/12672 Q/h at 8 streams).
- **Consistency across query shapes:** compare per-query (Q1–Q22) latency between the two runs to identify any queries that favor the opposite mode.

Design details: TPC-H SF1, 16 CPU / 64 GiB, rounds [1, 8], query_repeats 2, 3 repetitions, post_load statistics, single `PgDuckDB` entry on `cl-worker36`, `analytical-ssd` profile with `storage_class` unset (satisfies the profile's `[ssd, null]` requirement). Validation passed; estimate is 6 runs.
