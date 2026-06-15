# TPC-H Refresh Loader — PostgreSQL

Applies TPC-H RF1 (INSERT) and RF2 (DELETE) operations to a PostgreSQL database.
Reads pre-generated update files from `/data/tpch-refresh/SF<SF>/` on the PVC.
Runs as the main container (`benchmark_run=2`) of the refresh benchmarker job,
in parallel with the query-stream benchmarker (`benchmark_run=1`).

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `SF` | `1` | TPC-H scaling factor |
| `TPCH_REFRESH_STREAMS` | `1` | Number of RF1+RF2 pairs to apply |
| `TPCH_REFRESH_STREAM_OFFSET` | `0` | Start from set `OFFSET+1` |
| `STORE_RAW_DATA` | `1` | `1` = read from `/data/tpch-refresh/SF<SF>/`; `0` = `/tmp/...` |
| `BEXHOMA_HOST` | `www.example.com` | PostgreSQL host |
| `BEXHOMA_PORT` | `5432` | PostgreSQL port |
| `BEXHOMA_USER` | `postgres` | PostgreSQL user |
| `BEXHOMA_PASSWORD` | `postgres` | PostgreSQL password |
| `BEXHOMA_DATABASE` | `tpch` | Target database |
| `BEXHOMA_SCHEMA` | `public` | Target schema |
| `BEXHOMA_CONNECTION` | `postgresql` | Connection name (Redis counter key) |
| `BEXHOMA_EXPERIMENT` | `12345` | Experiment identifier |
| `BEXHOMA_EXPERIMENT_RUN` | `1` | Run number within experiment |
| `BEXHOMA_CLIENT` | `1` | Client round number |
| `BEXHOMA_BENCHMARK_RUN` | `2` | Parallel benchmark index (2 = refresh stream) |

## Execution flow

1. Sync with benchmarker job counter and round counter via Redis.
2. For each set K from `OFFSET+1` to `OFFSET+STREAMS`:
   - RF1: `\COPY orders FROM orders.tbl.uK` then `\COPY lineitem FROM lineitem.tbl.uK`
   - RF2: bulk DELETE lineitem and orders rows whose orderkeys are listed in `delete.K`
3. Emit `BEXHOMA_DURATION`, `BEXHOMA_START`, `BEXHOMA_END`.
