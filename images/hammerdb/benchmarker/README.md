# Benchmarker for TPC-C data (HammerDB)

The image is based on https://hub.docker.com/r/tpcorg/hammerdb

This folder contains the Dockerfile for a benchmarker that runs a timed TPC-C
workload against an already-loaded DBMS using HammerDB.
Supported backends: `postgresql`, `mysql`, `mariadb`, `citus`.

See [../README.md](../README.md) for shared design decisions and the full
supported-backend table.

## Execution flow (`benchmarker.sh`)

1. Capture script start time.
2. Optionally sleep until `BEXHOMA_TIME_START` (synchronised start across pods).
3. Pop the pod's child index from the Redis queue
   `bexhoma-benchmarker-<CONNECTION>-<EXPERIMENT>`.
4. Increment and poll the Redis counter
   `bexhoma-benchmarker-podcount-<CONNECTION>-<EXPERIMENT>` until all
   `BEXHOMA_NUM_PODS` pods are ready (synchronisation is unconditional).
5. Generate a `benchmark.tcl` script tailored to `HAMMERDB_TYPE`
   (postgresql / mysql / mariadb / citus).
6. Run `hammerdbcli auto benchmark.tcl`.
7. Copy `/tmp/hammerdb.log` into the result folder as
   `hammerdb.<CONNECTION>.<CLIENT>.<UUID>.log`.
8. Print `/tmp/hdbxtprofile.log` (per-transaction latency profile, when
   `HAMMERDB_TIMEPROFILE=true`).
9. Emit `BEXHOMA_DURATION`, `BEXHOMA_START`, `BEXHOMA_END` to stdout for the
   evaluator.

## Environment variables

### Scaling and parallelism

* `SF`: Scale factor — number of TPC-C warehouses.
* `BEXHOMA_NUM_PODS`: Number of parallel pods.
* `BEXHOMA_RNGSEED`: Random seed. Currently ignored.

### Target DBMS connection

* `BEXHOMA_DBMS_TYPE`: Backend type — `postgresql`, `mysql`, `mariadb`, or `citus`.
* `BEXHOMA_HOST`: Hostname of the target DBMS.
* `BEXHOMA_PORT`: Port of the target DBMS.
* `BEXHOMA_USER`: Database user.
* `BEXHOMA_PASSWORD`: Database password.
* `BEXHOMA_DATABASE`: Database name (used for Citus only; PostgreSQL uses `tpcc`).

### Bexhoma experiment identity

* `BEXHOMA_DBMS`: DBMS label. Echoed to the log.
* `BEXHOMA_CONFIGURATION`: Configuration name. Echoed to the log.
* `BEXHOMA_CONNECTION`: Bexhoma connection name. Used to address the Redis message queue.
* `BEXHOMA_EXPERIMENT`: Bexhoma experiment identifier. Used to address the Redis message queue.
* `BEXHOMA_EXPERIMENT_RUN`: Number of the current repetition of the complete experiment.
* `BEXHOMA_CLIENT`: Client index. Used to name the result log file.
* `BEXHOMA_CHILD`: Index of the current pod (1-based). Overwritten at runtime by the Redis queue entry.

### Pod synchronisation

Pods always synchronise before starting: each pod increments the Redis counter
`bexhoma-benchmarker-podcount-<CONNECTION>-<EXPERIMENT>` and waits until all
`BEXHOMA_NUM_PODS` pods are ready.

* `BEXHOMA_TIME_START`: Optional RFC-3339 timestamp. When non-zero, the pod sleeps until this time before starting.
* `BEXHOMA_TIME_NOW`: Informational timestamp of the planned start, echoed to the log.

### HammerDB workload parameters

* `HAMMERDB_TYPE`: Backend type — `postgresql`, `mysql`, `mariadb`, or `citus`.
* `HAMMERDB_RAMPUP`: Ramp-up time in minutes before the first transaction count is taken.
* `HAMMERDB_DURATION`: Duration in minutes before the second transaction count is taken.
* `HAMMERDB_ITERATIONS`: Maximum number of transactions before a virtual user logs off.
* `HAMMERDB_VUSERS`: Space-separated list of virtual-user counts to run in sequence (e.g. `1 2 4 8`).
* `HAMMERDB_NUM_VU`: Number of virtual users used during the setup phase.
* `HAMMERDB_MYSQL_ENGINE`: Storage engine for MySQL/MariaDB (default `innodb`).
* `HAMMERDB_TIMEPROFILE`: When `true`, per-transaction latency profiles are written to `/tmp/hdbxtprofile.log`.
* `HAMMERDB_ALLWAREHOUSES`: When `true`, virtual users are not pinned to a fixed warehouse at startup.
* `HAMMERDB_KEYANDTHINK`: When `true`, key-and-think time is added between transactions.
