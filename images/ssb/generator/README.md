# Generator for SSB data

Generates Star Schema Benchmark `.tbl` files (pipe-delimited, no trailing delimiter) with
`dbgen` from [eyalroz/ssb-dbgen](https://github.com/eyalroz/ssb-dbgen), built in the first
stage of the Dockerfile from commit `ae1e254aa4d603d8ef1f44078e5abed011634b23` plus
`dbgen-chunk-seeds.patch`. With `SSB_SCHEMA_VARIANT=flat` it also joins the lineorder chunk
with customer, supplier and part into `lineorder_flat.tbl`.

See [images/ssb/README.md](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/ssb/README.md) for the data layout and design decisions.

## Execution flow (`generator.sh`)

1. Pop child index from Redis queue
   `bexhoma-loading-<CONNECTION>-<EXPERIMENT>-<EXPERIMENT_RUN>-<DATA_JOB>`. Exits with `exit 1`
   if the queue is empty rather than defaulting to a fixed child index.
2. Write child index to `/tmp/ssb/BEXHOMA_CHILD` (the loader reads this file).
3. Determine `destination_raw`: `/data/ssb/SF<SF>[/<N>/<child>]` (normal) or
   `/data/ssb/SF<SF>/flat[/<N>/<child>]` (flat); `/tmp/ssb/...` if `STORE_RAW_DATA=0`.
   Exit early if it holds `.complete` and `STORE_RAW_DATA_RECREATE=0`. Otherwise remove its
   `.tbl` files and `.complete` (files only: with one pod the folder holds other splits too).
4. If `BEXHOMA_SYNCH_GENERATE=1`: sync on `bexhoma-generator-podcount-job-<CONNECTION>-<EXPERIMENT>-<DATA_JOB>`.
5. normal: `dbgen -T l [-C <N> -S <child>]`; child 1 also `dbgen -T c`, `-T s`, `-T p`, `-T d`.
   flat: lineorder chunk (reused from the normal folder if complete), full customer/supplier/part
   in `SSB_WORK_DIR`, then `sort | join | gawk -f flat.awk`, optional order restore, row count check.
6. Write `.complete`. Emit `BEXHOMA_DURATION`, `BEXHOMA_START`, `BEXHOMA_END`.

## Environment variables

### Scaling and parallelism

* `SF`: Scale factor; lineorder has about 6,000,000 x SF rows. Default: `1`.
* `BEXHOMA_NUM_PODS`: Total number of generator (= loader) pods, the number of lineorder chunks. Default: `4`.
* `BEXHOMA_CHILD`: Index of this pod (1-based). Overwritten at runtime by the value popped from the Redis queue. Default: `1`.

### Data storage

* `STORE_RAW_DATA`: `1` = store under `/data/ssb/...` (shared volume, reused); `0` = under `/tmp/ssb/...`. Default: `0` (bexhoma sets `1`).
* `STORE_RAW_DATA_RECREATE`: `1` = generate again even if the folder is complete. Default: `0`.

### Schema variant and flat generation

* `SSB_SCHEMA_VARIANT`: `normal` (star schema files) or `flat` (`lineorder_flat.tbl`). Default: `normal`.
* `SSB_WORK_DIR`: Folder for the flat step's work files (sort temp, dimensions, chunk). Default: `/work`.
* `SSB_SORT_MEM`: Memory buffer of each `sort`. Default: `512M`.
* `SSB_FLAT_RESTORE_ORDER`: `1` = sort the flat file back into lineorder order (`lo_orderkey, lo_linenumber`); `0` = leave it ordered by `lo_custkey`. Default: `1`.

### Redis message queue and identity

* `BEXHOMA_CONNECTION`, `BEXHOMA_EXPERIMENT`, `BEXHOMA_EXPERIMENT_RUN`, `BEXHOMA_DATA_JOB`: address the Redis queue.
* `BEXHOMA_CONFIGURATION`, `BEXHOMA_CLIENT`: echoed in the log.

### Pod synchronisation

* `BEXHOMA_SYNCH_GENERATE`: `1` = wait until all generator pods of the job have checked in. Default: `0`.
