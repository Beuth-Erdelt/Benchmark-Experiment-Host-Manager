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

## Scaling TiDB Components

TiDB has three independently deployed components, and bexhoma exposes an independent scaling flag for each of them:

| Component | Kubernetes kind | Flag | Default | Notes |
|---|---|---|---|---|
| TiKV (storage) | StatefulSet, `component: tikv` | `-nw` / `--num-worker` | 0 | The storage/sharding layer - this is the "worker" count used for every distributed DBMS in bexhoma. |
| PD (Placement Driver) | StatefulSet, `component: pd` | `-xnpd` / `--xnum-pd-nodes` | 3 | Cluster metadata/scheduling nodes. Sized independently of `-nw`, since PD and TiKV serve different roles and typically need different counts (PD is usually kept at a small odd number for quorum, e.g. 3 or 5; TiKV scales with storage/throughput needs). |
| TiDB server (SQL frontend) | Deployment, `component: sut` | `-xnsr` / `--xnum-sut-replicas` | 1 | Stateless SQL frontend; scales independently of storage. |

Example: `-nw 6 -xnpd 3 -xnsr 2` deploys 6 TiKV nodes, 3 PD nodes, and 2 `tidb-server` pods.

Two more scaling-related flags exist but are **not** pod-count knobs for TiDB:
* `-nwr` / `--num-worker-replicas` sets PD's `max-replicas` raft configuration (`SET CONFIG pd max-replicas = {num_worker_replicas}`, run once as part of the init schema) - the number of Raft replicas TiKV keeps per data region, a data-durability setting independent of how many TiKV/PD pods are actually running. It is exposed as `BEXHOMA_REPLICAS` on the SUT pods and in the eval summary, but no container in the TiDB manifest uses it as a pod count.
* `-nws` / `--num-worker-shards` currently has **no effect** for TiDB - it's a DDL parameter only wired up for Citus (`SET citus.shard_count = ...`). It is still parsed (shared across all entry scripts) but the TiDB init schema does not reference it.

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
BEXHOMA_STORAGE_CLASS="shared"

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
  -xnpd 3 \
  -nwr 3 \
  -xop 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  run &>$LOG_DIR/docs_ycsb_tidb_1.log
