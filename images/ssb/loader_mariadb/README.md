# Loader for SSB data into MariaDB

Loads the `.tbl` files of its pod's folder into MariaDB via `LOAD DATA LOCAL INFILE`. See
[images/ssb/README.md](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/ssb/README.md)
for the data layout. `loader.sh` is the same file as in `loader_mysql`; the images differ in
the client and base image, as the TPC-H loaders of the two DBMS.

## Execution flow (`loader.sh`)

1. Read the child index from `/tmp/ssb/BEXHOMA_CHILD` (written by the generator of the same pod).
2. Determine the folder like the generator: `/data/ssb/SF<SF>[/<N>/<child>]`, or `.../flat[/<N>/<child>]` with `SSB_SCHEMA_VARIANT=flat`.
3. If `BEXHOMA_SYNCH_LOAD=1`: wait on the job counter and the round counter (all loader pods start together).
4. For each `*tbl*` file: table = file name without `.tbl*` (`date.tbl` -> `dates`), skipped if `SSB_TABLE` names another table; `LOAD DATA LOCAL INFILE '<file>' INTO TABLE <database>.<table> FIELDS TERMINATED BY '|'; SELECT ROW_COUNT(); COMMIT;` in one session. The only output line must be the lines of the file. The `COMMIT` is needed because MySQL's load durability (`-xld relaxed`) switches autocommit off.
5. Emit `BEXHOMA_DURATION`, `BEXHOMA_START`, `BEXHOMA_END`; exit 1 if a table failed.

## Environment variables

* `SF`, `BEXHOMA_NUM_PODS`, `STORE_RAW_DATA`, `SSB_SCHEMA_VARIANT`: locate the folder (same values as the generator).
* `SSB_TABLE`: load only this table (`customer`, `supplier`, `part`, `dates`, `lineorder`, `lineorder_flat`). Default: `""` (all).
* `BEXHOMA_HOST`, `BEXHOMA_PORT`, `BEXHOMA_USER`, `BEXHOMA_PASSWORD`: connection (set by bexhoma).
* `BEXHOMA_VOLUME`: the database (`ssb`).
* `MYSQL_CLIENT_OPTIONS`: extra client options; the MySQL job template sets `--skip-ssl`. Default: `""`.
* `BEXHOMA_SYNCH_LOAD`: `1` = wait for all loader pods of the job and round. Default: `0` (bexhoma sets `1`).
* `BEXHOMA_CONNECTION`, `BEXHOMA_EXPERIMENT`, `BEXHOMA_EXPERIMENT_RUN`, `BEXHOMA_CONFIGURATION`, `BEXHOMA_DATA_JOB`: address the Redis counters.
