# Generator for TPC-C data (HammerDB version)

The image is based on https://hub.docker.com/r/tpcorg/hammerdb

Currently, TPC-C is adapted for PostgreSQL, MySQL and MariaDB here.

The following parameter (ENV) have been added:

* `SF`: scaling factor (number of warehouses)
* `NUM_PODS`: number of pods in the k8s job
* `CHILD`: number of the current pod in the job, will be overwritten by redis queue value
* `RNGSEED`: seed for random number generator, currently ignored
* `CONNECTION`: name of the connection (i.e., dbms configuration) to be queried (deprecated)
* `EXPERIMENT`: code of the experiment this is part of, deprecated
* `USER`: username for sut dbms connection
* `PASSWORD`: password for sut dbms connection
* `DATABASE`: database name for sut dbms connection
* `BEXHOMA_URL`: url of the sut dbms, currently ignored
* `BEXHOMA_HOST`: host of the sut dbms
* `BEXHOMA_PORT`: port of the sut dbms
* `BEXHOMA_JAR`: name of jdbc jar file, currently ignored
* `BEXHOMA_DRIVER`: jdbc driver name, currently ignored
* `BEXHOMA_CONNECTION`: name of the connection (i.e., dbms configuration) to be queried
* `BEXHOMA_EXPERIMENT`: code of the experiment this is part of
* `BEXHOMA_CLIENT`: number of the client in a list of executors
* `BEXHOMA_USER`: username for sut dbms connection, for future use only
* `BEXHOMA_PASSWORD`: password for sut dbms connection, for future use only
* `BEXHOMA_DATABASE`: database name for sut dbms connection, for future use only
* `DBMSBENCHMARKER_START`: anticipated start time for benchmarking
* `DBMSBENCHMARKER_NOW`: time job was launched
* `HAMMERDB_TYPE`: type of sut dbms (postgresql, mysql, mariadb, citus)
* `HAMMERDB_RAMPUP`: rampup time in minutes before first Transaction Count is taken
* `HAMMERDB_DURATION`: duration in minutes before second Transaction Count is taken
* `HAMMERDB_ITERATIONS`: number of transactions before logging off
* `HAMMERDB_VUSERS`: number of vusers (threads)
* `HAMMERDB_MYSQL_ENGINE`: engine to be used by MySQL (default innodb)

This folder contains the Dockerfile for a data generator, that loads data into a DBMS.
