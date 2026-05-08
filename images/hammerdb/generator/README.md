# Generator for TPC-C data (HammerDB)

The image is based on https://hub.docker.com/r/tpcorg/hammerdb

This folder contains the Dockerfile for a data generator that loads TPC-C data
into a DBMS using HammerDB's `buildschema` command.
Supported backends: `postgresql`, `mysql`, `mariadb`, `citus`.

## Environment variables

### Scaling and parallelism

* `SF`: Scale factor — number of TPC-C warehouses to load.
* `BEXHOMA_NUM_PODS`: Number of parallel pods. Echoed to the log.
* `BEXHOMA_RNGSEED`: Random seed. Currently ignored.

### Target DBMS connection

* `BEXHOMA_HOST`: Hostname of the target DBMS.
* `BEXHOMA_PORT`: Port of the target DBMS.
* `BEXHOMA_USER`: Database user.
* `BEXHOMA_PASSWORD`: Database password.
* `BEXHOMA_DATABASE`: Database name (used for Citus only; PostgreSQL uses `tpcc`).

### Bexhoma experiment identity

* `BEXHOMA_DBMS`: DBMS label. Echoed to the log.
* `BEXHOMA_CONFIGURATION`: Configuration name. Echoed to the log.
* `BEXHOMA_CONNECTION`: Bexhoma connection name. Echoed to the log.
* `BEXHOMA_EXPERIMENT`: Bexhoma experiment identifier. Echoed to the log.
* `BEXHOMA_EXPERIMENT_RUN`: Number of the current repetition of the complete experiment.
* `BEXHOMA_CLIENT`: Client index. Echoed to the log.
* `BEXHOMA_CHILD`: Index of the current pod (1-based). Echoed to the log.

### HammerDB workload parameters

* `HAMMERDB_TYPE`: Backend type — `postgresql`, `mysql`, `mariadb`, or `citus`.
* `HAMMERDB_VUSERS`: Number of virtual users (threads) for the load phase.
* `HAMMERDB_NUM_VU`: Number of virtual users used during setup. Echoed to the log.
* `HAMMERDB_MYSQL_ENGINE`: Storage engine for MySQL/MariaDB (default `innodb`).
* `HAMMERDB_RAMPUP`: Echoed to the log. Not used during loading.
* `HAMMERDB_DURATION`: Echoed to the log. Not used during loading.
* `HAMMERDB_ITERATIONS`: Echoed to the log. Not used during loading.
