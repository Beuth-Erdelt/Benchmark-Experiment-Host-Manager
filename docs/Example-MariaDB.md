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
|---|---|---|---|---|
| `engine` | TPC-H | `InnoDB`, `Aria`, `MyISAM` | `InnoDB` | storage engine of all tables (for ColumnStore use -dbms MariaDBCS) |
| `histograms` | TPC-H, SSB, TPC-DS | `off`, `on` | `off` | engine-independent statistics with histograms (ANALYZE TABLE ... PERSISTENT FOR ALL, JSON_HB, a full scan per table) in initstatistics (-xis); off: plain ANALYZE TABLE, which collects none (use_stat_tables = PREFERABLY_FOR_QUERIES, MariaDB 12.3) |
| `row_format` | YCSB | `default`, `DYNAMIC`, `COMPRESSED` | `default` | InnoDB row format of usertable (default: innodb_default_row_format, DYNAMIC): COMPRESSED stores pages zlib-compressed: less I/O, more CPU |
| `collation` | YCSB | `default`, `utf8mb4_bin`, `latin1` | `default` | character set and collation of usertable (default: the database default): cost of comparing the VARCHAR(255) key (binary vs. linguistic) and bytes per character |

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
* Duration: 816s 
* Code: 1793874430
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
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
  * Benchmarking is run as [1] times the number of benchmarking pods.
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
  * disk:954350
  * datadisk:4470
  * volume_size:1.8T
  * volume_used:932G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793874430

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1793874430-7776c84f57-ms7bf: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |    1 |      159.00 |           1.00 |            1.00 |         63.00 |           86.00 |              8 |           0 |             | None           |             0 | False         |               22.64 | False               |

### Benchmarking

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| mariadb-1-1-1-1-1 | MariaDB-1       | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        354 |            0.73 |             4974.76 |           1006.78 |          -1 | mariadb-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        354 |            0.73 |             4974.76 |           1006.78 |          -1 |

#### Query Completion per Phase

| phase         |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:--------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mariadb-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   mariadb-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |               11.58 |
| TPC-DS Q2     |             3709.16 |
| TPC-DS Q3     |                5.59 |
| TPC-DS Q4     |             9379.15 |
| TPC-DS Q5     |             6725.26 |
| TPC-DS Q6     |              573.45 |
| TPC-DS Q7     |             2637.68 |
| TPC-DS Q8     |              261.40 |
| TPC-DS Q9     |             3327.16 |
| TPC-DS Q10    |               25.53 |
| TPC-DS Q11    |             6133.76 |
| TPC-DS Q12    |              191.17 |
| TPC-DS Q13    |              693.27 |
| TPC-DS Q14a+b |            41420.36 |
| TPC-DS Q15    |              123.08 |
| TPC-DS Q16    |            22251.08 |
| TPC-DS Q17    |             4505.01 |
| TPC-DS Q18    |             8763.95 |
| TPC-DS Q19    |              358.88 |
| TPC-DS Q20    |              380.64 |
| TPC-DS Q21    |             1126.57 |
| TPC-DS Q22    |            15236.61 |
| TPC-DS Q23a+b |            49381.41 |
| TPC-DS Q24a+b |             1751.53 |
| TPC-DS Q25    |              108.55 |
| TPC-DS Q26    |              612.19 |
| TPC-DS Q27    |             2567.69 |
| TPC-DS Q28    |             2565.46 |
| TPC-DS Q29    |               69.91 |
| TPC-DS Q30    |               76.55 |
| TPC-DS Q31    |              971.96 |
| TPC-DS Q32    |                7.44 |
| TPC-DS Q33    |              111.53 |
| TPC-DS Q34    |             2236.11 |
| TPC-DS Q35    |              871.70 |
| TPC-DS Q36    |             2256.78 |
| TPC-DS Q37    |             4042.19 |
| TPC-DS Q38    |             6462.52 |
| TPC-DS Q39a+b |              920.13 |
| TPC-DS Q40    |              132.50 |
| TPC-DS Q41    |              349.36 |
| TPC-DS Q42    |              163.03 |
| TPC-DS Q43    |              839.91 |
| TPC-DS Q44    |             1379.55 |
| TPC-DS Q45    |               99.77 |
| TPC-DS Q46    |             2928.77 |
| TPC-DS Q47    |            12727.05 |
| TPC-DS Q48    |              847.45 |
| TPC-DS Q49    |               84.68 |
| TPC-DS Q50    |               17.11 |
| TPC-DS Q51    |             7444.91 |
| TPC-DS Q52    |              160.45 |
| TPC-DS Q53    |              116.14 |
| TPC-DS Q54    |              859.98 |
| TPC-DS Q55    |              160.14 |
| TPC-DS Q56    |              152.72 |
| TPC-DS Q57    |             4669.23 |
| TPC-DS Q58    |             4278.91 |
| TPC-DS Q59    |             6749.45 |
| TPC-DS Q60    |              231.81 |
| TPC-DS Q61    |              268.26 |
| TPC-DS Q62    |             1284.56 |
| TPC-DS Q63    |              117.88 |
| TPC-DS Q64    |              469.43 |
| TPC-DS Q65    |             4360.88 |
| TPC-DS Q66    |              852.29 |
| TPC-DS Q67    |             5177.95 |
| TPC-DS Q68    |             2447.89 |
| TPC-DS Q69    |                2.10 |
| TPC-DS Q70    |             6720.23 |
| TPC-DS Q71    |              328.43 |
| TPC-DS Q72    |              596.06 |
| TPC-DS Q73    |             2105.05 |
| TPC-DS Q74    |             4422.77 |
| TPC-DS Q75    |             4014.99 |
| TPC-DS Q76    |              337.99 |
| TPC-DS Q77    |             5752.21 |
| TPC-DS Q78    |             4156.30 |
| TPC-DS Q79    |             2415.13 |
| TPC-DS Q80    |              384.07 |
| TPC-DS Q81    |              274.82 |
| TPC-DS Q82    |             3664.04 |
| TPC-DS Q83    |              699.66 |
| TPC-DS Q84    |               39.11 |
| TPC-DS Q85    |               96.69 |
| TPC-DS Q86    |              627.14 |
| TPC-DS Q87    |             5272.10 |
| TPC-DS Q88    |            17476.92 |
| TPC-DS Q89    |             1032.78 |
| TPC-DS Q90    |               83.92 |
| TPC-DS Q91    |               11.03 |
| TPC-DS Q92    |                4.42 |
| TPC-DS Q93    |               25.60 |
| TPC-DS Q94    |              353.83 |
| TPC-DS Q95    |              583.47 |
| TPC-DS Q96    |             2281.34 |
| TPC-DS Q97    |             4000.74 |
| TPC-DS Q98    |              699.30 |
| TPC-DS Q99    |             2981.45 |

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
* Duration: 757s 
* Code: 1793875294
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
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
  * disk:954351
  * datadisk:4478
  * volume_size:1.8T
  * volume_used:932G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793875294

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1793875294-595d8fcb6d-tsgdl: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |    1 |      161.00 |           1.00 |            1.00 |         68.00 |           83.00 |              8 |           0 |             | None           |             0 | False         |               22.36 | False               |

