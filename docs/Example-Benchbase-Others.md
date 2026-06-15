# Benchmark: Benchbase's Others

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

Benchbase contains 18 benchmarks.
In principle, all of them can be run in bexhoma.
So far, only a few have been fully implemented and tested.
Further examples are listed below.

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. OLTP-Bench: An Extensible Testbed for Benchmarking Relational Databases: http://www.vldb.org/pvldb/vol7/p277-difallah.pdf
1. A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools: https://doi.org/10.1007/978-3-031-68031-1_9

## Twitter Benchmark

<img src="https://raw.githubusercontent.com/wiki/cmu-db/benchbase/img/twitter.png" alt="drawing" width="600"/>

> The Twitter workload is inspired by the popular micro-blogging website. In order to provide a realistic benchmark, we obtained an anonymized snapshot of the Twitter social graph from August 2009 that contains 51 million users and almost 2 billion follows relationships [...]. We created a synthetic workload generator that is based on an approximation of the queries/transactions needed to support the application functionalities as we observe them by using the web site, along with information derived from a data set of 200,000 tweets. Although we do not claim that this is a precise representation of Twitter's system, it still reflects its important characteristics, such as heavily skewed many-to-many relationships. [1]

1. OLTP-Bench: An Extensible Testbed for Benchmarking Relational Databases: http://www.vldb.org/pvldb/vol7/p277-difallah.pdf
1. Image Benchbase Twitter Benchmark: https://github.com/cmu-db/benchbase/wiki/Twitter

You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"
BEXHOMA_MS=1

mkdir -p $LOG_DIR
```

### Twitter Simple Testrun

For performing the experiment we can run the [benchbase file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/benchbase.py).

Example:
```bash
bexhoma benchbase -ms $BEXHOMA_MS -tr \
  -sf 16 \
  -xsd 5 \
  -dbms PostgreSQL \
  -nbp 1 \
  -nbt 16 \
  -xnbf 16 \
  -xtb 1024 \
  -xbt twitter \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_twitter_simple.log
```

This
* starts a clean instance of PostgreSQL (`-dbms`)
  * data directory inside a Docker container
* starts 1 loader pod (per DBMS) that
  * creates the schema in the database
  * imports data for scale factor 16 (`-sf`) (i.e., 16 * 500 the number of users) into the DBMS
  * using all threads of driver machine (benchbase setting)
* runs streams of twitter queries (per DBMS)
    * running for 5 (`-xsd`) minutes
    * each stream (pod) having 16 threads to simulate 16 users (`-nbt`)
    * `-nbp`: first stream 1 pod
    * target is 16x(`-ltf`) 1024 (`-xtb`) ops
* with a maximum of 1 DBMS per time (`-ms`)
* tests if results match workflow (`-tr`)
* shows a summary

### Evaluate Results

At the end of a benchmark you will see a summary like

doc_benchbase_testcase_twitter_simple.log
```markdown
﻿## Show Summary

### Workload
Benchbase Workload twitter SF=16
* Type: benchbase
* Duration: 583s 
* Code: 1773914979
* Benchbase runs the Twitter benchmark.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'twitter'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.4.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker14.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1024-1 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:150152
  * datadisk:263
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1773914979
    * TENANT_VOL:False

### Execution

#### Per Pod

| DBMS                    |   experiment_run |   terminals |   target |   client |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------------|-----------------:|------------:|---------:|---------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1024-1-1 |                1 |          16 |    16384 |        1 |       1 |    300 |            0 |                        16369.9 |                     16369.9 |            0 |                                                          1935 |                                                   919 |

#### Aggregated Parallel

| DBMS                  |   experiment_run |   terminals |   target |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|-----------------:|------------:|---------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1024-1 |                1 |          16 |    16384 |           1 |    300 |            0 |                        16369.9 |                     16369.9 |            0 |                                                          1935 |                                                   919 |

### Workflow

#### Actual

* DBMS PostgreSQL-1-1-1024 - Pods [[1]]

#### Planned

* DBMS PostgreSQL-1-1-1024 - Pods [[1]]

### Loading

| DBMS                  |   time_load |   terminals |   pods |   Throughput [SF/h] |
|:----------------------|------------:|------------:|-------:|--------------------:|
| PostgreSQL-1-1-1024-1 |           8 |           1 |      1 |                7200 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```

### SQL Scrips

The SQL scripts for pre and post ingestion can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/benchbase/twitter

There are per DBMS
* `initschema`-files, that are invoked before loading of data
* `checkschema`-files, that are invoked after loading of data

You can find the output of the files in the result folder.


### Twitter More Complex


```bash
bexhoma benchbase -ms $BEXHOMA_MS -tr \
  -sf 1600 \
  -xsd 20 \
  -dbms PostgreSQL \
  -nbp 1,2,4,8 \
  -nbt 160 \
  -xnbf 16 \
  -xtb 1024 \
  -xbt twitter \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -m -mc \
  run &>$LOG_DIR/doc_benchbase_testcase_twitter_scale.log
