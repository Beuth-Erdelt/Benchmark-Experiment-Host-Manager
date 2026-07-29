# Benchmark: YCSB

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

YCSB does allow scaling data generation and ingestion, and scaling the benchmarking driver.
Scale-out can simulate distributed clients.
It is not self-evident and sure, that scale-out and scale-up yield the same performance results [3].

> The goal of the YCSB project is to develop a framework and common set of workloads for evaluating the performance of different key-value and cloud-serving stores. [...]
The workloads in the core package are a variation of the same basic application type. In this application, there is a table of records, each with F fields. Each record is identif ied by a primary key, which is a string like user234123. Each field is named field0, field1 and so on. The values of each field are a random string of ASCII characters of length L.
Each operation against the data store is randomly chosen to be one of:
> * Insert: Insert a new record.
> * Update: Update a record by replacing the value of one f ield. 
> * Read: Read a record, either one randomly chosen field or all fields.
> * Scan: Scan records in order, starting at a randomly chosen record key. The number of records to scan is randomly chosen. [1,2]

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. YCSB Repository: https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload
1. Benchmarking cloud serving systems with YCSB: https://dl.acm.org/doi/10.1145/1807128.1807152
1. A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools: https://doi.org/10.1007/978-3-031-68031-1_9

## Perform Benchmark

You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"
BEXHOMA_MS=1
BEXHOMA_STORAGE_CLASS="shared"

mkdir -p $LOG_DIR
```

For performing the experiment we can run the [ycsb file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/ycsb.py).

Example: 
```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 2 \
  -xnlf 1,4 \
  -nc 1 \
  -ne 1 \
  -nlp 1,8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_postgresql_loading.log
```

This
* loops over `n` in [1,8] and `t` in [1,4]
  * starts a clean instance of PostgreSQL (`-dbms`)
    * data directory inside a Docker container
  * creates YCSB schema in each database
  * starts `n` loader pods per DBMS
    * with a loading container each
      * threads = 64/`n` (`-nlt`)
      * target throughput is `t` * 16384
      * generates YCSB data = 1.000.000 rows (i.e., SF=1, `-sf`)
      * imports it into the DBMS
  * loops over `m` in [1] and `s` in [2]
    * runs `m` parallel streams of YCSB queries per DBMS
      * 1.000.000 operations
      * workload A = 50% read / 50% write (`--workload`)
      * target throughput is `s` * 16384
      * threads = 64/`m` (`-nbt`)
    * with a maximum of 1 DBMS per time (`-ms`)
* tests if results match workflow (`-tr`)
* shows a summary

### Status

You can watch the status while benchmark is running via `bexhoma status`

```bash
Dashboard: Running
Cluster Prometheus: Running
Message Queue: Running
Data directory: Running
Result directory: Running
+-----------------------+--------------+--------------+------------+-------------+
| 1726160982            | sut          |   loaded [s] | use case   | loading     |
+=======================+==============+==============+============+=============+
| PostgreSQL-64-1-16384 | (1. Running) |            1 | ycsb       | (1 Running) |
+-----------------------+--------------+--------------+------------+-------------+
```

The code `1726160982` is the unique identifier of the experiment.
You can find the number also in the output of `ycsb.py`.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1726160982` (removes everything that is related to experiment `1726160982`).

## Evaluate Results

At the end of a benchmark you will see a summary like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_postgresql_loading_summary.md" target="_blank" rel="noopener">docs_ycsb_postgresql_loading.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 605s 
* Code: 1785150902
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [1, 4].
  * Factors for benchmarking are [2].
  * Status is logged every 10s.
  * Experiment uses bexhoma version 0.10.8.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 and 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:826020
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785150902
* PostgreSQL-2-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:822807
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785150902
* PostgreSQL-3-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:826582
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785150902
* PostgreSQL-4-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:825669
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785150902

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1785150902-76d6f8f9d4-sddgr: 0 0
* bexhoma-sut-postgresql-2-1785150902-5b89559bd5-4g6dl: 0 0
* bexhoma-sut-postgresql-3-1785150902-7c67d77486-bsvk2: 0 0
* bexhoma-sut-postgresql-4-1785150902-865cd8d87f-vsr6t: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-3 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-4 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-3 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-4 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| PostgreSQL-1-1-0-1-1 |             1.00 |     64.00 | 16384.00 |        1.00 |         0.00 |                        16308.42 |                61318.00 |           1000000.00 |                             15543.00 | 1.00 |               58.71 |
| PostgreSQL-2-1-0-1-1 |             1.00 |     64.00 | 65536.00 |        1.00 |         0.00 |                        55367.92 |                18061.00 |           1000000.00 |                              4123.00 | 1.00 |              199.32 |
| PostgreSQL-3-1-0-1-1 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.48 |                61290.00 |            125000.00 |                             16559.00 | 1.00 |               58.74 |
| PostgreSQL-3-1-0-1-2 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.05 |                61303.00 |            125000.00 |                             16591.00 | 1.00 |               58.72 |
| PostgreSQL-3-1-0-1-3 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.22 |                61268.00 |            125000.00 |                             16463.00 | 1.00 |               58.76 |
| PostgreSQL-3-1-0-1-4 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.45 |                61291.00 |            125000.00 |                             16543.00 | 1.00 |               58.74 |
| PostgreSQL-3-1-0-1-5 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.15 |                61300.00 |            125000.00 |                             16479.00 | 1.00 |               58.73 |
| PostgreSQL-3-1-0-1-6 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.15 |                61270.00 |            125000.00 |                             16463.00 | 1.00 |               58.76 |
| PostgreSQL-3-1-0-1-7 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.55 |                61288.00 |            125000.00 |                             16559.00 | 1.00 |               58.74 |
| PostgreSQL-3-1-0-1-8 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.05 |                61273.00 |            125000.00 |                             16447.00 | 1.00 |               58.75 |
| PostgreSQL-4-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7190.93 |                17383.00 |            125000.00 |                              5755.00 | 1.00 |              207.10 |
| PostgreSQL-4-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7062.94 |                17698.00 |            125000.00 |                              6111.00 | 1.00 |              203.41 |
| PostgreSQL-4-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7157.58 |                17464.00 |            125000.00 |                              5183.00 | 1.00 |              206.14 |
| PostgreSQL-4-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         6998.49 |                17861.00 |            125000.00 |                              5247.00 | 1.00 |              201.56 |
| PostgreSQL-4-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7244.70 |                17254.00 |            125000.00 |                              4935.00 | 1.00 |              208.65 |
| PostgreSQL-4-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7290.33 |                17146.00 |            125000.00 |                              5051.00 | 1.00 |              209.96 |
| PostgreSQL-4-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7051.79 |                17726.00 |            125000.00 |                              5011.00 | 1.00 |              203.09 |
| PostgreSQL-4-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7118.05 |                17561.00 |            125000.00 |                              6067.00 | 1.00 |              205.00 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 16384.00 |        1.00 |         0.00 | 1.00 |               58.71 |                        16308.42 |                61318.00 |           1000000.00 |                             15543.00 |
| PostgreSQL-2-1 |             1.00 |     64.00 | 65536.00 |        1.00 |         0.00 | 1.00 |              199.32 |                        55367.92 |                18061.00 |           1000000.00 |                              4123.00 |
| PostgreSQL-3-1 |             1.00 |     64.00 | 16384.00 |        8.00 |         0.00 | 1.00 |               58.72 |                        16317.11 |                61303.00 |           1000000.00 |                             16513.00 |
| PostgreSQL-4-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 1.00 |              201.56 |                        57114.81 |                17861.00 |           1000000.00 |                              5420.00 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        32341.53 |                30920.00 |             499746 |                            1659.00 |               500254 |                              8975.00 |
| PostgreSQL-2-1-1-1-1 | PostgreSQL-2-1-1 | PostgreSQL-2-1-1-1 | PostgreSQL-2    |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        32462.26 |                30805.00 |             500129 |                             645.00 |               499871 |                             11911.00 |
| PostgreSQL-3-1-1-1-1 | PostgreSQL-3-1-1 | PostgreSQL-3-1-1-1 | PostgreSQL-3    |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        32415.96 |                30849.00 |             500306 |                            1092.00 |               499694 |                              8439.00 |
| PostgreSQL-4-1-1-1-1 | PostgreSQL-4-1-1 | PostgreSQL-4-1-1-1 | PostgreSQL-4    |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        32464.37 |                30803.00 |             500405 |                             637.00 |               499595 |                             14391.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                        32341.53 |                30920.00 |             499746 |                            1659.00 |               500254 |                              8975.00 |
| PostgreSQL-2-1-1 | PostgreSQL-2-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                        32462.26 |                30805.00 |             500129 |                             645.00 |               499871 |                             11911.00 |
| PostgreSQL-3-1-1 | PostgreSQL-3-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                        32415.96 |                30849.00 |             500306 |                            1092.00 |               499694 |                              8439.00 |
| PostgreSQL-4-1-1 | PostgreSQL-4-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                        32464.37 |                30803.00 |             500405 |                             637.00 |               499595 |                             14391.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>

