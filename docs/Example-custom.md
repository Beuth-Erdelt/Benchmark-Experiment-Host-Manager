# Example: Run a custom SQL workload

This example assumes you have
* a DBMS installed outside of bexhoma
* a database loaded
* a sequence of SQL queries you want to run against the database

## Prerequisites

This needs a dummy that stands for a DBMS managed by bexhoma, and a query file in a certain format.

### Dummy DBMS

Inside the `docker` section of the `cluster.config` define how to connect to the DBMS (keep key `Dummy` here, adjust all the rest):
```python
        'Dummy': {
            'loadData': '',
            'delay_prepare': 0,
            'template': {
                'version': 'v1.0',
                'alias': 'Dummy',
                'docker_alias': 'ABC',
                 'JDBC': {
                    'driver': "com.yugabyte.Driver",
                    'auth': ["yugabyte", ""],
                    'url': 'jdbc:yugabytedb://yb-tserver-service.perdelt.svc.cluster.local:5433/yugabyte?load-balance=true',
                    'jar': 'jdbc-yugabytedb-42.3.5-yb-2.jar'
                }
            },
            'logfile': '/usr/local/data/logfile',
            'datadir': '/var/lib/postgresql/data/',
            'priceperhourdollar': 0.0,
        },
```

### Queries File

Overwrite the file `queries.config` in `experiments/example` with a custom file.
For more details about the format see https://dbmsbenchmarker.readthedocs.io/en/latest/Options.html#query-file


## Run Experiment

Example: Run `python example.py run -dbms Dummy -ne 5 -xqr 100` to run experiment with 5 parallel benchmarkers and repeat each query 100 times.

## Background Information

1. The script installs a Dummy DBMS according to `k8s/deploymenttemplate-Dummy.yml`. This is just a lightweight busybox container running an endless sleep. Bexhoma writes status information about the components to the benchmarked DBMS container. A DBMS not managed by bexhoma therefore needs such a Dummy container. The container will be removed automatically after experiment has finished.

The DBMSBenchmarker Docker container needs to have the required JDBC driver included.

The JDBC drivers of the image are listed in its [Dockerfile](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/benchmarker_dbmsbenchmarker).

## Status and Evaluation

You can see the status of running experiments via `bexhoma status`

Finished experiments can be inspected locally or using the dashboard container.
`bexhoma dashboard` forwards to dashboard to `localhost:8888`.
You can connect to a Jupyter server there (password is admin).

There is a variety of evaluation tools included.
For example to compute the total throughput:
```python
from dbmsbenchmarker import *

resultfolder = "/results/"
code = "1234"

# load merged results
evaluate = inspector.inspector(resultfolder)
evaluate.load_experiment(code)

# read dict of benchmarking times per stream
list_connections = evaluate.get_experiment_list_connections()
benchmarker_times = evaluate.get_experiment_connection_properties(list_connections[0])['times']['total']

# compute min of start and max of end for timespan
times_start=[]
times_end=[]
for t in benchmarker_times:
    times_start.append(benchmarker_times[t]['time_start'])
    times_end.append(benchmarker_times[t]['time_end'])

time_start = min(times_start)
time_end = max(times_end)
print(time_start, time_end, time_end-time_start)
```
might print something like `1691160697 1691160833 136` (total time of 136 seconds).

The dict `benchmarker_times` contains (for 20 parallel benchmarkers) something like
```bash
Dummy-BHT-1-1-1-9
  time_start:1691160740
  time_end:1691160741
Dummy-BHT-1-1-1-19
  time_start:1691160825
  time_end:1691160826
Dummy-BHT-1-1-1-6
  time_start:1691160717
  time_end:1691160719
Dummy-BHT-1-1-1-20
  time_start:1691160831
  time_end:1691160833
Dummy-BHT-1-1-1-5
  time_start:1691160716
  time_end:1691160718
Dummy-BHT-1-1-1-12
  time_start:1691160759
  time_end:1691160761
Dummy-BHT-1-1-1-17
  time_start:1691160802
  time_end:1691160804
Dummy-BHT-1-1-1-10
  time_start:1691160742
  time_end:1691160744
Dummy-BHT-1-1-1-3
  time_start:1691160703
  time_end:1691160705
Dummy-BHT-1-1-1-8
  time_start:1691160730
  time_end:1691160732
Dummy-BHT-1-1-1-11
  time_start:1691160751
  time_end:1691160753
Dummy-BHT-1-1-1-15
  time_start:1691160782
  time_end:1691160784
Dummy-BHT-1-1-1-4
  time_start:1691160709
  time_end:1691160711
Dummy-BHT-1-1-1-7
  time_start:1691160727
  time_end:1691160728
Dummy-BHT-1-1-1-2
  time_start:1691160699
  time_end:1691160700
Dummy-BHT-1-1-1-16
  time_start:1691160791
  time_end:1691160792
Dummy-BHT-1-1-1-13
  time_start:1691160767
  time_end:1691160769
Dummy-BHT-1-1-1-1
  time_start:1691160697
  time_end:1691160698
Dummy-BHT-1-1-1-14
  time_start:1691160778
  time_end:1691160779
Dummy-BHT-1-1-1-18
  time_start:1691160821
  time_end:1691160823
```


