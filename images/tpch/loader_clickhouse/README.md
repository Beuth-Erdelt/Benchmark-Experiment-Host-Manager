# Loader for TPC-H data into ClickHouse

Loads pre-generated TPC-H `.tbl` files into ClickHouse using `clickhouse-client` `INSERT INTO <table> FORMAT CSV` over the native protocol (port 9000). Used for `ClickHouse` and `ClickHouseCluster`; in the cluster the target tables are Distributed tables on the coordinator, which pass the rows on to the shards before the `INSERT` returns (`distributed_foreground_insert=1`).

The image is based on `clickhouse/clickhouse-server` (same version as the SUT templates) for its client; the server does not start.

See [images/tpch/README.md](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/tpch/README.md) for the shared TPC-H pipeline design.

## Execution flow (`loader.sh`)

1. Read `BEXHOMA_CHILD` from `/tmp/tpch/BEXHOMA_CHILD`.
2. Determine `destination_raw` path (same logic as the generator).
3. No multi-tenant handling — this loader does not support it.
4. If `BEXHOMA_SYNCH_LOAD=1`: sync on the job counter `bexhoma-loader-podcount-job-<CONNECTION>-<EXPERIMENT>`,
   then the round counter `bexhoma-loader-podcount-round-<CONFIGURATION>-<EXPERIMENT>`.
5. Loop over `.tbl` files; skip `nation` and `region` for pods > 1.
6. If `TPCH_TABLE` is set: only load that table.
7. Execute `clickhouse-client ... --query "INSERT INTO <table> FORMAT CSV" < <file>` per file with `format_csv_delimiter='|'` and `format_csv_allow_double_quotes=0`. The generator removes the trailing `|` (`TRANSFORM_RAW_DATA=1`). A failed `INSERT` is not retried (it may have written some blocks already); the loader exits with code 1 and lists the failed tables.
8. Emit `BEXHOMA_DURATION`, `BEXHOMA_START`, `BEXHOMA_END`.

## Environment variables

### Scaling and parallelism

* `SF`: Scale factor — used to locate the correct data subdirectory. Default: `1`.
* `BEXHOMA_NUM_PODS`: Total number of loader pods. Default: `4`.
* `BEXHOMA_CHILD`: Pod index (1-based). Overwritten at runtime from `/tmp/tpch/BEXHOMA_CHILD`. Default: `1`.
* `BEXHOMA_RNGSEED`: Not used by this loader. Default: `123`.

### Target DBMS connection

* `BEXHOMA_HOST`: ClickHouse hostname (the SUT service). Default: `www.example.com`.
* `CLICKHOUSE_PORT`: Native protocol port of the SUT service. Default: `9000`.
* `BEXHOMA_DATABASE`: Target database name. Default: `default`.
* `BEXHOMA_PORT`, `BEXHOMA_URL`, `BEXHOMA_JAR`, `BEXHOMA_DRIVER`, `BEXHOMA_USER`, `BEXHOMA_PASSWORD`: Not used by this loader (`BEXHOMA_PORT` is the HTTP port for JDBC; the user is `default` without password) — declared for compatibility.

### Bexhoma experiment identity

* `BEXHOMA_CONNECTION`: Logical connection name — used to address the Redis synchronisation counter. Default: `clickhouse`.
* `BEXHOMA_EXPERIMENT`: Experiment ID. Default: `12345`.
* `BEXHOMA_EXPERIMENT_RUN`: Run counter within the experiment. Default: `1`.
* `BEXHOMA_CONFIGURATION`: Configuration label echoed in log output.
* `BEXHOMA_CLIENT`: Client index echoed in log output. Default: `1`.

### Data storage and loading control

* `STORE_RAW_DATA`: `0` = read data from `/tmp/tpch/`; `1` = read from `/data/tpch/`. Default: `0`.
* `BEXHOMA_SYNCH_LOAD`: `1` = wait on the Redis counters until all loader pods have checked in before starting. Default: `0`.
* `TPCH_TABLE`: When set to a table name only that table is loaded; all others are skipped. Default: `""`.
