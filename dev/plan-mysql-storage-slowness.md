# Plan: why MySQL on persistent storage is so slow (TPC-H, TPC-DS, SF 10)

Status: not started (2026-11-08). Evidence below; nothing implemented.

## Evidence

| Run (MySQL, SF 10) | Storage | Duration |
|---|---|---|
| TPC-H `docs_tpch_mysql_ramdisk` | ramdisk | 1863 s |
| TPC-H `docs_tpch_mysql_monitoring` | ephemeral | 4927 s |
| TPC-H `docs_tpch_mysql_storage` | nvme | 22155 s; Q15 hit the 1200 s timeout in all 6 connections (about 164 s on ramdisk and ephemeral) |
| TPC-DS `docs_tpcds_mysql_storage` | nvme | more than 22 h, experiment 1794055327, kept for inspection, result not committed |

The storage runs overlapped with other runs on the cluster, so the numbers are not like for like.
The nvme TPC-H run's own log is kept as `docs_tpch_mysql_storage.parallel-run.log` in the scratchpad.

## Measured on the TPC-DS storage run before it was stopped (2026-11-08, second SUT, up 5 h)

- The `nvme` volume is `/dev/rbd3`, a Ceph RBD block device (network storage), not a local disk.
- `innodb_buffer_pool_size` was 8G. `Innodb_data_read` was 298 GB (18 M physical reads) in 5 h, so the volume was read about 16 MB/s on average.
- `Created_tmp_disk_tables` 50 of 220 tmp tables, `Created_tmp_files` 4634, `Sort_merge_passes` 9728. `#innodb_temp` on the volume held 6.3 GB, `/mysqltmp` was empty.
- `tmp_table_size` 16M and `temptable_max_ram` 1G were at their defaults.
- Raw output: `mysql_status.txt`, `benchmarker.log` and the log of the run, kept in the scratchpad (`tpcds_storage_run/`). The loaded volume `bexhoma-storage-my-nvme-tpcds-10` and the result folder `C:\data\benchmarks\1794055327` were kept.

## Main hypothesis: internal temporary tables go to disk

Both workloads only read, so the slowdown should not come from writes to the tables.
The defaults are `temptable_max_ram` = 1G and `tmp_table_size` = 16M (the template has `--tmp-table-size` commented out).
An internal temp table above that limit becomes an on-disk InnoDB table (session temp tablespace under the data directory, i.e. on the persistent volume).
Sort files go to `--tmpdir=/mysqltmp`, a RAM-backed emptyDir.
So a query that builds large intermediate results (Q15 twice over the CTE, most of TPC-DS) writes and reads them on the volume.
On ramdisk the data directory is memory, which would explain why it is fast there.
Seen before: `Created_tmp_disk_tables` was 49 and `Created_tmp_files` 7187 on the SF 10 monitoring run, and TPC-DS Q31 failed with `Table './mysqltmp/#sql…' doesn't exist`.

Checks:
1. Read `Created_tmp_tables`, `Created_tmp_disk_tables`, `Created_tmp_files` and `Select_full_join` before and after a single query (Q15 first), and the size of `#innodb_temp` in the data directory.
2. Repeat on the storage class with `--set deployment[bexhoma-deployment-mysql].container[dbms].temptable_max_ram=32G` plus `tmp_table_size=32G` and `max_heap_table_size=32G` (as in the SF 3 monitoring run).
3. If the disk tables remain, point `innodb_temp_tablespaces_dir` at the tmpfs, or switch `internal_tmp_mem_storage_engine`.

## Quick check of the temp-table hypothesis (planned 2026-11-08)

Reuse the loaded TPC-H SF 10 volume `bexhoma-storage-mysql-nvme-tpch-10` (no `-rsr`, no reload) and run only the queries that build large intermediate results
(`-xaq 15,18,21,9,13`, Q15 is the known timeout), one client, one repetition, `-ma` for the MySQL counters
(`created_tmp_disk_tables`, `created_tmp_files`, `sort_merge_passes`, `innodb_buffer_pool_reads`), nothing else on the cluster, three runs one after another:

| Run | `--set deployment[bexhoma-deployment-mysql].container[dbms].` | tests |
|---|---|---|
| A | none (`temptable_max_ram` 1G, `tmp_table_size` 16M) | baseline: Q15 time, temp counters |
| B | `temptable_max_ram=32G`, `tmp_table_size=32G`, `max_heap_table_size=32G` | temp tables stay in RAM? |
| C | B and `innodb_buffer_pool_size=64G` | separates temp tables from re-reading data from the volume |

