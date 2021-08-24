# Image of the Query Executor Container

This image contains an instance of [DBMSBenchmarker](https://github.com/Beuth-Erdelt/DBMS-Benchmarker).

The container expects some environment variables:
* `$DBMSBENCHMARKER_CODE`: Code of the DBMSBenchmarker experiment.
* `$DBMSBENCHMARKER_CONNECTION`: Name of the connection (to the DBMS).
* `$DBMSBENCHMARKER_SLEEP`: Number of seconds to wait before starting the benchmarking.
* `$DBMSBENCHMARKER_CLIENT`: Number of parallel clients (i.e. Docker containers) for this connection.
* `$DBMSBENCHMARKER_START`: Start time for container to start benchmarking. This is for synching several containers.


This yields a run command as
```
CMD python ./benchmark.py run -b -d -w connection -mps -f /results/$DBMSBENCHMARKER_CODE -r /results/$DBMSBENCHMARKER_CODE -sf $DBMSBENCHMARKER_CONNECTION -cs -sl $DBMSBENCHMARKER_SLEEP -c "$DBMSBENCHMARKER_CONNECTION" -ca "$DBMSBENCHMARKER_ALIAS" -cf ${DBMSBENCHMARKER_CONNECTION}.config -ms $DBMSBENCHMARKER_CLIENT -st "$DBMSBENCHMARKER_START"
```
See [docs](https://github.com/Beuth-Erdelt/DBMS-Benchmarker) of DBMSBenchmarker for details.

## Build Commands

```
docker build -t perdelt/bexhoma:dbmsbenchmarker --no-cache .
docker push perdelt/bexhoma:dbmsbenchmarker
```
