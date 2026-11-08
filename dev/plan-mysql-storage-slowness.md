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
