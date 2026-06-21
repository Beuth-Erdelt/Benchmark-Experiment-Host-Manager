## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 2397s 
* Code: 1782049832
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [4].
  * Experiment uses bexhoma version 0.9.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type cephcsi and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* CockroachDB-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:258556
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1335734
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-255
  * worker 1
    * RAM:1081649803264
    * Cores:56
    * host:6.8.0-111-generic
    * node:cl-worker34
    * disk:308070
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-55
  * worker 2
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:1327391
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-223
  * eval_parameters
    * code:1782049832
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* CockroachDB-1-2-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:258912
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1335736
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-255
  * worker 1
    * RAM:1081649803264
    * Cores:56
    * host:6.8.0-111-generic
    * node:cl-worker34
    * disk:308070
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-55
  * worker 2
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:1327383
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-223
  * worker 3
    * node:cl-worker24
  * eval_parameters
    * code:1782049832
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS CockroachDB-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS CockroachDB-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection            |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:----------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| CockroachDB-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                            8.10 |               504318.00 |              4086.00 |                           1108991.00 | 1.00 |                7.14 |
| CockroachDB-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                           13.37 |               503702.00 |              6734.00 |                           1240063.00 | 1.00 |                7.15 |
| CockroachDB-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                           10.74 |               503713.00 |              5409.00 |                           1168383.00 | 1.00 |                7.15 |
| CockroachDB-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                           10.73 |               504103.00 |              5408.00 |                           1178623.00 | 1.00 |                7.14 |
| CockroachDB-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                           10.70 |               504567.00 |              5400.00 |                           1163263.00 | 1.00 |                7.13 |
| CockroachDB-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                           13.36 |               503937.00 |              6733.00 |                           1239039.00 | 1.00 |                7.14 |
| CockroachDB-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                           50.48 |                54835.00 |              2768.00 |                            761855.00 | 1.00 |               65.65 |
| CockroachDB-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                           15.97 |               504588.00 |              8057.00 |                           1302527.00 | 1.00 |                7.13 |

#### Per Run

| DBMS            |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 1.00 |                7.13 |                          133.45 |               504588.00 |             44595.00 |                           1145343.00 |

### Execution

#### Per Connection

list index out of range
list index out of range
Traceback (most recent call last):
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\ycsb.py", line 821, in <module>
    experiment.process()
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\experiments\base.py", line 291, in process
    self.show_summary()
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\experiments\mixed.py", line 126, in 
show_summary
    benchmark.show_summary(self)
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\benchmarks\base.py", line 161, in show_summary
    print(df_conn.to_markdown(index=True, floatfmt=".2f"))
          ^^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'to_markdown'
