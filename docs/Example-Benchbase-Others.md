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

> The Twitter workload is inspired by the popular micro-blogging
website. In order to provide a realistic benchmark, we obtained
an anonymized snapshot of the Twitter social graph from August
2009 that contains 51 million users and almost 2 billion “follows”
relationships [...]. We created a synthetic workload generator that
is based on an approximation of the queries/transactions needed to
support the application functionalities as we observe them by using the web site, along with information derived from a data set
of 200,000 tweets. Although we do not claim that this is a precise
representation of Twitter’s system, it still reflects its important characteristics, such as heavily skewed many-to-many relationships. [1]

1. OLTP-Bench: An Extensible Testbed for Benchmarking Relational Databases: http://www.vldb.org/pvldb/vol7/p277-difallah.pdf
1. Image Benchbase Twitter Benchmark: https://github.com/cmu-db/benchbase/wiki/Twitter

You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"

mkdir -p $LOG_DIR
```

### Twitter Simple Testrun

For performing the experiment we can run the [benchbase file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/benchbase.py).

Example:
```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms PostgreSQL \
  -nbp 1 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -b twitter \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_twitter_simple.log &
```

This
* starts a clean instance of PostgreSQL (`-dbms`)
  * data directory inside a Docker container
* starts 1 loader pod (per DBMS) that
  * creates the schema in the database
  * imports data for scale factor 16 (`-sf`) (i.e., 16 * 500 the number of users) into the DBMS
  * using all threads of driver machine (benchbase setting)
* runs streams of twitter queries (per DBMS)
    * running for 5 (`-sd`) minutes
    * each stream (pod) having 16 threads to simulate 16 users (`-nbt`)
    * `-nbp`: first stream 1 pod
    * target is 16x(`-ltf`) 1024 (`-tb`) ops
* with a maximum of 1 DBMS per time (`-ms`)
* tests if results match workflow (`-tr`)
* shows a summary

### Evaluate Results

At the end of a benchmark you will see a summary like

doc_benchbase_testcase_twitter_simple
```markdown
## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 625s 
    Code: 1744645235
    Benchbase runs the Twitter benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'twitter'. Scaling factor (e.g., number of warehouses for TPC-C) is 16. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
    Experiment uses bexhoma version 0.8.4.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:202609136
    datadisk:264
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1744645235

### Execution
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         16   16384          1  300.0           0                        689.61                     689.66         0.0                                                      41497.0                                              23190.0

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-1-1-1024-1        4.0        1.0   1.0                    14400.0

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```

### SQL Scrips

The SQL scripts for pre and post ingestion can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/benchbase/twitter

There are per DBMS
* `initschema`-files, that are invoked before loading of data
* `checkschema`-files, that are invoked after loading of data

You can find the output of the files in the result folder.


### Twitter More Complex


```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 1600 \
  -sd 20 \
  -dbms PostgreSQL \
  -nbp 1,2,4,8 \
  -nbt 160 \
  -nbf 16 \
  -tb 1024 \
  -b twitter \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -m -mc \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_twitter_scale.log &
```

### Evaluate Results

doc_benchbase_testcase_twitter_scale.log
```markdown
## Show Summary

### Workload
Benchbase Workload SF=100
    Type: benchbase
    Duration: 10011s 
    Code: 1744653338
    Benchbase runs the CH-Benchmark benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'chbenchmark'. Scaling factor (e.g., number of warehouses for TPC-C) is 100. Benchmarking runs for 20 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
    Experiment uses bexhoma version 0.8.4.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [100] threads, split into [1, 2, 5, 10] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:229528392
    datadisk:26552
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1744653338
PostgreSQL-1-1-1024-2 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:229529532
    datadisk:26553
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1744653338
PostgreSQL-1-1-1024-3 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:229530724
    datadisk:26554
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    eval_parameters
                code:1744653338
PostgreSQL-1-1-1024-4 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:229530392
    datadisk:26554
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    eval_parameters
                code:1744653338

### Execution
                       experiment_run  terminals  target  pod_count    time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1        100   16384          1  1200.0           0                          1.44                       1.52         0.0                                                  146801459.0                                           39862157.0
PostgreSQL-1-1-1024-2               1        100   16384          2  1200.0           0                          1.51                       1.59         0.0                                                  156391241.0                                           40505643.0
PostgreSQL-1-1-1024-3               1        100   16380          5  1200.0           0                          1.50                       1.58         0.0                                                  171752857.0                                           44080615.0
PostgreSQL-1-1-1024-4               1        100   16380         10  1200.0           0                          1.45                       1.53         0.0                                                  166367823.0                                           40179146.0

