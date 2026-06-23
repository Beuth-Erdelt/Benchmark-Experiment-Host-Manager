## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1186s 
* Code: 1782151798
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.18.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* CockroachDB-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:219927
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:838989
    * datadisk:705754
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-223
  * worker 1
    * RAM:1081649803264
    * Cores:56
    * host:6.8.0-111-generic
    * node:cl-worker34
    * disk:312783
    * datadisk:705551
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-55
  * worker 2
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1338923
    * datadisk:705546
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-255
  * eval_parameters
    * code:1782151798
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* CockroachDB-1-1-2-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:219927
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:839257
    * datadisk:706027
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-223
  * worker 1
    * RAM:1081649803264
    * Cores:56
    * host:6.8.0-111-generic
    * node:cl-worker34
    * disk:313045
    * datadisk:705812
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-55
  * worker 2
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1339188
    * datadisk:705810
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-255
  * eval_parameters
    * code:1782151798
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

|                 |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:----------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| CockroachDB-1-1 |                1 |   16 |      349.00 |           2.00 |            0.00 |        155.00 |          192.00 |              1 |           1 |             | None           |             0 | False         |              165.04 |

### Execution

#### Per Connection

| DBMS                  | phase             | job                 |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:------------------|:--------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| CockroachDB-1-1-1-1-1 | CockroachDB-1-1-1 | CockroachDB-1-1-1-1 |                1 |          16 |    16384 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                         432.05 |                      430.22 |         0.00 |                                                      91614.00 |                                              37023.00 |
| CockroachDB-1-1-2-1-1 | CockroachDB-1-1-2 | CockroachDB-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       1 |          -1 | 300.00 |            0 |                         167.17 |                      166.47 |         0.00 |                                                     119261.00 |                                              47843.00 |
| CockroachDB-1-1-2-1-2 | CockroachDB-1-1-2 | CockroachDB-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       2 |          -1 | 300.00 |            0 |                         167.79 |                      167.06 |         0.00 |                                                     116025.00 |                                              47668.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:------------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| CockroachDB-1-1-1 | CockroachDB-1-1-1 |                1 |          16 |    16384 |               1 |           1 |          -1 | 300.00 |            0 |                         432.05 |                      430.22 |         0.00 |                                                      91614.00 |                                              37023.00 |
| CockroachDB-1-1-2 | CockroachDB-1-1-2 |                1 |          16 |    16384 |               1 |           2 |          -1 | 300.00 |            0 |                         334.96 |                      333.53 |         0.00 |                                                     119261.00 |                                              47755.50 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