```

### Evaluate Results

doc_benchbase_testcase_twitter_scale.log
```markdown
﻿## Show Summary

### Workload
Benchbase Workload twitter SF=1600
* Type: benchbase
* Duration: 6032s 
* Code: 1773915579
* Benchbase runs the Twitter benchmark.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'twitter'. Scaling factor is 1600. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 20 minutes.
  * Experiment uses bexhoma version 0.9.4.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker14.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1, 2, 4, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1024-1 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:172521
  * datadisk:22632
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773915579
    * TENANT_VOL:False
* PostgreSQL-1-1-1024-2 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:172647
  * datadisk:22758
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773915579
    * TENANT_VOL:False
* PostgreSQL-1-1-1024-3 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:172772
  * datadisk:22883
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773915579
    * TENANT_VOL:False
* PostgreSQL-1-1-1024-4 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:172916
  * datadisk:23026
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773915579
    * TENANT_VOL:False

### Execution

#### Per Pod

| DBMS                    |   experiment_run |   terminals |   target |   client |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------------|-----------------:|------------:|---------:|---------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1024-1-1 |                1 |         160 |    16384 |        1 |       1 |   1200 |            0 |                       16384    |                    16384.1  |            0 |                                                         18410 |                                                  3796 |
| PostgreSQL-1-1-1024-2-1 |                1 |          80 |     8192 |        2 |       1 |   1200 |            0 |                        8191.98 |                     8192.02 |            0 |                                                         18409 |                                                  3818 |
| PostgreSQL-1-1-1024-2-2 |                1 |          80 |     8192 |        2 |       2 |   1200 |            0 |                        8192.02 |                     8192.02 |            0 |                                                         18381 |                                                  3805 |
| PostgreSQL-1-1-1024-3-3 |                1 |          40 |     4096 |        3 |       1 |   1200 |            0 |                        4095.99 |                     4095.99 |            0 |                                                         18320 |                                                  3807 |
| PostgreSQL-1-1-1024-3-2 |                1 |          40 |     4096 |        3 |       2 |   1200 |            0 |                        4095.93 |                     4095.96 |            0 |                                                         18328 |                                                  3820 |
| PostgreSQL-1-1-1024-3-1 |                1 |          40 |     4096 |        3 |       3 |   1200 |            0 |                        4095.99 |                     4095.99 |            0 |                                                         18347 |                                                  3813 |
| PostgreSQL-1-1-1024-3-4 |                1 |          40 |     4096 |        3 |       4 |   1200 |            0 |                        4095.98 |                     4095.99 |            0 |                                                         18324 |                                                  3831 |
| PostgreSQL-1-1-1024-4-8 |                1 |          20 |     2048 |        4 |       1 |   1200 |            0 |                        2047.99 |                     2048    |            0 |                                                         18425 |                                                  3829 |
| PostgreSQL-1-1-1024-4-6 |                1 |          20 |     2048 |        4 |       2 |   1200 |            0 |                        2047.95 |                     2047.97 |            0 |                                                         18394 |                                                  3861 |
| PostgreSQL-1-1-1024-4-5 |                1 |          20 |     2048 |        4 |       3 |   1200 |            0 |                        2048    |                     2048    |            0 |                                                         18408 |                                                  3830 |
| PostgreSQL-1-1-1024-4-4 |                1 |          20 |     2048 |        4 |       4 |   1200 |            0 |                        2048    |                     2048    |            0 |                                                         18390 |                                                  3825 |
| PostgreSQL-1-1-1024-4-2 |                1 |          20 |     2048 |        4 |       5 |   1200 |            0 |                        2048    |                     2048    |            0 |                                                         18419 |                                                  3825 |
| PostgreSQL-1-1-1024-4-7 |                1 |          20 |     2048 |        4 |       6 |   1200 |            0 |                        2048    |                     2048    |            0 |                                                         18393 |                                                  3804 |
| PostgreSQL-1-1-1024-4-3 |                1 |          20 |     2048 |        4 |       7 |   1200 |            0 |                        2047.97 |                     2047.98 |            0 |                                                         18402 |                                                  3846 |
| PostgreSQL-1-1-1024-4-1 |                1 |          20 |     2048 |        4 |       8 |   1200 |            0 |                        2047.99 |                     2048    |            0 |                                                         18418 |                                                  3818 |

