# TPC-H Refresh Loader — MySQL

Applies TPC-H RF1 (INSERT) and RF2 (DELETE) operations to a MySQL database.
Reads pre-generated update files from `/data/tpch-refresh/SF<SF>/` on the PVC.
Runs as the main container (`benchmark_run=2`) of the refresh benchmarker job,
in parallel with the query-stream benchmarker (`benchmark_run=1`).

See [../README.md](../README.md) for the shared refresh-stream pipeline design.

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `SF` | `1` | TPC-H scaling factor |
| `TPCH_REFRESH_STREAMS` | `1` | Number of RF1+RF2 pairs to apply |
| `TPCH_REFRESH_STREAM_OFFSET` | `0` | Start from set `OFFSET+1` |
| `STORE_RAW_DATA` | `1` | `1` = read from `/data/tpch-refresh/SF<SF>/`; `0` = `/tmp/...` |
| `BEXHOMA_HOST` | `www.example.com` | MySQL host |
| `BEXHOMA_PORT` | `3306` | MySQL port |
| `BEXHOMA_USER` | `root` | MySQL user |
| `BEXHOMA_PASSWORD` | `root` | MySQL password |
| `BEXHOMA_VOLUME` | `tpch` | Database name (overrides `BEXHOMA_DATABASE` at runtime) |
| `BEXHOMA_CONNECTION` | `mysql` | Connection name (Redis counter key) |
| `BEXHOMA_EXPERIMENT` | `12345` | Experiment identifier |
| `BEXHOMA_EXPERIMENT_RUN` | `1` | Run number within experiment |
| `BEXHOMA_CLIENT` | `1` | Client round number |
| `BEXHOMA_BENCHMARK_RUN` | `2` | Parallel benchmark index (2 = refresh stream) |

## Execution flow

1. Set `BEXHOMA_DATABASE=$BEXHOMA_VOLUME`.
2. Compute `FIRST_SET = OFFSET+1`, `LAST_SET = OFFSET+STREAMS`; determine `destination_raw`.
3. Sync: decrement **job counter** `bexhoma-benchmarker-podcount-job-<CONNECTION>-<EXPERIMENT>`,
   poll until ≤ 0.
4. Sync: decrement **round counter**
   `bexhoma-benchmarker-podcount-round-<EXPERIMENT_RUN>-<CLIENT>-<CONFIGURATION>-<EXPERIMENT>`,
   poll until ≤ 0. This ensures the refresh stream starts at the same moment as
   the parallel query stream (`benchmark_run=1`).
5. For each set K from `FIRST_SET` to `LAST_SET`:
   - RF1: `LOAD DATA LOCAL INFILE` (column-mapped with `NULLIF`) for `orders.tbl.uK` and `lineitem.tbl.uK`
   - RF2: create temp table, load `delete.K`, bulk `DELETE l FROM lineitem l WHERE ...` + same for orders, drop temp table
6. Emit `BEXHOMA_DURATION`, `BEXHOMA_START`, `BEXHOMA_END`.