We can see that the overall throughput is very close to the target and that scaled-out drivers (8 pods with 8 threads each) have similar results as a monolithic driver (1 pod with 64 thread).
The runtime is between 8 seconds and 1 minute.

To see the summary again you can simply call `bexhoma summary -e 1708411664` with the experiment code.

### Detailed Evaluation

Results are transformed into pandas DataFrames and can be inspected in detail.
See for example
* [Jupyter Notebooks](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/evaluator_dbmsbenchmarker/notebooks/)

You can connect to an evaluation server in the cluster by `bexhoma dashboard`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888

You can connect to an evaluation server locally by `bexhoma jupyter`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888

### Time Series of Metrics

See an [example notebook](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/dev/Evaluation-YCSB-Timeseries-1739274625-Heatmaps-Compare.ipynb) about how to analyze results in detail.

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

There are per DBMS
* `initschema`-files, that are invoked before loading of data
* `checkschema`-files, that are invoked after loading of data

You can find the output of the files in the result folder.



### Dockerfiles

The Dockerfiles for the components can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/ycsb

### Command line

You maybe want to adjust some of the parameters that are set in the file: `python ycsb.py -h`

```bash
usage: ycsb.py [-h] [-aws] [-dbms {PostgreSQL,MySQL}] [-db] [-cx CONTEXT] [-e EXPERIMENT] [-m] [-mc] [-ms MAX_SUT] [-nc NUM_CONFIG] [-ne NUM_QUERY_EXECUTORS] [-nl NUM_LOADING] [-nlp NUM_LOADING_PODS] [-xwl {a,b,c,e,f}] [-sf SCALING_FACTOR] [-xop SCALING_FACTOR_OPERATIONS] [-su SCALING_USERS]
               [-xsbs SCALING_BATCHSIZE] [-ltf LIST_TARGET_FACTORS] [-xtb TARGET_BASE] [-t TIMEOUT] [-rr REQUEST_RAM] [-rc REQUEST_CPU] [-rct REQUEST_CPU_TYPE] [-rg REQUEST_GPU] [-rgt REQUEST_GPU_TYPE] [-rst {None,,local-hdd,shared}] [-rss REQUEST_STORAGE_SIZE] [-rnn REQUEST_NODE_NAME] [-rnl REQUEST_NODE_LOADING]
               [-rnb REQUEST_NODE_BENCHMARKING] [-tr]
               {run,start,load,summary}

Perform YCSB benchmarks in a Kubernetes cluster. Number of rows and operations is SF*1,000,000. This installs a clean copy for each target and split of the driver. Optionally monitoring is activated.

positional arguments:
  {run,start,load,summary}
                        import YCSB data or run YCSB queries

options:
  -h, --help            show this help message and exit
  -aws, --aws           fix components to node groups at AWS
  -dbms {PostgreSQL,MySQL}, --dbms {PostgreSQL,MySQL}
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
  -nl NUM_LOADING, --num-loading NUM_LOADING
                        number of parallel loaders per configuration
  -nlp NUM_LOADING_PODS, --num-loading-pods NUM_LOADING_PODS
                        total number of loaders per configuration
  -xwl {a,b,c,e,f}, --workload {a,b,c,e,f}
                        YCSB default workload
  -sf SCALING_FACTOR, --scaling-factor SCALING_FACTOR
                        scaling factor (SF) = number of rows in millions
  -xop SCALING_FACTOR_OPERATIONS, --scaling-factor-operations SCALING_FACTOR_OPERATIONS
                        scaling factor = number of operations in millions (=SF if not set)
  -su SCALING_USERS, --scaling-users SCALING_USERS
                        scaling factor = number of total threads
  -xsbs SCALING_BATCHSIZE, --scaling-batchsize SCALING_BATCHSIZE
                        batch size
  -ltf LIST_TARGET_FACTORS, --list-target-factors LIST_TARGET_FACTORS
                        comma separated list of factors of 16384 ops as target - default range(1,9)
  -xtb TARGET_BASE, --target-base TARGET_BASE
                        ops as target, base for factors - default 16384 = 2**14
  -t TIMEOUT, --timeout TIMEOUT
                        timeout for a run of a query
  -rr REQUEST_RAM, --request-ram REQUEST_RAM
                        request ram for sut, default 16Gi
  -rc REQUEST_CPU, --request-cpu REQUEST_CPU
                        request cpus for sut, default 4
  -rct REQUEST_CPU_TYPE, --request-cpu-type REQUEST_CPU_TYPE
                        request node for sut to have node label cpu=
  -rg REQUEST_GPU, --request-gpu REQUEST_GPU
                        request number of gpus for sut
  -rgt REQUEST_GPU_TYPE, --request-gpu-type REQUEST_GPU_TYPE
                        request node for sut to have node label gpu=
  -rst {None,,local-hdd,shared}, --request-storage-type {None,,local-hdd,shared}
                        request persistent storage of certain type
  -rss REQUEST_STORAGE_SIZE, --request-storage-size REQUEST_STORAGE_SIZE
                        request persistent storage of certain size
  -rnn REQUEST_NODE_NAME, --request-node-name REQUEST_NODE_NAME
                        request a specific node for sut
  -rnl REQUEST_NODE_LOADING, --request-node-loading REQUEST_NODE_LOADING
                        request a specific node for loading pods
  -rnb REQUEST_NODE_BENCHMARKING, --request-node-benchmarking REQUEST_NODE_BENCHMARKING
                        request a specific node for benchmarking pods
  -tr, --test-result    test if result fulfills some basic requirements
```

## Perform Execution Benchmark

The default behaviour of bexhoma is that several different settings of the loading component are compared.
We might only want to benchmark the workloads of YCSB in different configurations and have a fixed loading phase.

For performing the experiment we can run the [ycsb file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/ycsb.py).

