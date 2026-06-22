# Example: Benchmark TiDB

This differs from the default behaviour of bexhoma, since we benchmark **a distributed DBMS, that can be managed by bexhoma** and exists in the Kubernetes cluster in the same namespace.
TiDB is a disaggregated DBMS.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

TiDB offers several installation methods, including an operator [1].
We here rely on a [manifest](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-TiDB.yml) for a version that is suitable for bexhoma.
TiDB clusters consist of three core components: TiDB, PD (Placement Driver), and TiKV.
Unlike traditional databases, TiDB does not require a single coordinator node - PD handles cluster metadata management and scheduling.
In Bexhoma, TiDB pods are deployed as a Deployment, PD as a StatefulSet, and TiKV as another StatefulSet to ensure stable identities and persistent storage.
A Kubernetes Service exposes TiDB for external communication within the cluster, while headless Services enable internal discovery and communication between PD and TiKV pods.

This can be managed by bexhoma.


**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. Get started with TiDB:  https://docs.pingcap.com/tidb-in-kubernetes/stable/get-started/
1. YCSB Repository: https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload
1. Benchmarking cloud serving systems with YCSB: https://dl.acm.org/doi/10.1145/1807128.1807152
1. Benchbase Repository: https://github.com/cmu-db/benchbase/wiki/TPC-C
1. OLTP-Bench: An Extensible Testbed for Benchmarking Relational Databases: http://www.vldb.org/pvldb/vol7/p277-difallah.pdf
1. Orchestrating DBMS Benchmarking in the Cloud with Kubernetes: https://doi.org/10.1007/978-3-030-94437-7_6
1. A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools: https://doi.org/10.1007/978-3-031-68031-1_9


## Perform YCSB Benchmark - Ingestion of Data Included

You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"
BEXHOMA_MS=1

mkdir -p $LOG_DIR
```

For performing the experiment we can run the [ycsb file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/ycsb.py).

Example: 
```bash
bexhoma ycsb \
  -dbms TiDB \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 1 \
  -xnlf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xnsr 3 \
  -nw 3 \
  -nwr 3 \
  -xop 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  run &>$LOG_DIR/doc_ycsb_tidb_1.log
```

This
* loops over `n` in [8] and `t` in [4]
  * starts a clean instance of TiDB (`-dbms`) with 3 workers (`-nw`), i.e., PD and TiKV, with 3 main pods (`-xnsr`), i.e. TiDB, and replication factor 3 (`-nwr`)
    * data directory inside a Docker container
  * creates YCSB schema in each database
  * starts `n` loader pods per DBMS
    * with a loading container each
      * threads = 64/`n` (`-nlt`)
      * target throughput is `t` * 16384
      * generates YCSB data = 1.000.000 rows (i.e., SF=10, `-sf`)
      * imports it into the DBMS
  * loops over `m` in [1] and `s` in [1]
    * runs `m` parallel streams of YCSB queries per DBMS
      * 1.000.000 operations (`-xop`)
      * workload A = 50% read / 50% write (`--workload`)
      * target throughput is `s` * 16384
      * threads = 64/`m` (`-nbt`)
    * with a maximum of 1 DBMS per time (`-ms`)
* tests if results match workflow (`-tr`)
* monitors (`-m`) all components (`-mc`)
* shows a summary

### Status

You can watch the status while benchmark is running via `bexperiments status`

```bash
Dashboard: Running
Cluster Prometheus: Running
Message Queue: Running
Data directory: Running
Result directory: Running
+-----------------+--------------+--------------+------------+-------------+
| 1761748555      | sut          |   loaded [s] | use case   | worker      |
+=================+==============+==============+============+=============+
| TiDB-64-8-16384 | (1. Running) |          409 | ycsb       | (3 Running) |
+-----------------+--------------+--------------+------------+-------------+
```

The code `1761748555` is the unique identifier of the experiment.
You can find the number also in the output of `ycsb.py`.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1761748555` (removes everything that is related to experiment `1761748555`).

