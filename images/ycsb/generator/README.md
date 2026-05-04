# Generator for YCSB data

The image is based on https://github.com/brianfrankcooper/YCSB

This folder contains the Dockerfile for a data generator that loads data into a DBMS using the YCSB `load` phase. Parallel pods each receive a contiguous slice of the key space so the full dataset is loaded without overlap.

## Environment variables

### Scaling and parallelism

* `SF`: Scaling factor. Number of rows = 100,000 × SF if not set otherwise. Number of operations = 100,000 × SF if not set otherwise.
* `BEXHOMA_NUM_PODS`: Number of parallel pods.
* `BEXHOMA_RNGSEED`: Random seed. Currently ignored.

### Target DBMS connection

* `BEXHOMA_DBMS_TYPE`: Backend type — `jdbc`, `redis`, or `redis-cluster`.
* `BEXHOMA_URL`: JDBC connection URL (e.g. `jdbc:postgresql://host:5432/ycsb`). Used when `YCSB_USE_HOSTLIST=0`.
* `BEXHOMA_URL_LIST`: Comma-separated list of JDBC URLs for multi-host setups. Used when `YCSB_USE_HOSTLIST=1`.
* `BEXHOMA_HOST`: Redis host. Ignored for JDBC.
* `BEXHOMA_PORT`: Redis port. Ignored for JDBC.
* `BEXHOMA_JAR`: JDBC driver jar file name (must exist in `jars/` inside the image — see Dockerfile for bundled drivers).
* `BEXHOMA_DRIVER`: JDBC driver class name (e.g. `org.postgresql.Driver`).
* `BEXHOMA_USER`: Database user (`db.user`).
* `BEXHOMA_PASSWORD`: Database password (`db.passwd`).
* `DATABASE`: Database name. Currently unused by the entrypoint script.

### Bexhoma experiment identity

* `BEXHOMA_CONNECTION`: Bexhoma connection name. Used to address the Redis message queue.
* `BEXHOMA_EXPERIMENT`: Bexhoma experiment identifier. Used to address the Redis message queue.
* `BEXHOMA_EXPERIMENT_RUN`: Number of the current repetition of the complete experiment.
* `BEXHOMA_CHILD`: Index of the current pod (1-based). Overwritten at runtime by the Redis queue entry.

### Pod synchronisation

* `BEXHOMA_SYNCH_LOAD`: When non-zero, the pod waits for all `BEXHOMA_NUM_PODS` pods to register before starting the workload. Pods coordinate via the Redis counter `bexhoma-loader-podcount-<CONNECTION>-<EXPERIMENT>`.
* `BEXHOMA_TIME_START`: Optional RFC-3339 timestamp. When non-zero, the pod sleeps until this time before starting.
* `BEXHOMA_TIME_NOW`: Informational timestamp of the planned start, echoed to the log.

### YCSB workload parameters

* `YCSB_WORKLOAD`: YCSB workload name — `a`, `b`, `c`, `d`, `e`, or `f`.
* `YCSB_ROWS`: Total number of records to load. Defaults to `SF × 100,000`.
* `YCSB_OPERATIONS`: Number of operations per pod. Defaults to `SF × 100,000`.
* `YCSB_THREADCOUNT`: YCSB workload property `threadcount`.
* `YCSB_TARGET`: YCSB workload property `target` (operations per second cap; 0 = unlimited).
* `YCSB_STATUS_INTERVAL`: YCSB workload property `status.interval` (seconds between status lines).
* `YCSB_STATUS`: When non-zero, YCSB is invoked with `-s` to emit per-interval status lines.
* `YCSB_BATCHSIZE`: YCSB workload property `db.batchsize`. Also enables `jdbc.batchupdateapi=true`. Empty means no batching.
* `YCSB_MEASUREMENT_TYPE`: YCSB workload property `measurementtype` — `hdrhistogram` (default) or `histogram`.
* `YCSB_USE_HOSTLIST`: When `1` or `true`, use `BEXHOMA_URL_LIST` instead of `BEXHOMA_URL` for the JDBC connection.
* `YCSB_INSERTORDER`: YCSB workload property `insertorder` — `hashed` (default) or `ordered`.