Example: 
```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 2,3 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1,8 \
  -nbt 64 \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_postgresql_benchmarking.log
```
This loads a YCSB data set with 8 pods (`-lnp`) of 64 threads in total.
Each of the drivers has 64 threads and a target of twice or three times (`-ltf`) the base, that is 16384.

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_postgresql_benchmarking_summary.md" target="_blank" rel="noopener">docs_ycsb_postgresql_benchmarking.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 785s 
* Code: 1785151513
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [2, 3].
  * Status is logged every 10s.
  * Experiment uses bexhoma version 0.10.8.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:854550
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785151513
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:859498
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785151513
* PostgreSQL-1-1-3-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:863123
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785151513
* PostgreSQL-1-1-4-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:838966
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785151513

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1785151513-68c4d987db-kr9qs: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: ycsb (8 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: ycsb (8 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| PostgreSQL-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         3740.83 |                33415.00 |            125000.00 |                             36095.00 | 1.00 |              107.74 |
| PostgreSQL-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         3653.15 |                34217.00 |            125000.00 |                             36255.00 | 1.00 |              105.21 |
| PostgreSQL-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         3682.75 |                33942.00 |            125000.00 |                             35583.00 | 1.00 |              106.06 |
| PostgreSQL-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         3801.70 |                32880.00 |            125000.00 |                             35423.00 | 1.00 |              109.49 |
| PostgreSQL-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         3636.36 |                34375.00 |            125000.00 |                             36095.00 | 1.00 |              104.73 |
| PostgreSQL-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         3747.56 |                33355.00 |            125000.00 |                             36383.00 | 1.00 |              107.93 |
| PostgreSQL-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         3666.98 |                34088.00 |            125000.00 |                             36351.00 | 1.00 |              105.61 |
| PostgreSQL-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         3629.29 |                34442.00 |            125000.00 |                             35903.00 | 1.00 |              104.52 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 1.00 |              104.52 |                        29558.64 |                34442.00 |           1000000.00 |                             36011.00 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        32436.99 |                30829.00 |             499932 |                             644.00 |               500068 |                              8247.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       1 |         8 |     4096 |           8 |            0 |                         4056.47 |                30815.00 |              62341 |                             826.00 |                62659 |                              2591.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       2 |         8 |     4096 |           8 |            0 |                         4056.07 |                30818.00 |              62584 |                             926.00 |                62416 |                              2681.00 |
| PostgreSQL-1-1-2-1-3 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       3 |         8 |     4096 |           8 |            0 |                         4063.85 |                30759.00 |              62552 |                            1063.00 |                62448 |                              2731.00 |
| PostgreSQL-1-1-2-1-4 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       4 |         8 |     4096 |           8 |            0 |                         4055.28 |                30824.00 |              62314 |                             884.00 |                62686 |                              2707.00 |
| PostgreSQL-1-1-2-1-5 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       5 |         8 |     4096 |           8 |            0 |                         4058.18 |                30802.00 |              62496 |                            1023.00 |                62504 |                              2849.00 |
| PostgreSQL-1-1-2-1-6 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       6 |         8 |     4096 |           8 |            0 |                         4055.68 |                30821.00 |              62165 |                             787.00 |                62835 |                              2401.00 |
| PostgreSQL-1-1-2-1-7 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       7 |         8 |     4096 |           8 |            0 |                         4056.07 |                30818.00 |              62494 |                             788.00 |                62506 |                              2495.00 |
| PostgreSQL-1-1-2-1-8 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       8 |         8 |     4096 |           8 |            0 |                         4058.31 |                30801.00 |              62410 |                             876.00 |                62590 |                              2657.00 |
| PostgreSQL-1-1-3-1-1 | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 | PostgreSQL-1    |                1 |        3 |               1 |       1 |        64 |    49152 |           1 |            0 |                        48466.05 |                20633.00 |             499877 |                             604.00 |               500123 |                              1637.00 |
| PostgreSQL-1-1-4-1-1 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       1 |         8 |     6144 |           8 |            0 |                         6073.86 |                20580.00 |              62556 |                             616.00 |                62444 |                              1959.00 |
| PostgreSQL-1-1-4-1-2 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       2 |         8 |     6144 |           8 |            0 |                         6070.32 |                20592.00 |              62614 |                             629.00 |                62386 |                              1903.00 |
| PostgreSQL-1-1-4-1-3 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       3 |         8 |     6144 |           8 |            0 |                         6078.29 |                20565.00 |              62541 |                             594.00 |                62459 |                              1931.00 |
| PostgreSQL-1-1-4-1-4 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       4 |         8 |     6144 |           8 |            0 |                         6071.20 |                20589.00 |              62003 |                             616.00 |                62997 |                              1922.00 |
| PostgreSQL-1-1-4-1-5 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       5 |         8 |     6144 |           8 |            0 |                         6075.33 |                20575.00 |              62680 |                             630.00 |                62320 |                              1938.00 |
| PostgreSQL-1-1-4-1-6 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       6 |         8 |     6144 |           8 |            0 |                         6070.02 |                20593.00 |              62484 |                             586.00 |                62516 |                              1891.00 |
| PostgreSQL-1-1-4-1-7 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       7 |         8 |     6144 |           8 |            0 |                         6070.32 |                20592.00 |              62280 |                             606.00 |                62720 |                              1815.00 |
| PostgreSQL-1-1-4-1-8 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       8 |         8 |     6144 |           8 |            0 |                         6074.45 |                20578.00 |              62740 |                             598.00 |                62260 |                              1862.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                        32436.99 |                30829.00 |             499932 |                             644.00 |               500068 |                              8247.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        64 |    32768 |               1 |           8 |            0 |                        32459.91 |                30824.00 |             499356 |                            1063.00 |               500644 |                              2849.00 |
| PostgreSQL-1-1-3 | PostgreSQL-1-1-3 |                1 |        64 |    49152 |               1 |           1 |            0 |                        48466.05 |                20633.00 |             499877 |                             604.00 |               500123 |                              1637.00 |
| PostgreSQL-1-1-4 | PostgreSQL-1-1-4 |                1 |        64 |    49152 |               1 |           8 |            0 |                        48583.79 |                20593.00 |             499898 |                             630.00 |               500102 |                              1959.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>

## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).

Example:
```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 3 \
  -xwl a \
  -xtb 16384 \
  -xnbf 2,3 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1,8 \
  -nbt 64 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_postgresql_monitoring.log
```

If monitoring is activated, the summary also contains a section like this:

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_postgresql_monitoring_summary.md" target="_blank" rel="noopener">docs_ycsb_postgresql_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 1066s 
* Code: 1785152306
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 3000000.
  * Ordering of inserts is hashed.
  * Number of operations is 3000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [2, 3].
  * Status is logged every 10s.
  * Experiment uses bexhoma version 0.10.8.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:826626
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785152306
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:834665
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785152306
* PostgreSQL-1-1-3-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:836260
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785152306
* PostgreSQL-1-1-4-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:840097
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785152306

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1785152306-74bb8bf7d7-vlw65: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: ycsb (8 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: ycsb (8 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| PostgreSQL-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7641.21 |                49076.00 |            375000.00 |                              3609.00 | 3.00 |              220.07 |
| PostgreSQL-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7739.62 |                48452.00 |            375000.00 |                              3627.00 | 3.00 |              222.90 |
| PostgreSQL-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7078.54 |                52977.00 |            375000.00 |                              3691.00 | 3.00 |              203.86 |
| PostgreSQL-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7432.07 |                50457.00 |            375000.00 |                              3721.00 | 3.00 |              214.04 |
| PostgreSQL-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7170.86 |                52295.00 |            375000.00 |                              3675.00 | 3.00 |              206.52 |
| PostgreSQL-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7123.59 |                52642.00 |            375000.00 |                              3569.00 | 3.00 |              205.16 |
| PostgreSQL-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7347.32 |                51039.00 |            375000.00 |                              3719.00 | 3.00 |              211.60 |
| PostgreSQL-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7634.99 |                49116.00 |            375000.00 |                              3569.00 | 3.00 |              219.89 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 3.00 |              203.86 |                        59168.20 |                52977.00 |           3000000.00 |                              3647.50 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        32654.48 |                91871.00 |            1499254 |                            1225.00 |              1500746 |                              7971.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       1 |         8 |     4096 |           8 |            0 |                         4084.97 |                91800.00 |             187467 |                             602.00 |               187533 |                              1517.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       2 |         8 |     4096 |           8 |            0 |                         4085.46 |                91789.00 |             187269 |                             605.00 |               187731 |                              1573.00 |
| PostgreSQL-1-1-2-1-3 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       3 |         8 |     4096 |           8 |            0 |                         4086.30 |                91770.00 |             187585 |                             630.00 |               187415 |                              1611.00 |
| PostgreSQL-1-1-2-1-4 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       4 |         8 |     4096 |           8 |            0 |                         4084.79 |                91804.00 |             187582 |                             646.00 |               187418 |                              1595.00 |
| PostgreSQL-1-1-2-1-5 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       5 |         8 |     4096 |           8 |            0 |                         4085.41 |                91790.00 |             187594 |                             565.00 |               187406 |                              1531.00 |
| PostgreSQL-1-1-2-1-6 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       6 |         8 |     4096 |           8 |            0 |                         4085.55 |                91787.00 |             187554 |                             586.00 |               187446 |                              1658.00 |
| PostgreSQL-1-1-2-1-7 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       7 |         8 |     4096 |           8 |            0 |                         4084.92 |                91801.00 |             186774 |                             568.00 |               188226 |                              1505.00 |
| PostgreSQL-1-1-2-1-8 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       8 |         8 |     4096 |           8 |            0 |                         4085.46 |                91789.00 |             188020 |                             567.00 |               186980 |                              1479.00 |
| PostgreSQL-1-1-3-1-1 | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 | PostgreSQL-1    |                1 |        3 |               1 |       1 |        64 |    49152 |           1 |            0 |                        48907.73 |                61340.00 |            1499986 |                             701.00 |              1500014 |                              2075.00 |
| PostgreSQL-1-1-4-1-1 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       1 |         8 |     6144 |           8 |            0 |                         6113.86 |                61336.00 |             187559 |                             873.00 |               187441 |                              2503.00 |
| PostgreSQL-1-1-4-1-2 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       2 |         8 |     6144 |           8 |            0 |                         6115.66 |                61318.00 |             187925 |                             669.00 |               187075 |                              2367.00 |
| PostgreSQL-1-1-4-1-3 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       3 |         8 |     6144 |           8 |            0 |                         6118.75 |                61287.00 |             187471 |                             725.00 |               187529 |                              2509.00 |
| PostgreSQL-1-1-4-1-4 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       4 |         8 |     6144 |           8 |            0 |                         6112.07 |                61354.00 |             187671 |                             868.00 |               187329 |                              2555.00 |
| PostgreSQL-1-1-4-1-5 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       5 |         8 |     6144 |           8 |            0 |                         6112.47 |                61350.00 |             187783 |                             890.00 |               187217 |                              2539.00 |
| PostgreSQL-1-1-4-1-6 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       6 |         8 |     6144 |           8 |            0 |                         6114.66 |                61328.00 |             187965 |                             786.00 |               187035 |                              2459.00 |
| PostgreSQL-1-1-4-1-7 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       7 |         8 |     6144 |           8 |            0 |                         6111.57 |                61359.00 |             187913 |                             908.00 |               187087 |                              2603.00 |
| PostgreSQL-1-1-4-1-8 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       8 |         8 |     6144 |           8 |            0 |                         6119.05 |                61284.00 |             187033 |                             918.00 |               187967 |                              2559.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                        32654.48 |                91871.00 |            1499254 |                            1225.00 |              1500746 |                              7971.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        64 |    32768 |               1 |           8 |            0 |                        32682.85 |                91804.00 |            1499845 |                             646.00 |              1500155 |                              1658.00 |
| PostgreSQL-1-1-3 | PostgreSQL-1-1-3 |                1 |        64 |    49152 |               1 |           1 |            0 |                        48907.73 |                61340.00 |            1499986 |                             701.00 |              1500014 |                              2075.00 |
| PostgreSQL-1-1-4 | PostgreSQL-1-1-4 |                1 |        64 |    49152 |               1 |           8 |            0 |                        48918.10 |                61359.00 |            1501320 |                             918.00 |              1498680 |                              2603.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       272.17 |      4.84 |           3.94 |                  7.40 |
| PostgreSQL-1-1-2-1 |       272.17 |      4.84 |           3.94 |                  7.40 |
| PostgreSQL-1-1-3-1 |       272.17 |      4.84 |           3.94 |                  7.40 |
| PostgreSQL-1-1-4-1 |       272.17 |      4.84 |           3.94 |                  7.40 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       216.35 |      6.06 |           0.11 |                  0.11 |
| PostgreSQL-1-1-2-1 |       216.35 |      6.06 |           0.11 |                  0.11 |
| PostgreSQL-1-1-3-1 |       216.35 |      6.06 |           0.11 |                  0.11 |
| PostgreSQL-1-1-4-1 |       216.35 |      6.06 |           0.11 |                  0.11 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       242.12 |      3.00 |           5.05 |                  8.96 |
| PostgreSQL-1-1-2-1 |       222.22 |      2.51 |           5.17 |                  9.18 |
| PostgreSQL-1-1-3-1 |       231.25 |      3.77 |           5.19 |                  9.23 |
| PostgreSQL-1-1-4-1 |       168.33 |      3.72 |           5.21 |                  9.25 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       310.24 |      4.27 |           0.13 |                  0.13 |
| PostgreSQL-1-1-2-1 |       215.31 |      7.29 |           0.13 |                  0.13 |
| PostgreSQL-1-1-3-1 |       141.19 |      7.82 |           0.13 |                  0.13 |
| PostgreSQL-1-1-4-1 |       209.92 |     10.91 |           0.13 |                  0.13 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>

This gives a survey about CPU (in CPU seconds) and RAM usage (in Gb) during loading and execution of the benchmark.

In this example, metrics are very instable. Metrics are fetched every 30 seconds.
This is too coarse for such a quick example.

## Use Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.

Example:
```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 2,3 \
  -xnlf 4 \
  -nc 2 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1,8 \
  -nbt 64 \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_postgresql_storage.log
```
The following status shows we have one volume of type `shared`.
Every PostgreSQL experiment running YCSB of SF=1 will take the databases from these volumes and skip loading.
In this example `-nc` is set to two, that is the complete experiment is repeated twice for statistical confidence.
The first instance of PostgreSQL mounts the volume and generates the data.
All other instances just use the database without generating and loading data.

```bash
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| Volumes                                  | configuration   | experiment    | loaded [s]   |   timeLoading [s] | dbms       | storage_class_name   | storage   | status   | size   | used   |
+==========================================+=================+===============+==============+===================+============+======================+===========+==========+========+========+
| bexhoma-storage-postgresql-ycsb-1        | postgresql      | ycsb-1        | True         |                16 | PostgreSQL | shared               | 100Gi     | Bound    | 100G   | 3.7G   |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-postgresql-ycsb-10       | postgresql      | ycsb-10       | True         |               217 | PostgreSQL | shared               | 100Gi     | Bound    | 100G   | 33G    |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
```

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_postgresql_storage_summary.md" target="_blank" rel="noopener">docs_ycsb_postgresql_storage.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 4623s 
* Code: 1785153400
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [2, 3].
  * Status is logged every 10s.
  * Experiment uses bexhoma version 0.10.8.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:810298
  * volume_size:50G
  * volume_used:2.4G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785153400
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:808967
  * volume_size:50G
  * volume_used:2.4G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785153400
* PostgreSQL-1-1-3-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:809008
  * volume_size:50G
  * volume_used:2.4G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785153400
* PostgreSQL-1-1-4-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:837312
  * volume_size:50G
  * volume_used:2.4G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785153400
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:810141
  * volume_size:50G
  * volume_used:3.9G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785153400
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:808973
  * volume_size:50G
  * volume_used:3.9G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785153400
* PostgreSQL-1-2-3-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:808891
  * volume_size:50G
  * volume_used:3.9G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785153400
* PostgreSQL-1-2-4-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:807933
  * volume_size:50G
  * volume_used:3.9G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785153400

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1785153400-7c9dccb744-r79wj: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 3: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 4: ycsb (8 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 3: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 4: ycsb (8 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| PostgreSQL-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          358.02 |               349141.00 |            125000.00 |                            149375.00 | 1.00 |               10.31 |
| PostgreSQL-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          363.12 |               344240.00 |            125000.00 |                            149759.00 | 1.00 |               10.46 |
| PostgreSQL-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          358.08 |               349086.00 |            125000.00 |                            149375.00 | 1.00 |               10.31 |
| PostgreSQL-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          358.08 |               349086.00 |            125000.00 |                            149119.00 | 1.00 |               10.31 |
| PostgreSQL-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          358.22 |               348945.00 |            125000.00 |                            149247.00 | 1.00 |               10.32 |
| PostgreSQL-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          358.06 |               349103.00 |            125000.00 |                            149375.00 | 1.00 |               10.31 |
| PostgreSQL-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          358.09 |               349076.00 |            125000.00 |                            149759.00 | 1.00 |               10.31 |
| PostgreSQL-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          360.59 |               346650.00 |            125000.00 |                            149375.00 | 1.00 |               10.39 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 1.00 |               10.31 |                         2872.26 |               349141.00 |           1000000.00 |                            149423.00 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                         2718.20 |               367891.00 |             500354 |                             760.00 |               499646 |                            633343.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       1 |         8 |     4096 |           8 |            0 |                          388.97 |               321361.00 |              62530 |                             784.00 |                62470 |                            290047.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       2 |         8 |     4096 |           8 |            0 |                          439.28 |               284559.00 |              62367 |                             794.00 |                62633 |                            291583.00 |
| PostgreSQL-1-1-2-1-3 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       3 |         8 |     4096 |           8 |            0 |                          453.11 |               275873.00 |              62338 |                             786.00 |                62662 |                            293631.00 |
| PostgreSQL-1-1-2-1-4 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       4 |         8 |     4096 |           8 |            0 |                          366.96 |               340634.00 |              62159 |                             787.00 |                62841 |                            298239.00 |
| PostgreSQL-1-1-2-1-5 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       5 |         8 |     4096 |           8 |            0 |                          399.87 |               312600.00 |              62415 |                             790.00 |                62585 |                            302335.00 |
| PostgreSQL-1-1-2-1-6 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       6 |         8 |     4096 |           8 |            0 |                          386.06 |               323782.00 |              62659 |                             788.00 |                62341 |                            329983.00 |
| PostgreSQL-1-1-2-1-7 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       7 |         8 |     4096 |           8 |            0 |                          434.79 |               287495.00 |              62274 |                             777.00 |                62726 |                            299519.00 |
| PostgreSQL-1-1-2-1-8 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       8 |         8 |     4096 |           8 |            0 |                          556.57 |               224591.00 |              62260 |                             781.00 |                62740 |                            299775.00 |
| PostgreSQL-1-1-3-1-1 | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 | PostgreSQL-1    |                1 |        3 |               1 |       1 |        64 |    49152 |           1 |            0 |                         2737.60 |               365284.00 |             499856 |                             807.00 |               500144 |                            518399.00 |
| PostgreSQL-1-1-4-1-1 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       1 |         8 |     6144 |           8 |            0 |                          319.42 |               391336.00 |              62543 |                             808.00 |                62457 |                            516863.00 |
| PostgreSQL-1-1-4-1-2 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       2 |         8 |     6144 |           8 |            0 |                          316.16 |               395364.00 |              62380 |                             849.00 |                62620 |                            520447.00 |
| PostgreSQL-1-1-4-1-3 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       3 |         8 |     6144 |           8 |            0 |                          333.21 |               375136.00 |              62803 |                             805.00 |                62197 |                            424191.00 |
| PostgreSQL-1-1-4-1-4 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       4 |         8 |     6144 |           8 |            0 |                          318.26 |               392756.00 |              62495 |                             823.00 |                62505 |                            462591.00 |
| PostgreSQL-1-1-4-1-5 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       5 |         8 |     6144 |           8 |            0 |                          323.49 |               386415.00 |              62509 |                             806.00 |                62491 |                            501759.00 |
| PostgreSQL-1-1-4-1-6 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       6 |         8 |     6144 |           8 |            0 |                          325.83 |               383631.00 |              62533 |                             806.00 |                62467 |                            431359.00 |
| PostgreSQL-1-1-4-1-7 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       7 |         8 |     6144 |           8 |            0 |                          323.91 |               385908.00 |              62408 |                             815.00 |                62592 |                            511487.00 |
| PostgreSQL-1-1-4-1-8 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       8 |         8 |     6144 |           8 |            0 |                          325.77 |               383702.00 |              62906 |                             814.00 |                62094 |                            490495.00 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 | PostgreSQL-1    |                2 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                         2089.75 |               478525.00 |             500416 |                            1003.00 |               499584 |                            897023.00 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       1 |         8 |     4096 |           8 |            0 |                          324.15 |               385622.00 |              62533 |                            2393.00 |                62467 |                            662527.00 |
| PostgreSQL-1-2-2-1-2 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       2 |         8 |     4096 |           8 |            0 |                          322.20 |               387961.00 |              62123 |                            2343.00 |                62877 |                            634879.00 |
| PostgreSQL-1-2-2-1-3 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       3 |         8 |     4096 |           8 |            0 |                          323.25 |               386698.00 |              62649 |                            2087.00 |                62351 |                            650239.00 |
| PostgreSQL-1-2-2-1-4 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       4 |         8 |     4096 |           8 |            0 |                          321.24 |               389116.00 |              62275 |                            2545.00 |                62725 |                            671743.00 |
| PostgreSQL-1-2-2-1-5 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       5 |         8 |     4096 |           8 |            0 |                          324.93 |               384697.00 |              62360 |                            2573.00 |                62640 |                            680959.00 |
| PostgreSQL-1-2-2-1-6 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       6 |         8 |     4096 |           8 |            0 |                          322.57 |               387511.00 |              62620 |                            2443.00 |                62380 |                            646655.00 |
| PostgreSQL-1-2-2-1-7 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       7 |         8 |     4096 |           8 |            0 |                          321.81 |               388427.00 |              62505 |                            2659.00 |                62495 |                            613887.00 |
| PostgreSQL-1-2-2-1-8 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       8 |         8 |     4096 |           8 |            0 |                          324.87 |               384768.00 |              62491 |                            2469.00 |                62509 |                            641535.00 |
| PostgreSQL-1-2-3-1-1 | PostgreSQL-1-2-3 | PostgreSQL-1-2-3-1 | PostgreSQL-1    |                2 |        3 |               1 |       1 |        64 |    49152 |           1 |            0 |                         2398.05 |               417005.00 |             500457 |                            1810.00 |               499543 |                            619007.00 |
| PostgreSQL-1-2-4-1-1 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       1 |         8 |     6144 |           8 |            0 |                          398.30 |               313837.00 |              62482 |                            2125.00 |                62518 |                            500479.00 |
| PostgreSQL-1-2-4-1-2 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       2 |         8 |     6144 |           8 |            0 |                          393.79 |               317430.00 |              62842 |                            1825.00 |                62158 |                            538623.00 |
| PostgreSQL-1-2-4-1-3 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       3 |         8 |     6144 |           8 |            0 |                          396.09 |               315588.00 |              62388 |                            1851.00 |                62612 |                            532479.00 |
| PostgreSQL-1-2-4-1-4 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       4 |         8 |     6144 |           8 |            0 |                          395.39 |               316145.00 |              62391 |                            2167.00 |                62609 |                            476927.00 |
| PostgreSQL-1-2-4-1-5 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       5 |         8 |     6144 |           8 |            0 |                          396.03 |               315631.00 |              62438 |                            1882.00 |                62562 |                            580607.00 |
| PostgreSQL-1-2-4-1-6 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       6 |         8 |     6144 |           8 |            0 |                          391.34 |               319416.00 |              62600 |                            1983.00 |                62400 |                            539647.00 |
| PostgreSQL-1-2-4-1-7 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       7 |         8 |     6144 |           8 |            0 |                          395.41 |               316127.00 |              62295 |                            2139.00 |                62705 |                            594943.00 |
| PostgreSQL-1-2-4-1-8 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       8 |         8 |     6144 |           8 |            0 |                          387.83 |               322308.00 |              62616 |                            2287.00 |                62384 |                            552447.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                         2718.20 |               367891.00 |             500354 |                             760.00 |               499646 |                            633343.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        64 |    32768 |               1 |           8 |            0 |                         3425.61 |               340634.00 |             499002 |                             794.00 |               500998 |                            329983.00 |
| PostgreSQL-1-1-3 | PostgreSQL-1-1-3 |                1 |        64 |    49152 |               1 |           1 |            0 |                         2737.60 |               365284.00 |             499856 |                             807.00 |               500144 |                            518399.00 |
| PostgreSQL-1-1-4 | PostgreSQL-1-1-4 |                1 |        64 |    49152 |               1 |           8 |            0 |                         2586.06 |               395364.00 |             500577 |                             849.00 |               499423 |                            520447.00 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |        64 |    32768 |               1 |           1 |            0 |                         2089.75 |               478525.00 |             500416 |                            1003.00 |               499584 |                            897023.00 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |        64 |    32768 |               1 |           8 |            0 |                         2585.02 |               389116.00 |             499556 |                            2659.00 |               500444 |                            680959.00 |
| PostgreSQL-1-2-3 | PostgreSQL-1-2-3 |                2 |        64 |    49152 |               1 |           1 |            0 |                         2398.05 |               417005.00 |             500457 |                            1810.00 |               499543 |                            619007.00 |
| PostgreSQL-1-2-4 | PostgreSQL-1-2-4 |                2 |        64 |    49152 |               1 |           8 |            0 |                         3154.17 |               322308.00 |             500052 |                            2287.00 |               499948 |                            594943.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>

Note the added section about `volume_size` and `volume_used` in the connections section.




## Set DBMS Args

Some DBMS allow to set parameter via args during startup.
In general, the Kubernetes manifest should be used to set all arguments.
In special cases (for example a batch of benchmarks) you may want to set a parameter via CLI.
Here is an example for how to use `--set` for PostgreSQL 18. This sets `effective_io_concurrency` to 64.

```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 2 \
  -xnlf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 1 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=64 \
  run &>$LOG_DIR/docs_ycsb_postgresql_loading_patch.log
```

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_postgresql_loading_patch_summary.md" target="_blank" rel="noopener">docs_ycsb_postgresql_loading_patch.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 401s 
* Code: 1785158039
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [1].
  * Factors for benchmarking are [2].
  * Status is logged every 10s.
  * Experiment uses bexhoma version 0.10.8.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [1] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_io_concurrency'}, '64')].
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540590804992
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-124-generic
  * node:cl-worker24
  * disk:174814
  * cpu_list:0-95
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'effective_io_concurrency=64']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785158039

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1785158039-67bb795d7d-dcr9z: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| PostgreSQL-1-1-0-1-1 |             1.00 |     64.00 | 16384.00 |        1.00 |         0.00 |                        16292.75 |                61377.00 |           1000000.00 |                             39583.00 | 1.00 |               58.65 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 16384.00 |        1.00 |         0.00 | 1.00 |               58.65 |                        16292.75 |                61377.00 |           1000000.00 |                             39583.00 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        32391.81 |                30872.00 |             500437 |                             200.00 |               499563 |                              6707.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                        32391.81 |                30872.00 |             500437 |                             200.00 |               499563 |                              6707.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>

## Reset Scripts

For repeated benchmarking rounds against the same database, bloat and stale planner statistics can drift the result away from the first round.
Bexhoma can run a pre-benchmark reset script (`CHECKPOINT` + `VACUUM ANALYZE` on `usertable` for PostgreSQL) before each round to start every round from a comparable state.
The feature is off by default; pass `-ar` to activate it.

Example (`-ne 1,2` sweeps two rounds, so the reset script runs twice):
```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 1 \
  -xwl a \
  -xtb 1024 \
  -xnbf 1 \
  -xnlf 1 \
  -nc 1 \
  -ne 1,2 \
  -nlp 1 \
  -nlt 8 \
  -nbp 1 \
  -nbt 8 \
  -ar \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_postgresql_reset.log
```

The reset script's own stdout/stderr is saved next to the other per-DBMS SQL script logs in the result folder, one pair of files per round, e.g. `bexhoma-reset_1_1_1-postgresql-1-reset-ycsb-postgres.sql.log` / `.error`.

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_postgresql_reset_summary.md" target="_blank" rel="noopener">docs_ycsb_postgresql_reset.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 2908s 
* Code: 1785158445
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '1024'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1]. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Status is logged every 10s.
  * Experiment uses bexhoma version 0.10.8.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 10Gi.
  * Loading is tested with [8] threads, split into [1] pods.
  * Benchmarking is tested with [8] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:810313
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785158445
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:811325
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785158445

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1785158445-68f446f9b5-zwp8r: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (2 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| PostgreSQL-1-1-0-1-1 |             1.00 |      8.00 |  1024.00 |        1.00 |         0.00 |                         1023.76 |               976793.00 |           1000000.00 |                              1572.00 | 1.00 |                3.69 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |      8.00 |  1024.00 |        1.00 |         0.00 | 1.00 |                3.69 |                         1023.76 |               976793.00 |           1000000.00 |                              1572.00 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |         8 |     1024 |           1 |            0 |                         1023.76 |               976793.00 |             500665 |                             708.00 |               499335 |                              2435.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       1 |         8 |     1024 |           2 |            0 |                         1023.51 |               488517.00 |             249977 |                             710.00 |               250023 |                              1468.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       2 |         8 |     1024 |           2 |            0 |                         1023.51 |               488517.00 |             249390 |                             704.00 |               250610 |                              1410.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |         8 |     1024 |               1 |           1 |            0 |                         1023.76 |               976793.00 |             500665 |                             708.00 |               499335 |                              2435.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        16 |     2048 |               1 |           2 |            0 |                         2047.01 |               488517.00 |             499367 |                             710.00 |               500633 |                              1468.00 |

#### Reset

| phase            | job                |   experiment_run |   client |   benchmark_run |   time_reset |
|:-----------------|:-------------------|-----------------:|---------:|----------------:|-------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |         2.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |         4.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |         4.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>

At this scale (SF=1, 1000 rows) `CHECKPOINT` and `VACUUM ANALYZE` complete in well under a second, so `time_reset` rounds to `0`.
On a larger, longer-running dataset this section is where you'd see the reset cost start to matter relative to the benchmarking duration itself.

## All Workloads

### Workload A

Workload A is 50% READ and 50% UPDATE.

Example:
```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 10 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1,8 \
  -nbt 64 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_postgresql_wl_a.log
```

### Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_postgresql_wl_a_summary.md" target="_blank" rel="noopener">docs_ycsb_postgresql_wl_a.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=10
* Type: ycsb
* Duration: 1047s 
* Code: 1785161359
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 10000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [4].
  * Status is logged every 10s.
  * Experiment uses bexhoma version 0.10.8.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:831382
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1785161359
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:834784
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1785161359

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1785161359-5d57c877cc-wc9kl: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (8 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (8 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |    sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|------:|--------------------:|
| PostgreSQL-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8009.79 |               156059.00 |           1250000.00 |                              2905.00 | 10.00 |              230.68 |
| PostgreSQL-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7580.86 |               164889.00 |           1250000.00 |                              2943.00 | 10.00 |              218.33 |
| PostgreSQL-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7799.19 |               160273.00 |           1250000.00 |                              2921.00 | 10.00 |              224.62 |
| PostgreSQL-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7910.64 |               158015.00 |           1250000.00 |                              2925.00 | 10.00 |              227.83 |
| PostgreSQL-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7531.53 |               165969.00 |           1250000.00 |                              2971.00 | 10.00 |              216.91 |
| PostgreSQL-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8080.21 |               154699.00 |           1250000.00 |                              2907.00 | 10.00 |              232.71 |
| PostgreSQL-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8127.97 |               153790.00 |           1250000.00 |                              2921.00 | 10.00 |              234.09 |
| PostgreSQL-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7955.20 |               157130.00 |           1250000.00 |                              2935.00 | 10.00 |              229.11 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |    sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|------:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 10.00 |              216.91 |                        62995.38 |               165969.00 |          10000000.00 |                              2928.50 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                        65412.92 |               152875.00 |            5000990 |                             598.00 |              4999010 |                              2709.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       1 |         8 |     8192 |           8 |            0 |                         8178.70 |               152836.00 |             625962 |                             639.00 |               624038 |                              2777.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       2 |         8 |     8192 |           8 |            0 |                         8179.56 |               152820.00 |             623960 |                             599.00 |               626040 |                              2461.00 |
| PostgreSQL-1-1-2-1-3 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       3 |         8 |     8192 |           8 |            0 |                         8179.29 |               152825.00 |             625099 |                             596.00 |               624901 |                              2577.00 |
| PostgreSQL-1-1-2-1-4 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       4 |         8 |     8192 |           8 |            0 |                         8178.01 |               152849.00 |             625805 |                             616.00 |               624195 |                              2671.00 |
| PostgreSQL-1-1-2-1-5 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       5 |         8 |     8192 |           8 |            0 |                         8178.33 |               152843.00 |             625718 |                             652.00 |               624282 |                              2787.00 |
| PostgreSQL-1-1-2-1-6 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       6 |         8 |     8192 |           8 |            0 |                         8179.83 |               152815.00 |             625109 |                             604.00 |               624891 |                              2551.00 |
| PostgreSQL-1-1-2-1-7 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       7 |         8 |     8192 |           8 |            0 |                         8178.27 |               152844.00 |             624603 |                             622.00 |               625397 |                              2633.00 |
| PostgreSQL-1-1-2-1-8 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       8 |         8 |     8192 |           8 |            0 |                         8179.02 |               152830.00 |             625570 |                             636.00 |               624430 |                              2687.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                        65412.92 |               152875.00 |            5000990 |                             598.00 |              4999010 |                              2709.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        64 |    65536 |               1 |           8 |            0 |                        65431.00 |               152849.00 |            5001826 |                             652.00 |              4998174 |                              2787.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       880.06 |      5.65 |          12.22 |                 23.66 |
| PostgreSQL-1-1-2-1 |       880.06 |      5.65 |          12.22 |                 23.66 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       860.97 |      6.51 |           0.11 |                  0.11 |
| PostgreSQL-1-1-2-1 |       860.97 |      6.51 |           0.11 |                  0.11 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       667.31 |      5.30 |          15.58 |                 28.53 |
| PostgreSQL-1-1-2-1 |       794.36 |      5.85 |          16.14 |                 29.61 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       567.94 |      4.66 |           0.13 |                  0.14 |
| PostgreSQL-1-1-2-1 |       705.25 |     11.33 |           0.13 |                  0.14 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>



### Workload B

Workload B is 95% READ and 5% UPDATE.

Example:
```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 10 \
  -xwl b \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1,8 \
  -nbt 64 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_postgresql_wl_b.log
```

### Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_postgresql_wl_b_summary.md" target="_blank" rel="noopener">docs_ycsb_postgresql_wl_b.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=10
* Type: ycsb
* Duration: 995s 
* Code: 1785162433
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'B'.
  * Number of rows to insert is 10000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [4].
  * Status is logged every 10s.
  * Experiment uses bexhoma version 0.10.8.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:831384
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1785162433
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:831608
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1785162433

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1785162433-558c9ccbcb-prlt8: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (8 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (8 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |    sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|------:|--------------------:|
| PostgreSQL-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7901.24 |               158203.00 |           1250000.00 |                              2939.00 | 10.00 |              227.56 |
| PostgreSQL-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7525.54 |               166101.00 |           1250000.00 |                              2915.00 | 10.00 |              216.74 |
| PostgreSQL-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7616.98 |               164107.00 |           1250000.00 |                              2973.00 | 10.00 |              219.37 |
| PostgreSQL-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7811.08 |               160029.00 |           1250000.00 |                              2947.00 | 10.00 |              224.96 |
| PostgreSQL-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7679.08 |               162780.00 |           1250000.00 |                              2935.00 | 10.00 |              221.16 |
| PostgreSQL-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7843.28 |               159372.00 |           1250000.00 |                              2903.00 | 10.00 |              225.89 |
| PostgreSQL-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7656.97 |               163250.00 |           1250000.00 |                              2953.00 | 10.00 |              220.52 |
| PostgreSQL-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7615.54 |               164138.00 |           1250000.00 |                              2989.00 | 10.00 |              219.33 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |    sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|------:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 10.00 |              216.74 |                        61649.72 |               166101.00 |          10000000.00 |                              2944.25 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                        65412.06 |               152877.00 |            9498827 |                             520.00 |               501173 |                              3765.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       1 |         8 |     8192 |           8 |            0 |                         8178.22 |               152845.00 |            1187451 |                             520.00 |                62549 |                              1539.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       2 |         8 |     8192 |           8 |            0 |                         8179.34 |               152824.00 |            1187663 |                             525.00 |                62337 |                              1547.00 |
| PostgreSQL-1-1-2-1-3 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       3 |         8 |     8192 |           8 |            0 |                         8179.61 |               152819.00 |            1187270 |                             484.00 |                62730 |                              1483.00 |
| PostgreSQL-1-1-2-1-4 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       4 |         8 |     8192 |           8 |            0 |                         8178.92 |               152832.00 |            1187152 |                             508.00 |                62848 |                              1551.00 |
| PostgreSQL-1-1-2-1-5 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       5 |         8 |     8192 |           8 |            0 |                         8178.86 |               152833.00 |            1186998 |                             509.00 |                63002 |                              1535.00 |
| PostgreSQL-1-1-2-1-6 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       6 |         8 |     8192 |           8 |            0 |                         8177.95 |               152850.00 |            1187038 |                             515.00 |                62962 |                              1570.00 |
| PostgreSQL-1-1-2-1-7 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       7 |         8 |     8192 |           8 |            0 |                         8177.58 |               152857.00 |            1187407 |                             559.00 |                62593 |                              1588.00 |
| PostgreSQL-1-1-2-1-8 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       8 |         8 |     8192 |           8 |            0 |                         8178.97 |               152831.00 |            1187630 |                             505.00 |                62370 |                              1537.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                        65412.06 |               152877.00 |            9498827 |                             520.00 |               501173 |                              3765.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        64 |    65536 |               1 |           8 |            0 |                        65429.45 |               152857.00 |            9498609 |                             559.00 |               501391 |                              1588.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       903.15 |      5.71 |          12.24 |                 23.67 |
| PostgreSQL-1-1-2-1 |       903.15 |      5.71 |          12.24 |                 23.67 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       862.80 |      6.16 |           0.11 |                  0.11 |
| PostgreSQL-1-1-2-1 |       862.80 |      6.16 |           0.11 |                  0.11 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       492.40 |      3.94 |          14.14 |                 25.85 |
| PostgreSQL-1-1-2-1 |       508.38 |      4.03 |          14.43 |                 26.41 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       635.97 |      4.73 |           0.13 |                  0.14 |
| PostgreSQL-1-1-2-1 |       792.41 |     10.96 |           0.13 |                  0.13 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>



### Workload C

Workload C is 100% READ.

Example:
```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 10 \
  -xwl c \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1,8 \
  -nbt 64 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_postgresql_wl_c.log
```

### Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_postgresql_wl_c_summary.md" target="_blank" rel="noopener">docs_ycsb_postgresql_wl_c.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=10
* Type: ycsb
* Duration: 1018s 
* Code: 1785163457
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'C'.
  * Number of rows to insert is 10000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [4].
  * Status is logged every 10s.
  * Experiment uses bexhoma version 0.10.8.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:831272
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1785163457
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:831273
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1785163457

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1785163457-59f654979b-q5w9n: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (8 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (8 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |    sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|------:|--------------------:|
| PostgreSQL-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7946.40 |               157304.00 |           1250000.00 |                              2961.00 | 10.00 |              228.86 |
| PostgreSQL-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7899.89 |               158230.00 |           1250000.00 |                              2975.00 | 10.00 |              227.52 |
| PostgreSQL-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8015.60 |               155946.00 |           1250000.00 |                              2941.00 | 10.00 |              230.85 |
| PostgreSQL-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7919.96 |               157829.00 |           1250000.00 |                              2973.00 | 10.00 |              228.09 |
| PostgreSQL-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7921.32 |               157802.00 |           1250000.00 |                              2951.00 | 10.00 |              228.13 |
| PostgreSQL-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8069.05 |               154913.00 |           1250000.00 |                              2937.00 | 10.00 |              232.39 |
| PostgreSQL-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7926.09 |               157707.00 |           1250000.00 |                              2929.00 | 10.00 |              228.27 |
| PostgreSQL-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7947.10 |               157290.00 |           1250000.00 |                              2963.00 | 10.00 |              228.88 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |    sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|------:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 10.00 |              227.52 |                        63645.41 |               158230.00 |          10000000.00 |                              2953.75 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                        65408.21 |               152886.00 |           10000000 |                             497.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       1 |         8 |     8192 |           8 |            0 |                         8178.22 |               152845.00 |            1250000 |                             468.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       2 |         8 |     8192 |           8 |            0 |                         8179.13 |               152828.00 |            1250000 |                             524.00 |
| PostgreSQL-1-1-2-1-3 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       3 |         8 |     8192 |           8 |            0 |                         8179.61 |               152819.00 |            1250000 |                             525.00 |
| PostgreSQL-1-1-2-1-4 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       4 |         8 |     8192 |           8 |            0 |                         8178.17 |               152846.00 |            1250000 |                             517.00 |
| PostgreSQL-1-1-2-1-5 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       5 |         8 |     8192 |           8 |            0 |                         8179.02 |               152830.00 |            1250000 |                             513.00 |
| PostgreSQL-1-1-2-1-6 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       6 |         8 |     8192 |           8 |            0 |                         8178.65 |               152837.00 |            1250000 |                             499.00 |
| PostgreSQL-1-1-2-1-7 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       7 |         8 |     8192 |           8 |            0 |                         8178.92 |               152832.00 |            1250000 |                             533.00 |
| PostgreSQL-1-1-2-1-8 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       8 |         8 |     8192 |           8 |            0 |                         8179.40 |               152823.00 |            1250000 |                             522.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                        65408.21 |               152886.00 |           10000000 |                             497.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        64 |    65536 |               1 |           8 |            0 |                        65431.11 |               152846.00 |           10000000 |                             533.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       864.62 |      5.63 |          12.79 |                 23.66 |
| PostgreSQL-1-1-2-1 |       864.62 |      5.63 |          12.79 |                 23.66 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       852.31 |      6.38 |           0.11 |                  0.11 |
| PostgreSQL-1-1-2-1 |       852.31 |      6.38 |           0.11 |                  0.11 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       466.96 |      3.35 |          13.78 |                 25.21 |
| PostgreSQL-1-1-2-1 |       513.02 |      3.53 |          13.78 |                 25.21 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       623.50 |      4.62 |           0.13 |                  0.13 |
| PostgreSQL-1-1-2-1 |       747.73 |     10.61 |           0.13 |                  0.13 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>



### Workload D

Workload D is 95% READ and 5% INSERT.
This means there are more rows in the database after the benchmark than before the benchmark.
The range of key that can be read or inserted changes.
Repetition is only fully sensible after a clean creation of the database.
It is not possible to scale out the driver.
This is because of the `latest` distribution.
It assumes the keyspace is filled completely up to some `recordcount` and new data is added straight after this number [1].

[1] https://github.com/brianfrankcooper/YCSB/blob/1e62880552fc95fa4b012846c0f3887420e676a8/core/src/main/java/site/ycsb/workloads/CoreWorkload.java#L491

Example:
```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 10 \
  -xwl d \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xio hashed \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_postgresql_wl_d.log
```

### Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_postgresql_wl_d_summary.md" target="_blank" rel="noopener">docs_ycsb_postgresql_wl_d.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=10
* Type: ycsb
* Duration: 748s 
* Code: 1785164502
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'D'.
  * Number of rows to insert is 10000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [4].
  * Status is logged every 10s.
  * Experiment uses bexhoma version 0.10.8.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:830233
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1785164502

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1785164502-744f6dbb-wxmpn: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |    sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|------:|--------------------:|
| PostgreSQL-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7204.53 |               173502.00 |           1250000.00 |                              3259.00 | 10.00 |              207.49 |
| PostgreSQL-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7413.65 |               168608.00 |           1250000.00 |                              3227.00 | 10.00 |              213.51 |
| PostgreSQL-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7718.62 |               161946.00 |           1250000.00 |                              3179.00 | 10.00 |              222.30 |
| PostgreSQL-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7235.97 |               172748.00 |           1250000.00 |                              3235.00 | 10.00 |              208.40 |
| PostgreSQL-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7862.77 |               158977.00 |           1250000.00 |                              3137.00 | 10.00 |              226.45 |
| PostgreSQL-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8055.21 |               155179.00 |           1250000.00 |                              3197.00 | 10.00 |              231.99 |
| PostgreSQL-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7707.49 |               162180.00 |           1250000.00 |                              3227.00 | 10.00 |              221.98 |
| PostgreSQL-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7928.71 |               157655.00 |           1250000.00 |                              3139.00 | 10.00 |              228.35 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |    sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|------:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 10.00 |              207.49 |                        61126.95 |               173502.00 |          10000000.00 |                              3200.00 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-------------------:|-----------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                        65404.79 |               152894.00 |               500931 |                              2137.00 |            9499069 |                             548.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-------------------:|-----------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                        65404.79 |               152894.00 |               500931 |                              2137.00 |            9499069 |                             548.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       838.93 |      5.33 |          12.08 |                 17.52 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       903.18 |      6.28 |           0.11 |                  0.11 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       504.49 |      3.76 |          14.37 |                 26.30 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       683.97 |      4.86 |           0.13 |                  0.14 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>



### Workload E

Workload E is 95% SCAN and 5% INSERT.
This means there are more rows in the database after the benchmark than before the benchmark.
The range of key that can be read or inserted changes.
Repetition is only fully sensible after a clean creation of the database.
This workload can be scaled out.
*Currently this does not seem to work properly.*
Scans might be done over empty keyspaces.

Example:
```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 10 \
  -xwl e \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xio ordered \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_postgresql_wl_e.log
```

### Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_postgresql_wl_e_summary.md" target="_blank" rel="noopener">docs_ycsb_postgresql_wl_e.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=10
* Type: ycsb
* Duration: 892s 
* Code: 1785165274
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'E'.
  * Number of rows to insert is 10000000.
  * Ordering of inserts is ordered.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [4].
  * Status is logged every 10s.
  * Experiment uses bexhoma version 0.10.8.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:830215
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1785165274

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1785165274-84ddc46776-cbx26: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |    sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|------:|--------------------:|
| PostgreSQL-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8115.30 |               154030.00 |           1250000.00 |                              2807.00 | 10.00 |              233.72 |
| PostgreSQL-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8065.71 |               154977.00 |           1250000.00 |                              2821.00 | 10.00 |              232.29 |
| PostgreSQL-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8017.24 |               155914.00 |           1250000.00 |                              2795.00 | 10.00 |              230.90 |
| PostgreSQL-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7870.10 |               158829.00 |           1250000.00 |                              2821.00 | 10.00 |              226.66 |
| PostgreSQL-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7936.31 |               157504.00 |           1250000.00 |                              2777.00 | 10.00 |              228.57 |
| PostgreSQL-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7957.32 |               157088.00 |           1250000.00 |                              2821.00 | 10.00 |              229.17 |
| PostgreSQL-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8039.31 |               155486.00 |           1250000.00 |                              2833.00 | 10.00 |              231.53 |
| PostgreSQL-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8133.57 |               153684.00 |           1250000.00 |                              2783.00 | 10.00 |              234.25 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |    sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|------:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 10.00 |              226.66 |                        64134.87 |               158829.00 |          10000000.00 |                              2807.25 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   [SCAN].Return=OK |   [SCAN].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-------------------:|-----------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                        33862.03 |               295316.00 |               499484 |                              6039.00 |            9500516 |                            6503.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   [SCAN].Return=OK |   [SCAN].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-------------------:|-----------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                        33862.03 |               295316.00 |               499484 |                              6039.00 |            9500516 |                            6503.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       851.84 |      5.46 |          12.24 |                 23.66 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       923.27 |      6.55 |           0.11 |                  0.11 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      2024.33 |      7.97 |          13.00 |                 24.92 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      3557.48 |     14.19 |           0.14 |                  0.14 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>



### Workload F

Workload F is 50% READ and 50% READ-MODIFY-WRITE.

Example:
```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 10 \
  -xwl f \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1,8 \
  -nbt 64 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_postgresql_wl_f.log
```

### Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_postgresql_wl_f_summary.md" target="_blank" rel="noopener">docs_ycsb_postgresql_wl_f.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=10
* Type: ycsb
* Duration: 1006s 
* Code: 1785166191
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'F'.
  * Number of rows to insert is 10000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [4].
  * Status is logged every 10s.
  * Experiment uses bexhoma version 0.10.8.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:830241
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1785166191
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:833631
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1785166191

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1785166191-7db684d4f-5jwtr: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (8 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (8 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |    sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|------:|--------------------:|
| PostgreSQL-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7775.61 |               160759.00 |           1250000.00 |                              2975.00 | 10.00 |              223.94 |
| PostgreSQL-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7927.00 |               157689.00 |           1250000.00 |                              2921.00 | 10.00 |              228.30 |
| PostgreSQL-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7552.96 |               165498.00 |           1250000.00 |                              2931.00 | 10.00 |              217.53 |
| PostgreSQL-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7789.13 |               160480.00 |           1250000.00 |                              2949.00 | 10.00 |              224.33 |
| PostgreSQL-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7534.89 |               165895.00 |           1250000.00 |                              2965.00 | 10.00 |              217.00 |
| PostgreSQL-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7991.66 |               156413.00 |           1250000.00 |                              2897.00 | 10.00 |              230.16 |
| PostgreSQL-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7233.42 |               172809.00 |           1250000.00 |                              2961.00 | 10.00 |              208.32 |
| PostgreSQL-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7392.64 |               169087.00 |           1250000.00 |                              2925.00 | 10.00 |              212.91 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |    sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|------:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 10.00 |              208.32 |                        61197.32 |               172809.00 |          10000000.00 |                              2940.50 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |   [READ-MODIFY-WRITE].Operations |   [READ-MODIFY-WRITE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|---------------------------------:|------------------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                        65397.09 |               152912.00 |           10000000 |                             661.00 |              5000591 |                              2733.00 |                          5000591 |                                         3207.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       1 |         8 |     8192 |           8 |            0 |                         8178.59 |               152838.00 |            1250000 |                             667.00 |               625286 |                              1839.00 |                           625286 |                                         2277.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       2 |         8 |     8192 |           8 |            0 |                         8178.27 |               152844.00 |            1250000 |                             649.00 |               624294 |                              1799.00 |                           624294 |                                         2227.00 |
| PostgreSQL-1-1-2-1-3 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       3 |         8 |     8192 |           8 |            0 |                         8179.13 |               152828.00 |            1250000 |                             666.00 |               625528 |                              1913.00 |                           625528 |                                         2339.00 |
| PostgreSQL-1-1-2-1-4 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       4 |         8 |     8192 |           8 |            0 |                         8178.27 |               152844.00 |            1250000 |                             654.00 |               624353 |                              1812.00 |                           624353 |                                         2237.00 |
| PostgreSQL-1-1-2-1-5 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       5 |         8 |     8192 |           8 |            0 |                         8177.15 |               152865.00 |            1250000 |                             648.00 |               624728 |                              1825.00 |                           624728 |                                         2253.00 |
| PostgreSQL-1-1-2-1-6 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       6 |         8 |     8192 |           8 |            0 |                         8178.01 |               152849.00 |            1250000 |                             659.00 |               624648 |                              1929.00 |                           624648 |                                         2365.00 |
| PostgreSQL-1-1-2-1-7 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       7 |         8 |     8192 |           8 |            0 |                         8178.81 |               152834.00 |            1250000 |                             676.00 |               625147 |                              1940.00 |                           625147 |                                         2379.00 |
| PostgreSQL-1-1-2-1-8 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       8 |         8 |     8192 |           8 |            0 |                         8178.86 |               152833.00 |            1250000 |                             633.00 |               624868 |                              1737.00 |                           624868 |                                         2137.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |   [READ-MODIFY-WRITE].Operations |   [READ-MODIFY-WRITE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|---------------------------------:|------------------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                        65397.09 |               152912.00 |           10000000 |                             661.00 |              5000591 |                              2733.00 |                          5000591 |                                         3207.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        64 |    65536 |               1 |           8 |            0 |                        65427.10 |               152865.00 |           10000000 |                             676.00 |              4998852 |                              1940.00 |                          4998852 |                                         2379.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       869.57 |      5.46 |          12.23 |                 23.65 |
| PostgreSQL-1-1-2-1 |       869.57 |      5.46 |          12.23 |                 23.65 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       886.95 |      6.51 |           0.11 |                  0.11 |
| PostgreSQL-1-1-2-1 |       886.95 |      6.51 |           0.11 |                  0.11 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      1006.17 |      7.76 |          15.59 |                 28.54 |
| PostgreSQL-1-1-2-1 |       961.07 |      6.92 |          16.05 |                 29.41 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       902.20 |      7.00 |           0.14 |                  0.14 |
| PostgreSQL-1-1-2-1 |      1059.90 |     16.13 |           0.14 |                  0.14 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>