## Evaluate Results

At the end of a benchmark you will see a summary like

doc_ycsb_tidb_1.log
```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 457s 
* Code: 1782072943
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Experiment uses bexhoma version 0.9.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['TiDB'].
  * Import is handled by 8 processes (pods).
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* TiDB-1-1-1-1 uses docker image pingcap/tidb:v7.1.6
  * RAM:540590841856
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-117-generic
  * node:cl-worker25
  * disk:184602
  * cpu_list:0-95
  * requests_cpu:4
  * requests_memory:16Gi
  * sut 0
    * RAM:540590841856
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-117-generic
    * node:cl-worker25
    * disk:184602
    * cpu_list:0-95
  * sut 1
    * RAM:540579295232
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-124-generic
    * node:cl-worker22
    * disk:399606
    * cpu_list:0-127
  * sut 2
    * RAM:540590825472
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-117-generic
    * node:cl-worker23
    * disk:1419279
    * cpu_list:0-95
  * pd 0
    * RAM:540597927936
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-124-generic
    * node:cl-worker39
    * disk:277866
    * cpu_list:0-255
  * pd 1
    * RAM:540590841856
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-117-generic
    * node:cl-worker25
    * disk:184602
    * cpu_list:0-95
  * pd 2
    * RAM:540590825472
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-117-generic
    * node:cl-worker23
    * disk:1419279
    * cpu_list:0-95
  * tikv 0
    * RAM:1077382602752
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-1052-nvidia
    * node:cl-worker28
    * disk:393225
    * cpu_list:0-255
  * tikv 1
    * RAM:540597927936
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-124-generic
    * node:cl-worker39
    * disk:277866
    * cpu_list:0-255
  * tikv 2
    * RAM:1077381271552
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1354293
    * cpu_list:0-255
  * eval_parameters
    * code:1782072943
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Workflow

#### Actual

* DBMS TiDB-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS TiDB-1 - Experiment 1 Client 1: ycsb (1 pods)
    experiment.process()
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\experiments\base.py", line 291, in process
    self.show_summary()
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\experiments\mixed.py", line 126, in show_summary
    benchmark.show_summary(self)
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\benchmarks\base.py", line 155, in show_summary
    df_loading = self._show_loading_sections(experiment, is_multitenant)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\benchmarks\ycsb.py", line 136, in _show_loading_sections
    df_loading = self.evaluator.get_summary_loading_per_connection()
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\evaluators\ycsb.py", line 1038, in get_summary_loading_per_connection
    df_plot = self.loading_set_datatypes(df)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\evaluators\ycsb.py", line 452, in loading_set_datatypes
    df_typed = df.astype({
               ^^^^^^^^^^^
  File "C:\Users\Patrick\anaconda3\envs\bexhoma\Lib\site-packages\pandas\core\generic.py", line 6627, in astype
    raise KeyError(
KeyError: "Only a column name can be used for the key in a dtype mappings argument. '[CLEANUP].Operations' not found in columns."
```

To see the summary again you can simply call `bexperiments summary -e 1761748555` with the experiment code.

### Detailed Evaluation

Results are transformed into pandas DataFrames and can be inspected in detail.
See for example
* [Jupyter Notebooks](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/evaluator_dbmsbenchmarker/notebooks/)

You can connect to an evaluation server locally by `bexperiments jupyter`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888




## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).

All metrics in monitoring are summed across all matching components of the same type.
In this example, this means that used memory, CPU time, etc. are summed across all nodes of the TiDB cluster for the components PD, TiKV and TiDB resp.

## Use Persistent Storage

**Persistent storage currently is not yet implemented.**


## YCSB Example Explained

### Configuration of Bexhoma

In `cluster.config` there is a section:

```python
'TiDB': {
    'loadData': 'mysql --local-infile -h 127.0.0.1 -P 4000 < {scriptname}',
    'delay_prepare': 60,
    'template': {
        'version': 'CE 8.0.22',
        'alias': 'General-C',
        'docker_alias': 'GP-C',
        'dialect': 'MySQL',
        'JDBC': {
            'driver': "com.mysql.cj.jdbc.Driver",
            'auth': ["root", "root"],
            'url': 'jdbc:mysql://{serverip}:9091/{dbname}',
            'jar': ['mysql-connector-j-8.0.31.jar', 'slf4j-simple-1.7.21.jar'],
            'database': 'test',
        }
    },
    'logfile': '/var/log/mysqld.log',
    'datadir': '/var/lib/mysql/',
    'priceperhourdollar': 0.0,
    'worker_port': 2379,
    'store_args': False,
},
```

where
* `loadData`: This command is used to create the schema
* `JDBC`: These infos are used to configure YCSB
* `worker_port`: This tells bexhoma what the port for internal communication is
* `store_args`: This tells bexhoma not to log args of the containers, since they do not contain parameters

TiDB uses the MySQL JDBC driver.



### Schema SQL File

If data should be loaded, bexhoma at first creates a schema according to: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/TiDB







## Benchbase's TPC-C

### Simple Run

TPC-C is performed at 16 warehouses.
The 16 threads of the client are split into a cascading sequence of 1 and 2 pods.
TiDB has 3 workers (TiDB, PD and TiKV).

```bash
bexhoma benchbase \
  -dbms TiDB \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 16 \
  -xnsr 3 \
  -nw 3 \
  -nwr 3 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  run &>$LOG_DIR/doc_benchbase_tidb_1.log
```

### Evaluate Results

doc_benchbase_tidb_1.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 2242s 
* Code: 1781989868
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['TiDB'].
  * Import is handled by 1 processes (pods).
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* TiDB-1-1-1-1 uses docker image pingcap/tidb:v7.1.6
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1352694
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * sut 0
    * RAM:2164173246464
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:1352695
    * cpu_list:0-223
  * sut 1
    * RAM:1081853939712
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:610110
    * cpu_list:0-127
  * sut 2
    * RAM:540597927936
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-124-generic
    * node:cl-worker39
    * disk:268232
    * cpu_list:0-255
  * pd 0
    * RAM:2164173246464
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:1352694
    * cpu_list:0-223
  * pd 1
    * RAM:540579295232
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-124-generic
    * node:cl-worker22
    * disk:408647
    * cpu_list:0-127
  * pd 2
    * RAM:540597927936
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-124-generic
    * node:cl-worker39
    * disk:268232
    * cpu_list:0-255
  * tikv 0
    * RAM:2164173246464
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:1352695
    * cpu_list:0-223
  * tikv 1
    * RAM:1081649803264
    * CPU:AMD EPYC 7453 28-Core Processor
    * Cores:56
    * host:6.8.0-111-generic
    * node:cl-worker34
    * disk:319309
    * cpu_list:0-55
  * tikv 2
    * RAM:540579295232
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-124-generic
    * node:cl-worker22
    * disk:408647
    * cpu_list:0-127
  * eval_parameters
    * code:1781989868
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* TiDB-1-1-2-1 uses docker image pingcap/tidb:v7.1.6
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1349409
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * sut 0
    * RAM:2164173246464
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:1349410
    * cpu_list:0-223
  * sut 1
    * RAM:1081853939712
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:610111
    * cpu_list:0-127
  * sut 2
    * RAM:540597927936
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-124-generic
    * node:cl-worker39
    * disk:268234
    * cpu_list:0-255
  * pd 0
    * RAM:2164173246464
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:1349409
    * cpu_list:0-223
  * pd 1
    * RAM:540579295232
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-124-generic
    * node:cl-worker22
    * disk:405272
    * cpu_list:0-127
  * pd 2
    * RAM:540597927936
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-124-generic
    * node:cl-worker39
    * disk:268234
    * cpu_list:0-255
  * tikv 0
    * RAM:2164173246464
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:1349410
    * cpu_list:0-223
  * tikv 1
    * RAM:1081649803264
    * CPU:AMD EPYC 7453 28-Core Processor
    * Cores:56
    * host:6.8.0-111-generic
    * node:cl-worker34
    * disk:316144
    * cpu_list:0-55
  * tikv 2
    * RAM:540579295232
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-124-generic
    * node:cl-worker22
    * disk:405272
    * cpu_list:0-127
  * eval_parameters
    * code:1781989868
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Workflow

