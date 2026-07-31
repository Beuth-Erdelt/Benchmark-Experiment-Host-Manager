# Loader for TPC-H data into MySQL

Loads pre-generated TPC-H `.tbl` files into MySQL. The active script (`loader.sh`) uses `mysql LOAD DATA LOCAL INFILE` with per-table `NULLIF` column mappings. The folder also contains `loader-parallel.sh`, which uses `mysqlsh util.import_table` for parallel loading — it is not the active `CMD`. Sets `BEXHOMA_DATABASE=$BEXHOMA_VOLUME` at startup so the target database name is taken from the Bexhoma volume variable rather than `BEXHOMA_DATABASE`.

See [../README.md](../README.md) for the shared TPC-H pipeline design.

## Execution flow (`loader.sh`)

1. Read `BEXHOMA_CHILD` from `/tmp/tpch/BEXHOMA_CHILD`.
2. Determine `destination_raw` path (same logic as the generator).
3. No multi-tenant handling — this loader does not support it (PostgreSQL is the only one that does).
4. If `BEXHOMA_SYNCH_LOAD=1`: sync on the job counter `bexhoma-loader-podcount-job-<CONNECTION>-<EXPERIMENT>`,
   then the round counter `bexhoma-loader-podcount-round-<CONFIGURATION>-<EXPERIMENT>` (always
   initialized by Python, even for a single loader entry; only meaningful when the SUT
   configuration has more than one parallel loader entry — see `bexhoma/CLAUDE.md`).
5. Loop over `.tbl` files; skip `nation` and `region` for pods > 1 in non-tenant mode.
6. If `TPCH_TABLE` is set: only load that table.
7. Execute `mysql LOAD DATA LOCAL INFILE` per table with column mapping via `NULLIF`; retry on known transient errors.
8. Emit `BEXHOMA_DURATION`, `BEXHOMA_START`, `BEXHOMA_END`.

`loader-parallel.sh` collects all partitions from all pods into one loader (pod 1 only)
via `mysqlsh util.import_table`; it is inactive and kept for reference.

## Environment variables

### Scaling and parallelism

* `SF`: Scale factor — used to locate the correct data subdirectory. Default: `1`.
* `BEXHOMA_NUM_PODS`: Total number of loader pods. Default: `4`.
* `BEXHOMA_CHILD`: Pod index (1-based). Overwritten at runtime from `/tmp/tpch/BEXHOMA_CHILD`. Default: `1`.
* `BEXHOMA_RNGSEED`: Not used by this loader. Default: `123`.

### Target DBMS connection

* `BEXHOMA_HOST`: MySQL hostname. Default: `www.example.com`.
* `BEXHOMA_PORT`: MySQL port. Default: `3306`.
* `BEXHOMA_USER`: MySQL username. Default: `root`.
* `BEXHOMA_PASSWORD`: MySQL password. Default: `root`.
* `BEXHOMA_DATABASE`: Default database name — overridden at startup by `BEXHOMA_VOLUME`. Default: `demo`.
* `BEXHOMA_VOLUME`: Actual target database name. The loader script sets `BEXHOMA_DATABASE=$BEXHOMA_VOLUME` at startup. Default: `""`.
* `BEXHOMA_URL`, `BEXHOMA_JAR`, `BEXHOMA_DRIVER`: Not used by this loader — declared for compatibility.

### Bexhoma experiment identity

* `BEXHOMA_CONNECTION`: Logical connection name — used to address the Redis synchronisation counter. Default: `mysql`.
* `BEXHOMA_EXPERIMENT`: Experiment ID. Default: `12345`.
* `BEXHOMA_EXPERIMENT_RUN`: Run counter within the experiment. Default: `1`.
* `BEXHOMA_CONFIGURATION`: Configuration label echoed in log output.
* `BEXHOMA_CLIENT`: Client index echoed in log output. Default: `1`.

### Data storage and loading control

* `STORE_RAW_DATA`: `0` = read data from `/tmp/tpch/`; `1` = read from `/data/tpch/`. Default: `0`.
* `BEXHOMA_SYNCH_LOAD`: `1` = wait on Redis counter `bexhoma-loader-podcount-<CONNECTION>-<EXPERIMENT>` until all loader pods have checked in before starting. Default: `0`.
* `TPCH_TABLE`: When set to a table name only that table is loaded; all others are skipped. Default: `""`.
* `MYSQL_LOADING_FROM`: Must be `LOCAL` to use `LOAD DATA LOCAL INFILE`. Default: `LOCAL`.
* `MYSQL_LOADING_THREADS`: Thread count for parallel loading — only used by `loader-parallel.sh`. Default: `8`.
* `MYSQL_LOADING_PARALLEL`: `1` = use parallel multi-pod loading in `loader-parallel.sh` — only used by `loader-parallel.sh`; `loader.sh` ignores this variable. Default: `0`.
