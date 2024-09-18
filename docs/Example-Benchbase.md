# Example: Benchbase

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

> TPC-C involves a mix of five concurrent transactions of different types and complexity either executed on-line or queued for deferred execution. The database is comprised of nine types of tables with a wide range of record and population sizes. TPC-C is measured in transactions per minute (tpmC). While the benchmark portrays the activity of a wholesale supplier, TPC-C is not limited to the activity of any particular business segment, but, rather represents any industry that must manage, sell, or distribute a product or service.

<img src="https://raw.githubusercontent.com/wiki/cmu-db/benchbase/img/tpcc.png" alt="drawing" width="600"/>

References:
1. https://github.com/cmu-db/benchbase/wiki/TPC-C
1. http://www.vldb.org/pvldb/vol7/p277-difallah.pdf


## Perform Benchmark

For performing the experiment we can run the [benchbase file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/benchbase.py).

Example:
```
python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms PostgreSQL \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  run
```

This
* starts a clean instance of PostgreSQL (`-dbms`)
  * data directory inside a Docker container
* starts 1 loader pod (per DBMS) that
  * creates TPC-C schema in the database
  * imports data for 16 (`-sf`) warehouses into the DBMS
  * using all threads of driver machine (benchbase setting)
* runs streams of TPC-C queries (per DBMS)
    * running for 5 (`-sd`) minutes
    * each stream (pod) having 16 threads to simulate 16 users (`-nbt`)
    * `-nbp`: first stream 1 pos, second stream 2 pods (8 threads each)
    * target is 16x(`-ltf`) 1024 (`-tb`) ops
* with a maximum of 1 DBMS per time (`-ms`)
* tests if results match workflow (`-tr`)
* shows a summary

### Status

You can watch the status while benchmark is running via `bexperiments status`

```
Dashboard: Running
Cluster Prometheus: Running
Message Queue: Running
Data directory: Running
Result directory: Running
+---------------------+--------------+--------------+----------------+-----------------------------+
| 1726658756          | sut          |   loaded [s] | use case       | benchmarker                 |
+=====================+==============+==============+================+=============================+
| PostgreSQL-1-1-1024 | (1. Running) |           62 | benchbase_tpcc | (2. Succeeded) (2. Running) |
+---------------------+--------------+--------------+----------------+-----------------------------+
```

The code `1726658756` is the unique identifier of the experiment.
You can find the number also in the output of `benchbase.py`.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1726658756` (removes everything that is related to experiment `1726658756`).

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

To see the summary of experiment `1726658756` you can simply call `python benchbase.py -e 1726658756 summary`.

### Detailed Evaluation

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

The SQL scripts for pre and post ingestion can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/benchbase

### Dockerfiles

The Dockerfiles for the components can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/benchbase

### Command line

You maybe want to adjust some of the parameters that are set in the file: `python hammerdb.py -h`

```bash
usage: benchbase.py [-h] [-aws] [-dbms {PostgreSQL,MySQL,MariaDB,YugabyteDB}] [-db] [-cx CONTEXT] [-e EXPERIMENT] [-m] [-mc] [-ms MAX_SUT] [-nc NUM_CONFIG] [-ne NUM_QUERY_EXECUTORS] [-nlp NUM_LOADING_PODS]
                    [-nlt NUM_LOADING_THREADS] [-nbp NUM_BENCHMARKING_PODS] [-nbt NUM_BENCHMARKING_THREADS] [-nbf NUM_BENCHMARKING_TARGET_FACTORS] [-sf SCALING_FACTOR] [-sd SCALING_DURATION] [-t TIMEOUT]
                    [-rr REQUEST_RAM] [-rc REQUEST_CPU] [-rct REQUEST_CPU_TYPE] [-rg REQUEST_GPU] [-rgt REQUEST_GPU_TYPE] [-rst {None,,local-hdd,shared}] [-rss REQUEST_STORAGE_SIZE]
                    [-rnn REQUEST_NODE_NAME] [-rnl REQUEST_NODE_LOADING] [-rnb REQUEST_NODE_BENCHMARKING] [-tr] [-b {tpcc,twitter}] [-tb TARGET_BASE]
                    {run,start,load}

