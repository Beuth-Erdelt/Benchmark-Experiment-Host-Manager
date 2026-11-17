## Show Summary

### Workload
Benchbase Workload tpcc SF=4
* Type: benchbase
* Duration: 724s 
* Code: 1794841105
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 4. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking runs for 2 minutes. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [40] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 3 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* cockroachdb-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1277960
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:659577
    * datadisk:1714
    * cpu_list:0-127
  * worker 1
    * RAM:540579299328
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:222413
    * datadisk:1578
    * cpu_list:0-127
  * worker 2
    * RAM:540597886976
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:301742
    * datadisk:1508
    * cpu_list:0-255
  * resources_total: 12.25 CPU, 48.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794841105
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cockroachdb-1-1-2-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1277845
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:660304
    * datadisk:1809
    * cpu_list:0-127
  * worker 1
    * RAM:540579299328
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:222504
    * datadisk:1667
    * cpu_list:0-127
  * worker 2
    * RAM:540597886976
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:301833
    * datadisk:1597
    * cpu_list:0-255
  * resources_total: 12.25 CPU, 48.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794841105
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Init Scripts Not in Folder
* CockroachDB-1: skipped initschema-benchbase.sql

### Ingestion
* CockroachDB-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1794841105-97dd46f9c-g6c2m: 0
* bx-w-cr-1-1794841105-0: 0
* bx-w-cr-1-1794841105-1: 0
* bx-w-cr-1-1794841105-2: 0

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

| DBMS            |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| CockroachDB-1-1 |                1 |    4 |      145.00 |           1.00 |            0.00 |        142.00 |            2.00 |              1 |         1 |             | None           |             0 | False         |               99.31 | False               |

### Benchmarking

#### Per Connection

| connection            | phase             | job                 |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:------------------|:--------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| cockroachdb-1-1-1-1-1 | cockroachdb-1-1-1 | cockroachdb-1-1-1-1 |                1 |        1 |               1 |       1 |        40 |     1024 |          -1 | 120.00 |        0 |                         446.30 |                      444.54 |         0.00 |                                                     170197.00 |                                              89529.00 |
| cockroachdb-1-1-2-1-1 | cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |        2 |               1 |       1 |        40 |     1024 |          -1 | 120.00 |        0 |                          69.60 |                       69.71 |         0.00 |                                                    1417871.00 |                                             572453.00 |
| cockroachdb-1-1-2-1-2 | cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |        2 |               1 |       2 |        40 |     1024 |          -1 | 120.00 |        0 |                          70.83 |                       70.74 |         0.00 |                                                    1411518.00 |                                             562285.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:------------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| cockroachdb-1-1-1 | cockroachdb-1-1-1 |                1 |        1 |               1 |           1 |        40 |     1024 |          -1 | 120.00 |        0 |                         446.30 |                      444.54 |         0.00 |                                                     170197.00 |                                              89529.00 |
| cockroachdb-1-1-2 | cockroachdb-1-1-2 |                1 |        2 |               1 |           2 |        80 |     2048 |          -1 | 120.00 |        0 |                         140.43 |                      140.45 |         0.00 |                                                    1417871.00 |                                             567369.00 |

#### Reset

| phase             | job                 |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:------------------|:--------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| cockroachdb-1-1-1 | cockroachdb-1-1-1-1 |                1 |        1 |               1 |        12.00 |                |
| cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |        2 |               1 |        12.00 |                |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
* TEST passed: Reset scripts ran without errors