#### Aggregated Parallel

| DBMS                  |   experiment_run |   terminals |   target |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|-----------------:|------------:|---------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1024-1 |                1 |         160 |    16384 |           1 |   1200 |            0 |                        16384   |                       16384 |            0 |                                                         18410 |                                               3796    |
| PostgreSQL-1-1-1024-2 |                1 |         160 |    16384 |           2 |   1200 |            0 |                        16384   |                       16384 |            0 |                                                         18409 |                                               3811.5  |
| PostgreSQL-1-1-1024-3 |                1 |         160 |    16384 |           4 |   1200 |            0 |                        16383.9 |                       16384 |            0 |                                                         18347 |                                               3817.75 |
| PostgreSQL-1-1-1024-4 |                1 |         160 |    16384 |           8 |   1200 |            0 |                        16383.9 |                       16384 |            0 |                                                         18425 |                                               3829.75 |

### Workflow

#### Actual

* DBMS PostgreSQL-1-1-1024 - Pods [[2, 8, 1, 4]]

#### Planned

* DBMS PostgreSQL-1-1-1024 - Pods [[1, 2, 4, 8]]

### Loading

| DBMS                  |   time_load |   terminals |   pods |   Throughput [SF/h] |
|:----------------------|------------:|------------:|-------:|--------------------:|
| PostgreSQL-1-1-1024-1 |         593 |           1 |      1 |             9713.32 |
| PostgreSQL-1-1-1024-2 |         593 |           1 |      2 |             9713.32 |
| PostgreSQL-1-1-1024-3 |         593 |           1 |      4 |             9713.32 |
| PostgreSQL-1-1-1024-4 |         593 |           1 |      8 |             9713.32 |

### Monitoring

### Loading phase: SUT deployment

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-1 |      2713.56 |      6.37 |          13.91 |                 18.71 |
| PostgreSQL-1-1-1024-2 |      2713.56 |      6.37 |          13.91 |                 18.71 |
| PostgreSQL-1-1-1024-3 |      2713.56 |      6.37 |          13.91 |                 18.71 |
| PostgreSQL-1-1-1024-4 |      2713.56 |      6.37 |          13.91 |                 18.71 |

### Loading phase: component loader

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-1 |        149.5 |      0.25 |           0.25 |                  0.25 |
| PostgreSQL-1-1-1024-2 |        149.5 |      0.25 |           0.25 |                  0.25 |
| PostgreSQL-1-1-1024-3 |        149.5 |      0.25 |           0.25 |                  0.25 |
| PostgreSQL-1-1-1024-4 |        149.5 |      0.25 |           0.25 |                  0.25 |

### Execution phase: SUT deployment

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-1 |      15519.3 |     13.43 |          20.38 |                 25.41 |
| PostgreSQL-1-1-1024-2 |      15508.8 |     13.46 |          20.43 |                 25.51 |
| PostgreSQL-1-1-1024-3 |      15074   |     13.3  |          20.49 |                 25.61 |
| PostgreSQL-1-1-1024-4 |      15472   |     13.48 |          20.57 |                 25.73 |

### Execution phase: component benchmarker

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-1 |      3065.81 |      2.53 |           2.38 |                  2.94 |
| PostgreSQL-1-1-1024-2 |      3065.81 |      4.79 |           2.38 |                  2.94 |
| PostgreSQL-1-1-1024-3 |      3183.87 |      3.5  |           1.13 |                  1.13 |
| PostgreSQL-1-1-1024-4 |      3251.86 |      6.13 |           0.78 |                  0.78 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
```









## CH-benCHmark

<img src="https://raw.githubusercontent.com/wiki/cmu-db/benchbase/img/chbenchmark.png" alt="drawing" width="600"/>

> This is a mixed workload derived from TPC-Cand TPC-H [...].
It is useful to evaluate DBMSs designed to serve both OLTP and
OLAP workloads. The implementation leverages the ability of
OLTP-Bench to run multiple workloads. It uses our built-in implementation of TPC-C along with 22 additional analytical queries. [1]

1. OLTP-Bench: An Extensible Testbed for Benchmarking Relational Databases: http://www.vldb.org/pvldb/vol7/p277-difallah.pdf
1. Image Benchbase CH-benCHmark: https://github.com/cmu-db/benchbase/wiki/CH-benCHmark
1. CH-benCHmark: https://db.in.tum.de/research/projects/CHbenCHmark/?lang=en


You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"
BEXHOMA_MS=1

mkdir -p $LOG_DIR
```

