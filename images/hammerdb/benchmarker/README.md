# Benchmarker for TPC-C data (HammerDB version)

The image is based on https://hub.docker.com/r/tpcorg/hammerdb

Currently, TPC-C is adapted for PostgreSQL, MySQL and MariaDB here.

The following parameter (ENV) have been added:

* `SF`: scaling factor (number of warehouses)
* `BEXHOMA_NUM_PODS`: number of pods in the k8s job
* `BEXHOMA_CHILD`: number of the current pod in the job, will be overwritten by redis queue value
* `BEXHOMA_RNGSEED`: seed for random number generator, currently ignored
* `BEXHOMA_URL`: url of the sut dbms, currently ignored
* `BEXHOMA_HOST`: host of the sut dbms
* `BEXHOMA_PORT`: port of the sut dbms
* `BEXHOMA_JAR`: name of jdbc jar file, currently ignored
* `BEXHOMA_DRIVER`: jdbc driver name, currently ignored
* `BEXHOMA_CONNECTION`: name of the connection (i.e., dbms configuration) to be queried
* `BEXHOMA_EXPERIMENT`: code of the experiment this is part of
* `BEXHOMA_EXPERIMENT_RUN`: number of total runs (for repetition of the complete experiment)
* `BEXHOMA_CLIENT`: number of the client in a list of executors
* `BEXHOMA_USER`: username for sut dbms connection
* `BEXHOMA_PASSWORD`: password for sut dbms connection
* `BEXHOMA_DATABASE`: database name for sut dbms connection
* `BEXHOMA_TIME_START`: Optional. If non-zero, pod will wait until time encoded in this var before starting doing something.
* `BEXHOMA_TIME_NOW`: Optional. Includes time about planned start.
* `HAMMERDB_TYPE`: type of sut dbms (postgresql, mysql, mariadb, citus)
* `HAMMERDB_RAMPUP`: rampup time in minutes before first Transaction Count is taken
* `HAMMERDB_DURATION`: duration in minutes before second Transaction Count is taken
* `HAMMERDB_ITERATIONS`: number of transactions before logging off
* `HAMMERDB_VUSERS`: number of vusers (threads)
* `HAMMERDB_NUM_VU`: number of vusers for setup
* `HAMMERDB_MYSQL_ENGINE`: engine to be used by MySQL (default innodb)
* `HAMMERDB_TIMEPROFILE`: default true, true means latencies are logged, too
* `HAMMERDB_ALLWAREHOUSES`: default false, true means vusers do not get assigned to a fixed warehouse at startup, but use all (new assignment for each transaction)
* `HAMMERDB_KEYANDTHINK`: default false (activate key and think times between transactions)

This folder contains the Dockerfile for a benchmarker, that runs the workload against a loaded DBMS.
