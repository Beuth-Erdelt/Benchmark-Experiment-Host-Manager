# Benchmarker for TPC-C data (HammerDB version)

The image is based on https://hub.docker.com/r/tpcorg/hammerdb

Currently, TPC-C is adapted for PostgreSQL, MySQL and MariaDB here.

The following parameter (ENV) have been added:

* `SF`: 
* `NUM_PODS`: 
* `CHILD`: 
* `RNGSEED`: 
* `CONNECTION`: 
* `EXPERIMENT`: 
* `BEXHOMA_URL`: 
* `BEXHOMA_HOST`: 
* `BEXHOMA_PORT`: 
* `BEXHOMA_JAR`: 
* `BEXHOMA_DRIVER`: 
* `BEXHOMA_CONNECTION`: 
* `BEXHOMA_EXPERIMENT`: 
* `BEXHOMA_USER`: 
* `BEXHOMA_PASSWORD`: 
* `BEXHOMA_DATABASE`: 
* `DBMSBENCHMARKER_START`: 
* `DBMSBENCHMARKER_NOW`: 
* `HAMMERDB_TYPE postgresql`: 
* `HAMMERDB_RAMPUP`: Rampup time in minutes before first Transaction Count is taken
* `HAMMERDB_DURATION`: Duration in minutes before second Transaction Count is taken
* `HAMMERDB_ITERATIONS`: Number of transactions before logging off
* `HAMMERDB_VUSERS`: 
* `HAMMERDB_MYSQL_ENGINE`: 
* `HAMMERDB_TIMEPROFILE`: default true, true means latencies are logged, too
* `HAMMERDB_ALLWAREHOUSES`: default false, true means vusers do not get assigned to a fixed warehouse at startup, but use all (new assignment for each transaction)
* `HAMMERDB_KEYANDTHINK`: default false (activate key and think times between transactions)

This folder contains the Dockerfile for a benchmarker, that runs the workload against a loaded DBMS.
