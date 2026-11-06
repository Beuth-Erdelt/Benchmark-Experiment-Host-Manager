# Plan: Uniform DBMS Example Pages

Status: proposed, 2026-11-03. Nothing implemented yet.

## Goal

Every supported DBMS has one page `docs/Example-<DBMS>.md` titled `Example: Benchmark <DBMS>`, with the same structure.
Each page has its own test script `scripts/test-docs-<dbms>.sh` / `.ps1`, whose runs appear in page order.
No content is copied: DBMS-specific content moves out of `DBMS.md` and `TestCases.md` into the pages.

## 1. Page template

```
# Example: Benchmark <DBMS>
Intro: what the DBMS is, single vs. cluster, what bexhoma deploys, supported workloads
Disclaimer (not official results)
References: clickable links (DBMS, benchmark, papers, test script .sh/.ps1)

## Perform <Main> Benchmark            quick run: SF 1, no monitoring
### Status
### Cleanup
### Evaluate Results                   summary + root notebooks/ (Collector-<Benchmark>.ipynb)

## Monitoring                          -m / -mc, aggregation across components
### Example Result                     bigger run: SF 3, -m -mc, >= 1 min benchmarking
### Application Metrics                only if supported: -ma, embeds docs_<bench>_<dbms>_appmetrics

## Persistent Storage                  -rst / -rss / -rsr / -rsrp
### Example Result                     (+ cluster / ramdisk example where available)

## Variants                            only if applicable
### <Cluster / Replication / Scaling components / Pooling / ...>   each with example result

## Technical Details
### Configuration of Bexhoma           cluster.config section (from "Example Explained" + DBMS.md)
### Deployment                         template, services, monitoring exporter, placeholder SUT, ...
### Schema and Scripts                 init/check scripts per benchmark
### Load Durability                    what -xld does for this DBMS + link to Test-Durability result
### Reset Scripts                      what -ar does for this DBMS + link to Test-Reset result

## <Further use case>                  e.g. Benchbase's TPC-C, HammerDB, TPC-DS, SSB
...
```

Sections that do not apply are omitted, not left empty.
Reset and durability results are linked (as Test-Reset.md does), not embedded, to limit page size.

## 2. Run roles and log names

`docs_<benchmark>_<dbms>[_<role>].log`, same `_summary.md`:

| Role | Suffix | Rule |
|---|---|---|
| main | none | quick, SF 1, no `-m` |
| monitoring | `_monitoring` | SF 3 (or larger), `-m -mc`, benchmarking >= 1 min |
| app metrics | `_appmetrics` | stays in `test-docs-appmetrics` (except YugabyteDB), embedded on the page |
| persistency | `_storage` | `-rst -rsr -nc 2` |
| ramdisk | `_ramdisk` | `-rst ramdisk` |
| variants | `_cluster`, `_replica`, `_cluster_storage`, ... | |
| further use cases | `docs_<bench>_<dbms>[_role]` | |

Numbered logs (`docs_ycsb_redis_1`) and `testcase_*` logs are renamed with `git mv` (log + summary),
references in docs and scripts updated. Reruns only where a run violates the rules above.

## 3. Scripts

- one script per DBMS page, sections commented in page order
- `test-docs-cases`: MySQL -> `test-docs-mysql`, MariaDB -> `test-docs-mariadb`, PostgreSQL -> `test-docs-postgresql`,
  MonetDB -> `test-docs-monetdb`, fio sweeps -> `test-docs-hardware`; only the Compare runs remain
- `test-docs-tpch`: MonetDB SF 100 runs -> `test-docs-monetdb`
- `test-docs-ti` -> `test-docs-tidb`
- `test-docs-cedardb`, `Example-Other-DBMS.md`: unchanged (CedarDB results may not be published)
- new `test-docs-pgduckdb`: collects the PgDuckDB runs (TPC-H, SSB, ...) for its own page
- cross-cutting scripts stay: appmetrics, reset, durability, modes, multitenant, collector, benchmark pages
- `.sh` and `.ps1` always changed together

