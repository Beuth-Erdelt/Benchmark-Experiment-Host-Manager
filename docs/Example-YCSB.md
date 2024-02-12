# Example: YCSB

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

References:
1. https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload

## Perform Benchmark

For performing the experiment we can run the [ycsb file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/ycsb.py).

Example: `python ycsb.py -ms 1 -dbms PostgreSQL -workload a -tr run`

This
* loops over `n` in [1,8] and `t` in [1,2,3,4,5,6,7,8]
  * starts a clean instance of PostgreSQL
    * data directory inside a Docker container
  * creates YCSB schema in each database
  * starts `n` loader pods per DBMS
    * with a loading container each
      * threads = 64/`n`
      * target throughput is `t` * 16384
      * generates YCSB data = 1.000.000 rows (i.e., SF=1)
      * imports it into the DBMS
  * runs `n` parallel streams of YCSB queries per DBMS
    * 1.000.000 operations
    * workload A = 50% read / 50% write
    * target throughput is `t` * 16384
  * with a maximum of 1 DBMS per time
* tests if results match workflow
* shows a summary

### Status

You can watch the status while benchmark is running via `bexperiments status`

```
Dashboard: Running
Message Queue: Running
Data directory: Running
Result directory: Running
+------------------------+--------------+--------------+-------------+--------------+
| 1706264335             | sut          |   loaded [s] | loading     | monitoring   |
+========================+==============+==============+=============+==============+
| PostgreSQL-64-1-131072 | (1. Running) |         0.64 | (1 Running) | (Running)    |
+------------------------+--------------+--------------+-------------+--------------+
```

The code `1706264335` is the unique identifier of the experiment.
You can find the number also in the output of `ycsb.py`.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1706264335` (removes everything that is related to experiment `1706264335`).

## Evaluate Results

At the end of a benchmark you will see a summary like

```bash
### Loading
                        threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-1-16384        64   16384          1                   16285.849226                61403.0             1000000                             1283.00
PostgreSQL-64-8-16384        64   16384          8                   16189.808395                62334.0             1000000                             1029.25
PostgreSQL-64-1-32768        64   32768          1                   32334.206357                30927.0             1000000                             2993.00
PostgreSQL-64-8-32768        64   32768          8                   32487.310483                30788.0             1000000                             2362.50
PostgreSQL-64-1-49152        64   49152          1                   47429.330298                21084.0             1000000                             4343.00
PostgreSQL-64-8-49152        64   49152          8                   48401.920774                20850.0             1000000                             3848.50
PostgreSQL-64-1-65536        64   65536          1                   63881.436055                15654.0             1000000                             6127.00
PostgreSQL-64-8-65536        64   65536          8                   64436.143011                15540.0             1000000                             4843.00
PostgreSQL-64-1-81920        64   81920          1                   71078.257161                14069.0             1000000                             6219.00
PostgreSQL-64-8-81920        64   81920          8                   72415.868804                14361.0             1000000                             5296.00
PostgreSQL-64-1-98304        64   98304          1                   81586.032471                12257.0             1000000                             5027.00
PostgreSQL-64-8-98304        64   98304          8                   86657.160474                11681.0             1000000                             5571.00
PostgreSQL-64-1-114688       64  114688          1                   74693.755602                13388.0             1000000                             5923.00
PostgreSQL-64-8-114688       64  114688          8                   80616.643342                13037.0             1000000                             5275.50
PostgreSQL-64-1-131072       64  131072          1                   81766.148814                12230.0             1000000                             6087.00
PostgreSQL-64-8-131072       64  131072          8                   80708.979092                12469.0             1000000                             5656.00

### Execution
                          threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-1-16384-1        64   16384          1                       16281.61                61419.0            499663                            540.00              500337                              743.00