### CH-benCHmark Simple Testrun

For performing the experiment we can run the [benchbase file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/benchbase.py).

Example:
```bash
bexhoma benchbase -ms $BEXHOMA_MS -tr \
  -sf 10 \
  -xsd 5 \
  -dbms PostgreSQL \
  -nbp 1 \
  -nbt 100 \
  -xnbf 16 \
  -xtb 1024 \
  -xbt chbenchmark \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_chbenchmark_simple.log
```

This
* starts a clean instance of PostgreSQL (`-dbms`)
  * data directory inside a Docker container
* starts 1 loader pod (per DBMS) that
  * creates the schema in the database
  * imports data for scale factor 16 (`-sf`) (i.e., 16 * 500 the number of users) into the DBMS
  * using all threads of driver machine (benchbase setting)
* runs streams of twitter queries (per DBMS)
    * running for 5 (`-xsd`) minutes
    * each stream (pod) having 16 threads to simulate 16 users (`-nbt`)
    * `-nbp`: first stream 1 pod
    * target is 16x(`-ltf`) 1024 (`-xtb`) ops
* with a maximum of 1 DBMS per time (`-ms`)
* tests if results match workflow (`-tr`)
* shows a summary

### Evaluate Results

At the end of a benchmark you will see a summary like

doc_benchbase_testcase_chbenchmark_simple.log
```markdown
﻿## Show Summary

### Workload
Benchbase Workload chbenchmark SF=10
* Type: benchbase
* Duration: 1048s 
* Code: 1773921642
* Benchbase runs the CH-Benchmark benchmark.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'chbenchmark'. Scaling factor is 10. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.4.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker14.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [100] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1024-1 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:152611
  * datadisk:2722
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1773921642
    * TENANT_VOL:False

### Execution

#### Per Pod

| DBMS                    |   experiment_run |   terminals |   target |   client |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------------|-----------------:|------------:|---------:|---------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1024-1-1 |                1 |         100 |    16384 |        1 |       1 |    300 |            0 |                        4.13333 |                        4.47 |            0 |                                                   3.06305e+07 |                                            1.0041e+07 |

#### Aggregated Parallel

| DBMS                  |   experiment_run |   terminals |   target |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|-----------------:|------------:|---------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1024-1 |                1 |         100 |    16384 |           1 |    300 |            0 |                           4.13 |                        4.47 |            0 |                                                   3.06305e+07 |                                            1.0041e+07 |

### Workflow

#### Actual

* DBMS PostgreSQL-1-1-1024 - Pods [[1]]

#### Planned

* DBMS PostgreSQL-1-1-1024 - Pods [[1]]

### Loading

| DBMS                  |   time_load |   terminals |   pods |   Throughput [SF/h] |
|:----------------------|------------:|------------:|-------:|--------------------:|
| PostgreSQL-1-1-1024-1 |         186 |           1 |      1 |             193.548 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```

### SQL Scrips

The SQL scripts for pre and post ingestion can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/benchbase/chbenchmark

There are per DBMS
* `initschema`-files, that are invoked before loading of data
* `checkschema`-files, that are invoked after loading of data

You can find the output of the files in the result folder.


### CH-benCHmark More Complex


```bash
bexhoma benchbase -ms $BEXHOMA_MS -tr \
  -sf 100 \
  -xsd 20 \
  -dbms PostgreSQL \
  -nbp 1,2,5,10 \
  -nbt 100 \
  -xnbf 16 \
  -xtb 1024 \
  -xbt chbenchmark \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_chbenchmark_scale.log
```

### Evaluate Results

