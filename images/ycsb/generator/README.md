# Generator for YCSB data

The image is based on https://github.com/brianfrankcooper/YCSB

Currently, TPC-C is adapted for PostgreSQL, MySQL, MariaDB, SingleStore, Kinetica and YugabyteDB here.
It requires the JDBC driver to be included.

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
* `YCSB_THREADCOUNT`: 
* `YCSB_TARGET`: 
* `YCSB_STATUS_INTERVAL`: 
* `YCSB_STATUS`: 
* `YCSB_WORKLOAD`: 
* `YCSB_BATCHSIZE`: 

This folder contains the Dockerfile for a data generator, that loads data into a DBMS.