### Benchmarking

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| mariadb-1-1-1-1-1 | MariaDB-1       | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        296 |            0.68 |             5416.26 |           1204.05 |          -1 | mariadb-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        296 |            0.68 |             5416.26 |           1204.05 |          -1 |

#### Query Completion per Phase

| phase         |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:--------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mariadb-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   mariadb-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |               12.18 |
| TPC-DS Q2     |             4249.46 |
| TPC-DS Q3     |                7.50 |
| TPC-DS Q4     |             9135.26 |
| TPC-DS Q5     |             6778.28 |
| TPC-DS Q6     |              636.44 |
| TPC-DS Q7     |             2873.28 |
| TPC-DS Q8     |              273.67 |
| TPC-DS Q9     |             3388.60 |
| TPC-DS Q10    |               81.18 |
| TPC-DS Q11    |             6685.15 |
| TPC-DS Q12    |              190.16 |
| TPC-DS Q13    |              773.09 |
| TPC-DS Q14a+b |            40570.61 |
| TPC-DS Q15    |              120.48 |
| TPC-DS Q16    |             7688.05 |
| TPC-DS Q17    |              511.27 |
| TPC-DS Q18    |             1483.22 |
| TPC-DS Q19    |              195.72 |
| TPC-DS Q20    |              334.14 |
| TPC-DS Q21    |              873.92 |
| TPC-DS Q22    |            12948.33 |
| TPC-DS Q23a+b |            44384.67 |
| TPC-DS Q24a+b |               53.00 |
| TPC-DS Q25    |              196.34 |
| TPC-DS Q26    |              917.16 |
| TPC-DS Q27    |             2455.46 |
| TPC-DS Q28    |             2525.72 |
| TPC-DS Q29    |               39.70 |
| TPC-DS Q30    |               76.65 |
| TPC-DS Q31    |              976.14 |
| TPC-DS Q32    |                5.08 |
| TPC-DS Q33    |              117.52 |
| TPC-DS Q34    |             2381.20 |
| TPC-DS Q35    |              888.71 |
| TPC-DS Q36    |             2251.92 |
| TPC-DS Q37    |             2947.03 |
| TPC-DS Q38    |             5264.09 |
| TPC-DS Q39a+b |              939.38 |
| TPC-DS Q40    |              135.17 |
| TPC-DS Q41    |              362.07 |
| TPC-DS Q42    |              168.54 |
| TPC-DS Q43    |              763.88 |
| TPC-DS Q44    |                1.99 |
| TPC-DS Q45    |              689.95 |
| TPC-DS Q46    |             2698.33 |
| TPC-DS Q47    |            12453.07 |
| TPC-DS Q48    |              816.72 |
| TPC-DS Q49    |               92.23 |
| TPC-DS Q50    |               20.68 |
| TPC-DS Q51    |             6425.26 |
| TPC-DS Q52    |              176.90 |
| TPC-DS Q53    |               96.20 |
| TPC-DS Q54    |              907.19 |
| TPC-DS Q55    |              168.09 |
| TPC-DS Q56    |              226.17 |
| TPC-DS Q57    |             5079.23 |
| TPC-DS Q58    |             4407.07 |
| TPC-DS Q59    |             7050.59 |
| TPC-DS Q60    |              481.12 |
| TPC-DS Q61    |              267.94 |
| TPC-DS Q62    |             1309.76 |
| TPC-DS Q63    |              123.28 |
| TPC-DS Q64    |              443.49 |
| TPC-DS Q65    |             4498.91 |
| TPC-DS Q66    |              822.01 |
| TPC-DS Q67    |             5393.33 |
| TPC-DS Q68    |             2388.29 |
| TPC-DS Q69    |              282.33 |
| TPC-DS Q70    |             5948.41 |
| TPC-DS Q71    |              333.46 |
| TPC-DS Q72    |              589.23 |
| TPC-DS Q73    |             2287.34 |
| TPC-DS Q74    |             4417.39 |
| TPC-DS Q75    |             4046.70 |
| TPC-DS Q76    |              333.94 |
| TPC-DS Q77    |             4650.57 |
| TPC-DS Q78    |             4950.69 |
| TPC-DS Q79    |             2586.96 |
| TPC-DS Q80    |              459.12 |
| TPC-DS Q81    |              173.96 |
| TPC-DS Q82    |             3743.50 |
| TPC-DS Q83    |              726.57 |
| TPC-DS Q84    |               42.31 |
| TPC-DS Q85    |              129.85 |
| TPC-DS Q86    |              635.63 |
| TPC-DS Q87    |             5368.60 |
| TPC-DS Q88    |             6640.94 |
| TPC-DS Q89    |             1034.51 |
| TPC-DS Q90    |              240.23 |
| TPC-DS Q91    |                9.57 |
| TPC-DS Q92    |                3.95 |
| TPC-DS Q93    |               25.41 |
| TPC-DS Q94    |              340.30 |
| TPC-DS Q95    |              559.21 |
| TPC-DS Q96    |              478.16 |
| TPC-DS Q97    |             3988.28 |
| TPC-DS Q98    |              657.23 |
| TPC-DS Q99    |             2523.03 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |       269.76 |      3.13 |           4.10 |                  4.19 |

