# Example: YCSB

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

References:
1. https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload

## Perform Benchmark

For performing the experiment we can run the [ycsb file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/ycsb.py).

Example: `python ycsb.py -ms 4 -dbms PostgreSQL -workload a run`

This
* starts a clean instance of PostgreSQL
  * data directory inside a Docker container
* creates YCSB schema in each database
* starts `n` loader pods per DBMS
  * with a loading container each
    * generates YCSB data = 1.000.000 rows
    * imports it into the DBMS
* runs 1 stream of YCSB queries per DBMS
  * 1.000.000 operations
  * workload A = 50% read / 50% write
  * target throughput is `t` * 16384
* loops over `n` in [1,8] and `t` in [1,2,3,4,5,6,7,8]
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


### Evaluate Results in Dashboard

At the end of a benchmark you will see a summary like that

```
Connections:
MonetDB-BHT-8-1-1
MySQL-BHT-8-16-1-1
PostgreSQL-BHT-8-1-1
Queries:
0: Q1 = Pricing Summary Report (TPC-H Q1)
1: Q2 = Minimum Cost Supplier Query (TPC-H Q2)
2: Q3 = Shipping Priority (TPC-H Q3)
3: Q4 = Order Priority Checking Query (TPC-H Q4)
4: Q5 = Local Supplier Volume (TPC-H Q5)
5: Q6 = Forecasting Revenue Change (TPC-H Q6)
6: Q7 = Forecasting Revenue Change (TPC-H Q7)
7: Q8 = National Market Share (TPC-H Q8)
8: Q9 = Product Type Profit Measure (TPC-H Q9)
9: Q10 = Forecasting Revenue Change (TPC-H Q10)
10: Q11 = Important Stock Identification (TPC-H Q11)
11: Q12 = Shipping Modes and Order Priority (TPC-H Q12)
12: Q13 = Customer Distribution (TPC-H Q13)
13: Q14 = Forecasting Revenue Change (TPC-H Q14)
14: Q15 = Top Supplier Query (TPC-H Q15)
15: Q16 = Parts/Supplier Relationship (TPC-H Q16)
16: Q17 = Small-Quantity-Order Revenue (TPC-H Q17)
17: Q18 = Large Volume Customer (TPC-H Q18)
18: Q19 = Discounted Revenue (TPC-H Q19)
19: Q20 = Potential Part Promotion (TPC-H Q20)
20: Q21 = Suppliers Who Kept Orders Waiting Query (TPC-H Q21)
21: Q22 = Global Sales Opportunity Query (TPC-H Q22)
Load Evaluation
### Errors
     MonetDB-BHT-8-1-1  MySQL-BHT-8-16-1-1  PostgreSQL-BHT-8-1-1
Q1               False               False                 False
Q2               False               False                 False
Q3               False               False                 False
Q4               False               False                 False
Q5               False               False                 False
Q6               False               False                 False
Q7               False               False                 False
Q8               False               False                 False
Q9               False               False                 False
Q10              False               False                 False
Q11              False               False                 False
Q12              False               False                 False
Q13              False               False                 False
Q14              False               False                 False
Q15              False               False                 False
Q16              False               False                 False
Q17              False               False                 False
Q18              False               False                 False
Q19              False               False                 False
Q20              False               False                 False
Q21              False               False                 False
Q22              False               False                 False
### Warnings
     MonetDB-BHT-8-1-1  MySQL-BHT-8-16-1-1  PostgreSQL-BHT-8-1-1
Q1               False               False                 False
Q2               False               False                 False
Q3               False               False                 False
Q4               False               False                 False
Q5               False               False                 False
Q6               False               False                 False
Q7               False               False                 False
Q8               False               False                 False
Q9               False               False                 False
Q10              False               False                 False
Q11              False               False                 False
Q12              False               False                 False
Q13              False               False                 False
Q14              False               False                 False
Q15              False               False                 False
Q16              False               False                 False
Q17              False               False                 False
Q18              False               False                 False
Q19              False               False                 False
Q20              False               False                 False
Q21              False               False                 False
Q22              False               False                 False
### Geometric Mean of Medians of Timer Run [s]
DBMS             MonetDB-BHT-8-1-1  MySQL-BHT-8-16-1-1  PostgreSQL-BHT-8-1-1
total_timer_run                0.1                1.48                  0.56
MonetDB-BHT-8-1-1
MySQL-BHT-8-16-1-1
PostgreSQL-BHT-8-1-1
### Loading [s]
               MonetDB-BHT-8-1-1  MySQL-BHT-8-16-1-1  PostgreSQL-BHT-8-1-1
timeGenerate                1.00                1.00                  1.00
timeIngesting              10.00              108.00                 23.00
timeSchema                  0.95                5.10                  0.51
timeIndex                  17.07              496.56                 43.85
timeLoad                   46.02              627.65                 85.36
### Latency of Timer Execution [ms]
DBMS  MonetDB-BHT-8-1-1  MySQL-BHT-8-16-1-1  PostgreSQL-BHT-8-1-1
Q1           540.266769        13403.575217           1394.948800
Q2            32.445064          140.819682            235.456771
Q3           107.648707         1871.247458            472.850334
Q4            43.393589          771.850379            804.222555
Q5            53.208980         1433.090793            417.965981
Q6            23.235807         2102.604461            310.579344
Q7            67.450407         3430.779209            477.439999
Q8           187.965117         2688.095795            406.967678
Q9            81.846076         2499.057111            712.869145
Q10           97.086058         2082.182153            793.103422
Q11           18.448853          279.750079            155.313325
Q12           50.426757         3109.570189            622.492888
Q13          245.087787         3461.542013           1098.003893
Q14           35.918594         2320.781684            341.247769
Q15           29.761279        11305.257101            335.477490
Q16           66.997990          555.879030            343.637448
Q17           71.115009          321.034775           1165.672948
Q18          149.304385         2785.999462           3708.772301
Q19           69.044638          177.866275            435.700887
Q20           81.822519          304.060695            345.359304
Q21          872.301944         6716.680256            564.431586
Q22           52.956324          233.065151            150.500087
```
Detailed evaluations can be done using DBMSBenchmarker
* [Dashboard](https://dbmsbenchmarker.readthedocs.io/en/latest/Dashboard.html)
* [Jupyter Notebooks](https://beuth-erdelt.github.io/DBMS-Benchmarker/Evaluation-Demo.html)

You can connect to an evaluation server by `bexperiments dashboard`.
This forwards ports, so you have
* a dashboard in browser at http://localhost:8050
* a Jupyter notebook server at http://localhost:8888


## Adjust Parameter

### Manifests

The YAML manifests for the components can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/k8s

### SQL Scrips

The SQL scripts for pre and post ingestion can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch

### Dockerfiles

The Dockerfiles for the components can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/tpch

### Command line

You maybe want to adjust some of the parameters that are set in the file: `python tpch.py -h`

```
usage: tpch.py [-h] [-aws] [-dbms {PostgreSQL,MonetDB,MySQL}] [-lit LIMIT_IMPORT_TABLE] [-db] [-cx CONTEXT] [-e EXPERIMENT] [-d] [-m] [-mc] [-ms MAX_SUT] [-dt] [-md MONITORING_DELAY] [-nr NUM_RUN] [-nc NUM_CONFIG] [-ne NUM_QUERY_EXECUTORS]
               [-nls NUM_LOADING_SPLIT] [-nlp NUM_LOADING_PODS] [-nlt NUM_LOADING_THREADS] [-sf SCALING_FACTOR] [-t TIMEOUT] [-rr REQUEST_RAM] [-rc REQUEST_CPU] [-rct REQUEST_CPU_TYPE] [-rg REQUEST_GPU] [-rgt REQUEST_GPU_TYPE] [-rst {None,,local-hdd,shared}] [-rss REQUEST_STORAGE_SIZE] [-rnn REQUEST_NODE_NAME]
               [-tr] [-ii] [-ic] [-is] [-rcp RECREATE_PARAMETER]
               {profiling,run,start,load,empty}

Performs a TPC-H loading experiment. Data is generated and imported into a DBMS from a distributed filesystem.

positional arguments:
  {profiling,run,start,load,empty}
                        profile the import or run the TPC-H queries

options:
  -h, --help            show this help message and exit
  -aws, --aws           fix components to node groups at AWS
  -dbms {PostgreSQL,MonetDB,SingleStore,CockroachDB,MySQL,MariaDB,YugabyteDB,Kinetica}
                        DBMS to load the data
  -lit LIMIT_IMPORT_TABLE, --limit-import-table LIMIT_IMPORT_TABLE
                        limit import to one table, name of this table
  -db, --debug          dump debug informations
  -cx CONTEXT, --context CONTEXT
                        context of Kubernetes (for a multi cluster environment), default is current context
  -e EXPERIMENT, --experiment EXPERIMENT
                        sets experiment code for continuing started experiment
  -d, --detached        puts most of the experiment workflow inside the cluster
  -m, --monitoring      activates monitoring
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
  -nls NUM_LOADING_SPLIT, --num-loading-split NUM_LOADING_SPLIT
                        portion of loaders that should run in parallel
  -nlp NUM_LOADING_PODS, --num-loading-pods NUM_LOADING_PODS
                        total number of loaders per configuration
  -nlt NUM_LOADING_THREADS, --num-loading-threads NUM_LOADING_THREADS
                        total number of threads per loading process
  -sf SCALING_FACTOR, --scaling-factor SCALING_FACTOR
                        scaling factor (SF)
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
  -tr, --test-result    test if result fulfills some basic requirements
  -ii, --init-indexes   adds indexes to tables after ingestion
  -ic, --init-constraints
                        adds constraints to tables after ingestion
  -is, --init-statistics
                        recomputes statistics of tables after ingestion
  -rcp RECREATE_PARAMETER, --recreate-parameter RECREATE_PARAMETER
                        recreate parameter for randomized queries
```

## Monitoring

[monitoring](Monitoring.html)