```

This
* loops over `n` in [8] and `t` in [4]
  * starts a clean instance of TiDB (`-dbms`) with 3 TiKV nodes (`-nw`), 3 PD nodes (`-xnpd`), 3 tidb-server pods (`-xnsr`), and a PD raft replication factor of 3 (`-nwr`) - see [Scaling TiDB Components](#scaling-tidb-components)
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

You can watch the status while benchmark is running via `bexhoma status`

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

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_tidb_1_summary.md" target="_blank" rel="noopener">docs_ycsb_tidb_1.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 785s 
* Code: 1783870690
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
  * Experiment uses bexhoma version 0.10.5.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['TiDB'].
  * Import is handled by 8 processes (pods).
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* TiDB-1-1-1-1 uses docker image pingcap/tidb:v7.1.6
  * RAM:540590804992
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-124-generic
  * node:cl-worker24
  * disk:131929
  * cpu_list:0-95
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * sut 0
    * RAM:540590804992
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-124-generic
    * node:cl-worker24
    * disk:131930
    * cpu_list:0-95
  * sut 1
    * RAM:1077382598656
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-1058-nvidia
    * node:cl-worker28
    * disk:582821
    * cpu_list:0-255
  * sut 2
    * RAM:1081742745600
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-117-generic
    * node:cl-worker29
    * disk:940285
    * cpu_list:0-127
  * pd 0
    * RAM:1077382598656
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-1058-nvidia
    * node:cl-worker28
    * disk:584532
    * cpu_list:0-255
  * pd 1
    * RAM:540590841856
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-117-generic
    * node:cl-worker25
    * disk:163405
    * cpu_list:0-95
  * pd 2
    * RAM:2164173213696
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:1090603
    * cpu_list:0-223
  * tikv 0
    * RAM:1077382598656
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-1058-nvidia
    * node:cl-worker28
    * disk:584050
    * cpu_list:0-255
  * tikv 1
    * RAM:2164173213696
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:1091017
    * cpu_list:0-223
  * tikv 2
    * RAM:1081853972480
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-134-generic
    * node:cl-worker37
    * disk:539092
    * cpu_list:0-127
  * eval_parameters
    * code:1783870690
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-tidb-1-1783870690-8f5675c8-2n8nf: 0
* bexhoma-sut-tidb-1-1783870690-8f5675c8-bkbsl: 0
* bexhoma-sut-tidb-1-1783870690-8f5675c8-fkrdb: 0
* bexhoma-pd-tidb-ycsb-1-0: 0
* bexhoma-pd-tidb-ycsb-1-1: 0
* bexhoma-pd-tidb-ycsb-1-2: 0
* bexhoma-tikv-tidb-ycsb-1-0: 0
* bexhoma-tikv-tidb-ycsb-1-1: 0
* bexhoma-tikv-tidb-ycsb-1-2: 0

### Workflow

#### Actual

* DBMS TiDB-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS TiDB-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection     |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| TiDB-1-1-0-1-1 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1201.87 |               104005.00 |            125000.00 |                             20943.00 | 1.00 |               34.61 |
| TiDB-1-1-0-1-2 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1185.96 |               105400.00 |            125000.00 |                             20511.00 | 1.00 |               34.16 |
| TiDB-1-1-0-1-3 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1133.36 |               110292.00 |            125000.00 |                             21759.00 | 1.00 |               32.64 |
| TiDB-1-1-0-1-4 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1130.41 |               110579.00 |            125000.00 |                             21903.00 | 1.00 |               32.56 |
| TiDB-1-1-0-1-5 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1197.34 |               104398.00 |            125000.00 |                             20991.00 | 1.00 |               34.48 |
| TiDB-1-1-0-1-6 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1200.51 |               104122.00 |            125000.00 |                             20879.00 | 1.00 |               34.57 |
| TiDB-1-1-0-1-7 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1176.07 |               106286.00 |            125000.00 |                             20831.00 | 1.00 |               33.87 |
| TiDB-1-1-0-1-8 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1174.41 |               106436.00 |            125000.00 |                             21183.00 | 1.00 |               33.82 |

#### Per Run

| DBMS     |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| TiDB-1-1 |             1.00 |     64.00 | 16384.00 |        8.00 |         0.00 | 1.00 |               32.56 |                         9399.93 |               110579.00 |           1000000.00 |                             21125.00 |

### Execution

#### Per Connection

| DBMS           | phase      | job          | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------|:-----------|:-------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| TiDB-1-1-1-1-1 | TiDB-1-1-1 | TiDB-1-1-1-1 | TiDB-1          |                1 |        1 |               1 |       1 |        64 |    16384 |           1 |            0 |                        10834.35 |                92299.00 |             499501 |                            3455.00 |               500499 |                            158207.00 |

#### Per Phase

| DBMS       | phase      |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------|:-----------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| TiDB-1-1-1 | TiDB-1-1-1 |                1 |        64 |    16384 |               1 |           1 |            0 |                        10834.35 |                92299.00 |             499501 |                            3455.00 |               500499 |                            158207.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |       960.01 |      9.91 |           3.09 |                  3.42 |

### Loading phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |       134.18 |      1.17 |           0.26 |                  0.26 |

### Loading phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |      1129.02 |     11.55 |           6.86 |                 17.00 |

### Loading phase: component loader

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |       127.87 |      1.89 |           0.45 |                  0.46 |

### Execution phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |       739.90 |      9.81 |           1.13 |                  1.47 |

### Execution phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |        70.86 |      1.17 |           0.26 |                  0.26 |

### Execution phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |      1200.20 |     16.34 |           8.36 |                 22.16 |

### Execution phase: component benchmarker

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |       183.76 |      2.21 |           0.15 |                  0.15 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component pd contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component tikv contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component pd contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component tikv contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>

To see the summary again you can simply call `bexhoma summary -e 1761748555` with the experiment code.

### Detailed Evaluation

Results are transformed into pandas DataFrames and can be inspected in detail.
See for example
* [Jupyter Notebooks](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/evaluator_dbmsbenchmarker/notebooks/)

You can connect to an evaluation server locally by `bexhoma jupyter`.
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
TiDB has 3 tidb-server pods (`-xnsr`), 3 TiKV nodes (`-nw`), and 3 PD nodes (`-xnpd`) - see [Scaling TiDB Components](#scaling-tidb-components).

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
  -xnpd 3 \
  -nwr 3 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  run &>$LOG_DIR/docs_benchbase_tidb_1.log
```

### Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_tidb_1_summary.md" target="_blank" rel="noopener">docs_benchbase_tidb_1.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1479s 
* Code: 1783871513
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.10.5.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['TiDB'].
  * Import is handled by 1 processes (pods).
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* TiDB-1-1-1-1 uses docker image pingcap/tidb:v7.1.6
  * RAM:1077382598656
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-1058-nvidia
  * node:cl-worker28
  * disk:573659
  * cpu_list:0-255
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * sut 0
    * RAM:1077382598656
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-1058-nvidia
    * node:cl-worker28
    * disk:573099
    * cpu_list:0-255
  * sut 1
    * RAM:1081742745600
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-117-generic
    * node:cl-worker29
    * disk:965992
    * cpu_list:0-127
  * sut 2
    * RAM:540597907456
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-124-generic
    * node:cl-worker39
    * disk:320533
    * cpu_list:0-255
  * pd 0
    * RAM:1077382598656
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-1058-nvidia
    * node:cl-worker28
    * disk:573729
    * cpu_list:0-255
  * pd 1
    * RAM:540590841856
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-117-generic
    * node:cl-worker25
    * disk:160447
    * cpu_list:0-95
  * pd 2
    * RAM:2164173213696
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:1079035
    * cpu_list:0-223
  * tikv 0
    * RAM:540590804992
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-124-generic
    * node:cl-worker24
    * disk:141570
    * cpu_list:0-95
  * tikv 1
    * RAM:1077381287936
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1394849
    * cpu_list:0-255
  * tikv 2
    * RAM:1081742745600
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-117-generic
    * node:cl-worker29
    * disk:965992
    * cpu_list:0-127
  * eval_parameters
    * code:1783871513
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* TiDB-1-1-2-1 uses docker image pingcap/tidb:v7.1.6
  * RAM:1077382598656
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-1058-nvidia
  * node:cl-worker28
  * disk:572637
  * cpu_list:0-255
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * sut 0
    * RAM:1077382598656
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-1058-nvidia
    * node:cl-worker28
    * disk:574545
    * cpu_list:0-255
  * sut 1
    * RAM:1081742745600
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-117-generic
    * node:cl-worker29
    * disk:964096
    * cpu_list:0-127
  * sut 2
    * RAM:540597907456
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-124-generic
    * node:cl-worker39
    * disk:320529
    * cpu_list:0-255
  * pd 0
    * RAM:1077382598656
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-1058-nvidia
    * node:cl-worker28
    * disk:573157
    * cpu_list:0-255
  * pd 1
    * RAM:540590841856
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-117-generic
    * node:cl-worker25
    * disk:160448
    * cpu_list:0-95
  * pd 2
    * RAM:2164173213696
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:1079556
    * cpu_list:0-223
  * tikv 0
    * RAM:540590804992
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-124-generic
    * node:cl-worker24
    * disk:139675
    * cpu_list:0-95
  * tikv 1
    * RAM:1077381287936
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1392808
    * cpu_list:0-255
  * tikv 2
    * RAM:1081742745600
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-117-generic
    * node:cl-worker29
    * disk:964096
    * cpu_list:0-127
  * eval_parameters
    * code:1783871513
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-tidb-1-1783871513-6749c58f7-dfzcl: 0
* bexhoma-sut-tidb-1-1783871513-6749c58f7-hzh6d: 0
* bexhoma-sut-tidb-1-1783871513-6749c58f7-vgz8n: 0
* bexhoma-pd-tidb-benchbase-tpcc-16-0: 0
* bexhoma-pd-tidb-benchbase-tpcc-16-1: 0
* bexhoma-pd-tidb-benchbase-tpcc-16-2: 0
* bexhoma-tikv-tidb-benchbase-tpcc-16-0: 0
* bexhoma-tikv-tidb-benchbase-tpcc-16-1: 0
* bexhoma-tikv-tidb-benchbase-tpcc-16-2: 0

