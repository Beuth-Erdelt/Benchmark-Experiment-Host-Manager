# Benchbase

The image is based on https://github.com/cmu-db/benchbase

Currently, TPC-C is adapted for PostgreSQL here.

The following parameter (ENV) have been added:

* `SF`: scaling factor (e.g., number of warehouses)
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
* `BENCHBASE_BENCH`: name of the benchmark. currently only tpcc is supported
* `BENCHBASE_PROFILE`: name of the dbms to be benchmarked. corresponds to a folder in the benchbase config
* `BENCHBASE_TARGET`: target throughput. if used, throughput will be throttled
* `BENCHBASE_TIME`: duration of the benchmark in seconds
* `BENCHBASE_TERMINALS`: number of client terminals to simulate, similar to threads
* `BENCHBASE_BATCHSIZE`: batchsize for batching queries to be sent to the dbms
* `BENCHBASE_ISOLATION`: isolation level, for example TRANSACTION_READ_COMMITTED
* `BENCHBASE_KEY_AND_THINK`: true = activate key and think time in tpcc (default false)
* `BENCHBASE_NEWCONNPERTXN`: true = reconnect after each transaction (default false)
* `BENCHBASE_YCSB_WEIGHTS`: YCSB weights of query types (read, insert, scan, update, delete, readmodifywrite). This is set via `BENCHBASE_YCSB_WORKLOAD`.
* `BENCHBASE_YCSB_WORKLOAD`: YCSB workload (a, ..., f)
* `BENCHBASE_STATUS_INTERVAL`: log status every x milliseconds.
* `BENCHBASE_CREATE_SCHEMA`: if 1, schema will be created. Set to 0, if schema is created outside of these containers.

This folder contains two Dockerfiles:
1. a data generator, that loads data into a DBMS
1. a benchmarker, that runs the workload against a loaded DBMS
