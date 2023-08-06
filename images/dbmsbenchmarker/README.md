# Image of the Query Executor Container

This image contains an instance of [DBMSBenchmarker](https://github.com/Beuth-Erdelt/DBMS-Benchmarker).

The container expects some environment variables:
* `$DBMSBENCHMARKER_CODE`: Code of the DBMSBenchmarker experiment.
* `$DBMSBENCHMARKER_CONNECTION`: Name of the connection (to the DBMS).
* `$DBMSBENCHMARKER_SLEEP`: Number of seconds to wait before starting the benchmarking.
* `$DBMSBENCHMARKER_CLIENT`: Number of parallel clients (i.e. Docker containers) for this connection.
* `$DBMSBENCHMARKER_START`: Start time for container to start benchmarking. This is for synching several containers.
* `$DBMSBENCHMARKER_RECREATE_PARAMETER`: 
* `$DBMSBENCHMARKER_VERBOSE`: 
* `$DBMSBENCHMARKER_DEV`: 
* `$DBMSBENCHMARKER_NOW`: 
* `$DBMSBENCHMARKER_SHUFFLE_QUERIES`: 

See [docs](https://github.com/Beuth-Erdelt/DBMS-Benchmarker) of DBMSBenchmarker for details.