### Loading phase: component data generator

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |         2.85 |      0.06 |           0.01 |                  0.76 |

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |       272.64 |      1.16 |           4.37 |                  4.39 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |        17.89 |      0.35 |           0.29 |                  0.30 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (data pre-existing; series exists only while non-zero)
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
* Duration: 2307s 
* Code: 1793873688
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.
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
  * disk:944580
  * datadisk:4502
  * volume_size:49G
  * volume_used:4.4G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793873688
* mariadb-1-1-2-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:947579
  * datadisk:4502
  * volume_size:49G
  * volume_used:4.4G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793873688
* mariadb-1-1-2-1-2 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:947579
  * datadisk:4502
  * volume_size:49G
  * volume_used:4.4G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793873688
* mariadb-1-2-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:954341
  * datadisk:4503
  * volume_size:49G
  * volume_used:4.4G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793873688
* mariadb-1-2-2-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:951737
  * datadisk:4503
  * volume_size:49G
  * volume_used:4.4G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793873688
* mariadb-1-2-2-1-2 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:951737
  * datadisk:4503
  * volume_size:49G
  * volume_used:4.4G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793873688

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MariaDB-1-2

### Data Parameters of Reused Volumes
* MariaDB-1: DDL values of the volume: histograms=off
* MariaDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1793873688-6d44cbbd48-fb8n5: 0
* bexhoma-sut-mariadb-1-1793873688-7d8fd78447-bw82v: 0

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

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |    1 |      198.00 |           1.00 |            1.00 |         82.00 |          105.00 |              8 |           0 |             | None           |             0 | False         |               18.18 | False               |
| MariaDB-1-2 |                2 |    1 |      198.00 |           1.00 |            1.00 |         82.00 |          105.00 |              8 |           0 |             | None           |             0 | False         |               18.18 | True                |

### Benchmarking

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| mariadb-1-1-1-1-1 | MariaDB-1       | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        360 |            0.69 |             5293.02 |            990.00 |          -1 | mariadb-1-1-1-1-1 |
| mariadb-1-1-2-1-1 | MariaDB-1       | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               99 |                  99 |        381 |            0.72 |             5062.63 |            935.43 |          -1 | mariadb-1-1-2-1-1 |
| mariadb-1-1-2-1-2 | MariaDB-1       | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               99 |                  99 |        383 |            0.71 |             5153.04 |            930.55 |          -1 | mariadb-1-1-2-1-2 |
| mariadb-1-2-1-1-1 | MariaDB-1       | mariadb-1-2-1 | mariadb-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        342 |            0.73 |             5032.36 |           1042.11 |          -1 | mariadb-1-2-1-1-1 |
| mariadb-1-2-2-1-1 | MariaDB-1       | mariadb-1-2-2 | mariadb-1-2-2-1 |                2 |        2 |               1 |           1 | 1.00 |               99 |                  99 |        365 |            0.71 |             5170.21 |            976.44 |          -1 | mariadb-1-2-2-1-1 |
| mariadb-1-2-2-1-2 | MariaDB-1       | mariadb-1-2-2 | mariadb-1-2-2-1 |                2 |        2 |               1 |           1 | 1.00 |               99 |                  99 |        365 |            0.71 |             5141.68 |            976.44 |          -1 | mariadb-1-2-2-1-2 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        360 |            0.69 |             5293.02 |            990.00 |          -1 |
| mariadb-1-1-2 | mariadb-1-1-2 |                1 |        2 |               1 |           2 | 1.00 |              198 |                 198 |        383 |            0.71 |             5107.63 |           1861.10 |          -1 |
| mariadb-1-2-1 | mariadb-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        342 |            0.73 |             5032.36 |           1042.11 |          -1 |
| mariadb-1-2-2 | mariadb-1-2-2 |                2 |        2 |               1 |           2 | 1.00 |              198 |                 198 |        365 |            0.71 |             5155.93 |           1952.88 |          -1 |

#### Query Completion per Phase

