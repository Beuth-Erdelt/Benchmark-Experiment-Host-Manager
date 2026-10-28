# Loader for SSB data into MonetDB

Loads the `.tbl` files of its pod's folder into MonetDB via `mclient COPY ... FROM STDIN`. See
[images/ssb/README.md](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/ssb/README.md)
for the data layout.

## Execution flow (`loader.sh`)

1. Read the child index from `/tmp/ssb/BEXHOMA_CHILD` (written by the generator of the same pod).
2. Determine the folder like the generator: `/data/ssb/SF<SF>[/<N>/<child>]`, or `.../flat[/<N>/<child>]` with `SSB_SCHEMA_VARIANT=flat`.
3. Write the credentials to `/tmp/ssb/.monetdb` (`DOTMONETDBFILE`), outside the shared data folder.
4. If `BEXHOMA_SYNCH_LOAD=1`: wait on the job counter and the round counter.
5. For each `*tbl*` file: table = file name without `.tbl*` (`date.tbl` -> `dates`), skipped if `SSB_TABLE` names another table; `COPY <lines> RECORDS INTO <table> FROM STDIN USING DELIMITERS '|' NULL AS ''`. The answer must report `<lines> affected rows`; ROLLBACK, thread start errors and empty login challenges are retried (at most 10 attempts).
6. Emit `BEXHOMA_DURATION`, `BEXHOMA_START`, `BEXHOMA_END`; exit 1 if a table failed.

## Environment variables

* `SF`, `BEXHOMA_NUM_PODS`, `STORE_RAW_DATA`, `SSB_SCHEMA_VARIANT`: locate the folder (same values as the generator).
* `SSB_TABLE`: load only this table. Default: `""` (all).
* `BEXHOMA_HOST`, `BEXHOMA_PORT`, `BEXHOMA_DATABASE`: connection (set by bexhoma).
* `BEXHOMA_SYNCH_LOAD`: `1` = wait for all loader pods of the job and round. Default: `0` (bexhoma sets `1`).
* `BEXHOMA_CONNECTION`, `BEXHOMA_EXPERIMENT`, `BEXHOMA_EXPERIMENT_RUN`, `BEXHOMA_CONFIGURATION`, `BEXHOMA_DATA_JOB`: address the Redis counters.
