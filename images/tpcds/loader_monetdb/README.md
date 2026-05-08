# Loader for TPC-DS data into MonetDB

Loads pre-generated TPC-DS `.dat` files into MonetDB using `mclient COPY ... FROM STDIN`. Writes a `.monetdb` credentials file before loading. Retries on worker/producer thread errors.

## Environment variables

### Scaling and parallelism

* `SF`: Scale factor — used to locate the correct data subdirectory. Default: `1`.
* `BEXHOMA_NUM_PODS`: Total number of loader pods. Default: `4`.
* `BEXHOMA_CHILD`: Pod index (1-based). Overwritten at runtime from `/tmp/tpcds/BEXHOMA_CHILD`. Default: `1`.
* `BEXHOMA_RNGSEED`: Not used by this loader. Default: `123`.

### Target DBMS connection

* `BEXHOMA_HOST`: MonetDB hostname. Default: `www.example.com`.
* `BEXHOMA_PORT`: MonetDB port. Default: `3306`.
* `BEXHOMA_USER`: MonetDB username — written to the `.monetdb` credentials file. Default: `root`.
* `BEXHOMA_PASSWORD`: MonetDB password — written to the `.monetdb` credentials file. Default: `root`.
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