All with `-lr 128Gi -rr 128Gi` and the `mysqltmp` volume at 64Gi. Reading: A vs B big speedup and the disk counter near 0 means temp tables are the cause;
only C faster means re-reading data; neither means the volume itself (step 6, `fio`). The TPC-DS Q31 temp-table error should disappear in B and C.
Output goes to the scratchpad, not to `logs_tests/`.

### Result of the quick check (run 2026-11-08, TPC-H SF 10, one client, MySQL 9.7.2, nothing else on the cluster)

| Query | A: defaults, buffer pool 8G | B: temp tables 32G | C: B and buffer pool 64G |
|---|---|---|---|
| Q9 | 893 s | 960 s | 471 s |
| Q13 | 54 s | 56 s | 59 s |
| Q15 | timeout (1200 s) | timeout (1200 s) | 194 s |
| Q18 | 127 s | 135 s | 14 s |
| Q21 | 301 s | 300 s | 35 s |
| whole run | 2952 s | 3025 s | 1128 s |

B had the settings (`temptable_max_ram=32G`, `tmp_table_size=32G`, checked in its log) and was not faster than A, so the temp-table hypothesis is **not supported**.
Only the larger buffer pool helped (Q18 9x, Q21 8.5x, Q15 now passes), so the slowness is mainly reading the data again and again from the Ceph RBD volume with an 8G buffer pool.
Caveats: A ran first and C last (a warm Ceph cache could help C; A and B ran in that order and are equal), one run each, the `-ma` metrics of the three runs show no temp-table counters
(the shown ratios are cumulative and identical), and the temp-table counters were not read directly.
Next: rerun C first (or twice) to rule out the cache order, then 32G as buffer pool, then decide the buffer pool of the storage examples (`--set ...innodb_buffer_pool_size=64G`).
Raw logs: scratchpad `tmpcheck/`.

### Second set (2026-11-08 evening, same set-up, run alone)

| Query | C: temp 32G, buffer pool 64G | C2: repeat of C | D: temp 32G, buffer pool 32G | E: temp defaults, buffer pool 64G |
|---|---|---|---|---|
| Q9 | 471 s | 394 s | 393 s | 438 s |
| Q13 | 59 s | 53 s | 51 s | 54 s |
| Q15 | 194 s | 178 s | 178 s | 198 s |
| Q18 | 14 s | 13 s | 12 s | 15 s |
| Q21 | 35 s | 39 s | 35 s | 41 s |
| whole run | 1128 s | 1044 s | 1034 s | 1110 s |

- C2 is as fast as C, so the order of the runs (a warm Ceph cache) does not explain the speedup.
- D (32G) is as fast as 64G: the buffer pool has to be larger than the default 8G, but 32G is enough for SF 10.
- E (temp-table defaults) is as fast as C: the temp-table settings are not needed.
- All of C, C2, D and E have 0 FAIL, Q15 passes in about 180-200 s (A and B: timeout).

Conclusion: the slowness of MySQL on the storage runs is the buffer pool of 8G (template default), not temp tables and not the volume as such.
Proposal: `--set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G` in the TPC-H and TPC-DS storage runs (scripts and Example-MySQL.md), then rerun them.
Not tried: 16G, and SF 100. Whether the template default of 8G should rise is a separate decision, it affects every MySQL run.

## Other causes to separate out

4. Run alone: rerun TPC-H storage with nothing else on the cluster (queued after the database-service pair).
5. Buffer pool: the template default is 8G, SF 10 does not fit. Try 64G on the storage run, as the monitoring run does.
6. Volume: short `fio` run on the nvme volume, IOPS and latency, with the hardware benchmark.
7. Storage classes: same TPC-H SF 10, one run at a time, on nvme, ceph and local-hdd, with ephemeral and ramdisk as references.
8. Other DBMS: PostgreSQL and MariaDB on the same nvme volume at SF 10 (existing storage logs are SF 1 or 3).
9. Run `ANALYZE` after the load, and look at the plans of Q15 and of the slowest TPC-DS queries.
10. Look at the kept TPC-DS run: which queries time out, how many rounds it needed.

## Result

If the temp tables are the cause, fix by default in the template or the storage script flags, then re-run the storage examples and update the docs.
If the volume is the cause, document it and keep the storage examples at a smaller scale factor.
