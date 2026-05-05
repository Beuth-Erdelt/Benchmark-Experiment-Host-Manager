# Benchmarker for DBMSBenchmarker

The image is based on [DBMSBenchmarker](https://github.com/Beuth-Erdelt/DBMS-Benchmarker).

This folder contains the Dockerfile template for a benchmarker that runs a DBMSBenchmarker
query workload against an already-loaded DBMS.

## Environment variables

### Scaling and parallelism

* `SF`: Scaling factor. Passed to the benchmark configuration to control the dataset size.
* `BEXHOMA_NUM_PODS`: Number of parallel pods in the Kubernetes job. Used for pod-count synchronisation.
* `BEXHOMA_CHILD`: Index of the current pod (1-based). Overwritten at runtime by the Redis queue entry.
* `BEXHOMA_RNGSEED`: Random seed. Currently passed as context but not consumed by DBMSBenchmarker directly.

### Target DBMS connection

* `BEXHOMA_URL`: JDBC connection URL (e.g. `jdbc:mysql://localhost:3306/ycsb`). Written into the per-connection config file.
* `BEXHOMA_HOST`: Hostname of the target DBMS.
* `BEXHOMA_PORT`: Port of the target DBMS.
* `BEXHOMA_JAR`: JDBC driver jar file name (must exist in `jars/` inside the image — see Dockerfile for bundled drivers).
* `BEXHOMA_DRIVER`: JDBC driver class name (e.g. `com.mysql.cj.jdbc.Driver`).
* `BEXHOMA_USER`: Database username.
* `BEXHOMA_PASSWORD`: Database password.
* `BEXHOMA_DATABASE`: Database (catalog) name. Passed to DBMSBenchmarker via `-fixdb`. In `database` tenancy mode this is overridden to `tenant_<N>`.
* `BEXHOMA_SCHEMA`: Schema name. Passed to DBMSBenchmarker via `-fixs`. In `schema` tenancy mode this is overridden to `tenant_<N>`.

### Bexhoma experiment identity

* `BEXHOMA_DBMS`: DBMS type identifier (e.g. `postgresql`). Informational only.
* `BEXHOMA_CONFIGURATION`: Bexhoma configuration name. Informational only.
* `BEXHOMA_CONNECTION`: Bexhoma connection name. Used to address the Redis message queue and counter keys.
* `BEXHOMA_EXPERIMENT`: Bexhoma experiment identifier. Used to address the Redis message queue and counter keys, and to name the result sub-folder.
* `BEXHOMA_EXPERIMENT_RUN`: Number of the current repetition of the complete experiment.
* `BEXHOMA_CLIENT`: Client index (1-based) within the current run. Used as the upper bound on result sub-folders (`-ms`).

### Pod synchronisation

* `BEXHOMA_TIME_START`: Optional RFC-3339 timestamp. When non-zero, the pod sleeps until this time before proceeding.
* `BEXHOMA_TIME_NOW`: Informational timestamp of the planned start, echoed to the log.

### Multi-tenant parameters

* `BEXHOMA_TENANT_BY`: Tenancy mode. One of `schema`, `database`, or `container`. Empty means no multi-tenant mode. Controls how `BEXHOMA_CHILD` and `BEXHOMA_NUM_PODS` are adjusted before the benchmark run.
* `BEXHOMA_TENANT_NUM`: Number of tenants. Used to partition `BEXHOMA_NUM_PODS` and compute the per-tenant child index. Default: `1`.
* `BEXHOMA_NUM_PODS_TOTAL`: Total number of pods across all tenants. Used for the cross-tenant pod-count barrier when `BEXHOMA_TENANT_BY=container`. Default: `4`.

### DBMSBenchmarker parameters

* `DBMSBENCHMARKER_CODE`: Experiment code used as the result folder name (`/results/<CODE>`). No Docker default — must be set at runtime.
* `DBMSBENCHMARKER_CONNECTION`: DBMSBenchmarker connection name. Passed via `-c` and used to locate the per-connection config file (`<CONNECTION>.config`). Should match `BEXHOMA_CONNECTION`.
* `DBMSBENCHMARKER_ALIAS`: Alias for the DBMS connection. Passed via `-ca`.
* `DBMSBENCHMARKER_CLIENT`: Maximum number of per-connection result sub-folders. Passed via `-ms`. Should match `BEXHOMA_CLIENT`.
* `DBMSBENCHMARKER_SLEEP`: Sleep seconds before benchmarking. Kept for reference; timing is handled by the shell via `BEXHOMA_TIME_START` instead.
* `DBMSBENCHMARKER_RECREATE_PARAMETER`: When `True`, force recreation of query parameters for each stream (`-rcp 1`). Default: `False` (all streams share the same parameters).
* `DBMSBENCHMARKER_VERBOSE`: When non-zero, enable verbose output flags (`-d -vq -vr -vp -vs`). Default: `0`.
* `DBMSBENCHMARKER_DEV`: When non-zero, check out the `dev` branch of the cloned repository and pass `-db` to DBMSBenchmarker. Default: `0`.
* `DBMSBENCHMARKER_SHUFFLE_QUERIES`: When `True`, randomise query order per stream (`-ssh 1`). Default: `False`.
* `DBMSBENCHMARKER_TESTRUN`: When non-zero, run a quick self-test (TPC-DS against MonetDB at localhost) and exit immediately. Default: `0`.

## Bundled JDBC drivers

| Driver | Version | Jar |
|---|---|---|
| PostgreSQL | 42.5.0 | `postgresql-42.5.0.jar` |
| MySQL | 8.0.31 | `mysql-connector-j-8.0.31.jar` |
| MariaDB | 3.1.0 | `mariadb-java-client-3.1.0.jar` |
| MonetDB | 12.1 (jre8) | `monetdb-jdbc-12.1.jre8.jar` |
| MonetDB | 12.2 (jre8) | `monetdb-jdbc-12.2.jre8.jar` |
| SingleStore | 1.1.4 | `singlestore-jdbc-client-1.1.4.jar` |
| YugabyteDB | 42.3.5-yb-2 | `jdbc-yugabytedb-42.3.5-yb-2.jar` |

See [DBMSBenchmarker docs](https://github.com/Beuth-Erdelt/DBMS-Benchmarker) for details
on the query workload configuration.