PostgreSQL-64-8-16384-1        64   16384          8                       16313.68                61310.0            500621                            544.75              499379                              759.38
PostgreSQL-64-1-32768-1        64   32768          1                       32171.93                31083.0            500316                            570.00              499684                              925.00
PostgreSQL-64-8-32768-1        64   32768          8                       32481.38                30794.0            500704                            594.88              499296                              839.75
PostgreSQL-64-1-49152-1        64   49152          1                       48351.22                20682.0            499465                            808.00              500535                             1395.00
PostgreSQL-64-8-49152-1        64   49152          8                       48521.04                20624.0            500275                            946.75              499725                             1554.88
PostgreSQL-64-1-65536-1        64   65536          1                       62468.77                16008.0            499253                           1069.00              500747                             1656.00
PostgreSQL-64-8-65536-1        64   65536          8                       64434.09                15541.0            500305                           1056.00              499695                             1617.00
PostgreSQL-64-1-81920-1        64   81920          1                       78659.64                12713.0            500203                           1313.00              499797                             2055.00
PostgreSQL-64-8-81920-1        64   81920          8                       79285.81                12740.0            500409                           1337.38              499591                             2126.25
PostgreSQL-64-1-98304-1        64   98304          1                       89421.44                11183.0            499133                           1425.00              500867                             2767.00
PostgreSQL-64-8-98304-1        64   98304          8                       87541.47                11748.0            500122                           1363.75              499878                             2414.00
PostgreSQL-64-1-114688-1       64  114688          1                      101770.81                 9826.0            500000                           1351.00              500000                             2213.00
PostgreSQL-64-8-114688-1       64  114688          8                      104663.23                 9835.0            500450                           1515.62              499550                             2866.25
PostgreSQL-64-1-131072-1       64  131072          1                       88354.83                11318.0            499788                           1566.00              500212                             3451.00
PostgreSQL-64-8-131072-1       64  131072          8                      115356.26                 9250.0            500084                           1526.75              499916                             3356.75
```

We can see that the overall throughput is close to the target and that scaled-out drivers (8 pods with 8 threads each) have similar results as a monolithic driver (1 pod with 64 thread).
The runtime is between 8 seconds and 1 minute.

Results are transformed into pandas DataFrames and can be inspected in detail.
See for example
* [Jupyter Notebooks](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/evaluator_dbmsbenchmarker/notebooks/)

You can connect to an evaluation server in the cluster by `bexperiments dashboard`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888

You can connect to an evaluation server locally by `bexperiments jupyter`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888

## Adjust Parameters

The script supports
* exact repetitions for statistical confidence
* variations to scan a large parameters space
* combine results for easy evaluation

There are various ways to change parameters.

### Manifests

The YAML manifests for the components can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/k8s

### SQL Scrips

The SQL scripts for pre and post ingestion can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb

### Dockerfiles

The Dockerfiles for the components can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/ycsb

### Command line

You maybe want to adjust some of the parameters that are set in the file: `python ycsb.py -h`

```bash
usage: ycsb.py [-h] [-aws] [-dbms {PostgreSQL,MySQL}] [-workload {a,b,c,d,e,f}] [-db] [-cx CONTEXT] [-e EXPERIMENT] [-d] [-m] [-mc] [-ms MAX_SUT] [-dt] [-md MONITORING_DELAY] [-nr NUM_RUN] [-nc NUM_CONFIG] [-ne NUM_QUERY_EXECUTORS] [-nl NUM_LOADING]
               [-nlp NUM_LOADING_PODS] [-sf SCALING_FACTOR] [-sfo SCALING_FACTOR_OPERATIONS] [-su SCALING_USERS] [-sbs SCALING_BATCHSIZE] [-ltf LIST_TARGET_FACTORS] [-tb TARGET_BASE] [-t TIMEOUT] [-rr REQUEST_RAM] [-rc REQUEST_CPU] [-rct REQUEST_CPU_TYPE] [-rg REQUEST_GPU] [-rgt REQUEST_GPU_TYPE]
               [-rst {None,,local-hdd,shared}] [-rss REQUEST_STORAGE_SIZE] [-rnn REQUEST_NODE_NAME] [-rnl REQUEST_NODE_LOADING] [-rnb REQUEST_NODE_BENCHMARKING] [-tr]
               {run,start,load}

Perform YCSB benchmarks in a Kubernetes cluster. Number of rows and operations is SF*1,000,000. Optionally monitoring is activated.

positional arguments:
  {run,start,load}      import YCSB data or run YCSB queries

