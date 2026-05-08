# Generator for TPC-H data

Based on https://www.tpc.org/tpch/ — generates flat `.tbl` files (pipe-delimited, one row per line ending with `|`) using the `dbgen` binary. Expects the pre-compiled `dbgen` binary and `dists.dss` in the build context. In multi-pod mode each pod generates one partition of the data set.

## Environment variables

### Scaling and parallelism

* `SF`: Scale factor — total data size in GB (1 ≈ 1 GB). Each pod generates its share using `dbgen -S <CHILD> -C <NUM_PODS>`. Default: `1`.
* `BEXHOMA_NUM_PODS`: Total number of generator pods. Default: `4`.
* `BEXHOMA_CHILD`: Index of this pod (1-based). Overwritten at runtime by the value popped from the Redis queue. Default: `1`.
* `BEXHOMA_RNGSEED`: Random-number seed passed to the script — ignored by `dbgen` itself. Default: `123`.

### Data storage

* `STORE_RAW_DATA`: `1` = store generated files persistently under `/data/tpch/SF<SF>/<NUM_PODS>/<CHILD>/`; `0` = store locally under `/tmp/tpch/SF<SF>/<NUM_PODS>/<CHILD>/`. Default: `0`.
* `STORE_RAW_DATA_RECREATE`: `1` = delete and regenerate data even if the destination folder already exists; `0` = skip generation and exit early if the folder exists. Default: `0`.
* `TRANSFORM_RAW_DATA`: `1` = strip the trailing `|` delimiter from every line of every `.tbl` file via `sed 's/.$//' -i` after generation. Default: `1`.

### Redis message queue

* `BEXHOMA_CONNECTION`: Logical connection name — used to address the Redis queue `bexhoma-loading-<CONNECTION>-<EXPERIMENT>`.
* `BEXHOMA_EXPERIMENT`: Experiment ID — used together with `BEXHOMA_CONNECTION` to address the Redis queue.

### Bexhoma experiment identity

* `BEXHOMA_EXPERIMENT_RUN`: Run counter within the experiment. Default: `1`.
* `BEXHOMA_CONFIGURATION`: Configuration label echoed in log output.
* `BEXHOMA_CLIENT`: Client index echoed in log output. Default: `1`.

### Multi-tenancy

* `BEXHOMA_TENANT_BY`: Isolation mode — `schema` or `database` remaps `BEXHOMA_NUM_PODS` and `BEXHOMA_CHILD` per tenant so each tenant gets its own data partition; `container` mode logs the setting but does not remap. Default: `""` (disabled).
* `BEXHOMA_TENANT_NUM`: Total number of tenants. Used together with `BEXHOMA_TENANT_BY` to compute per-tenant child and pod counts.
* `BEXHOMA_SCHEMA`: Target schema name. In schema isolation mode this is derived from `BEXHOMA_CHILD`. Default: `""`.

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
