# Loader for TPC-H data into PostgreSQL

Loads pre-generated TPC-H `.tbl` files into PostgreSQL using `psql \COPY`. The child index is read from `/tmp/tpch/BEXHOMA_CHILD` (written by the generator pod running in the same Kubernetes pod). `nation` and `region` are only loaded by the first pod in non-tenant mode to avoid duplicate key errors. Supports schema and database multi-tenancy with different index-mapping logic.

See [../README.md](../README.md) for the shared TPC-H pipeline design.

## Execution flow (`loader.sh`)

1. Read `BEXHOMA_CHILD` from `/tmp/tpch/BEXHOMA_CHILD`.
2. Determine `destination_raw` path (same logic as the generator).
3. Multi-tenant handling — the only TPC-H loader that supports this.
4. If `BEXHOMA_SYNCH_LOAD=1`: sync on the job counter `bexhoma-loader-podcount-job-<CONNECTION>-<EXPERIMENT>`,
   then the round counter `bexhoma-loader-podcount-round-<CONFIGURATION>-<EXPERIMENT>` (always
   initialized by Python, even for a single loader entry; only meaningful when the SUT
   configuration has more than one parallel loader entry — see `bexhoma/CLAUDE.md`).
   Additionally syncs on `bexhoma-loader-podcount-<EXPERIMENT>` when `BEXHOMA_TENANT_BY=container`.
5. Loop over `.tbl` files; skip `nation` and `region` for pods > 1 in non-tenant mode.
6. If `TPCH_TABLE` is set: only load that table.
7. Execute `psql \COPY` per table, using `PGOPTIONS --search_path` for schema isolation; retry on known transient errors.
8. Emit `BEXHOMA_DURATION`, `BEXHOMA_START`, `BEXHOMA_END`.

## Environment variables

### Scaling and parallelism

* `SF`: Scale factor — used to locate the correct data subdirectory. Default: `1`.
* `BEXHOMA_NUM_PODS`: Total number of loader pods. Default: `4`.
* `BEXHOMA_CHILD`: Pod index (1-based). Overwritten at runtime from `/tmp/tpch/BEXHOMA_CHILD`. Default: `1`.
* `BEXHOMA_RNGSEED`: Not used by this loader. Default: `123`.

### Target DBMS connection

* `BEXHOMA_HOST`: PostgreSQL hostname. Default: `www.example.com`.
* `BEXHOMA_PORT`: PostgreSQL port. Default: `5432`.
* `BEXHOMA_USER`: PostgreSQL username. Default: `postgres`.
* `BEXHOMA_PASSWORD`: PostgreSQL password. Default: `postgres`.
* `BEXHOMA_DATABASE`: Target database name. Default: `tpch`.
* `BEXHOMA_SCHEMA`: Target schema name. Set via `PGOPTIONS --search_path` when non-empty. In multi-tenant schema mode this is derived automatically. Default: `""`.
* `BEXHOMA_URL`, `BEXHOMA_JAR`, `BEXHOMA_DRIVER`: Not used by this loader — declared for compatibility.

### Bexhoma experiment identity

* `BEXHOMA_CONNECTION`: Logical connection name — used to address the Redis synchronisation counter. Default: `mysql`.
* `BEXHOMA_EXPERIMENT`: Experiment ID. Default: `12345`.
* `BEXHOMA_EXPERIMENT_RUN`: Run counter within the experiment. Default: `1`.
* `BEXHOMA_CONFIGURATION`: Configuration label echoed in log output.
* `BEXHOMA_CLIENT`: Client index echoed in log output. Default: `1`.

### Multi-tenancy

* `BEXHOMA_TENANT_BY`: Isolation mode. `schema` — `SCHEMA_INDEX = (CHILD-1) % TENANT_NUM`; remaps `BEXHOMA_CHILD` and shrinks `BEXHOMA_NUM_PODS` per tenant, sets `BEXHOMA_SCHEMA`. `database` — same remapping but sets `BEXHOMA_DATABASE` instead. `container` — no index remapping; uses a second Redis barrier on `bexhoma-loader-podcount-<EXPERIMENT>`. Default: `""` (disabled).
* `BEXHOMA_TENANT_NUM`: Total number of tenants. Default: `""`.
* `BEXHOMA_NUM_PODS_TOTAL`: Used for the container-tenancy cross-loader synchronisation barrier `bexhoma-loader-podcount-<EXPERIMENT>`. Default: `""`.

### Data storage and loading control

* `STORE_RAW_DATA`: `0` = read data from `/tmp/tpch/`; `1` = read from `/data/tpch/`. Default: `0`.
* `BEXHOMA_SYNCH_LOAD`: `1` = wait on Redis counter `bexhoma-loader-podcount-<CONNECTION>-<EXPERIMENT>` until all loader pods have checked in before starting. Container tenancy mode adds a second barrier. Default: `0`.
* `TPCH_TABLE`: When set to a table name only that table is loaded; all others are skipped. Default: `""`.