doc_benchbase_testcase_chbenchmark_scale.log
```markdown
﻿## Show Summary

### Workload
Benchbase Workload chbenchmark SF=100
    Type: benchbase
    Duration: 28149s 
    Code: 1769711345
    Intro: Benchbase runs the CH-Benchmark benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'chbenchmark'. Scaling factor is 100. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 20 minutes.
    Experiment uses bexhoma version 0.8.20.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [100] threads, split into [1, 2, 5, 10] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:121550
    datadisk:26551
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:128Gi
    limits_memory:128Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1769711345
                TENANT_VOL:False
PostgreSQL-1-1-1024-2 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:121551
    datadisk:26552
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:128Gi
    limits_memory:128Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1769711345
                TENANT_VOL:False
PostgreSQL-1-1-1024-3 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:121553
    datadisk:26553
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:128Gi
    limits_memory:128Gi
    client:3
    numExperiment:1
    eval_parameters
                code:1769711345
                TENANT_VOL:False
PostgreSQL-1-1-1024-4 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:121554
    datadisk:26554
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:128Gi
    limits_memory:128Gi
    client:4
    numExperiment:1
    eval_parameters
                code:1769711345
                TENANT_VOL:False

### Execution

#### Per Pod
                          experiment_run  terminals  target  client  child    time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                       
PostgreSQL-1-1-1024-1-1                1        100   16384       1      1  1200.0           0                      1.305833                   1.389167         0.0                                                  151416763.0                                           36135855.0
PostgreSQL-1-1-1024-2-1                1         50    8192       2      1  1200.0           0                      0.816667                   0.858333         0.0                                                  152281461.0                                           35185760.0
PostgreSQL-1-1-1024-2-2                1         50    8192       2      2  1200.0           0                      0.672500                   0.714167         0.0                                                  149561106.0                                           37882450.0
PostgreSQL-1-1-1024-3-4                1         20    3276       3      1  1200.0           0                      0.299167                   0.315833         0.0                                                  141921391.0                                           31337907.0
PostgreSQL-1-1-1024-3-5                1         20    3276       3      2  1200.0           0                      0.275000                   0.291667         0.0                                                  159692838.0                                           33584855.0
PostgreSQL-1-1-1024-3-3                1         20    3276       3      3  1200.0           0                      0.270000                   0.286667         0.0                                                  124688355.0                                           30029797.0
PostgreSQL-1-1-1024-3-2                1         20    3276       3      4  1200.0           0                      0.346667                   0.363333         0.0                                                  115455529.0                                           29153268.0
PostgreSQL-1-1-1024-3-1                1         20    3276       3      5  1200.0           0                      0.151667                   0.168333         0.0                                                  199020582.0                                           51030100.0
PostgreSQL-1-1-1024-4-9                1         10    1638       4      1  1200.0           0                      0.139167                   0.148333         0.0                                                  117861669.0                                           28162282.0
PostgreSQL-1-1-1024-4-8                1         10    1638       4      2  1200.0           0                      0.168333                   0.176667         0.0                                                  114463914.0                                           24092157.0
PostgreSQL-1-1-1024-4-6                1         10    1638       4      3  1200.0           0                      0.133333                   0.142500         0.0                                                  105598190.0                                           24386481.0
PostgreSQL-1-1-1024-4-10               1         10    1638       4      4  1200.0           0                      0.124167                   0.132500         0.0                                                  145410189.0                                           32230068.0
PostgreSQL-1-1-1024-4-5                1         10    1638       4      5  1200.0           0                      0.132500                   0.141667         0.0                                                  113440999.0                                           29401984.0
PostgreSQL-1-1-1024-4-4                1         10    1638       4      6  1200.0           0                      0.105833                   0.115000         0.0                                                  137983316.0                                           31487385.0
PostgreSQL-1-1-1024-4-2                1         10    1638       4      7  1200.0           0                      0.125833                   0.134167         0.0                                                  125049955.0                                           31459832.0
PostgreSQL-1-1-1024-4-1                1         10    1638       4      8  1200.0           0                      0.191667                   0.200833         0.0                                                  140162337.0                                           34524133.0
PostgreSQL-1-1-1024-4-7                1         10    1638       4      9  1200.0           0                      0.121667                   0.130000         0.0                                                  124211024.0                                           37291231.0
PostgreSQL-1-1-1024-4-3                1         10    1638       4     10  1200.0           0                      0.098333                   0.107500         0.0                                                  152749259.0                                           30912961.0

#### Aggregated Parallel
                       experiment_run  terminals  target  pod_count    time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1        100   16384          1  1200.0           0                          1.31                       1.39         0.0                                                  151416763.0                                           36135855.0
PostgreSQL-1-1-1024-2               1        100   16384          2  1200.0           0                          1.49                       1.57         0.0                                                  152281461.0                                           36534105.0
PostgreSQL-1-1-1024-3               1        100   16380          5  1200.0           0                          1.34                       1.43         0.0                                                  199020582.0                                           35027185.4
PostgreSQL-1-1-1024-4               1        100   16380         10  1200.0           0                          1.34                       1.43         0.0                                                  152749259.0                                           30394851.4

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2, 5, 10]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2, 5, 10]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1      972.0        1.0   1.0          370.37037
PostgreSQL-1-1-1024-2      972.0        1.0   2.0          370.37037
PostgreSQL-1-1-1024-3      972.0        1.0   5.0          370.37037
PostgreSQL-1-1-1024-4      972.0        1.0  10.0          370.37037

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```



