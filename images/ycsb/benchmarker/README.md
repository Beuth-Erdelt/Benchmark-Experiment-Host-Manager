# Benchmarker for YCSB data

The image is based on https://github.com/brianfrankcooper/YCSB

This folder contains the Dockerfile for a benchmarker that runs a YCSB workload against an already-loaded DBMS.

See [../README.md](../README.md) for shared design decisions, bundled JDBC
drivers, and the workload template placeholder reference.

## Execution flow (`benchmarker.sh`)

1. Capture script start time.
2. Optionally sleep until `BEXHOMA_TIME_START` (synchronized start across pods).
3. Pop the pod's child index from the Redis queue
   `bexhoma-benchmarker-<CONNECTION>-<EXPERIMENT>`.
4. Compute row-range parameters; override to full key range
   (`ROW_START=0`, `ROW_PART=YCSB_ROWS`) so every benchmarking pod covers the
   complete dataset.
5. Increment and poll the Redis counter
   `bexhoma-benchmarker-podcount-<CONNECTION>-<EXPERIMENT>` until all
   `BEXHOMA_NUM_PODS` pods are ready.
6. Write `db.properties` (JDBC or Redis branch, optionally with batch settings).
7. Copy workload template → `/tmp/workload`; substitute placeholder tokens via
   `sed`.
8. Run `ycsb run` (redis / redis-cluster / jdbc branch, with or without `-s`).
9. Emit `BEXHOMA_DURATION`, `BEXHOMA_START`, `BEXHOMA_END` to stdout for the
   evaluator.

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

* `BEXHOMA_SYNCH_LOAD`: When non-zero, the pod waits for all `BEXHOMA_NUM_PODS` pods to register before starting the workload. Pods coordinate via the Redis counter `bexhoma-benchmarker-podcount-<CONNECTION>-<EXPERIMENT>`.
* `BEXHOMA_TIME_START`: Optional RFC-3339 timestamp. When non-zero, the pod sleeps until this time before starting.
* `BEXHOMA_TIME_NOW`: Informational timestamp of the planned start, echoed to the log.

### YCSB workload parameters

* `YCSB_WORKLOAD`: YCSB workload name — `a`, `b`, `c`, `d`, `e`, or `f`.
* `YCSB_ROWS`: Total number of records in the dataset. Defaults to `SF × 100,000`.
* `YCSB_OPERATIONS`: Number of operations per pod. Defaults to `SF × 100,000`.
* `YCSB_THREADCOUNT`: YCSB workload property `threadcount`.
* `YCSB_TARGET`: YCSB workload property `target` (operations per second cap; 0 = unlimited).
* `YCSB_STATUS_INTERVAL`: YCSB workload property `status.interval` (seconds between status lines).
* `YCSB_STATUS`: When non-zero, YCSB is invoked with `-s` to emit per-interval status lines.
* `YCSB_BATCHSIZE`: YCSB workload property `db.batchsize`. Also enables `jdbc.batchupdateapi=true`. Empty means no batching.
* `YCSB_MEASUREMENT_TYPE`: YCSB workload property `measurementtype` — `hdrhistogram` (default) or `histogram`.
* `YCSB_USE_HOSTLIST`: When `1` or `true`, use `BEXHOMA_URL_LIST` instead of `BEXHOMA_URL` for the JDBC connection.
* `YCSB_INSERTORDER`: YCSB workload property `insertorder` — `hashed` (default) or `ordered`.
