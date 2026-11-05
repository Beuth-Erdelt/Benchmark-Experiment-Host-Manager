# Example: Benchmark MariaDB

This example shows how to benchmark MariaDB with TPC-H, TPC-DS, Benchbase's TPC-C, HammerDB's TPC-C and YCSB.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

[MariaDB](https://mariadb.org/) is a relational DBMS, a fork of MySQL. Bexhoma runs it on a single node.
It uses a dedicated `bexhoma` database user rather than `root`.
For the columnar engine of MariaDB see [MariaDB ColumnStore](Example-MariaDBCS.md).

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. [MariaDB](https://mariadb.org/)
1. [MariaDB in Docker](https://hub.docker.com/_/mariadb)
1. [TPC-H](https://www.tpc.org/tpch/)
1. [TPC-DS](https://www.tpc.org/tpcds/)
1. [Benchbase Repository](https://github.com/cmu-db/benchbase/wiki/TPC-C)
1. [HammerDB](https://www.hammerdb.com/)
1. [YCSB Repository](https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload)
1. [Benchmarking cloud serving systems with YCSB](https://dl.acm.org/doi/10.1145/1807128.1807152)
1. [Orchestrating DBMS Benchmarking in the Cloud with Kubernetes](https://doi.org/10.1007/978-3-030-94437-7_6)
1. [A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools](https://doi.org/10.1007/978-3-031-68031-1_9)
1. Test script of this page: [test-docs-mariadb.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-mariadb.sh), [test-docs-mariadb.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-mariadb.ps1)


## Perform TPC-H Benchmark

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

For performing the experiment we can run the [tpch file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpch.py).

Example:
```bash
bexhoma tpch \
  -dbms MariaDB \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_mariadb.log
```

This
* starts a clean instance of MariaDB (`-dbms`)
  * data directory inside a Docker container
* creates the TPC-H schema
* starts 8 loader pods (`-nlp`) with 8 threads each (`-nlt`)
  * with a data generator (init container) each, which generates a share of TPC-H data of SF=1 (`-sf`)
  * and a loading container each, which loads the data into the DBMS
* creates indexes (`-xii`), constraints (`-xic`) and statistics (`-xis`)
* runs 1 stream of the 22 TPC-H queries (`-ne`) with a timeout of 1200 s per query (`-t`), measuring the data transfer volume per query (`-xdt`)
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

```

The code of the experiment is its unique identifier.
You can find the number also in the output of the benchmark script.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e <code>` (removes everything that is related to experiment `<code>`).

### Evaluate Results

At the end of a benchmark you will see a summary like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_mariadb_summary.md" target="_blank" rel="noopener">docs_tpch_mariadb.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 708s 
* Code: 1782332846
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MariaDB-1-1-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:265547
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782332846

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |    1 |      367.00 |           1.00 |           25.00 |         36.00 |          302.00 |              8 |           0 |             | None           |             0 | False         |                9.81 |

### Execution

#### Per Connection

|                   | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MariaDB-1-1-1-1-1 | MariaDB-1       | MariaDB-1-1-1 | MariaDB-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |        107 |            1.15 |             3301.61 |            740.19 |          -1 | MariaDB-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MariaDB-1-1-1 | MariaDB-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |        107 |            1.15 |             3301.61 |            740.19 |          -1 |

### Latency of Timer Execution [ms]
| Queries                                             |   MariaDB-1-1-1-1-1 |
|:----------------------------------------------------|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |             8140.58 |
| Minimum Cost Supplier Query (TPC-H Q2)              |              542.66 |
| Shipping Priority (TPC-H Q3)                        |             1629.37 |
| Order Priority Checking Query (TPC-H Q4)            |              372.68 |
| Local Supplier Volume (TPC-H Q5)                    |             1190.27 |
| Forecasting Revenue Change (TPC-H Q6)               |             1298.28 |
| Volume Shipping Query (TPC-H Q7)                    |             1265.87 |
| National Market Share (TPC-H Q8)                    |             2202.44 |
| Product Type Profit Measure (TPC-H Q9)              |             2062.75 |
| Returned Item Reporting Query (TPC-H Q10)           |              896.30 |
| Important Stock Identification (TPC-H Q11)          |              150.67 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             3196.19 |
| Customer Distribution (TPC-H Q13)                   |             3191.68 |
| Promotion Effect Query (TPC-H Q14)                  |            12756.89 |
| Top Supplier Query (TPC-H Q15)                      |             2071.70 |
| Parts/Supplier Relationship (TPC-H Q16)             |              238.70 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               62.08 |
| Large Volume Customer (TPC-H Q18)                   |             3098.08 |
| Discounted Revenue (TPC-H Q19)                      |               97.96 |
| Potential Part Promotion (TPC-H Q20)                |              227.04 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            57943.45 |
| Global Sales Opportunity Query (TPC-H Q22)          |              130.66 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```

</details>

To see the summary again you can simply call `bexhoma summary -e <code>` with the experiment code.

Results are transformed into pandas DataFrames and can be inspected in detail.
See for example the [Jupyter notebooks](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/notebooks/), in particular [Collector-TPC-H.ipynb](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/notebooks/Collector-TPC-H.ipynb).

You can connect to an evaluation server locally by `bexhoma jupyter`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888


## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).
Metrics are sampled every few seconds, so the benchmarking phase should take at least a minute.

```bash
bexhoma tpch \
  -dbms MariaDB \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_mariadb_monitoring.log
```

### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_mariadb_monitoring_summary.md" target="_blank" rel="noopener">docs_tpch_mariadb_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 725s 
* Code: 1782333577
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MariaDB-1-1-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:254316
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782333577

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |    1 |      361.00 |           1.00 |           18.00 |         47.00 |          292.00 |              8 |           0 |             | None           |             0 | False         |                9.97 |

### Execution

#### Per Connection

|                   | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MariaDB-1-1-1-1-1 | MariaDB-1       | MariaDB-1-1-1 | MariaDB-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |        107 |            1.12 |             3444.13 |            740.19 |          -1 | MariaDB-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MariaDB-1-1-1 | MariaDB-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |        107 |            1.12 |             3444.13 |            740.19 |          -1 |

### Latency of Timer Execution [ms]
| Queries                                             |   MariaDB-1-1-1-1-1 |
|:----------------------------------------------------|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |             7826.42 |
| Minimum Cost Supplier Query (TPC-H Q2)              |              508.07 |
| Shipping Priority (TPC-H Q3)                        |             1652.33 |
| Order Priority Checking Query (TPC-H Q4)            |              400.18 |
| Local Supplier Volume (TPC-H Q5)                    |             1065.60 |
| Forecasting Revenue Change (TPC-H Q6)               |              897.29 |
| Volume Shipping Query (TPC-H Q7)                    |             1131.93 |
| National Market Share (TPC-H Q8)                    |             2075.71 |
| Product Type Profit Measure (TPC-H Q9)              |             2037.49 |
| Returned Item Reporting Query (TPC-H Q10)           |              904.34 |
| Important Stock Identification (TPC-H Q11)          |              139.67 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             3119.38 |
| Customer Distribution (TPC-H Q13)                   |             3115.70 |
| Promotion Effect Query (TPC-H Q14)                  |            12671.14 |
| Top Supplier Query (TPC-H Q15)                      |             1997.16 |
| Parts/Supplier Relationship (TPC-H Q16)             |              210.77 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               59.44 |
| Large Volume Customer (TPC-H Q18)                   |             3205.99 |
| Discounted Revenue (TPC-H Q19)                      |              106.26 |
| Potential Part Promotion (TPC-H Q20)                |              222.20 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            58675.88 |
| Global Sales Opportunity Query (TPC-H Q22)          |              127.26 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |       519.88 |      6.76 |           5.68 |                  5.78 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |         2.75 |      0.05 |           0.00 |                  0.11 |

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |        83.67 |      1.00 |           5.91 |                  6.02 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |        14.63 |      0.46 |           0.30 |                  0.31 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```

</details>



## Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.
With repetitions (`-nc`), `-rsr` removes an existing volume only before the first repetition and later repetitions reuse it without loading; `-rsrp` removes it before every repetition. See [Concepts](Concepts.html).

This is a throughput test: one round with 1 stream and one with 2 parallel streams (`-ne 1,2`), repeated (`-nc 2`), so the second repetition runs on the loaded volume:

```bash
bexhoma tpch \
  -dbms MariaDB \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 2 \
  -ne 1,2 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rsr \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_mariadb_storage.log
```

### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_mariadb_storage_summary.md" target="_blank" rel="noopener">docs_tpch_mariadb_storage.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 2627s 
* Code: 1782334385
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 50Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* MariaDB-1-1-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220467
  * volume_size:50G
  * volume_used:2.1G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782334385
* MariaDB-1-1-2-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220467
  * volume_size:50G
  * volume_used:2.1G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782334385
* MariaDB-1-1-2-1-2 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220467
  * volume_size:50G
  * volume_used:2.1G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782334385
* MariaDB-1-2-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220467
  * volume_size:50G
  * volume_used:2.1G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782334385
* MariaDB-1-2-2-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:253328
  * volume_size:50G
  * volume_used:2.1G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782334385
* MariaDB-1-2-2-1-2 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:253328
  * volume_size:50G
  * volume_used:2.1G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782334385

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 2: tpch (2 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 2: tpch (2 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |    1 |     1725.00 |           3.00 |           33.00 |        510.00 |         1172.00 |              8 |           0 |             | None           |             0 | False         |                2.09 |
| MariaDB-1-2 |                2 |    1 |     1725.00 |           3.00 |           33.00 |        510.00 |         1172.00 |              8 |           0 |             | None           |             0 | False         |                2.09 |

### Execution

#### Per Connection

|                   | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MariaDB-1-1-1-1-1 | MariaDB-1       | MariaDB-1-1-1 | MariaDB-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |        103 |            1.08 |             3525.92 |            768.93 |          -1 | MariaDB-1-1-1-1-1 |
| MariaDB-1-1-2-1-1 | MariaDB-1       | MariaDB-1-1-2 | MariaDB-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               22 |        121 |            1.17 |             3264.87 |            654.55 |          -1 | MariaDB-1-1-2-1-1 |
| MariaDB-1-1-2-1-2 | MariaDB-1       | MariaDB-1-1-2 | MariaDB-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               22 |        119 |            1.18 |             3237.13 |            665.55 |          -1 | MariaDB-1-1-2-1-2 |
| MariaDB-1-2-1-1-1 | MariaDB-1       | MariaDB-1-2-1 | MariaDB-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |        107 |            1.16 |             3324.21 |            740.19 |          -1 | MariaDB-1-2-1-1-1 |
| MariaDB-1-2-2-1-1 | MariaDB-1       | MariaDB-1-2-2 | MariaDB-1-2-2-1 |                2 |        2 |               1 |           1 | 1.00 |               22 |        135 |            1.37 |             2770.37 |            586.67 |          -1 | MariaDB-1-2-2-1-1 |
| MariaDB-1-2-2-1-2 | MariaDB-1       | MariaDB-1-2-2 | MariaDB-1-2-2-1 |                2 |        2 |               1 |           1 | 1.00 |               22 |        134 |            1.43 |             2674.87 |            591.04 |          -1 | MariaDB-1-2-2-1-2 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MariaDB-1-1-1 | MariaDB-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |        103 |            1.08 |             3525.92 |            768.93 |          -1 |
| MariaDB-1-1-2 | MariaDB-1-1-2 |                1 |        2 |               1 |           2 | 1.00 |               44 |        121 |            1.18 |             3250.97 |           1309.09 |          -1 |
| MariaDB-1-2-1 | MariaDB-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |        107 |            1.16 |             3324.21 |            740.19 |          -1 |
| MariaDB-1-2-2 | MariaDB-1-2-2 |                2 |        2 |               1 |           2 | 1.00 |               44 |        135 |            1.40 |             2722.20 |           1173.33 |          -1 |

### Latency of Timer Execution [ms]
| Queries                                             |   MariaDB-1-1-1-1-1 |   MariaDB-1-1-2-1-1 |   MariaDB-1-1-2-1-2 |   MariaDB-1-2-1-1-1 |   MariaDB-1-2-2-1-1 |   MariaDB-1-2-2-1-2 |
|:----------------------------------------------------|--------------------:|--------------------:|--------------------:|--------------------:|--------------------:|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |             7835.73 |             7460.30 |             7576.32 |             7445.58 |             7798.95 |             7445.41 |
| Minimum Cost Supplier Query (TPC-H Q2)              |              445.24 |              413.40 |              452.21 |              562.07 |              698.00 |              629.33 |
| Shipping Priority (TPC-H Q3)                        |             1551.76 |             1716.63 |             1743.74 |             1536.82 |             2642.48 |             2428.26 |
| Order Priority Checking Query (TPC-H Q4)            |              339.95 |              350.44 |              357.45 |              351.30 |              398.86 |              386.22 |
| Local Supplier Volume (TPC-H Q5)                    |              966.73 |             1102.55 |             1067.68 |              965.93 |             1496.52 |             1452.50 |
| Forecasting Revenue Change (TPC-H Q6)               |              826.30 |              813.59 |              799.97 |              806.65 |              802.49 |              802.31 |
| Volume Shipping Query (TPC-H Q7)                    |             1078.50 |             1090.08 |             1134.41 |             1098.53 |             1394.57 |             1357.76 |
| National Market Share (TPC-H Q8)                    |             1828.43 |             2211.54 |             2201.69 |             1924.68 |             3119.33 |             3003.46 |
| Product Type Profit Measure (TPC-H Q9)              |             3999.56 |             4395.40 |             4387.79 |             4681.89 |             5739.51 |             5963.52 |
| Returned Item Reporting Query (TPC-H Q10)           |              927.14 |              925.49 |              928.07 |              925.57 |             1174.82 |             1175.41 |
| Important Stock Identification (TPC-H Q11)          |              134.54 |              147.96 |              141.73 |              146.11 |              217.12 |              218.17 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             3029.25 |             3415.46 |             3422.66 |             3044.02 |             4549.91 |             4266.76 |
| Customer Distribution (TPC-H Q13)                   |             2995.40 |             3887.61 |             3889.33 |             3221.74 |             4031.94 |             3630.11 |
| Promotion Effect Query (TPC-H Q14)                  |            12074.97 |            14588.29 |            14297.04 |            14396.01 |            18364.82 |            17723.74 |
| Top Supplier Query (TPC-H Q15)                      |             1780.15 |             1809.90 |             1816.64 |             1751.99 |             1732.48 |             2195.46 |
| Parts/Supplier Relationship (TPC-H Q16)             |              220.32 |              221.36 |              206.89 |              213.05 |              234.73 |              226.32 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               69.54 |               61.56 |               65.50 |               75.99 |               62.19 |               61.79 |
| Large Volume Customer (TPC-H Q18)                   |             2930.59 |             3922.40 |             3912.35 |             2979.81 |             3533.70 |             3592.21 |
| Discounted Revenue (TPC-H Q19)                      |               95.73 |              104.56 |              105.85 |              103.57 |               96.93 |              161.23 |
| Potential Part Promotion (TPC-H Q20)                |              206.68 |              235.15 |              220.62 |              242.60 |              218.74 |              385.86 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            55401.87 |            66972.36 |            65984.58 |            56422.19 |            71639.16 |            71949.04 |
| Global Sales Opportunity Query (TPC-H Q22)          |              113.79 |              115.17 |              139.42 |              144.84 |              158.60 |              159.10 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |      1541.04 |      2.44 |           5.93 |                  6.04 |
| MariaDB-1-1-2-1 |      1541.04 |      2.44 |           5.93 |                  6.04 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| MariaDB-1-1-2-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |         4.79 |      0.05 |           0.00 |                  0.13 |
| MariaDB-1-1-2-1 |         4.79 |      0.05 |           0.00 |                  0.13 |

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |        69.86 |      0.99 |           5.99 |                  6.09 |
| MariaDB-1-1-2-1 |       205.20 |      2.00 |           6.00 |                  6.10 |
| MariaDB-1-2-1-1 |        92.51 |      1.00 |           3.72 |                  3.75 |
| MariaDB-1-2-2-1 |       224.20 |      2.00 |           3.73 |                  3.76 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |        15.09 |      0.17 |           0.30 |                  0.30 |
| MariaDB-1-1-2-1 |        29.66 |      0.21 |           0.33 |                  0.34 |
| MariaDB-1-2-1-1 |        16.76 |      0.46 |           0.34 |                  0.35 |
| MariaDB-1-2-2-1 |        30.93 |      0.24 |           0.34 |                  0.35 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```

</details>

### RAM Disk

This loads TPC-H data into a database that is stored on a RAM disk (`-rst ramdisk`).
Make sure you have enough RAM.

```bash
bexhoma tpch \
  -dbms MariaDB \
  -sf 10 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ma \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rst ramdisk \
  -rss 150Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_mariadb_ramdisk.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_mariadb_ramdisk_summary.md" target="_blank" rel="noopener">docs_tpch_mariadb_ramdisk.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=10
* Type: tpch
* Duration: 3579s 
* Code: 1782340884
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type ramdisk and size 100Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MariaDB-1-1-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:225014
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782340884

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |   10 |     2433.00 |           2.00 |           25.00 |        384.00 |         2018.00 |              8 |           0 |             | None           |             0 | False         |               14.80 |

### Execution

#### Per Connection

|                   | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MariaDB-1-1-1-1-1 | MariaDB-1       | MariaDB-1-1-1 | MariaDB-1-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |       1148 |           12.78 |             2877.44 |            689.90 |          -1 | MariaDB-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MariaDB-1-1-1 | MariaDB-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |       1148 |           12.78 |             2877.44 |            689.90 |          -1 |

### Latency of Timer Execution [ms]
| Queries                                             |   MariaDB-1-1-1-1-1 |
|:----------------------------------------------------|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |            70985.56 |
| Minimum Cost Supplier Query (TPC-H Q2)              |             5073.32 |
| Shipping Priority (TPC-H Q3)                        |            20450.51 |
| Order Priority Checking Query (TPC-H Q4)            |            21473.07 |
| Local Supplier Volume (TPC-H Q5)                    |            11632.52 |
| Forecasting Revenue Change (TPC-H Q6)               |             8384.30 |
| Volume Shipping Query (TPC-H Q7)                    |            12469.46 |
| National Market Share (TPC-H Q8)                    |            25097.32 |
| Product Type Profit Measure (TPC-H Q9)              |            23869.39 |
| Returned Item Reporting Query (TPC-H Q10)           |            10857.62 |
| Important Stock Identification (TPC-H Q11)          |             1819.67 |
| Shipping Modes and Order Priority (TPC-H Q12)       |            32846.25 |
| Customer Distribution (TPC-H Q13)                   |            42904.62 |
| Promotion Effect Query (TPC-H Q14)                  |           162749.93 |
| Top Supplier Query (TPC-H Q15)                      |            18011.23 |
| Parts/Supplier Relationship (TPC-H Q16)             |             2189.07 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |              623.10 |
| Large Volume Customer (TPC-H Q18)                   |            39322.71 |
| Discounted Revenue (TPC-H Q19)                      |             1202.30 |
| Potential Part Promotion (TPC-H Q20)                |             3050.72 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |           624716.37 |
| Global Sales Opportunity Query (TPC-H Q22)          |             1195.83 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |      7280.38 |     11.95 |          74.05 |                 74.05 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |         0.02 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |        29.18 |      0.22 |           0.01 |                  1.31 |

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |      1143.73 |      1.07 |          59.70 |                 59.70 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |        18.50 |      0.09 |           0.34 |                  0.34 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component data generator contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```

</details>


## Refresh Stream

`-xrs N` runs the TPC-H refresh functions RF1 (insert new orders) and RF2 (delete old orders) as an additional job next to the query streams, see [TPC-H](Example-TPC-H.md#refresh-stream).
For MariaDB, the loader image applies RF1 with `LOAD DATA LOCAL INFILE` and RF2 with a temporary table and a `DELETE` joined to it.
Here, 3 query streams run in parallel with a refresh stream of 3 RF1+RF2 pairs.

```bash
bexhoma tpch \
  -dbms MariaDB \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii \
  -xic \
  -xis \
  -ne 3 \
  -xrs 3 \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_mariadb_refresh.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_mariadb_refresh_summary.md" target="_blank" rel="noopener">docs_tpch_mariadb_refresh.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 595s 
* Code: 1793810040
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * A TPC-H refresh stream (RF1+RF2) runs in parallel, with 3 pair(s) applied per round.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [3] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* mariadb-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:887021
  * datadisk:1954
  * volume_size:1.8T
  * volume_used:867G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793810040
* mariadb-1-1-1-1-2 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:887021
  * datadisk:1954
  * volume_size:1.8T
  * volume_used:867G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793810040
* mariadb-1-1-1-1-3 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:887021
  * datadisk:1954
  * volume_size:1.8T
  * volume_used:867G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793810040

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1793810040-5995bbdd88-cq8jk: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |    1 |       87.00 |           2.00 |           39.00 |         16.00 |           22.00 |              8 |           0 |             | None           |             0 | False         |               41.38 | False               |

### Benchmarking

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| mariadb-1-1-1-1-1 | MariaDB-1       | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |        130 |            1.12 |             3205.52 |            609.23 |          -1 | mariadb-1-1-1-1-1 |
| mariadb-1-1-1-1-2 | MariaDB-1       | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |        132 |            1.20 |             3008.14 |            600.00 |          -1 | mariadb-1-1-1-1-2 |
| mariadb-1-1-1-1-3 | MariaDB-1       | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |        125 |            1.07 |             3357.13 |            633.60 |          -1 | mariadb-1-1-1-1-3 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           3 | 1.00 |               66 |                  66 |        132 |            1.13 |             3187.04 |           1800.00 |          -1 |

#### Query Completion per Phase

| phase         |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:--------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| mariadb-1-1-1 |      3 | 3/3                                 | 3/3                                      | 3/3                            | 3/3                                        | 3/3                                | 3/3                                     | 3/3                                | 3/3                                | 3/3                                      | 3/3                                         | 3/3                                          | 3/3                                             | 3/3                                 | 3/3                                  | 3/3                              | 3/3                                       | 3/3                                        | 3/3                                 | 3/3                              | 3/3                                    | 3/3                                                   | 3/3                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### tpch_refresh

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count | benchmark_begin     | benchmark_end       |   benchmark_duration |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|:--------------------|:--------------------|---------------------:|
| mariadb-1-1-1-2-1 | mariadb-1-1-1 | mariadb-1-1-1-2 |                1 |        1 |               2 |           1 | 2026-11-04 17:41:15 | 2026-11-04 17:41:19 |                    4 |

### Latency of Timer Execution [ms]
| Queries                                             |   mariadb-1-1-1-1-1 |   mariadb-1-1-1-1-2 |   mariadb-1-1-1-1-3 |
|:----------------------------------------------------|--------------------:|--------------------:|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |             7738.74 |             6998.91 |             6196.46 |
| Minimum Cost Supplier Query (TPC-H Q2)              |              401.36 |              416.59 |              398.19 |
| Shipping Priority (TPC-H Q3)                        |             1921.11 |             2106.80 |             1884.84 |
| Order Priority Checking Query (TPC-H Q4)            |              400.02 |              343.77 |              424.39 |
| Local Supplier Volume (TPC-H Q5)                    |             1002.09 |             1211.78 |             1434.98 |
| Forecasting Revenue Change (TPC-H Q6)               |              777.23 |              898.41 |              906.82 |
| Volume Shipping Query (TPC-H Q7)                    |             1201.98 |             1176.72 |             1130.06 |
| National Market Share (TPC-H Q8)                    |             2217.71 |             2597.57 |             2149.81 |
| Product Type Profit Measure (TPC-H Q9)              |             2429.44 |             2593.51 |             2132.44 |
| Returned Item Reporting Query (TPC-H Q10)           |              949.04 |              988.05 |              918.03 |
| Important Stock Identification (TPC-H Q11)          |              121.93 |              334.75 |              152.03 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             4268.71 |             4113.92 |             3954.57 |
| Customer Distribution (TPC-H Q13)                   |             4699.52 |             4854.75 |             3721.23 |
| Promotion Effect Query (TPC-H Q14)                  |            15167.74 |            15342.18 |            14817.56 |
| Top Supplier Query (TPC-H Q15)                      |             2068.71 |             2037.01 |             1978.85 |
| Parts/Supplier Relationship (TPC-H Q16)             |              310.02 |              284.97 |              184.14 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               47.32 |               50.31 |               52.12 |
| Large Volume Customer (TPC-H Q18)                   |             4022.12 |             4027.78 |             3179.30 |
| Discounted Revenue (TPC-H Q19)                      |              130.72 |              129.38 |               85.58 |
| Potential Part Promotion (TPC-H Q20)                |              249.13 |              249.00 |              219.40 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            77485.35 |            79225.59 |            76960.38 |
| Global Sales Opportunity Query (TPC-H Q22)          |               98.42 |               93.81 |              131.58 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
```

</details>

The section `### tpch_refresh` shows the refresh job: it applied the 3 pairs in ---------------------: s, while the query streams ran.


## Technical Details

### Configuration of Bexhoma

In `cluster.config` there is a section:

```python
'MariaDB': {
    'loadData': 'mariadb --user=bexhoma --password=password < {scriptname}',
    'template': {
        'version': 'v10.4.6',
        'alias': 'General-A',
        'docker_alias': 'GP-A',
        'dialect': 'MySQL',
        'JDBC': {
            'driver': "org.mariadb.jdbc.Driver",
            'auth': ["bexhoma", "password"],
            'url': 'jdbc:mariadb://{serverip}:9091/{dbname}?rewriteBatchedStatements=true',
            'jar': 'mariadb-java-client-3.1.0.jar',
            'database': 'mariadb',  # placeholder — must be overwritten per experiment
        },
        'init_SQL': "SET optimizer_switch = 'mrr=on,mrr_cost_based=off'",
    },
    'logfile': '/usr/local/data/logfile',
    'datadir': '/var/lib/mysql/',
    'priceperhourdollar': 0.0,
},
```

### Deployment

* [deploymenttemplate-MariaDB.yml](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-MariaDB.yml): one SUT pod.
* The default deployment sets the I/O threads, `innodb-log-buffer-size=1G`, temporary table sizes and `innodb-buffer-pool-size=8G`.
* As for MySQL, the 8G pool fits the default pod size (`-rr 16Gi`); give larger pods a larger pool with `--set ...container[dbms].innodb_buffer_pool_size=32G`.
* The `init_SQL` statement is executed after each connection is established and enables multi-range read optimisation.

### Schema and Scripts

DDL scripts per benchmark:
- [TPC-H](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch/MariaDB)
- [TPC-DS](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpcds/MariaDB)
- [TPC-C](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpcc/MariaDB)
- [YCSB](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/MariaDB)



DDL parameters (`-xddl`, see [DDL parameters](DBMS.md#ddl-parameters--xddl)):

| Key | Benchmarks | Values | Default | Effect |
|

### Load Durability

With `-xld`, the durability scripts (`.sh`, run as root) run before and after the load:

* `durable`: `innodb_flush_log_at_trx_commit=1`, doublewrite on
* `relaxed` (default): `innodb_flush_log_at_trx_commit=2`
* `unsafe`: also doublewrite off

The restore returns to the startup values, which the scripts save in `bexhoma.saved_settings`.

See [Load durability](DBMS.md#load-durability--xld) and [Test: Load Durability](Test-Durability.md), with results for [TPC-H relaxed](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_tpch_mariadb_relaxed_summary.md).

### Reset Scripts

With `-ar`, the reset runs before each benchmarking round:

1. Statistics: `ANALYZE TABLE` (`reset-<benchmark>.sql`)
2. Persist: `reset-flush.sh`: `innodb_max_dirty_pages_pct = 0`, wait until no dirty pages are left (at most 600 s), restore the old value
3. Counters: `FLUSH STATUS` (in `reset-flush.sh`)

See [Reset scripts](DBMS.md#reset-scripts--ar) for the reset contract and [Test: Reset Scripts](Test-Reset.md) for the test runs, with results for [YCSB](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_mariadb_summary.md), [Benchbase](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_benchbase_mariadb_summary.md), [HammerDB](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_hammerdb_mariadb_summary.md), [TPC-H](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_tpch_mariadb_summary.md), [TPC-DS](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_tpcds_mariadb_summary.md).


## TPC-DS

For performing the experiment we can run the [tpcds file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpcds.py).

### Power Test

```bash
bexhoma tpcds \
  -dbms MariaDB \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_mariadb.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_mariadb_summary.md" target="_blank" rel="noopener">docs_tpcds_mariadb.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 4037s 
* Code: 1782833902
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.2.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MariaDB-1-1-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:268035
  * datadisk:4543
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782833902

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1782833902-fdb6f66d8-5zpn7: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |    1 |      585.00 |           0.00 |            0.00 |         66.00 |          512.00 |              8 |           0 |             | None           |             0 | False         |                6.15 |

### Execution

#### Per Connection

|                   | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MariaDB-1-1-1-1-1 | MariaDB-1       | MariaDB-1-1-1 | MariaDB-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               97 |       3204 |            0.99 |             3680.65 |            108.99 |          -1 | MariaDB-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MariaDB-1-1-1 | MariaDB-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               97 |       3204 |            0.99 |             3680.65 |            108.99 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   MariaDB-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |               21.54 |
| TPC-DS Q2     |             4688.76 |
| TPC-DS Q3     |               19.31 |
| TPC-DS Q4     |            12070.81 |
| TPC-DS Q5     |             8657.12 |
| TPC-DS Q6     |              741.86 |
| TPC-DS Q7     |             4017.22 |
| TPC-DS Q8     |              381.48 |
| TPC-DS Q9     |             3799.48 |
| TPC-DS Q10    |               60.42 |
| TPC-DS Q11    |             8152.01 |
| TPC-DS Q12    |              258.03 |
| TPC-DS Q13    |             1067.62 |
| TPC-DS Q14a+b |            49638.93 |
| TPC-DS Q15    |              175.56 |
| TPC-DS Q16    |            11121.39 |
| TPC-DS Q17    |              707.26 |
| TPC-DS Q18    |             1952.32 |
| TPC-DS Q19    |              309.52 |
| TPC-DS Q20    |              433.49 |
| TPC-DS Q21    |            21572.00 |
| TPC-DS Q22    |            19869.36 |
| TPC-DS Q23a+b |            57465.28 |
| TPC-DS Q24a+b |               32.58 |
| TPC-DS Q25    |              153.86 |
| TPC-DS Q26    |              868.66 |
| TPC-DS Q27    |             1665.35 |
| TPC-DS Q28    |             2837.08 |
| TPC-DS Q29    |               94.89 |
| TPC-DS Q30    |              106.37 |
| TPC-DS Q31    |             1408.80 |
| TPC-DS Q32    |               12.06 |
| TPC-DS Q33    |              158.76 |
| TPC-DS Q34    |             3045.86 |
| TPC-DS Q35    |             1288.52 |
| TPC-DS Q36    |             1771.70 |
| TPC-DS Q37    |             3663.48 |
| TPC-DS Q38    |             7218.75 |
| TPC-DS Q39a+b |             1314.93 |
| TPC-DS Q40    |              179.28 |
| TPC-DS Q41    |              408.73 |
| TPC-DS Q42    |              281.63 |
| TPC-DS Q43    |             1109.11 |
| TPC-DS Q44    |             1198.02 |
| TPC-DS Q45    |              134.35 |
| TPC-DS Q46    |             3230.52 |
| TPC-DS Q47    |            15022.31 |
| TPC-DS Q48    |             1248.50 |
| TPC-DS Q49    |              109.78 |
| TPC-DS Q50    |               35.45 |
| TPC-DS Q51    |             7916.88 |
| TPC-DS Q52    |              314.14 |
| TPC-DS Q53    |              153.86 |
| TPC-DS Q54    |             1086.61 |
| TPC-DS Q55    |              247.21 |
| TPC-DS Q56    |              160.67 |
| TPC-DS Q57    |             6159.56 |
| TPC-DS Q58    |             5881.91 |
| TPC-DS Q59    |             9180.81 |
| TPC-DS Q60    |              663.17 |
| TPC-DS Q61    |              402.53 |
| TPC-DS Q62    |             1681.06 |
| TPC-DS Q63    |              136.88 |
| TPC-DS Q64    |              548.86 |
| TPC-DS Q65    |             5857.24 |
| TPC-DS Q66    |             1228.97 |
| TPC-DS Q67    |             7050.47 |
| TPC-DS Q68    |             3057.05 |
| TPC-DS Q69    |                3.60 |
| TPC-DS Q70    |             8193.80 |
| TPC-DS Q71    |              529.04 |
| TPC-DS Q72    |           403601.33 |
| TPC-DS Q73    |             3509.42 |
| TPC-DS Q74    |             6182.05 |
| TPC-DS Q75    |             5714.65 |
| TPC-DS Q76    |              465.15 |
| TPC-DS Q77    |             6261.85 |
| TPC-DS Q78    |             5726.20 |
| TPC-DS Q79    |             3437.41 |
| TPC-DS Q80    |              548.97 |
| TPC-DS Q81    |              220.27 |
| TPC-DS Q82    |             3659.84 |
| TPC-DS Q83    |              935.74 |
| TPC-DS Q84    |               59.40 |
| TPC-DS Q85    |              146.99 |
| TPC-DS Q86    |              919.30 |
| TPC-DS Q87    |             7199.08 |
| TPC-DS Q88    |            16154.30 |
| TPC-DS Q89    |             1615.79 |
| TPC-DS Q90    |              119.56 |
| TPC-DS Q91    |               24.38 |
| TPC-DS Q92    |                9.40 |
| TPC-DS Q93    |               45.70 |
| TPC-DS Q96    |              807.61 |
| TPC-DS Q97    |             5338.46 |
| TPC-DS Q98    |              875.80 |
| TPC-DS Q99    |             4938.86 |

### Errors (failed queries)

|                   |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| MariaDB-1-1-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |
* TPC-DS Q94
  * MariaDB-1-1-1-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=59) Query execution was interrupted (max_statement_time exceeded)
* TPC-DS Q95
  * MariaDB-1-1-1-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=59) Query execution was interrupted (max_statement_time exceeded)

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST failed: SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```

</details>

### Monitoring

```bash
bexhoma tpcds \
  -dbms MariaDB \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_mariadb_monitoring.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_mariadb_monitoring_summary.md" target="_blank" rel="noopener">docs_tpcds_mariadb_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 4175s 
* Code: 1782408033
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MariaDB-1-1-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:225003
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782408033

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |    1 |      659.00 |           2.00 |            1.00 |         63.00 |          586.00 |              8 |           0 |             | None           |             0 | False         |                5.46 |

### Execution

#### Per Connection

|                   | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MariaDB-1-1-1-1-1 | MariaDB-1       | MariaDB-1-1-1 | MariaDB-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               97 |       3222 |            1.00 |             3615.10 |            108.38 |          -1 | MariaDB-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MariaDB-1-1-1 | MariaDB-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               97 |       3222 |            1.00 |             3615.10 |            108.38 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   MariaDB-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |               20.58 |
| TPC-DS Q2     |             5155.74 |
| TPC-DS Q3     |               17.24 |
| TPC-DS Q4     |            12760.85 |
| TPC-DS Q5     |             8530.52 |
| TPC-DS Q6     |              788.63 |
| TPC-DS Q7     |             3533.69 |
| TPC-DS Q8     |              364.70 |
| TPC-DS Q9     |             3826.11 |
| TPC-DS Q10    |               47.09 |
| TPC-DS Q11    |             8029.01 |
| TPC-DS Q12    |              249.82 |
| TPC-DS Q13    |             1138.95 |
| TPC-DS Q14a+b |            49164.50 |
| TPC-DS Q15    |              173.35 |
| TPC-DS Q16    |            11244.66 |
| TPC-DS Q17    |              803.62 |
| TPC-DS Q18    |             1934.76 |
| TPC-DS Q19    |              255.67 |
| TPC-DS Q20    |              437.01 |
| TPC-DS Q21    |            21254.04 |
| TPC-DS Q22    |            19635.03 |
| TPC-DS Q23a+b |            58108.26 |
| TPC-DS Q24a+b |             2072.30 |
| TPC-DS Q25    |              158.64 |
| TPC-DS Q26    |              898.32 |
| TPC-DS Q27    |             1680.10 |
| TPC-DS Q28    |             2833.70 |
| TPC-DS Q29    |               97.75 |
| TPC-DS Q30    |              103.69 |
| TPC-DS Q31    |             1445.23 |
| TPC-DS Q32    |               10.71 |
| TPC-DS Q33    |              204.18 |
| TPC-DS Q34    |             3192.23 |
| TPC-DS Q35    |             1189.62 |
| TPC-DS Q36    |             1688.02 |
| TPC-DS Q37    |             3737.26 |
| TPC-DS Q38    |             7163.57 |
| TPC-DS Q39a+b |             1324.60 |
| TPC-DS Q40    |              186.38 |
| TPC-DS Q41    |              413.10 |
| TPC-DS Q42    |              239.73 |
| TPC-DS Q43    |             1148.65 |
| TPC-DS Q44    |                2.52 |
| TPC-DS Q45    |              128.51 |
| TPC-DS Q46    |             3546.82 |
| TPC-DS Q47    |            13981.45 |
| TPC-DS Q48    |             1259.37 |
| TPC-DS Q49    |              114.33 |
| TPC-DS Q50    |               30.74 |
| TPC-DS Q51    |             7630.46 |
| TPC-DS Q52    |              224.42 |
| TPC-DS Q53    |              161.65 |
| TPC-DS Q54    |             1039.59 |
| TPC-DS Q55    |              218.12 |
| TPC-DS Q56    |              133.75 |
| TPC-DS Q57    |             6727.82 |
| TPC-DS Q58    |             5732.05 |
| TPC-DS Q59    |             9403.49 |
| TPC-DS Q60    |              663.03 |
| TPC-DS Q61    |              370.34 |
| TPC-DS Q62    |             1684.59 |
| TPC-DS Q63    |              152.48 |
| TPC-DS Q64    |              566.63 |
| TPC-DS Q65    |             5794.88 |
| TPC-DS Q66    |             1281.28 |
| TPC-DS Q67    |             7257.30 |
| TPC-DS Q68    |             3197.45 |
| TPC-DS Q69    |                3.45 |
| TPC-DS Q70    |             8595.11 |
| TPC-DS Q71    |              522.66 |
| TPC-DS Q72    |           406943.14 |
| TPC-DS Q73    |             2959.08 |
| TPC-DS Q74    |             6295.58 |
| TPC-DS Q75    |             5770.01 |
| TPC-DS Q76    |              845.91 |
| TPC-DS Q77    |             6337.57 |
| TPC-DS Q78    |             5962.35 |
| TPC-DS Q79    |             3277.33 |
| TPC-DS Q80    |              842.18 |
| TPC-DS Q81    |              316.31 |
| TPC-DS Q82    |             4404.48 |
| TPC-DS Q83    |              948.80 |
| TPC-DS Q84    |               59.16 |
| TPC-DS Q85    |              148.73 |
| TPC-DS Q86    |              980.04 |
| TPC-DS Q87    |             7542.86 |
| TPC-DS Q88    |            25828.87 |
| TPC-DS Q89    |             1677.75 |
| TPC-DS Q90    |              395.91 |
| TPC-DS Q91    |               28.21 |
| TPC-DS Q92    |               10.74 |
| TPC-DS Q93    |               44.28 |
| TPC-DS Q96    |             2678.46 |
| TPC-DS Q97    |             5174.98 |
| TPC-DS Q98    |              857.55 |
| TPC-DS Q99    |             4862.09 |

### Errors (failed queries)

|                   |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| MariaDB-1-1-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |
* TPC-DS Q94
  * MariaDB-1-1-1-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=61) Query execution was interrupted (max_statement_time exceeded)
* TPC-DS Q95
  * MariaDB-1-1-1-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=61) Query execution was interrupted (max_statement_time exceeded)

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |       752.71 |      4.40 |           8.68 |                  8.79 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |         2.14 |      0.04 |           0.01 |                  0.76 |

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |      3193.56 |      1.00 |           8.93 |                  9.04 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |        20.80 |      0.02 |           0.30 |                  0.31 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST failed: SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```

</details>

### Throughput Test on Persistent Storage

```bash
bexhoma tpcds \
  -dbms MariaDB \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 2 \
  -ne 1,2 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rsr \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_mariadb_storage.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_mariadb_storage_summary.md" target="_blank" rel="noopener">docs_tpcds_mariadb_storage.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 16025s 
* Code: 1782408084
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 10Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* MariaDB-1-1-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:225003
  * volume_size:10G
  * volume_used:4.5G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782408084
* MariaDB-1-1-2-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220477
  * volume_size:10G
  * volume_used:4.5G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782408084
* MariaDB-1-1-2-1-2 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220477
  * volume_size:10G
  * volume_used:4.5G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782408084
* MariaDB-1-2-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220478
  * volume_size:10G
  * volume_used:4.5G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782408084
* MariaDB-1-2-2-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220478
  * volume_size:10G
  * volume_used:4.5G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782408084
* MariaDB-1-2-2-1-2 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220478
  * volume_size:10G
  * volume_used:4.5G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782408084

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: tpcds (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: tpcds (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 2: tpcds (2 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: tpcds (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: tpcds (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 2: tpcds (2 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |    1 |     2391.00 |           5.00 |            1.00 |        464.00 |         1913.00 |              8 |           0 |             | None           |             0 | False         |                1.51 |
| MariaDB-1-2 |                2 |    1 |     2391.00 |           5.00 |            1.00 |        464.00 |         1913.00 |              8 |           0 |             | None           |             0 | False         |                1.51 |

### Execution

#### Per Connection

|                   | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MariaDB-1-1-1-1-1 | MariaDB-1       | MariaDB-1-1-1 | MariaDB-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               97 |       3190 |            1.03 |             3534.75 |            109.47 |          -1 | MariaDB-1-1-1-1-1 |
| MariaDB-1-1-2-1-1 | MariaDB-1       | MariaDB-1-1-2 | MariaDB-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               97 |       3269 |            1.10 |             3286.12 |            106.82 |          -1 | MariaDB-1-1-2-1-1 |
| MariaDB-1-1-2-1-2 | MariaDB-1       | MariaDB-1-1-2 | MariaDB-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               97 |       3265 |            1.09 |             3332.89 |            106.95 |          -1 | MariaDB-1-1-2-1-2 |
| MariaDB-1-2-1-1-1 | MariaDB-1       | MariaDB-1-2-1 | MariaDB-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               97 |       3176 |            1.03 |             3536.56 |            109.95 |          -1 | MariaDB-1-2-1-1-1 |
| MariaDB-1-2-2-1-1 | MariaDB-1       | MariaDB-1-2-2 | MariaDB-1-2-2-1 |                2 |        2 |               1 |           1 | 1.00 |               97 |       3309 |            1.16 |             3112.08 |            105.53 |          -1 | MariaDB-1-2-2-1-1 |
| MariaDB-1-2-2-1-2 | MariaDB-1       | MariaDB-1-2-2 | MariaDB-1-2-2-1 |                2 |        2 |               1 |           1 | 1.00 |               97 |       3310 |            1.13 |             3204.20 |            105.50 |          -1 | MariaDB-1-2-2-1-2 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MariaDB-1-1-1 | MariaDB-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               97 |       3190 |            1.03 |             3534.75 |            109.47 |          -1 |
| MariaDB-1-1-2 | MariaDB-1-1-2 |                1 |        2 |               1 |           2 | 1.00 |              194 |       3269 |            1.10 |             3309.42 |            213.64 |          -1 |
| MariaDB-1-2-1 | MariaDB-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               97 |       3176 |            1.03 |             3536.56 |            109.95 |          -1 |
| MariaDB-1-2-2 | MariaDB-1-2-2 |                2 |        2 |               1 |           2 | 1.00 |              194 |       3310 |            1.15 |             3157.80 |            211.00 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   MariaDB-1-1-1-1-1 |   MariaDB-1-1-2-1-1 |   MariaDB-1-1-2-1-2 |   MariaDB-1-2-1-1-1 |   MariaDB-1-2-2-1-1 |   MariaDB-1-2-2-1-2 |
|:--------------|--------------------:|--------------------:|--------------------:|--------------------:|--------------------:|--------------------:|
| TPC-DS Q1     |               21.25 |               21.99 |               20.65 |              156.55 |               19.74 |               19.42 |
| TPC-DS Q2     |             4572.82 |             4580.97 |             4652.58 |             4663.55 |             4672.21 |             4425.77 |
| TPC-DS Q3     |               12.23 |               10.62 |               10.31 |               29.80 |                9.75 |               10.38 |
| TPC-DS Q4     |            11814.81 |            12501.07 |            12437.42 |            12102.38 |            12928.04 |            12800.08 |
| TPC-DS Q5     |             8366.21 |             9842.79 |             9910.66 |             9389.33 |            10867.63 |            10874.60 |
| TPC-DS Q6     |              739.85 |             1265.71 |              849.79 |              748.56 |             1320.35 |             1188.27 |
| TPC-DS Q7     |             3376.76 |             4458.41 |             4393.45 |             3429.95 |             5104.82 |             5209.71 |
| TPC-DS Q8     |              343.92 |              367.82 |              338.62 |              363.22 |              492.11 |              486.03 |
| TPC-DS Q9     |             3799.43 |             3882.50 |             3799.12 |             3794.98 |             3878.79 |             3896.92 |
| TPC-DS Q10    |               35.46 |               54.46 |               29.46 |               37.15 |               57.30 |               30.34 |
| TPC-DS Q11    |             8050.92 |             9397.69 |             9382.76 |             8350.30 |             9387.13 |             9359.84 |
| TPC-DS Q12    |              248.72 |              362.98 |              362.63 |              249.00 |              348.20 |              349.12 |
| TPC-DS Q13    |             1054.74 |             1461.56 |             1461.12 |             1191.68 |             1474.66 |             1474.37 |
| TPC-DS Q14a+b |            48552.25 |            62756.87 |            62759.34 |            48582.69 |            63169.03 |            62933.92 |
| TPC-DS Q15    |              163.26 |              196.61 |              181.96 |              177.04 |              166.73 |              180.11 |
| TPC-DS Q16    |            10847.69 |            14153.72 |            14151.81 |            10820.47 |            12814.62 |            13007.66 |
| TPC-DS Q17    |              728.31 |             1050.29 |             1050.16 |              767.33 |             1008.07 |              940.85 |
| TPC-DS Q18    |             1844.73 |             2495.47 |             2494.17 |             1850.02 |             2570.09 |             2592.19 |
| TPC-DS Q19    |              238.02 |              255.75 |              275.81 |              231.32 |              244.95 |              263.61 |
| TPC-DS Q20    |              458.56 |              591.78 |              601.10 |              442.84 |              568.52 |              571.26 |
| TPC-DS Q21    |            21074.79 |            33681.57 |            32755.89 |            21235.75 |            34368.12 |            34372.27 |
| TPC-DS Q22    |            19298.32 |            23518.30 |            22760.57 |            19338.94 |            24807.46 |            25263.17 |
| TPC-DS Q23a+b |            48300.77 |            60779.03 |            58433.79 |            47628.03 |            60414.22 |            60098.87 |
| TPC-DS Q24a+b |             2055.66 |             2286.62 |             2203.90 |             2019.86 |             2589.10 |             2494.32 |
| TPC-DS Q25    |              141.25 |              148.99 |              158.71 |              149.85 |              174.74 |              151.71 |
| TPC-DS Q26    |              831.80 |              833.36 |              875.27 |              873.59 |             1117.71 |             1120.46 |
| TPC-DS Q27    |             1652.02 |             1693.30 |             2310.39 |             1698.96 |             2212.60 |             2216.17 |
| TPC-DS Q28    |             2802.26 |             2788.12 |             2818.67 |             2791.98 |             2903.12 |             2926.11 |
| TPC-DS Q29    |               88.25 |               93.80 |               96.65 |               88.78 |              126.71 |              127.19 |
| TPC-DS Q30    |              102.43 |              139.73 |              108.13 |              105.74 |              127.20 |              129.53 |
| TPC-DS Q31    |             1396.46 |             1451.24 |             1466.10 |             1386.77 |             1709.62 |             1711.92 |
| TPC-DS Q32    |               10.50 |               10.73 |                9.95 |                9.58 |               10.85 |               10.44 |
| TPC-DS Q33    |              164.08 |              183.65 |              178.22 |              170.11 |              229.13 |              219.65 |
| TPC-DS Q34    |             2912.74 |             3104.45 |             2968.59 |             2874.04 |             3912.62 |             3927.87 |
| TPC-DS Q35    |             1133.96 |             1218.13 |             1243.14 |             1140.08 |             1648.53 |             1643.21 |
| TPC-DS Q36    |             1620.78 |             1799.61 |             1786.51 |             1645.18 |             2414.60 |             3016.97 |
| TPC-DS Q37    |             3538.03 |             3763.53 |             3979.29 |             3637.88 |             4191.12 |             5101.84 |
| TPC-DS Q38    |             7006.01 |             8248.53 |             8141.00 |             7148.33 |             8886.38 |             8664.93 |
| TPC-DS Q39a+b |             1168.31 |             1189.52 |             1202.60 |             1223.29 |             1203.41 |             1191.13 |
| TPC-DS Q40    |              175.99 |              180.18 |              237.27 |              180.80 |              183.92 |              203.87 |
| TPC-DS Q41    |              397.18 |              400.24 |              402.33 |              391.30 |              390.42 |              394.80 |
| TPC-DS Q42    |              223.24 |              233.10 |              246.26 |              216.27 |              232.34 |              263.56 |
| TPC-DS Q43    |             1152.75 |             1409.22 |             1312.66 |             1126.98 |             1276.68 |             1215.07 |
| TPC-DS Q44    |             1165.07 |             1181.96 |             1174.86 |             1154.83 |             1181.82 |             1146.20 |
| TPC-DS Q45    |              217.63 |              143.93 |              140.66 |              135.37 |              168.65 |              138.83 |
| TPC-DS Q46    |             5502.38 |             3800.02 |             4170.88 |             3534.17 |             4205.41 |             4251.95 |
| TPC-DS Q47    |            14345.68 |            13441.87 |            13457.65 |            12648.00 |            13383.53 |            13805.53 |
| TPC-DS Q48    |             1272.92 |             1339.87 |             1379.83 |             1206.61 |             1347.37 |             1324.44 |
| TPC-DS Q49    |              111.87 |               96.78 |              111.16 |              113.47 |              110.14 |               89.87 |
| TPC-DS Q50    |               34.56 |               37.21 |               35.83 |               34.25 |               51.22 |               34.18 |
| TPC-DS Q51    |             7653.39 |             8029.37 |             8192.90 |             7680.66 |             9296.93 |             8714.28 |
| TPC-DS Q52    |              246.52 |              264.49 |              249.46 |              239.00 |              238.53 |              279.04 |
| TPC-DS Q53    |              143.85 |              155.63 |              143.53 |              143.00 |              142.95 |              155.68 |
| TPC-DS Q54    |             1048.88 |             1048.92 |             1034.33 |             1034.47 |             1101.29 |             1060.13 |
| TPC-DS Q55    |              229.28 |              247.48 |              227.60 |              224.44 |              255.68 |              246.92 |
| TPC-DS Q56    |              187.73 |              195.42 |              186.39 |              183.33 |              204.72 |              195.20 |
| TPC-DS Q57    |             6036.70 |             6392.01 |             6499.07 |             6089.04 |             6472.27 |             6442.59 |
| TPC-DS Q58    |             5944.94 |             7312.86 |             6721.07 |             5767.65 |             7401.82 |             7508.00 |
| TPC-DS Q59    |            11047.43 |            10566.60 |            10791.14 |             9049.94 |            10927.35 |            10747.04 |
| TPC-DS Q60    |              832.57 |              622.17 |              609.61 |              586.81 |              605.42 |              626.48 |
| TPC-DS Q61    |              390.04 |              386.09 |              385.62 |              363.84 |              413.20 |              377.21 |
| TPC-DS Q62    |             2319.48 |             2007.23 |             1930.39 |             1674.97 |             1926.94 |             1942.67 |
| TPC-DS Q63    |              262.15 |              207.31 |              164.45 |              162.91 |              200.26 |              171.74 |
| TPC-DS Q64    |              992.38 |              572.70 |              573.98 |              581.89 |              617.66 |              577.34 |
| TPC-DS Q65    |             6354.56 |             7478.49 |             7259.60 |             5843.99 |             7971.14 |             7874.61 |
| TPC-DS Q66    |             1235.07 |             1197.58 |             1205.87 |             1191.99 |             1378.54 |             1305.24 |
| TPC-DS Q67    |             7011.01 |             7170.33 |             7799.37 |             7045.88 |             8046.68 |             7982.74 |
| TPC-DS Q68    |             3061.65 |             3885.38 |             3029.25 |             3057.08 |             4063.73 |             4067.12 |
| TPC-DS Q69    |                3.57 |                2.98 |                2.98 |                3.60 |                3.69 |                2.96 |
| TPC-DS Q70    |             9522.08 |             9712.56 |            10397.34 |             8257.08 |            10838.14 |            10661.19 |
| TPC-DS Q71    |              597.96 |              477.95 |              475.43 |              485.90 |              582.93 |              495.58 |
| TPC-DS Q72    |           395212.23 |           409650.17 |           409844.91 |           391651.39 |           433132.47 |           435601.07 |
| TPC-DS Q73    |             2878.01 |             3006.95 |             3124.16 |             2908.24 |             3292.84 |             3213.67 |
| TPC-DS Q74    |             6129.58 |             6673.63 |             6618.97 |             5944.10 |             6730.25 |             6691.07 |
| TPC-DS Q75    |             5740.42 |             6206.04 |             6408.75 |             5536.32 |             6355.60 |             6155.40 |
| TPC-DS Q76    |              477.30 |              483.95 |              464.51 |              436.51 |              476.69 |              482.97 |
| TPC-DS Q77    |             6169.36 |             7420.22 |             7319.68 |             6029.10 |             7686.24 |             7760.36 |
| TPC-DS Q78    |             5676.84 |             6071.62 |             6103.93 |             5591.84 |             6073.52 |             5978.85 |
| TPC-DS Q79    |             3413.31 |             3822.91 |             3841.43 |             3421.33 |             3922.41 |             3980.36 |
| TPC-DS Q80    |              523.73 |              562.09 |              652.70 |              534.16 |              662.63 |              563.60 |
| TPC-DS Q81    |              220.88 |              220.16 |              221.36 |              212.61 |              219.78 |              212.44 |
| TPC-DS Q82    |             3862.53 |             4060.44 |             4096.51 |             3763.48 |             4172.12 |             4060.20 |
| TPC-DS Q83    |              913.73 |             1526.93 |              943.23 |              886.67 |              934.27 |             1058.47 |
| TPC-DS Q84    |               56.86 |               58.31 |               58.37 |               56.50 |               60.29 |               57.42 |
| TPC-DS Q85    |              121.47 |              130.24 |              136.11 |              121.23 |              130.96 |              128.22 |
| TPC-DS Q86    |              903.70 |             1164.70 |              964.87 |              906.07 |             1017.96 |             1163.04 |
| TPC-DS Q87    |             6966.96 |             8403.44 |             8802.19 |             7092.20 |             8822.29 |             8679.90 |
| TPC-DS Q88    |            15895.84 |            18404.17 |            18551.36 |            15518.00 |            21083.81 |            21158.54 |
| TPC-DS Q89    |             1555.02 |             1577.60 |             1782.64 |             1584.78 |             1755.49 |             1539.85 |
| TPC-DS Q90    |              341.08 |              331.89 |              389.58 |              358.96 |              396.67 |              328.63 |
| TPC-DS Q91    |               16.67 |               16.61 |               17.02 |               19.73 |               21.68 |               16.29 |
| TPC-DS Q92    |               10.02 |                9.39 |                9.23 |                9.23 |                9.79 |                9.45 |
| TPC-DS Q93    |               38.31 |               38.44 |               40.50 |               44.05 |               44.03 |               37.44 |
| TPC-DS Q96    |              779.19 |              749.65 |              800.53 |              782.43 |              763.98 |              735.48 |
| TPC-DS Q97    |             5163.54 |             5996.10 |             5872.14 |             5179.33 |             6084.32 |             6250.16 |
| TPC-DS Q98    |              879.55 |             1046.87 |             1113.54 |              883.05 |             1178.87 |             1030.93 |
| TPC-DS Q99    |             4918.81 |             5354.58 |             5563.41 |             4911.81 |             5592.88 |             5456.76 |

### Errors (failed queries)

|                   |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| MariaDB-1-1-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| MariaDB-1-1-2-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| MariaDB-1-1-2-1-2 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| MariaDB-1-2-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| MariaDB-1-2-2-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| MariaDB-1-2-2-1-2 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |
* TPC-DS Q94
  * MariaDB-1-1-2-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=140) Query execution was interrupted (max_statement_time exceeded)
  * MariaDB-1-1-2-1-2: numRun 1: : java.sql.SQLTimeoutException: (conn=141) Query execution was interrupted (max_statement_time exceeded)
  * MariaDB-1-2-1-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=8) Query execution was interrupted (max_statement_time exceeded)
  * MariaDB-1-1-1-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=83) Query execution was interrupted (max_statement_time exceeded)
  * MariaDB-1-2-2-1-2: numRun 1: : java.sql.SQLTimeoutException: (conn=65) Query execution was interrupted (max_statement_time exceeded)
  * MariaDB-1-2-2-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=64) Query execution was interrupted (max_statement_time exceeded)
* TPC-DS Q95
  * MariaDB-1-1-2-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=140) Query execution was interrupted (max_statement_time exceeded)
  * MariaDB-1-1-2-1-2: numRun 1: : java.sql.SQLTimeoutException: (conn=141) Query execution was interrupted (max_statement_time exceeded)
  * MariaDB-1-2-1-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=8) Query execution was interrupted (max_statement_time exceeded)
  * MariaDB-1-1-1-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=83) Query execution was interrupted (max_statement_time exceeded)
  * MariaDB-1-2-2-1-2: numRun 1: : java.sql.SQLTimeoutException: (conn=65) Query execution was interrupted (max_statement_time exceeded)
  * MariaDB-1-2-2-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=64) Query execution was interrupted (max_statement_time exceeded)

### Warnings (result mismatch)

|                   |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| MariaDB-1-1-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| MariaDB-1-1-2-1-2 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| MariaDB-1-2-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| MariaDB-1-2-2-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| MariaDB-1-2-2-1-2 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |      2090.86 |      2.86 |           8.74 |                  8.85 |
| MariaDB-1-1-2-1 |      2090.86 |      2.86 |           8.74 |                  8.85 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| MariaDB-1-1-2-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |         3.46 |      0.04 |           0.00 |                  0.00 |
| MariaDB-1-1-2-1 |         3.46 |      0.04 |           0.00 |                  0.00 |

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |      3178.46 |      1.00 |           8.84 |                  8.94 |
| MariaDB-1-1-2-1 |      6509.84 |      2.00 |           9.32 |                  9.45 |
| MariaDB-1-2-1-1 |      3150.31 |      1.00 |           5.85 |                  5.89 |
| MariaDB-1-2-2-1 |      6573.27 |      2.00 |           6.18 |                  6.23 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |        21.13 |      0.41 |           0.32 |                  0.32 |
| MariaDB-1-1-2-1 |        27.56 |      0.07 |           0.33 |                  0.33 |
| MariaDB-1-2-1-1 |        20.90 |      0.38 |           0.31 |                  0.31 |
| MariaDB-1-2-2-1 |        26.77 |      0.06 |           0.33 |                  0.33 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST failed: SQL errors
* TEST failed: SQL warnings (result mismatch)
* TEST passed: Workflow as planned
```

</details>


## Benchbase's TPC-C

See [Example: Benchbase](Example-Benchbase.md) for the parameters.

### Simple

```bash
bexhoma benchbase \
  -dbms MariaDB \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_mariadb.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_mariadb_summary.md" target="_blank" rel="noopener">docs_benchbase_mariadb.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 835s 
* Code: 1782361791
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.10.0.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MariaDB-1-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:261844
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782361791

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: benchbase (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: benchbase (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |   16 |      265.00 |           2.00 |            0.00 |        114.00 |          149.00 |              1 |           1 |             | None           |             0 | False         |              217.36 |

### Execution

#### Per Connection

| DBMS              | phase         | job             |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:--------------|:----------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MariaDB-1-1-1-1-1 | MariaDB-1-1-1 | MariaDB-1-1-1-1 |                1 |         160 |     8192 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                        6489.12 |                     6382.97 |         0.00 |                                                      68949.00 |                                              21665.00 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:--------------|:--------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MariaDB-1-1-1 | MariaDB-1-1-1 |                1 |         160 |     8192 |               1 |           1 |          -1 | 300.00 |            0 |                        6489.12 |                     6382.97 |         0.00 |                                                      68949.00 |                                              21665.00 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```

</details>

### Persistent Storage

The second repetition (`-nc 2`) runs on the loaded volume.

```bash
bexhoma benchbase \
  -dbms MariaDB \
  -sf 16 \
  -xsd 1 \
  -xtb 1024 \
  -nc 2 \
  -ne 1 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rsr \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_mariadb_storage.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_mariadb_storage_summary.md" target="_blank" rel="noopener">docs_benchbase_mariadb_storage.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1331s 
* Code: 1782362666
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 1 minutes.
  * Experiment uses bexhoma version 0.10.0.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 30Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* MariaDB-1-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:253332
  * volume_size:30G
  * volume_used:1.9G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782362666
* MariaDB-1-2-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:260794
  * volume_size:30G
  * volume_used:2.0G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782362666

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: benchbase (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: benchbase (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |   16 |      761.00 |           2.00 |            0.00 |        356.00 |          403.00 |              1 |           1 |             | None           |             0 | False         |               75.69 |
| MariaDB-1-2 |                2 |   16 |      761.00 |           2.00 |            0.00 |        356.00 |          403.00 |              1 |           1 |             | None           |             0 | False         |               75.69 |

### Execution

#### Per Connection

| DBMS              | phase         | job             |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:--------------|:----------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MariaDB-1-1-1-1-1 | MariaDB-1-1-1 | MariaDB-1-1-1-1 |                1 |         160 |     8192 |        1 |               1 |       1 |          -1 |  60.00 |            0 |                        1143.50 |                     1127.18 |         0.00 |                                                     542141.00 |                                             137600.00 |
| MariaDB-1-2-1-1-1 | MariaDB-1-2-1 | MariaDB-1-2-1-1 |                2 |         160 |     8192 |        1 |               1 |       1 |          -1 |  60.00 |            0 |                        1116.67 |                     1101.28 |         0.00 |                                                     250549.00 |                                             130235.00 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:--------------|:--------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MariaDB-1-1-1 | MariaDB-1-1-1 |                1 |         160 |     8192 |               1 |           1 |          -1 |  60.00 |            0 |                        1143.50 |                     1127.18 |         0.00 |                                                     542141.00 |                                             137600.00 |
| MariaDB-1-2-1 | MariaDB-1-2-1 |                2 |         160 |     8192 |               1 |           1 |          -1 |  60.00 |            0 |                        1116.67 |                     1101.28 |         0.00 |                                                     250549.00 |                                             130235.00 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```

</details>

### Monitoring

```bash
bexhoma benchbase \
  -dbms MariaDB \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_mariadb_monitoring.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_mariadb_monitoring_summary.md" target="_blank" rel="noopener">docs_benchbase_mariadb_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 893s 
* Code: 1782364006
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MariaDB-1-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:222370
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364006

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: benchbase (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: benchbase (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |   16 |      332.00 |           2.00 |            0.00 |        142.00 |          188.00 |              1 |           1 |             | None           |             0 | False         |              173.49 |

### Execution

#### Per Connection

| DBMS              | phase         | job             |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:--------------|:----------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MariaDB-1-1-1-1-1 | MariaDB-1-1-1 | MariaDB-1-1-1-1 |                1 |         160 |     8192 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                        8191.94 |                     8102.43 |         0.00 |                                                      10659.00 |                                               5096.00 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:--------------|:--------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MariaDB-1-1-1 | MariaDB-1-1-1 |                1 |         160 |     8192 |               1 |           1 |          -1 | 300.00 |            0 |                        8191.94 |                     8102.43 |         0.00 |                                                      10659.00 |                                               5096.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |       267.20 |      3.31 |           3.79 |                  3.89 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |      1835.23 |     15.32 |           0.24 |                  0.24 |

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |      5273.25 |     18.16 |           5.49 |                  5.60 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |      4183.33 |     14.61 |           1.67 |                  1.67 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```

</details>

### Scaling the Clients

1 and 2 benchmarker pods (`-nbp 1,2`) and 1 and 2 rounds (`-ne 1,2`), on the volume loaded by the persistent storage run.

```bash
bexhoma benchbase \
  -dbms MariaDB \
  -sf 16 \
  -xsd 2 \
  -xtb 1024 \
  -nc 2 \
  -ne 1,2 \
  -nbp 1,2 \
  -nbt 160 \
  -xnbf 8 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_mariadb_scale.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_mariadb_scale_summary.md" target="_blank" rel="noopener">docs_benchbase_mariadb_scale.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 2495s 
* Code: 1782364932
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 2 minutes.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 30Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1, 2] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* MariaDB-1-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220471
  * volume_size:30G
  * volume_used:2.0G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364932
* MariaDB-1-1-2-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220471
  * volume_size:30G
  * volume_used:2.0G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364932
* MariaDB-1-1-3-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220471
  * volume_size:30G
  * volume_used:2.0G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364932
* MariaDB-1-1-4-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220472
  * volume_size:30G
  * volume_used:2.0G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364932
* MariaDB-1-2-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220472
  * volume_size:30G
  * volume_used:2.3G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364932
* MariaDB-1-2-2-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220472
  * volume_size:30G
  * volume_used:2.3G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364932
* MariaDB-1-2-3-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220471
  * volume_size:30G
  * volume_used:2.3G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364932
* MariaDB-1-2-4-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220471
  * volume_size:30G
  * volume_used:2.3G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364932

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS MariaDB-1 - Experiment 1 Client 3: benchbase (2 pods)
* DBMS MariaDB-1 - Experiment 1 Client 4: benchbase (4 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: benchbase (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 2: benchbase (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 3: benchbase (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 4: benchbase (4 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS MariaDB-1 - Experiment 1 Client 3: benchbase (2 pods)
* DBMS MariaDB-1 - Experiment 1 Client 4: benchbase (4 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: benchbase (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 2: benchbase (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 3: benchbase (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 4: benchbase (4 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |   16 |      761.00 |           2.00 |            0.00 |        356.00 |          403.00 |              0 |           1 |             | None           |             0 | False         |               75.69 |
| MariaDB-1-2 |                2 |   16 |      761.00 |           2.00 |            0.00 |        356.00 |          403.00 |              0 |           1 |             | None           |             0 | False         |               75.69 |

### Execution

#### Per Connection

| DBMS              | phase         | job             |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:--------------|:----------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MariaDB-1-1-1-1-1 | MariaDB-1-1-1 | MariaDB-1-1-1-1 |                1 |         160 |     8192 |        1 |               1 |       1 |          -1 | 120.00 |            0 |                         967.06 |                      952.57 |         0.00 |                                                     492745.00 |                                             164974.00 |
| MariaDB-1-1-2-1-1 | MariaDB-1-1-2 | MariaDB-1-1-2-1 |                1 |         160 |     8192 |        2 |               1 |       1 |          -1 | 120.00 |            0 |                         320.49 |                      316.64 |         0.00 |                                                    2093763.00 |                                             494056.00 |
| MariaDB-1-1-2-1-2 | MariaDB-1-1-2 | MariaDB-1-1-2-1 |                1 |         160 |     8192 |        2 |               1 |       2 |          -1 | 120.00 |            0 |                         242.21 |                      239.85 |         0.00 |                                                    2804421.00 |                                             659793.00 |
| MariaDB-1-1-3-1-1 | MariaDB-1-1-3 | MariaDB-1-1-3-1 |                1 |          80 |     4096 |        3 |               1 |       1 |          -1 | 120.00 |            0 |                         451.47 |                      445.15 |         0.00 |                                                     135576.00 |                                             169888.00 |
| MariaDB-1-1-3-1-2 | MariaDB-1-1-3 | MariaDB-1-1-3-1 |                1 |          80 |     4096 |        3 |               1 |       2 |          -1 | 120.00 |            0 |                         425.37 |                      419.38 |         0.00 |                                                     141231.00 |                                             179604.00 |
| MariaDB-1-1-4-1-1 | MariaDB-1-1-4 | MariaDB-1-1-4-1 |                1 |          80 |     4096 |        4 |               1 |       1 |          -1 | 120.00 |            0 |                         210.65 |                      208.06 |         0.00 |                                                    1383547.00 |                                             379692.00 |
| MariaDB-1-1-4-1-2 | MariaDB-1-1-4 | MariaDB-1-1-4-1 |                1 |          80 |     4096 |        4 |               1 |       2 |          -1 | 120.00 |            0 |                         232.05 |                      229.02 |         0.00 |                                                    1189542.00 |                                             343797.00 |
| MariaDB-1-1-4-1-3 | MariaDB-1-1-4 | MariaDB-1-1-4-1 |                1 |          80 |     4096 |        4 |               1 |       3 |          -1 | 120.00 |            0 |                         213.38 |                      210.43 |         0.00 |                                                    1355253.00 |                                             374383.00 |
| MariaDB-1-1-4-1-4 | MariaDB-1-1-4 | MariaDB-1-1-4-1 |                1 |          80 |     4096 |        4 |               1 |       4 |          -1 | 120.00 |            0 |                         225.12 |                      222.47 |         0.00 |                                                    1238071.00 |                                             353898.00 |
| MariaDB-1-2-1-1-1 | MariaDB-1-2-1 | MariaDB-1-2-1-1 |                2 |         160 |     8192 |        1 |               1 |       1 |          -1 | 120.00 |            0 |                         920.43 |                      906.26 |         0.00 |                                                     571446.00 |                                             172230.00 |
| MariaDB-1-2-2-1-1 | MariaDB-1-2-2 | MariaDB-1-2-2-1 |                2 |         160 |     8192 |        2 |               1 |       1 |          -1 | 120.00 |            0 |                         427.24 |                      421.13 |         0.00 |                                                    1017372.00 |                                             372815.00 |
| MariaDB-1-2-2-1-2 | MariaDB-1-2-2 | MariaDB-1-2-2-1 |                2 |         160 |     8192 |        2 |               1 |       2 |          -1 | 120.00 |            0 |                         357.92 |                      353.82 |         0.00 |                                                    1227140.00 |                                             445660.00 |
| MariaDB-1-2-3-1-1 | MariaDB-1-2-3 | MariaDB-1-2-3-1 |                2 |          80 |     4096 |        3 |               1 |       1 |          -1 | 120.00 |            0 |                         379.06 |                      373.49 |         0.00 |                                                     917359.00 |                                             199443.00 |
| MariaDB-1-2-3-1-2 | MariaDB-1-2-3 | MariaDB-1-2-3-1 |                2 |          80 |     4096 |        3 |               1 |       2 |          -1 | 120.00 |            0 |                         348.27 |                      343.62 |         0.00 |                                                     987067.00 |                                             216431.00 |
| MariaDB-1-2-4-1-1 | MariaDB-1-2-4 | MariaDB-1-2-4-1 |                2 |          80 |     4096 |        4 |               1 |       1 |          -1 | 120.00 |            0 |                         200.48 |                      197.60 |         0.00 |                                                    1357630.00 |                                             397247.00 |
| MariaDB-1-2-4-1-2 | MariaDB-1-2-4 | MariaDB-1-2-4-1 |                2 |          80 |     4096 |        4 |               1 |       2 |          -1 | 120.00 |            0 |                         220.92 |                      217.98 |         0.00 |                                                    1163093.00 |                                             360457.00 |
| MariaDB-1-2-4-1-3 | MariaDB-1-2-4 | MariaDB-1-2-4-1 |                2 |          80 |     4096 |        4 |               1 |       3 |          -1 | 120.00 |            0 |                         202.23 |                      199.54 |         0.00 |                                                    1305829.00 |                                             395153.00 |
| MariaDB-1-2-4-1-4 | MariaDB-1-2-4 | MariaDB-1-2-4-1 |                2 |          80 |     4096 |        4 |               1 |       4 |          -1 | 120.00 |            0 |                         207.67 |                      205.04 |         0.00 |                                                    1262583.00 |                                             384669.00 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:--------------|:--------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MariaDB-1-1-1 | MariaDB-1-1-1 |                1 |         160 |     8192 |               1 |           1 |          -1 | 120.00 |            0 |                         967.06 |                      952.57 |         0.00 |                                                     492745.00 |                                             164974.00 |
| MariaDB-1-1-2 | MariaDB-1-1-2 |                1 |         320 |    16384 |               1 |           2 |          -1 | 120.00 |            0 |                         562.70 |                      556.49 |         0.00 |                                                    2804421.00 |                                             576924.50 |
| MariaDB-1-1-3 | MariaDB-1-1-3 |                1 |         160 |     8192 |               1 |           2 |          -1 | 120.00 |            0 |                         876.85 |                      864.53 |         0.00 |                                                     141231.00 |                                             174746.00 |
| MariaDB-1-1-4 | MariaDB-1-1-4 |                1 |         320 |    16384 |               1 |           4 |          -1 | 120.00 |            0 |                         881.21 |                      869.98 |         0.00 |                                                    1383547.00 |                                             362942.50 |
| MariaDB-1-2-1 | MariaDB-1-2-1 |                2 |         160 |     8192 |               1 |           1 |          -1 | 120.00 |            0 |                         920.43 |                      906.26 |         0.00 |                                                     571446.00 |                                             172230.00 |
| MariaDB-1-2-2 | MariaDB-1-2-2 |                2 |         320 |    16384 |               1 |           2 |          -1 | 120.00 |            0 |                         785.17 |                      774.95 |         0.00 |                                                    1227140.00 |                                             409237.50 |
| MariaDB-1-2-3 | MariaDB-1-2-3 |                2 |         160 |     8192 |               1 |           2 |          -1 | 120.00 |            0 |                         727.33 |                      717.11 |         0.00 |                                                     987067.00 |                                             207937.00 |
| MariaDB-1-2-4 | MariaDB-1-2-4 |                2 |         320 |    16384 |               1 |           4 |          -1 | 120.00 |            0 |                         831.32 |                      820.17 |         0.00 |                                                    1357630.00 |                                             384381.50 |

### Monitoring

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |      2031.17 |     28.21 |           4.00 |                  4.10 |
| MariaDB-1-1-2-1 |      1322.28 |     18.92 |           4.23 |                  4.33 |
| MariaDB-1-1-3-1 |      1209.81 |     13.68 |           4.33 |                  4.43 |
| MariaDB-1-1-4-1 |      1048.15 |     11.39 |           4.49 |                  4.59 |
| MariaDB-1-2-1-1 |      1304.29 |     14.17 |           4.26 |                  4.36 |
| MariaDB-1-2-2-1 |      1065.69 |     15.92 |           4.55 |                  4.65 |
| MariaDB-1-2-3-1 |       926.95 |     10.39 |           4.62 |                  4.72 |
| MariaDB-1-2-4-1 |      1001.09 |     12.19 |           4.80 |                  4.90 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |       194.52 |      2.35 |           0.70 |                  0.70 |
| MariaDB-1-1-2-1 |       168.41 |      2.97 |           0.74 |                  0.74 |
| MariaDB-1-1-3-1 |       213.01 |      3.25 |           0.74 |                  0.74 |
| MariaDB-1-1-4-1 |       253.99 |      3.43 |           0.50 |                  0.50 |
| MariaDB-1-2-1-1 |       197.18 |      2.65 |           0.71 |                  0.71 |
| MariaDB-1-2-2-1 |       228.81 |      4.92 |           0.79 |                  0.79 |
| MariaDB-1-2-3-1 |       171.83 |      4.99 |           0.79 |                  0.79 |
| MariaDB-1-2-4-1 |       235.27 |      4.42 |           0.49 |                  0.49 |

### Tests
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```

</details>


## HammerDB's TPC-C

See [Example: HammerDB](Example-HammerDB.md) for the parameters.

### Simple

```bash
bexhoma hammerdb \
  -dbms MariaDB \
  -sf 16 \
  -nlt 8 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 16 \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hammerdb_mariadb.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hammerdb_mariadb_summary.md" target="_blank" rel="noopener">docs_hammerdb_mariadb.log</a></summary>

```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 885s 
* Code: 1780052904
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.9.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker3.
  * Loading is tested with [8] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MariaDB-1-1-1 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:59776
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780052904

### Workflow

#### Actual

* DBMS MariaDB-1 - Pods [[1]]

#### Planned

* DBMS MariaDB-1 - Pods [[1]]

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |   16 |      190.00 |           1.00 |            0.00 |         80.00 |          109.00 |              1 |           8 |          | None           |             0 | False         |              303.16 |

### Execution

#### Per Connection

| DBMS            |   experiment_run |   vusers |   client |   child |   NOPM |    TPM |   efficiency |   duration |   errors |
|:----------------|-----------------:|---------:|---------:|--------:|-------:|-------:|-------------:|-----------:|---------:|
| MariaDB-1-1-1-1 |                1 |       16 |        1 |       1 |  63390 | 147366 |         0.00 |          5 |        0 |

#### Per Phase

| DBMS          |   experiment_run |   vusers |   client |   pod_count |   efficiency |     NOPM |       TPM |   duration |   errors |
|:--------------|-----------------:|---------:|---------:|------------:|-------------:|---------:|----------:|-----------:|---------:|
| MariaDB-1-1-1 |             1.00 |    16.00 |     1.00 |        1.00 |         0.00 | 63390.00 | 147366.00 |       5.00 |     0.00 |

### Tests
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
```

</details>

### Monitoring on Persistent Storage

```bash
bexhoma hammerdb \
  -dbms MariaDB \
  -sf 16 \
  -nlt 8 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 16 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rsr \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hammerdb_mariadb_monitoring.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hammerdb_mariadb_monitoring_summary.md" target="_blank" rel="noopener">docs_hammerdb_mariadb_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 1155s 
* Code: 1780053795
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.9.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker3.
  * Database is persisted to disk of type shared and size 30Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MariaDB-1-1-1 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:1.7G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780053795

### Workflow

#### Actual

* DBMS MariaDB-1 - Pods [[1]]

#### Planned

* DBMS MariaDB-1 - Pods [[1]]

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |   16 |      700.00 |           1.00 |            0.00 |        335.00 |          364.00 |              1 |           8 |          | None           |             0 | False         |               82.29 |

### Execution

#### Per Connection

| DBMS            |   experiment_run |   vusers |   client |   child |   NOPM |   TPM |   efficiency |   duration |   errors |
|:----------------|-----------------:|---------:|---------:|--------:|-------:|------:|-------------:|-----------:|---------:|
| MariaDB-1-1-1-1 |                1 |       16 |        1 |       1 |   9805 | 22794 |         0.00 |          5 |        0 |

#### Per Phase

| DBMS          |   experiment_run |   vusers |   client |   pod_count |   efficiency |    NOPM |      TPM |   duration |   errors |
|:--------------|-----------------:|---------:|---------:|------------:|-------------:|--------:|---------:|-----------:|---------:|
| MariaDB-1-1-1 |             1.00 |    16.00 |     1.00 |        1.00 |         0.00 | 9805.00 | 22794.00 |       5.00 |     0.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1 |       845.08 |      3.35 |           7.06 |                  7.16 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1 |       271.99 |      1.16 |           0.10 |                  0.10 |

### Execution phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1 |       947.62 |      3.68 |           7.16 |                  7.26 |

### Execution phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1 |        40.35 |      0.15 |           0.07 |                  0.07 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
```

</details>

### Scaling the Clients

1 and 2 benchmarker pods (`-nbp 1,2`) and 1 and 2 rounds (`-ne 1,2`), on the volume loaded by the monitoring run.

```bash
bexhoma hammerdb \
  -dbms MariaDB \
  -sf 16 \
  -xsd 2 \
  -nlt 8 \
  -nc 2 \
  -ne 1,2 \
  -nbp 1,2 \
  -nbt 16 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hammerdb_mariadb_scale.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hammerdb_mariadb_scale_summary.md" target="_blank" rel="noopener">docs_hammerdb_mariadb_scale.log</a></summary>

```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 3224s 
* Code: 1780054976
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 2 minutes.
  * Experiment uses bexhoma version 0.9.9.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker3.
  * Database is persisted to disk of type shared and size 30Gi.
  * Loading is tested with [8] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* MariaDB-1-1-1 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780054976
* MariaDB-1-1-2 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780054976
* MariaDB-1-1-3 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780054976
* MariaDB-1-1-4 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780054976
* MariaDB-1-2-1 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:1.9G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780054976
* MariaDB-1-2-2 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:1.9G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780054976
* MariaDB-1-2-3 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:1.9G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780054976
* MariaDB-1-2-4 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:1.9G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780054976

### Workflow

#### Actual

* DBMS MariaDB-1 - Pods [[1, 2, 2, 4], [1, 2, 2, 4]]

#### Planned

* DBMS MariaDB-1 - Pods [[1, 2, 2, 4], [1, 2, 2, 4]]

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |   16 |      700.00 |           1.00 |            0.00 |        335.00 |          364.00 |              0 |           8 |          | None           |             0 | False         |               82.29 |
| MariaDB-1-2 |                2 |   16 |      700.00 |           1.00 |            0.00 |        335.00 |          364.00 |              0 |           8 |          | None           |             0 | False         |               82.29 |

### Execution

#### Per Connection

| DBMS            |   experiment_run |   vusers |   client |   child |   NOPM |   TPM |   efficiency |   duration |   errors |
|:----------------|-----------------:|---------:|---------:|--------:|-------:|------:|-------------:|-----------:|---------:|
| MariaDB-1-1-1-1 |                1 |       16 |        1 |       1 |  12123 | 28299 |         0.00 |          2 |        0 |
| MariaDB-1-1-2-1 |                1 |       16 |        2 |       1 |   9914 | 22893 |         0.00 |          2 |        0 |
| MariaDB-1-1-2-1 |                1 |       16 |        2 |       1 |  10146 | 23427 |         0.00 |          2 |        0 |
| MariaDB-1-1-3-1 |                1 |        8 |        3 |       1 |   7436 | 17246 |         0.00 |          2 |        0 |
| MariaDB-1-1-3-1 |                1 |        8 |        3 |       1 |   7440 | 17252 |         0.00 |          2 |        0 |
| MariaDB-1-1-4-1 |                1 |        8 |        4 |       1 |   6528 | 15148 |         0.00 |          2 |        0 |
| MariaDB-1-1-4-1 |                1 |        8 |        4 |       1 |   6591 | 15283 |         0.00 |          2 |        0 |
| MariaDB-1-1-4-1 |                1 |        8 |        4 |       1 |   6535 | 15169 |         0.00 |          2 |        0 |
| MariaDB-1-1-4-1 |                1 |        8 |        4 |       1 |   6560 | 15217 |         0.00 |          2 |        0 |
| MariaDB-1-2-1-1 |                2 |       16 |        1 |       1 |   9101 | 21227 |         0.00 |          2 |        0 |
| MariaDB-1-2-2-1 |                2 |       16 |        2 |       1 |   9011 | 20796 |         0.00 |          2 |        0 |
| MariaDB-1-2-2-1 |                2 |       16 |        2 |       1 |   9077 | 20938 |         0.00 |          2 |        0 |
| MariaDB-1-2-3-1 |                2 |        8 |        3 |       1 |   8350 | 19461 |         0.00 |          2 |        0 |
| MariaDB-1-2-3-1 |                2 |        8 |        3 |       1 |   8295 | 19358 |         0.00 |          2 |        0 |
| MariaDB-1-2-4-1 |                2 |        8 |        4 |       1 |   8527 | 19937 |         0.00 |          2 |        0 |
| MariaDB-1-2-4-1 |                2 |        8 |        4 |       1 |   8431 | 19717 |         0.00 |          2 |        0 |
| MariaDB-1-2-4-1 |                2 |        8 |        4 |       1 |   8498 | 19865 |         0.00 |          2 |        0 |
| MariaDB-1-2-4-1 |                2 |        8 |        4 |       1 |   8431 | 19717 |         0.00 |          2 |        0 |

#### Per Phase

| DBMS          |   experiment_run |   vusers |   client |   pod_count |   efficiency |     NOPM |      TPM |   duration |   errors |
|:--------------|-----------------:|---------:|---------:|------------:|-------------:|---------:|---------:|-----------:|---------:|
| MariaDB-1-1-1 |             1.00 |    16.00 |     1.00 |        1.00 |         0.00 | 12123.00 | 28299.00 |       2.00 |     0.00 |
| MariaDB-1-1-2 |             1.00 |    32.00 |     2.00 |        2.00 |         0.00 | 10030.00 | 23160.00 |       2.00 |     0.00 |
| MariaDB-1-1-3 |             1.00 |    16.00 |     3.00 |        2.00 |         0.00 |  7438.00 | 17249.00 |       2.00 |     0.00 |
| MariaDB-1-1-4 |             1.00 |    32.00 |     4.00 |        4.00 |         0.00 |  6553.50 | 15204.25 |       2.00 |     0.00 |
| MariaDB-1-2-1 |             2.00 |    16.00 |     1.00 |        1.00 |         0.00 |  9101.00 | 21227.00 |       2.00 |     0.00 |
| MariaDB-1-2-2 |             2.00 |    32.00 |     2.00 |        2.00 |         0.00 |  9044.00 | 20867.00 |       2.00 |     0.00 |
| MariaDB-1-2-3 |             2.00 |    16.00 |     3.00 |        2.00 |         0.00 |  8322.50 | 19409.50 |       2.00 |     0.00 |
| MariaDB-1-2-4 |             2.00 |    32.00 |     4.00 |        4.00 |         0.00 |  8471.75 | 19809.00 |       2.00 |     0.00 |

### Monitoring

### Execution phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1 |       585.20 |      2.97 |           6.84 |                  6.94 |
| MariaDB-1-1-2 |       871.45 |      6.59 |           6.95 |                  7.05 |
| MariaDB-1-1-3 |       506.27 |      4.93 |           6.98 |                  7.08 |
| MariaDB-1-1-4 |       940.30 |      5.49 |           7.06 |                  7.16 |
| MariaDB-1-2-1 |      3027.35 |      2.36 |           7.06 |                  7.16 |
| MariaDB-1-2-2 |       863.04 |      4.29 |           7.06 |                  7.16 |
| MariaDB-1-2-3 |       418.66 |      2.17 |           7.09 |                  7.19 |
| MariaDB-1-2-4 |       798.13 |      3.86 |           7.18 |                  7.28 |

### Execution phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1 |        24.52 |      0.13 |           0.07 |                  0.07 |
| MariaDB-1-1-2 |        24.52 |      0.34 |           0.07 |                  0.07 |
| MariaDB-1-1-3 |        21.49 |      0.28 |           0.07 |                  0.07 |
| MariaDB-1-1-4 |        16.11 |      0.25 |           0.04 |                  0.05 |
| MariaDB-1-2-1 |        22.71 |      0.13 |           0.07 |                  0.07 |
| MariaDB-1-2-2 |        22.71 |      0.27 |           0.07 |                  0.07 |
| MariaDB-1-2-3 |        22.87 |      0.21 |           0.07 |                  0.07 |
| MariaDB-1-2-4 |        18.35 |      0.26 |           0.04 |                  0.05 |

### Tests
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
```

</details>


## YCSB

See [Example: YCSB](Example-YCSB.md) for the parameters.

### Scaling the Loader

4 and 8 loader pods (`-nlp 4,8`) with 32 and 64 threads (`-nlt 32,64`):

```bash
bexhoma ycsb \
  -dbms MariaDB \
  -sf 1 \
  -xwl a \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nlp 4,8 \
  -nlt 32,64 \
  -xnlf 1 \
  -nbp 1 \
  -nbt 64 \
  -xnbf 1 \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_mariadb_loading.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_mariadb_loading_summary.md" target="_blank" rel="noopener">docs_ycsb_mariadb_loading.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 2348s 
* Code: 1793642911
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '1024'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 4 and 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [32, 64] threads, split into [4, 8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mariadb', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mariadb-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:706546
  * datadisk:1794
  * volume_size:1.8T
  * volume_used:690G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793642911
* mariadb-2-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:706546
  * datadisk:1770
  * volume_size:1.8T
  * volume_used:690G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793642911
* mariadb-3-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:706546
  * datadisk:1794
  * volume_size:1.8T
  * volume_used:690G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793642911
* mariadb-4-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:706546
  * datadisk:1770
  * volume_size:1.8T
  * volume_used:690G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793642911

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1793642911-f9765f99f-x6kxz: 0
* bexhoma-sut-mariadb-2-1793642911-66f867bcbf-mq2t5: 0
* bexhoma-sut-mariadb-3-1793642911-5fbb6674dc-gssns: 0
* bexhoma-sut-mariadb-4-1793642911-56456f74cc-r598l: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MariaDB-2 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MariaDB-3 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MariaDB-4 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MariaDB-2 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MariaDB-3 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MariaDB-4 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection        |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| mariadb-1-1-0-1-1 |             1.00 |      8.00 |   256.00 |        4.00 |         0.00 |                          255.93 |               976820.00 |            250000.00 |                              2705.00 | 1.00 |                3.69 |
| mariadb-1-1-0-1-2 |             1.00 |      8.00 |   256.00 |        4.00 |         0.00 |                          255.93 |               976812.00 |            250000.00 |                              2737.00 | 1.00 |                3.69 |
| mariadb-1-1-0-1-3 |             1.00 |      8.00 |   256.00 |        4.00 |         0.00 |                          255.94 |               976808.00 |            250000.00 |                              2637.00 | 1.00 |                3.69 |
| mariadb-1-1-0-1-4 |             1.00 |      8.00 |   256.00 |        4.00 |         0.00 |                          255.94 |               976806.00 |            250000.00 |                              2731.00 | 1.00 |                3.69 |
| mariadb-2-1-0-1-1 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976838.00 |            125000.00 |                              2709.00 | 1.00 |                3.69 |
| mariadb-2-1-0-1-2 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.97 |               976790.00 |            125000.00 |                              2715.00 | 1.00 |                3.69 |
| mariadb-2-1-0-1-3 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976858.00 |            125000.00 |                              2719.00 | 1.00 |                3.69 |
| mariadb-2-1-0-1-4 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976837.00 |            125000.00 |                              2825.00 | 1.00 |                3.69 |
| mariadb-2-1-0-1-5 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.97 |               976803.00 |            125000.00 |                              2631.00 | 1.00 |                3.69 |
| mariadb-2-1-0-1-6 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976866.00 |            125000.00 |                              2579.00 | 1.00 |                3.69 |
| mariadb-2-1-0-1-7 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976836.00 |            125000.00 |                              2861.00 | 1.00 |                3.69 |
| mariadb-2-1-0-1-8 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.97 |               976798.00 |            125000.00 |                              2697.00 | 1.00 |                3.69 |
| mariadb-3-1-0-1-1 |             1.00 |     16.00 |   256.00 |        4.00 |         0.00 |                          255.89 |               976968.00 |            250000.00 |                              2825.00 | 1.00 |                3.68 |
| mariadb-3-1-0-1-2 |             1.00 |     16.00 |   256.00 |        4.00 |         0.00 |                          255.90 |               976938.00 |            250000.00 |                              2765.00 | 1.00 |                3.68 |
| mariadb-3-1-0-1-3 |             1.00 |     16.00 |   256.00 |        4.00 |         0.00 |                          255.90 |               976933.00 |            250000.00 |                              2807.00 | 1.00 |                3.69 |
| mariadb-3-1-0-1-4 |             1.00 |     16.00 |   256.00 |        4.00 |         0.00 |                          255.90 |               976940.00 |            250000.00 |                              2817.00 | 1.00 |                3.68 |
| mariadb-4-1-0-1-1 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976887.00 |            125000.00 |                              2745.00 | 1.00 |                3.69 |
| mariadb-4-1-0-1-2 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.95 |               976906.00 |            125000.00 |                              2829.00 | 1.00 |                3.69 |
| mariadb-4-1-0-1-3 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976888.00 |            125000.00 |                              2751.00 | 1.00 |                3.69 |
| mariadb-4-1-0-1-4 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.95 |               976917.00 |            125000.00 |                              2933.00 | 1.00 |                3.69 |
| mariadb-4-1-0-1-5 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.95 |               976908.00 |            125000.00 |                              2815.00 | 1.00 |                3.69 |
| mariadb-4-1-0-1-6 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976889.00 |            125000.00 |                              2847.00 | 1.00 |                3.69 |
| mariadb-4-1-0-1-7 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.95 |               976922.00 |            125000.00 |                              2837.00 | 1.00 |                3.69 |
| mariadb-4-1-0-1-8 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976890.00 |            125000.00 |                              2793.00 | 1.00 |                3.69 |

#### Per Run

| DBMS        |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MariaDB-1-1 |             1.00 |     32.00 |  1024.00 |        4.00 |         0.00 | 1.00 |                3.69 |                         1023.74 |               976820.00 |           1000000.00 |                              2702.50 |
| MariaDB-2-1 |             1.00 |     32.00 |  1024.00 |        8.00 |         0.00 | 1.00 |                3.69 |                         1023.72 |               976866.00 |           1000000.00 |                              2717.00 |
| MariaDB-3-1 |             1.00 |     64.00 |  1024.00 |        4.00 |         0.00 | 1.00 |                3.68 |                         1023.60 |               976968.00 |           1000000.00 |                              2803.50 |
| MariaDB-4-1 |             1.00 |     64.00 |  1024.00 |        8.00 |         0.00 | 1.00 |                3.69 |                         1023.65 |               976922.00 |           1000000.00 |                              2818.75 |

### Benchmarking

#### Per Connection

| DBMS              | phase         | job             | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------|:--------------|:----------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 | MariaDB-1       |                1 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1023.50 |               977036.00 |             499765 |                            1157.00 |               500235 |                            196991.00 |
| mariadb-2-1-1-1-1 | mariadb-2-1-1 | mariadb-2-1-1-1 | MariaDB-2       |                1 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1023.54 |               976997.00 |             499792 |                            1143.00 |               500208 |                            183551.00 |
| mariadb-3-1-1-1-1 | mariadb-3-1-1 | mariadb-3-1-1-1 | MariaDB-3       |                1 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1023.53 |               977010.00 |             500423 |                            1133.00 |               499577 |                            215167.00 |
| mariadb-4-1-1-1-1 | mariadb-4-1-1 | mariadb-4-1-1-1 | MariaDB-4       |                1 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1023.55 |               976991.00 |             499979 |                            1159.00 |               500021 |                            189439.00 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------|:--------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        64 |     1024 |               1 |           1 |            0 |                         1023.50 |               977036.00 |             499765 |                            1157.00 |               500235 |                            196991.00 |
| mariadb-2-1-1 | mariadb-2-1-1 |                1 |        64 |     1024 |               1 |           1 |            0 |                         1023.54 |               976997.00 |             499792 |                            1143.00 |               500208 |                            183551.00 |
| mariadb-3-1-1 | mariadb-3-1-1 |                1 |        64 |     1024 |               1 |           1 |            0 |                         1023.53 |               977010.00 |             500423 |                            1133.00 |               499577 |                            215167.00 |
| mariadb-4-1-1 | mariadb-4-1-1 |                1 |        64 |     1024 |               1 |           1 |            0 |                         1023.55 |               976991.00 |             499979 |                            1159.00 |               500021 |                            189439.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>

### Persistent Storage

This loads the volume used by the following runs.

```bash
bexhoma ycsb \
  -dbms MariaDB \
  -sf 1 \
  -xwl a \
  -xtb 1024 \
  -nc 2 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1 \
  -nbt 64 \
  -xnbf 1 \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rsr \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_mariadb_storage.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_mariadb_storage_summary.md" target="_blank" rel="noopener">docs_ycsb_mariadb_storage.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 3555s 
* Code: 1793645275
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '1024'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mariadb', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mariadb-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:753686
  * datadisk:1770
  * volume_size:49G
  * volume_used:1.8G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793645275
* mariadb-1-2-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:807155
  * datadisk:1770
  * volume_size:49G
  * volume_used:1.8G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793645275

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MariaDB-1-2

### Data Parameters of Reused Volumes
* MariaDB-1: DDL values of the volume: row_format=default, collation=default
* MariaDB-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1793645275-8fbc4d86b-h7rt8: 0
* bexhoma-sut-mariadb-1-1793645275-64b8bd44d8-kc99n: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection        |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| mariadb-1-1-0-1-1 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976891.00 |            125000.00 |                              4679.00 | 1.00 |                3.69 |
| mariadb-1-1-0-1-2 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976905.00 |            125000.00 |                              4931.00 | 1.00 |                3.69 |
| mariadb-1-1-0-1-3 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976895.00 |            125000.00 |                              4751.00 | 1.00 |                3.69 |
| mariadb-1-1-0-1-4 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976887.00 |            125000.00 |                              4859.00 | 1.00 |                3.69 |
| mariadb-1-1-0-1-5 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976884.00 |            125000.00 |                              4791.00 | 1.00 |                3.69 |
| mariadb-1-1-0-1-6 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.95 |               976920.00 |            125000.00 |                              4815.00 | 1.00 |                3.69 |
| mariadb-1-1-0-1-7 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976893.00 |            125000.00 |                              4687.00 | 1.00 |                3.69 |
| mariadb-1-1-0-1-8 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976894.00 |            125000.00 |                              4727.00 | 1.00 |                3.69 |

#### Per Run

| DBMS        |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MariaDB-1-1 |             1.00 |     64.00 |  1024.00 |        8.00 |         0.00 | 1.00 |                3.69 |                         1023.65 |               976920.00 |           1000000.00 |                              4780.00 |

### Benchmarking

#### Per Connection

| DBMS              | phase         | job             | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------|:--------------|:----------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 | MariaDB-1       |                1 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1023.52 |               977021.00 |             500169 |                            1168.00 |               499831 |                              3567.00 |
| mariadb-1-2-1-1-1 | mariadb-1-2-1 | mariadb-1-2-1-1 | MariaDB-1       |                2 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1023.52 |               977025.00 |             499892 |                            1183.00 |               500108 |                              3797.00 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------|:--------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        64 |     1024 |               1 |           1 |            0 |                         1023.52 |               977021.00 |             500169 |                            1168.00 |               499831 |                              3567.00 |
| mariadb-1-2-1 | mariadb-1-2-1 |                2 |        64 |     1024 |               1 |           1 |            0 |                         1023.52 |               977025.00 |             499892 |                            1183.00 |               500108 |                              3797.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>

### Scaling the Benchmarker

1 and 8 benchmarker pods (`-nbp 1,8`) and 1 and 2 rounds (`-ne 1,2`), repeated (`-nc 2`), on the loaded volume:

```bash
bexhoma ycsb \
  -dbms MariaDB \
  -sf 1 \
  -xwl a \
  -xtb 1024 \
  -nc 2 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 1 \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_mariadb_scale.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_mariadb_scale_summary.md" target="_blank" rel="noopener">docs_ycsb_mariadb_scale.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 6706s 
* Code: 1793648842
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '1024'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mariadb', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mariadb-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:808746
  * datadisk:1770
  * volume_size:49G
  * volume_used:1.8G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1793648842
* mariadb-1-1-2-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:808759
  * datadisk:1770
  * volume_size:49G
  * volume_used:1.8G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1793648842
* mariadb-1-1-3-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:808752
  * datadisk:1770
  * volume_size:49G
  * volume_used:1.8G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1793648842
* mariadb-1-1-4-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:808758
  * datadisk:1770
  * volume_size:49G
  * volume_used:1.8G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1793648842
* mariadb-1-2-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:808771
  * datadisk:1770
  * volume_size:49G
  * volume_used:1.8G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1793648842
* mariadb-1-2-2-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:808777
  * datadisk:1770
  * volume_size:49G
  * volume_used:1.8G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1793648842
* mariadb-1-2-3-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:808780
  * datadisk:1770
  * volume_size:49G
  * volume_used:1.8G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1793648842
* mariadb-1-2-4-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:808777
  * datadisk:1770
  * volume_size:49G
  * volume_used:1.8G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1793648842

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MariaDB-1

### Data Parameters of Reused Volumes
* MariaDB-1: DDL values of the volume: row_format=default, collation=default
* MariaDB-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1793648842-7f599f687b-hwmz2: 0
* bexhoma-sut-mariadb-1-1793648842-dffdd7c7c-64bfc: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: ycsb (2 pods)
* DBMS MariaDB-1 - Experiment 1 Client 3: ycsb (8 pods)
* DBMS MariaDB-1 - Experiment 1 Client 4: ycsb (16 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: ycsb (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 2: ycsb (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 3: ycsb (8 pods)
* DBMS MariaDB-1 - Experiment 2 Client 4: ycsb (16 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: ycsb (2 pods)
* DBMS MariaDB-1 - Experiment 1 Client 3: ycsb (8 pods)
* DBMS MariaDB-1 - Experiment 1 Client 4: ycsb (16 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: ycsb (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 2: ycsb (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 3: ycsb (8 pods)
* DBMS MariaDB-1 - Experiment 2 Client 4: ycsb (16 pods)

### Benchmarking

#### Per Connection

| DBMS               | phase         | job             | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------------|:--------------|:----------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mariadb-1-1-1-1-1  | mariadb-1-1-1 | mariadb-1-1-1-1 | MariaDB-1       |                1 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1023.41 |               977130.00 |             499755 |                            1177.00 |               500245 |                              3623.00 |
| mariadb-1-1-2-1-1  | mariadb-1-1-2 | mariadb-1-1-2-1 | MariaDB-1       |                1 |        2 |               1 |       1 |        64 |     1024 |           2 |            0 |                         1023.04 |               488741.00 |             249147 |                            1219.00 |               250853 |                              4179.00 |
| mariadb-1-1-2-1-2  | mariadb-1-1-2 | mariadb-1-1-2-1 | MariaDB-1       |                1 |        2 |               1 |       2 |        64 |     1024 |           2 |            0 |                         1022.97 |               488775.00 |             249843 |                            1216.00 |               250157 |                              4139.00 |
| mariadb-1-1-3-1-1  | mariadb-1-1-3 | mariadb-1-1-3-1 | MariaDB-1       |                1 |        3 |               1 |       1 |         8 |      128 |           8 |            0 |                          127.97 |               976810.00 |              62611 |                            1182.00 |                62389 |                              3741.00 |
| mariadb-1-1-3-1-2  | mariadb-1-1-3 | mariadb-1-1-3-1 | MariaDB-1       |                1 |        3 |               1 |       2 |         8 |      128 |           8 |            0 |                          127.97 |               976825.00 |              62424 |                            1200.00 |                62576 |                              3879.00 |
| mariadb-1-1-3-1-3  | mariadb-1-1-3 | mariadb-1-1-3-1 | MariaDB-1       |                1 |        3 |               1 |       3 |         8 |      128 |           8 |            0 |                          127.96 |               976850.00 |              62430 |                            1247.00 |                62570 |                              3879.00 |
| mariadb-1-1-3-1-4  | mariadb-1-1-3 | mariadb-1-1-3-1 | MariaDB-1       |                1 |        3 |               1 |       4 |         8 |      128 |           8 |            0 |                          127.96 |               976833.00 |              62687 |                            1205.00 |                62313 |                              3677.00 |
| mariadb-1-1-3-1-5  | mariadb-1-1-3 | mariadb-1-1-3-1 | MariaDB-1       |                1 |        3 |               1 |       5 |         8 |      128 |           8 |            0 |                          127.97 |               976822.00 |              62336 |                            1197.00 |                62664 |                              3929.00 |
| mariadb-1-1-3-1-6  | mariadb-1-1-3 | mariadb-1-1-3-1 | MariaDB-1       |                1 |        3 |               1 |       6 |         8 |      128 |           8 |            0 |                          127.97 |               976826.00 |              62584 |                            1189.00 |                62416 |                              3819.00 |
| mariadb-1-1-3-1-7  | mariadb-1-1-3 | mariadb-1-1-3-1 | MariaDB-1       |                1 |        3 |               1 |       7 |         8 |      128 |           8 |            0 |                          127.97 |               976827.00 |              62635 |                            1197.00 |                62365 |                              3827.00 |
| mariadb-1-1-3-1-8  | mariadb-1-1-3 | mariadb-1-1-3-1 | MariaDB-1       |                1 |        3 |               1 |       8 |         8 |      128 |           8 |            0 |                          127.96 |               976842.00 |              62714 |                            1217.00 |                62286 |                              3921.00 |
| mariadb-1-1-4-1-1  | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |       1 |         8 |      128 |          16 |            0 |                          127.92 |               488599.00 |              31331 |                            1240.00 |                31169 |                              4063.00 |
| mariadb-1-1-4-1-2  | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |       2 |         8 |      128 |          16 |            0 |                          127.92 |               488604.00 |              30974 |                            1184.00 |                31526 |                              3739.00 |
| mariadb-1-1-4-1-3  | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |       3 |         8 |      128 |          16 |            0 |                          127.92 |               488571.00 |              31190 |                            1225.00 |                31310 |                              3969.00 |
| mariadb-1-1-4-1-4  | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |       4 |         8 |      128 |          16 |            0 |                          127.92 |               488577.00 |              30981 |                            1224.00 |                31519 |                              3797.00 |
| mariadb-1-1-4-1-5  | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |       5 |         8 |      128 |          16 |            0 |                          127.92 |               488598.00 |              31153 |                            1185.00 |                31347 |                              3741.00 |
| mariadb-1-1-4-1-6  | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |       6 |         8 |      128 |          16 |            0 |                          127.92 |               488605.00 |              31158 |                            1263.00 |                31342 |                              3905.00 |
| mariadb-1-1-4-1-7  | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |       7 |         8 |      128 |          16 |            0 |                          127.92 |               488581.00 |              31100 |                            1187.00 |                31400 |                              3945.00 |
| mariadb-1-1-4-1-8  | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |       8 |         8 |      128 |          16 |            0 |                          127.92 |               488603.00 |              31141 |                            1203.00 |                31359 |                              3879.00 |
| mariadb-1-1-4-1-9  | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |       9 |         8 |      128 |          16 |            0 |                          127.91 |               488608.00 |              31406 |                            1183.00 |                31094 |                              3833.00 |
| mariadb-1-1-4-1-10 | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |      10 |         8 |      128 |          16 |            0 |                          127.92 |               488584.00 |              31170 |                            1175.00 |                31330 |                              3893.00 |
| mariadb-1-1-4-1-11 | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |      11 |         8 |      128 |          16 |            0 |                          127.92 |               488582.00 |              31253 |                            1196.00 |                31247 |                              3743.00 |
| mariadb-1-1-4-1-12 | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |      12 |         8 |      128 |          16 |            0 |                          127.91 |               488615.00 |              31132 |                            1231.00 |                31368 |                              3799.00 |
| mariadb-1-1-4-1-13 | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |      13 |         8 |      128 |          16 |            0 |                          127.92 |               488592.00 |              31202 |                            1210.00 |                31298 |                              3905.00 |
| mariadb-1-1-4-1-14 | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |      14 |         8 |      128 |          16 |            0 |                          127.93 |               488551.00 |              31144 |                            1219.00 |                31356 |                              3915.00 |
| mariadb-1-1-4-1-15 | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |      15 |         8 |      128 |          16 |            0 |                          127.92 |               488583.00 |              31316 |                            1193.00 |                31184 |                              3997.00 |
| mariadb-1-1-4-1-16 | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |      16 |         8 |      128 |          16 |            0 |                          127.92 |               488589.00 |              31204 |                            1232.00 |                31296 |                              4009.00 |
| mariadb-1-2-1-1-1  | mariadb-1-2-1 | mariadb-1-2-1-1 | MariaDB-1       |                2 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1023.30 |               977231.00 |             500238 |                            1202.00 |               499762 |                              3963.00 |
| mariadb-1-2-2-1-1  | mariadb-1-2-2 | mariadb-1-2-2-1 | MariaDB-1       |                2 |        2 |               1 |       1 |        64 |     1024 |           2 |            0 |                         1022.92 |               488797.00 |             250286 |                            1212.00 |               249714 |                              4001.00 |
| mariadb-1-2-2-1-2  | mariadb-1-2-2 | mariadb-1-2-2-1 | MariaDB-1       |                2 |        2 |               1 |       2 |        64 |     1024 |           2 |            0 |                         1023.01 |               488754.00 |             250199 |                            1199.00 |               249801 |                              3965.00 |
| mariadb-1-2-3-1-1  | mariadb-1-2-3 | mariadb-1-2-3-1 | MariaDB-1       |                2 |        3 |               1 |       1 |         8 |      128 |           8 |            0 |                          127.96 |               976881.00 |              62484 |                            1240.00 |                62516 |                              3875.00 |
| mariadb-1-2-3-1-2  | mariadb-1-2-3 | mariadb-1-2-3-1 | MariaDB-1       |                2 |        3 |               1 |       2 |         8 |      128 |           8 |            0 |                          127.95 |               976919.00 |              62796 |                            1231.00 |                62204 |                              3665.00 |
| mariadb-1-2-3-1-3  | mariadb-1-2-3 | mariadb-1-2-3-1 | MariaDB-1       |                2 |        3 |               1 |       3 |         8 |      128 |           8 |            0 |                          127.95 |               976910.00 |              62474 |                            1231.00 |                62526 |                              3647.00 |
| mariadb-1-2-3-1-4  | mariadb-1-2-3 | mariadb-1-2-3-1 | MariaDB-1       |                2 |        3 |               1 |       4 |         8 |      128 |           8 |            0 |                          127.95 |               976910.00 |              62464 |                            1310.00 |                62536 |                              3625.00 |
| mariadb-1-2-3-1-5  | mariadb-1-2-3 | mariadb-1-2-3-1 | MariaDB-1       |                2 |        3 |               1 |       5 |         8 |      128 |           8 |            0 |                          127.95 |               976913.00 |              62425 |                            1306.00 |                62575 |                              3681.00 |
| mariadb-1-2-3-1-6  | mariadb-1-2-3 | mariadb-1-2-3-1 | MariaDB-1       |                2 |        3 |               1 |       6 |         8 |      128 |           8 |            0 |                          127.96 |               976904.00 |              62445 |                            1221.00 |                62555 |                              3417.00 |
| mariadb-1-2-3-1-7  | mariadb-1-2-3 | mariadb-1-2-3-1 | MariaDB-1       |                2 |        3 |               1 |       7 |         8 |      128 |           8 |            0 |                          127.95 |               976907.00 |              62759 |                            1246.00 |                62241 |                              3811.00 |
| mariadb-1-2-3-1-8  | mariadb-1-2-3 | mariadb-1-2-3-1 | MariaDB-1       |                2 |        3 |               1 |       8 |         8 |      128 |           8 |            0 |                          127.96 |               976894.00 |              62310 |                            1221.00 |                62690 |                              3739.00 |
| mariadb-1-2-4-1-1  | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |       1 |         8 |      128 |          16 |            0 |                          127.90 |               488669.00 |              30967 |                            1240.00 |                31533 |                              4089.00 |
| mariadb-1-2-4-1-2  | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |       2 |         8 |      128 |          16 |            0 |                          127.90 |               488678.00 |              31309 |                            1235.00 |                31191 |                              3947.00 |
| mariadb-1-2-4-1-3  | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |       3 |         8 |      128 |          16 |            0 |                          127.91 |               488632.00 |              31105 |                            1241.00 |                31395 |                              4119.00 |
| mariadb-1-2-4-1-4  | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |       4 |         8 |      128 |          16 |            0 |                          127.90 |               488645.00 |              31340 |                            1233.00 |                31160 |                              4259.00 |
| mariadb-1-2-4-1-5  | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |       5 |         8 |      128 |          16 |            0 |                          127.90 |               488647.00 |              31463 |                            1255.00 |                31037 |                              4191.00 |
| mariadb-1-2-4-1-6  | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |       6 |         8 |      128 |          16 |            0 |                          127.90 |               488648.00 |              31280 |                            1229.00 |                31220 |                              4215.00 |
| mariadb-1-2-4-1-7  | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |       7 |         8 |      128 |          16 |            0 |                          127.91 |               488630.00 |              31105 |                            1245.00 |                31395 |                              4223.00 |
| mariadb-1-2-4-1-8  | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |       8 |         8 |      128 |          16 |            0 |                          127.90 |               488662.00 |              31054 |                            1192.00 |                31446 |                              4073.00 |
| mariadb-1-2-4-1-9  | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |       9 |         8 |      128 |          16 |            0 |                          127.91 |               488643.00 |              31329 |                            1224.00 |                31171 |                              4167.00 |
| mariadb-1-2-4-1-10 | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |      10 |         8 |      128 |          16 |            0 |                          127.90 |               488672.00 |              31103 |                            1258.00 |                31397 |                              4107.00 |
| mariadb-1-2-4-1-11 | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |      11 |         8 |      128 |          16 |            0 |                          127.90 |               488649.00 |              31438 |                            1248.00 |                31062 |                              4199.00 |
| mariadb-1-2-4-1-12 | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |      12 |         8 |      128 |          16 |            0 |                          127.90 |               488648.00 |              31218 |                            1238.00 |                31282 |                              4065.00 |
| mariadb-1-2-4-1-13 | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |      13 |         8 |      128 |          16 |            0 |                          127.90 |               488653.00 |              31438 |                            1213.00 |                31062 |                              4203.00 |
| mariadb-1-2-4-1-14 | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |      14 |         8 |      128 |          16 |            0 |                          127.90 |               488649.00 |              31324 |                            1241.00 |                31176 |                              4187.00 |
| mariadb-1-2-4-1-15 | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |      15 |         8 |      128 |          16 |            0 |                          127.91 |               488641.00 |              31268 |                            1256.00 |                31232 |                              4187.00 |
| mariadb-1-2-4-1-16 | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |      16 |         8 |      128 |          16 |            0 |                          127.90 |               488662.00 |              31582 |                            1234.00 |                30918 |                              4295.00 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------|:--------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        64 |     1024 |               1 |           1 |            0 |                         1023.41 |               977130.00 |             499755 |                            1177.00 |               500245 |                              3623.00 |
| mariadb-1-1-2 | mariadb-1-1-2 |                1 |       128 |     2048 |               1 |           2 |            0 |                         2046.00 |               488775.00 |             498990 |                            1219.00 |               501010 |                              4179.00 |
| mariadb-1-1-3 | mariadb-1-1-3 |                1 |        64 |     1024 |               1 |           8 |            0 |                         1023.72 |               976850.00 |             500421 |                            1247.00 |               499579 |                              3929.00 |
| mariadb-1-1-4 | mariadb-1-1-4 |                1 |       128 |     2048 |               1 |          16 |            0 |                         2046.71 |               488615.00 |             498855 |                            1263.00 |               501145 |                              4063.00 |
| mariadb-1-2-1 | mariadb-1-2-1 |                2 |        64 |     1024 |               1 |           1 |            0 |                         1023.30 |               977231.00 |             500238 |                            1202.00 |               499762 |                              3963.00 |
| mariadb-1-2-2 | mariadb-1-2-2 |                2 |       128 |     2048 |               1 |           2 |            0 |                         2045.93 |               488797.00 |             500485 |                            1212.00 |               499515 |                              4001.00 |
| mariadb-1-2-3 | mariadb-1-2-3 |                2 |        64 |     1024 |               1 |           8 |            0 |                         1023.64 |               976919.00 |             500157 |                            1310.00 |               499843 |                              3875.00 |
| mariadb-1-2-4 | mariadb-1-2-4 |                2 |       128 |     2048 |               1 |          16 |            0 |                         2046.45 |               488678.00 |             500323 |                            1258.00 |               499677 |                              4295.00 |

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MariaDB-1)
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>

### Workload E

```bash
bexhoma ycsb \
  -dbms MariaDB \
  -sf 1 \
  -xwl e \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 8 \
  -nbt 64 \
  -xnbf 1 \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_mariadb_workload_e.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_mariadb_workload_e_summary.md" target="_blank" rel="noopener">docs_ycsb_mariadb_workload_e.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 2334s 
* Code: 1793824154
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'E'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '1024'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mariadb', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mariadb-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:850944
  * datadisk:1770
  * volume_size:49G
  * volume_used:1.8G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793824154

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1793824154-6c8964577-8c49x: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: ycsb (8 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: ycsb (8 pods)

### Loading

#### Per Connection

| connection        |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| mariadb-1-1-0-1-1 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.95 |               976921.00 |            125000.00 |                              5051.00 | 1.00 |                3.69 |
| mariadb-1-1-0-1-2 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.95 |               976919.00 |            125000.00 |                              4975.00 | 1.00 |                3.69 |
| mariadb-1-1-0-1-3 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.95 |               976921.00 |            125000.00 |                              4863.00 | 1.00 |                3.69 |
| mariadb-1-1-0-1-4 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.95 |               976908.00 |            125000.00 |                              5015.00 | 1.00 |                3.69 |
| mariadb-1-1-0-1-5 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976891.00 |            125000.00 |                              4911.00 | 1.00 |                3.69 |
| mariadb-1-1-0-1-6 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.95 |               976922.00 |            125000.00 |                              4751.00 | 1.00 |                3.69 |
| mariadb-1-1-0-1-7 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976897.00 |            125000.00 |                              4983.00 | 1.00 |                3.69 |
| mariadb-1-1-0-1-8 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976896.00 |            125000.00 |                              4887.00 | 1.00 |                3.69 |

#### Per Run

| DBMS        |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MariaDB-1-1 |             1.00 |     64.00 |  1024.00 |        8.00 |         0.00 | 1.00 |                3.69 |                         1023.64 |               976922.00 |           1000000.00 |                              4929.50 |

### Benchmarking

#### Per Connection

| DBMS              | phase         | job             | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   [SCAN].Return=OK |   [SCAN].99thPercentileLatency(us) |
|:------------------|:--------------|:----------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-------------------:|-----------------------------------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 | MariaDB-1       |                1 |        1 |               1 |       1 |         8 |      128 |           8 |            0 |                          127.96 |               976854.00 |                 6200 |                              3937.00 |             118800 |                            1500.00 |
| mariadb-1-1-1-1-2 | mariadb-1-1-1 | mariadb-1-1-1-1 | MariaDB-1       |                1 |        1 |               1 |       2 |         8 |      128 |           8 |            0 |                          127.96 |               976894.00 |                 6264 |                              3695.00 |             118736 |                            1496.00 |
| mariadb-1-1-1-1-3 | mariadb-1-1-1 | mariadb-1-1-1-1 | MariaDB-1       |                1 |        1 |               1 |       3 |         8 |      128 |           8 |            0 |                          127.95 |               976929.00 |                 6192 |                              3823.00 |             118808 |                            1482.00 |
| mariadb-1-1-1-1-4 | mariadb-1-1-1 | mariadb-1-1-1-1 | MariaDB-1       |                1 |        1 |               1 |       4 |         8 |      128 |           8 |            0 |                          127.96 |               976876.00 |                 6221 |                              4371.00 |             118779 |                            1456.00 |
| mariadb-1-1-1-1-5 | mariadb-1-1-1 | mariadb-1-1-1-1 | MariaDB-1       |                1 |        1 |               1 |       5 |         8 |      128 |           8 |            0 |                          127.96 |               976842.00 |                 6463 |                              3793.00 |             118537 |                            1490.00 |
| mariadb-1-1-1-1-6 | mariadb-1-1-1 | mariadb-1-1-1-1 | MariaDB-1       |                1 |        1 |               1 |       6 |         8 |      128 |           8 |            0 |                          127.95 |               976911.00 |                 6290 |                              4143.00 |             118710 |                            1491.00 |
| mariadb-1-1-1-1-7 | mariadb-1-1-1 | mariadb-1-1-1-1 | MariaDB-1       |                1 |        1 |               1 |       7 |         8 |      128 |           8 |            0 |                          127.96 |               976905.00 |                 6248 |                              3625.00 |             118752 |                            1485.00 |
| mariadb-1-1-1-1-8 | mariadb-1-1-1 | mariadb-1-1-1-1 | MariaDB-1       |                1 |        1 |               1 |       8 |         8 |      128 |           8 |            0 |                          127.96 |               976840.00 |                 6363 |                              3959.00 |             118637 |                            1461.00 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   [SCAN].Return=OK |   [SCAN].99thPercentileLatency(us) |
|:--------------|:--------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-------------------:|-----------------------------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        64 |     1024 |               1 |           8 |            0 |                         1023.67 |               976929.00 |                50241 |                              4371.00 |             949759 |                            1500.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>

### Monitoring

```bash
bexhoma ycsb \
  -dbms MariaDB \
  -sf 1 \
  -xwl a \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_mariadb_monitoring.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_mariadb_monitoring_summary.md" target="_blank" rel="noopener">docs_ycsb_mariadb_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 2277s 
* Code: 1793656861
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '1024'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mariadb', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mariadb-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:808788
  * datadisk:1851
  * volume_size:49G
  * volume_used:1.9G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1793656861
* mariadb-1-1-2-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:808793
  * datadisk:1851
  * volume_size:49G
  * volume_used:1.9G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1793656861

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MariaDB-1

### Data Parameters of Reused Volumes
* MariaDB-1: DDL values of the volume: row_format=default, collation=default
* MariaDB-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1793656861-8554c84df5-rbtnk: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: ycsb (8 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: ycsb (8 pods)

### Benchmarking

#### Per Connection

| DBMS              | phase         | job             | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------|:--------------|:----------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 | MariaDB-1       |                1 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1023.52 |               977017.00 |             499582 |                            1186.00 |               500418 |                              3867.00 |
| mariadb-1-1-2-1-1 | mariadb-1-1-2 | mariadb-1-1-2-1 | MariaDB-1       |                1 |        2 |               1 |       1 |         8 |      128 |           8 |            0 |                          127.96 |               976892.00 |              62376 |                            1194.00 |                62624 |                              3967.00 |
| mariadb-1-1-2-1-2 | mariadb-1-1-2 | mariadb-1-1-2-1 | MariaDB-1       |                1 |        2 |               1 |       2 |         8 |      128 |           8 |            0 |                          127.96 |               976904.00 |              62565 |                            1216.00 |                62435 |                              3977.00 |
| mariadb-1-1-2-1-3 | mariadb-1-1-2 | mariadb-1-1-2-1 | MariaDB-1       |                1 |        2 |               1 |       3 |         8 |      128 |           8 |            0 |                          127.95 |               976909.00 |              62597 |                            1206.00 |                62403 |                              3793.00 |
| mariadb-1-1-2-1-4 | mariadb-1-1-2 | mariadb-1-1-2-1 | MariaDB-1       |                1 |        2 |               1 |       4 |         8 |      128 |           8 |            0 |                          127.96 |               976882.00 |              62301 |                            1220.00 |                62699 |                              3927.00 |
| mariadb-1-1-2-1-5 | mariadb-1-1-2 | mariadb-1-1-2-1 | MariaDB-1       |                1 |        2 |               1 |       5 |         8 |      128 |           8 |            0 |                          127.95 |               976911.00 |              62172 |                            1195.00 |                62828 |                              3743.00 |
| mariadb-1-1-2-1-6 | mariadb-1-1-2 | mariadb-1-1-2-1 | MariaDB-1       |                1 |        2 |               1 |       6 |         8 |      128 |           8 |            0 |                          127.96 |               976899.00 |              62628 |                            1216.00 |                62372 |                              3951.00 |
| mariadb-1-1-2-1-7 | mariadb-1-1-2 | mariadb-1-1-2-1 | MariaDB-1       |                1 |        2 |               1 |       7 |         8 |      128 |           8 |            0 |                          127.95 |               976912.00 |              62395 |                            1205.00 |                62605 |                              3999.00 |
| mariadb-1-1-2-1-8 | mariadb-1-1-2 | mariadb-1-1-2-1 | MariaDB-1       |                1 |        2 |               1 |       8 |         8 |      128 |           8 |            0 |                          127.95 |               976922.00 |              62639 |                            1243.00 |                62361 |                              3857.00 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------|:--------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        64 |     1024 |               1 |           1 |            0 |                         1023.52 |               977017.00 |             499582 |                            1186.00 |               500418 |                              3867.00 |
| mariadb-1-1-2 | mariadb-1-1-2 |                1 |        64 |     1024 |               1 |           8 |            0 |                         1023.64 |               976922.00 |             499673 |                            1243.00 |               500327 |                              3999.00 |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |       185.27 |      0.24 |           2.45 |                  2.45 |
| mariadb-1-1-2-1 |       190.56 |      0.31 |           2.45 |                  2.45 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |       325.04 |      0.73 |           0.19 |                  0.19 |
| mariadb-1-1-2-1 |       392.62 |      1.11 |           0.10 |                  0.10 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-2-1 (bexhoma-metrics-mariadb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-2-1 (bexhoma-metrics-mariadb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-2-1 (bexhoma-metrics-mariadb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-2-1 (bexhoma-metrics-mariadb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MariaDB-1)
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>


## More

* SSB on MariaDB: see [Example: SSB](Example-SSB.md).
