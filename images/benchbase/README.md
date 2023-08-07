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
* `BENCHBASE_BENCH`: 
* `BENCHBASE_PROFILE`: 
* `BENCHBASE_TARGET`: 
* `BENCHBASE_TIME`: 
* `BENCHBASE_TERMINALS`: 
* `BENCHBASE_BATCHSIZE`: 
* `BENCHBASE_ISOLATION`: 

This folder contains two Dockerfiles:
1. a data generator, that loads data into a DBMS
1. a benchmarker, that runs the workload against a loaded DBMS