## 4. Other files

- `DBMS.md`: keeps general concepts (configuration reference, template conventions, reset/durability overview
  tables, add a new DBMS) and a short paragraph + link per DBMS; the rest moves to the pages.
  ClickHouseCluster -> ClickHouse page, DragonflyCluster -> Dragonfly page, Hardware -> Example-Hardware.
- `TestCases.md`: keeps Compare (anchors `#tpc-h`, `#tpc-ds` stay), becomes the index of all test scripts;
  hardware section -> Example-Hardware.
- `Example-TPC-H.md`: MonetDB SF 100 section -> Example-MonetDB, link remains.
- `Example-Result-TPC-H-MonetDB.md`: absorbed into Example-MonetDB, deleted.
- `index.rst`, cross-links and anchors updated; `scan-docs.py` lists missing logs at the end.

## 5. Phases (one commit each, no live runs)

1. Pilot Redis
2. Dragonfly, Valkey, Garnet, Cassandra
3. Citus, YugabyteDB, CockroachDB, TiDB, PGBouncer
4. ClickHouse, MariaDBCS
5. PostgreSQL, PgDuckDB, MySQL, MariaDB, MonetDB (split test-docs-cases, TestCases.md, fio -> Hardware)
6. DatabaseService, DBMS.md cleanup, index.rst, cross-links, final scan

After each phase: list of runs that have to be (re)run on the cluster.

## 6. Pilot Redis

| Section | Log | Source |
|---|---|---|
| Main | `docs_ycsb_redis` | NEW run: SF 1, no `-m` |
| Monitoring | `docs_ycsb_redis_monitoring` | NEW run: `_1` with `-xop 10` (`_1` benchmarks only 15 s); `_1` is deleted |
| App Metrics | `docs_ycsb_redis_appmetrics` | existing |
| Persistency | `docs_ycsb_redis_storage` | rename `_4` |
| Variants: Cluster | `docs_ycsb_redis_cluster`, `docs_ycsb_redis_cluster_storage` | rename `_2`, `_5` |
| Variants: Replication | `docs_ycsb_redis_replica` | rename `_3` |
| Technical Details | links `docs_reset_ycsb_redis`, `docs_reset_ycsb_redis_cluster` | existing |

Status pilot: implemented 2026-11-03 (page, scripts, log renames, DBMS.md section). Open runs: `docs_ycsb_redis`, `docs_ycsb_redis_monitoring`.

## Notes

- Do not run `scripts/_sync_docs.py` as a check: it rewrites commands in all pages, and several pages have drifted
  from their scripts (e.g. TiDB `-rnw`, Collectors, TPC-DS). Sync per page while restructuring it.

Status phase 2: implemented 2026-11-03 (Dragonfly, Valkey, Garnet, Cassandra). Open runs (all new, not yet on the cluster):
`docs_ycsb_<dbms>` and `docs_ycsb_<dbms>_monitoring` for all four, plus `docs_ycsb_valkey_appmetrics`.
- Monitoring runs include `-ma` where the SUT pod is discovered (Dragonfly, Cassandra); Redis and Valkey
  discover workers only, so their app metrics come from a cluster run (`_appmetrics`).
- Fixed in ycsb.py: Redis, Valkey, Garnet set `monitoring_sut = False` also for a single host, so single-host
  runs had no SUT metrics. Now only in cluster mode (as Dragonfly).
- Helper scripts for the rollout are in the session scratchpad (restructure.py, gen_*.py); not part of the repo.

Status phase 3: implemented 2026-11-03 (Citus, YugabyteDB, CockroachDB, TiDB, PGBouncer). Open runs: only the quick
main runs `docs_ycsb_<dbms>`; the old first runs benchmark >= 1 min and became `_monitoring`.
- `.sh` had drifted from `.ps1` (the script that is run): `-rnw` missing in Citus, CockroachDB, TiDB and the
  CockroachDB/TiDB app-metrics runs, YugabyteDB installed without node pinning, `BEXHOMA_NODES_WORKER(_4)` missing in
  testfunctions.sh. Fixed; page commands now taken from the synced `.sh`.