## YCSB Benchmark

<img src="https://raw.githubusercontent.com/wiki/cmu-db/benchbase/img/ycsb.png" alt="drawing" width="200"/>

> The Yahoo! Cloud Serving Benchmark (YCSB) is a collection of micro-benchmarks that represent data management applications whose workload is simple but requires high scalability [16]. Such applications are often large-scale services created by Web-based companies. Although these services are often deployed using distributed key/value storage systems, this benchmark can also provide insight into the capabilities of traditional DBMSs. [1]

1. OLTP-Bench: An Extensible Testbed for Benchmarking Relational Databases: http://www.vldb.org/pvldb/vol7/p277-difallah.pdf
1. Image Benchbase YCSB Benchmark: https://github.com/cmu-db/benchbase/wiki/YCSB

You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"
BEXHOMA_MS=1

mkdir -p $LOG_DIR
```

### YCSB Simple Testrun Workload C

For performing the experiment we can run the [benchbase file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/benchbase.py).

Example:
```bash
bexhoma benchbase -tr \
  -sf 1000 \
  -xsd 5 \
  --benchmark ycsb \
  --workload c \
  -dbms PostgreSQL \
  -nlt 64 \
  -nbp 1,2 \
  -nbt 32 \
  -xnbf 16 \
  -xtb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_ycsb_c.log
```

This
* starts a clean instance of PostgreSQL (`-dbms`)
  * data directory inside a Docker container
* starts 1 loader pod (per DBMS) that
  * creates the schema in the database
  * imports data for scale factor 1000 (`-sf`) (i.e., 1000 * 1000 the number of rows) into the DBMS
  * using all threads of driver machine (benchbase setting)
* runs streams of ycsb (`--benchmark`) queries (per DBMS) workload c (`--workload`)
    * running for 5 (`-xsd`) minutes
    * each stream (pod) having 32 threads to simulate 32 users (`-nbt`)
    * `-nbp`: first stream 1 pod, second stream 2 pods
    * target is 16x(`-ltf`) 1024 (`-xtb`) ops
* with a maximum of 1 DBMS per time (`-ms`)
* tests if results match workflow (`-tr`)
* shows a summary

### Evaluate Results

At the end of a benchmark you will see a summary like

doc_benchbase_testcase_ycsb_c.log
```markdown
﻿## Show Summary

### Workload
Benchbase Workload ycsb SF=1000
    Type: benchbase
    Duration: 970s 
    Code: 1769696010
    Intro: Benchbase runs an YCSB experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'ycsb'. Workload is 'c'. Scaling factor is 1000. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.20.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [64] threads, split into [1] pods.
    Benchmarking is tested with [32] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97295
    datadisk:2297
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1769696010
                TENANT_VOL:False
PostgreSQL-1-1-1024-2 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97295
    datadisk:2297
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1769696010
                TENANT_VOL:False

### Execution

#### Per Pod
                         experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                     
PostgreSQL-1-1-1024-1-1               1         32   16384       1      1  300.0           0                  16384.057849               16384.064516         0.0                                                        478.0                                                394.0
PostgreSQL-1-1-1024-2-1               1         16    8192       2      1  300.0           0                   8192.028060                8192.028060         0.0                                                        477.0                                                396.0
PostgreSQL-1-1-1024-2-2               1         16    8192       2      2  300.0           0                   8192.027663                8192.027663         0.0                                                        474.0                                                397.0