Warehouses: 100

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[10, 2, 5, 1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2, 5, 10]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-1-1-1024-1      540.0        1.0   1.0                 666.666667
PostgreSQL-1-1-1024-2      540.0        1.0   2.0                 666.666667
PostgreSQL-1-1-1024-3      540.0        1.0   5.0                 666.666667
PostgreSQL-1-1-1024-4      540.0        1.0  10.0                 666.666667

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
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

mkdir -p $LOG_DIR
```

### CH-benCHmark Simple Testrun

For performing the experiment we can run the [benchbase file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/benchbase.py).

Example:
```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 10 \
  -sd 5 \
  -dbms PostgreSQL \
  -nbp 1 \
  -nbt 100 \
  -nbf 16 \
  -tb 1024 \
  -b chbenchmark \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_chbenchmark_simple.log &
```

This
* starts a clean instance of PostgreSQL (`-dbms`)
  * data directory inside a Docker container
* starts 1 loader pod (per DBMS) that
  * creates the schema in the database
  * imports data for scale factor 16 (`-sf`) (i.e., 16 * 500 the number of users) into the DBMS
  * using all threads of driver machine (benchbase setting)
* runs streams of twitter queries (per DBMS)
    * running for 5 (`-sd`) minutes
    * each stream (pod) having 16 threads to simulate 16 users (`-nbt`)
    * `-nbp`: first stream 1 pod
    * target is 16x(`-ltf`) 1024 (`-tb`) ops
* with a maximum of 1 DBMS per time (`-ms`)
* tests if results match workflow (`-tr`)
* shows a summary

### Evaluate Results

At the end of a benchmark you will see a summary like

doc_benchbase_testcase_chbenchmark_simple.log
```markdown
## Show Summary

### Workload
Benchbase Workload SF=10
    Type: benchbase
    Duration: 1469s 
    Code: 1747700828
    Benchbase runs the CH-Benchmark benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'chbenchmark'. Scaling factor is 10. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
    Experiment uses bexhoma version 0.8.5.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [100] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:256844040
    datadisk:2722
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1747700828

### Execution
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1        100   16384          1  300.0           0                          3.61                       3.94         0.0                                                   19443973.0                                            6507230.0

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1       93.0        1.0   1.0         387.096774

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```

### SQL Scrips

The SQL scripts for pre and post ingestion can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/benchbase/chbenchmark

There are per DBMS
* `initschema`-files, that are invoked before loading of data
* `checkschema`-files, that are invoked after loading of data

You can find the output of the files in the result folder.


### CH-benCHmark More Complex


```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 100 \
  -sd 20 \
  -dbms PostgreSQL \
  -nbp 1,2,5,10 \
  -nbt 100 \
  -nbf 16 \
  -tb 1024 \
  -b chbenchmark \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_chbenchmark_scale.log &
```

### Evaluate Results

doc_benchbase_testcase_chbenchmark_scale.log
```markdown
## Show Summary

### Workload
Benchbase Workload SF=100
    Type: benchbase
    Duration: 10011s 
    Code: 1744653338
    Benchbase runs the CH-Benchmark benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'chbenchmark'. Scaling factor (e.g., number of warehouses for TPC-C) is 100. Benchmarking runs for 20 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
    Experiment uses bexhoma version 0.8.4.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [100] threads, split into [1, 2, 5, 10] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:229528392
    datadisk:26552
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1744653338
PostgreSQL-1-1-1024-2 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:229529532
    datadisk:26553
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1744653338
PostgreSQL-1-1-1024-3 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:229530724
    datadisk:26554
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    eval_parameters
                code:1744653338
PostgreSQL-1-1-1024-4 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:229530392
    datadisk:26554
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    eval_parameters
                code:1744653338

### Execution
                       experiment_run  terminals  target  pod_count    time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1        100   16384          1  1200.0           0                          1.44                       1.52         0.0                                                  146801459.0                                           39862157.0
PostgreSQL-1-1-1024-2               1        100   16384          2  1200.0           0                          1.51                       1.59         0.0                                                  156391241.0                                           40505643.0
PostgreSQL-1-1-1024-3               1        100   16380          5  1200.0           0                          1.50                       1.58         0.0                                                  171752857.0                                           44080615.0
PostgreSQL-1-1-1024-4               1        100   16380         10  1200.0           0                          1.45                       1.53         0.0                                                  166367823.0                                           40179146.0

Warehouses: 100

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[10, 2, 5, 1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2, 5, 10]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-1-1-1024-1      540.0        1.0   1.0                 666.666667
PostgreSQL-1-1-1024-2      540.0        1.0   2.0                 666.666667
PostgreSQL-1-1-1024-3      540.0        1.0   5.0                 666.666667
PostgreSQL-1-1-1024-4      540.0        1.0  10.0                 666.666667

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