- Further use cases are named like the PostgreSQL pages: `_scale`, `_keytime`, `_storage`, `_columnar`, `_paper`.
- TiDB: `docs_ycsb_tidb_3` was the same run as `docs_ycsb_tidb_appmetrics` (only -lr/-rr differ), removed;
  `test-docs-ti` renamed to `test-docs-tidb`.
- YugabyteDB: every run section has its own install/remove; the `-sl` run follows the monitoring run on the same install.
- `scripts/test-pool.sh` (old, not a docs script) still writes `docs_ycsb_pgbouncer_1/2.log`; names no longer used.

Status phase 4: implemented 2026-11-03 (ClickHouse, MariaDBCS). Open runs: `docs_tpch_<dbms>` (SF 1, no storage,
no monitoring) and `docs_tpch_<dbms>_monitoring` (SF 10: at SF 1 the 22 queries take 9 s / 25 s).
- The existing runs (storage, -nc 2) became `_storage`; ClickHouseCluster is a variant (`_cluster`).
- MariaDBCS: main and monitoring run MariaDBCS only; `_storage` keeps the comparison with MariaDB (-xdt).
- DBMS.md: ClickHouse, ClickHouseCluster, MariaDB ColumnStore reduced to a summary; tables moved to the pages.

Status phase 5: implemented 2026-11-03 (PostgreSQL, PgDuckDB, MySQL, MariaDB, MonetDB, TestCases, fio).
- MySQL, MariaDB: all runs from test-docs-cases (testcase_* renamed to docs_<bench>_<dbms>_<role>), no new runs.
- PostgreSQL (decision 2026-11-03): page reuses the runs of the benchmark pages, no own script; the 18
  testcase_*_postgresql duplicates removed; RAM disk run moved to test-docs-tpch as docs_tpch_postgresql_ramdisk.
- MonetDB: SF 100 (TPC-H) and SF 30 (TPC-DS) sections moved from Example-TPC-H/-TPC-DS (pointer left),
  Example-Result-TPC-H-MonetDB.md deleted. New runs: docs_tpch_monetdb, _monitoring (SF 30), _storage.
- PgDuckDB: new script, all runs new (derived from the PostgreSQL TPC-H runs, -xdfe; --set targets
  bexhoma-deployment-pg-duck). Check that the SF 10 monitoring run benchmarks >= 1 min in DuckDB's engine.
- fio sweeps 5-12 moved to test-docs-hardware / Example-Hardware; test-docs-cases keeps the two Compare runs
  (docs_tpch_compare, docs_tpcds_compare); TestCases.md is the index of all test scripts.
- -xdt comment fixed in all scripts ("also measure data transfer volume per query").
- Leftovers not touched: logs_tests/test_tpcds_testcase_compare_summary.md (v0.10.0, unreferenced),
  scripts/test-cloud-notes.sh and test-pool.sh (old, own log names).

Status phase 6: implemented 2026-11-03.
- Example-CloudDatabase (DatabaseService): template order; logs renamed in place (script order kept for the kubectl
  placeholder glue); the -sl run (152 s benchmarking, -m -mc) is the monitoring example. No new runs.
- DBMS.md: overview table (key, benchmarks from the -dbms choices of the entry scripts, example page), short
  PgDuckDB section, Hardware details moved to Example-Hardware#technical-details, page structure and log naming
  documented as step 6 of "Add a New DBMS". DBMS.md: 1489 -> 699 lines.
- docs/conf.py: myst_heading_anchors = 4 (heading links resolve in Sphinx as on GitHub).
- Link check: no broken page/anchor links on the restructured pages (remaining: API.md, Examples.md, old pages).