#### Aggregated Parallel
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         32   16384          1  300.0           0                      16384.06                   16384.06         0.0                                                        478.0                                                394.0
PostgreSQL-1-1-1024-2               1         32   16384          2  300.0           0                      16384.06                   16384.06         0.0                                                        477.0                                                396.5

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[2, 1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1       46.0        1.0   1.0       78260.869565
PostgreSQL-1-1-1024-2       46.0        1.0   2.0       78260.869565

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```



### YCSB Simple Testrun Workload A

For performing the experiment we can run the [benchbase file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/benchbase.py).

Example:
```bash
bexhoma benchbase -tr \
  -sf 1000 \
  -xsd 5 \
  --benchmark ycsb \
  --workload a \
  -dbms PostgreSQL \
  -nlt 64 \
  -nbp 1,2 \
  -nbt 32 \
  -xnbf 16 \
  -xtb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_ycsb_a.log
```


### Evaluate Results

At the end of a benchmark you will see a summary like

doc_benchbase_testcase_ycsb_a.log
```markdown
﻿## Show Summary

### Workload
Benchbase Workload ycsb SF=1000
    Type: benchbase
    Duration: 966s 
    Code: 1769697030
    Intro: Benchbase runs an YCSB experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'ycsb'. Workload is 'a'. Scaling factor is 1000. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.20.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [64] threads, split into [1] pods.
    Benchmarking is tested with [32] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97295
    datadisk:2297
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1769697030
                TENANT_VOL:False
PostgreSQL-1-1-1024-2 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97770
    datadisk:2773
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1769697030
                TENANT_VOL:False

### Execution

#### Per Pod
                         experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                     
PostgreSQL-1-1-1024-1-1               1         32   16384       1      1  300.0           0                   1680.006658                1680.113325         0.0                                                      41361.0                                              19037.0
PostgreSQL-1-1-1024-2-1               1         16    8192       2      1  300.0           0                    844.683011                 844.736344         0.0                                                      41030.0                                              18933.0
PostgreSQL-1-1-1024-2-2               1         16    8192       2      2  300.0           0                    836.026604                 836.079937         0.0                                                      41109.0                                              19117.0

#### Aggregated Parallel
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         32   16384          1  300.0           0                       1680.01                    1680.11         0.0                                                      41361.0                                              19037.0
PostgreSQL-1-1-1024-2               1         32   16384          2  300.0           0                       1680.71                    1680.82         0.0                                                      41109.0                                              19025.0

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[2, 1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1       46.0        1.0   1.0       78260.869565
PostgreSQL-1-1-1024-2       46.0        1.0   2.0       78260.869565

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```


### YCSB Simple Testrun Workload B

For performing the experiment we can run the [benchbase file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/benchbase.py).

Example:
```bash
bexhoma benchbase -tr \
  -sf 1000 \
  -xsd 5 \
  --benchmark ycsb \
  --workload b \
  -dbms PostgreSQL \
  -nlt 64 \
  -nbp 1,2 \
  -nbt 32 \
  -xnbf 16 \
  -xtb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_ycsb_b.log
```


### Evaluate Results

At the end of a benchmark you will see a summary like

doc_benchbase_testcase_ycsb_b.log
```markdown
﻿## Show Summary

### Workload
Benchbase Workload ycsb SF=1000
    Type: benchbase
    Duration: 998s 
    Code: 1769698050
    Intro: Benchbase runs an YCSB experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'ycsb'. Workload is 'b'. Scaling factor is 1000. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.20.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [64] threads, split into [1] pods.
    Benchmarking is tested with [32] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97295
    datadisk:2297
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1769698050
                TENANT_VOL:False
PostgreSQL-1-1-1024-2 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97737
    datadisk:2740
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1769698050
                TENANT_VOL:False

### Execution

#### Per Pod
                         experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                     
PostgreSQL-1-1-1024-1-1               1         32   16384       1      1  300.0           0                  16185.568604               16185.648604         0.0                                                       8992.0                                               1762.0
PostgreSQL-1-1-1024-2-2               1         16    8192       2      1  300.0           0                   8123.977893                8124.031226         0.0                                                       8958.0                                               1780.0
PostgreSQL-1-1-1024-2-1               1         16    8192       2      2  300.0           0                   8111.756480                8111.809814         0.0                                                       8981.0                                               1779.0

#### Aggregated Parallel
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         32   16384          1  300.0           0                      16185.57                   16185.65         0.0                                                       8992.0                                               1762.0
PostgreSQL-1-1-1024-2               1         32   16384          2  300.0           0                      16235.73                   16235.84         0.0                                                       8981.0                                               1779.5

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1       47.0        1.0   1.0       76595.744681
PostgreSQL-1-1-1024-2       47.0        1.0   2.0       76595.744681

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```




### YCSB Simple Testrun Workload D

For performing the experiment we can run the [benchbase file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/benchbase.py).

Example:
```bash
bexhoma benchbase -tr \
  -sf 1000 \
  -xsd 5 \
  --benchmark ycsb \
  --workload d \
  -dbms PostgreSQL \
  -nlt 64 \
  -nbp 1 \
  -nbt 32 \
  -xnbf 16 \
  -xtb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_ycsb_d.log
```

This time we only use a single benchmarking pod.
This is because the workload contains INSERTs and two parallel pods would try to insert the same data.
Other than the original YCSB tool, Benchbase does not offer an option to limit the range of keys to be inserted.

### Evaluate Results

At the end of a benchmark you will see a summary like

doc_benchbase_testcase_ycsb_d.log
```markdown
﻿## Show Summary

### Workload
Benchbase Workload ycsb SF=1000
    Type: benchbase
    Duration: 640s 
    Code: 1769699070
    Intro: Benchbase runs an YCSB experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'ycsb'. Workload is 'd'. Scaling factor is 1000. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.20.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [64] threads, split into [1] pods.
    Benchmarking is tested with [32] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97295
    datadisk:2297
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1769699070
                TENANT_VOL:False

### Execution

#### Per Pod
                         experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                     
PostgreSQL-1-1-1024-1-1               1         32   16384       1      1  300.0           0                  16286.720704               16286.764037         0.0                                                       6340.0                                               1214.0

#### Aggregated Parallel
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         32   16384          1  300.0           0                      16286.72                   16286.76         0.0                                                       6340.0                                               1214.0

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1       50.0        1.0   1.0            72000.0

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```




### YCSB Simple Testrun Workload E

For performing the experiment we can run the [benchbase file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/benchbase.py).

Example:
```bash
bexhoma benchbase -tr \
  -sf 1000 \
  -xsd 5 \
  --benchmark ycsb \
  --workload e \
  -dbms PostgreSQL \
  -nlt 64 \
  -nbp 1 \
  -nbt 32 \
  -xnbf 16 \
  -xtb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_ycsb_e.log
```

This time we only use a single benchmarking pod.
This is because the workload contains INSERTs and two parallel pods would try to insert the same data.
Other than the original YCSB tool, Benchbase does not offer an option to limit the range of keys to be inserted.

### Evaluate Results

At the end of a benchmark you will see a summary like

doc_benchbase_testcase_ycsb_e.log
```markdown
﻿## Show Summary

### Workload
Benchbase Workload ycsb SF=1000
    Type: benchbase
    Duration: 612s 
    Code: 1769699731
    Intro: Benchbase runs an YCSB experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'ycsb'. Workload is 'e'. Scaling factor is 1000. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.20.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [64] threads, split into [1] pods.
    Benchmarking is tested with [32] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97295
    datadisk:2297
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1769699731
                TENANT_VOL:False

### Execution

#### Per Pod
                         experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                     
PostgreSQL-1-1-1024-1-1               1         32   16384       1      1  300.0           0                   2788.339637                2788.446304         0.0                                                      23818.0                                              11464.0

#### Aggregated Parallel
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         32   16384          1  300.0           0                       2788.34                    2788.45         0.0                                                      23818.0                                              11464.0

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1       45.0        1.0   1.0            80000.0

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```




### YCSB Simple Testrun Workload F

For performing the experiment we can run the [benchbase file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/benchbase.py).

Example:
```bash
bexhoma benchbase -tr \
  -sf 1000 \
  -xsd 5 \
  --benchmark ycsb \
  --workload f \
  -dbms PostgreSQL \
  -nlt 64 \
  -nbp 1,2 \
  -nbt 32 \
  -xnbf 16 \
  -xtb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_ycsb_f.log
```

### Evaluate Results

At the end of a benchmark you will see a summary like

doc_benchbase_testcase_ycsb_f.log
```markdown
﻿## Show Summary

### Workload
Benchbase Workload ycsb SF=1000
    Type: benchbase
    Duration: 967s 
    Code: 1769700391
    Intro: Benchbase runs an YCSB experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'ycsb'. Workload is 'f'. Scaling factor is 1000. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.20.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [64] threads, split into [1] pods.
    Benchmarking is tested with [32] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97295
    datadisk:2297
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1769700391
                TENANT_VOL:False
PostgreSQL-1-1-1024-2 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97789
    datadisk:2791
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1769700391
                TENANT_VOL:False

### Execution

#### Per Pod
                         experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                     
PostgreSQL-1-1-1024-1-1               1         32   16384       1      1  300.0           0                   1694.903109                1695.009776         0.0                                                      41243.0                                              18865.0
PostgreSQL-1-1-1024-2-1               1         16    8192       2      1  300.0           0                    830.676481                 830.729815         0.0                                                      41126.0                                              19245.0
PostgreSQL-1-1-1024-2-2               1         16    8192       2      2  300.0           0                    861.889900                 861.943234         0.0                                                      40662.0                                              18546.0

#### Aggregated Parallel
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         32   16384          1  300.0           0                       1694.90                    1695.01         0.0                                                      41243.0                                              18865.0
PostgreSQL-1-1-1024-2               1         32   16384          2  300.0           0                       1692.57                    1692.67         0.0                                                      41126.0                                              18895.5

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[2, 1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1       34.0        1.0   1.0      105882.352941
PostgreSQL-1-1-1024-2       34.0        1.0   2.0      105882.352941

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```





