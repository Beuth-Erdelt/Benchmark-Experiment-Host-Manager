# Generator for TPC-H data

Based on https://www.tpc.org/tpch/ — generates flat `.tbl` files (pipe-delimited, one row per line ending with `|`) using the `dbgen` binary. Expects the pre-compiled `dbgen` binary and `dists.dss` in the build context. In multi-pod mode each pod generates one partition of the data set.

See [../README.md](../README.md) for the shared TPC-H pipeline design and per-DBMS loader differences.

## Execution flow (`generator.sh`)

1. Pop child index from Redis queue
   `bexhoma-loading-<CONNECTION>-<EXPERIMENT>-<EXPERIMENT_RUN>-<DATA_JOB>` (scoped by
   `EXPERIMENT_RUN` because loading is redone from scratch for every experiment_run — see
   `bexhoma/CLAUDE.md`'s "Chunk-assignment queue" section). Exits with `exit 1` if the queue is
   empty rather than defaulting to a fixed child index, since another pod may already own it.
2. Write child index to `/tmp/tpch/BEXHOMA_CHILD` (loaders read this file).
3. Multi-tenant handling: `schema` or `database` mode remaps `BEXHOMA_CHILD` and scales `BEXHOMA_NUM_PODS` per tenant; `container` mode logs but does not remap.
4. Determine `destination_raw`: `/data/tpch/SF<SF>[/<N>/<child>]` if `STORE_RAW_DATA=1`, else `/tmp/tpch/SF<SF>[/<N>/<child>]`. Exit early if the folder exists **and contains at least one `.tbl` file** (checked via a `nullglob` array, not just directory existence — an empty folder created as a parent for another child's subfolder must not be mistaken for already-generated data) and `STORE_RAW_DATA_RECREATE=0`.
5. If `BEXHOMA_SYNCH_GENERATE=1`: sync on `bexhoma-generator-podcount-<CONNECTION>-<EXPERIMENT>`.
6. Run `dbgen -s <SF>` (single pod) or `dbgen -s <SF> -S <child> -C <num_pods>` (multi-pod).
7. If `TRANSFORM_RAW_DATA=1`: strip trailing `|` from every `.tbl` file via `sed 's/.$//' -i`.
8. Emit `BEXHOMA_DURATION`, `BEXHOMA_START`, `BEXHOMA_END`.

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

* `BEXHOMA_CONNECTION`: Logical connection name — used to address the Redis queue `bexhoma-loading-<CONNECTION>-<EXPERIMENT>-<EXPERIMENT_RUN>-<DATA_JOB>`.
* `BEXHOMA_EXPERIMENT`: Experiment ID — used together with `BEXHOMA_CONNECTION`, `BEXHOMA_EXPERIMENT_RUN` and `BEXHOMA_DATA_JOB` to address the Redis queue.

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