mkdir -p $LOG_DIR
```

### YCSB Simple Testrun Workload C

For performing the experiment we can run the [benchbase file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/benchbase.py).

Example:
```bash
nohup python benchbase.py -tr \
  -sf 1000 \
  -sd 5 \
  --benchmark ycsb \
  --workload c \
  -dbms PostgreSQL \
  -nlt 64 \
  -nbp 1,2 \
  -nbt 32 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_ycsb_c.log &
```

This
* starts a clean instance of PostgreSQL (`-dbms`)
  * data directory inside a Docker container
* starts 1 loader pod (per DBMS) that
  * creates the schema in the database
  * imports data for scale factor 1000 (`-sf`) (i.e., 1000 * 1000 the number of rows) into the DBMS
  * using all threads of driver machine (benchbase setting)
* runs streams of ycsb (`--benchmark`) queries (per DBMS) workload c (`--workload`)
    * running for 5 (`-sd`) minutes
    * each stream (pod) having 32 threads to simulate 32 users (`-nbt`)
    * `-nbp`: first stream 1 pod, second stream 2 pods
    * target is 16x(`-ltf`) 1024 (`-tb`) ops
* with a maximum of 1 DBMS per time (`-ms`)
* tests if results match workflow (`-tr`)
* shows a summary

### Evaluate Results

At the end of a benchmark you will see a summary like

doc_benchbase_testcase_ycsb_c.log
```markdown
## Show Summary

### Workload
Benchbase Workload SF=1000
    Type: benchbase
    Duration: 1031s 
    Code: 1747712652
    Benchbase runs the YCSB benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'ycsb'. Workload is 'c'. Scaling factor is 1000. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
    Experiment uses bexhoma version 0.8.5.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [1] pods.
    Benchmarking is tested with [32] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:256417620
    datadisk:2297
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1747712652
PostgreSQL-1-1-1024-2 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:256417620
    datadisk:2297
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1747712652

