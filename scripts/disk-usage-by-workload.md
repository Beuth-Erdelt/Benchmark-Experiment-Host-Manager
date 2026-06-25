# Database Disk Usage by Workload / DBMS / SF

Extracted from log files in `logs_tests/`.

- **✓ extracted** — value read directly from `volume_used` or `datadisk` in a log file
- **~ proposed** — estimated by linear extrapolation or analogy; no measured log exists

`datadisk` unit note: for TPC-DS storage logs the value is in 1 K-blocks (KB); for TPC-H, YCSB and Benchbase logs it is in MB.  
`volume_used` is always human-readable and is the preferred source.

---

## TPC-H

| DBMS | SF | volume\_used | datadisk | Status | Source |
|------|----|-------------|---------|--------|--------|
| PostgreSQL | 0.1 | 312 MB | 315–316 MB | ✓ extracted | `doc_tpch_testcase_fractional.log`, `test_tpch_run_postgresql_small.log` |
| PostgreSQL | 1 | 2.7 G | 2,757–2,758 MB | ✓ extracted | `doc_tpch_testcase_storage.log`, multiple test logs |
| PostgreSQL | 1 (2 schemas) | 5.4 G | 5,476 MB | ✓ extracted | `test_tpch_run_postgresql_tenants_schema_storage.log` |
| PostgreSQL | 3 | ~8 G | — | ~ proposed | linear from SF=1→SF=10 |
| PostgreSQL | 10 | ~27 G | 27,209 MB | ✓ extracted | `doc_tpch_testcase_monitoring.log` |
| PostgreSQL | 30 | ~81 G | — | ~ proposed | linear from SF=10 |
| PostgreSQL | 100 | ~270 G | — | ~ proposed | linear from SF=10 |
| MonetDB | 1 | ~2 G | — | ~ proposed | scaled from SF=100 (162–200 G ÷ 100) |
| MonetDB | 10 | ~18 G | — | ~ proposed | scaled from SF=100 |
| MonetDB | 100 | 162–200 G | 165,384 MB | ✓ extracted | `doc_tpch_monetdb_1.log`, `_2.log`, `_3.log` |
| MariaDB | 1 | 2.1 G | — | ✓ extracted | `test_tpch_testcase_mariadb_3.log` |
| MariaDB | 3 | ~7 G | — | ~ proposed | linear from SF=1 |
| MariaDB | 10 | ~22 G | — | ~ proposed | linear from SF=1 |
| MySQL | 1 | 8.1 G | 8,286 MB | ✓ extracted | `test_tpch_testcase_mysql_3.log` |
| MySQL | 3 | ~25 G | — | ~ proposed | linear from SF=1 |
| MySQL | 10 | ~85 G | — | ~ proposed | linear from SF=1 |
| Citus | 10 | ~40 M (coord) | — | ✓ extracted (coord only) | `test_tpch_testcase_citus_2/3.log` — data is distributed on worker nodes |

---

## TPC-DS

| DBMS | SF | volume\_used | datadisk | Status | Source |
|------|----|-------------|---------|--------|--------|
| PostgreSQL | 1 | 5.7 G | 5,959,496 KB | ✓ extracted | `doc_tpcds_testcase_postgresql_storage.log` |
| PostgreSQL | 3 | ~16 G | — | ~ proposed | interpolated between SF=1 (5.7 G) and SF=10 (54 G) |
| PostgreSQL | 10 | 54 G | 55,265–55,281 MB | ✓ extracted | `test_tpcds_testcase_postgresql_2/3.log` |
| PostgreSQL | 30 | ~165 G | — | ~ proposed | linear from SF=10 |
| PostgreSQL | 100 | ~500 G | — | ~ proposed | linear from SF=10; PostgreSQL larger than MonetDB at SF=100 |
| MonetDB | 1 | 3.8 G | 3,933,059 KB | ✓ extracted | `doc_tpcds_testcase_monetdb_storage.log` |
| MonetDB | 3 | 5.3 G | 5,486,698–6,065,324 KB | ✓ extracted | `test_tpcds_testcase_monetdb_1/2/3.log` |
| MonetDB | 10 | 40 G | — | ✓ extracted | `doc_tpcds_testcase_profiling.log` |
| MonetDB | 30 | 52–75 G (avg 74 G) | — | ✓ extracted | `doc_tpcds_monetdb_1/2/3.log` |
| MonetDB | 100 | 151–155 G | 162,530,732 KB | ✓ extracted | `test_tpcds_testcase_monetdb_4.log` |
| MariaDB | 1 | 4.5 G | 4,680,562 KB | ✓ extracted | `doc_tpcds_testcase_mariadb_storage.log` |
| MariaDB | 3 | ~14 G | — | ~ proposed | linear from SF=1 |
| MariaDB | 10 | ~50 G | — | ~ proposed | linear from SF=1 |
| MariaDB | 30 | ~140 G | — | ~ proposed | linear from SF=1 |
| MariaDB | 100 | ~450 G | — | ~ proposed | linear from SF=1 |
| MySQL | 1 | 8.1 G | 8,487,723 KB | ✓ extracted | `doc_tpcds_testcase_mysql_storage.log` |
| MySQL | 3 | ~25 G | — | ~ proposed | linear from SF=1 |
| MySQL | 10 | 8.1 G ⚠ | 8,289 MB | ✓ extracted, anomalous | `test_tpcds_testcase_mysql_3.log` — same size as SF=1; likely a reused/non-wiped volume |
| MySQL | 30 | ~250 G | — | ~ proposed | linear from SF=1 |
| MySQL | 100 | ~800 G | — | ~ proposed | linear from SF=1 |

