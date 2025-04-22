# Benchbase

The image is based on https://github.com/cmu-db/benchbase

Currently, TPC-C is adapted for PostgreSQL here.

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
* `BENCHBASE_BENCH`: name of the benchmark. currently only tpcc is supported
* `BENCHBASE_PROFILE`: name of the dbms to be benchmarked. corresponds to a folder in the benchbase config
* `BENCHBASE_TARGET`: target throughput. if used, throughput will be throttled
* `BENCHBASE_TIME`: duration of the benchmark in seconds
* `BENCHBASE_TERMINALS`: number of client terminals to simulate, similar to threads
* `BENCHBASE_BATCHSIZE`: batchsize for batching queries to be sent to the dbms
* `BENCHBASE_ISOLATION`: isolation level, for example TRANSACTION_READ_COMMITTED
* `BENCHBASE_KEY_AND_THINK`: true = activate key and think time in tpcc (default false)
* `BENCHBASE_NEWCONNPERTXN`: true = reconnect after each transaction (default false)
* `BENCHBASE_YCSB_WEIGHTS`: YCSB weights of query types (read, insert, scan, update, delete, readmodifywrite)
* `BENCHBASE_YCSB_WORKLOAD`: YCSB workload (a, ..., f)


This folder contains two Dockerfiles:
1. a data generator, that loads data into a DBMS
1. a benchmarker, that runs the workload against a loaded DBMS
