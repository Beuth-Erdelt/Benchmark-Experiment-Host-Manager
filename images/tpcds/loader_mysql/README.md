# Loader for TPC-DS data into MySQL

Loads pre-generated TPC-DS `.dat` files into MySQL. The active script (`loader.sh`) uses `mysql LOAD DATA LOCAL INFILE` with per-table `NULLIF` column mappings. The folder also contains `loader-parallel.sh`, which uses `mysqlsh util.import_table` for parallel loading — it is not the active `CMD`. Unlike the TPC-H MySQL loader, this loader does not override `BEXHOMA_DATABASE` with a volume variable.

## Environment variables

### Scaling and parallelism

* `SF`: Scale factor — used to locate the correct data subdirectory. Default: `1`.
* `BEXHOMA_NUM_PODS`: Total number of loader pods. Default: `4`.
* `BEXHOMA_CHILD`: Pod index (1-based). Overwritten at runtime from `/tmp/tpcds/BEXHOMA_CHILD`. Default: `1`.
* `BEXHOMA_RNGSEED`: Not used by this loader. Default: `123`.

### Target DBMS connection

* `BEXHOMA_HOST`: MySQL hostname. Default: `www.example.com`.
* `BEXHOMA_PORT`: MySQL port. Default: `3306`.
* `BEXHOMA_USER`: MySQL username. Default: `root`.
* `BEXHOMA_PASSWORD`: MySQL password. Default: `root`.
* `BEXHOMA_DATABASE`: Target database name. Default: `demo`.
* `BEXHOMA_URL`, `BEXHOMA_JAR`, `BEXHOMA_DRIVER`: Not used by this loader — declared for compatibility.

### Bexhoma experiment identity

* `BEXHOMA_CONNECTION`: Logical connection name — used to address the Redis synchronisation counter. Default: `mysql`.
* `BEXHOMA_EXPERIMENT`: Experiment ID. Default: `12345`.
* `BEXHOMA_EXPERIMENT_RUN`: Run counter within the experiment. Default: `1`.
* `BEXHOMA_CONFIGURATION`: Configuration label echoed in log output.
* `BEXHOMA_CLIENT`: Client index echoed in log output. Default: `1`.

### Data storage and loading control

* `STORE_RAW_DATA`: `0` = read data from `/tmp/tpcds/`; `1` = read from `/data/tpcds/`. Default: `0`.
* `BEXHOMA_SYNCH_LOAD`: `1` = wait on Redis counter `bexhoma-loader-podcount-<CONNECTION>-<EXPERIMENT>` until all loader pods have checked in before starting. Default: `0`.
* `TPCDS_TABLE`: When set to a table name only that table is loaded; all others are skipped. Default: `""`.
* `MYSQL_LOADING_FROM`: Must be `LOCAL` to use `LOAD DATA LOCAL INFILE`. Default: `LOCAL`.
* `MYSQL_LOADING_THREADS`: Thread count for parallel loading — only used by `loader-parallel.sh`. Default: `8`.
* `MYSQL_LOADING_PARALLEL`: `1` = use parallel multi-pod loading in `loader-parallel.sh` — only used by `loader-parallel.sh`; `loader.sh` ignores this variable. Default: `0`.
