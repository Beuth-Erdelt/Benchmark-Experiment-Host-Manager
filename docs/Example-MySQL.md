# Example: Benchmark MySQL

This example shows how to benchmark MySQL with TPC-H, TPC-DS, Benchbase's TPC-C, HammerDB's TPC-C and YCSB.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

[MySQL](https://www.mysql.com/) is a relational DBMS. Bexhoma runs MySQL 9.7 (LTS) on a single node.
MySQL 9 has no `mysql_native_password`; `root@'%'` uses `caching_sha2_password`, whose first login needs TLS or the server's RSA key.
Bexhoma therefore creates a TLS Secret per SUT and mounts it into MySQL and the HammerDB jobs.

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. [MySQL](https://www.mysql.com/)
1. [MySQL 9.7 documentation](https://dev.mysql.com/doc/refman/9.7/en/)
1. [TPC-H](https://www.tpc.org/tpch/)
1. [TPC-DS](https://www.tpc.org/tpcds/)
1. [Benchbase Repository](https://github.com/cmu-db/benchbase/wiki/TPC-C)
1. [HammerDB](https://www.hammerdb.com/)
1. [YCSB Repository](https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload)
1. [Benchmarking cloud serving systems with YCSB](https://dl.acm.org/doi/10.1145/1807128.1807152)
1. [Orchestrating DBMS Benchmarking in the Cloud with Kubernetes](https://doi.org/10.1007/978-3-030-94437-7_6)
1. [A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools](https://doi.org/10.1007/978-3-031-68031-1_9)
1. Test script of this page: [test-docs-mysql.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-mysql.sh), [test-docs-mysql.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-mysql.ps1)


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
  -dbms MySQL \
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
  run &>$LOG_DIR/docs_tpch_mysql.log
```

This
* starts a clean instance of MySQL (`-dbms`)
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
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_mysql_summary.md" target="_blank" rel="noopener">docs_tpch_mysql.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 678s 
* Code: 1782332824
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MySQL-1-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:265547
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782332824

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MySQL-1-1 |                1 |    1 |      235.00 |           2.00 |           21.00 |         18.00 |          190.00 |              8 |           0 |             | None           |             0 | False         |               15.32 |

### Execution

#### Per Connection

|                 | configuration   | phase       | job           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod             |
|:----------------|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------|
| MySQL-1-1-1-1-1 | MySQL-1         | MySQL-1-1-1 | MySQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         52 |            1.01 |             3713.89 |           1523.08 |          -1 | MySQL-1-1-1-1-1 |

#### Per Phase

|             | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MySQL-1-1-1 | MySQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         52 |            1.01 |             3713.89 |           1523.08 |          -1 |

### Latency of Timer Execution [ms]
| Queries                                             |   MySQL-1-1-1-1-1 |
|:----------------------------------------------------|------------------:|
| Pricing Summary Report (TPC-H Q1)                   |           8498.18 |
| Minimum Cost Supplier Query (TPC-H Q2)              |            125.34 |
| Shipping Priority (TPC-H Q3)                        |           1411.44 |
| Order Priority Checking Query (TPC-H Q4)            |            469.69 |
| Local Supplier Volume (TPC-H Q5)                    |           1073.29 |
| Forecasting Revenue Change (TPC-H Q6)               |           1202.28 |
| Volume Shipping Query (TPC-H Q7)                    |            763.35 |
| National Market Share (TPC-H Q8)                    |           2860.23 |
| Product Type Profit Measure (TPC-H Q9)              |           2027.72 |
| Returned Item Reporting Query (TPC-H Q10)           |           1140.93 |
| Important Stock Identification (TPC-H Q11)          |            167.67 |
| Shipping Modes and Order Priority (TPC-H Q12)       |           1912.12 |
| Customer Distribution (TPC-H Q13)                   |           3513.30 |
| Promotion Effect Query (TPC-H Q14)                  |           1378.28 |
| Top Supplier Query (TPC-H Q15)                      |          13242.41 |
| Parts/Supplier Relationship (TPC-H Q16)             |            390.39 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |            325.20 |
| Large Volume Customer (TPC-H Q18)                   |           1705.66 |
| Discounted Revenue (TPC-H Q19)                      |            139.85 |
| Potential Part Promotion (TPC-H Q20)                |            261.68 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |           4691.05 |
| Global Sales Opportunity Query (TPC-H Q22)          |            143.28 |

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
  -dbms MySQL \
  -sf 10 \
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
  -rss 150Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_mysql_monitoring.log
```

### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_mysql_monitoring_summary.md" target="_blank" rel="noopener">docs_tpch_mysql_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=10
* Type: tpch
* Duration: 4927s 
* Code: 1782333525
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MySQL-1-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:280818
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782333525

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MySQL-1-1 |                1 |   10 |      999.00 |           3.00 |           22.00 |        174.00 |          798.00 |              8 |           0 |             | None           |             0 | False         |               36.04 |

### Execution

#### Per Connection

|                 | configuration   | phase       | job           |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod             |
|:----------------|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------|
| MySQL-1-1-1-1-1 | MySQL-1         | MySQL-1-1-1 | MySQL-1-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |        583 |           11.12 |             3302.77 |           1358.49 |          -1 | MySQL-1-1-1-1-1 |

#### Per Phase

|             | phase       |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MySQL-1-1-1 | MySQL-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |        583 |           11.12 |             3302.77 |           1358.49 |          -1 |

### Latency of Timer Execution [ms]
| Queries                                             |   MySQL-1-1-1-1-1 |
|:----------------------------------------------------|------------------:|
| Pricing Summary Report (TPC-H Q1)                   |          78397.68 |
| Minimum Cost Supplier Query (TPC-H Q2)              |           1132.37 |
| Shipping Priority (TPC-H Q3)                        |          15992.19 |
| Order Priority Checking Query (TPC-H Q4)            |           4625.08 |
| Local Supplier Volume (TPC-H Q5)                    |          13016.57 |
| Forecasting Revenue Change (TPC-H Q6)               |          11604.60 |
| Volume Shipping Query (TPC-H Q7)                    |           9224.89 |
| National Market Share (TPC-H Q8)                    |          36335.05 |
| Product Type Profit Measure (TPC-H Q9)              |          26303.56 |
| Returned Item Reporting Query (TPC-H Q10)           |          16749.76 |
| Important Stock Identification (TPC-H Q11)          |           2484.84 |
| Shipping Modes and Order Priority (TPC-H Q12)       |          18967.48 |
| Customer Distribution (TPC-H Q13)                   |          80492.53 |
| Promotion Effect Query (TPC-H Q14)                  |          15317.14 |
| Top Supplier Query (TPC-H Q15)                      |         163969.15 |
| Parts/Supplier Relationship (TPC-H Q16)             |           3084.69 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |           3258.76 |
| Large Volume Customer (TPC-H Q18)                   |          17093.37 |
| Discounted Revenue (TPC-H Q19)                      |           1373.38 |
| Potential Part Promotion (TPC-H Q20)                |           2822.47 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |          51820.62 |
| Global Sales Opportunity Query (TPC-H Q22)          |           1382.15 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |      3755.41 |      9.06 |          25.92 |                 52.97 |

### Loading phase: component data generator

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |        24.86 |      0.45 |           0.01 |                  1.14 |

### Execution phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |       568.65 |      1.02 |          26.65 |                 53.71 |

### Execution phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |        20.83 |      0.22 |           0.40 |                  0.41 |

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

### Application Metrics

Collecting application metrics for MySQL is supported.
It can be activated by `-m -mc -ma`, with the metric set `mysql` of [cluster.config](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s-cluster.config).
See [Metrics](Example-Metrics.html) for application metrics of all DBMS and benchmarks.

```bash
bexhoma tpch \
  -dbms MySQL \
  -sf 3 \
  -nlp 2 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_mysql_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_mysql_appmetrics_summary.md" target="_blank" rel="noopener">docs_tpch_mysql_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 982s 
* Code: 1792329039
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Experiment uses bexhoma version 0.11.6.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 2 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [2] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size'}, '32G')].
  * SUT requests 4 CPU and 16Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:860816
  * volume_size:1.8T
  * volume_used:841G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792329039

### SUT Container Restarts
* bexhoma-sut-mysql-1-1792329039-cc675b756-j27d5: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |    3 |      157.00 |           5.00 |            1.00 |         85.00 |           51.00 |              2 |           0 |             | None           |             0 | False         |               68.79 | False               |

### Benchmarking

#### Per Connection

| DBMS            | configuration   | phase       | job           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod             |
|:----------------|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------|
| mysql-1-1-1-1-1 | MySQL-1         | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  22 |        130 |            2.42 |             4617.93 |           1827.69 |          -1 | mysql-1-1-1-1-1 |

#### Per Phase

|             | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  22 |        130 |            2.42 |             4617.93 |           1827.69 |          -1 |

#### Query Completion per Phase

| phase       |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| mysql-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   mysql-1-1-1-1-1 |
|:----------------------------------------------------|------------------:|
| Pricing Summary Report (TPC-H Q1)                   |          19344.83 |
| Minimum Cost Supplier Query (TPC-H Q2)              |            261.48 |
| Shipping Priority (TPC-H Q3)                        |           4312.15 |
| Order Priority Checking Query (TPC-H Q4)            |           1029.26 |
| Local Supplier Volume (TPC-H Q5)                    |           2498.32 |
| Forecasting Revenue Change (TPC-H Q6)               |           2450.32 |
| Volume Shipping Query (TPC-H Q7)                    |           1889.96 |
| National Market Share (TPC-H Q8)                    |           6322.49 |
| Product Type Profit Measure (TPC-H Q9)              |           5605.84 |
| Returned Item Reporting Query (TPC-H Q10)           |           3392.17 |
| Important Stock Identification (TPC-H Q11)          |            458.71 |
| Shipping Modes and Order Priority (TPC-H Q12)       |           3991.19 |
| Customer Distribution (TPC-H Q13)                   |          14136.89 |
| Promotion Effect Query (TPC-H Q14)                  |           3076.50 |
| Top Supplier Query (TPC-H Q15)                      |          37232.33 |
| Parts/Supplier Relationship (TPC-H Q16)             |            901.65 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |            597.21 |
| Large Volume Customer (TPC-H Q18)                   |           3776.26 |
| Discounted Revenue (TPC-H Q19)                      |            311.71 |
| Potential Part Promotion (TPC-H Q20)                |            672.57 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |          10645.32 |
| Global Sales Opportunity Query (TPC-H Q22)          |            311.95 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       215.93 |      2.79 |           8.05 |                 13.56 |

### Loading phase: component data generator

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |         6.07 |      0.05 |           0.01 |                  1.36 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |        93.29 |      1.01 |           8.42 |                 13.93 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |        14.66 |      0.03 |           0.30 |                  0.30 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                             0.87 |                            0.00 |                            0.02 |                              0.00 |

#### Benchmarking phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                             1.19 |                            0.00 |                            0.02 |                              0.00 |

### Tests
* TEST passed: Loading measured in this experiment
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


## Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.
With repetitions (`-nc`), `-rsr` removes an existing volume only before the first repetition and later repetitions reuse it without loading; `-rsrp` removes it before every repetition. See [Concepts](Concepts.html).

This is a throughput test: one round with 1 stream and one with 2 parallel streams (`-ne 1,2`), repeated (`-nc 2`), so the second repetition runs on the loaded volume:

```bash
bexhoma tpch \
  -dbms MySQL \
  -sf 10 \
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
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 150Gi \
  -rsr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_mysql_storage.log
```

### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_mysql_storage_summary.md" target="_blank" rel="noopener">docs_tpch_mysql_storage.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 1241s 
    Code: 1748912641
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MySQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
MySQL-BHT-8-1-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317384432
    datadisk:8286
    volume_size:30G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748912641
MySQL-BHT-8-1-2-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317384432
    datadisk:8286
    volume_size:30G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748912641
MySQL-BHT-8-1-2-2 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317384432
    datadisk:8286
    volume_size:30G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748912641
MySQL-BHT-8-2-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317384416
    datadisk:8286
    volume_size:30G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748912641
MySQL-BHT-8-2-2-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317384420
    datadisk:8286
    volume_size:30G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748912641
MySQL-BHT-8-2-2-2 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317384420
    datadisk:8286
    volume_size:30G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748912641

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 MySQL-BHT-8-1-1-1  MySQL-BHT-8-1-2-1  MySQL-BHT-8-1-2-2  MySQL-BHT-8-2-1-1  MySQL-BHT-8-2-2-1  MySQL-BHT-8-2-2-2
Pricing Summary Report (TPC-H Q1)                                77.71              71.17             113.27              90.10              68.93              81.12
Minimum Cost Supplier Query (TPC-H Q2)                            4.07               3.44               3.64              16.93               4.26               3.92
Shipping Priority (TPC-H Q3)                                      2.18               1.87               2.57               3.00               1.75               2.78
Order Priority Checking Query (TPC-H Q4)                          1.64               1.53               3.12               3.66               1.49               2.79
Local Supplier Volume (TPC-H Q5)                                  1.87               1.74               3.57               2.56               1.77               3.41
Forecasting Revenue Change (TPC-H Q6)                             1.33               1.32               2.57               2.35               1.45               2.29
Forecasting Revenue Change (TPC-H Q7)                             1.90               2.24               3.55               2.75               1.87               2.75
National Market Share (TPC-H Q8)                                  3.18               1.92               3.07               3.26               2.51               2.98
Product Type Profit Measure (TPC-H Q9)                            1.94               1.69               2.81               2.76               1.92               2.73
Forecasting Revenue Change (TPC-H Q10)                            2.34               1.73               2.02               3.02               1.69               2.82
Important Stock Identification (TPC-H Q11)                        2.17               1.62               2.62               2.36               1.46               2.78
Shipping Modes and Order Priority (TPC-H Q12)                     2.92               1.41               3.14               2.75               1.71               2.73
Customer Distribution (TPC-H Q13)                                 2.79               1.47               2.62               2.19               1.32               2.65
Forecasting Revenue Change (TPC-H Q14)                            1.91               1.28               2.55               2.31               1.13               2.48
Top Supplier Query (TPC-H Q15)                                    4.25               2.78               4.84               5.21               3.27               4.68
Parts/Supplier Relationship (TPC-H Q16)                           2.79               1.84               3.10               2.31               2.02               3.30
Small-Quantity-Order Revenue (TPC-H Q17)                          2.13               1.24               5.14               2.00               1.73               2.81
Large Volume Customer (TPC-H Q18)                                 2.22               1.51               2.48               2.56               2.05               3.17
Discounted Revenue (TPC-H Q19)                                    2.26               1.71               2.63               2.48               2.09               2.37
Potential Part Promotion (TPC-H Q20)                              2.61               1.49               3.36               2.88               1.79               3.23
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)               3.06               1.52               3.19               3.00               1.87               3.14
Global Sales Opportunity Query (TPC-H Q22)                        2.52               1.74               2.90               2.54               2.01               2.95

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MySQL-BHT-8-1-1-1           1.0            4.0         9.0       20.0      41.0
MySQL-BHT-8-1-2-1           1.0            4.0         9.0       20.0      41.0
MySQL-BHT-8-1-2-2           1.0            4.0         9.0       20.0      41.0
MySQL-BHT-8-2-1-1           1.0            4.0         9.0       20.0      41.0
MySQL-BHT-8-2-2-1           1.0            4.0         9.0       20.0      41.0
MySQL-BHT-8-2-2-2           1.0            4.0         9.0       20.0      41.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MySQL-BHT-8-1-1-1            0.0
MySQL-BHT-8-1-2-1            0.0
MySQL-BHT-8-1-2-2            0.0
MySQL-BHT-8-2-1-1            0.0
MySQL-BHT-8-2-2-1            0.0
MySQL-BHT-8-2-2-2            0.0

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MySQL-BHT-8-1-1-1         1287048.59
MySQL-BHT-8-1-2-1         1775137.53
MySQL-BHT-8-1-2-2         1003150.78
MySQL-BHT-8-2-1-1         1034211.47
MySQL-BHT-8-2-2-1         1630827.76
MySQL-BHT-8-2-2-2         1050194.94

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                              time [s]  count  SF  Throughput@Size
DBMS            SF num_experiment num_client                                      
MySQL-BHT-8-1-1 1  1              1                  2      1   1          39600.0
MySQL-BHT-8-1-2 1  1              2                  3      2   1          52800.0
MySQL-BHT-8-2-1 1  2              1                  2      1   1          39600.0
MySQL-BHT-8-2-2 1  2              2                  3      2   1          52800.0

### Workflow

#### Actual
DBMS MySQL-BHT-8 - Pods [[1, 2], [1, 2]]

#### Planned
DBMS MySQL-BHT-8 - Pods [[1, 2], [1, 2]]

### Ingestion - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1        4.72     0.02         37.47                45.51
MySQL-BHT-8-1-2        4.72     0.02         37.47                45.51

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1           0        0           0.0                  0.0
MySQL-BHT-8-1-2           0        0           0.0                  0.0

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1        0.00     0.00         37.47                45.51
MySQL-BHT-8-1-2        1.35     0.00         37.75                45.78
MySQL-BHT-8-2-1      255.00     0.00         75.20                91.06
MySQL-BHT-8-2-2        0.00     0.02         37.46                45.29

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1        0.00      0.0           0.0                  0.0
MySQL-BHT-8-1-2        0.00      0.0           0.0                  0.0
MySQL-BHT-8-2-1        0.00      0.0           0.0                  0.0
MySQL-BHT-8-2-2        0.03      0.0           0.0                  0.0

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST failed: Ingestion Loader contains 0 or NaN in CPU [CPUs]
TEST failed: Execution SUT contains 0 or NaN in CPU [CPUs]
TEST failed: Execution Benchmarker contains 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

</details>

### RAM Disk

This loads TPC-H data into a database that is stored on a RAM disk (`-rst ramdisk`).
Make sure you have enough RAM.

```bash
bexhoma tpch \
  -dbms MySQL \
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
  run &>$LOG_DIR/docs_tpch_mysql_ramdisk.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_mysql_ramdisk_summary.md" target="_blank" rel="noopener">docs_tpch_mysql_ramdisk.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=10
* Type: tpch
* Duration: 1863s 
* Code: 1782406715
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
  * Experiment is limited to DBMS ['MySQL'].
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
* MySQL-1-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220477
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782406715

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MySQL-1-1 |                1 |   10 |      968.00 |           2.00 |           16.00 |        143.00 |          803.00 |              8 |           0 |             | None           |             0 | False         |               37.19 |

### Execution

#### Per Connection

|                 | configuration   | phase       | job           |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod             |
|:----------------|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------|
| MySQL-1-1-1-1-1 | MySQL-1         | MySQL-1-1-1 | MySQL-1-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |        586 |           11.21 |             3262.50 |           1351.54 |          -1 | MySQL-1-1-1-1-1 |

#### Per Phase

|             | phase       |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MySQL-1-1-1 | MySQL-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |        586 |           11.21 |             3262.50 |           1351.54 |          -1 |

### Latency of Timer Execution [ms]
| Queries                                             |   MySQL-1-1-1-1-1 |
|:----------------------------------------------------|------------------:|
| Pricing Summary Report (TPC-H Q1)                   |          77080.85 |
| Minimum Cost Supplier Query (TPC-H Q2)              |           1046.80 |
| Shipping Priority (TPC-H Q3)                        |          15651.20 |
| Order Priority Checking Query (TPC-H Q4)            |           4487.97 |
| Local Supplier Volume (TPC-H Q5)                    |          12609.95 |
| Forecasting Revenue Change (TPC-H Q6)               |          12032.87 |
| Volume Shipping Query (TPC-H Q7)                    |           8701.39 |
| National Market Share (TPC-H Q8)                    |          34697.33 |
| Product Type Profit Measure (TPC-H Q9)              |          24026.03 |
| Returned Item Reporting Query (TPC-H Q10)           |          16264.46 |
| Important Stock Identification (TPC-H Q11)          |           2368.88 |
| Shipping Modes and Order Priority (TPC-H Q12)       |          19935.53 |
| Customer Distribution (TPC-H Q13)                   |          78864.00 |
| Promotion Effect Query (TPC-H Q14)                  |          14272.63 |
| Top Supplier Query (TPC-H Q15)                      |         165623.67 |
| Parts/Supplier Relationship (TPC-H Q16)             |           3191.36 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |           3602.01 |
| Large Volume Customer (TPC-H Q18)                   |          19186.95 |
| Discounted Revenue (TPC-H Q19)                      |           1519.51 |
| Potential Part Promotion (TPC-H Q20)                |           3022.54 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |          58908.85 |
| Global Sales Opportunity Query (TPC-H Q22)          |           1635.99 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |      3966.62 |      9.51 |          75.54 |                 75.54 |

### Loading phase: component data generator

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |        25.07 |      0.30 |           0.03 |                  1.14 |

### Execution phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |       575.47 |      1.02 |          76.32 |                 76.32 |

### Execution phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |        22.67 |      0.48 |           0.42 |                  0.42 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio |   Queries Per Second (QPS) |   Connection Usage Ratio |   Slow Queries Rate |   InnoDB Log Waits Rate |
|:--------------|-------------------------------:|---------------------------:|-------------------------:|--------------------:|------------------------:|
| MySQL-1-1-1-1 |                           1.00 |                       1.33 |                     0.01 |                0.09 |                    0.00 |

#### Execution phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio |   Queries Per Second (QPS) |   Connection Usage Ratio |   Slow Queries Rate |   InnoDB Log Waits Rate |
|:--------------|-------------------------------:|---------------------------:|-------------------------:|--------------------:|------------------------:|
| MySQL-1-1-1-1 |                           1.00 |                       0.84 |                     0.00 |                0.03 |                    0.00 |

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


## Refresh Stream

`-xrs N` runs the TPC-H refresh functions RF1 (insert new orders) and RF2 (delete old orders) as an additional job next to the query streams, see [TPC-H](Example-TPC-H.md#refresh-stream).
For MySQL, the loader image applies RF1 with `LOAD DATA LOCAL INFILE` and RF2 with a temporary table and a `DELETE` joined to it.
Here, 3 query streams run in parallel with a refresh stream of 3 RF1+RF2 pairs.

```bash
bexhoma tpch \
  -dbms MySQL \
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
  run &>$LOG_DIR/docs_tpch_mysql_refresh.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_mysql_refresh_summary.md" target="_blank" rel="noopener">docs_tpch_mysql_refresh.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 569s 
* Code: 1793810082
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
  * Experiment is limited to DBMS ['MySQL'].
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
* mysql-1-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:888071
  * datadisk:34793
  * volume_size:1.8T
  * volume_used:868G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793810082
* mysql-1-1-1-1-2 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:888071
  * datadisk:34793
  * volume_size:1.8T
  * volume_used:868G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793810082
* mysql-1-1-1-1-3 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:888071
  * datadisk:34793
  * volume_size:1.8T
  * volume_used:868G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793810082

### SUT Container Restarts
* bexhoma-sut-mysql-1-1793810082-6d67b4d94b-qtm95: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |    1 |       74.00 |           2.00 |           22.00 |         16.00 |           29.00 |              8 |           0 |             | None           |             0 | False         |               48.65 | False               |

### Benchmarking

#### Per Connection

| DBMS            | configuration   | phase       | job           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod             |
|:----------------|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------|
| mysql-1-1-1-1-1 | MySQL-1         | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         51 |            0.83 |             4314.39 |           1552.94 |          -1 | mysql-1-1-1-1-1 |
| mysql-1-1-1-1-2 | MySQL-1         | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         49 |            0.85 |             4253.85 |           1616.33 |          -1 | mysql-1-1-1-1-2 |
| mysql-1-1-1-1-3 | MySQL-1         | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         51 |            0.84 |             4276.59 |           1552.94 |          -1 | mysql-1-1-1-1-3 |

#### Per Phase

|             | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           3 | 1.00 |               66 |                  66 |         51 |            0.84 |             4281.54 |           4658.82 |          -1 |

#### Query Completion per Phase

| phase       |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| mysql-1-1-1 |      3 | 3/3                                 | 3/3                                      | 3/3                            | 3/3                                        | 3/3                                | 3/3                                     | 3/3                                | 3/3                                | 3/3                                      | 3/3                                         | 3/3                                          | 3/3                                             | 3/3                                 | 3/3                                  | 3/3                              | 3/3                                       | 3/3                                        | 3/3                                 | 3/3                              | 3/3                                    | 3/3                                                   | 3/3                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### tpch_refresh

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   pod_count | benchmark_begin     | benchmark_end       |   benchmark_duration |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|------------:|:--------------------|:--------------------|---------------------:|
| mysql-1-1-1-2-1 | mysql-1-1-1 | mysql-1-1-1-2 |                1 |        1 |               2 |           1 | 2026-11-04 17:42:51 | 2026-11-04 17:43:00 |                    9 |

### Latency of Timer Execution [ms]
| Queries                                             |   mysql-1-1-1-1-1 |   mysql-1-1-1-1-2 |   mysql-1-1-1-1-3 |
|:----------------------------------------------------|------------------:|------------------:|------------------:|
| Pricing Summary Report (TPC-H Q1)                   |           7241.92 |           6886.24 |           7255.07 |
| Minimum Cost Supplier Query (TPC-H Q2)              |             80.55 |             78.01 |             81.09 |
| Shipping Priority (TPC-H Q3)                        |           1727.17 |           1570.48 |           1726.39 |
| Order Priority Checking Query (TPC-H Q4)            |            396.65 |            360.61 |            397.61 |
| Local Supplier Volume (TPC-H Q5)                    |           1243.33 |           1046.44 |           1243.15 |
| Forecasting Revenue Change (TPC-H Q6)               |            847.16 |            843.89 |            873.07 |
| Volume Shipping Query (TPC-H Q7)                    |            756.76 |            653.07 |            764.16 |
| National Market Share (TPC-H Q8)                    |           3229.64 |           3227.68 |           3267.49 |
| Product Type Profit Measure (TPC-H Q9)              |           2143.74 |           2173.71 |           2090.55 |
| Returned Item Reporting Query (TPC-H Q10)           |           1018.05 |           1019.56 |           1039.68 |
| Important Stock Identification (TPC-H Q11)          |            177.02 |            149.78 |            168.89 |
| Shipping Modes and Order Priority (TPC-H Q12)       |           1317.28 |           1353.53 |           1379.27 |
| Customer Distribution (TPC-H Q13)                   |           4092.78 |           3946.84 |           4138.00 |
| Promotion Effect Query (TPC-H Q14)                  |           1130.58 |           1139.02 |           1113.34 |
| Top Supplier Query (TPC-H Q15)                      |          16593.67 |          15613.32 |          16549.46 |
| Parts/Supplier Relationship (TPC-H Q16)             |            198.93 |            408.53 |            212.83 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |            266.53 |            426.90 |            269.87 |
| Large Volume Customer (TPC-H Q18)                   |           1194.86 |           1470.86 |           1193.96 |
| Discounted Revenue (TPC-H Q19)                      |             82.86 |             78.02 |             84.39 |
| Potential Part Promotion (TPC-H Q20)                |            208.48 |            230.77 |            226.13 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |           4794.50 |           3532.38 |           4869.78 |
| Global Sales Opportunity Query (TPC-H Q22)          |             88.37 |             87.30 |             84.02 |

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
'MySQL': {
    'loadData': 'mysql --local-infile {database} < {scriptname}',
    'delay_prepare': 120,
    'template': {
        'version': 'CE 8.0.36',
        'alias': 'General-C',
        'docker_alias': 'GP-C',
        'dialect': 'MySQL',
        'JDBC': {
            'driver': "com.mysql.cj.jdbc.Driver",
            'auth': ["root", "root"],
            'url': 'jdbc:mysql://{serverip}:9091/{dbname}?rewriteBatchedStatements=true',
            'jar': ['mysql-connector-j-8.0.31.jar', 'slf4j-simple-1.7.21.jar'],
            'database': 'mysql',  # placeholder — must be overwritten per experiment
        }
    },
    'logfile': '/var/log/mysqld.log',
    'datadir': '/var/lib/mysql/',
    'priceperhourdollar': 0.0,
    'monitor': {
        'sut': {
            'metrics': 'mysql',
            'blackbox': False,
        },
    },
},
```

### Deployment

* [deploymenttemplate-MySQL.yml](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-MySQL.yml): one SUT pod.
* The template sets the server options as `--key=value` arguments (e.g. `--innodb-buffer-pool-size=8G`); change them per run with `--set ...container[dbms].innodb_buffer_pool_size=32G`.
* The buffer pool of 8G fits the default pod size (`-rr 16Gi`; the namespace sets the memory limit equal to the request when `-lr` is not given). Bexhoma does not adapt it to `-rr`/`-lr`: give larger pods a larger pool with `--set`. Until 2026-10-22 the template had 96G, which was OOM-killed in a 16Gi pod as soon as the data filled it (TPC-H SF 10).
* MySQL writes temporary tables to `--tmpdir=/mysqltmp`, a tmpfs of 32Gi in RAM (volume `mysqltmp`). Large sorts and groupings need more, e.g. TPC-DS Q22 at SF 10 fails with `No space left on device`. Enlarge it per run with `--set deployment[bexhoma-deployment-mysql].volume[mysqltmp].sizeLimit=64Gi`; it counts against the memory limit (`-lr`), together with the buffer pool. `.volume[mysqltmp].medium=` moves it to the node's disk. Internal temporary tables are held in RAM only up to `temptable_max_ram` (1G) and `tmp_table_size` (16M); beyond that MySQL converts them to on-disk tables, and at larger scale factors TPC-DS Q31 then fails with `Table './mysqltmp/#sql…' doesn't exist`. Raise them per run with `--set deployment[bexhoma-deployment-mysql].container[dbms].temptable_max_ram=32G` (and likewise `tmp_table_size`, `max_heap_table_size`).
* The template sets no durability options: MySQL runs crash-safe by default (`innodb_flush_log_at_trx_commit=1`, doublewrite on); relax the benchmark per run with `--set ...container[dbms].innodb_flush_log_at_trx_commit=2`.
* `delay_prepare: 120` makes bexhoma wait 2 minutes before querying the DBMS. This accounts for InnoDB's buffer pool initialisation, which can cause a brief restart.
* `'tls': {'secret': True}` creates a CA and server certificate Secret per SUT for the server and HammerDB.

### Schema and Scripts

DDL scripts per benchmark:
- [TPC-H](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch/MySQL)
- [TPC-DS](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpcds/MySQL)
- [TPC-C](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpcc/MySQL)
- [YCSB](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/MySQL)

The `initconstraints` scripts (TPC-H, TPC-DS) add the foreign keys with `SET SESSION foreign_key_checks = 0`, as for MariaDB: with checks on, MySQL validates every row and its memory grew past 16 GB while adding lineitem->orders at TPC-H SF 1 (OOM-killed, 2026-10-21).

DDL parameters (`-xddl`, see [DDL parameters](DBMS.md#ddl-parameters--xddl)):

| Key | Benchmarks | Values | Default | Effect |
|---|---|---|---|---|
| `histograms` | TPC-H | `off`, `on` | `off` | column histograms (ANALYZE TABLE ... UPDATE HISTOGRAM, 100 buckets) on all columns except primary keys and comments, in initstatistics (-xis): selectivity of filters on columns without an index; off: plain ANALYZE TABLE (index statistics only) |
| `stats_sample_pages` | TPC-H | `default`, `100`, `1000` | `default` | pages sampled per index by ANALYZE TABLE on each table (default: innodb_stats_persistent_sample_pages, 20): plan quality vs. ANALYZE time |
| `row_format` | YCSB | `DYNAMIC`, `COMPRESSED` | `DYNAMIC` | InnoDB row format of usertable (MySQL default DYNAMIC): COMPRESSED stores pages zlib-compressed (KEY_BLOCK_SIZE 8): less I/O, more CPU, the buffer pool may hold both copies of a page |
| `collation` | YCSB | `utf8mb4_0900_ai_ci`, `utf8mb4_bin`, `latin1` | `utf8mb4_0900_ai_ci` | character set and collation of usertable: cost of comparing the VARCHAR(255) key (binary vs. linguistic) and bytes per character |

### Load Durability

With `-xld`, the durability scripts (`.sql`) run before and after the load:

* `durable`: `innodb_flush_log_at_trx_commit=1`
* `relaxed` (default): `innodb_flush_log_at_trx_commit=2` (TPC-C and YCSB: 0, log buffer 1G), key checks off (TPC-H also autocommit)
* `unsafe`: also the redo log off, doublewrite `DETECT_ONLY`

The restore returns to the startup values, which the scripts save in `bexhoma.saved_settings`.
Doublewrite cannot be switched between on and off at runtime in MySQL, so with `--set ...innodb_doublewrite=OFF` it stays off during an `-xld durable` load.

See [Load durability](DBMS.md#load-durability--xld) and [Test: Load Durability](Test-Durability.md), with results for [TPC-H durable](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_tpch_mysql_durable_summary.md), [TPC-H relaxed](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_tpch_mysql_relaxed_summary.md), [TPC-H unsafe](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_tpch_mysql_unsafe_summary.md), [TPC-DS relaxed](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_tpcds_mysql_relaxed_summary.md), [TPC-DS unsafe](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_tpcds_mysql_unsafe_summary.md), [YCSB relaxed](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_ycsb_mysql_relaxed_summary.md), [YCSB unsafe](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_ycsb_mysql_unsafe_summary.md), [HammerDB relaxed](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_hammerdb_mysql_relaxed_summary.md), [HammerDB unsafe](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_hammerdb_mysql_unsafe_summary.md), [Benchbase relaxed](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_benchbase_mysql_relaxed_summary.md), [Benchbase unsafe](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_benchbase_mysql_unsafe_summary.md).

### Reset Scripts

With `-ar`, the reset runs before each benchmarking round:

1. Statistics: `ANALYZE TABLE` (`reset-<benchmark>.sql`)
2. Persist: `reset-flush.sh`: `innodb_max_dirty_pages_pct = 0`, wait until no dirty pages are left (at most 600 s), restore the old value
3. Counters: `FLUSH STATUS` (in `reset-flush.sh`)

See [Reset scripts](DBMS.md#reset-scripts--ar) for the reset contract and [Test: Reset Scripts](Test-Reset.md) for the test runs, with results for [YCSB](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_mysql_summary.md), [Benchbase](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_benchbase_mysql_summary.md), [HammerDB](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_hammerdb_mysql_summary.md), [TPC-H](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_tpch_mysql_summary.md), [TPC-DS](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_tpcds_mysql_summary.md).


## TPC-DS

For performing the experiment we can run the [tpcds file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpcds.py).

### Power Test

```bash
bexhoma tpcds \
  -dbms MySQL \
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
  run &>$LOG_DIR/docs_tpcds_mysql.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_mysql_summary.md" target="_blank" rel="noopener">docs_tpcds_mysql.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 1204s 
* Code: 1794056742
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.13.
  * Experiment is limited to DBMS ['MySQL'].
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
* mysql-1-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:889509
  * datadisk:37612
  * volume_size:1.8T
  * volume_used:869G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794056742

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794056742-598769b998-7qsnq: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |    1 |      221.00 |           3.00 |            1.00 |         74.00 |          131.00 |              8 |           0 |             | None           |             0 | False         |               16.29 | False               |

### Benchmarking

#### Per Connection

| DBMS            | configuration   | phase       | job           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod             |
|:----------------|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------|
| mysql-1-1-1-1-1 | MySQL-1         | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        485 |            0.77 |             4769.05 |            734.85 |          -1 | mysql-1-1-1-1-1 |

#### Per Phase

|             | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        485 |            0.77 |             4769.05 |            734.85 |          -1 |

#### Query Completion per Phase

| phase       |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mysql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   mysql-1-1-1-1-1 |
|:--------------|------------------:|
| TPC-DS Q1     |             53.72 |
| TPC-DS Q2     |           3536.81 |
| TPC-DS Q3     |              9.75 |
| TPC-DS Q4     |          44276.04 |
| TPC-DS Q5     |          14974.10 |
| TPC-DS Q6     |          62675.78 |
| TPC-DS Q7     |           1542.51 |
| TPC-DS Q8     |            316.94 |
| TPC-DS Q9     |           3473.66 |
| TPC-DS Q10    |            268.29 |
| TPC-DS Q11    |          26430.74 |
| TPC-DS Q12    |            231.63 |
| TPC-DS Q13    |           1786.33 |
| TPC-DS Q14a+b |          35019.21 |
| TPC-DS Q15    |            141.35 |
| TPC-DS Q16    |            169.44 |
| TPC-DS Q17    |            913.38 |
| TPC-DS Q18    |           1574.86 |
| TPC-DS Q19    |            330.88 |
| TPC-DS Q20    |            408.30 |
| TPC-DS Q21    |           1374.36 |
| TPC-DS Q22    |           6750.05 |
| TPC-DS Q23a+b |          40156.36 |
| TPC-DS Q24a+b |           1887.95 |
| TPC-DS Q25    |            141.18 |
| TPC-DS Q26    |            491.23 |
| TPC-DS Q27    |            579.42 |
| TPC-DS Q28    |           3439.47 |
| TPC-DS Q29    |             54.20 |
| TPC-DS Q30    |            394.89 |
| TPC-DS Q31    |          10730.40 |
| TPC-DS Q32    |            246.26 |
| TPC-DS Q33    |            573.63 |
| TPC-DS Q34    |           1512.71 |
| TPC-DS Q35    |          12814.67 |
| TPC-DS Q36    |           2353.63 |
| TPC-DS Q37    |              7.01 |
| TPC-DS Q38    |           6450.34 |
| TPC-DS Q39a+b |            942.42 |
| TPC-DS Q40    |            128.47 |
| TPC-DS Q41    |           1051.13 |
| TPC-DS Q42    |             18.21 |
| TPC-DS Q43    |              2.20 |
| TPC-DS Q44    |              5.35 |
| TPC-DS Q45    |            148.17 |
| TPC-DS Q46    |           2101.18 |
| TPC-DS Q47    |           9202.59 |
| TPC-DS Q48    |            603.43 |
| TPC-DS Q49    |            112.94 |
| TPC-DS Q50    |             19.91 |
| TPC-DS Q51    |           6872.68 |
| TPC-DS Q52    |             17.85 |
| TPC-DS Q53    |            171.05 |
| TPC-DS Q54    |           2439.92 |
| TPC-DS Q55    |             11.52 |
| TPC-DS Q56    |            197.55 |
| TPC-DS Q57    |           2522.28 |
| TPC-DS Q58    |           4779.06 |
| TPC-DS Q59    |           4758.80 |
| TPC-DS Q60    |            330.20 |
| TPC-DS Q61    |              2.32 |
| TPC-DS Q62    |           2336.42 |
| TPC-DS Q63    |            180.77 |
| TPC-DS Q64    |            327.51 |
| TPC-DS Q65    |           5369.76 |
| TPC-DS Q66    |           2186.22 |
| TPC-DS Q67    |           7514.10 |
| TPC-DS Q68    |            264.15 |
| TPC-DS Q69    |            399.75 |
| TPC-DS Q70    |          10469.41 |
| TPC-DS Q71    |            373.73 |
| TPC-DS Q72    |          11442.23 |
| TPC-DS Q73    |           1119.06 |
| TPC-DS Q74    |           7894.49 |
| TPC-DS Q75    |           2423.69 |
| TPC-DS Q76    |            533.23 |
| TPC-DS Q77    |          10343.57 |
| TPC-DS Q78    |          20322.83 |
| TPC-DS Q79    |           5398.11 |
| TPC-DS Q80    |          12373.17 |
| TPC-DS Q81    |           3072.73 |
| TPC-DS Q82    |              8.09 |
| TPC-DS Q83    |            855.53 |
| TPC-DS Q84    |             72.06 |
| TPC-DS Q85    |            126.43 |
| TPC-DS Q86    |           1218.65 |
| TPC-DS Q87    |           8506.68 |
| TPC-DS Q88    |           2474.25 |
| TPC-DS Q89    |             93.21 |
| TPC-DS Q90    |            390.75 |
| TPC-DS Q91    |             15.90 |
| TPC-DS Q92    |             57.53 |
| TPC-DS Q93    |             46.67 |
| TPC-DS Q94    |            500.87 |
| TPC-DS Q95    |           4201.58 |
| TPC-DS Q96    |            142.29 |
| TPC-DS Q97    |           9542.70 |
| TPC-DS Q98    |           1335.71 |
| TPC-DS Q99    |          13457.41 |

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
  -dbms MySQL \
  -sf 3 \
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
  --set deployment[bexhoma-deployment-mysql].volume[mysqltmp].sizeLimit=64Gi \
  --set deployment[bexhoma-deployment-mysql].container[dbms].temptable_max_ram=32G \
  --set deployment[bexhoma-deployment-mysql].container[dbms].tmp_table_size=32G \
  --set deployment[bexhoma-deployment-mysql].container[dbms].max_heap_table_size=32G \
  -rr 128Gi \
  -rsr \
  -rss 150Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_mysql_monitoring.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_mysql_monitoring_summary.md" target="_blank" rel="noopener">docs_tpcds_mysql_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 2536s 
* Code: 1794055293
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.13.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 150Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'volume': 'mysqltmp', 'field': 'sizeLimit', 'target': 'volume'}, '64Gi'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'temptable_max_ram', 'target': 'container'}, '32G'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'tmp_table_size', 'target': 'container'}, '32G'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'max_heap_table_size', 'target': 'container'}, '32G')].
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* mysql-1-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:894778
  * datadisk:45123
  * volume_size:1.8T
  * volume_used:874G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem', '--temptable_max_ram=32G', '--tmp_table_size=32G', '--max_heap_table_size=32G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794055293

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794055293-7cfc797866-5ggmf: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |    3 |      553.00 |           4.00 |            1.00 |        187.00 |          352.00 |              8 |           0 |             | None           |             0 | False         |               19.53 | False               |

### Benchmarking

#### Per Connection

| DBMS            | configuration   | phase       | job           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod             |
|:----------------|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------|
| mysql-1-1-1-1-1 | MySQL-1         | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |       1495 |            2.71 |             4022.52 |            715.18 |          -1 | mysql-1-1-1-1-1 |

#### Per Phase

|             | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |       1495 |            2.71 |             4022.52 |            715.18 |          -1 |

#### Query Completion per Phase

| phase       |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mysql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   mysql-1-1-1-1-1 |
|:--------------|------------------:|
| TPC-DS Q1     |             66.89 |
| TPC-DS Q2     |          10021.20 |
| TPC-DS Q3     |             23.98 |
| TPC-DS Q4     |          79709.48 |
| TPC-DS Q5     |          28316.03 |
| TPC-DS Q6     |         242263.53 |
| TPC-DS Q7     |           4097.10 |
| TPC-DS Q8     |            927.66 |
| TPC-DS Q9     |          11616.61 |
| TPC-DS Q10    |           1250.61 |
| TPC-DS Q11    |          51059.46 |
| TPC-DS Q12    |            685.28 |
| TPC-DS Q13    |           5982.55 |
| TPC-DS Q14a+b |         164041.76 |
| TPC-DS Q15    |            475.61 |
| TPC-DS Q16    |           1098.94 |
| TPC-DS Q17    |           1361.21 |
| TPC-DS Q18    |           3643.26 |
| TPC-DS Q19    |            785.44 |
| TPC-DS Q20    |           1204.69 |
| TPC-DS Q21    |          75448.04 |
| TPC-DS Q22    |          20256.49 |
| TPC-DS Q23a+b |         110640.96 |
| TPC-DS Q24a+b |          11890.39 |
| TPC-DS Q25    |            576.96 |
| TPC-DS Q26    |            913.95 |
| TPC-DS Q27    |            993.24 |
| TPC-DS Q28    |          12142.51 |
| TPC-DS Q29    |            197.05 |
| TPC-DS Q30    |           5991.42 |
| TPC-DS Q31    |          46359.94 |
| TPC-DS Q32    |           1783.32 |
| TPC-DS Q33    |           2157.44 |
| TPC-DS Q34    |           4515.03 |
| TPC-DS Q35    |          71155.11 |
| TPC-DS Q36    |          18644.05 |
| TPC-DS Q37    |             19.71 |
| TPC-DS Q38    |          29965.70 |
| TPC-DS Q39a+b |           6624.29 |
| TPC-DS Q40    |           2275.85 |
| TPC-DS Q41    |           7782.04 |
| TPC-DS Q42    |            151.15 |
| TPC-DS Q43    |              1.83 |
| TPC-DS Q44    |           3439.12 |
| TPC-DS Q45    |            558.14 |
| TPC-DS Q46    |           5130.67 |
| TPC-DS Q47    |          25139.22 |
| TPC-DS Q48    |           6172.33 |
| TPC-DS Q49    |            983.97 |
| TPC-DS Q50    |            217.67 |
| TPC-DS Q51    |          22065.90 |
| TPC-DS Q52    |            164.04 |
| TPC-DS Q53    |            523.33 |
| TPC-DS Q54    |           6749.46 |
| TPC-DS Q55    |             26.18 |
| TPC-DS Q56    |            693.19 |
| TPC-DS Q57    |           7707.57 |
| TPC-DS Q58    |          14812.69 |
| TPC-DS Q59    |          15468.11 |
| TPC-DS Q60    |           1121.85 |
| TPC-DS Q61    |            833.09 |
| TPC-DS Q62    |           7339.94 |
| TPC-DS Q63    |            528.42 |
| TPC-DS Q64    |           1143.86 |
| TPC-DS Q65    |          17867.58 |
| TPC-DS Q66    |          10187.20 |
| TPC-DS Q67    |          22823.06 |
| TPC-DS Q68    |            816.27 |
| TPC-DS Q69    |           1315.36 |
| TPC-DS Q70    |          37425.06 |
| TPC-DS Q71    |           1247.04 |
| TPC-DS Q72    |          32622.23 |
| TPC-DS Q73    |           3867.15 |
| TPC-DS Q74    |          13488.47 |
| TPC-DS Q75    |           3920.55 |
| TPC-DS Q76    |           1221.87 |
| TPC-DS Q77    |          24977.49 |
| TPC-DS Q78    |          31294.97 |
| TPC-DS Q79    |           3432.44 |
| TPC-DS Q80    |          14787.35 |
| TPC-DS Q81    |          22932.83 |
| TPC-DS Q82    |             13.88 |
| TPC-DS Q83    |           1623.13 |
| TPC-DS Q84    |            240.39 |
| TPC-DS Q85    |            325.51 |
| TPC-DS Q86    |           3455.84 |
| TPC-DS Q87    |          19734.90 |
| TPC-DS Q88    |           8193.98 |
| TPC-DS Q89    |            182.25 |
| TPC-DS Q90    |            989.70 |
| TPC-DS Q91    |             45.41 |
| TPC-DS Q92    |             96.07 |
| TPC-DS Q93    |            124.98 |
| TPC-DS Q94    |           1122.60 |
| TPC-DS Q95    |           9557.32 |
| TPC-DS Q96    |            492.13 |
| TPC-DS Q97    |          13698.05 |
| TPC-DS Q98    |           2938.89 |
| TPC-DS Q99    |          13040.84 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       792.04 |      6.14 |           7.96 |                 14.98 |

### Loading phase: component data generator

| DBMS          | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|:-------------|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |        15.17 |      0.04 |           0.01 |                  2.54 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      1441.29 |      1.02 |          16.30 |                 23.32 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |        26.61 |      0.43 |           0.34 |                  0.35 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)

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
  -dbms MySQL \
  -sf 10 \
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
  -rss 150Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_mysql_storage.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_mysql_storage_summary.md" target="_blank" rel="noopener">docs_tpcds_mysql_storage.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=10
    Type: tpcds
    Duration: 1381s 
    Code: 1750148746
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=10) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.8.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['MySQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 100Gi.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
MySQL-BHT-8-1-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393510268
    datadisk:8289
    volume_size:100G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750148746
MySQL-BHT-8-1-2-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393510692
    datadisk:8289
    volume_size:100G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750148746
MySQL-BHT-8-1-2-2 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393510692
    datadisk:8289
    volume_size:100G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750148746
MySQL-BHT-8-2-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393512176
    datadisk:8289
    volume_size:100G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750148746
MySQL-BHT-8-2-2-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393220484
    datadisk:8289
    volume_size:100G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750148746
MySQL-BHT-8-2-2-2 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393220484
    datadisk:8289
    volume_size:100G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750148746

### Errors (failed queries)
No errors

### Warnings (result mismatch)
               MySQL-BHT-8-1-1-1  MySQL-BHT-8-1-2-1  MySQL-BHT-8-1-2-2  MySQL-BHT-8-2-1-1  MySQL-BHT-8-2-2-1  MySQL-BHT-8-2-2-2
TPC-DS Q39a+b               True               True               True               True              False               True

### Latency of Timer Execution [ms]
DBMS           MySQL-BHT-8-1-1-1  MySQL-BHT-8-1-2-1  MySQL-BHT-8-1-2-2  MySQL-BHT-8-2-1-1  MySQL-BHT-8-2-2-1  MySQL-BHT-8-2-2-2
TPC-DS Q1                  93.99              80.91              87.56             229.54              91.51              82.45
TPC-DS Q2                   9.65               8.10               7.65              18.15               7.36               7.91
TPC-DS Q3                   2.49               2.68               3.18              14.24               2.90               2.79
TPC-DS Q4                  18.67              21.01              18.71              18.88              20.74              21.40
TPC-DS Q5                  10.73              11.70              11.91              13.84              15.50              11.75
TPC-DS Q6                   2.09               2.88               3.41              21.14               2.73               2.87
TPC-DS Q7                   2.17               3.76               3.30              28.42               2.83               2.91
TPC-DS Q8                   3.91               5.85               5.75               7.36               4.98               5.28
TPC-DS Q9                   2.88               3.92               4.34              12.08               3.63               3.89
TPC-DS Q10                  3.56               5.69               5.96               7.50               5.58               6.53
TPC-DS Q11                  8.66              10.95              10.72              10.28              10.66              11.25
TPC-DS Q12                  2.60               3.63               3.35               2.71               3.02               3.15
TPC-DS Q13                  2.74               3.91               3.55              19.57               3.78               3.87
TPC-DS Q14a+b              21.01              17.50              23.73              30.14              21.51              23.72
TPC-DS Q15                  2.32               2.82               2.87               2.35               2.54               2.84
TPC-DS Q16                  2.69               3.32               3.53               3.98               2.71               2.71
TPC-DS Q17                  2.96               3.86               3.95               3.36               3.48               4.39
TPC-DS Q18                  2.69               3.66               3.74               3.01               3.13               4.14
TPC-DS Q19                  2.49               2.78               2.78               2.21               2.27               3.24
TPC-DS Q20                  2.17               3.03               2.70               2.02               2.20               2.48
TPC-DS Q21                  2.71               3.39               3.43              11.40               2.16               2.43
TPC-DS Q22                  2.32               2.87               2.35               1.90               1.76               1.97
TPC-DS Q23a+b              12.75              13.30              12.55              10.45              10.11              12.37
TPC-DS Q24a+b               8.26               9.59               8.68               7.60               6.97               7.95
TPC-DS Q25                  3.35               3.39               2.97               2.46               2.30               2.57
TPC-DS Q26                  2.36               2.37               2.50               1.94               1.94               2.29
TPC-DS Q27                  3.02               2.91               3.44               2.17               1.94               2.61
TPC-DS Q28                  3.69               3.72               4.31               3.21               3.05               3.55
TPC-DS Q29                  4.49               3.01               3.06               2.57               2.25               2.48
TPC-DS Q30                  4.68               4.73               5.06               3.58               3.26               3.06
TPC-DS Q31                  7.68               7.21               8.02               7.31               6.03               5.80
TPC-DS Q32                  2.24               2.18               2.88               1.98               1.49               1.81
TPC-DS Q33                  6.22               5.85               6.61               7.57               4.26               4.28
TPC-DS Q34                  3.50               2.73               2.92               2.50               2.00               2.35
TPC-DS Q35                  4.29               3.90               4.18               3.36               2.81               3.18
TPC-DS Q36                  3.22               2.80               3.12               2.21               2.00               2.20
TPC-DS Q37                  2.58               2.48               2.70               1.73               1.71               1.64
TPC-DS Q38                  3.14               2.88               2.77               1.91               2.77               2.79
TPC-DS Q39a+b               9.48               6.11               9.11               7.42               6.66               7.38
TPC-DS Q40                  2.86               2.59               2.96               2.14               2.21               2.58
TPC-DS Q41                  2.80               2.60               3.02               2.25               2.38               2.49
TPC-DS Q42                  2.65               2.05               2.26               2.31               1.73               2.10
TPC-DS Q43                  2.97               2.31               2.89               1.84               2.82               2.30
TPC-DS Q44                  3.03               2.84               2.82               3.55               2.86               2.62
TPC-DS Q45                  2.81               3.06               2.45               2.94               2.17               1.95
TPC-DS Q46                  2.75               3.32               3.11               2.75               2.20               2.15
TPC-DS Q47                  6.13               6.32               6.53               7.54               5.35               4.99
TPC-DS Q48                  2.64               2.81               2.46               2.91               2.04               2.02
TPC-DS Q49                  8.06               4.90               4.77               4.95               3.74               5.79
TPC-DS Q50                  3.09               2.88               3.29               3.19               2.09               2.63
TPC-DS Q51                  4.56               4.02               4.34               5.11               3.63               3.92
TPC-DS Q52                  2.54               1.98               2.29               2.47               1.65               1.70
TPC-DS Q53                  2.92               3.05               2.66               2.66               2.06               1.95
TPC-DS Q54                  4.58               3.68               4.05               3.82               3.17               3.28
TPC-DS Q55                  2.52               1.79               2.55               1.84               1.48               1.89
TPC-DS Q56                  5.00               4.45               4.72               4.69               3.85               3.99
TPC-DS Q57                  5.75               5.44               5.32               5.77               4.53               4.31
TPC-DS Q58                  5.38               4.91               4.90               8.15               3.75               3.73
TPC-DS Q59                  4.86               4.35               7.21               4.27               3.46               3.40
TPC-DS Q60                  4.62               4.87               4.33               4.00               3.50               3.91
TPC-DS Q61                  3.11               3.02               2.80               2.86               2.79               2.57
TPC-DS Q62                  3.37               3.31               3.70               8.59               2.56               2.48
TPC-DS Q63                  3.00               2.66               3.31               2.16               2.07               1.95
TPC-DS Q64                  7.05               7.23               7.41               8.12               5.85               5.78
TPC-DS Q65                  2.74               2.89               2.83               2.22               1.90               2.70
TPC-DS Q66                  5.81               5.82               5.90              22.32              10.37               5.56
TPC-DS Q67                  2.41               2.70               2.82               2.27               2.20               2.37
TPC-DS Q68                  3.09               2.73               2.61               2.44               2.29               2.90
TPC-DS Q69                  2.53               3.09               2.90               2.36               2.50               2.52
TPC-DS Q70                  3.08               5.55               2.51               2.27               2.19               2.36
TPC-DS Q71                  2.85               3.15               3.32               2.57               2.13               2.32
TPC-DS Q72                  3.32               2.42               2.74               2.37               2.20               2.77
TPC-DS Q73                  2.38               2.88               2.51               2.19               2.05               2.33
TPC-DS Q74                  5.54               5.39               4.92               8.53               4.43               4.61
TPC-DS Q75                  5.30               5.42               5.17               4.74               4.26               4.38
TPC-DS Q76                  2.79               3.07               2.80               3.18               1.99               2.22
TPC-DS Q77                  5.83               6.05               5.84               5.90               4.74               4.57
TPC-DS Q78                  4.20               4.18               4.06               4.36               3.28               3.46
TPC-DS Q79                  2.47               2.28               3.43               2.97               1.85               2.03
TPC-DS Q80                  4.35               4.08               5.06               5.22               3.54               3.84
TPC-DS Q81                  3.34               3.07               3.32               4.68               2.35               2.49
TPC-DS Q82                  2.46               1.96               2.31               2.17               1.59               1.50
TPC-DS Q83                  3.82               3.62               3.81               5.89               3.01               2.73
TPC-DS Q84                  2.28               2.36               2.45               1.82               1.54               1.64
TPC-DS Q85                  3.38               3.52               3.48               3.09               2.37               2.47
TPC-DS Q86                  2.66               3.04               2.15               3.28               1.74               1.69
TPC-DS Q87                  2.73               2.91               2.75               2.01               1.82               1.92
TPC-DS Q88                  6.07               6.06               5.47               5.06               5.53               5.68
TPC-DS Q89                  3.12               3.12               2.48               1.86               2.03               2.23
TPC-DS Q90                  2.78               2.68               2.51               1.86               1.76               1.89
TPC-DS Q91                  2.44               2.93               2.46               4.06               1.95               1.92
TPC-DS Q92                  2.25               2.40               2.34               2.17               1.61               1.56
TPC-DS Q93                  2.62               2.65               2.54               2.39               1.73               7.51
TPC-DS Q94                  2.92               2.62               2.60               2.32               1.78               2.32
TPC-DS Q95                  3.23               3.13               3.46               2.70               2.34               2.80
TPC-DS Q96                  2.33               2.14               1.99               1.34               1.89               1.78
TPC-DS Q97                  3.17               3.42               3.79               3.30               3.00               2.81
TPC-DS Q98                  2.63               2.72               2.70               1.56               2.45               2.15
TPC-DS Q99                  2.69               2.69               2.80               1.59               2.31               2.18

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MySQL-BHT-8-1-1-1           0.0           26.0        21.0      253.0     308.0
MySQL-BHT-8-1-2-1           0.0           26.0        21.0      253.0     308.0
MySQL-BHT-8-1-2-2           0.0           26.0        21.0      253.0     308.0
MySQL-BHT-8-2-1-1           0.0           26.0        21.0      253.0     308.0
MySQL-BHT-8-2-2-1           0.0           26.0        21.0      253.0     308.0
MySQL-BHT-8-2-2-2           0.0           26.0        21.0      253.0     308.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MySQL-BHT-8-1-1-1            0.0
MySQL-BHT-8-1-2-1            0.0
MySQL-BHT-8-1-2-2            0.0
MySQL-BHT-8-2-1-1            0.0
MySQL-BHT-8-2-2-1            0.0
MySQL-BHT-8-2-2-2            0.0

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MySQL-BHT-8-1-1-1         9592942.85
MySQL-BHT-8-1-2-1         9429060.52
MySQL-BHT-8-1-2-2         9236386.35
MySQL-BHT-8-2-1-1         8773386.10
MySQL-BHT-8-2-2-1        11741502.08
MySQL-BHT-8-2-2-2        10964590.31

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                time [s]  count    SF  Throughput@Size
DBMS            SF   num_experiment num_client                                        
MySQL-BHT-8-1-1 10.0 1              1                  7      1  10.0        509142.86
MySQL-BHT-8-1-2 10.0 1              2                 17      2  10.0        419294.12
MySQL-BHT-8-2-1 10.0 2              1                  4      1  10.0        891000.00
MySQL-BHT-8-2-2 10.0 2              2                  4      2  10.0       1782000.00

### Workflow

#### Actual
DBMS MySQL-BHT-8 - Pods [[1, 2], [1, 2]]

#### Planned
DBMS MySQL-BHT-8 - Pods [[1, 2], [1, 2]]

### Ingestion - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1      188.77     1.11         37.69                45.73
MySQL-BHT-8-1-2      188.77     1.11         37.69                45.73

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1           0        0           0.0                  0.0
MySQL-BHT-8-1-2           0        0           0.0                  0.0

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1        0.00     0.00         37.69                45.73
MySQL-BHT-8-1-2        1.71     0.00         37.70                45.73
MySQL-BHT-8-2-1      475.11     0.00         75.15                91.12
MySQL-BHT-8-2-2        0.00     0.02         37.47                45.41

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1        0.00      0.0           0.0                  0.0
MySQL-BHT-8-1-2        0.00      0.0           0.0                  0.0
MySQL-BHT-8-2-1        0.00      0.0           0.0                  0.0
MySQL-BHT-8-2-2        0.03      0.0           0.0                  0.0

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST failed: SQL warnings (result mismatch)
TEST passed: Workflow as planned
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST failed: Ingestion Loader contains 0 or NaN in CPU [CPUs]
TEST failed: Execution SUT contains 0 or NaN in CPU [CPUs]
TEST failed: Execution Benchmarker contains 0 or NaN in CPU [CPUs]
```

</details>


## Benchbase's TPC-C

See [Example: Benchbase](Example-Benchbase.md) for the parameters.

### Simple

```bash
bexhoma benchbase \
  -dbms MySQL \
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
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_mysql.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_mysql_summary.md" target="_blank" rel="noopener">docs_benchbase_mysql.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 945s 
* Code: 1782361781
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.10.0.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MySQL-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:267301
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782361781
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MySQL-1-1 |                1 |   16 |      340.00 |           2.00 |            0.00 |        148.00 |          190.00 |              1 |           1 |             |                |             0 | False         |              169.41 |

### Execution

#### Per Connection

| DBMS            | phase       | job           |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------|:------------|:--------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MySQL-1-1-1-1-1 | MySQL-1-1-1 | MySQL-1-1-1-1 |                1 |         160 |     8192 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                        5342.18 |                     5259.56 |         0.00 |                                                      88779.00 |                                              28617.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------|:------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MySQL-1-1-1 | MySQL-1-1-1 |                1 |         160 |     8192 |               1 |           1 |          -1 | 300.00 |            0 |                        5342.18 |                     5259.56 |         0.00 |                                                      88779.00 |                                              28617.00 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```

</details>

### Persistent Storage

The second repetition (`-nc 2`) runs on the loaded volume.

```bash
bexhoma benchbase \
  -dbms MySQL \
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
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rsr \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_mysql_storage.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_mysql_storage_summary.md" target="_blank" rel="noopener">docs_benchbase_mysql_storage.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 982s 
* Code: 1794062743
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 1 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.13.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806832
  * datadisk:34681
  * volume_size:49G
  * volume_used:34G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794062743
    * TENANT_VOL:False
* mysql-1-2-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806433
  * datadisk:35100
  * volume_size:49G
  * volume_used:35G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794062743
    * TENANT_VOL:False

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MySQL-1-2

### Data Parameters of Reused Volumes
* MySQL-1: loading values of the volume: script=Schema, indexing=Checks

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794062743-7774d54876-g6fd4: 0
* bexhoma-sut-mysql-1-1794062743-5899d78769-f8rvw: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS MySQL-1 - Experiment 2 Client 1: benchbase (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS MySQL-1 - Experiment 2 Client 1: benchbase (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |   16 |       85.00 |           5.00 |            0.00 |         75.00 |            5.00 |              1 |           1 |             |                |             0 | False         |              677.65 | False               |
| MySQL-1-2 |                2 |   16 |       85.00 |           5.00 |            0.00 |         75.00 |            5.00 |              1 |           1 |             |                |             0 | False         |              677.65 | True                |

### Benchmarking

#### Per Connection

| DBMS            | phase       | job           |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------|:------------|:--------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |         160 |     8192 |        1 |               1 |       1 |          -1 |  60.00 |            0 |                        8192.53 |                     8117.52 |         0.00 |                                                      14397.00 |                                               8124.00 |
| mysql-1-2-1-1-1 | mysql-1-2-1 | mysql-1-2-1-1 |                2 |         160 |     8192 |        1 |               1 |       1 |          -1 |  60.00 |            0 |                        8190.28 |                     8109.78 |         0.00 |                                                      16279.00 |                                               9587.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------|:------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |         160 |     8192 |               1 |           1 |          -1 |  60.00 |            0 |                        8192.53 |                     8117.52 |         0.00 |                                                      14397.00 |                                               8124.00 |
| mysql-1-2-1 | mysql-1-2-1 |                2 |         160 |     8192 |               1 |           1 |          -1 |  60.00 |            0 |                        8190.28 |                     8109.78 |         0.00 |                                                      16279.00 |                                               9587.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
```

</details>

### Monitoring

```bash
bexhoma benchbase \
  -dbms MySQL \
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
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_mysql_monitoring.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_mysql_monitoring_summary.md" target="_blank" rel="noopener">docs_benchbase_mysql_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 977s 
* Code: 1782363268
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MySQL-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:260482
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782363268
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MySQL-1-1 |                1 |   16 |      355.00 |           2.00 |            0.00 |        159.00 |          194.00 |              1 |           1 |             |                |             0 | False         |              162.25 |

### Execution

#### Per Connection

| DBMS            | phase       | job           |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------|:------------|:--------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MySQL-1-1-1-1-1 | MySQL-1-1-1 | MySQL-1-1-1-1 |                1 |         160 |     8192 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                        5472.97 |                     5384.40 |         0.00 |                                                      81681.00 |                                              29194.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------|:------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MySQL-1-1-1 | MySQL-1-1-1 |                1 |         160 |     8192 |               1 |           1 |          -1 | 300.00 |            0 |                        5472.97 |                     5384.40 |         0.00 |                                                      81681.00 |                                              29194.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |       414.07 |      7.90 |           9.58 |                 12.83 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |      1724.24 |     14.72 |           0.55 |                  0.55 |

### Execution phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |      6946.42 |     26.99 |          11.03 |                 16.00 |

### Execution phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |      5191.00 |     21.74 |           1.36 |                  1.36 |

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
  -dbms MySQL \
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
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_mysql_scale.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_mysql_scale_summary.md" target="_blank" rel="noopener">docs_benchbase_mysql_scale.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1984s 
* Code: 1794063742
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 2 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.13.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1, 2] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806436
  * datadisk:35509
  * volume_size:49G
  * volume_used:35G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794063742
    * TENANT_VOL:False
* mysql-1-1-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806437
  * datadisk:36192
  * volume_size:49G
  * volume_used:36G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794063742
    * TENANT_VOL:False
* mysql-1-1-3-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806437
  * datadisk:37564
  * volume_size:49G
  * volume_used:37G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794063742
    * TENANT_VOL:False
* mysql-1-1-4-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806477
  * datadisk:38236
  * volume_size:49G
  * volume_used:38G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794063742
    * TENANT_VOL:False
* mysql-1-2-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:812183
  * datadisk:39605
  * volume_size:49G
  * volume_used:39G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794063742
    * TENANT_VOL:False
* mysql-1-2-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:812250
  * datadisk:40593
  * volume_size:49G
  * volume_used:40G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794063742
    * TENANT_VOL:False
* mysql-1-2-3-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:812335
  * datadisk:41853
  * volume_size:49G
  * volume_used:41G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794063742
    * TENANT_VOL:False
* mysql-1-2-4-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806547
  * datadisk:42565
  * volume_size:49G
  * volume_used:42G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794063742
    * TENANT_VOL:False

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MySQL-1

### Data Parameters of Reused Volumes
* MySQL-1: loading values of the volume: script=Schema, indexing=Checks

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794063742-d655899d5-jlltd: 0
* bexhoma-sut-mysql-1-1794063742-85c7c79b4d-kb2d2: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS MySQL-1 - Experiment 1 Client 3: benchbase (2 pods)
* DBMS MySQL-1 - Experiment 1 Client 4: benchbase (4 pods)
* DBMS MySQL-1 - Experiment 2 Client 1: benchbase (1 pods)
* DBMS MySQL-1 - Experiment 2 Client 2: benchbase (2 pods)
* DBMS MySQL-1 - Experiment 2 Client 3: benchbase (2 pods)
* DBMS MySQL-1 - Experiment 2 Client 4: benchbase (4 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS MySQL-1 - Experiment 1 Client 3: benchbase (2 pods)
* DBMS MySQL-1 - Experiment 1 Client 4: benchbase (4 pods)
* DBMS MySQL-1 - Experiment 2 Client 1: benchbase (1 pods)
* DBMS MySQL-1 - Experiment 2 Client 2: benchbase (2 pods)
* DBMS MySQL-1 - Experiment 2 Client 3: benchbase (2 pods)
* DBMS MySQL-1 - Experiment 2 Client 4: benchbase (4 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |   16 |       85.00 |           5.00 |            0.00 |         75.00 |            5.00 |              0 |           1 |             |                |             0 | False         |              677.65 | True                |
| MySQL-1-2 |                2 |   16 |       85.00 |           5.00 |            0.00 |         75.00 |            5.00 |              0 |           1 |             |                |             0 | False         |              677.65 | True                |

### Benchmarking

#### Per Connection

| DBMS            | phase       | job           |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------|:------------|:--------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |         160 |     8192 |        1 |               1 |       1 |          -1 | 120.00 |            0 |                        8191.74 |                     8110.19 |         0.00 |                                                      16022.00 |                                               9500.00 |
| mysql-1-1-2-1-1 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |         160 |     8192 |        2 |               1 |       1 |          -1 | 120.00 |            0 |                        8165.72 |                     8049.73 |         0.00 |                                                      30679.00 |                                              13936.00 |
| mysql-1-1-2-1-2 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |         160 |     8192 |        2 |               1 |       2 |          -1 | 120.00 |            0 |                        8192.67 |                     8074.90 |         0.00 |                                                      30434.00 |                                              13718.00 |
| mysql-1-1-3-1-1 | mysql-1-1-3 | mysql-1-1-3-1 |                1 |          80 |     4096 |        3 |               1 |       1 |          -1 | 120.00 |            0 |                        4095.73 |                     4054.95 |         0.00 |                                                      16151.00 |                                               9066.00 |
| mysql-1-1-3-1-2 | mysql-1-1-3 | mysql-1-1-3-1 |                1 |          80 |     4096 |        3 |               1 |       2 |          -1 | 120.00 |            0 |                        4095.76 |                     4055.55 |         0.00 |                                                      16225.00 |                                               9027.00 |
| mysql-1-1-4-1-1 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |          80 |     4096 |        4 |               1 |       1 |          -1 | 120.00 |            0 |                        4000.13 |                     3937.68 |         0.00 |                                                      42761.00 |                                              19984.00 |
| mysql-1-1-4-1-2 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |          80 |     4096 |        4 |               1 |       2 |          -1 | 120.00 |            0 |                        4075.22 |                     4010.99 |         0.00 |                                                      42496.00 |                                              19617.00 |
| mysql-1-1-4-1-3 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |          80 |     4096 |        4 |               1 |       3 |          -1 | 120.00 |            0 |                        4029.27 |                     3965.83 |         0.00 |                                                      42724.00 |                                              19840.00 |
| mysql-1-1-4-1-4 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |          80 |     4096 |        4 |               1 |       4 |          -1 | 120.00 |            0 |                        3999.28 |                     3935.51 |         0.00 |                                                      42789.00 |                                              19987.00 |
| mysql-1-2-1-1-1 | mysql-1-2-1 | mysql-1-2-1-1 |                2 |         160 |     8192 |        1 |               1 |       1 |          -1 | 120.00 |            0 |                        8191.11 |                     8101.74 |         0.00 |                                                      17712.00 |                                               9672.00 |
| mysql-1-2-2-1-1 | mysql-1-2-2 | mysql-1-2-2-1 |                2 |         160 |     8192 |        2 |               1 |       1 |          -1 | 120.00 |            0 |                        7476.89 |                     7354.32 |         0.00 |                                                      47518.00 |                                              21347.00 |
| mysql-1-2-2-1-2 | mysql-1-2-2 | mysql-1-2-2-1 |                2 |         160 |     8192 |        2 |               1 |       2 |          -1 | 120.00 |            0 |                        7581.75 |                     7456.69 |         0.00 |                                                      47093.00 |                                              21055.00 |
| mysql-1-2-3-1-1 | mysql-1-2-3 | mysql-1-2-3-1 |                2 |          80 |     4096 |        3 |               1 |       1 |          -1 | 120.00 |            0 |                        4096.07 |                     4049.67 |         0.00 |                                                      17439.00 |                                               9137.00 |
| mysql-1-2-3-1-2 | mysql-1-2-3 | mysql-1-2-3-1 |                2 |          80 |     4096 |        3 |               1 |       2 |          -1 | 120.00 |            0 |                        4095.65 |                     4050.10 |         0.00 |                                                      17505.00 |                                               9162.00 |
| mysql-1-2-4-1-1 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |          80 |     4096 |        4 |               1 |       1 |          -1 | 120.00 |            0 |                        4095.76 |                     4027.08 |         0.00 |                                                      38943.00 |                                              17006.00 |
| mysql-1-2-4-1-2 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |          80 |     4096 |        4 |               1 |       2 |          -1 | 120.00 |            0 |                        4095.73 |                     4027.20 |         0.00 |                                                      38823.00 |                                              16828.00 |
| mysql-1-2-4-1-3 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |          80 |     4096 |        4 |               1 |       3 |          -1 | 120.00 |            0 |                        4095.77 |                     4026.72 |         0.00 |                                                      38890.00 |                                              16925.00 |
| mysql-1-2-4-1-4 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |          80 |     4096 |        4 |               1 |       4 |          -1 | 120.00 |            0 |                        4096.30 |                     4028.72 |         0.00 |                                                      38907.00 |                                              17012.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------|:------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |         160 |     8192 |               1 |           1 |          -1 | 120.00 |            0 |                        8191.74 |                     8110.19 |         0.00 |                                                      16022.00 |                                               9500.00 |
| mysql-1-1-2 | mysql-1-1-2 |                1 |         320 |    16384 |               1 |           2 |          -1 | 120.00 |            0 |                       16358.39 |                    16124.63 |         0.00 |                                                      30679.00 |                                              13827.00 |
| mysql-1-1-3 | mysql-1-1-3 |                1 |         160 |     8192 |               1 |           2 |          -1 | 120.00 |            0 |                        8191.49 |                     8110.49 |         0.00 |                                                      16225.00 |                                               9046.50 |
| mysql-1-1-4 | mysql-1-1-4 |                1 |         320 |    16384 |               1 |           4 |          -1 | 120.00 |            0 |                       16103.89 |                    15850.01 |         0.00 |                                                      42789.00 |                                              19857.00 |
| mysql-1-2-1 | mysql-1-2-1 |                2 |         160 |     8192 |               1 |           1 |          -1 | 120.00 |            0 |                        8191.11 |                     8101.74 |         0.00 |                                                      17712.00 |                                               9672.00 |
| mysql-1-2-2 | mysql-1-2-2 |                2 |         320 |    16384 |               1 |           2 |          -1 | 120.00 |            0 |                       15058.64 |                    14811.01 |         0.00 |                                                      47518.00 |                                              21201.00 |
| mysql-1-2-3 | mysql-1-2-3 |                2 |         160 |     8192 |               1 |           2 |          -1 | 120.00 |            0 |                        8191.71 |                     8099.77 |         0.00 |                                                      17505.00 |                                               9149.50 |
| mysql-1-2-4 | mysql-1-2-4 |                2 |         320 |    16384 |               1 |           4 |          -1 | 120.00 |            0 |                       16383.55 |                    16109.71 |         0.00 |                                                      38943.00 |                                              16942.75 |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      1443.99 |     13.53 |           5.85 |                  8.21 |
| mysql-1-1-2-1 |      2672.84 |     28.19 |           7.50 |                 13.92 |
| mysql-1-1-3-1 |      1273.62 |     12.89 |           8.43 |                 17.86 |
| mysql-1-1-4-1 |      2802.09 |     30.50 |           9.76 |                 23.43 |
| mysql-1-2-1-1 |      1652.65 |     15.40 |           7.59 |                 10.13 |
| mysql-1-2-2-1 |      3168.05 |     31.51 |           9.89 |                 16.74 |
| mysql-1-2-3-1 |      1677.23 |     14.59 |          10.91 |                 20.66 |
| mysql-1-2-4-1 |      3703.97 |     31.16 |          12.55 |                 27.14 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      1205.44 |     12.28 |           1.43 |                  1.43 |
| mysql-1-1-2-1 |      1624.34 |     21.87 |           1.57 |                  1.57 |
| mysql-1-1-3-1 |      1097.18 |     15.53 |           1.31 |                  1.31 |
| mysql-1-1-4-1 |      2528.81 |     21.74 |           1.08 |                  1.08 |
| mysql-1-2-1-1 |      1239.97 |     12.45 |           1.87 |                  1.87 |
| mysql-1-2-2-1 |      2264.94 |     26.46 |           1.49 |                  1.49 |
| mysql-1-2-3-1 |      1370.28 |     12.73 |           1.09 |                  1.09 |
| mysql-1-2-4-1 |      2017.65 |     21.09 |           0.96 |                  0.96 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-3-1 (bexhoma-metrics-mysql-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-3-1 (bexhoma-metrics-mysql-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-3-1 (bexhoma-metrics-mysql-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-3-1 (bexhoma-metrics-mysql-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-4-1 (bexhoma-metrics-mysql-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-4-1 (bexhoma-metrics-mysql-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-4-1 (bexhoma-metrics-mysql-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-4-1 (bexhoma-metrics-mysql-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-2-1-1 (bexhoma-metrics-mysql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-2-1-1 (bexhoma-metrics-mysql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-2-1-1 (bexhoma-metrics-mysql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-2-1-1 (bexhoma-metrics-mysql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-2-2-1 (bexhoma-metrics-mysql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-2-2-1 (bexhoma-metrics-mysql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-2-2-1 (bexhoma-metrics-mysql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-2-2-1 (bexhoma-metrics-mysql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-2-3-1 (bexhoma-metrics-mysql-1-2-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-2-3-1 (bexhoma-metrics-mysql-1-2-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-2-3-1 (bexhoma-metrics-mysql-1-2-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-2-3-1 (bexhoma-metrics-mysql-1-2-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-2-4-1 (bexhoma-metrics-mysql-1-2-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-2-4-1 (bexhoma-metrics-mysql-1-2-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-2-4-1 (bexhoma-metrics-mysql-1-2-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-2-4-1 (bexhoma-metrics-mysql-1-2-4-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MySQL-1)
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
```

</details>


## HammerDB's TPC-C

See [Example: HammerDB](Example-HammerDB.md) for the parameters.

### Simple

```bash
bexhoma hammerdb \
  -dbms MySQL \
  -sf 16 \
  -nlt 8 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 16 \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hammerdb_mysql.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hammerdb_mysql_summary.md" target="_blank" rel="noopener">docs_hammerdb_mysql.log</a></summary>

```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 1347s 
* Code: 1782626077
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.10.2.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * Database uses ephemeral storage of size 16Gi.
  * Loading is tested with [8] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MySQL-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:1077381271552
  * Cores:256
  * host:6.8.0-111-generic
  * node:cl-worker27
  * disk:1407972
  * cpu_list:0-255
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782626077

### SUT Container Restarts
* bexhoma-sut-mysql-1-1782626077-58dcb6d95-bkq4d: 0 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: hammerdb (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: hammerdb (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MySQL-1-1 |                1 |   16 |      257.00 |          14.00 |            0.00 |         85.00 |          158.00 |              1 |           8 |             | None           |             0 | False         |              224.12 |

### Execution

#### Per Connection

| DBMS            | phase       | job           |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |    TPM |   efficiency |   duration |   errors |
|:----------------|:------------|:--------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|-------:|-------------:|-----------:|---------:|
| MySQL-1-1-1-1-1 | MySQL-1-1-1 | MySQL-1-1-1-1 |                1 |       16 |        1 |               1 |       1 | 181106 | 421095 |         0.00 |          5 |        0 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   efficiency |      NOPM |       TPM |   duration |   errors |
|:------------|:------------|-----------------:|---------:|---------:|----------------:|------------:|-------------:|----------:|----------:|-----------:|---------:|
| MySQL-1-1-1 | MySQL-1-1-1 |                1 |       16 |        1 |               1 |           1 |         0.00 | 181106.00 | 421095.00 |          5 |        0 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
```

</details>

### Monitoring on Persistent Storage

```bash
bexhoma hammerdb \
  -dbms MySQL \
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
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 128Gi \
  -rsr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hammerdb_mysql_monitoring.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hammerdb_mysql_monitoring_summary.md" target="_blank" rel="noopener">docs_hammerdb_mysql_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 932s 
* Code: 1794058559
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Ramp-up period is 2 minutes before measurements begin.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.13.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 128Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:809808
  * datadisk:34381
  * volume_size:125G
  * volume_used:34G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794058559

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794058559-5757f7b4b7-5j69w: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: hammerdb (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: hammerdb (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |   16 |       65.00 |           5.00 |            0.00 |         55.00 |            5.00 |              1 |           8 |             | None           |             0 | False         |              886.15 | False               |

### Benchmarking

#### Per Connection

| DBMS            | phase       | job           |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |    TPM |   efficiency |   duration |   errors |
|:----------------|:------------|:--------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|-------:|-------------:|-----------:|---------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |       16 |        1 |               1 |       1 |  72858 | 169102 |         0.00 |          5 |        0 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   efficiency |     NOPM |       TPM |   duration |   errors |
|:------------|:------------|-----------------:|---------:|---------:|----------------:|------------:|-------------:|---------:|----------:|-----------:|---------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |       16 |        1 |               1 |           1 |         0.00 | 72858.00 | 169102.00 |          5 |        0 |

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |        77.89 |      1.52 |           5.48 |                  7.26 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       177.77 |      6.29 |           0.10 |                  0.10 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      1400.12 |      3.69 |           5.24 |                 10.50 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       649.51 |      1.66 |           0.08 |                  0.08 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)

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
  -dbms MySQL \
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
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hammerdb_mysql_scale.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hammerdb_mysql_scale_summary.md" target="_blank" rel="noopener">docs_hammerdb_mysql_scale.log</a></summary>

```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 2927s 
* Code: 1794059536
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 2 minutes. Ramp-up period is 2 minutes before measurements begin.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.13.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MySQL'].
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:811244
  * datadisk:35023
  * volume_size:125G
  * volume_used:35G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794059536
* mysql-1-1-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806784
  * datadisk:35327
  * volume_size:125G
  * volume_used:35G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794059536
* mysql-1-1-3-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806785
  * datadisk:35965
  * volume_size:125G
  * volume_used:36G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794059536
* mysql-1-1-4-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806786
  * datadisk:36293
  * volume_size:125G
  * volume_used:36G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794059536
* mysql-1-2-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806796
  * datadisk:36974
  * volume_size:125G
  * volume_used:37G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794059536
* mysql-1-2-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806996
  * datadisk:37311
  * volume_size:125G
  * volume_used:37G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794059536
* mysql-1-2-3-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806788
  * datadisk:37952
  * volume_size:125G
  * volume_used:38G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794059536
* mysql-1-2-4-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806789
  * datadisk:38272
  * volume_size:125G
  * volume_used:38G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794059536

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MySQL-1

### Data Parameters of Reused Volumes
* MySQL-1: loading values of the volume: script=Schema, indexing=Checks

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794059536-577498c799-5mpf5: 0
* bexhoma-sut-mysql-1-1794059536-6c57f88c58-hpnkx: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: hammerdb (2 pods)
* DBMS MySQL-1 - Experiment 1 Client 3: hammerdb (2 pods)
* DBMS MySQL-1 - Experiment 1 Client 4: hammerdb (4 pods)
* DBMS MySQL-1 - Experiment 2 Client 1: hammerdb (1 pods)
* DBMS MySQL-1 - Experiment 2 Client 2: hammerdb (2 pods)
* DBMS MySQL-1 - Experiment 2 Client 3: hammerdb (2 pods)
* DBMS MySQL-1 - Experiment 2 Client 4: hammerdb (4 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: hammerdb (2 pods)
* DBMS MySQL-1 - Experiment 1 Client 3: hammerdb (2 pods)
* DBMS MySQL-1 - Experiment 1 Client 4: hammerdb (4 pods)
* DBMS MySQL-1 - Experiment 2 Client 1: hammerdb (1 pods)
* DBMS MySQL-1 - Experiment 2 Client 2: hammerdb (2 pods)
* DBMS MySQL-1 - Experiment 2 Client 3: hammerdb (2 pods)
* DBMS MySQL-1 - Experiment 2 Client 4: hammerdb (4 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |   16 |       65.00 |           5.00 |            0.00 |         55.00 |            5.00 |              0 |           8 |             | None           |             0 | False         |              886.15 | True                |
| MySQL-1-2 |                2 |   16 |       65.00 |           5.00 |            0.00 |         55.00 |            5.00 |              0 |           8 |             | None           |             0 | False         |              886.15 | True                |

### Benchmarking

#### Per Connection

| DBMS            | phase       | job           |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |    TPM |   efficiency |   duration |   errors |
|:----------------|:------------|:--------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|-------:|-------------:|-----------:|---------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |       16 |        1 |               1 |       1 |  68558 | 160100 |         0.00 |          2 |        0 |
| mysql-1-1-2-1-1 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |       16 |        2 |               1 |       1 | 143381 | 333424 |         0.00 |          2 |        0 |
| mysql-1-1-2-1-2 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |       16 |        2 |               1 |       2 | 143221 | 333016 |         0.00 |          2 |        0 |
| mysql-1-1-3-1-1 | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        8 |        3 |               1 |       1 |  71494 | 166215 |         0.00 |          2 |        0 |
| mysql-1-1-3-1-2 | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        8 |        3 |               1 |       2 |  71393 | 165969 |         0.00 |          2 |        0 |
| mysql-1-1-4-1-1 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        8 |        4 |               1 |       1 | 148204 | 344735 |         0.00 |          2 |        0 |
| mysql-1-1-4-1-2 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        8 |        4 |               1 |       2 | 147893 | 343974 |         0.00 |          2 |        0 |
| mysql-1-1-4-1-3 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        8 |        4 |               1 |       3 | 148076 | 344413 |         0.00 |          2 |        0 |
| mysql-1-1-4-1-4 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        8 |        4 |               1 |       4 | 148201 | 344725 |         0.00 |          2 |        0 |
| mysql-1-2-1-1-1 | mysql-1-2-1 | mysql-1-2-1-1 |                2 |       16 |        1 |               1 |       1 |  74164 | 172707 |         0.00 |          2 |        0 |
| mysql-1-2-2-1-1 | mysql-1-2-2 | mysql-1-2-2-1 |                2 |       16 |        2 |               1 |       1 | 143047 | 332717 |         0.00 |          2 |        0 |
| mysql-1-2-2-1-2 | mysql-1-2-2 | mysql-1-2-2-1 |                2 |       16 |        2 |               1 |       2 | 142742 | 332116 |         0.00 |          2 |        0 |
| mysql-1-2-3-1-1 | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        8 |        3 |               1 |       1 |  69346 | 160892 |         0.00 |          2 |        0 |
| mysql-1-2-3-1-2 | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        8 |        3 |               1 |       2 |  69382 | 160925 |         0.00 |          2 |        0 |
| mysql-1-2-4-1-1 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        8 |        4 |               1 |       1 | 139983 | 325140 |         0.00 |          2 |        0 |
| mysql-1-2-4-1-2 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        8 |        4 |               1 |       2 | 139994 | 325186 |         0.00 |          2 |        0 |
| mysql-1-2-4-1-3 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        8 |        4 |               1 |       3 | 139894 | 324983 |         0.00 |          2 |        0 |
| mysql-1-2-4-1-4 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        8 |        4 |               1 |       4 | 139989 | 325143 |         0.00 |          2 |        0 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   efficiency |      NOPM |       TPM |   duration |   errors |
|:------------|:------------|-----------------:|---------:|---------:|----------------:|------------:|-------------:|----------:|----------:|-----------:|---------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |       16 |        1 |               1 |           1 |         0.00 |  68558.00 | 160100.00 |          2 |        0 |
| mysql-1-1-2 | mysql-1-1-2 |                1 |       32 |        2 |               1 |           2 |         0.00 | 143301.00 | 333220.00 |          2 |        0 |
| mysql-1-1-3 | mysql-1-1-3 |                1 |       16 |        3 |               1 |           2 |         0.00 |  71443.50 | 166092.00 |          2 |        0 |
| mysql-1-1-4 | mysql-1-1-4 |                1 |       32 |        4 |               1 |           4 |         0.00 | 148093.50 | 344461.75 |          2 |        0 |
| mysql-1-2-1 | mysql-1-2-1 |                2 |       16 |        1 |               1 |           1 |         0.00 |  74164.00 | 172707.00 |          2 |        0 |
| mysql-1-2-2 | mysql-1-2-2 |                2 |       32 |        2 |               1 |           2 |         0.00 | 142894.50 | 332416.50 |          2 |        0 |
| mysql-1-2-3 | mysql-1-2-3 |                2 |       16 |        3 |               1 |           2 |         0.00 |  69364.00 | 160908.50 |          2 |        0 |
| mysql-1-2-4 | mysql-1-2-4 |                2 |       32 |        4 |               1 |           4 |         0.00 | 139965.00 | 325113.00 |          2 |        0 |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       674.64 |      3.16 |           4.69 |                  6.48 |
| mysql-1-1-2-1 |      1167.93 |      5.56 |           5.55 |                 10.73 |
| mysql-1-1-3-1 |       708.11 |      3.10 |           5.98 |                 13.38 |
| mysql-1-1-4-1 |      1329.75 |      5.95 |           6.78 |                 18.06 |
| mysql-1-2-1-1 |       724.05 |      3.55 |           4.95 |                  6.77 |
| mysql-1-2-2-1 |      1379.02 |      6.26 |           6.11 |                 11.80 |
| mysql-1-2-3-1 |       650.77 |      3.34 |           6.50 |                 13.82 |
| mysql-1-2-4-1 |      1307.31 |      6.21 |           7.27 |                 18.37 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       324.12 |      1.62 |           0.08 |                  0.08 |
| mysql-1-1-2-1 |       604.47 |      2.59 |           0.08 |                  0.08 |
| mysql-1-1-3-1 |       360.03 |      1.66 |           0.05 |                  0.05 |
| mysql-1-1-4-1 |       546.93 |      2.56 |           0.05 |                  0.05 |
| mysql-1-2-1-1 |       367.03 |      1.68 |           0.08 |                  0.08 |
| mysql-1-2-2-1 |       517.98 |      2.54 |           0.08 |                  0.08 |
| mysql-1-2-3-1 |       374.06 |      1.69 |           0.05 |                  0.05 |
| mysql-1-2-4-1 |       523.53 |      2.49 |           0.05 |                  0.05 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-3-1 (bexhoma-metrics-mysql-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-3-1 (bexhoma-metrics-mysql-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-3-1 (bexhoma-metrics-mysql-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-3-1 (bexhoma-metrics-mysql-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-4-1 (bexhoma-metrics-mysql-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-4-1 (bexhoma-metrics-mysql-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-4-1 (bexhoma-metrics-mysql-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-4-1 (bexhoma-metrics-mysql-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-2-1-1 (bexhoma-metrics-mysql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-2-1-1 (bexhoma-metrics-mysql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-2-1-1 (bexhoma-metrics-mysql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-2-1-1 (bexhoma-metrics-mysql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-2-2-1 (bexhoma-metrics-mysql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-2-2-1 (bexhoma-metrics-mysql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-2-2-1 (bexhoma-metrics-mysql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-2-2-1 (bexhoma-metrics-mysql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-2-3-1 (bexhoma-metrics-mysql-1-2-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-2-3-1 (bexhoma-metrics-mysql-1-2-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-2-3-1 (bexhoma-metrics-mysql-1-2-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-2-3-1 (bexhoma-metrics-mysql-1-2-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-2-4-1 (bexhoma-metrics-mysql-1-2-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-2-4-1 (bexhoma-metrics-mysql-1-2-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-2-4-1 (bexhoma-metrics-mysql-1-2-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-2-4-1 (bexhoma-metrics-mysql-1-2-4-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MySQL-1)
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
  -dbms MySQL \
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
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_mysql_loading.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_mysql_loading_summary.md" target="_blank" rel="noopener">docs_ycsb_mysql_loading.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 2439s 
* Code: 1793626129
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
  * Experiment is limited to DBMS ['MySQL'].
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:838530
  * datadisk:34754
  * volume_size:1.8T
  * volume_used:819G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793626129
* mysql-2-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:838530
  * datadisk:34722
  * volume_size:1.8T
  * volume_used:819G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793626129
* mysql-3-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:838530
  * datadisk:34750
  * volume_size:1.8T
  * volume_used:819G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793626129
* mysql-4-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:838530
  * datadisk:34722
  * volume_size:1.8T
  * volume_used:819G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793626129

### SUT Container Restarts
* bexhoma-sut-mysql-1-1793626129-5bc9754b5-dxnqt: 0
* bexhoma-sut-mysql-2-1793626129-6864d4dfdc-tghth: 0
* bexhoma-sut-mysql-3-1793626129-7566786f9c-jdllp: 0
* bexhoma-sut-mysql-4-1793626129-697866cbf9-jcgrk: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MySQL-2 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MySQL-3 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MySQL-4 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MySQL-2 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MySQL-3 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MySQL-4 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| mysql-1-1-0-1-1 |             1.00 |      8.00 |   256.00 |        4.00 |         0.00 |                          255.77 |               977455.00 |            250000.00 |                              1275.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-2 |             1.00 |      8.00 |   256.00 |        4.00 |         0.00 |                          255.77 |               977458.00 |            250000.00 |                              1269.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-3 |             1.00 |      8.00 |   256.00 |        4.00 |         0.00 |                          255.77 |               977448.00 |            250000.00 |                              1260.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-4 |             1.00 |      8.00 |   256.00 |        4.00 |         0.00 |                          255.77 |               977446.00 |            250000.00 |                              1248.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-1 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.89 |               977399.00 |            125000.00 |                              1284.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-2 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.89 |               977368.00 |            125000.00 |                              1271.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-3 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.90 |               977363.00 |            125000.00 |                              1263.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-4 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.90 |               977304.00 |            125000.00 |                              1306.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-5 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.90 |               977293.00 |            125000.00 |                              1284.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-6 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.91 |               977278.00 |            125000.00 |                              1302.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-7 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.90 |               977315.00 |            125000.00 |                              1295.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-8 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.90 |               977302.00 |            125000.00 |                              1225.00 | 1.00 |                3.68 |
| mysql-3-1-0-1-1 |             1.00 |     16.00 |   256.00 |        4.00 |         0.00 |                          255.68 |               977780.00 |            250000.00 |                              1398.00 | 1.00 |                3.68 |
| mysql-3-1-0-1-2 |             1.00 |     16.00 |   256.00 |        4.00 |         0.00 |                          255.72 |               977644.00 |            250000.00 |                              1372.00 | 1.00 |                3.68 |
| mysql-3-1-0-1-3 |             1.00 |     16.00 |   256.00 |        4.00 |         0.00 |                          255.70 |               977727.00 |            250000.00 |                              1395.00 | 1.00 |                3.68 |
| mysql-3-1-0-1-4 |             1.00 |     16.00 |   256.00 |        4.00 |         0.00 |                          255.67 |               977818.00 |            250000.00 |                              1372.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-1 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.87 |               977581.00 |            125000.00 |                              1423.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-2 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.88 |               977448.00 |            125000.00 |                              1361.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-3 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.88 |               977505.00 |            125000.00 |                              1388.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-4 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.87 |               977557.00 |            125000.00 |                              1336.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-5 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.89 |               977409.00 |            125000.00 |                              1411.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-6 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.87 |               977565.00 |            125000.00 |                              1425.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-7 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.88 |               977499.00 |            125000.00 |                              1377.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-8 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.87 |               977547.00 |            125000.00 |                              1403.00 | 1.00 |                3.68 |

#### Per Run

| DBMS      |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1 |             1.00 |     32.00 |  1024.00 |        4.00 |         0.00 | 1.00 |                3.68 |                         1023.07 |               977458.00 |           1000000.00 |                              1263.00 |
| MySQL-2-1 |             1.00 |     32.00 |  1024.00 |        8.00 |         0.00 | 1.00 |                3.68 |                         1023.20 |               977399.00 |           1000000.00 |                              1278.75 |
| MySQL-3-1 |             1.00 |     64.00 |  1024.00 |        4.00 |         0.00 | 1.00 |                3.68 |                         1022.76 |               977818.00 |           1000000.00 |                              1384.25 |
| MySQL-4-1 |             1.00 |     64.00 |  1024.00 |        8.00 |         0.00 | 1.00 |                3.68 |                         1023.00 |               977581.00 |           1000000.00 |                              1390.50 |

### Benchmarking

#### Per Connection

| DBMS            | phase       | job           | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1021.58 |               978878.00 |             499524 |                            1321.00 |               500476 |                              3217.00 |
| mysql-2-1-1-1-1 | mysql-2-1-1 | mysql-2-1-1-1 | MySQL-2         |                1 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1021.88 |               978590.00 |             499825 |                            1317.00 |               500175 |                              3199.00 |
| mysql-3-1-1-1-1 | mysql-3-1-1 | mysql-3-1-1-1 | MySQL-3         |                1 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1021.63 |               978830.00 |             501045 |                            1325.00 |               498955 |                              3237.00 |
| mysql-4-1-1-1-1 | mysql-4-1-1 | mysql-4-1-1-1 | MySQL-4         |                1 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1021.37 |               979076.00 |             499813 |                            1320.00 |               500187 |                              3193.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        64 |     1024 |               1 |           1 |            0 |                         1021.58 |               978878.00 |             499524 |                            1321.00 |               500476 |                              3217.00 |
| mysql-2-1-1 | mysql-2-1-1 |                1 |        64 |     1024 |               1 |           1 |            0 |                         1021.88 |               978590.00 |             499825 |                            1317.00 |               500175 |                              3199.00 |
| mysql-3-1-1 | mysql-3-1-1 |                1 |        64 |     1024 |               1 |           1 |            0 |                         1021.63 |               978830.00 |             501045 |                            1325.00 |               498955 |                              3237.00 |
| mysql-4-1-1 | mysql-4-1-1 |                1 |        64 |     1024 |               1 |           1 |            0 |                         1021.37 |               979076.00 |             499813 |                            1320.00 |               500187 |                              3193.00 |

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
  -dbms MySQL \
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
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rsr \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_mysql_storage.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_mysql_storage_summary.md" target="_blank" rel="noopener">docs_ycsb_mysql_storage.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 3719s 
* Code: 1793628584
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
  * Experiment is limited to DBMS ['MySQL'].
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:699336
  * datadisk:34722
  * volume_size:49G
  * volume_used:34G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793628584
* mysql-1-2-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:699349
  * datadisk:34723
  * volume_size:49G
  * volume_used:34G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793628584

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MySQL-1-2

### Data Parameters of Reused Volumes
* MySQL-1: DDL values of the volume: row_format=DYNAMIC, collation=utf8mb4_0900_ai_ci
* MySQL-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### SUT Container Restarts
* bexhoma-sut-mysql-1-1793628584-5b695b5b5d-cvt22: 0
* bexhoma-sut-mysql-1-1793628584-67d6cc6486-xknsn: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MySQL-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MySQL-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| mysql-1-1-0-1-1 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.85 |               977720.00 |            125000.00 |                              1892.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-2 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.81 |               977985.00 |            125000.00 |                              1789.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-3 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.82 |               977975.00 |            125000.00 |                              1799.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-4 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.85 |               977731.00 |            125000.00 |                              1765.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-5 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.81 |               977995.00 |            125000.00 |                              1867.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-6 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.83 |               977878.00 |            125000.00 |                              1783.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-7 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.84 |               977762.00 |            125000.00 |                              1768.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-8 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.83 |               977876.00 |            125000.00 |                              1725.00 | 1.00 |                3.68 |

#### Per Run

| DBMS      |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1 |             1.00 |     64.00 |  1024.00 |        8.00 |         0.00 | 1.00 |                3.68 |                         1022.64 |               977995.00 |           1000000.00 |                              1798.50 |

### Benchmarking

#### Per Connection

| DBMS            | phase       | job           | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1022.26 |               978226.00 |             500026 |                            1359.00 |               499974 |                              7171.00 |
| mysql-1-2-1-1-1 | mysql-1-2-1 | mysql-1-2-1-1 | MySQL-1         |                2 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1022.23 |               978251.00 |             500504 |                            2095.00 |               499496 |                              7039.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        64 |     1024 |               1 |           1 |            0 |                         1022.26 |               978226.00 |             500026 |                            1359.00 |               499974 |                              7171.00 |
| mysql-1-2-1 | mysql-1-2-1 |                2 |        64 |     1024 |               1 |           1 |            0 |                         1022.23 |               978251.00 |             500504 |                            2095.00 |               499496 |                              7039.00 |

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
  -dbms MySQL \
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
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_mysql_scale.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_mysql_scale_summary.md" target="_blank" rel="noopener">docs_ycsb_mysql_scale.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 6843s 
* Code: 1793632316
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
  * Experiment is limited to DBMS ['MySQL'].
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:699365
  * datadisk:34723
  * volume_size:49G
  * volume_used:34G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1793632316
* mysql-1-1-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:699371
  * datadisk:34723
  * volume_size:49G
  * volume_used:34G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1793632316
* mysql-1-1-3-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:699374
  * datadisk:34723
  * volume_size:49G
  * volume_used:34G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1793632316
* mysql-1-1-4-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:699381
  * datadisk:34723
  * volume_size:49G
  * volume_used:34G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1793632316
* mysql-1-2-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:699405
  * datadisk:34723
  * volume_size:49G
  * volume_used:34G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1793632316
* mysql-1-2-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:699432
  * datadisk:34723
  * volume_size:49G
  * volume_used:34G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1793632316
* mysql-1-2-3-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:699435
  * datadisk:34723
  * volume_size:49G
  * volume_used:34G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1793632316
* mysql-1-2-4-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:699443
  * datadisk:34723
  * volume_size:49G
  * volume_used:34G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1793632316

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MySQL-1

### Data Parameters of Reused Volumes
* MySQL-1: DDL values of the volume: row_format=DYNAMIC, collation=utf8mb4_0900_ai_ci
* MySQL-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### SUT Container Restarts
* bexhoma-sut-mysql-1-1793632316-bd7c65ccb-fjxlk: 0
* bexhoma-sut-mysql-1-1793632316-649f7bc8cc-thjch: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: ycsb (2 pods)
* DBMS MySQL-1 - Experiment 1 Client 3: ycsb (8 pods)
* DBMS MySQL-1 - Experiment 1 Client 4: ycsb (16 pods)
* DBMS MySQL-1 - Experiment 2 Client 1: ycsb (1 pods)
* DBMS MySQL-1 - Experiment 2 Client 2: ycsb (2 pods)
* DBMS MySQL-1 - Experiment 2 Client 3: ycsb (8 pods)
* DBMS MySQL-1 - Experiment 2 Client 4: ycsb (16 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: ycsb (2 pods)
* DBMS MySQL-1 - Experiment 1 Client 3: ycsb (8 pods)
* DBMS MySQL-1 - Experiment 1 Client 4: ycsb (16 pods)
* DBMS MySQL-1 - Experiment 2 Client 1: ycsb (1 pods)
* DBMS MySQL-1 - Experiment 2 Client 2: ycsb (2 pods)
* DBMS MySQL-1 - Experiment 2 Client 3: ycsb (8 pods)
* DBMS MySQL-1 - Experiment 2 Client 4: ycsb (16 pods)

### Benchmarking

#### Per Connection

| DBMS             | phase       | job           | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1-1-1  | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1021.93 |               978544.00 |             499989 |                            1975.00 |               500011 |                              6611.00 |
| mysql-1-1-2-1-1  | mysql-1-1-2 | mysql-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       1 |        64 |     1024 |           2 |            0 |                         1019.90 |               490244.00 |             249863 |                            1310.00 |               250137 |                              8099.00 |
| mysql-1-1-2-1-2  | mysql-1-1-2 | mysql-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       2 |        64 |     1024 |           2 |            0 |                         1019.82 |               490284.00 |             250239 |                            1330.00 |               249761 |                              7487.00 |
| mysql-1-1-3-1-1  | mysql-1-1-3 | mysql-1-1-3-1 | MySQL-1         |                1 |        3 |               1 |       1 |         8 |      128 |           8 |            0 |                          127.89 |               977431.00 |              62389 |                            1408.00 |                62611 |                              7347.00 |
| mysql-1-1-3-1-2  | mysql-1-1-3 | mysql-1-1-3-1 | MySQL-1         |                1 |        3 |               1 |       2 |         8 |      128 |           8 |            0 |                          127.87 |               977521.00 |              62436 |                            1384.00 |                62564 |                              7047.00 |
| mysql-1-1-3-1-3  | mysql-1-1-3 | mysql-1-1-3-1 | MySQL-1         |                1 |        3 |               1 |       3 |         8 |      128 |           8 |            0 |                          127.87 |               977557.00 |              62471 |                            1474.00 |                62529 |                              7327.00 |
| mysql-1-1-3-1-4  | mysql-1-1-3 | mysql-1-1-3-1 | MySQL-1         |                1 |        3 |               1 |       4 |         8 |      128 |           8 |            0 |                          127.89 |               977423.00 |              62299 |                            1405.00 |                62701 |                              7327.00 |
| mysql-1-1-3-1-5  | mysql-1-1-3 | mysql-1-1-3-1 | MySQL-1         |                1 |        3 |               1 |       5 |         8 |      128 |           8 |            0 |                          127.88 |               977475.00 |              62143 |                            1389.00 |                62857 |                              7283.00 |
| mysql-1-1-3-1-6  | mysql-1-1-3 | mysql-1-1-3-1 | MySQL-1         |                1 |        3 |               1 |       6 |         8 |      128 |           8 |            0 |                          127.88 |               977457.00 |              62350 |                            1377.00 |                62650 |                              7083.00 |
| mysql-1-1-3-1-7  | mysql-1-1-3 | mysql-1-1-3-1 | MySQL-1         |                1 |        3 |               1 |       7 |         8 |      128 |           8 |            0 |                          127.88 |               977491.00 |              62463 |                            1376.00 |                62537 |                              7379.00 |
| mysql-1-1-3-1-8  | mysql-1-1-3 | mysql-1-1-3-1 | MySQL-1         |                1 |        3 |               1 |       8 |         8 |      128 |           8 |            0 |                          127.88 |               977471.00 |              62481 |                            1389.00 |                62519 |                              7543.00 |
| mysql-1-1-4-1-1  | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       1 |         8 |      128 |          16 |            0 |                          127.65 |               489602.00 |              31124 |                            1681.00 |                31376 |                              6523.00 |
| mysql-1-1-4-1-2  | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       2 |         8 |      128 |          16 |            0 |                          127.56 |               489955.00 |              31322 |                            1582.00 |                31178 |                              6471.00 |
| mysql-1-1-4-1-3  | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       3 |         8 |      128 |          16 |            0 |                          127.59 |               489863.00 |              31317 |                            1791.00 |                31183 |                              6523.00 |
| mysql-1-1-4-1-4  | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       4 |         8 |      128 |          16 |            0 |                          127.57 |               489915.00 |              31347 |                            1772.00 |                31153 |                              6515.00 |
| mysql-1-1-4-1-5  | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       5 |         8 |      128 |          16 |            0 |                          127.62 |               489748.00 |              31293 |                            1782.00 |                31207 |                              6323.00 |
| mysql-1-1-4-1-6  | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       6 |         8 |      128 |          16 |            0 |                          127.58 |               489903.00 |              31130 |                            1715.00 |                31370 |                              6499.00 |
| mysql-1-1-4-1-7  | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       7 |         8 |      128 |          16 |            0 |                          127.60 |               489801.00 |              31346 |                            1726.00 |                31154 |                              6371.00 |
| mysql-1-1-4-1-8  | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       8 |         8 |      128 |          16 |            0 |                          127.64 |               489660.00 |              31330 |                            1679.00 |                31170 |                              6411.00 |
| mysql-1-1-4-1-9  | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       9 |         8 |      128 |          16 |            0 |                          127.63 |               489702.00 |              31465 |                            1696.00 |                31035 |                              6335.00 |
| mysql-1-1-4-1-10 | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |      10 |         8 |      128 |          16 |            0 |                          127.58 |               489878.00 |              31376 |                            1711.00 |                31124 |                              6351.00 |
| mysql-1-1-4-1-11 | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |      11 |         8 |      128 |          16 |            0 |                          127.62 |               489720.00 |              31178 |                            1682.00 |                31322 |                              6527.00 |
| mysql-1-1-4-1-12 | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |      12 |         8 |      128 |          16 |            0 |                          127.62 |               489747.00 |              31178 |                            1657.00 |                31322 |                              6471.00 |
| mysql-1-1-4-1-13 | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |      13 |         8 |      128 |          16 |            0 |                          127.58 |               489906.00 |              31296 |                            1819.00 |                31204 |                              6443.00 |
| mysql-1-1-4-1-14 | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |      14 |         8 |      128 |          16 |            0 |                          127.60 |               489826.00 |              31228 |                            1812.00 |                31272 |                              6491.00 |
| mysql-1-1-4-1-15 | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |      15 |         8 |      128 |          16 |            0 |                          127.60 |               489819.00 |              31360 |                            1646.00 |                31140 |                              6343.00 |
| mysql-1-1-4-1-16 | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |      16 |         8 |      128 |          16 |            0 |                          127.61 |               489767.00 |              30896 |                            1651.00 |                31604 |                              6455.00 |
| mysql-1-2-1-1-1  | mysql-1-2-1 | mysql-1-2-1-1 | MySQL-1         |                2 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1022.16 |               978323.00 |             500218 |                            2101.00 |               499782 |                              7455.00 |
| mysql-1-2-2-1-1  | mysql-1-2-2 | mysql-1-2-2-1 | MySQL-1         |                2 |        2 |               1 |       1 |        64 |     1024 |           2 |            0 |                         1019.35 |               490511.00 |             250095 |                            1401.00 |               249905 |                              6843.00 |
| mysql-1-2-2-1-2  | mysql-1-2-2 | mysql-1-2-2-1 | MySQL-1         |                2 |        2 |               1 |       2 |        64 |     1024 |           2 |            0 |                         1019.94 |               490223.00 |             250373 |                            1404.00 |               249627 |                              6871.00 |
| mysql-1-2-3-1-1  | mysql-1-2-3 | mysql-1-2-3-1 | MySQL-1         |                2 |        3 |               1 |       1 |         8 |      128 |           8 |            0 |                          127.80 |               978067.00 |              62508 |                            1468.00 |                62492 |                              6423.00 |
| mysql-1-2-3-1-2  | mysql-1-2-3 | mysql-1-2-3-1 | MySQL-1         |                2 |        3 |               1 |       2 |         8 |      128 |           8 |            0 |                          127.84 |               977801.00 |              62361 |                            1550.00 |                62639 |                              6847.00 |
| mysql-1-2-3-1-3  | mysql-1-2-3 | mysql-1-2-3-1 | MySQL-1         |                2 |        3 |               1 |       3 |         8 |      128 |           8 |            0 |                          127.83 |               977866.00 |              62491 |                            1465.00 |                62509 |                              6591.00 |
| mysql-1-2-3-1-4  | mysql-1-2-3 | mysql-1-2-3-1 | MySQL-1         |                2 |        3 |               1 |       4 |         8 |      128 |           8 |            0 |                          127.85 |               977726.00 |              62727 |                            1434.00 |                62273 |                              6715.00 |
| mysql-1-2-3-1-5  | mysql-1-2-3 | mysql-1-2-3-1 | MySQL-1         |                2 |        3 |               1 |       5 |         8 |      128 |           8 |            0 |                          127.81 |               978017.00 |              62491 |                            1491.00 |                62509 |                              6779.00 |
| mysql-1-2-3-1-6  | mysql-1-2-3 | mysql-1-2-3-1 | MySQL-1         |                2 |        3 |               1 |       6 |         8 |      128 |           8 |            0 |                          127.84 |               977777.00 |              62711 |                            1440.00 |                62289 |                              6683.00 |
| mysql-1-2-3-1-7  | mysql-1-2-3 | mysql-1-2-3-1 | MySQL-1         |                2 |        3 |               1 |       7 |         8 |      128 |           8 |            0 |                          127.81 |               978024.00 |              62383 |                            1475.00 |                62617 |                              6871.00 |
| mysql-1-2-3-1-8  | mysql-1-2-3 | mysql-1-2-3-1 | MySQL-1         |                2 |        3 |               1 |       8 |         8 |      128 |           8 |            0 |                          127.84 |               977791.00 |              62578 |                            1452.00 |                62422 |                              6727.00 |
| mysql-1-2-4-1-1  | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |       1 |         8 |      128 |          16 |            0 |                          127.71 |               489405.00 |              31317 |                            1693.00 |                31183 |                              7543.00 |
| mysql-1-2-4-1-2  | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |       2 |         8 |      128 |          16 |            0 |                          127.67 |               489547.00 |              31227 |                            1647.00 |                31273 |                              7395.00 |
| mysql-1-2-4-1-3  | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |       3 |         8 |      128 |          16 |            0 |                          127.64 |               489669.00 |              31444 |                            1655.00 |                31056 |                              7423.00 |
| mysql-1-2-4-1-4  | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |       4 |         8 |      128 |          16 |            0 |                          127.71 |               489373.00 |              30956 |                            1743.00 |                31544 |                              7479.00 |
| mysql-1-2-4-1-5  | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |       5 |         8 |      128 |          16 |            0 |                          127.68 |               489491.00 |              31402 |                            1650.00 |                31098 |                              7531.00 |
| mysql-1-2-4-1-6  | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |       6 |         8 |      128 |          16 |            0 |                          127.68 |               489515.00 |              31291 |                            1675.00 |                31209 |                              7491.00 |
| mysql-1-2-4-1-7  | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |       7 |         8 |      128 |          16 |            0 |                          127.72 |               489346.00 |              31262 |                            1657.00 |                31238 |                              7283.00 |
| mysql-1-2-4-1-8  | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |       8 |         8 |      128 |          16 |            0 |                          127.70 |               489419.00 |              31247 |                            1682.00 |                31253 |                              7479.00 |
| mysql-1-2-4-1-9  | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |       9 |         8 |      128 |          16 |            0 |                          127.67 |               489529.00 |              31223 |                            1583.00 |                31277 |                              7411.00 |
| mysql-1-2-4-1-10 | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |      10 |         8 |      128 |          16 |            0 |                          127.71 |               489377.00 |              31099 |                            1755.00 |                31401 |                              7531.00 |
| mysql-1-2-4-1-11 | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |      11 |         8 |      128 |          16 |            0 |                          127.71 |               489397.00 |              31093 |                            1718.00 |                31407 |                              7507.00 |
| mysql-1-2-4-1-12 | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |      12 |         8 |      128 |          16 |            0 |                          127.68 |               489497.00 |              31342 |                            1701.00 |                31158 |                              7483.00 |
| mysql-1-2-4-1-13 | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |      13 |         8 |      128 |          16 |            0 |                          127.73 |               489316.00 |              31228 |                            1717.00 |                31272 |                              7495.00 |
| mysql-1-2-4-1-14 | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |      14 |         8 |      128 |          16 |            0 |                          127.72 |               489365.00 |              31309 |                            1751.00 |                31191 |                              7471.00 |
| mysql-1-2-4-1-15 | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |      15 |         8 |      128 |          16 |            0 |                          127.69 |               489478.00 |              31426 |                            1678.00 |                31074 |                              7459.00 |
| mysql-1-2-4-1-16 | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |      16 |         8 |      128 |          16 |            0 |                          127.68 |               489521.00 |              31263 |                            1661.00 |                31237 |                              7447.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        64 |     1024 |               1 |           1 |            0 |                         1021.93 |               978544.00 |             499989 |                            1975.00 |               500011 |                              6611.00 |
| mysql-1-1-2 | mysql-1-1-2 |                1 |       128 |     2048 |               1 |           2 |            0 |                         2039.72 |               490284.00 |             500102 |                            1330.00 |               499898 |                              8099.00 |
| mysql-1-1-3 | mysql-1-1-3 |                1 |        64 |     1024 |               1 |           8 |            0 |                         1023.04 |               977557.00 |             499032 |                            1474.00 |               500968 |                              7543.00 |
| mysql-1-1-4 | mysql-1-1-4 |                1 |       128 |     2048 |               1 |          16 |            0 |                         2041.65 |               489955.00 |             500186 |                            1819.00 |               499814 |                              6527.00 |
| mysql-1-2-1 | mysql-1-2-1 |                2 |        64 |     1024 |               1 |           1 |            0 |                         1022.16 |               978323.00 |             500218 |                            2101.00 |               499782 |                              7455.00 |
| mysql-1-2-2 | mysql-1-2-2 |                2 |       128 |     2048 |               1 |           2 |            0 |                         2039.29 |               490511.00 |             500468 |                            1404.00 |               499532 |                              6871.00 |
| mysql-1-2-3 | mysql-1-2-3 |                2 |        64 |     1024 |               1 |           8 |            0 |                         1022.62 |               978067.00 |             500250 |                            1550.00 |               499750 |                              6871.00 |
| mysql-1-2-4 | mysql-1-2-4 |                2 |       128 |     2048 |               1 |          16 |            0 |                         2043.10 |               489669.00 |             500129 |                            1755.00 |               499871 |                              7543.00 |

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MySQL-1)
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
  -dbms MySQL \
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
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_mysql_workload_e.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_mysql_workload_e_summary.md" target="_blank" rel="noopener">docs_ycsb_mysql_workload_e.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 2400s 
* Code: 1793824142
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
  * Experiment is limited to DBMS ['MySQL'].
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:850944
  * datadisk:34722
  * volume_size:49G
  * volume_used:34G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793824142

### SUT Container Restarts
* bexhoma-sut-mysql-1-1793824142-57db6db5ff-smw4q: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (8 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (8 pods)

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| mysql-1-1-0-1-1 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.84 |               977786.00 |            125000.00 |                              1588.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-2 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.84 |               977789.00 |            125000.00 |                              1566.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-3 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.82 |               977953.00 |            125000.00 |                              1635.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-4 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.81 |               977996.00 |            125000.00 |                              1618.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-5 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.83 |               977871.00 |            125000.00 |                              1560.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-6 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.80 |               978083.00 |            125000.00 |                              1559.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-7 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.84 |               977798.00 |            125000.00 |                              1600.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-8 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.81 |               977985.00 |            125000.00 |                              1553.00 | 1.00 |                3.68 |

#### Per Run

| DBMS      |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1 |             1.00 |     64.00 |  1024.00 |        8.00 |         0.00 | 1.00 |                3.68 |                         1022.59 |               978083.00 |           1000000.00 |                              1584.88 |

### Benchmarking

#### Per Connection

| DBMS            | phase       | job           | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   [SCAN].Return=OK |   [SCAN].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-------------------:|-----------------------------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       1 |         8 |      128 |           8 |            0 |                          127.87 |               977533.00 |                 6267 |                              8223.00 |             118733 |                            4687.00 |
| mysql-1-1-1-1-2 | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       2 |         8 |      128 |           8 |            0 |                          127.87 |               977547.00 |                 6211 |                              8711.00 |             118789 |                            4523.00 |
| mysql-1-1-1-1-3 | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       3 |         8 |      128 |           8 |            0 |                          127.89 |               977411.00 |                 6286 |                              8187.00 |             118714 |                            4435.00 |
| mysql-1-1-1-1-4 | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       4 |         8 |      128 |           8 |            0 |                          127.88 |               977449.00 |                 6204 |                              8471.00 |             118796 |                            4335.00 |
| mysql-1-1-1-1-5 | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       5 |         8 |      128 |           8 |            0 |                          127.87 |               977533.00 |                 6218 |                              8807.00 |             118782 |                            4331.00 |
| mysql-1-1-1-1-6 | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       6 |         8 |      128 |           8 |            0 |                          127.88 |               977474.00 |                 6336 |                              8391.00 |             118664 |                            4343.00 |
| mysql-1-1-1-1-7 | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       7 |         8 |      128 |           8 |            0 |                          127.87 |               977554.00 |                 6217 |                              8455.00 |             118783 |                            4399.00 |
| mysql-1-1-1-1-8 | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       8 |         8 |      128 |           8 |            0 |                          127.88 |               977458.00 |                 6253 |                              8231.00 |             118747 |                            4447.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   [SCAN].Return=OK |   [SCAN].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-------------------:|-----------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        64 |     1024 |               1 |           8 |            0 |                         1023.02 |               977554.00 |                49992 |                              8807.00 |             950008 |                            4687.00 |

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
  -dbms MySQL \
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
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_mysql_monitoring.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_mysql_monitoring_summary.md" target="_blank" rel="noopener">docs_ycsb_mysql_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 2348s 
* Code: 1793640530
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
  * Experiment is limited to DBMS ['MySQL'].
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:699395
  * datadisk:34815
  * volume_size:49G
  * volume_used:34G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1793640530
* mysql-1-1-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:699406
  * datadisk:34815
  * volume_size:49G
  * volume_used:34G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1793640530

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MySQL-1

### Data Parameters of Reused Volumes
* MySQL-1: DDL values of the volume: row_format=DYNAMIC, collation=utf8mb4_0900_ai_ci
* MySQL-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### SUT Container Restarts
* bexhoma-sut-mysql-1-1793640530-84598d6777-x5pdr: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: ycsb (8 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: ycsb (8 pods)

### Benchmarking

#### Per Connection

| DBMS            | phase       | job           | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1021.64 |               978822.00 |             500455 |                            2105.00 |               499545 |                              7375.00 |
| mysql-1-1-2-1-1 | mysql-1-1-2 | mysql-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       1 |         8 |      128 |           8 |            0 |                          127.86 |               977621.00 |              62477 |                            1576.00 |                62523 |                              6835.00 |
| mysql-1-1-2-1-2 | mysql-1-1-2 | mysql-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       2 |         8 |      128 |           8 |            0 |                          127.88 |               977446.00 |              62276 |                            1532.00 |                62724 |                              6979.00 |
| mysql-1-1-2-1-3 | mysql-1-1-2 | mysql-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       3 |         8 |      128 |           8 |            0 |                          127.82 |               977937.00 |              62452 |                            1543.00 |                62548 |                              7047.00 |
| mysql-1-1-2-1-4 | mysql-1-1-2 | mysql-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       4 |         8 |      128 |           8 |            0 |                          127.83 |               977846.00 |              62495 |                            1559.00 |                62505 |                              6935.00 |
| mysql-1-1-2-1-5 | mysql-1-1-2 | mysql-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       5 |         8 |      128 |           8 |            0 |                          127.87 |               977536.00 |              62549 |                            1532.00 |                62451 |                              6727.00 |
| mysql-1-1-2-1-6 | mysql-1-1-2 | mysql-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       6 |         8 |      128 |           8 |            0 |                          127.83 |               977871.00 |              62348 |                            1560.00 |                62652 |                              6939.00 |
| mysql-1-1-2-1-7 | mysql-1-1-2 | mysql-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       7 |         8 |      128 |           8 |            0 |                          127.84 |               977800.00 |              62326 |                            1586.00 |                62674 |                              6875.00 |
| mysql-1-1-2-1-8 | mysql-1-1-2 | mysql-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       8 |         8 |      128 |           8 |            0 |                          127.88 |               977477.00 |              62475 |                            1553.00 |                62525 |                              6763.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        64 |     1024 |               1 |           1 |            0 |                         1021.64 |               978822.00 |             500455 |                            2105.00 |               499545 |                              7375.00 |
| mysql-1-1-2 | mysql-1-1-2 |                1 |        64 |     1024 |               1 |           8 |            0 |                         1022.82 |               977937.00 |             499398 |                            1586.00 |               500602 |                              7047.00 |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       253.26 |      0.37 |           4.70 |                  4.95 |
| mysql-1-1-2-1 |       246.34 |      0.35 |           4.73 |                  5.23 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       526.51 |      3.85 |           0.33 |                  0.33 |
| mysql-1-1-2-1 |       545.91 |      2.96 |           0.13 |                  0.14 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MySQL-1)
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

* SSB on MySQL: see [Example: SSB](Example-SSB.md).
* MySQL with several tenants: see [Example: Multi-Tenant](Example-Multi-Tenant.md).