options:
  -h, --help            show this help message and exit
  -aws, --aws           fix components to node groups at AWS
  -dbms {PostgreSQL,MonetDB,SingleStore,CockroachDB,MySQL,MariaDB,YugabyteDB,Kinetica}
                        DBMS to load the data
  -workload {a,b,c,d,e,f}
                        YCSB default workload
  -db, --debug          dump debug informations
  -cx CONTEXT, --context CONTEXT
                        context of Kubernetes (for a multi cluster environment), default is current context
  -e EXPERIMENT, --experiment EXPERIMENT
                        sets experiment code for continuing started experiment
  -d, --detached        puts most of the experiment workflow inside the cluster
  -m, --monitoring      activates monitoring for sut
  -mc, --monitoring-cluster
                        activates monitoring for all nodes of cluster
  -ms MAX_SUT, --max-sut MAX_SUT
                        maximum number of parallel DBMS configurations, default is no limit
  -dt, --datatransfer   activates datatransfer
  -md MONITORING_DELAY, --monitoring-delay MONITORING_DELAY
                        time to wait [s] before execution of the runs of a query
  -nr NUM_RUN, --num-run NUM_RUN
                        number of runs per query
  -nc NUM_CONFIG, --num-config NUM_CONFIG
                        number of runs per configuration
  -ne NUM_QUERY_EXECUTORS, --num-query-executors NUM_QUERY_EXECUTORS
                        comma separated list of number of parallel clients
  -nl NUM_LOADING, --num-loading NUM_LOADING
                        number of parallel loaders per configuration
  -nlp NUM_LOADING_PODS, --num-loading-pods NUM_LOADING_PODS
                        total number of loaders per configuration
  -sf SCALING_FACTOR, --scaling-factor SCALING_FACTOR
                        scaling factor (SF) = number of rows in millions
  -sfo SCALING_FACTOR_OPERATIONS, --scaling-factor-operations SCALING_FACTOR_OPERATIONS
                        scaling factor (SF) = number of operations in millions (=SF if not set)
  -su SCALING_USERS, --scaling-users SCALING_USERS
                        scaling factor = number of total threads
  -sbs SCALING_BATCHSIZE, --scaling-batchsize SCALING_BATCHSIZE
                        batch size
  -ltf LIST_TARGET_FACTORS, --list-target-factors LIST_TARGET_FACTORS
                        comma separated list of factors of 16384 ops as target - default range(1,9)
  -tb TARGET_BASE, --target-base TARGET_BASE
                        ops as target, base for factors - default 16384 = 2**14
  -t TIMEOUT, --timeout TIMEOUT
                        timeout for a run of a query
  -rr REQUEST_RAM, --request-ram REQUEST_RAM
                        request ram
  -rc REQUEST_CPU, --request-cpu REQUEST_CPU
                        request cpus
  -rct REQUEST_CPU_TYPE, --request-cpu-type REQUEST_CPU_TYPE
                        request node having node label cpu=
  -rg REQUEST_GPU, --request-gpu REQUEST_GPU
                        request number of gpus
  -rgt REQUEST_GPU_TYPE, --request-gpu-type REQUEST_GPU_TYPE
                        request node having node label gpu=
  -rst {None,,local-hdd,shared}, --request-storage-type {None,,local-hdd,shared}
                        request persistent storage of certain type
  -rss REQUEST_STORAGE_SIZE, --request-storage-size REQUEST_STORAGE_SIZE
                        request persistent storage of certain size
  -rnn REQUEST_NODE_NAME, --request-node-name REQUEST_NODE_NAME
                        request a specific node
  -rnl REQUEST_NODE_LOADING, --request-node-loading REQUEST_NODE_LOADING
                        request a specific node
  -rnb REQUEST_NODE_BENCHMARKING, --request-node-benchmarking REQUEST_NODE_BENCHMARKING
                        request a specific node
  -tr, --test-result    test if result fulfills some basic requirements
```

## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).

If monitoring is activated, the summary also contains a section like

```bash
### Ingestion
                          SUT - CPU of Ingestion (via counter) [CPUs]  SUT - Max RAM of Ingestion [Gb]
