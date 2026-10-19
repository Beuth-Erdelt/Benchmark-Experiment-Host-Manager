## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1256s 
* Code: 1792377776
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.11.6.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 3 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* cockroachdb-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:567739
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:540590800896
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:147386
    * datadisk:691778
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-95
  * worker 1
    * RAM:540579299328
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:161811
    * datadisk:691638
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-127
  * worker 2
    * RAM:1077382627328
    * Cores:256
    * host:6.8.0-1060-nvidia
    * node:cl-worker28
    * disk:887042
    * datadisk:691499
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-255
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * eval_parameters
    * code:1792377776
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cockroachdb-1-1-2-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:567741
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:540590800896
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:147182
    * datadisk:691879
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-95
  * worker 1
    * RAM:540579299328
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:161936
    * datadisk:691808
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-127
  * worker 2
    * RAM:1077382627328
    * Cores:256
    * host:6.8.0-1060-nvidia
    * node:cl-worker28
    * disk:887214
    * datadisk:691670
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-255
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * eval_parameters
    * code:1792377776
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1792377776-8684988789-vc67q: 0
* bexhoma-worker-cockroachdb-benchbase-tpcc-16-0: 0
* bexhoma-worker-cockroachdb-benchbase-tpcc-16-1: 0
* bexhoma-worker-cockroachdb-benchbase-tpcc-16-2: 0

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

|                 |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| CockroachDB-1-1 |                1 |   16 |      242.00 |           3.00 |            0.00 |        237.00 |            2.00 |              1 |           1 |             | None           |             0 | False         |              238.02 | False               |

### Benchmarking

#### Per Connection

| DBMS                  | phase             | job                 |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:------------------|:--------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| cockroachdb-1-1-1-1-1 | cockroachdb-1-1-1 | cockroachdb-1-1-1-1 |                1 |          16 |    16384 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                         254.60 |                      253.55 |         0.00 |                                                     125014.00 |                                              62828.00 |
| cockroachdb-1-1-2-1-1 | cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       1 |          -1 | 300.00 |            0 |                          98.00 |                       97.62 |         0.00 |                                                     181082.00 |                                              81604.00 |
| cockroachdb-1-1-2-1-2 | cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       2 |          -1 | 300.00 |            0 |                          98.85 |                       98.43 |         0.00 |                                                     180352.00 |                                              80911.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:------------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| cockroachdb-1-1-1 | cockroachdb-1-1-1 |                1 |          16 |    16384 |               1 |           1 |          -1 | 300.00 |            0 |                         254.60 |                      253.55 |         0.00 |                                                     125014.00 |                                              62828.00 |
| cockroachdb-1-1-2 | cockroachdb-1-1-2 |                1 |          16 |    16384 |               1 |           2 |          -1 | 300.00 |            0 |                         196.85 |                      196.06 |         0.00 |                                                     181082.00 |                                              81257.50 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
