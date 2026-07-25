# Generator for TPC-DS data

Based on https://www.tpc.org/tpcds/ — generates flat `.dat` files (pipe-delimited) using the `dsdgen` binary. Expects the pre-compiled `dsdgen` binary and `tpcds.idx` in the build context. In multi-pod mode each pod generates one partition of the data set. Unlike TPC-H, `customer.dat` is encoded in ISO-8859-1 and must be converted to UTF-8 (handled by `TRANSFORM_RAW_DATA`).

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
