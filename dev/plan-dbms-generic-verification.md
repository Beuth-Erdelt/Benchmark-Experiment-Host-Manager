# Plan: what is left after the DBMS-generic refactor (#850)

Status: **open, 2026-11-22.** The refactor (branch dbms-agnostic-code, #850) is in v0.11.13. The full
test-docs suite (~490 logs, 2026-11-11..18) passed and covers most of the old checklist. This plan lists only
what was never checked after the refactor, and what follows from it.

Checked 2026-11-23: section 1 is **done** and merged in #901 (v0.12.2). The 1.5 rerun with indexes,
constraints and statistics `true` (`tests/yaml_experiments/tpch-postgres-vs-pgduckdb.yaml`) passed every test;
the docs placeholders are filled, `logs_tests/SUMMARY.md` has no unchecked row. Still open, with no change since
2026-11-22: section 2 (CedarDB SSB never ran; `docs_tpch_databaseservice_execution.log` is still 0.11.12),
section 3 (`_show_loading_provenance()` still records "Loading measured" as passed under `-sl`), sections 4, 5, 7.
Side finding of 1.5, not fixed: the PgDuckDB force-execution workload note ignores a system's own `sut_parameters`.

Already covered, do not re-propose: refresh for CedarDB/Citus/ClickHouseCluster/DatabaseService; tenancy
container/database/schema; `-xdim distributed`; `-xcol`; `-xdfe`; TiDB/YugabyteDB/CockroachDB/Cassandra;
key-value cluster and replica modes; MariaDBCS `-nlp` notice; PGBouncer pooling with single values;
`-sl` on YugabyteDB (YCSB, 0.11.18) and DatabaseService (Benchbase, 0.11.13).

Branch: `dbms-generic-verification-runs` (from dev, commit b2a26bfc, not pushed).

## 1. New blocks (run 2026-11-22, done, #901)

The four new blocks of b2a26bfc run one after the other, log to `logs_tests/`:

| Item | Script | Log | Check |
|---|---|---|---|
| 1.1 refresh stream, PostgreSQL + PgDuckDB, `-xrs 3` | test-docs-tpch | `docs_tpch_refresh_two_dbms.log` | one refresh section per DBMS; RF1 inserts = RF2 deletes in orders/lineitem for each; same job template |
| 1.5 `bexhoma experiment dev/yaml_experiments/tpch-postgres-vs-pgduckdb.yaml` | test-docs-tpch | `docs_tpch_yaml_experiment.log` | PostgreSQL alias "DBMS A2" (from the YAML), PgDuckDB = template alias; `DUCKDB_FORCE_EXECUTION=true` in the PgDuckDB SUT; storage prefix per DBMS |
| 3.1 Benchbase PGBouncer, `-xnpp 1,2 -xnpi 32,64 -xnpo 32` | test-docs-pgbouncer | `docs_benchbase_pgbouncer_pool_sweep.log` | 4 configurations; 1 and 2 pooler pods; MAX_CLIENT_CONN 32/64; pool size 32 |
| 3.2 YCSB PGBouncer, `-nlt 16,64`, no pool flags | test-docs-pgbouncer | `docs_ycsb_pgbouncer_pool_default.log` | default pool size = 16 and 64, per configuration (before the refactor: always the first value) |

Runner: a copy of exactly these blocks (scratchpad `run_new_blocks.sh`), so the commands equal the scripts.

Results (2026-11-22, bexhoma 0.12.2, 11:27-13:04):

- [x] 1.1 passed (7 min): `tpch_refresh` job per DBMS (`pgduckdb-1-1-1-2`, `postgresql-1-1-1-2`), no SQL errors.
  The summary shows only the refresh job times, not RF1/RF2 row counts, so that part of the check is not visible.
- [ ] 1.5 **failed** (73 min): `SQL errors` and `Some active queries missing from the totals`: PostgreSQL
  Q17 and Q20 cancelled by the 600 s timeout in every phase (`canceling statement due to user request`).
  Cause: the YAML sets `init_indexes/init_constraints/init_statistics: false`; the command line examples use
  `-xii -xic -xis`. The rest is right (checked in the result folder): alias `DBMS A2` for PostgreSQL,
  `General-F` (template) for PgDuckDB; storage `postgresql` and `PgDuckDB`; `DUCKDB_FORCE_EXECUTION=true` in
  the PgDuckDB SUT manifest. Side finding: the workload note "PgDuckDB queries are forced through the DuckDB
  execution engine" is missing, because the note follows only the global `tpch.duckdb_force_execution`, not a
  system's own `sut_parameters`.
  Fix proposal: indexes, constraints, statistics `true` in the YAML, then rerun only this block.
- [x] 3.1 passed (11 min): 4 configurations; pooler pods 1, 1, 2, 2; MAX_CLIENT_CONN 32, 64, 32, 64;
  DEFAULT/MIN_POOL_SIZE 32 everywhere (from the pool pods' describe logs; the summary does not show pool sizes).
- [x] 3.2 passed (4 min): DEFAULT/MIN_POOL_SIZE and MAX_CLIENT_CONN = 16 for PGBouncer-1, 64 for PGBouncer-2.

After the runs:

- [ ] Check every log against its "Check:" column; any failed test is a finding, not a doc edit.
- [ ] `python scripts/replace-docs.py`: fills the "(not run yet)" placeholders in
  `docs/Example-TPC-H.md` ("Refresh Stream on two DBMS"), `docs/Example-PGBouncer.md` ("Sweeping the Pool"),
  `docs/Design-Yaml-Experiment-Entry-Script.md` ("Example Run").
- [ ] `python scripts/demo-runs.py`: regenerate `logs_tests/SUMMARY.md` (now 4 unchecked rows; CI `--check`).
- [ ] Commit logs, summaries, docs on the branch (`Test: ...`), do not push.

## 2. Existing blocks that never ran after the refactor

- [ ] 1.2 CedarDB SSB, dialect CedarDB: `scripts/test-docs-cedardb.sh` block with log
  `doc_ssb_testcase_cedardb_normal.log`. All 13 queries succeed, queries unchanged.
  CedarDB results are never published (`tests/test_unpublished_results.py`): log stays internal, no doc page.
- [ ] 2.1 TPC-H DatabaseService `-sl`: `scripts/test-docs-databaseservice.sh`, log
  `docs_tpch_databaseservice_execution.log`; last run was 0.11.12 (pre-refactor). Needs the
  `docs_tpch_databaseservice.log` block before it, which loads the external database.

## 3. Bug: "Loading measured in this experiment" passes with `-sl`

All `-sl` logs show `TEST passed: Loading measured in this experiment`, although nothing was loaded.

Cause: `_show_loading_provenance()` (`bexhoma/experiments/base.py:1898-1921`) only knows `storage_reused`,
which comes from the PVC `loaded=True` gate. `-sl` is for DBMS bexhoma does not manage (no PVC, state
unknown), so `storage_reused` is False and the test is recorded as passed.

- [x] Fix (2026-11-23): `connections.config` gets `loading_deactivated` per connection
  (`configurations/metrics.py`); `_show_loading_provenance()` records the test as skipped
  "(loading skipped by -sl, DBMS not managed by bexhoma: <configurations>)", combined with the reuse reason when
  both apply. Results without the field fall back to the workload note "Loading is skipped.". Result contract
  1.15.0 (`skipped_when` extended).
- [x] Unit tests in `tests/test_storage_classes.py::LoadingProvenanceTest` (with/without `-sl`, both reasons,
  old results); the report's interpretation text in `report_writer.py` describes the skipped variant.
- [ ] Verified by the 2.1 rerun (section 2): the summary must show the skipped test.

## 4. Phase 0: local refusals (no cluster; kubectl context without access)

- [ ] 0.1 `bexhoma hammerdb -h`, `bexhoma ycsb -h`: `-dbms` choices = DBMS whose cluster.config
  `benchmarks:` lists the benchmark.
- [ ] 0.2 Refused early with a clear reason, before any Kubernetes call:
  `tpch -dbms MySQL -mtn 2 -mtb database`; `benchbase -dbms MySQL -mtn 2 -mtb schema`;
  `tpch -dbms Citus -xdim distributed`; `tpch -dbms PostgreSQL ClickHouse -xrs 1` ("need different ones").
- [ ] If they pass: turn them into unit tests next to `tests/test_system_builder.py`, so they need no rerun.

## 5. Decisions for the user (before any run)

- [ ] 4.1 SSB `-xsv flat`: PostgreSQL/MonetDB/CedarDB/PgDuckDB use `reset-ssb.sql`,
  MySQL/MariaDB/MariaDBCS/ClickHouseCluster/Citus `reset-ssb-flat.sql`. Intended?
  Test: `bexhoma ssb -dbms PostgreSQL -xsv flat -ar run`.
- [ ] 4.2 Container tenancy for MySQL/MariaDB: try `bexhoma tpch -dbms MySQL -mtn 2 -mtb container -nlp 2 run`;
  if it works, add `multi_tenancy: [container]` to their tpch entries in cluster.config.
- [ ] 4.3 Dragonfly cluster with `-m`: "Monitoring metrics missing" (worker filesystem series absent for
  in-memory runs). Proposal: DBMS-level `sparse_metrics` {metric: [component types]} merged into
  `sparse_components` in `metrics.py`. Not implemented.

## 6. Deferred

- 1.4 Aliases (user: "for the future"): an existing multi-DBMS summary and one anonymized DBMSBenchmarker
  dashboard show only architecture aliases (General-D, Columnwise-A, ...), never "DBMS A1", nothing reveals a
  derived DBMS.

## 7. Tooling found broken on the way

- [ ] `scripts/_reorder_flags.py` is stale: moves `-rnp` and `-ar` to the end of each call; one run rewrote
  53 files. Fix the flag order it expects, or remove it. Do not run it until then.
- [ ] `scripts/_sync_ps.py`: drops the second value of `-dbms A B`, and mangles a call without flags
  (`bexhoma experiment <yaml>`). Both fixed by hand in b2a26bfc; fix the tool and add a test case for both.

## Order

1 (done) → 3 (small fix, then verified by 2.1) → 2 → 7 → 4 → 5 after decisions.
