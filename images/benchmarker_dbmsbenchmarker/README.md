# Image of the Query Executor Container

This image contains an instance of [DBMSBenchmarker](https://github.com/Beuth-Erdelt/DBMS-Benchmarker).

The container expects some environment variables:
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
* `DBMSBENCHMARKER_ALIAS`: alias name for the dbms
* `DBMSBENCHMARKER_SLEEP`: number of seconds to wait before starting the benchmarking.
* `DBMSBENCHMARKER_RECREATE_PARAMETER`: should the parameters of queries be recreated for each stream
* `DBMSBENCHMARKER_VERBOSE`: show more output
* `DBMSBENCHMARKER_DEV`: switch to dev channel and show debug output
* `DBMSBENCHMARKER_SHUFFLE_QUERIES`: shuffle the queries, i.e., do not follow natural ordering
* `DBMSBENCHMARKER_TESTRUN`: deprecated

See [docs](https://github.com/Beuth-Erdelt/DBMS-Benchmarker) of DBMSBenchmarker for details.