Perform TPC-C inspired benchmarks based on Benchbase in a Kubernetes cluster. Optionally monitoring is actived. User can also choose some parameters like number of warehouses and request some resources.

positional arguments:
  {run,start,load}      start sut, also load data or also run the TPC-C queries

options:
  -h, --help            show this help message and exit
  -aws, --aws           fix components to node groups at AWS
  -dbms {PostgreSQL,MySQL,MariaDB,YugabyteDB}, --dbms {PostgreSQL,MySQL,MariaDB,YugabyteDB}
                        DBMS to load the data
  -db, --debug          dump debug informations
  -cx CONTEXT, --context CONTEXT
                        context of Kubernetes (for a multi cluster environment), default is current context
  -e EXPERIMENT, --experiment EXPERIMENT
                        sets experiment code for continuing started experiment
  -m, --monitoring      activates monitoring for sut
  -mc, --monitoring-cluster
                        activates monitoring for all nodes of cluster
  -ms MAX_SUT, --max-sut MAX_SUT
                        maximum number of parallel DBMS configurations, default is no limit
  -nc NUM_CONFIG, --num-config NUM_CONFIG
                        number of runs per configuration
  -ne NUM_QUERY_EXECUTORS, --num-query-executors NUM_QUERY_EXECUTORS
                        comma separated list of number of parallel clients
  -nlp NUM_LOADING_PODS, --num-loading-pods NUM_LOADING_PODS
                        total number of loaders per configuration
  -nlt NUM_LOADING_THREADS, --num-loading-threads NUM_LOADING_THREADS
                        total number of threads per loading process
  -nbp NUM_BENCHMARKING_PODS, --num-benchmarking-pods NUM_BENCHMARKING_PODS
                        comma separated list of number of benchmarkers per configuration
  -nbt NUM_BENCHMARKING_THREADS, --num-benchmarking-threads NUM_BENCHMARKING_THREADS
                        total number of threads per benchmarking process
  -nbf NUM_BENCHMARKING_TARGET_FACTORS, --num-benchmarking-target-factors NUM_BENCHMARKING_TARGET_FACTORS
                        comma separated list of factors of 16384 ops as target - default range(1,9)
  -sf SCALING_FACTOR, --scaling-factor SCALING_FACTOR
                        scaling factor (SF) = number of warehouses
  -sd SCALING_DURATION, --scaling-duration SCALING_DURATION
                        scaling factor = duration in minutes
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
  -b {tpcc,twitter}, --benchmark {tpcc,twitter}
                        type of benchmark
  -tb TARGET_BASE, --target-base TARGET_BASE
                        ops as target, base for factors - default 1024 = 2**10
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

This gives a survey about CPU (in CPU seconds) and RAM usage (in Gb) during loading and execution of the benchmark.

In this example, metrics are very instable. Metrics are fetched every 30 seconds.
This is too coarse for such a quick example.


## Use Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.

Example: `python benchbase.py -dbms PostgreSQL -nvu '8' -su 16 -sf 16 -nbp 1 -sd 5 -nc 2 -rst local-hdd -rss 50Gi run`

The following status shows we have two volumes of type `local-hdd`. Every experiment running HammerDB's TPC-C of SF=16 (warehouses) will take the databases from these volumes and skip loading.
In this example `-nc` is set to two, that is the complete experiment is repeated twice for statistical confidence.
The first instance of PostgreSQL mounts the volume and generates the data.
All other instances just use the database without generating and loading data.

```
+------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| Volumes                            | configuration   | experiment   | loaded [s]   |   timeLoading [s] | dbms       | storage_class_name   | storage   | status   | size   | used   |
+====================================+=================+==============+==============+===================+============+======================+===========+==========+========+========+
| bexhoma-storage-postgresql-ycsb-1  | postgresql      | ycsb-1       | True         |                64 | PostgreSQL | shared               | 50Gi      | Bound    | 50G    | 2.1G   |
+------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
+------------------+--------------+--------------+--------------------------+

+------------------+--------------+--------------+--------------+---------------+
| 1706957093       | sut          |   loaded [s] | monitoring   | benchmarker   |
+==================+==============+==============+==============+===============+
| MySQL-64-1-16384 | (2. Running) |      2398.11 | (Running)    | (1. Running)  |
+------------------+--------------+--------------+--------------+---------------+
```




