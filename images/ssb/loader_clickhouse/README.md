# Loader for SSB data into ClickHouse

Loads the `.tbl` files of its pod's folder into ClickHouse via `clickhouse-client` over the
native protocol. Only the client of the base image is used. See
[images/ssb/README.md](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/ssb/README.md)
for the data layout.

## Execution flow (`loader.sh`)

1. Read the child index from `/tmp/ssb/BEXHOMA_CHILD` (written by the generator of the same pod).
2. Determine the folder like the generator: `/data/ssb/SF<SF>[/<N>/<child>]`, or `.../flat[/<N>/<child>]` with `SSB_SCHEMA_VARIANT=flat`.
3. If `BEXHOMA_SYNCH_LOAD=1`: wait on the job counter and the round counter.
4. For each `*tbl*` file: table = file name without `.tbl*` (`date.tbl` -> `dates`), skipped if `SSB_TABLE` names another table; `INSERT INTO <table> FORMAT CSV` with `--format_csv_delimiter='|' --format_csv_allow_double_quotes=0`. No retry: a failed INSERT may have written some blocks already.
5. Emit `BEXHOMA_DURATION`, `BEXHOMA_START`, `BEXHOMA_END`; exit 1 if a table failed.

## Environment variables

* `SF`, `BEXHOMA_NUM_PODS`, `STORE_RAW_DATA`, `SSB_SCHEMA_VARIANT`: locate the folder (same values as the generator).
* `SSB_TABLE`: load only this table. Default: `""` (all).
* `BEXHOMA_HOST`, `BEXHOMA_DATABASE`: connection (set by bexhoma).
* `CLICKHOUSE_PORT`: native port of the SUT (`BEXHOMA_PORT` is the HTTP/JDBC port). Default: `9000`.
* `BEXHOMA_SYNCH_LOAD`: `1` = wait for all loader pods of the job and round. Default: `0` (bexhoma sets `1`).
* `BEXHOMA_CONNECTION`, `BEXHOMA_EXPERIMENT`, `BEXHOMA_EXPERIMENT_RUN`, `BEXHOMA_CONFIGURATION`, `BEXHOMA_DATA_JOB`: address the Redis counters.
