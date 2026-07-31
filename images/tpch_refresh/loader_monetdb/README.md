# TPC-H Refresh Loader — MonetDB

Applies TPC-H RF1 (INSERT) and RF2 (DELETE) operations to a MonetDB database.
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
| `BEXHOMA_HOST` | `www.example.com` | MonetDB host |
| `BEXHOMA_PORT` | `3306` | MonetDB port |
| `BEXHOMA_USER` | `monetdb` | MonetDB user — written to the `.monetdb` credentials file |
| `BEXHOMA_PASSWORD` | `monetdb` | MonetDB password — written to the `.monetdb` credentials file |
| `BEXHOMA_DATABASE` | `tpch` | Target database |
| `BEXHOMA_CONNECTION` | `monetdb` | Connection name (Redis counter key) |
| `BEXHOMA_EXPERIMENT` | `12345` | Experiment identifier |
| `BEXHOMA_EXPERIMENT_RUN` | `1` | Run number within experiment |
| `BEXHOMA_CLIENT` | `1` | Client round number |
| `BEXHOMA_BENCHMARK_RUN` | `2` | Parallel benchmark index (2 = refresh stream) |

## Execution flow

1. Determine `destination_raw` (same logic as the generator); write the `.monetdb`
   credentials file.
2. Compute `FIRST_SET = OFFSET+1`, `LAST_SET = OFFSET+STREAMS`.
3. Sync: decrement **job counter** `bexhoma-benchmarker-podcount-job-<CONNECTION>-<EXPERIMENT>`,
   poll until ≤ 0.
4. Sync: decrement **round counter**
   `bexhoma-benchmarker-podcount-round-<EXPERIMENT_RUN>-<CLIENT>-<CONFIGURATION>-<EXPERIMENT>`,
   poll until ≤ 0. This ensures the refresh stream starts at the same moment as
   the parallel query stream (`benchmark_run=1`).
5. For each set K from `FIRST_SET` to `LAST_SET`:
   - RF1: count lines, then `mclient -s "COPY N RECORDS INTO orders/lineitem FROM STDIN ..."` piped from `orders.tbl.uK` / `lineitem.tbl.uK`
   - RF2: pipe `CREATE TEMPORARY TABLE`, `COPY N RECORDS INTO ... FROM STDIN`, the contents of `delete.K`,
     the two `DELETE FROM lineitem/orders WHERE ...` statements, and `DROP TABLE` as one `mclient` session —
     `mclient` reads the N data records from stdin immediately after `COPY`, then continues reading SQL
     from the same stdin stream, so the temporary table persists across statements.
6. Emit `BEXHOMA_DURATION`, `BEXHOMA_START`, `BEXHOMA_END`.
