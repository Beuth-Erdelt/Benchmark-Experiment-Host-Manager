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
      * generates YCSB data = 1.000.000 rows
      * imports it into the DBMS
  * runs 1 stream of YCSB queries per DBMS
    * 1.000.000 operations
    * workload A = 50% read / 50% write
    * target throughput is `t` * 16384
  * with a maximum of 1 DBMS per time
* tests if results match workflow
* shows a summary

### Status

You can watch the status while benchmark is running via `bexperiments status`

```
|-----------------------|--------------|--------------|----------|---------------|-----------|--------------|---------------|
| 1705792604            | sut          |   loaded [s] | worker   | maintaining   | loading   | monitoring   | benchmarker   |
|=======================|==============|==============|==========|===============|===========|==============|===============|
| PostgreSQL-64-8-98304 | (1. Running) |         2.02 |          |               |           | (Running)    |               |
|-----------------------|--------------|--------------|----------|---------------|-----------|--------------|---------------|
```


### Evaluate Results

At the end of a benchmark you will see a summary like

```
### Loading
                        threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-1-16384        64   16384          1                   16189.612744                61768.0             1000000                            2681.000
PostgreSQL-64-8-16384        64   16384          8                   16290.460785                61423.0             1000000                            1914.875
PostgreSQL-64-1-32768        64   32768          1                   31790.437436                31456.0             1000000                            4291.000
PostgreSQL-64-8-32768        64   32768          8                   32382.512889                30905.0             1000000                            3568.375
PostgreSQL-64-1-49152        64   49152          1                   46988.065031                21282.0             1000000                            5839.000
PostgreSQL-64-8-49152        64   49152          8                   48297.297444                20734.0             1000000                            4505.250
PostgreSQL-64-1-65536        64   65536          1                   61195.765253                16341.0             1000000                           13919.000
PostgreSQL-64-8-65536        64   65536          8                   63976.271400                15698.0             1000000                            6979.500
PostgreSQL-64-1-81920        64   81920          1                   67686.476242                14774.0             1000000                           17999.000
PostgreSQL-64-8-81920        64   81920          8                   70846.906870                14443.0             1000000                           17417.000
PostgreSQL-64-1-98304        64   98304          1                   69463.739928                14396.0             1000000                           17583.000
PostgreSQL-64-8-98304        64   98304          8                   71737.729166                14223.0             1000000                           17561.000
PostgreSQL-64-1-114688       64  114688          1                   64964.594296                15393.0             1000000                           17439.000
PostgreSQL-64-8-114688       64  114688          8                   73400.511966                13901.0             1000000                           17617.000
PostgreSQL-64-1-131072       64  131072          1                   66755.674232                14980.0             1000000                           17311.000
PostgreSQL-64-8-131072       64  131072          8                   72717.753600                14027.0             1000000                           17657.000
### Execution
                          threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-1-16384-1        64   16384          1                   16213.499360                61677.0            499683                           337.000              500317                             515.000
PostgreSQL-64-8-16384-1        64   16384          8                   16290.459069                61395.0            499459                           405.750              500541                             654.625
PostgreSQL-64-1-32768-1        64   32768          1                   32121.289991                31132.0            499075                           428.000              500925                             734.000
PostgreSQL-64-8-32768-1        64   32768          8                   32389.983393                30894.0            499684                           376.375              500316                             623.375
PostgreSQL-64-1-49152-1        64   49152          1                   47481.126252                21061.0            500296                           432.000              499704                             839.000
PostgreSQL-64-8-49152-1        64   49152          8                   48290.849290                20735.0            499596                           480.625              500404                             847.125
PostgreSQL-64-1-65536-1        64   65536          1                   62814.070352                15920.0            500532                           494.000              499468                            1056.000
PostgreSQL-64-8-65536-1        64   65536          8                   63964.278070                15667.0            500037                           460.375              499963                             798.500
PostgreSQL-64-1-81920-1        64   81920          1                   77984.870935                12823.0            500074                           564.000              499926                            1296.000
PostgreSQL-64-8-81920-1        64   81920          8                   79493.727010                12606.0            499672                           544.375              500328                             964.750
PostgreSQL-64-1-98304-1        64   98304          1                   92310.532632                10833.0            500250                           661.000              499750                            1484.000
PostgreSQL-64-8-98304-1        64   98304          8                   94688.479434                10592.0            500164                           773.125              499836                            1429.125
PostgreSQL-64-1-114688-1       64  114688          1                  101626.016260                 9840.0            500292                           897.000              499708                            2525.000
PostgreSQL-64-8-114688-1       64  114688          8                  109414.770086                 9302.0            499729                          1016.000              500271                            1957.125
PostgreSQL-64-1-131072-1       64  131072          1                  112271.247334                 8907.0            499597                          1145.000              500403                            3639.000
PostgreSQL-64-8-131072-1       64  131072          8                  124446.118042                 8156.0            499575                          1300.250              500425                            3351.750
```

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

```
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