#### Actual

* DBMS TiDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS TiDB-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS TiDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS TiDB-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

|          |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| TiDB-1-1 |                1 |   16 |     1550.00 |           1.00 |            0.00 |        692.00 |          857.00 |              1 |           1 |             | None           |             0 | False         |               37.16 |

### Execution

#### Per Connection

| DBMS           | phase      | job          |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------|:-----------|:-------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| TiDB-1-1-1-1-1 | TiDB-1-1-1 | TiDB-1-1-1-1 |                1 |          16 |    16384 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                         135.02 |                      134.50 |         0.00 |                                                     232020.00 |                                             118465.00 |
| TiDB-1-1-2-1-1 | TiDB-1-1-2 | TiDB-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       1 |          -1 | 300.00 |            0 |                          54.37 |                       53.95 |         0.00 |                                                     310406.00 |                                             147058.00 |
| TiDB-1-1-2-1-2 | TiDB-1-1-2 | TiDB-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       2 |          -1 | 300.00 |            0 |                          55.16 |                       54.76 |         0.00 |                                                     303193.00 |                                             144977.00 |

#### Per Phase

| DBMS       | phase      |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------|:-----------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| TiDB-1-1-1 | TiDB-1-1-1 |                1 |          16 |    16384 |               1 |           1 |          -1 | 300.00 |            0 |                         135.02 |                      134.50 |         0.00 |                                                     232020.00 |                                             118465.00 |
| TiDB-1-1-2 | TiDB-1-1-2 |                1 |          16 |    16384 |               1 |           2 |          -1 | 300.00 |            0 |                         109.53 |                      108.72 |         0.00 |                                                     310406.00 |                                             146017.50 |

### Monitoring

### Loading phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |      3452.44 |     28.66 |           4.30 |                  4.45 |
| TiDB-1-1-2-1 |      3452.44 |     28.66 |           4.30 |                  4.45 |

### Loading phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |       134.49 |      0.26 |           0.28 |                  0.28 |
| TiDB-1-1-2-1 |       134.49 |      0.26 |           0.28 |                  0.28 |

### Loading phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |      1983.73 |      5.85 |          10.36 |                 29.58 |
| TiDB-1-1-2-1 |      1983.73 |      5.85 |          10.36 |                 29.58 |

### Loading phase: component loader

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |       141.14 |      1.10 |           0.51 |                  0.52 |
| TiDB-1-1-2-1 |       141.14 |      1.10 |           0.51 |                  0.52 |

### Execution phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |      1396.95 |      5.24 |           1.59 |                  1.77 |
| TiDB-1-1-2-1 |      1274.08 |      4.64 |           1.74 |                  1.92 |

### Execution phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |       151.81 |      0.55 |           0.26 |                  0.26 |
| TiDB-1-1-2-1 |       138.04 |      0.49 |           0.27 |                  0.27 |

### Execution phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |       679.74 |      2.54 |          11.81 |                 31.95 |
| TiDB-1-1-2-1 |       615.81 |      2.17 |          13.17 |                 24.50 |

### Execution phase: component benchmarker

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |       106.63 |      0.38 |           0.31 |                  0.31 |
| TiDB-1-1-2-1 |       106.63 |      0.49 |           0.31 |                  0.31 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component pd contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component tikv contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component pd contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component tikv contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```