| phase         |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:--------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mariadb-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| mariadb-1-1-2 |      2 | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | yes        |
| mariadb-1-2-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| mariadb-1-2-2 |      2 | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   mariadb-1-1-1-1-1 |   mariadb-1-1-2-1-1 |   mariadb-1-1-2-1-2 |   mariadb-1-2-1-1-1 |   mariadb-1-2-2-1-1 |   mariadb-1-2-2-1-2 |
|:--------------|--------------------:|--------------------:|--------------------:|--------------------:|--------------------:|--------------------:|
| TPC-DS Q1     |               12.21 |               13.93 |               15.35 |               28.48 |               13.03 |               13.96 |
| TPC-DS Q2     |             3845.20 |             3625.71 |             3637.00 |            12590.57 |             3936.34 |             4050.29 |
| TPC-DS Q3     |                5.52 |                7.76 |                7.74 |              237.05 |                5.23 |                4.88 |
| TPC-DS Q4     |             8917.70 |             9625.30 |             9904.03 |            10105.94 |            10190.22 |            10233.54 |
| TPC-DS Q5     |             7563.07 |             8673.96 |             9288.37 |             7911.35 |             8478.16 |             8543.11 |
| TPC-DS Q6     |              620.38 |              800.55 |              568.90 |              943.30 |              662.92 |              656.32 |
| TPC-DS Q7     |             2738.51 |             3698.66 |             3697.41 |             2752.12 |             3934.59 |             3936.18 |
| TPC-DS Q8     |              262.85 |              412.36 |              306.65 |              264.40 |              304.79 |              305.69 |
| TPC-DS Q9     |             3645.74 |             3418.79 |             3359.48 |             3316.98 |             3882.09 |             3746.26 |
| TPC-DS Q10    |               48.73 |               41.59 |               21.99 |               32.45 |               19.01 |               24.08 |
| TPC-DS Q11    |             7093.05 |             6245.17 |             6145.63 |             6298.79 |             7121.65 |             6632.17 |
| TPC-DS Q12    |              187.68 |              185.89 |              182.42 |              195.04 |              186.54 |              183.76 |
| TPC-DS Q13    |              722.66 |              766.98 |              727.36 |              728.44 |              669.78 |              709.52 |
| TPC-DS Q14a+b |            71653.43 |            51736.16 |            52411.30 |            39988.65 |            47186.16 |            44716.88 |
| TPC-DS Q15    |              125.92 |              130.06 |              116.89 |              118.63 |              121.80 |              125.92 |
| TPC-DS Q16    |             8345.55 |             8329.56 |             8469.42 |             7375.62 |             7739.87 |             8705.27 |
| TPC-DS Q17    |              517.23 |              573.35 |              466.56 |              497.90 |              484.55 |              576.28 |
| TPC-DS Q18    |             1458.24 |             1589.44 |             1583.52 |             1399.15 |             1399.00 |             1402.88 |
| TPC-DS Q19    |              177.55 |              175.26 |              169.41 |              172.41 |              173.84 |              193.01 |
| TPC-DS Q20    |              350.94 |              347.23 |              362.70 |              394.35 |              362.11 |              342.29 |
| TPC-DS Q21    |              905.72 |              853.36 |              867.42 |             2752.85 |              836.90 |              842.13 |
| TPC-DS Q22    |            14746.57 |            16233.80 |            15832.48 |            20567.11 |            14996.99 |            15516.90 |
| TPC-DS Q23a+b |            50089.00 |            58697.62 |            59547.36 |            48641.30 |            55678.43 |            57458.38 |
| TPC-DS Q24a+b |               48.78 |               51.53 |               45.22 |               48.87 |               58.04 |               45.40 |
| TPC-DS Q25    |              115.13 |              116.71 |              101.17 |              114.43 |              117.77 |               91.91 |
| TPC-DS Q26    |              606.26 |              605.70 |              593.75 |              720.62 |              676.91 |              606.47 |
| TPC-DS Q27    |             2571.62 |             3030.53 |             3002.22 |             2566.80 |             3524.91 |             3473.49 |
| TPC-DS Q28    |             2592.61 |             2561.38 |             2561.38 |             2556.16 |             2581.97 |             2788.73 |
| TPC-DS Q29    |               69.11 |               67.06 |               65.70 |               65.96 |               70.16 |              181.93 |
| TPC-DS Q30    |               28.17 |               27.98 |               25.11 |               28.16 |               42.82 |               74.92 |
| TPC-DS Q31    |             1366.32 |              991.73 |              986.72 |              988.53 |             1751.05 |             1424.63 |
| TPC-DS Q32    |               15.36 |                5.53 |                5.33 |                5.04 |                5.52 |                5.27 |
| TPC-DS Q33    |              435.47 |              137.31 |              134.08 |              136.14 |              136.08 |              118.14 |
| TPC-DS Q34    |             2313.34 |             2678.74 |             2670.45 |             2587.84 |             2920.50 |             3471.56 |
| TPC-DS Q35    |              935.74 |              832.86 |             1013.85 |              846.93 |             1017.31 |              765.09 |
| TPC-DS Q36    |             3215.90 |             3861.34 |             4206.33 |             2210.71 |             3076.15 |             3060.59 |
| TPC-DS Q37    |             4192.74 |             4635.31 |             3661.16 |             3005.04 |             3465.21 |             3362.12 |
| TPC-DS Q38    |             5490.15 |             7746.44 |             8372.97 |             5639.19 |             6674.92 |             6548.99 |
| TPC-DS Q39a+b |             2092.76 |              969.98 |              967.85 |              984.94 |             1407.91 |             1944.29 |
| TPC-DS Q40    |              133.20 |              158.05 |              126.82 |              133.24 |              133.29 |              177.38 |
| TPC-DS Q41    |              363.63 |              363.16 |              359.44 |              353.46 |              369.49 |              349.87 |
| TPC-DS Q42    |              166.70 |              164.65 |              146.44 |              164.50 |              194.37 |              159.71 |
| TPC-DS Q43    |              792.57 |              763.46 |              758.03 |              764.19 |              824.30 |              768.43 |
| TPC-DS Q44    |                1.53 |                1.36 |                1.02 |                1.24 |                1.11 |                1.23 |
| TPC-DS Q45    |              100.06 |               97.27 |               95.92 |               95.87 |               96.98 |               92.83 |
| TPC-DS Q46    |             2730.53 |             2933.51 |             4345.33 |             3560.20 |             3064.61 |             3235.59 |
| TPC-DS Q47    |            15179.13 |            16436.18 |            15688.84 |            15787.83 |            15265.81 |            15408.96 |
| TPC-DS Q48    |              873.67 |              947.36 |              836.57 |             1240.74 |              812.00 |              769.64 |
| TPC-DS Q49    |               94.86 |               84.63 |               81.10 |              284.79 |               84.60 |               79.39 |
| TPC-DS Q50    |               20.87 |               17.82 |               18.96 |               17.48 |               16.63 |               16.35 |
| TPC-DS Q51    |             7335.35 |             7875.41 |             7866.13 |             7083.63 |             7144.51 |             6687.01 |
| TPC-DS Q52    |              187.01 |              160.86 |              165.18 |              155.51 |              156.62 |              145.87 |
| TPC-DS Q53    |              105.95 |              103.66 |              105.28 |              103.95 |              103.57 |              125.55 |
| TPC-DS Q54    |              912.94 |              863.27 |              853.31 |              842.21 |              863.04 |              839.61 |
| TPC-DS Q55    |              170.03 |              157.74 |              170.91 |              158.79 |              150.69 |              155.22 |
| TPC-DS Q56    |              116.79 |              115.79 |              200.65 |              107.02 |              109.36 |              105.23 |
| TPC-DS Q57    |             4783.85 |             5660.04 |             6005.47 |             5175.57 |             4638.28 |             4628.28 |
| TPC-DS Q58    |             4412.76 |             6949.13 |             6907.75 |             4790.29 |             5126.47 |             5291.17 |
| TPC-DS Q59    |             8181.77 |             9098.57 |             8887.92 |             7304.29 |             8422.86 |             8304.75 |
| TPC-DS Q60    |              354.75 |              240.40 |              610.55 |              316.73 |              227.34 |              213.60 |
| TPC-DS Q61    |              299.37 |              288.67 |              275.47 |              287.86 |              262.85 |              260.21 |
| TPC-DS Q62    |             1293.05 |             2147.83 |             1458.06 |             1301.97 |             1349.24 |             1408.31 |
| TPC-DS Q63    |              108.32 |              222.99 |              175.25 |              108.41 |              123.69 |              180.75 |
| TPC-DS Q64    |              441.04 |              518.38 |              487.06 |              450.57 |              429.27 |              593.01 |
| TPC-DS Q65    |             5238.87 |             6880.98 |             6851.30 |             5118.62 |             6141.12 |             6127.95 |
| TPC-DS Q66    |              908.88 |              941.43 |              942.20 |             1289.45 |             1611.90 |             1317.58 |
| TPC-DS Q67    |             6951.27 |             5967.06 |             5977.07 |             6458.09 |             6658.62 |             6289.58 |
| TPC-DS Q68    |             2399.37 |             3154.95 |             3154.41 |             3410.14 |             2929.10 |             2963.04 |
| TPC-DS Q69    |              269.81 |              322.42 |              254.98 |              285.14 |              343.85 |              256.68 |
| TPC-DS Q70    |             6314.31 |             8253.03 |             8329.92 |             6464.80 |             8075.36 |             8551.48 |
| TPC-DS Q71    |              334.87 |              401.90 |              331.79 |              348.76 |              625.60 |              355.93 |
| TPC-DS Q72    |              586.38 |              619.61 |              583.30 |              601.12 |              741.10 |              580.98 |
| TPC-DS Q73    |             2116.92 |             2656.20 |             2643.01 |             2144.91 |             2630.59 |             2610.99 |
| TPC-DS Q74    |             4757.09 |             4717.66 |             4811.81 |             4761.45 |             5645.58 |             5460.05 |
| TPC-DS Q75    |             4243.01 |             4175.79 |             4232.64 |             4341.33 |             4273.95 |             4114.48 |
| TPC-DS Q76    |              341.47 |              380.91 |              781.79 |              342.97 |              333.07 |              337.89 |
| TPC-DS Q77    |             4557.05 |             5990.54 |             5830.71 |             4766.43 |             5829.28 |             5821.83 |
| TPC-DS Q78    |             4073.36 |             4306.94 |             4371.22 |             4612.22 |             4477.99 |             4426.91 |
| TPC-DS Q79    |             2459.34 |             2783.96 |             2794.56 |             2414.28 |             3079.32 |             3089.98 |
| TPC-DS Q80    |              383.81 |              512.44 |              383.13 |              382.31 |              471.87 |              471.72 |
| TPC-DS Q81    |              154.07 |              156.23 |              157.85 |              149.27 |              164.21 |              158.28 |
| TPC-DS Q82    |             3008.29 |             3684.59 |             3402.26 |             3299.82 |             3782.24 |             3780.48 |
| TPC-DS Q83    |              782.40 |              696.20 |              865.63 |              687.23 |              900.00 |              901.15 |
| TPC-DS Q84    |               39.21 |               39.40 |               41.40 |               38.48 |               56.40 |               55.01 |
| TPC-DS Q85    |               97.70 |              102.95 |               98.11 |              105.46 |               96.35 |               94.06 |
| TPC-DS Q86    |              638.32 |              815.79 |              851.90 |              628.68 |              791.35 |              785.88 |
| TPC-DS Q87    |             6170.63 |             6580.98 |             6334.77 |             5631.45 |             6482.95 |             6469.96 |
| TPC-DS Q88    |            19712.38 |            25596.42 |            25800.47 |            18723.99 |            23413.98 |            24051.24 |
| TPC-DS Q89    |             1117.10 |             1151.08 |             1143.40 |             1099.60 |             1110.53 |             1072.92 |
| TPC-DS Q90    |              243.23 |              287.01 |              249.82 |              243.69 |              245.41 |              234.47 |
| TPC-DS Q91    |               10.40 |               12.59 |               10.41 |               14.91 |               13.45 |                9.36 |
| TPC-DS Q92    |                4.78 |                4.81 |                4.67 |                4.45 |                4.40 |                5.22 |
| TPC-DS Q93    |               27.18 |               32.68 |               27.54 |               34.16 |               25.49 |               27.17 |
| TPC-DS Q94    |              141.81 |              154.12 |              150.68 |              140.10 |              136.92 |              143.07 |
| TPC-DS Q95    |              573.19 |              606.40 |              585.38 |              590.78 |              591.77 |              797.17 |
| TPC-DS Q96    |             1910.17 |             1907.76 |             1981.28 |             2279.50 |             2495.68 |             2171.15 |
| TPC-DS Q97    |             3994.38 |             4374.46 |             4685.65 |             4146.24 |             4734.05 |             4680.97 |
| TPC-DS Q98    |              673.06 |              858.55 |              974.54 |              741.38 |              661.72 |              667.72 |
| TPC-DS Q99    |             2643.62 |             2940.90 |             2523.05 |             3067.95 |             2836.92 |             2809.68 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |       256.39 |      3.71 |           3.91 |                  4.04 |
| mariadb-1-1-2-1 |       256.39 |      3.71 |           3.91 |                  4.04 |

