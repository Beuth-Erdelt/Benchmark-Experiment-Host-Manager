# Generator for TPC-DS data

Based on https://www.tpc.org/tpcds/ — generates flat `.dat` files (pipe-delimited) using the `dsdgen` binary. Expects the pre-compiled `dsdgen` binary and `tpcds.idx` in the build context. In multi-pod mode each pod generates one partition of the data set. Unlike TPC-H, `customer.dat` is encoded in ISO-8859-1 and must be converted to UTF-8 (handled by `TRANSFORM_RAW_DATA`).

See [../README.md](../README.md) for the shared TPC-DS pipeline design and differences from TPC-H.

## Execution flow (`generator.sh`)

1. Pop child index from Redis queue
   `bexhoma-loading-<CONNECTION>-<EXPERIMENT>-<EXPERIMENT_RUN>-<DATA_JOB>` (scoped by
   `EXPERIMENT_RUN` because loading is redone from scratch for every experiment_run — see
   `bexhoma/CLAUDE.md`'s "Chunk-assignment queue" section). Exits with `exit 1` if the queue is
   empty rather than defaulting to a fixed child index, since another pod may already own it.
2. Write child index to `/tmp/tpcds/BEXHOMA_CHILD` (loaders read this file).
3. If `BEXHOMA_SYNCH_GENERATE=1`: sync on `bexhoma-generator-podcount-<CONNECTION>-<EXPERIMENT>`.
4. Determine destination: `/data/tpcds/SF<SF>[/<N>/<child>]` or `/tmp/tpcds/SF<SF>[/<N>/<child>]`. Exit early if the folder exists **and contains at least one `.dat` file** (checked via a `nullglob` array, not just directory existence — an empty folder created as a parent for another child's subfolder must not be mistaken for already-generated data) and `STORE_RAW_DATA_RECREATE=0`.
5. Run `dsdgen -dir <dst> -scale <SF>` (single pod) or `dsdgen -dir <dst> -scale <SF> -parallel <N> -child <i>` (multi-pod).
6. If `TRANSFORM_RAW_DATA=1`: convert `customer.dat` from ISO-8859-1 to UTF-8 via `iconv`, then strip trailing `|` from all `.dat` files via `sed 's/.$//' -i`.
7. Emit `BEXHOMA_DURATION`, `BEXHOMA_START`, `BEXHOMA_END`.

No multi-tenant logic in the TPC-DS generator (unlike the TPC-H generator).

## Environment variables

### Scaling and parallelism

* `SF`: Scale factor — total data size in GB (1 ≈ 1 GB). Each pod generates its share using `dsdgen -scale <SF> -parallel <NUM_PODS> -child <CHILD>`. Default: `1`.
* `BEXHOMA_NUM_PODS`: Total number of generator pods. Default: `4`.
* `BEXHOMA_CHILD`: Index of this pod (1-based). Overwritten at runtime by the value popped from the Redis queue. Default: `1`.
* `BEXHOMA_RNGSEED`: Random-number seed passed to the script — ignored by `dsdgen` itself. Default: `123`.

### Data storage

* `STORE_RAW_DATA`: `1` = store generated files persistently under `/data/tpcds/SF<SF>/<NUM_PODS>/<CHILD>/`; `0` = store locally under `/tmp/tpcds/SF<SF>/<NUM_PODS>/<CHILD>/`. Default: `0`.
* `STORE_RAW_DATA_RECREATE`: `1` = delete and regenerate data even if the destination folder already exists; `0` = skip generation and exit early if the folder exists. Default: `0`.
* `TRANSFORM_RAW_DATA`: `1` = converts `customer.dat` from ISO-8859-1 to UTF-8 using `iconv`, then strips the trailing `|` delimiter from every `.dat` line via `sed 's/.$//' -i`. Default: `1`.

### Redis message queue

* `BEXHOMA_CONNECTION`: Logical connection name — used to address the Redis queue `bexhoma-loading-<CONNECTION>-<EXPERIMENT>-<EXPERIMENT_RUN>-<DATA_JOB>`.
* `BEXHOMA_EXPERIMENT`: Experiment ID — used together with `BEXHOMA_CONNECTION`, `BEXHOMA_EXPERIMENT_RUN` and `BEXHOMA_DATA_JOB` to address the Redis queue.

### Bexhoma experiment identity

* `BEXHOMA_EXPERIMENT_RUN`: Run counter within the experiment. Default: `1`.
* `BEXHOMA_CONFIGURATION`: Configuration label echoed in log output.
* `BEXHOMA_CLIENT`: Client index echoed in log output. Default: `1`.

### Pod synchronisation

* `BEXHOMA_SYNCH_GENERATE`: `1` = wait on Redis counter `bexhoma-generator-podcount-<CONNECTION>-<EXPERIMENT>` until all generator pods have checked in before starting generation. Default: `0`.

### Unused / compatibility

* `BEXHOMA_URL`: JDBC URL — declared for compatibility with other Bexhoma images; not used by this script.
* `BEXHOMA_JAR`: JDBC driver JAR — not used by this script.
* `BEXHOMA_DRIVER`: JDBC driver class — not used by this script.
* `BEXHOMA_HOST`: DBMS hostname — not used by this script.
* `BEXHOMA_PORT`: DBMS port — not used by this script.
* `BEXHOMA_USER`: DBMS username — not used by this script.
* `BEXHOMA_PASSWORD`: DBMS password — not used by this script.
* `BEXHOMA_DATABASE`: DBMS database name — not used by this script.
