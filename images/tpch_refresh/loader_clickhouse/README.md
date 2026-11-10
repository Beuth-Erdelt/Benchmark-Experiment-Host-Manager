# TPC-H Refresh Loader — ClickHouse

Applies TPC-H RF1 (INSERT) and RF2 (DELETE) operations to a ClickHouse database, single node
or cluster. Reads pre-generated update files from `/data/tpch-refresh/SF<SF>/` on the PVC.
Runs as the main container (`benchmark_run=2`) of the refresh benchmarker job, in parallel
with the query-stream benchmarker (`benchmark_run=1`).

See [images/tpch_refresh/README.md](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/tpch_refresh/README.md) for the shared refresh-stream pipeline design.

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `SF` | `1` | TPC-H scaling factor |
| `TPCH_REFRESH_STREAMS` | `1` | Number of RF1+RF2 pairs to apply |
| `TPCH_REFRESH_STREAM_OFFSET` | `0` | Start from set `OFFSET+1` |
| `STORE_RAW_DATA` | `1` | `1` = read from `/data/tpch-refresh/SF<SF>/`; `0` = `/tmp/...` |
| `BEXHOMA_HOST` | `www.example.com` | ClickHouse host |
| `BEXHOMA_PORT` | `9091` | HTTP port of the service (JDBC; not used here) |
| `CLICKHOUSE_PORT` | `9000` | Native port used by `clickhouse-client` |
| `BEXHOMA_DATABASE` | `default` | Database |
| `BEXHOMA_CLICKHOUSE_CLUSTER` | empty | Name of the cluster (`ClickHouseCluster`); empty for a single node |
| `BEXHOMA_CONNECTION` | `clickhouse` | Connection name (Redis counter key) |
| `BEXHOMA_EXPERIMENT` | `12345` | Experiment identifier |
| `BEXHOMA_EXPERIMENT_RUN` | `1` | Run number within experiment |
| `BEXHOMA_CLIENT` | `1` | Client round number |
| `BEXHOMA_BENCHMARK_RUN` | `2` | Parallel benchmark index (2 = refresh stream) |

## Execution flow

1. Compute `FIRST_SET = OFFSET+1`, `LAST_SET = OFFSET+STREAMS`.
2. Sync with the query stream through the job and round counters in Redis, as the other refresh loaders do.
3. For each set K:
   * **RF1**: `INSERT INTO orders|lineitem FORMAT CSV` (delimiter `|`) from `orders.tbl.uK` and `lineitem.tbl.uK`.
     On a cluster the tables are Distributed and send the rows to the shards before the INSERT returns.
   * **RF2**: the order keys of `delete.K` in chunks of 10000: `DELETE FROM lineitem WHERE l_orderkey IN (...)`,
     then the same on `orders` (lightweight delete, waits for all replicas). With `BEXHOMA_CLICKHOUSE_CLUSTER`
     set, a Distributed table cannot be deleted from, so the DELETE runs on `lineitem_local` and `orders_local`
     on every shard: the loader reads the hosts of cluster `<name>` from `system.clusters`
     and connects to each (the coordinator has only the Distributed tables, so `ON CLUSTER` does not work).
4. Print `BEXHOMA_DURATION`, `BEXHOMA_START` and `BEXHOMA_END`.

## Failure

Any failing statement is reported and the container exits with 1. So does a cluster whose hosts cannot be read
from `system.clusters` (query failed or no rows): RF2 would delete nothing. The loader still runs the stream to the
end in that case, so the query stream is not left waiting. The job has `backoffLimit: 0`: ClickHouse has no
primary key to refuse a second RF1, so a retry would insert the rows twice.