PostgreSQL-64-1-16384-1                                        211.08                             3.56
PostgreSQL-64-1-32768-1                                        208.34                             3.51
PostgreSQL-64-1-49152-1                                         43.55                             2.78
PostgreSQL-64-1-65536-1                                         95.57                             3.16
PostgreSQL-64-1-81920-1                                        224.71                             3.50
PostgreSQL-64-1-98304-1                                        208.72                             3.50
PostgreSQL-64-1-114688-1                                        39.80                             2.74
PostgreSQL-64-1-131072-1                                       142.15                             3.47
PostgreSQL-64-8-16384-1                                        192.93                             3.51
PostgreSQL-64-8-32768-1                                        185.90                             3.50
PostgreSQL-64-8-49152-1                                        191.40                             3.81
PostgreSQL-64-8-65536-1                                        189.31                             3.77
PostgreSQL-64-8-81920-1                                        141.00                             3.46
PostgreSQL-64-8-98304-1                                        117.22                             3.28
PostgreSQL-64-8-114688-1                                       209.95                             3.50
PostgreSQL-64-8-131072-1                                       208.55                             3.50

### Execution
                          SUT - CPU of Execution (via counter) [CPUs]  SUT - Max RAM of Execution [Gb]
PostgreSQL-64-1-16384-1                                        158.03                             4.02
PostgreSQL-64-1-32768-1                                        171.52                             4.02
PostgreSQL-64-1-49152-1                                        131.15                             3.98
PostgreSQL-64-1-65536-1                                        185.56                             3.68
PostgreSQL-64-1-81920-1                                          0.00                             3.50
PostgreSQL-64-1-98304-1                                          0.00                             3.50
PostgreSQL-64-1-114688-1                                         0.00                             3.50
PostgreSQL-64-1-131072-1                                         0.00                             3.50
PostgreSQL-64-8-16384-1                                        122.51                             3.98
PostgreSQL-64-8-32768-1                                        110.22                             3.97
PostgreSQL-64-8-49152-1                                        163.70                             4.00
PostgreSQL-64-8-65536-1                                          0.00                             3.50
PostgreSQL-64-8-81920-1                                        169.54                             4.00
PostgreSQL-64-8-98304-1                                         66.88                             3.92
PostgreSQL-64-8-114688-1                                       190.45                             3.69
PostgreSQL-64-8-131072-1                                       146.15                             4.02
```

This gives a survey about CPU (in CPU seconds) and RAM usage (in Mb) during loading and execution of the benchmark.

In this example, metrics are very instable. Metrics are fetched every 30 seconds.
This is too coarse for such a quick example.

## Perform Execution Benchmark

The default behaviour of bexhoma is that several different settings of the loading component are compared.
We might only want to benchmark the workloads of YCSB in different configurations and have a fixed loading phase.

For performing the experiment we can run the [ycsb file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/ycsb.py).

Example: `python ycsb.py -ms 1 -dbms PostgreSQL -workload a -tr run`


## Use Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.

Example: `python ycsb.py -ms 1 -m -dbms MySQL -workload a -tr -nc 2 -rst local-hdd -rss 50Gi run`

The following status shows we have two volumes of type `local-hdd`. Every experiment running YCSB of SF=1, if it's MySQL or PostgreSQL, will take the databases from these volumes and skip loading.
In this example `-nc` is set to two, that is the complete experiment is repeated twice for statistical confidence.
The first instance of MySQL mounts the volume and generates the data.
All other instances just use the database without generating and loading data.

```
+-----------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+
| Volumes                           | configuration   | experiment   | loaded [s]   |   timeLoading [s] | dbms       | storage_class_name   |   storage | status   |
+===================================+=================+==============+==============+===================+============+======================+===========+==========+
| bexhoma-storage-mysql-ycsb-1      | mysql           | ycsb-1       | True         |           2398.11 | MySQL      | local-hdd            |      50Gi | Bound    |
+-----------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+
| bexhoma-storage-postgresql-ycsb-1 | postgresql      | ycsb-1       | True         |             61.82 | PostgreSQL | local-hdd            |      50Gi | Bound    |
+-----------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+
+------------------+--------------+--------------+--------------+---------------+
| 1706957093       | sut          |   loaded [s] | monitoring   | benchmarker   |
+==================+==============+==============+==============+===============+
| MySQL-64-1-16384 | (2. Running) |      2398.11 | (Running)    | (1. Running)  |
+------------------+--------------+--------------+--------------+---------------+
```