### Loading phase: component data generator

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |
| mariadb-1-1-2-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |         2.40 |      0.05 |           0.01 |                  0.76 |
| mariadb-1-1-2-1 |         2.40 |      0.05 |           0.01 |                  0.76 |

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |       332.42 |      1.00 |           4.88 |                  4.90 |
| mariadb-1-1-2-1 |       730.47 |      2.00 |           4.35 |                  4.36 |
| mariadb-1-2-1-1 |       295.34 |      1.75 |           2.73 |                  2.74 |
| mariadb-1-2-2-1 |       637.79 |      2.00 |           3.04 |                  3.05 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |        19.17 |      0.44 |           0.30 |                  0.31 |
| mariadb-1-1-2-1 |        41.83 |      0.51 |           0.32 |                  0.32 |
| mariadb-1-2-1-1 |        20.09 |      0.04 |           0.30 |                  0.31 |
| mariadb-1-2-2-1 |        41.35 |      1.66 |           0.33 |                  0.34 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-2-1 (bexhoma-metrics-mariadb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-2-1 (bexhoma-metrics-mariadb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-2-1-1 (bexhoma-metrics-mariadb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-2-1-1 (bexhoma-metrics-mariadb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-2-2-1 (bexhoma-metrics-mariadb-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-2-2-1 (bexhoma-metrics-mariadb-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (data pre-existing; series exists only while non-zero)
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
* Duration: 826s 
* Code: 1794139955
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Ramp-up period is 2 minutes before measurements begin.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.13.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mariadb', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mariadb-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:807007
  * datadisk:1674
  * volume_size:1.8T
  * volume_used:789G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794139955

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1794139955-76b5d4969f-jlcg7: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: hammerdb (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: hammerdb (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |   16 |       58.00 |           3.00 |            0.00 |         51.00 |            4.00 |              1 |           8 |             | None           |             0 | False         |              993.10 | False               |

### Benchmarking

#### Per Connection

| DBMS              | phase         | job             |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |    TPM |   efficiency |   duration |   errors |
|:------------------|:--------------|:----------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|-------:|-------------:|-----------:|---------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |       16 |        1 |               1 |       1 | 165001 | 383789 |         0.00 |          5 |        0 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   efficiency |      NOPM |       TPM |   duration |   errors |
|:--------------|:--------------|-----------------:|---------:|---------:|----------------:|------------:|-------------:|----------:|----------:|-----------:|---------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |       16 |        1 |               1 |           1 |         0.00 | 165001.00 | 383789.00 |          5 |        0 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: NOPM contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey))
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
* Duration: 881s 
* Code: 1794140798
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Ramp-up period is 2 minutes before measurements begin.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.13.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mariadb', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mariadb-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:805272
  * datadisk:1694
  * volume_size:49G
  * volume_used:1.7G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794140798

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1794140798-6869c8fc94-9lknz: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: hammerdb (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: hammerdb (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |   16 |       75.00 |           5.00 |            0.00 |         65.00 |            5.00 |              1 |           8 |             | None           |             0 | False         |              768.00 | False               |

### Benchmarking

#### Per Connection

| DBMS              | phase         | job             |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |    TPM |   efficiency |   duration |   errors |
|:------------------|:--------------|:----------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|-------:|-------------:|-----------:|---------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |       16 |        1 |               1 |       1 |  99225 | 230446 |         0.00 |          5 |        0 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   efficiency |     NOPM |       TPM |   duration |   errors |
|:--------------|:--------------|-----------------:|---------:|---------:|----------------:|------------:|-------------:|---------:|----------:|-----------:|---------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |       16 |        1 |               1 |           1 |         0.00 | 99225.00 | 230446.00 |          5 |        0 |

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |        92.37 |      1.64 |           2.56 |                  2.57 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |       239.84 |      5.02 |           0.10 |                  0.10 |

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |      1717.30 |      4.53 |           3.30 |                  3.31 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |       657.08 |      1.68 |           0.08 |                  0.08 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: NOPM contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey))
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
* Duration: 2808s 
* Code: 1794141725
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 2 minutes. Ramp-up period is 2 minutes before measurements begin.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.13.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi.
  * Loading is tested with [8] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mariadb', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mariadb-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:805270
  * datadisk:2417
  * volume_size:49G
  * volume_used:2.4G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794141725
* mariadb-1-1-2-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:805272
  * datadisk:2876
  * volume_size:49G
  * volume_used:2.9G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794141725
* mariadb-1-1-3-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:805275
  * datadisk:3491
  * volume_size:49G
  * volume_used:3.5G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794141725
* mariadb-1-1-4-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:805277
  * datadisk:3944
  * volume_size:49G
  * volume_used:3.9G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794141725
* mariadb-1-2-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:805280
  * datadisk:4520
  * volume_size:49G
  * volume_used:4.5G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794141725
* mariadb-1-2-2-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:805099
  * datadisk:4957
  * volume_size:49G
  * volume_used:4.9G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794141725
* mariadb-1-2-3-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:805450
  * datadisk:5527
  * volume_size:49G
  * volume_used:5.4G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794141725
* mariadb-1-2-4-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:805501
  * datadisk:5920
  * volume_size:49G
  * volume_used:5.8G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794141725

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MariaDB-1

### Data Parameters of Reused Volumes
* MariaDB-1: loading values of the volume: script=Schema, indexing=Checks

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1794141725-6f59c979cd-6wkf9: 0
* bexhoma-sut-mariadb-1-1794141725-5dccfc64c5-v468k: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: hammerdb (2 pods)
* DBMS MariaDB-1 - Experiment 1 Client 3: hammerdb (2 pods)
* DBMS MariaDB-1 - Experiment 1 Client 4: hammerdb (4 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: hammerdb (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 2: hammerdb (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 3: hammerdb (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 4: hammerdb (4 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: hammerdb (2 pods)
* DBMS MariaDB-1 - Experiment 1 Client 3: hammerdb (2 pods)
* DBMS MariaDB-1 - Experiment 1 Client 4: hammerdb (4 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: hammerdb (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 2: hammerdb (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 3: hammerdb (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 4: hammerdb (4 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |   16 |       75.00 |           5.00 |            0.00 |         65.00 |            5.00 |              0 |           8 |             | None           |             0 | False         |              768.00 | True                |
| MariaDB-1-2 |                2 |   16 |       75.00 |           5.00 |            0.00 |         65.00 |            5.00 |              0 |           8 |             | None           |             0 | False         |              768.00 | True                |

### Benchmarking

#### Per Connection

| DBMS              | phase         | job             |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |    TPM |   efficiency |   duration |   errors |
|:------------------|:--------------|:----------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|-------:|-------------:|-----------:|---------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |       16 |        1 |               1 |       1 | 113682 | 264347 |         0.00 |          2 |        0 |
| mariadb-1-1-2-1-1 | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |       16 |        2 |               1 |       1 | 151453 | 352201 |         0.00 |          2 |        0 |
| mariadb-1-1-2-1-2 | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |       16 |        2 |               1 |       2 | 151446 | 352161 |         0.00 |          2 |        0 |
| mariadb-1-1-3-1-1 | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        8 |        3 |               1 |       1 | 110665 | 256934 |         0.00 |          2 |        0 |
| mariadb-1-1-3-1-2 | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        8 |        3 |               1 |       2 | 110701 | 257077 |         0.00 |          2 |        0 |
| mariadb-1-1-4-1-1 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        8 |        4 |               1 |       1 | 141212 | 327672 |         0.00 |          2 |        0 |
| mariadb-1-1-4-1-2 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        8 |        4 |               1 |       2 | 141272 | 327803 |         0.00 |          2 |        0 |
| mariadb-1-1-4-1-3 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        8 |        4 |               1 |       3 | 141356 | 327980 |         0.00 |          2 |        0 |
| mariadb-1-1-4-1-4 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        8 |        4 |               1 |       4 | 141259 | 327792 |         0.00 |          2 |        0 |
| mariadb-1-2-1-1-1 | mariadb-1-2-1 | mariadb-1-2-1-1 |                2 |       16 |        1 |               1 |       1 | 106493 | 247611 |         0.00 |          2 |        0 |
| mariadb-1-2-2-1-1 | mariadb-1-2-2 | mariadb-1-2-2-1 |                2 |       16 |        2 |               1 |       1 | 142715 | 331550 |         0.00 |          2 |        0 |
| mariadb-1-2-2-1-2 | mariadb-1-2-2 | mariadb-1-2-2-1 |                2 |       16 |        2 |               1 |       2 | 142765 | 331663 |         0.00 |          2 |        0 |
| mariadb-1-2-3-1-1 | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        8 |        3 |               1 |       1 |  97647 | 226790 |         0.00 |          2 |        0 |
| mariadb-1-2-3-1-2 | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        8 |        3 |               1 |       2 |  97463 | 226348 |         0.00 |          2 |        0 |
| mariadb-1-2-4-1-1 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        8 |        4 |               1 |       1 | 145887 | 338205 |         0.00 |          2 |        0 |
| mariadb-1-2-4-1-2 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        8 |        4 |               1 |       2 | 145894 | 338265 |         0.00 |          2 |        0 |
| mariadb-1-2-4-1-3 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        8 |        4 |               1 |       3 | 145934 | 338335 |         0.00 |          2 |        0 |
| mariadb-1-2-4-1-4 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        8 |        4 |               1 |       4 | 145907 | 338220 |         0.00 |          2 |        0 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   efficiency |      NOPM |       TPM |   duration |   errors |
|:--------------|:--------------|-----------------:|---------:|---------:|----------------:|------------:|-------------:|----------:|----------:|-----------:|---------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |       16 |        1 |               1 |           1 |         0.00 | 113682.00 | 264347.00 |          2 |        0 |
| mariadb-1-1-2 | mariadb-1-1-2 |                1 |       32 |        2 |               1 |           2 |         0.00 | 151449.50 | 352181.00 |          2 |        0 |
| mariadb-1-1-3 | mariadb-1-1-3 |                1 |       16 |        3 |               1 |           2 |         0.00 | 110683.00 | 257005.50 |          2 |        0 |
| mariadb-1-1-4 | mariadb-1-1-4 |                1 |       32 |        4 |               1 |           4 |         0.00 | 141274.75 | 327811.75 |          2 |        0 |
| mariadb-1-2-1 | mariadb-1-2-1 |                2 |       16 |        1 |               1 |           1 |         0.00 | 106493.00 | 247611.00 |          2 |        0 |
| mariadb-1-2-2 | mariadb-1-2-2 |                2 |       32 |        2 |               1 |           2 |         0.00 | 142740.00 | 331606.50 |          2 |        0 |
| mariadb-1-2-3 | mariadb-1-2-3 |                2 |       16 |        3 |               1 |           2 |         0.00 |  97555.00 | 226569.00 |          2 |        0 |
| mariadb-1-2-4 | mariadb-1-2-4 |                2 |       32 |        4 |               1 |           4 |         0.00 | 145905.50 | 338256.25 |          2 |        0 |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |       847.64 |      4.12 |           3.30 |                  3.30 |
| mariadb-1-1-2-1 |      1604.73 |      6.94 |           4.02 |                  4.02 |
| mariadb-1-1-3-1 |      1005.82 |      4.40 |           4.44 |                  4.44 |
| mariadb-1-1-4-1 |      1621.55 |      6.82 |           5.04 |                  5.05 |
| mariadb-1-2-1-1 |      1007.64 |      4.79 |           5.33 |                  5.34 |
| mariadb-1-2-2-1 |      1499.75 |      7.17 |           5.95 |                  5.95 |
| mariadb-1-2-3-1 |      1035.64 |      4.65 |           6.37 |                  6.37 |
| mariadb-1-2-4-1 |      1575.98 |      7.46 |           6.91 |                  6.91 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |       360.85 |      1.60 |           0.08 |                  0.08 |
| mariadb-1-1-2-1 |       459.24 |      2.13 |           0.08 |                  0.08 |
| mariadb-1-1-3-1 |       363.96 |      1.59 |           0.05 |                  0.05 |
| mariadb-1-1-4-1 |       435.64 |      1.97 |           0.05 |                  0.05 |
| mariadb-1-2-1-1 |       346.55 |      1.69 |           0.08 |                  0.08 |
| mariadb-1-2-2-1 |       398.65 |      1.80 |           0.08 |                  0.08 |
| mariadb-1-2-3-1 |       358.84 |      1.68 |           0.05 |                  0.05 |
| mariadb-1-2-4-1 |       460.80 |      2.03 |           0.05 |                  0.05 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-2-1 (bexhoma-metrics-mariadb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-2-1 (bexhoma-metrics-mariadb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-2-1 (bexhoma-metrics-mariadb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-2-1 (bexhoma-metrics-mariadb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-3-1 (bexhoma-metrics-mariadb-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-3-1 (bexhoma-metrics-mariadb-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-3-1 (bexhoma-metrics-mariadb-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-3-1 (bexhoma-metrics-mariadb-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-4-1 (bexhoma-metrics-mariadb-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-4-1 (bexhoma-metrics-mariadb-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-4-1 (bexhoma-metrics-mariadb-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-4-1 (bexhoma-metrics-mariadb-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-2-1-1 (bexhoma-metrics-mariadb-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-2-1-1 (bexhoma-metrics-mariadb-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-2-1-1 (bexhoma-metrics-mariadb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-2-1-1 (bexhoma-metrics-mariadb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-2-2-1 (bexhoma-metrics-mariadb-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-2-2-1 (bexhoma-metrics-mariadb-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-2-2-1 (bexhoma-metrics-mariadb-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-2-2-1 (bexhoma-metrics-mariadb-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-2-3-1 (bexhoma-metrics-mariadb-1-2-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-2-3-1 (bexhoma-metrics-mariadb-1-2-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-2-3-1 (bexhoma-metrics-mariadb-1-2-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-2-3-1 (bexhoma-metrics-mariadb-1-2-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-2-4-1 (bexhoma-metrics-mariadb-1-2-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-2-4-1 (bexhoma-metrics-mariadb-1-2-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-2-4-1 (bexhoma-metrics-mariadb-1-2-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-2-4-1 (bexhoma-metrics-mariadb-1-2-4-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MariaDB-1)
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: NOPM contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey))
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