### Execution
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         32   16384          1  300.0           0                      16384.06                   16384.06         0.0                                                        552.0                                                462.0
PostgreSQL-1-1-1024-2               1         32   16384          2  300.0           0                      16384.08                   16384.09         0.0                                                        566.0                                                474.0

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[2, 1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1        7.0        1.0   1.0      514285.714286
PostgreSQL-1-1-1024-2        7.0        1.0   2.0      514285.714286

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```



### YCSB Simple Testrun Workload A

For performing the experiment we can run the [benchbase file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/benchbase.py).

Example:
```bash
nohup python benchbase.py -tr \
  -sf 1000 \
  -sd 5 \
  --benchmark ycsb \
  --workload a \
  -dbms PostgreSQL \
  -nlt 64 \
  -nbp 1,2 \
  -nbt 32 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_ycsb_a.log &
```


### Evaluate Results

At the end of a benchmark you will see a summary like

doc_benchbase_testcase_ycsb_a.log
```markdown
## Show Summary

### Workload
Benchbase Workload SF=1000
    Type: benchbase
    Duration: 1031s 
    Code: 1747713732
    Benchbase runs the YCSB benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'ycsb'. Workload is 'a'. Scaling factor is 1000. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
    Experiment uses bexhoma version 0.8.5.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [1] pods.
    Benchmarking is tested with [32] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:256417604
    datadisk:2297
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1747713732
PostgreSQL-1-1-1024-2 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:260204816
    datadisk:5996
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1747713732

### Execution
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         32   16384          1  300.0           0                      16384.05                   16384.06         0.0                                                        631.0                                                507.0
PostgreSQL-1-1-1024-2               1         32   16384          2  300.0           0                      16384.06                   16384.07         0.0                                                        649.0                                                523.0

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1        7.0        1.0   1.0      514285.714286
PostgreSQL-1-1-1024-2        7.0        1.0   2.0      514285.714286

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```


### YCSB Simple Testrun Workload B

For performing the experiment we can run the [benchbase file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/benchbase.py).

Example:
```bash
nohup python benchbase.py -tr \
  -sf 1000 \
  -sd 5 \
  --benchmark ycsb \
  --workload b \
  -dbms PostgreSQL \
  -nlt 64 \
  -nbp 1,2 \
  -nbt 32 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_ycsb_b.log &
```


### Evaluate Results

At the end of a benchmark you will see a summary like

doc_benchbase_testcase_ycsb_b.log
```markdown
## Show Summary

### Workload
Benchbase Workload SF=1000
    Type: benchbase
    Duration: 1031s 
    Code: 1747714812
    Benchbase runs the YCSB benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'ycsb'. Workload is 'b'. Scaling factor is 1000. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
    Experiment uses bexhoma version 0.8.5.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [1] pods.
    Benchmarking is tested with [32] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:256417616
    datadisk:2297
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1747714812
PostgreSQL-1-1-1024-2 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:256829112
    datadisk:2699
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1747714812

### Execution
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         32   16384          1  300.0           0                      16384.14                   16384.14         0.0                                                        590.0                                                474.0
PostgreSQL-1-1-1024-2               1         32   16384          2  300.0           0                      16384.05                   16384.06         0.0                                                        590.0                                                483.0

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[2, 1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1        7.0        1.0   1.0      514285.714286
PostgreSQL-1-1-1024-2        7.0        1.0   2.0      514285.714286

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```




### YCSB Simple Testrun Workload D

For performing the experiment we can run the [benchbase file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/benchbase.py).

Example:
```bash
nohup python benchbase.py -tr \
  -sf 1000 \
  -sd 5 \
  --benchmark ycsb \
  --workload d \
  -dbms PostgreSQL \
  -nlt 64 \
  -nbp 1 \
  -nbt 32 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_ycsb_d.log &
```

This time we only use a single benchmarking pod.
This is because the workload contains INSERTs and two parallel pods would try to insert the same data.
Other than the original YCSB tool, Benchbase does not offer an option to limit the range of keys to be inserted.

### Evaluate Results

At the end of a benchmark you will see a summary like

doc_benchbase_testcase_ycsb_d.log
```markdown
## Show Summary

### Workload
Benchbase Workload SF=1000
    Type: benchbase
    Duration: 655s 
    Code: 1747715893
    Benchbase runs the YCSB benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'ycsb'. Workload is 'd'. Scaling factor is 1000. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
    Experiment uses bexhoma version 0.8.5.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [1] pods.
    Benchmarking is tested with [32] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:256421144
    datadisk:2297
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1747715893

### Execution
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         32   16384          1  300.0           0                      16384.06                   16384.07         0.0                                                        567.0                                                466.0

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1        6.0        1.0   1.0           600000.0

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```




### YCSB Simple Testrun Workload E

For performing the experiment we can run the [benchbase file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/benchbase.py).

Example:
```bash
nohup python benchbase.py -tr \
  -sf 1000 \
  -sd 5 \
  --benchmark ycsb \
  --workload e \
  -dbms PostgreSQL \
  -nlt 64 \
  -nbp 1 \
  -nbt 32 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_ycsb_e.log &
```

This time we only use a single benchmarking pod.
This is because the workload contains INSERTs and two parallel pods would try to insert the same data.
Other than the original YCSB tool, Benchbase does not offer an option to limit the range of keys to be inserted.

### Evaluate Results

At the end of a benchmark you will see a summary like

doc_benchbase_testcase_ycsb_e.log
```markdown
## Show Summary

### Workload
Benchbase Workload SF=1000
    Type: benchbase
    Duration: 623s 
    Code: 1747716553
    Benchbase runs the YCSB benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'ycsb'. Workload is 'e'. Scaling factor is 1000. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
    Experiment uses bexhoma version 0.8.5.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [1] pods.
    Benchmarking is tested with [32] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:256421128
    datadisk:2297
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1747716553

### Execution
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         32   16384          1  300.0           0                         70.11                      70.22         0.0                                                     746867.0                                             456019.0

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1        7.0        1.0   1.0      514285.714286

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```




### YCSB Simple Testrun Workload F

For performing the experiment we can run the [benchbase file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/benchbase.py).

Example:
```bash
nohup python benchbase.py -tr \
  -sf 1000 \
  -sd 5 \
  --benchmark ycsb \
  --workload f \
  -dbms PostgreSQL \
  -nlt 64 \
  -nbp 1,2 \
  -nbt 32 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_ycsb_f.log &
```

### Evaluate Results

At the end of a benchmark you will see a summary like

doc_benchbase_testcase_ycsb_f.log
```markdown
## Show Summary

### Workload
Benchbase Workload SF=1000
    Type: benchbase
    Duration: 1029s 
    Code: 1747717213
    Benchbase runs the YCSB benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'ycsb'. Workload is 'f'. Scaling factor is 1000. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
    Experiment uses bexhoma version 0.8.5.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [1] pods.
    Benchmarking is tested with [32] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:256421128
    datadisk:2297
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1747717213
PostgreSQL-1-1-1024-2 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:260343692
    datadisk:6128
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1747717213

### Execution
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         32   16384          1  300.0           0                      16384.04                   16384.06         0.0                                                        950.0                                                672.0
PostgreSQL-1-1-1024-2               1         32   16384          2  300.0           0                      16384.06                   16384.06         0.0                                                        959.0                                                677.5

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[2, 1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1        6.0        1.0   1.0           600000.0
PostgreSQL-1-1-1024-2        6.0        1.0   2.0           600000.0

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```



