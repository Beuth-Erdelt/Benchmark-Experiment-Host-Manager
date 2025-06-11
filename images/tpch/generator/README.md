# Generator for TPC-H data

The image is based on https://www.tpc.org/tpch/

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
* `STORE_RAW_DATA`: data should be stored in persistent volume (or only locally in /tmp)
* `STORE_RAW_DATA_RECREATE`: data should be removed and recreated, if it already exists
* `TRANSFORM_RAW_DATA`: clean raw data, i.e., remove last character per line
* `BEXHOMA_SYNCH_GENERATE`: generating starts only when all pods are ready

This folder contains the Dockerfile for a data generator, that generates data to (RAM) disk.

The Dockerfile expects `dbgen` and `dists.dss` in the current directory.