---

## YCSB

| DBMS | SF | volume\_used | datadisk | Status | Source |
|------|----|-------------|---------|--------|--------|
| PostgreSQL | 1 | 2.4 G | 2,390–2,392 MB | ✓ extracted | `doc_ycsb_testcase_storage.log`, `test_ycsb_testcase_postgresql_1/2.log` |
| PostgreSQL | 3 | ~8–10 G | 7,092–10,402 MB | ✓ extracted (datadisk only) | `doc_ycsb_testcase_monitoring.log` (values span benchmarking run) |
| PostgreSQL | 10 | ~23 G | 23,344–23,566 MB | ✓ extracted (datadisk only) | `doc_ycsb_testcase_b/c/d/e/f.log` |
| MariaDB | 1 | 1.8 G | 1,770–1,794 MB | ✓ extracted | `test_ycsb_testcase_mariadb_1/2/3/4/5.log` |
| MySQL | 1 | 36–48 G ⚠ | — | ✓ extracted, likely contaminated | `test_ycsb_testcase_mysql_2/3/4/5.log` — volume grew across tests without wipe; **clean-load estimate: 3–5 G** |
| CockroachDB | 1 | 1.9 G | 705,151 KB (full-disk) | ✓ extracted (`volume_used`) | `doc_ycsb_cockroachdb_2.log` — `datadisk` is the entire cluster disk (~705 GB); use `volume_used` |
| CockroachDB | 10 | — (full-disk 687 G) | — | ✓ extracted, full-disk only | `doc_ycsb_cockroachdb_3.log` — no separate `volume_used` for data only |
| Redis | 1 | ~1 G | — | ✓ extracted | `doc_ycsb_redis_4.log` (1.1 G), `_5.log` (708 M–968 M) |
| Citus | 1 | ~40 M (coord) | — | ✓ extracted (coord only) | `doc_ycsb_citus_2.log` — data on worker nodes |

---

## Benchbase (tpcc benchmark)

| DBMS | SF | volume\_used | datadisk | Status | Source |
|------|----|-------------|---------|--------|--------|
| PostgreSQL | 1 | ~330 MB | 330 MB | ✓ extracted | `test_benchbase_load/run_postgresql.log` |
| PostgreSQL | 16 | 4.2–5.2 G | 4,307–5,231 MB | ✓ extracted (datadisk only) | `doc_benchbase_testcase_full.log`, `doc_benchbase_testcase_newconn.log` |
| MariaDB | 16 | 1.9–2.3 G | — | ✓ extracted | `test_benchbase_testcase_mariadb_2/4.log` |
| MySQL | 16 | 11 G | 11,132–11,256 MB | ✓ extracted | `test_benchbase_testcase_mysql_2/4.log` |
| CockroachDB | 16 | — (full-disk 687 G) | 705,546 KB | ✓ extracted, full-disk | `doc_benchbase_cockroachdb_1.log` — `datadisk` is entire cluster node disk |
| CockroachDB | 128 | 9.5–12 G | 712,955–715,302 KB | ✓ extracted (`volume_used`) | `doc_benchbase_cockroachdb_3.log` |
| Citus | 128 | 6.3–12.7 G (per worker) | — | ✓ extracted | `doc_benchbase_citus_2/3.log` |

---

## HammerDB (TPC-C / warehouses)

| DBMS | SF (warehouses) | volume\_used | datadisk | Status | Source |
|------|----------------|-------------|---------|--------|--------|
| PostgreSQL | 1 | ~280 MB | 280 MB | ✓ extracted | `test_hammerdb_load_postgresql.log` |
| PostgreSQL | 16 | 3.3–4.8 G | — | ✓ extracted | `test_hammerdb_testcase_postgresql_2/3.log` |
| MariaDB | 16 | 1.7–1.9 G | — | ✓ extracted | `test_hammerdb_testcase_mariadb_2/3.log` |
| MySQL | 16 | ~11 G | 10,860–11,531 MB | ✓ extracted | `test_hammerdb_testcase_mysql_1/2/3.log` |
| Citus | 128 | 6.1–24.3 G (per worker) | — | ✓ extracted | `doc_hammerdb_citus_2.log` |
| Citus | 500 | 12.6–24.3 G (per worker) | — | ✓ extracted | `doc_hammerdb_citus_3.log` |

---

## Anomalies and caveats

| Case | Observed | Issue |
|------|----------|-------|
| MySQL YCSB SF=1 | 36–48 G | Volume grew sequentially across test runs without wipe; not a clean-load measurement. Clean-load estimate: **3–5 G**. |
| MySQL TPC-DS SF=10 | 8.1 G (same as SF=1) | Same size as SF=1 result; likely a non-wiped or reused volume. |
| CockroachDB `datadisk` | 700–715 GB | Reports the full cluster node disk, not just the database. Use `volume_used` for CockroachDB. |
| Citus `volume_used` (coordinator) | 40–104 M | Coordinator holds only metadata; actual table data lives on distributed worker nodes. |