### Workflow

#### Actual

* DBMS TiDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS TiDB-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS TiDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS TiDB-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

|          |   experiment_run |    SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------|-----------------:|------:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| TiDB-1-1 |                1 | 16.00 |      593.00 |           0.00 |            0.00 |        256.00 |          337.00 |              1 |           1 |             | None           |             0 | False         |               97.13 |

### Execution

#### Per Connection

| DBMS           | phase      | job          |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------|:-----------|:-------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| TiDB-1-1-1-1-1 | TiDB-1-1-1 | TiDB-1-1-1-1 |                1 |          16 |    16384 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                         299.26 |                      297.90 |         0.00 |                                                     149981.00 |                                              52661.00 |
| TiDB-1-1-2-1-1 | TiDB-1-1-2 | TiDB-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       1 |          -1 | 300.00 |            0 |                         142.38 |                      140.96 |         0.00 |                                                     142632.00 |                                              55498.00 |
| TiDB-1-1-2-1-2 | TiDB-1-1-2 | TiDB-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       2 |          -1 | 300.00 |            0 |                         144.33 |                      142.89 |         0.00 |                                                     146941.00 |                                              55407.00 |

#### Per Phase

| DBMS       | phase      |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------|:-----------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| TiDB-1-1-1 | TiDB-1-1-1 |                1 |          16 |    16384 |               1 |           1 |          -1 | 300.00 |            0 |                         299.26 |                      297.90 |         0.00 |                                                     149981.00 |                                              52661.00 |
| TiDB-1-1-2 | TiDB-1-1-2 |                1 |          16 |    16384 |               1 |           2 |          -1 | 300.00 |            0 |                         286.71 |                      283.85 |         0.00 |                                                     146941.00 |                                              55452.50 |

### Monitoring

### Loading phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |      1654.56 |      9.36 |           1.87 |                  2.20 |
| TiDB-1-1-2-1 |      1654.56 |      9.36 |           1.87 |                  2.20 |

### Loading phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |        77.99 |      0.32 |           0.27 |                  0.27 |
| TiDB-1-1-2-1 |        77.99 |      0.32 |           0.27 |                  0.27 |

### Loading phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |      2794.91 |     15.83 |          11.48 |                 31.02 |
| TiDB-1-1-2-1 |      2794.91 |     15.83 |          11.48 |                 31.02 |

### Loading phase: component loader

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |       129.14 |      1.11 |           1.53 |                  1.53 |
| TiDB-1-1-2-1 |       129.14 |      1.11 |           1.53 |                  1.53 |

### Execution phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |      2530.67 |     10.90 |           1.66 |                  1.99 |
| TiDB-1-1-2-1 |      2384.46 |      9.44 |           2.34 |                  2.67 |

### Execution phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |       304.61 |      1.31 |           0.27 |                  0.27 |
| TiDB-1-1-2-1 |       311.85 |      1.11 |           0.27 |                  0.27 |

### Execution phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |      3255.15 |     14.76 |          14.06 |                 34.69 |
| TiDB-1-1-2-1 |      3257.07 |     13.21 |          16.57 |                 34.91 |

### Execution phase: component benchmarker

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |       205.50 |      0.90 |           0.35 |                  0.35 |
| TiDB-1-1-2-1 |       205.50 |      1.23 |           0.63 |                  0.63 |

### Tests
* TEST passed: No SUT container restarts
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

</details>


