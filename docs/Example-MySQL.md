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
* Duration: 630s 
* Code: 1794642827
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
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
  * disk:1059762
  * datadisk:34785
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794642827

### Ingestion
* MySQL-1: 50 of 50 units ok

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794642827-6d5648fc8-4r45h: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

| DBMS      |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |    1 |       80.00 |           4.00 |           22.00 |         18.00 |           31.00 |              8 |         0 |             | None           |             0 | False         |               45.00 | False               |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         56 |            0.90 |             4724.50 |           1414.29 |          -1 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         56 |            0.90 |             4724.50 |           1414.29 |          -1 |

#### Query Completion per Phase

| phase       |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| mysql-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   mysql-1-1-1-1-1 |
|:----------------------------------------------------|------------------:|
| Pricing Summary Report (TPC-H Q1)                   |           6526.11 |
| Minimum Cost Supplier Query (TPC-H Q2)              |             86.37 |
| Shipping Priority (TPC-H Q3)                        |           1042.42 |
| Order Priority Checking Query (TPC-H Q4)            |            321.37 |
| Local Supplier Volume (TPC-H Q5)                    |            712.54 |
| Forecasting Revenue Change (TPC-H Q6)               |            774.25 |
| Volume Shipping Query (TPC-H Q7)                    |            525.57 |
| National Market Share (TPC-H Q8)                    |           2082.49 |
| Product Type Profit Measure (TPC-H Q9)              |           3483.40 |
| Returned Item Reporting Query (TPC-H Q10)           |            858.49 |
| Important Stock Identification (TPC-H Q11)          |            150.55 |
| Shipping Modes and Order Priority (TPC-H Q12)       |           1235.91 |
| Customer Distribution (TPC-H Q13)                   |           2328.53 |
| Promotion Effect Query (TPC-H Q14)                  |            938.97 |
| Top Supplier Query (TPC-H Q15)                      |          11296.17 |
| Parts/Supplier Relationship (TPC-H Q16)             |            332.37 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |            253.30 |
| Large Volume Customer (TPC-H Q18)                   |           1216.47 |
| Discounted Revenue (TPC-H Q19)                      |            131.11 |
| Potential Part Promotion (TPC-H Q20)                |            435.48 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |           3035.22 |
| Global Sales Opportunity Query (TPC-H Q22)          |             90.92 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
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
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
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
TPC-H Queries SF=10
* Type: tpch
* Duration: 4505s 
* Code: 1794648428
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 150Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* mysql-1-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1147171
  * datadisk:51262
  * volume_size:147G
  * volume_used:51G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794648428
* mysql-1-1-2-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1144849
  * datadisk:51262
  * volume_size:147G
  * volume_used:51G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794648428
* mysql-1-1-2-1-2 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1144849
  * datadisk:51262
  * volume_size:147G
  * volume_used:51G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794648428
* mysql-1-2-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1199116
  * datadisk:51264
  * volume_size:147G
  * volume_used:51G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794648428
* mysql-1-2-2-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1204072
  * datadisk:51264
  * volume_size:147G
  * volume_used:51G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794648428
* mysql-1-2-2-1-2 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1204072
  * datadisk:51264
  * volume_size:147G
  * volume_used:51G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794648428

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MySQL-1-2

### Data Parameters of Reused Volumes
* MySQL-1: DDL values of the volume: histograms=off, stats_sample_pages=default
* MySQL-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### Ingestion
* MySQL-1: 50 of 50 units ok

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794648428-6994bd77c7-l9ds6: 0
* bexhoma-sut-mysql-1-1794648428-6fc77f676d-8ww2l: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS MySQL-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS MySQL-1 - Experiment 2 Client 2: tpch (2 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS MySQL-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS MySQL-1 - Experiment 2 Client 2: tpch (2 pods)

### Loading

#### Per Run

| DBMS      |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |   10 |      660.00 |           5.00 |           24.00 |        146.00 |          481.00 |              8 |         0 |             | None           |             0 | False         |               54.55 | False               |
| MySQL-1-2 |                2 |   10 |      660.00 |           5.00 |           24.00 |        146.00 |          481.00 |              8 |         0 |             | None           |             0 | False         |               54.55 | True                |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 | 10.00 |               22 |                  22 |        632 |           11.53 |             3313.73 |           1253.16 |          -1 |
| mysql-1-1-2-1-1 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       1 | 10.00 |               22 |                  22 |        545 |            9.90 |             3691.35 |           1453.21 |          -1 |
| mysql-1-1-2-1-2 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       2 | 10.00 |               22 |                  22 |        544 |            9.53 |             3937.36 |           1455.88 |          -1 |
| mysql-1-2-1-1-1 | mysql-1-2-1 | mysql-1-2-1-1 |                2 |        1 |               1 |       1 | 10.00 |               22 |                  22 |        953 |           18.99 |             1905.29 |            831.06 |          -1 |
| mysql-1-2-2-1-1 | mysql-1-2-2 | mysql-1-2-2-1 |                2 |        2 |               1 |       1 | 10.00 |               22 |                  22 |        635 |           11.83 |             3095.32 |           1247.24 |          -1 |
| mysql-1-2-2-1-2 | mysql-1-2-2 | mysql-1-2-2-1 |                2 |        2 |               1 |       2 | 10.00 |               22 |                  22 |        634 |           11.94 |             3060.16 |           1249.21 |          -1 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |                  22 |        632 |           11.53 |             3313.73 |           1253.16 |          -1 |
| mysql-1-1-2 | mysql-1-1-2 |                1 |        2 |               1 |           2 | 10.00 |               44 |                  44 |        545 |            9.71 |             3812.37 |           2906.42 |          -1 |
| mysql-1-2-1 | mysql-1-2-1 |                2 |        1 |               1 |           1 | 10.00 |               22 |                  22 |        953 |           18.99 |             1905.29 |            831.06 |          -1 |
| mysql-1-2-2 | mysql-1-2-2 |                2 |        2 |               1 |           2 | 10.00 |               44 |                  44 |        635 |           11.89 |             3077.69 |           2494.49 |          -1 |

#### Query Completion per Phase

| phase       |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| mysql-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| mysql-1-1-2 |      2 | 2/2                                 | 2/2                                      | 2/2                            | 2/2                                        | 2/2                                | 2/2                                     | 2/2                                | 2/2                                | 2/2                                      | 2/2                                         | 2/2                                          | 2/2                                             | 2/2                                 | 2/2                                  | 2/2                              | 2/2                                       | 2/2                                        | 2/2                                 | 2/2                              | 2/2                                    | 2/2                                                   | 2/2                                          | yes        |
| mysql-1-2-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| mysql-1-2-2 |      2 | 2/2                                 | 2/2                                      | 2/2                            | 2/2                                        | 2/2                                | 2/2                                     | 2/2                                | 2/2                                | 2/2                                      | 2/2                                         | 2/2                                          | 2/2                                             | 2/2                                 | 2/2                                  | 2/2                              | 2/2                                       | 2/2                                        | 2/2                                 | 2/2                              | 2/2                                    | 2/2                                                   | 2/2                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   mysql-1-1-1-1-1 |   mysql-1-1-2-1-1 |   mysql-1-1-2-1-2 |   mysql-1-2-1-1-1 |   mysql-1-2-2-1-1 |   mysql-1-2-2-1-2 |
|:----------------------------------------------------|------------------:|------------------:|------------------:|------------------:|------------------:|------------------:|
| Pricing Summary Report (TPC-H Q1)                   |          84589.02 |          65420.26 |          65640.73 |         168530.82 |          77670.36 |          77100.80 |
| Minimum Cost Supplier Query (TPC-H Q2)              |            828.12 |           1205.66 |            683.77 |          12648.88 |            847.94 |            845.16 |
| Shipping Priority (TPC-H Q3)                        |          18415.39 |          16423.72 |          16049.73 |          82614.65 |          21910.28 |          21906.12 |
| Order Priority Checking Query (TPC-H Q4)            |           5316.30 |           4247.76 |           4164.97 |           5776.90 |           5910.35 |           5910.40 |
| Local Supplier Volume (TPC-H Q5)                    |          13106.80 |          14880.49 |          15002.80 |          19335.26 |          17738.01 |          18002.62 |
| Forecasting Revenue Change (TPC-H Q6)               |          12613.01 |          11557.21 |          11550.20 |          13828.80 |          10981.57 |          10498.01 |
| Volume Shipping Query (TPC-H Q7)                    |           9658.25 |           8527.60 |           8531.41 |          13392.52 |           9570.96 |           9741.60 |
| National Market Share (TPC-H Q8)                    |          33300.63 |          34918.32 |          35528.43 |          44908.55 |          37870.80 |          37832.96 |
| Product Type Profit Measure (TPC-H Q9)              |          66244.50 |          23962.92 |          23524.02 |         104453.99 |          28083.80 |          27909.38 |
| Returned Item Reporting Query (TPC-H Q10)           |          13589.29 |          12633.41 |          14213.60 |          18916.13 |          14441.00 |          13875.75 |
| Important Stock Identification (TPC-H Q11)          |           2878.46 |           2476.23 |           1631.48 |          15680.89 |           2163.86 |           2296.43 |
| Shipping Modes and Order Priority (TPC-H Q12)       |          13821.58 |          12552.79 |          13187.95 |          21528.58 |          13295.93 |          14264.66 |
| Customer Distribution (TPC-H Q13)                   |          58867.48 |          67486.69 |          64749.51 |          85762.15 |          66748.06 |          64752.89 |
| Promotion Effect Query (TPC-H Q14)                  |          11971.66 |          12402.61 |          12358.64 |          14215.52 |          10628.78 |          12055.97 |
| Top Supplier Query (TPC-H Q15)                      |         194893.73 |         174883.82 |         174166.97 |         231386.20 |         200901.77 |         200560.43 |
| Parts/Supplier Relationship (TPC-H Q16)             |           2151.93 |           2762.48 |           1976.78 |           5472.01 |           2408.47 |           2888.19 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |           2449.28 |           2979.76 |           2391.87 |           2939.55 |           4118.75 |           3969.49 |
| Large Volume Customer (TPC-H Q18)                   |          13246.80 |          14226.74 |          13452.92 |          19132.79 |          17794.00 |          17840.24 |
| Discounted Revenue (TPC-H Q19)                      |           2454.70 |           1140.46 |           1022.35 |           2186.56 |           2026.59 |           2025.12 |
| Potential Part Promotion (TPC-H Q20)                |           5616.62 |           2971.50 |           3170.65 |           6238.31 |           5088.85 |           5091.13 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |          41610.23 |          47969.78 |          49097.16 |          54573.79 |          74050.42 |          74147.54 |
| Global Sales Opportunity Query (TPC-H Q22)          |            861.55 |            779.79 |            871.27 |           1702.73 |           2054.99 |           1954.43 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      1051.05 |      5.70 |          19.27 |                 37.41 |
| mysql-1-1-2-1 |      1051.05 |      5.70 |          19.27 |                 37.41 |

### Loading phase: component data generator

| DBMS          | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|:-------------|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |
| mysql-1-1-2-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |        32.64 |      0.63 |           0.01 |                  1.14 |
| mysql-1-1-2-1 |        32.64 |      0.63 |           0.01 |                  1.14 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       527.91 |      1.02 |          21.16 |                 39.30 |
| mysql-1-1-2-1 |      1037.83 |      2.02 |          21.99 |                 40.13 |
| mysql-1-2-1-1 |       713.22 |      1.00 |          18.51 |                 18.52 |
| mysql-1-2-2-1 |      1197.06 |      2.01 |          19.31 |                 19.32 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |        38.13 |      0.61 |           0.41 |                  0.42 |
| mysql-1-1-2-1 |        48.89 |      1.38 |           0.38 |                  0.38 |
| mysql-1-2-1-1 |        23.07 |      1.01 |           0.38 |                  0.38 |
| mysql-1-2-2-1 |        46.21 |      2.04 |           0.37 |                  0.38 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-2-1-1 (bexhoma-metrics-mysql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-2-1-1 (bexhoma-metrics-mysql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-2-2-1 (bexhoma-metrics-mysql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-2-2-1 (bexhoma-metrics-mysql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
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
* Duration: 2478s 
* Code: 1794653069
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type ramdisk and size 150Gi.
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
  * disk:1192441
  * datadisk:51317
  * volume_size:129G
  * volume_used:51G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794653069

### Ingestion
* MySQL-1: 50 of 50 units ok

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794653069-694765b8cc-kmdp2: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

| DBMS      |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |   10 |      487.00 |           3.00 |           19.00 |        273.00 |          185.00 |              8 |         0 |             | None           |             0 | False         |               73.92 | False               |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 | 10.00 |               22 |                  22 |       1542 |           20.80 |             1738.72 |            513.62 |          -1 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |                  22 |       1542 |           20.80 |             1738.72 |            513.62 |          -1 |

#### Query Completion per Phase

| phase       |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| mysql-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   mysql-1-1-1-1-1 |
|:----------------------------------------------------|------------------:|
| Pricing Summary Report (TPC-H Q1)                   |          75487.51 |
| Minimum Cost Supplier Query (TPC-H Q2)              |           1146.55 |
| Shipping Priority (TPC-H Q3)                        |          24109.77 |
| Order Priority Checking Query (TPC-H Q4)            |           5214.38 |
| Local Supplier Volume (TPC-H Q5)                    |          12691.29 |
| Forecasting Revenue Change (TPC-H Q6)               |          11546.97 |
| Volume Shipping Query (TPC-H Q7)                    |          11291.19 |
| National Market Share (TPC-H Q8)                    |          32445.40 |
| Product Type Profit Measure (TPC-H Q9)              |          34556.03 |
| Returned Item Reporting Query (TPC-H Q10)           |          12460.54 |
| Important Stock Identification (TPC-H Q11)          |           2656.59 |
| Shipping Modes and Order Priority (TPC-H Q12)       |          24939.15 |
| Customer Distribution (TPC-H Q13)                   |         108874.11 |
| Promotion Effect Query (TPC-H Q14)                  |          23559.67 |
| Top Supplier Query (TPC-H Q15)                      |         834173.58 |
| Parts/Supplier Relationship (TPC-H Q16)             |          16272.60 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |          15638.09 |
| Large Volume Customer (TPC-H Q18)                   |          70473.72 |
| Discounted Revenue (TPC-H Q19)                      |          13973.59 |
| Potential Part Promotion (TPC-H Q20)                |          43134.68 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |         159465.74 |
| Global Sales Opportunity Query (TPC-H Q22)          |           1462.08 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      2286.88 |      7.47 |          59.39 |                 59.39 |

### Loading phase: component data generator

| DBMS          | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|:-------------|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |        35.13 |      0.17 |           0.01 |                  1.28 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      1537.21 |      1.18 |          60.31 |                 60.31 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |        21.55 |      0.58 |           0.38 |                  0.38 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                             1.57 |                            0.01 |                            0.10 |                              0.00 |

#### Benchmarking phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  0.99 |                             1.57 |                            0.00 |                            0.04 |                              0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
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
* Duration: 635s 
* Code: 1794719492
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * A TPC-H refresh stream (RF1+RF2) runs in parallel, with 3 pair(s) applied per round.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
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
  * disk:1081628
  * datadisk:34797
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794719492
* mysql-1-1-1-1-2 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1081628
  * datadisk:34797
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794719492
* mysql-1-1-1-1-3 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1081628
  * datadisk:34797
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794719492

### Ingestion
* MySQL-1: 50 of 50 units ok

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794719492-68c744d85d-gj79j: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

### Loading

#### Per Run

| DBMS      |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |    1 |       84.00 |           3.00 |           27.00 |         17.00 |           32.00 |              8 |         0 |             | None           |             0 | False         |               42.86 | False               |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         65 |            0.91 |             3954.77 |           1218.46 |          -1 |
| mysql-1-1-1-1-2 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       2 | 1.00 |               22 |                  22 |         64 |            0.92 |             3911.66 |           1237.50 |          -1 |
| mysql-1-1-1-1-3 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       3 | 1.00 |               22 |                  22 |         65 |            0.87 |             4122.63 |           1218.46 |          -1 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           3 | 1.00 |               66 |                  66 |         65 |            0.90 |             3995.32 |           3655.38 |          -1 |

#### Query Completion per Phase

| phase       |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| mysql-1-1-1 |      3 | 3/3                                 | 3/3                                      | 3/3                            | 3/3                                        | 3/3                                | 3/3                                     | 3/3                                | 3/3                                | 3/3                                      | 3/3                                         | 3/3                                          | 3/3                                             | 3/3                                 | 3/3                                  | 3/3                              | 3/3                                       | 3/3                                        | 3/3                                 | 3/3                              | 3/3                                    | 3/3                                                   | 3/3                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### tpch_refresh

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   pod_count | benchmark_begin     | benchmark_end       |   benchmark_duration |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|------------:|:--------------------|:--------------------|---------------------:|
| mysql-1-1-1-2-1 | mysql-1-1-1 | mysql-1-1-1-2 |                1 |        1 |               2 |           1 | 2026-11-15 06:20:39 | 2026-11-15 06:20:49 |                   10 |

### Latency of Timer Execution [ms]
| Queries                                             |   mysql-1-1-1-1-1 |   mysql-1-1-1-1-2 |   mysql-1-1-1-1-3 |
|:----------------------------------------------------|------------------:|------------------:|------------------:|
| Pricing Summary Report (TPC-H Q1)                   |           6750.32 |           7178.54 |           7410.71 |
| Minimum Cost Supplier Query (TPC-H Q2)              |             67.27 |             70.19 |             69.81 |
| Shipping Priority (TPC-H Q3)                        |           1422.60 |           1916.40 |           1749.81 |
| Order Priority Checking Query (TPC-H Q4)            |            365.44 |            819.87 |            599.04 |
| Local Supplier Volume (TPC-H Q5)                    |           1348.31 |           1359.48 |           1359.97 |
| Forecasting Revenue Change (TPC-H Q6)               |           1002.33 |            839.34 |            846.87 |
| Volume Shipping Query (TPC-H Q7)                    |            710.76 |           1178.49 |           1177.40 |
| National Market Share (TPC-H Q8)                    |           3853.07 |           3586.50 |           3798.56 |
| Product Type Profit Measure (TPC-H Q9)              |           1909.69 |           2371.57 |           2739.92 |
| Returned Item Reporting Query (TPC-H Q10)           |           1749.55 |            875.41 |            852.23 |
| Important Stock Identification (TPC-H Q11)          |            158.31 |            122.18 |            101.49 |
| Shipping Modes and Order Priority (TPC-H Q12)       |           1170.79 |           1171.96 |           1199.51 |
| Customer Distribution (TPC-H Q13)                   |           4584.49 |           4406.91 |           4227.74 |
| Promotion Effect Query (TPC-H Q14)                  |           1004.80 |            997.32 |           1015.45 |
| Top Supplier Query (TPC-H Q15)                      |          23100.76 |          21973.68 |          22309.14 |
| Parts/Supplier Relationship (TPC-H Q16)             |            405.15 |            346.17 |            212.74 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |            212.06 |            293.33 |            274.31 |
| Large Volume Customer (TPC-H Q18)                   |           1284.48 |           1314.04 |           1317.38 |
| Discounted Revenue (TPC-H Q19)                      |             98.10 |             84.68 |             75.38 |
| Potential Part Promotion (TPC-H Q20)                |            293.80 |            176.69 |            189.01 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |           5730.39 |           5079.64 |           5449.01 |
| Global Sales Opportunity Query (TPC-H Q22)          |            120.51 |            144.79 |            111.66 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
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
* A pool that is too small makes the persistent-storage runs very slow: the data of SF 10 does not fit into 8G, so queries read it again and again from the (network) volume. TPC-H SF 10 on the storage volume took 2952 s for Q9, Q13, Q15, Q18 and Q21 with 8G (Q15 timed out) and about 1050 s with 32G (Q18 and Q21 about 9 times faster); larger temporary-table limits (`temptable_max_ram`, `tmp_table_size`) made no difference. The storage runs below therefore set 32G. TPC-DS at SF 10 also sorts and joins a lot: with the default 256K for `sort_buffer_size` and `join_buffer_size` MySQL wrote thousands of merge passes to temporary files in `/mysqltmp`, and one query failed with `No space left on device` on the 32Gi tmpfs. Its storage run therefore sets both buffers and the temporary-table limits and a `mysqltmp` tmpfs of 72Gi: a 48Gi tmpfs ran full (`No space left on device`) when two clients ran the rollup queries (Q22) at the same time. The tmpfs is RAM and counts against the memory limit `-lr 128Gi`; the pool of 32G, a few GB for the server and the buffers of two clients and the 72Gi tmpfs stay below it (the rollup queries Q18, Q22, Q27, Q36, Q67, Q70 and Q86 with two clients peaked at 62 GB of RAM in the SUT).
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
* Duration: 1758s 
* Code: 1794655623
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
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
  * disk:1394132
  * datadisk:37564
  * volume_size:1.8T
  * volume_used:1.4T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794655623

### Ingestion
* MySQL-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794655623-5cd8cf6474-nbshf: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

| DBMS      |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |    1 |      330.00 |          38.00 |            1.00 |        112.00 |          170.00 |              8 |         0 |             | None           |             0 | False         |               10.91 | False               |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               99 |                  99 |        936 |            1.05 |             3474.47 |            380.77 |          -1 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        936 |            1.05 |             3474.47 |            380.77 |          -1 |

#### Query Completion per Phase

| phase       |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mysql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   mysql-1-1-1-1-1 |
|:--------------|------------------:|
| TPC-DS Q1     |             57.65 |
| TPC-DS Q2     |           9747.50 |
| TPC-DS Q3     |             56.63 |
| TPC-DS Q4     |         150431.73 |
| TPC-DS Q5     |          87076.73 |
| TPC-DS Q6     |           1206.26 |
| TPC-DS Q7     |           2721.15 |
| TPC-DS Q8     |           1513.70 |
| TPC-DS Q9     |          17729.39 |
| TPC-DS Q10    |           1230.65 |
| TPC-DS Q11    |         113988.58 |
| TPC-DS Q12    |            941.79 |
| TPC-DS Q13    |           5349.16 |
| TPC-DS Q14a+b |         145006.56 |
| TPC-DS Q15    |           1107.97 |
| TPC-DS Q16    |           1407.54 |
| TPC-DS Q17    |           4652.49 |
| TPC-DS Q18    |           6347.85 |
| TPC-DS Q19    |           2874.45 |
| TPC-DS Q20    |           1355.99 |
| TPC-DS Q21    |           3356.81 |
| TPC-DS Q22    |          54565.37 |
| TPC-DS Q23a+b |          80488.57 |
| TPC-DS Q24a+b |           1941.19 |
| TPC-DS Q25    |            210.96 |
| TPC-DS Q26    |            602.52 |
| TPC-DS Q27    |            562.58 |
| TPC-DS Q28    |           3487.84 |
| TPC-DS Q29    |             60.67 |
| TPC-DS Q30    |            445.55 |
| TPC-DS Q31    |          13247.53 |
| TPC-DS Q32    |            244.61 |
| TPC-DS Q33    |            592.18 |
| TPC-DS Q34    |           1484.85 |
| TPC-DS Q35    |          15477.08 |
| TPC-DS Q36    |           3289.66 |
| TPC-DS Q37    |             11.40 |
| TPC-DS Q38    |           7177.63 |
| TPC-DS Q39a+b |           1207.98 |
| TPC-DS Q40    |            128.35 |
| TPC-DS Q41    |           1006.00 |
| TPC-DS Q42    |             70.28 |
| TPC-DS Q43    |              1.78 |
| TPC-DS Q44    |              5.56 |
| TPC-DS Q45    |            166.58 |
| TPC-DS Q46    |            538.59 |
| TPC-DS Q47    |           9597.35 |
| TPC-DS Q48    |           1438.56 |
| TPC-DS Q49    |            146.02 |
| TPC-DS Q50    |             25.02 |
| TPC-DS Q51    |           7951.54 |
| TPC-DS Q52    |             60.28 |
| TPC-DS Q53    |            167.53 |
| TPC-DS Q54    |           2693.72 |
| TPC-DS Q55    |             35.11 |
| TPC-DS Q56    |            423.60 |
| TPC-DS Q57    |           5050.61 |
| TPC-DS Q58    |           5871.62 |
| TPC-DS Q59    |           5754.25 |
| TPC-DS Q60    |            410.17 |
| TPC-DS Q61    |              2.26 |
| TPC-DS Q62    |           2738.29 |
| TPC-DS Q63    |            213.33 |
| TPC-DS Q64    |            765.71 |
| TPC-DS Q65    |           7272.32 |
| TPC-DS Q66    |           2434.93 |
| TPC-DS Q67    |           8677.36 |
| TPC-DS Q68    |            557.78 |
| TPC-DS Q69    |              3.11 |
| TPC-DS Q70    |          12373.32 |
| TPC-DS Q71    |            687.79 |
| TPC-DS Q72    |          12187.04 |
| TPC-DS Q73    |            842.27 |
| TPC-DS Q74    |           6705.65 |
| TPC-DS Q75    |           2254.26 |
| TPC-DS Q76    |            479.70 |
| TPC-DS Q77    |           8855.17 |
| TPC-DS Q78    |          15438.24 |
| TPC-DS Q79    |           4110.23 |
| TPC-DS Q80    |           9818.36 |
| TPC-DS Q81    |           1895.91 |
| TPC-DS Q82    |             27.54 |
| TPC-DS Q83    |            622.01 |
| TPC-DS Q84    |             60.07 |
| TPC-DS Q85    |             81.54 |
| TPC-DS Q86    |           1330.92 |
| TPC-DS Q87    |           7237.69 |
| TPC-DS Q88    |           2413.87 |
| TPC-DS Q89    |            186.71 |
| TPC-DS Q90    |            334.40 |
| TPC-DS Q91    |             17.82 |
| TPC-DS Q92    |             50.15 |
| TPC-DS Q93    |             51.63 |
| TPC-DS Q94    |            418.57 |
| TPC-DS Q95    |           3640.85 |
| TPC-DS Q96    |            166.50 |
| TPC-DS Q97    |           7452.24 |
| TPC-DS Q98    |            982.53 |
| TPC-DS Q99    |          10532.52 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
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
* Duration: 2263s 
* Code: 1794657554
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
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
  * disk:1294706
  * datadisk:45103
  * volume_size:1.8T
  * volume_used:1.3T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem', '--temptable_max_ram=32G', '--tmp_table_size=32G', '--max_heap_table_size=32G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794657554

### Ingestion
* MySQL-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794657554-5845d9487d-857dp: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

| DBMS      |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |    3 |      515.00 |           3.00 |            1.00 |        173.00 |          328.00 |              8 |         0 |             | None           |             0 | False         |               20.97 | False               |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 | 3.00 |               99 |                  99 |       1184 |            2.07 |             5288.46 |            903.04 |          -1 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |       1184 |            2.07 |             5288.46 |            903.04 |          -1 |

#### Query Completion per Phase

| phase       |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mysql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   mysql-1-1-1-1-1 |
|:--------------|------------------:|
| TPC-DS Q1     |             53.85 |
| TPC-DS Q2     |           8689.84 |
| TPC-DS Q3     |             24.73 |
| TPC-DS Q4     |          66857.42 |
| TPC-DS Q5     |          27742.70 |
| TPC-DS Q6     |           2550.54 |
| TPC-DS Q7     |           4173.17 |
| TPC-DS Q8     |           1767.25 |
| TPC-DS Q9     |          10968.83 |
| TPC-DS Q10    |            738.96 |
| TPC-DS Q11    |          49270.66 |
| TPC-DS Q12    |            850.06 |
| TPC-DS Q13    |           6265.00 |
| TPC-DS Q14a+b |         155970.59 |
| TPC-DS Q15    |            680.66 |
| TPC-DS Q16    |             83.09 |
| TPC-DS Q17    |           1209.08 |
| TPC-DS Q18    |           3103.98 |
| TPC-DS Q19    |           1250.82 |
| TPC-DS Q20    |           1392.22 |
| TPC-DS Q21    |          76114.29 |
| TPC-DS Q22    |          18486.31 |
| TPC-DS Q23a+b |         109298.66 |
| TPC-DS Q24a+b |           3462.71 |
| TPC-DS Q25    |            408.38 |
| TPC-DS Q26    |            762.01 |
| TPC-DS Q27    |            840.53 |
| TPC-DS Q28    |          11337.73 |
| TPC-DS Q29    |            330.89 |
| TPC-DS Q30    |            450.74 |
| TPC-DS Q31    |          36223.37 |
| TPC-DS Q32    |            337.48 |
| TPC-DS Q33    |           1537.96 |
| TPC-DS Q34    |           3825.56 |
| TPC-DS Q35    |          68080.13 |
| TPC-DS Q36    |          18694.29 |
| TPC-DS Q37    |             16.32 |
| TPC-DS Q38    |          21692.17 |
| TPC-DS Q39a+b |           4699.22 |
| TPC-DS Q40    |            414.77 |
| TPC-DS Q41    |           5244.07 |
| TPC-DS Q42    |            166.23 |
| TPC-DS Q43    |              1.84 |
| TPC-DS Q44    |           2027.94 |
| TPC-DS Q45    |            353.83 |
| TPC-DS Q46    |           3015.68 |
| TPC-DS Q47    |          17701.34 |
| TPC-DS Q48    |           3093.40 |
| TPC-DS Q49    |            378.15 |
| TPC-DS Q50    |             94.92 |
| TPC-DS Q51    |          16777.14 |
| TPC-DS Q52    |             46.28 |
| TPC-DS Q53    |            640.48 |
| TPC-DS Q54    |           7891.20 |
| TPC-DS Q55    |             58.27 |
| TPC-DS Q56    |            706.20 |
| TPC-DS Q57    |           9291.81 |
| TPC-DS Q58    |          15604.77 |
| TPC-DS Q59    |          14906.58 |
| TPC-DS Q60    |            794.70 |
| TPC-DS Q61    |              2.91 |
| TPC-DS Q62    |           7686.07 |
| TPC-DS Q63    |            554.16 |
| TPC-DS Q64    |            906.46 |
| TPC-DS Q65    |          16984.68 |
| TPC-DS Q66    |           6795.52 |
| TPC-DS Q67    |          23141.54 |
| TPC-DS Q68    |            724.92 |
| TPC-DS Q69    |           1327.10 |
| TPC-DS Q70    |          36633.33 |
| TPC-DS Q71    |           2129.16 |
| TPC-DS Q72    |          40649.27 |
| TPC-DS Q73    |           3916.23 |
| TPC-DS Q74    |          15126.49 |
| TPC-DS Q75    |           5235.39 |
| TPC-DS Q76    |           1227.55 |
| TPC-DS Q77    |          25276.60 |
| TPC-DS Q78    |          34016.54 |
| TPC-DS Q79    |           2595.38 |
| TPC-DS Q80    |          14230.98 |
| TPC-DS Q81    |          22093.01 |
| TPC-DS Q82    |             26.96 |
| TPC-DS Q83    |           1948.83 |
| TPC-DS Q84    |            123.97 |
| TPC-DS Q85    |            277.39 |
| TPC-DS Q86    |           2978.17 |
| TPC-DS Q87    |          19688.28 |
| TPC-DS Q88    |           8841.41 |
| TPC-DS Q89    |             13.05 |
| TPC-DS Q90    |           1017.55 |
| TPC-DS Q91    |             41.09 |
| TPC-DS Q92    |            353.11 |
| TPC-DS Q93    |            147.57 |
| TPC-DS Q94    |           1135.52 |
| TPC-DS Q95    |          10376.49 |
| TPC-DS Q96    |            538.58 |
| TPC-DS Q97    |          15601.51 |
| TPC-DS Q98    |           3081.86 |
| TPC-DS Q99    |          18091.33 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       726.61 |      3.88 |           8.22 |                 15.24 |

### Loading phase: component data generator

| DBMS          | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|:-------------|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |        10.20 |      0.07 |           0.01 |                  2.24 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      1120.96 |      1.01 |          14.91 |                 21.94 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |        25.68 |      0.43 |           0.33 |                  0.34 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
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
 [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                             1.43 |                            0.00 |                            0.03 |                              0.00 |

#### Benchmarking phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                             1.46 |                            0.00 |                            0.04 |                              0.00 |

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
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  --set deployment[bexhoma-deployment-mysql].volume[mysqltmp].sizeLimit=72Gi \
  --set deployment[bexhoma-deployment-mysql].container[dbms].sort_buffer_size=32M \
  --set deployment[bexhoma-deployment-mysql].container[dbms].join_buffer_size=64M \
  --set deployment[bexhoma-deployment-mysql].container[dbms].tmp_table_size=1G \
  --set deployment[bexhoma-deployment-mysql].container[dbms].max_heap_table_size=1G \
  --set deployment[bexhoma-deployment-mysql].container[dbms].temptable_max_ram=4G \
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
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 2263s 
* Code: 1794657554
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
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
  * disk:1294706
  * datadisk:45103
  * volume_size:1.8T
  * volume_used:1.3T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem', '--temptable_max_ram=32G', '--tmp_table_size=32G', '--max_heap_table_size=32G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794657554

### Ingestion
* MySQL-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794657554-5845d9487d-857dp: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

| DBMS      |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |    3 |      515.00 |           3.00 |            1.00 |        173.00 |          328.00 |              8 |         0 |             | None           |             0 | False         |               20.97 | False               |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 | 3.00 |               99 |                  99 |       1184 |            2.07 |             5288.46 |            903.04 |          -1 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |       1184 |            2.07 |             5288.46 |            903.04 |          -1 |

#### Query Completion per Phase

| phase       |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mysql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   mysql-1-1-1-1-1 |
|:--------------|------------------:|
| TPC-DS Q1     |             53.85 |
| TPC-DS Q2     |           8689.84 |
| TPC-DS Q3     |             24.73 |
| TPC-DS Q4     |          66857.42 |
| TPC-DS Q5     |          27742.70 |
| TPC-DS Q6     |           2550.54 |
| TPC-DS Q7     |           4173.17 |
| TPC-DS Q8     |           1767.25 |
| TPC-DS Q9     |          10968.83 |
| TPC-DS Q10    |            738.96 |
| TPC-DS Q11    |          49270.66 |
| TPC-DS Q12    |            850.06 |
| TPC-DS Q13    |           6265.00 |
| TPC-DS Q14a+b |         155970.59 |
| TPC-DS Q15    |            680.66 |
| TPC-DS Q16    |             83.09 |
| TPC-DS Q17    |           1209.08 |
| TPC-DS Q18    |           3103.98 |
| TPC-DS Q19    |           1250.82 |
| TPC-DS Q20    |           1392.22 |
| TPC-DS Q21    |          76114.29 |
| TPC-DS Q22    |          18486.31 |
| TPC-DS Q23a+b |         109298.66 |
| TPC-DS Q24a+b |           3462.71 |
| TPC-DS Q25    |            408.38 |
| TPC-DS Q26    |            762.01 |
| TPC-DS Q27    |            840.53 |
| TPC-DS Q28    |          11337.73 |
| TPC-DS Q29    |            330.89 |
| TPC-DS Q30    |            450.74 |
| TPC-DS Q31    |          36223.37 |
| TPC-DS Q32    |            337.48 |
| TPC-DS Q33    |           1537.96 |
| TPC-DS Q34    |           3825.56 |
| TPC-DS Q35    |          68080.13 |
| TPC-DS Q36    |          18694.29 |
| TPC-DS Q37    |             16.32 |
| TPC-DS Q38    |          21692.17 |
| TPC-DS Q39a+b |           4699.22 |
| TPC-DS Q40    |            414.77 |
| TPC-DS Q41    |           5244.07 |
| TPC-DS Q42    |            166.23 |
| TPC-DS Q43    |              1.84 |
| TPC-DS Q44    |           2027.94 |
| TPC-DS Q45    |            353.83 |
| TPC-DS Q46    |           3015.68 |
| TPC-DS Q47    |          17701.34 |
| TPC-DS Q48    |           3093.40 |
| TPC-DS Q49    |            378.15 |
| TPC-DS Q50    |             94.92 |
| TPC-DS Q51    |          16777.14 |
| TPC-DS Q52    |             46.28 |
| TPC-DS Q53    |            640.48 |
| TPC-DS Q54    |           7891.20 |
| TPC-DS Q55    |             58.27 |
| TPC-DS Q56    |            706.20 |
| TPC-DS Q57    |           9291.81 |
| TPC-DS Q58    |          15604.77 |
| TPC-DS Q59    |          14906.58 |
| TPC-DS Q60    |            794.70 |
| TPC-DS Q61    |              2.91 |
| TPC-DS Q62    |           7686.07 |
| TPC-DS Q63    |            554.16 |
| TPC-DS Q64    |            906.46 |
| TPC-DS Q65    |          16984.68 |
| TPC-DS Q66    |           6795.52 |
| TPC-DS Q67    |          23141.54 |
| TPC-DS Q68    |            724.92 |
| TPC-DS Q69    |           1327.10 |
| TPC-DS Q70    |          36633.33 |
| TPC-DS Q71    |           2129.16 |
| TPC-DS Q72    |          40649.27 |
| TPC-DS Q73    |           3916.23 |
| TPC-DS Q74    |          15126.49 |
| TPC-DS Q75    |           5235.39 |
| TPC-DS Q76    |           1227.55 |
| TPC-DS Q77    |          25276.60 |
| TPC-DS Q78    |          34016.54 |
| TPC-DS Q79    |           2595.38 |
| TPC-DS Q80    |          14230.98 |
| TPC-DS Q81    |          22093.01 |
| TPC-DS Q82    |             26.96 |
| TPC-DS Q83    |           1948.83 |
| TPC-DS Q84    |            123.97 |
| TPC-DS Q85    |            277.39 |
| TPC-DS Q86    |           2978.17 |
| TPC-DS Q87    |          19688.28 |
| TPC-DS Q88    |           8841.41 |
| TPC-DS Q89    |             13.05 |
| TPC-DS Q90    |           1017.55 |
| TPC-DS Q91    |             41.09 |
| TPC-DS Q92    |            353.11 |
| TPC-DS Q93    |            147.57 |
| TPC-DS Q94    |           1135.52 |
| TPC-DS Q95    |          10376.49 |
| TPC-DS Q96    |            538.58 |
| TPC-DS Q97    |          15601.51 |
| TPC-DS Q98    |           3081.86 |
| TPC-DS Q99    |          18091.33 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       726.61 |      3.88 |           8.22 |                 15.24 |

### Loading phase: component data generator

| DBMS          | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|:-------------|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |        10.20 |      0.07 |           0.01 |                  2.24 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      1120.96 |      1.01 |          14.91 |                 21.94 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |        25.68 |      0.43 |           0.33 |                  0.34 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
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
 [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                             1.43 |                            0.00 |                            0.03 |                              0.00 |

#### Benchmarking phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                             1.46 |                            0.00 |                            0.04 |                              0.00 |

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
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              - waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.6s (0 kubectl calls 0.0s, 17 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 17 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 7.4s (0 kubectl calls 0.0s, 17 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.7s (0 kubectl calls 0.0s, 17 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 17 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.3s (0 kubectl calls 0.0s, 17 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.6s (0 kubectl calls 0.0s, 17 API requests 0.5s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 17 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 17 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.8s (0 kubectl calls 0.0s, 17 API requests 1.0s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 17 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 17 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 7.4s (0 kubectl calls 0.0s, 17 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 2.0s (0 kubectl calls 0.0s, 17 API requests 1.0s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.9s (0 kubectl calls 0.0s, 17 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.7s (0 kubectl calls 0.0s, 17 API requests 0.9s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.9s (0 kubectl calls 0.0s, 17 API requests 0.9s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.7s (0 kubectl calls 0.0s, 17 API requests 0.9s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.0s (0 kubectl calls 0.0s, 17 API requests 1.0s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.8s (0 kubectl calls 0.0s, 17 API requests 1.0s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.1s (0 kubectl calls 0.0s, 17 API requests 1.0s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.8s (0 kubectl calls 0.0s, 17 API requests 1.0s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 7.3s (0 kubectl calls 0.0s, 17 API requests 0.7s)
- waiting 30s -               : done
mysql-1-2-1-1                 : wrote benchmarking_timespans to D:/data/benchmarks/1794659963/mysql-1-2-1-1.config
mysql-1-2-1-1                 : showing benchmarker times
mysql-1-2-1-1                 : benchmarker timespan job from 1794676887 to 1794684509
mysql-1-2-1-1                 : benchmarker timespan pods from 1794676892 to 1794684496
mysql-1-2-1-1                 : benchmarker timespan (start to end single container [s]) = 7604
mysql-1-2-1-1                 : benchmarker times (start/end per pod and container) = [(1794676892, 1794684496)]
mysql-1-2-1-1                 : found and updated times {'benchmarker': [(1794676892, 1794684496)]}
mysql-1-2-1-1                 : needs monitoring (common metrics) for deployment sut
mysql-1-2-1-1                 : collecting execution metrics of SUT at connection mysql-1-2-1-1
mysql-1-2-1-1                 : collecting metrics of benchmarker at connection mysql-1-2-1-1
MySQL-1                       : get size via pod bexhoma-sut-mysql-1-1794659963-6d68b45cdd-v8hng and write to pvc bexhoma-storage-my-nvme-tpcds-10
mysql-1-2-1-1                 : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"(.*)mysql-1-1794659963(.*)", namespace="perdelt", container="dbms"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"(.*)mysql-1-1794659963(.*)", namespace="perdelt", container="dbms"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
mysql-1-2-1-1                 : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"bexhoma-benchmarker-mysql-1-1794659963-2-1-1-[a-z0-9]{5}", namespace="perdelt", container="dbmsbenchmarker"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"bexhoma-benchmarker-mysql-1-1794659963-2-1-1-[a-z0-9]{5}", namespace="perdelt", container="dbmsbenchmarker"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
mysql-1-2-1-1                 : WARNING metric missing for benchmarking: CPU Throttling Rate [s/s]
mysql-1-2-1-1                 : WARNING metric missing for benchmarking: CPU Throttled Time [s]
Experiment                    : fetched 2 metric sets in 11s (2 at once, 0 repeated, 0 follow-up actions; 4 kubectl calls 19.0s, 0 API requests 0.0s)
Loop pass                     : took 18.9s (9 kubectl calls 24.6s, 24 API requests 1.7s)
Experiment                    : Reset experiment counter. This is first run of client number 2.
Experiment                    : Round pod counter bexhoma-benchmarker-podcount-round-2-2-MySQL-1-1794659963 initialized to 2.
MySQL-1                       : benchmarks done 1 of 2. This will be client 2
mysql-1-2-2-1                 : start benchmarking (benchmark_run=1)
mysql-1-2-2-1                 : needs monitoring (common metrics) for deployment sut
MySQL-1                       : get size via pod bexhoma-sut-mysql-1-1794659963-6d68b45cdd-v8hng and write to pvc bexhoma-storage-my-nvme-tpcds-10
MySQL-1                       : benchmarking results in folder D:\data\benchmarks/1794659963
MySQL-1                       : submitted benchmarker job in 30.0s (3 kubectl calls 3.5s, 24 API requests 2.3s)
Loop pass                     : took 31.2s (3 kubectl calls 3.5s, 44 API requests 3.5s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 2.4s (0 kubectl calls 0.0s, 20 API requests 1.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.0s (0 kubectl calls 0.0s, 18 API requests 1.0s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.8s (0 kubectl calls 0.0s, 18 API requests 1.0s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.0s (0 kubectl calls 0.0s, 18 API requests 1.0s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.7s (0 kubectl calls 0.0s, 18 API requests 0.9s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.9s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 7.8s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.6s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.6s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.6s (0 kubectl calls 0.0s, 18 API requests 0.5s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 7.8s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.6s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.6s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 18 API requests 0.5s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 7.8s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.6s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 7.8s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.6s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.8s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 7.8s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.6s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.6s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.6s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.8s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.6s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 4.3s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.6s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.6s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.7s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.8s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 7.8s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.7s (0 kubectl calls 0.0s, 18 API requests 0.9s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.7s (0 kubectl calls 0.0s, 18 API requests 0.9s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.8s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.6s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.8s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.6s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 7.9s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 18 API requests 0.5s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.6s (0 kubectl calls 0.0s, 18 API requests 0.5s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 18 API requests 0.5s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.6s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 4.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.5s (0 kubectl calls 0.0s, 18 API requests 0.5s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.8s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 7.9s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.7s (0 kubectl calls 0.0s, 18 API requests 0.9s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.8s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.8s (0 kubectl calls 0.0s, 18 API requests 1.1s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.9s (0 kubectl calls 0.0s, 18 API requests 1.1s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.0s (0 kubectl calls 0.0s, 18 API requests 0.9s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.8s (0 kubectl calls 0.0s, 18 API requests 1.0s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 7.8s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.9s (0 kubectl calls 0.0s, 18 API requests 1.0s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.0s (0 kubectl calls 0.0s, 18 API requests 1.0s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.7s (0 kubectl calls 0.0s, 18 API requests 0.9s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.9s (0 kubectl calls 0.0s, 18 API requests 0.9s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.7s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.1s (0 kubectl calls 0.0s, 18 API requests 1.0s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.8s (0 kubectl calls 0.0s, 18 API requests 1.0s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.0s (0 kubectl calls 0.0s, 18 API requests 1.0s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 5.0s (0 kubectl calls 0.0s, 18 API requests 1.1s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 2.1s (0 kubectl calls 0.0s, 18 API requests 1.0s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.8s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.7s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.1s (0 kubectl calls 0.0s, 18 API requests 1.0s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.9s (0 kubectl calls 0.0s, 18 API requests 1.0s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.1s (0 kubectl calls 0.0s, 18 API requests 1.0s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.8s (0 kubectl calls 0.0s, 18 API requests 0.9s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.8s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 7.8s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.7s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.6s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.6s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.8s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 8.1s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.6s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.5s (0 kubectl calls 0.0s, 18 API requests 0.5s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.6s (0 kubectl calls 0.0s, 18 API requests 0.5s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.6s (0 kubectl calls 0.0s, 18 API requests 0.5s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 7.9s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.0s (0 kubectl calls 0.0s, 18 API requests 0.9s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.6s (0 kubectl calls 0.0s, 18 API requests 0.5s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.7s (0 kubectl calls 0.0s, 18 API requests 0.9s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 7.7s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.6s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.6s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 18 API requests 0.5s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.8s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 5.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.6s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.6s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.6s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.8s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 7.8s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.8s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.8s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.9s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 18 API requests 0.5s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 7.8s (0 kubectl calls 0.0s, 18 API requests 0.9s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.7s (0 kubectl calls 0.0s, 18 API requests 0.9s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.6s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 3.7s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.6s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.5s (0 kubectl calls 0.0s, 18 API requests 0.5s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.6s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.7s (0 kubectl calls 0.0s, 18 API requests 0.9s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.6s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.6s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 7.8s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.6s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.8s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.6s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.8s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.5s (0 kubectl calls 0.0s, 18 API requests 0.5s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 7.9s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.9s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.7s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.8s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.8s (0 kubectl calls 0.0s, 18 API requests 1.0s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.0s (0 kubectl calls 0.0s, 18 API requests 0.9s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.8s (0 kubectl calls 0.0s, 18 API requests 1.0s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.0s (0 kubectl calls 0.0s, 18 API requests 1.0s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.8s (0 kubectl calls 0.0s, 18 API requests 1.0s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 3.3s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.9s (0 kubectl calls 0.0s, 18 API requests 0.9s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.9s (0 kubectl calls 0.0s, 18 API requests 1.1s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.0s (0 kubectl calls 0.0s, 18 API requests 0.9s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.8s (0 kubectl calls 0.0s, 18 API requests 1.0s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.1s (0 kubectl calls 0.0s, 18 API requests 1.0s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.7s (0 kubectl calls 0.0s, 18 API requests 1.0s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.0s (0 kubectl calls 0.0s, 18 API requests 0.9s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.8s (0 kubectl calls 0.0s, 18 API requests 1.0s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 7.9s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.8s (0 kubectl calls 0.0s, 18 API requests 1.0s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.1s (0 kubectl calls 0.0s, 18 API requests 1.0s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.6s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.6s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.8s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 18 API requests 0.7s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 7.8s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.8s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.6s (0 kubectl calls 0.0s, 18 API requests 0.8s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
MySQL-1                       : has running benchmarks
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 18 API requests 0.6s)
- waiting 30s -               : done
mysql-1-2-2-1                 : wrote benchmarking_timespans to D:/data/benchmarks/1794659963/mysql-1-2-2-1.config
mysql-1-2-2-1                 : showing benchmarker times
mysql-1-2-2-1                 : benchmarker timespan job from 1794684554 to 1794692375
mysql-1-2-2-1                 : benchmarker timespan pods from 1794684566 to 1794692346
mysql-1-2-2-1                 : benchmarker timespan (start to end single container [s]) = 7780
mysql-1-2-2-1                 : benchmarker times (start/end per pod and container) = [(1794684566, 1794692345), (1794684567, 1794692346)]
mysql-1-2-2-1                 : found and updated times {'benchmarker': [(1794684566, 1794692345), (1794684567, 1794692346)]}
mysql-1-2-2-1                 : needs monitoring (common metrics) for deployment sut
mysql-1-2-2-1                 : collecting execution metrics of SUT at connection mysql-1-2-2-1
mysql-1-2-2-1                 : collecting metrics of benchmarker at connection mysql-1-2-2-1
MySQL-1                       : get size via pod bexhoma-sut-mysql-1-1794659963-6d68b45cdd-v8hng and write to pvc bexhoma-storage-my-nvme-tpcds-10
mysql-1-2-2-1                 : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"(.*)mysql-1-1794659963(.*)", namespace="perdelt", container="dbms"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"(.*)mysql-1-1794659963(.*)", namespace="perdelt", container="dbms"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
mysql-1-2-2-1                 : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"bexhoma-benchmarker-mysql-1-1794659963-2-2-1-[a-z0-9]{5}", namespace="perdelt", container="dbmsbenchmarker"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"bexhoma-benchmarker-mysql-1-1794659963-2-2-1-[a-z0-9]{5}", namespace="perdelt", container="dbmsbenchmarker"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
mysql-1-2-2-1                 : WARNING metric missing for benchmarking: CPU Throttling Rate [s/s]
mysql-1-2-2-1                 : WARNING metric missing for benchmarking: CPU Throttled Time [s]
Experiment                    : fetched 2 metric sets in 11s (2 at once, 0 repeated, 0 follow-up actions; 4 kubectl calls 19.0s, 0 API requests 0.0s)
Loop pass                     : took 21.2s (11 kubectl calls 26.8s, 28 API requests 1.6s)
MySQL-1                       : can be stopped
MySQL-1                       : had 0 restarts at worker bexhoma-sut-mysql-1-1794659963-6d68b45cdd-v8hng
Loop pass                     : took 5.4s (4 kubectl calls 4.1s, 30 API requests 0.9s)
Experiment                    : ends at 2026-11-14 22:39:56.447755 (328937.3569288) - 32430.21s total
Experiment                    : join results...done!
Experiment                    : build evaluation cube...done!
Experiment                    : downloading partial results
Experiment                    : uploading full results
Experiment                    : uploading workload file
Result workflow complete

## Show Summary

### Workload
TPC-DS Queries SF=10
* Type: tpcds
* Duration: 32431s 
* Code: 1794659963
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 150Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'volume': 'mysqltmp', 'field': 'sizeLimit', 'target': 'volume'}, '72Gi'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'sort_buffer_size', 'target': 'container'}, '32M'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'join_buffer_size', 'target': 'container'}, '64M'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'tmp_table_size', 'target': 'container'}, '1G'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'max_heap_table_size', 'target': 'container'}, '1G'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'temptable_max_ram', 'target': 'container'}, '4G')].
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* mysql-1-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1199369
  * datadisk:78402
  * volume_size:147G
  * volume_used:77G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem', '--sort_buffer_size=32M', '--join_buffer_size=64M', '--tmp_table_size=1G', '--max_heap_table_size=1G', '--temptable_max_ram=4G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794659963
* mysql-1-1-2-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1221297
  * datadisk:78402
  * volume_size:147G
  * volume_used:77G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem', '--sort_buffer_size=32M', '--join_buffer_size=64M', '--tmp_table_size=1G', '--max_heap_table_size=1G', '--temptable_max_ram=4G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794659963
* mysql-1-1-2-1-2 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1221297
  * datadisk:78402
  * volume_size:147G
  * volume_used:77G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem', '--sort_buffer_size=32M', '--join_buffer_size=64M', '--tmp_table_size=1G', '--max_heap_table_size=1G', '--temptable_max_ram=4G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794659963
* mysql-1-2-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1150073
  * datadisk:78406
  * volume_size:147G
  * volume_used:77G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem', '--sort_buffer_size=32M', '--join_buffer_size=64M', '--tmp_table_size=1G', '--max_heap_table_size=1G', '--temptable_max_ram=4G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794659963
* mysql-1-2-2-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1042325
  * datadisk:78406
  * volume_size:147G
  * volume_used:77G
  * cpu_list:0-223
bexhoma : C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\benchmarks\dbmsbenchmarker\benchmark.py:180: 
PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has 
poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use 
`newframe = frame.copy()`
In C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\scripts\test-docs-mysql.ps1:218 Zeichen:1
+ bexhoma tpcds `
+ ~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (C:\Users\Patric...= frame.copy()`:String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
  df_matrix['complete'] = complete.map({True: 'yes', False: 'no'})
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem', '--sort_buffer_size=32M', '--join_buffer_size=64M', '--tmp_table_size=1G', '--max_heap_table_size=1G', '--temptable_max_ram=4G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794659963
* mysql-1-2-2-1-2 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1042325
  * datadisk:78406
  * volume_size:147G
  * volume_used:77G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem', '--sort_buffer_size=32M', '--join_buffer_size=64M', '--tmp_table_size=1G', '--max_heap_table_size=1G', '--temptable_max_ram=4G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794659963

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MySQL-1-2

### Data Parameters of Reused Volumes
* MySQL-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### Ingestion
* MySQL-1: 67 of 67 units ok

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794659963-88d6c5f89-tqwcw: 0
* bexhoma-sut-mysql-1-1794659963-6d68b45cdd-v8hng: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: tpcds (2 pods)
* DBMS MySQL-1 - Experiment 2 Client 1: tpcds (1 pods)
* DBMS MySQL-1 - Experiment 2 Client 2: tpcds (2 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: tpcds (2 pods)
* DBMS MySQL-1 - Experiment 2 Client 1: tpcds (1 pods)
* DBMS MySQL-1 - Experiment 2 Client 2: tpcds (2 pods)

### Loading

#### Per Run

| DBMS      |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |   10 |     2571.00 |           5.00 |            0.00 |        374.00 |         2184.00 |              8 |         0 |             | None           |             0 | False         |               14.00 | False               |
| MySQL-1-2 |                2 |   10 |     2571.00 |           5.00 |            0.00 |        374.00 |         2184.00 |              8 |         0 |             | None           |             0 | False         |               14.00 | True                |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 | 10.00 |               99 |                  99 |       5647 |            7.82 |             4623.36 |            631.13 |          -1 |
| mysql-1-1-2-1-1 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       1 | 10.00 |               99 |                  99 |       7717 |            9.66 |             3742.51 |            461.84 |          -1 |
| mysql-1-1-2-1-2 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       2 | 10.00 |               99 |                  99 |       7716 |           10.08 |             3584.73 |            461.90 |          -1 |
| mysql-1-2-1-1-1 | mysql-1-2-1 | mysql-1-2-1-1 |                2 |        1 |               1 |       1 | 10.00 |               99 |                  99 |       7604 |            9.98 |             3616.63 |            468.70 |          -1 |
| mysql-1-2-2-1-1 | mysql-1-2-2 | mysql-1-2-2-1 |                2 |        2 |               1 |       1 | 10.00 |               99 |                  99 |       7779 |            9.95 |             3630.65 |            458.16 |          -1 |
| mysql-1-2-2-1-2 | mysql-1-2-2 | mysql-1-2-2-1 |                2 |        2 |               1 |       2 | 10.00 |               99 |                  99 |       7779 |            9.45 |             3824.36 |            458.16 |          -1 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               99 |                  99 |       5647 |            7.82 |             4623.36 |            631.13 |          -1 |
| mysql-1-1-2 | mysql-1-1-2 |                1 |        2 |               1 |           2 | 10.00 |              198 |                 198 |       7717 |            9.87 |             3662.77 |            923.68 |          -1 |
| mysql-1-2-1 | mysql-1-2-1 |                2 |        1 |               1 |           1 | 10.00 |               99 |                  99 |       7604 |            9.98 |             3616.63 |            468.70 |          -1 |
| mysql-1-2-2 | mysql-1-2-2 |                2 |        2 |               1 |           2 | 10.00 |              198 |                 198 |       7779 |            9.70 |             3726.25 |            916.31 |          -1 |

#### Query Completion per Phase

| phase       |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mysql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| mysql-1-1-2 |      2 | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | yes        |
| mysql-1-2-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| mysql-1-2-2 |      2 | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   mysql-1-1-1-1-1 |   mysql-1-1-2-1-1 |   mysql-1-1-2-1-2 |   mysql-1-2-1-1-1 |   mysql-1-2-2-1-1 |   mysql-1-2-2-1-2 |
|:--------------|------------------:|------------------:|------------------:|------------------:|------------------:|------------------:|
| TPC-DS Q1     |            139.05 |             53.14 |            139.10 |            104.94 |             54.11 |            145.68 |
| TPC-DS Q2     |          29521.16 |          36183.96 |          35197.52 |          59308.24 |          38575.74 |          38328.85 |
| TPC-DS Q3     |             66.97 |             55.68 |             66.51 |            423.98 |             64.06 |            190.68 |
| TPC-DS Q4     |         452037.98 |         565784.81 |         565221.27 |         977840.25 |         531257.72 |         530108.17 |
| TPC-DS Q5     |         115601.96 |         137117.13 |         136657.90 |         143494.54 |         132467.27 |         133435.88 |
| TPC-DS Q6     |          11387.69 |          10935.95 |          11362.41 |          31058.43 |          11229.55 |          11013.44 |
| TPC-DS Q7     |         124203.22 |         112226.52 |         114407.32 |         231432.33 |         142943.51 |         142688.75 |
| TPC-DS Q8     |         159178.26 |         192603.16 |         189950.50 |         162637.55 |         220290.68 |         220342.82 |
| TPC-DS Q9     |          38927.47 |          42423.02 |          42773.20 |          37962.06 |          37517.52 |          37646.28 |
| TPC-DS Q10    |           6728.73 |           5957.03 |           7197.76 |           7862.39 |           7985.66 |           8018.22 |
| TPC-DS Q11    |         274274.32 |         330133.23 |         344441.89 |         425654.45 |         334890.29 |         333721.19 |
| TPC-DS Q12    |           2283.07 |           2325.90 |           2459.30 |           3177.44 |           3147.55 |           2670.04 |
| TPC-DS Q13    |          75421.40 |          55982.35 |          57413.49 |          84756.29 |          57123.74 |          58167.74 |
| TPC-DS Q14a+b |         377363.72 |         473091.52 |         458008.99 |         394227.35 |         500430.13 |         502210.67 |
| TPC-DS Q15    |           1988.15 |           1921.83 |           1789.85 |           1954.82 |           2062.68 |           1884.60 |
| TPC-DS Q16    |              7.61 |              5.38 |              2.48 |              5.14 |              4.95 |              1.98 |
| TPC-DS Q17    |          75250.62 |          90949.81 |          90174.34 |          72544.53 |          76887.16 |          76573.45 |
| TPC-DS Q18    |          13767.84 |          14782.50 |          15057.48 |          15949.26 |          15590.07 |          14919.16 |
| TPC-DS Q19    |           3436.69 |           4443.70 |           4442.05 |           3384.14 |           4610.16 |           4610.47 |
| TPC-DS Q20    |           4142.65 |           5979.48 |           5918.29 |           3990.10 |           7234.84 |           7226.11 |
| TPC-DS Q21    |         404706.66 |         629017.97 |         629070.03 |         740520.61 |         613391.83 |         613391.18 |
| TPC-DS Q22    |          63579.97 |          65290.11 |          65958.23 |          61900.96 |          58376.69 |          58369.69 |
| TPC-DS Q23a+b |         551265.95 |         650488.53 |         647963.41 |         623938.92 |         648716.33 |         648713.57 |
| TPC-DS Q24a+b |          23768.61 |          31738.57 |          33506.00 |          25288.12 |          31736.28 |          32006.13 |
| TPC-DS Q25    |           2104.34 |          18006.28 |          18298.45 |           1512.60 |          19265.85 |          18779.75 |
| TPC-DS Q26    |          64057.45 |         206665.05 |         206666.12 |          65063.14 |         153965.95 |         153966.03 |
| TPC-DS Q27    |          24305.61 |          32598.64 |          32230.28 |          26485.92 |          30379.18 |          30381.42 |
| TPC-DS Q28    |          30037.06 |          31404.98 |          30962.11 |          35149.13 |          30914.29 |          29625.37 |
| TPC-DS Q29    |           1798.60 |           1690.51 |           2430.55 |           1757.96 |           1266.89 |           1997.54 |
| TPC-DS Q30    |          57813.96 |          64066.90 |          62917.75 |          59850.69 |          61685.46 |          62418.35 |
| TPC-DS Q31    |         146861.68 |         208408.21 |         196493.02 |         165919.00 |         199370.27 |         215280.81 |
| TPC-DS Q32    |           5016.11 |           6334.00 |           6544.62 |           5651.26 |           6465.66 |           6593.26 |
| TPC-DS Q33    |           3276.73 |           2770.73 |           2863.67 |           3472.43 |           2842.95 |           2542.38 |
| TPC-DS Q34    |              2.78 |              2.60 |              3.30 |              2.93 |              7.24 |              2.76 |
| TPC-DS Q35    |          47281.76 |          45427.20 |          58333.57 |          58663.30 |          60856.62 |          44980.74 |
| TPC-DS Q36    |          24863.45 |          32656.02 |          32900.26 |          31204.94 |          31190.56 |          29850.37 |
| TPC-DS Q37    |             31.84 |             40.73 |             34.79 |             34.12 |             29.47 |             49.56 |
| TPC-DS Q38    |          38540.92 |          49300.95 |          49415.49 |          48915.11 |          49177.46 |          51568.68 |
| TPC-DS Q39a+b |          12678.89 |          17348.17 |          16331.60 |          16133.37 |          17605.25 |          18253.70 |
| TPC-DS Q40    |          48321.99 |          60192.84 |          60825.10 |          82077.04 |          57444.91 |          55734.43 |
| TPC-DS Q41    |          35806.96 |          39242.44 |          38290.37 |          36366.49 |          37293.27 |          35942.17 |
| TPC-DS Q42    |           2700.96 |           2728.59 |           3334.19 |           3487.84 |           2996.83 |           3400.33 |
| TPC-DS Q43    |              2.17 |              2.35 |              2.60 |              1.76 |              1.81 |              2.01 |
| TPC-DS Q44    |              5.72 |              2.16 |             16.62 |             22.35 |              1.76 |             11.58 |
| TPC-DS Q45    |           1242.20 |           2041.36 |           1660.41 |           5051.79 |           1719.23 |           1289.75 |
| TPC-DS Q46    |              2.26 |              2.68 |              3.64 |              6.99 |              2.41 |              2.02 |
| TPC-DS Q47    |          85748.48 |         104757.25 |         103778.23 |          99874.97 |         116132.25 |         118357.52 |
| TPC-DS Q48    |          55944.36 |          59804.22 |          59930.26 |          91280.39 |          63317.83 |          63063.74 |
| TPC-DS Q49    |          34476.03 |          43349.25 |          44751.80 |          69493.18 |          41676.47 |          41149.97 |
| TPC-DS Q50    |            270.68 |            349.03 |            347.70 |            584.21 |            343.65 |            343.48 |
| TPC-DS Q51    |          44784.45 |          57050.49 |          53395.82 |         108902.64 |          60288.02 |          57496.27 |
| TPC-DS Q52    |           3058.29 |           3679.03 |           3313.39 |           3510.24 |           3355.94 |           2614.33 |
| TPC-DS Q53    |          73905.98 |          93314.47 |          97025.19 |          72405.96 |          79459.19 |          79963.41 |
| TPC-DS Q54    |          23276.94 |          35554.77 |          35399.78 |          33146.37 |          32089.18 |          32658.54 |
| TPC-DS Q55    |           2701.83 |           3692.92 |           3770.89 |           3434.92 |           2941.56 |           2891.84 |
| TPC-DS Q56    |           2207.59 |           3262.08 |           3620.28 |           3322.23 |           2237.86 |           2868.09 |
| TPC-DS Q57    |          55725.74 |          69033.32 |          68817.80 |          80901.25 |          67634.60 |          68550.42 |
| TPC-DS Q58    |          53071.15 |          71545.06 |          71662.07 |          55584.27 |          70715.56 |          71091.57 |
| TPC-DS Q59    |          65601.69 |          74635.97 |          74742.73 |          73167.06 |          79470.40 |          84239.50 |
| TPC-DS Q60    |           4636.56 |           6579.62 |           6481.69 |           6388.03 |           4874.64 |           5435.39 |
| TPC-DS Q61    |          90107.44 |         121072.81 |         114480.84 |         109154.03 |         111253.02 |         111690.87 |
| TPC-DS Q62    |          29481.76 |          39551.01 |          18194.99 |          69153.74 |          15294.36 |          34346.48 |
| TPC-DS Q63    |          66897.33 |          97882.61 |         101055.00 |          83595.57 |          84037.66 |          81623.95 |
| TPC-DS Q64    |           4101.42 |           3748.40 |           5232.86 |           9165.44 |           4587.51 |           4621.66 |
| TPC-DS Q65    |          33271.51 |          39107.51 |          39342.61 |          43390.84 |          39275.88 |          38653.15 |
| TPC-DS Q66    |          13778.13 |          12753.78 |          17229.17 |          36096.33 |          15883.47 |          11702.83 |
| TPC-DS Q67    |         107234.42 |         138709.97 |         139440.81 |         126693.02 |         125495.02 |         123273.99 |
| TPC-DS Q68    |              2.01 |              3.33 |              2.95 |              2.49 |              3.77 |              2.21 |
| TPC-DS Q69    |              3.96 |              3.07 |              7.21 |              5.92 |              3.61 |              2.59 |
| TPC-DS Q70    |         133800.88 |         175056.76 |         172706.58 |         152378.50 |         159298.24 |         160147.86 |
| TPC-DS Q71    |           5214.81 |           5084.08 |           6679.35 |           6918.62 |           5992.28 |           5357.38 |
| TPC-DS Q72    |         283306.20 |         675373.53 |         693974.55 |         418004.93 |         703088.62 |         687398.32 |
| TPC-DS Q73    |              2.65 |              2.06 |              1.70 |              2.18 |              5.17 |              2.63 |
| TPC-DS Q74    |          52071.75 |          75214.28 |          75192.71 |          63949.69 |          91978.29 |          92190.73 |
| TPC-DS Q75    |          13757.98 |          19551.70 |          19058.99 |          18939.37 |          17811.58 |          19253.47 |
| TPC-DS Q76    |           4572.41 |           5813.50 |           6326.08 |           5395.31 |           6184.53 |           5019.76 |
| TPC-DS Q77    |          92791.00 |         126637.03 |         126400.05 |         104071.06 |         186070.80 |         187325.54 |
| TPC-DS Q78    |         135283.01 |         213310.52 |         216519.42 |         155491.92 |         217223.10 |         217131.83 |
| TPC-DS Q79    |          69461.86 |          83210.12 |          81645.58 |          76997.40 |         134256.07 |         132889.96 |
| TPC-DS Q80    |         195284.56 |         298071.46 |         296705.46 |         207932.02 |         320169.53 |         320138.21 |
| TPC-DS Q81    |          46551.27 |          45389.76 |          45335.97 |          48622.58 |          50268.83 |          52434.57 |
| TPC-DS Q82    |             65.88 |             73.32 |             74.06 |             78.77 |             89.21 |             64.52 |
| TPC-DS Q83    |            464.76 |            971.61 |            972.94 |            517.77 |           1437.08 |            348.77 |
| TPC-DS Q84    |            517.23 |            600.79 |            589.14 |            547.12 |            611.52 |            262.78 |
| TPC-DS Q85    |           1017.76 |           1221.97 |           1219.79 |           1617.64 |           1261.11 |            588.18 |
| TPC-DS Q86    |           9114.29 |          11236.41 |          11437.48 |          11327.00 |          18613.68 |          18581.26 |
| TPC-DS Q87    |          39646.87 |          49804.99 |          49599.25 |          44088.71 |          75163.39 |          75194.24 |
| TPC-DS Q88    |          82285.30 |         103858.41 |         103784.21 |          83315.67 |         144677.18 |         153808.75 |
| TPC-DS Q89    |          73895.24 |          94889.27 |          95592.13 |          72446.58 |         127896.11 |         129833.25 |
| TPC-DS Q90    |           4790.04 |           7087.82 |           6454.80 |           4341.80 |           5873.10 |           5876.01 |
| TPC-DS Q91    |            131.95 |            228.09 |            219.81 |            159.97 |            351.47 |            110.91 |
| TPC-DS Q92    |            518.94 |            670.34 |            671.12 |            514.79 |           1330.31 |            568.28 |
| TPC-DS Q93    |            365.57 |            543.67 |            541.71 |            393.00 |            500.04 |            315.29 |
| TPC-DS Q94    |           8549.72 |          16863.08 |          16860.47 |           9918.93 |          15302.66 |           9329.80 |
| TPC-DS Q95    |          43894.51 |          58969.79 |          60185.10 |          41527.27 |          49109.42 |          48154.08 |
| TPC-DS Q96    |           9982.23 |          11862.87 |          11403.29 |           9505.02 |          11624.75 |          12004.57 |
| TPC-DS Q97    |          36608.07 |          61627.28 |          60400.08 |          38798.92 |          60589.43 |          63330.70 |
| TPC-DS Q98    |           9082.83 |          10754.56 |          10807.58 |           9192.84 |           9440.83 |          11082.12 |
| TPC-DS Q99    |          64576.50 |         182379.95 |         182807.90 |          62558.80 |          80844.35 |          73261.71 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      3237.86 |      6.50 |          32.03 |                 61.08 |
| mysql-1-1-2-1 |      3237.86 |      6.50 |          32.03 |                 61.08 |

### Loading phase: component data generator

| DBMS          | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|:-------------|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |
| mysql-1-1-2-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |        36.82 |      0.22 |           0.01 |                  2.83 |
| mysql-1-1-2-1 |        36.82 |      0.22 |           0.01 |                  2.83 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      5130.67 |      1.02 |          67.92 |                 96.97 |
| mysql-1-1-2-1 |     13386.21 |      2.02 |         104.00 |                128.00 |
| mysql-1-2-1-1 |      5831.99 |      1.05 |          50.70 |                 50.70 |
| mysql-1-2-2-1 |     13818.47 |      2.02 |          92.16 |                 92.16 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |        39.62 |      0.11 |           0.40 |                  0.42 |
| mysql-1-1-2-1 |        86.87 |      1.02 |           0.43 |                  0.44 |
| mysql-1-2-1-1 |        42.49 |      0.74 |           0.42 |                  0.43 |
| mysql-1-2-2-1 |        85.43 |      0.83 |           0.42 |                  0.43 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-2-1-1 (bexhoma-metrics-mysql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-2-1-1 (bexhoma-metrics-mysql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-2-2-1 (bexhoma-metrics-mysql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-2-2-1 (bexhoma-metrics-mysql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
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
* Duration: 789s 
* Code: 1794692663
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1078854
  * datadisk:34689
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794692663
    * TENANT_VOL:False

### Ingestion
* MySQL-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794692663-7cdddf5b74-vm6n8: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (1 pods)

### Loading

#### Per Run

| DBMS      |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |   16 |       86.00 |           4.00 |            0.00 |         78.00 |            4.00 |              1 |         1 |             |                |             0 | False         |              669.77 | False               |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 |       160 |     8192 |          -1 | 300.00 |        0 |                        8191.90 |                     8115.96 |         0.00 |                                                      10730.00 |                                               5630.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 |       160 |     8192 |          -1 | 300.00 |        0 |                        8191.90 |                     8115.96 |         0.00 |                                                      10730.00 |                                               5630.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
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
* Duration: 1006s 
* Code: 1794693468
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 1 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
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
  * disk:1043972
  * datadisk:34685
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
    * code:1794693468
    * TENANT_VOL:False
* mysql-1-2-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1043974
  * datadisk:35104
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
    * code:1794693468
    * TENANT_VOL:False

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MySQL-1-2

### Data Parameters of Reused Volumes
* MySQL-1: loading values of the volume: script=Schema, indexing=Checks

### Ingestion
* MySQL-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794693468-7f574f5bb8-gxnkf: 0
* bexhoma-sut-mysql-1-1794693468-6476f9d8f6-zp2lk: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS MySQL-1 - Experiment 2 Client 1: benchbase (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS MySQL-1 - Experiment 2 Client 1: benchbase (1 pods)

### Loading

#### Per Run

| DBMS      |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |   16 |       81.00 |           4.00 |            0.00 |         72.00 |            5.00 |              1 |         1 |             |                |             0 | False         |              711.11 | False               |
| MySQL-1-2 |                2 |   16 |       81.00 |           4.00 |            0.00 |         72.00 |            5.00 |              1 |         1 |             |                |             0 | False         |              711.11 | True                |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 |       160 |     8192 |          -1 |  60.00 |        0 |                        8191.32 |                     8111.74 |         0.00 |                                                      14393.00 |                                               8338.00 |
| mysql-1-2-1-1-1 | mysql-1-2-1 | mysql-1-2-1-1 |                2 |        1 |               1 |       1 |       160 |     8192 |          -1 |  60.00 |        0 |                        8193.18 |                     8109.78 |         0.00 |                                                      18143.00 |                                              10186.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 |       160 |     8192 |          -1 |  60.00 |        0 |                        8191.32 |                     8111.74 |         0.00 |                                                      14393.00 |                                               8338.00 |
| mysql-1-2-1 | mysql-1-2-1 |                2 |        1 |               1 |           1 |       160 |     8192 |          -1 |  60.00 |        0 |                        8193.18 |                     8109.78 |         0.00 |                                                      18143.00 |                                              10186.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
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
* Duration: 810s 
* Code: 1794694488
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1078665
  * datadisk:34689
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794694488
    * TENANT_VOL:False

### Ingestion
* MySQL-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794694488-ff6ff947d-rxbhg: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (1 pods)

### Loading

#### Per Run

| DBMS      |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |   16 |       79.00 |           3.00 |            0.00 |         73.00 |            3.00 |              1 |         1 |             |                |             0 | False         |              729.11 | False               |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 |       160 |     8192 |          -1 | 300.00 |        0 |                        8192.52 |                     8114.58 |         0.00 |                                                      11133.00 |                                               5554.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 |       160 |     8192 |          -1 | 300.00 |        0 |                        8192.52 |                     8114.58 |         0.00 |                                                      11133.00 |                                               5554.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       122.73 |      2.34 |           4.77 |                  6.84 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       648.75 |     14.23 |           0.38 |                  0.38 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      4212.50 |     14.90 |           6.79 |                 15.05 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      3398.11 |     12.37 |           1.67 |                  1.67 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
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
* Duration: 2047s 
* Code: 1794695341
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 2 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
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
  * disk:1046889
  * datadisk:35512
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
    * code:1794695341
    * TENANT_VOL:False
* mysql-1-1-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1049775
  * datadisk:36204
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
    * code:1794695341
    * TENANT_VOL:False
* mysql-1-1-3-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1049931
  * datadisk:37576
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
    * code:1794695341
    * TENANT_VOL:False
* mysql-1-1-4-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1045222
  * datadisk:38260
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
    * code:1794695341
    * TENANT_VOL:False
* mysql-1-2-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1048100
  * datadisk:39568
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
    * code:1794695341
    * TENANT_VOL:False
* mysql-1-2-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1048807
  * datadisk:40565
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
    * code:1794695341
    * TENANT_VOL:False
* mysql-1-2-3-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1049406
  * datadisk:41825
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
    * code:1794695341
    * TENANT_VOL:False
* mysql-1-2-4-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1043976
  * datadisk:42521
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
    * code:1794695341
    * TENANT_VOL:False

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MySQL-1

### Data Parameters of Reused Volumes
* MySQL-1: loading values of the volume: script=Schema, indexing=Checks

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794695341-6cf7f55896-67xn2: 0
* bexhoma-sut-mysql-1-1794695341-8568d65c57-44psq: 0

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

| DBMS      |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |   16 |       81.00 |           4.00 |            0.00 |         72.00 |            5.00 |              0 |         1 |             |                |             0 | False         |              711.11 | True                |
| MySQL-1-2 |                2 |   16 |       81.00 |           4.00 |            0.00 |         72.00 |            5.00 |              0 |         1 |             |                |             0 | False         |              711.11 | True                |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 |       160 |     8192 |          -1 | 120.00 |        0 |                        8192.15 |                     8106.06 |         0.00 |                                                      17513.00 |                                               9574.00 |
| mysql-1-1-2-1-1 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       1 |       160 |     8192 |          -1 | 120.00 |        0 |                        8176.36 |                     8054.58 |         0.00 |                                                      38179.00 |                                              16578.00 |
| mysql-1-1-2-1-2 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       2 |       160 |     8192 |          -1 | 120.00 |        0 |                        8191.60 |                     8067.66 |         0.00 |                                                      38157.00 |                                              16437.00 |
| mysql-1-1-3-1-1 | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       1 |        80 |     4096 |          -1 | 120.00 |        0 |                        4095.82 |                     4051.65 |         0.00 |                                                      17601.00 |                                               8914.00 |
| mysql-1-1-3-1-2 | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       2 |        80 |     4096 |          -1 | 120.00 |        0 |                        4095.41 |                     4052.27 |         0.00 |                                                      17521.00 |                                               8873.00 |
| mysql-1-1-4-1-1 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       1 |        80 |     4096 |          -1 | 120.00 |        0 |                        3888.92 |                     3828.38 |         0.00 |                                                      44730.00 |                                              20557.00 |
| mysql-1-1-4-1-2 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       2 |        80 |     4096 |          -1 | 120.00 |        0 |                        3933.24 |                     3871.41 |         0.00 |                                                      44529.00 |                                              20327.00 |
| mysql-1-1-4-1-3 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       3 |        80 |     4096 |          -1 | 120.00 |        0 |                        3912.59 |                     3851.14 |         0.00 |                                                      44578.00 |                                              20435.00 |
| mysql-1-1-4-1-4 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       4 |        80 |     4096 |          -1 | 120.00 |        0 |                        3897.09 |                     3835.52 |         0.00 |                                                      44720.00 |                                              20515.00 |
| mysql-1-2-1-1-1 | mysql-1-2-1 | mysql-1-2-1-1 |                2 |        1 |               1 |       1 |       160 |     8192 |          -1 | 120.00 |        0 |                        8191.84 |                     8095.09 |         0.00 |                                                      22259.00 |                                              11410.00 |
| mysql-1-2-2-1-1 | mysql-1-2-2 | mysql-1-2-2-1 |                2 |        2 |               1 |       1 |       160 |     8192 |          -1 | 120.00 |        0 |                        7456.47 |                     7331.72 |         0.00 |                                                      44388.00 |                                              21437.00 |
| mysql-1-2-2-1-2 | mysql-1-2-2 | mysql-1-2-2-1 |                2 |        2 |               1 |       2 |       160 |     8192 |          -1 | 120.00 |        0 |                        7606.34 |                     7477.68 |         0.00 |                                                      43846.00 |                                              21013.00 |
| mysql-1-2-3-1-1 | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       1 |        80 |     4096 |          -1 | 120.00 |        0 |                        4096.14 |                     4052.36 |         0.00 |                                                      17273.00 |                                               9066.00 |
| mysql-1-2-3-1-2 | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       2 |        80 |     4096 |          -1 | 120.00 |        0 |                        4095.81 |                     4050.75 |         0.00 |                                                      16957.00 |                                               8870.00 |
| mysql-1-2-4-1-1 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       1 |        80 |     4096 |          -1 | 120.00 |        0 |                        3992.49 |                     3925.28 |         0.00 |                                                      42551.00 |                                              20025.00 |
| mysql-1-2-4-1-2 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       2 |        80 |     4096 |          -1 | 120.00 |        0 |                        4042.53 |                     3974.39 |         0.00 |                                                      42220.00 |                                              19777.00 |
| mysql-1-2-4-1-3 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       3 |        80 |     4096 |          -1 | 120.00 |        0 |                        4001.26 |                     3934.53 |         0.00 |                                                      42475.00 |                                              19981.00 |
| mysql-1-2-4-1-4 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       4 |        80 |     4096 |          -1 | 120.00 |        0 |                        3992.10 |                     3924.74 |         0.00 |                                                      42533.00 |                                              20027.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 |       160 |     8192 |          -1 | 120.00 |        0 |                        8192.15 |                     8106.06 |         0.00 |                                                      17513.00 |                                               9574.00 |
| mysql-1-1-2 | mysql-1-1-2 |                1 |        2 |               1 |           2 |       320 |    16384 |          -1 | 120.00 |        0 |                       16367.95 |                    16122.24 |         0.00 |                                                      38179.00 |                                              16507.50 |
| mysql-1-1-3 | mysql-1-1-3 |                1 |        3 |               1 |           2 |       160 |     8192 |          -1 | 120.00 |        0 |                        8191.23 |                     8103.93 |         0.00 |                                                      17601.00 |                                               8893.50 |
| mysql-1-1-4 | mysql-1-1-4 |                1 |        4 |               1 |           4 |       320 |    16384 |          -1 | 120.00 |        0 |                       15631.84 |                    15386.46 |         0.00 |                                                      44730.00 |                                              20458.50 |
| mysql-1-2-1 | mysql-1-2-1 |                2 |        1 |               1 |           1 |       160 |     8192 |          -1 | 120.00 |        0 |                        8191.84 |                     8095.09 |         0.00 |                                                      22259.00 |                                              11410.00 |
| mysql-1-2-2 | mysql-1-2-2 |                2 |        2 |               1 |           2 |       320 |    16384 |          -1 | 120.00 |        0 |                       15062.81 |                    14809.40 |         0.00 |                                                      44388.00 |                                              21225.00 |
| mysql-1-2-3 | mysql-1-2-3 |                2 |        3 |               1 |           2 |       160 |     8192 |          -1 | 120.00 |        0 |                        8191.95 |                     8103.11 |         0.00 |                                                      17273.00 |                                               8968.00 |
| mysql-1-2-4 | mysql-1-2-4 |                2 |        4 |               1 |           4 |       320 |    16384 |          -1 | 120.00 |        0 |                       16028.38 |                    15758.94 |         0.00 |                                                      42551.00 |                                              19952.50 |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      1605.82 |     16.03 |           5.80 |                  7.97 |
| mysql-1-1-2-1 |      3824.36 |     32.57 |           7.75 |                 15.08 |
| mysql-1-1-3-1 |      1404.63 |     14.93 |           8.38 |                 17.68 |
| mysql-1-1-4-1 |      3417.61 |     31.55 |           9.88 |                 23.96 |
| mysql-1-2-1-1 |      1990.19 |     16.91 |           7.66 |                 10.39 |
| mysql-1-2-2-1 |      3749.29 |     32.10 |          10.01 |                 17.25 |
| mysql-1-2-3-1 |      1702.90 |     14.53 |          10.88 |                 20.60 |
| mysql-1-2-4-1 |      3539.39 |     31.89 |          12.40 |                 26.55 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      1433.26 |     13.95 |           1.41 |                  1.41 |
| mysql-1-1-2-1 |      2027.18 |     19.09 |           1.45 |                  1.45 |
| mysql-1-1-3-1 |      1440.33 |     12.66 |           1.16 |                  1.16 |
| mysql-1-1-4-1 |      2145.25 |     21.01 |           1.01 |                  1.01 |
| mysql-1-2-1-1 |      1403.71 |     12.75 |           1.38 |                  1.38 |
| mysql-1-2-2-1 |      1889.48 |     19.70 |           1.57 |                  1.57 |
| mysql-1-2-3-1 |      1051.35 |     11.44 |           1.26 |                  1.26 |
| mysql-1-2-4-1 |      1892.67 |     21.76 |           1.05 |                  1.05 |

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
* TEST passed: Loading completed without failures
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
* Type: hammerdb
* Duration: 883s 
* Code: 1794697432
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Ramp-up period is 2 minutes before measurements begin.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * Experiment is limited to DBMS ['MySQL'].
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1078008
  * datadisk:34377
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794697432

### Ingestion
* MySQL-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794697432-5b447d5bf4-4h2mt: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: hammerdb (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: hammerdb (1 pods)

### Loading

#### Per Run

| DBMS      |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |   16 |       57.00 |           4.00 |            0.00 |         50.00 |            3.00 |              1 |         8 |             | None           |             0 | False         |             1010.53 | False               |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   NOPM |    TPM |   efficiency |   duration |   errors |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|-------:|-------:|-------------:|-----------:|---------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 |        16 | 122330 | 284262 |         0.00 |          5 |        0 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   efficiency |      NOPM |       TPM |   duration |   errors |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|-------------:|----------:|----------:|-----------:|---------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 |        16 |         0.00 | 122330.00 | 284262.00 |          5 |        0 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
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
* Type: hammerdb
* Duration: 917s 
* Code: 1794698330
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Ramp-up period is 2 minutes before measurements begin.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
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
  * disk:1053727
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
    * code:1794698330

### Ingestion
* MySQL-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794698330-85b867f455-868sz: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: hammerdb (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: hammerdb (1 pods)

### Loading

#### Per Run

| DBMS      |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |   16 |       65.00 |           5.00 |            0.00 |         55.00 |            5.00 |              1 |         8 |             | None           |             0 | False         |              886.15 | False               |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   NOPM |    TPM |   efficiency |   duration |   errors |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|-------:|-------:|-------------:|-----------:|---------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 |        16 |  70972 | 164697 |         0.00 |          5 |        0 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   efficiency |     NOPM |       TPM |   duration |   errors |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|-------------:|---------:|----------:|-----------:|---------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 |        16 |         0.00 | 70972.00 | 164697.00 |          5 |        0 |

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |        89.44 |      1.79 |           5.48 |                  7.26 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       128.09 |      0.00 |           0.09 |                  0.09 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      1292.56 |      3.39 |           5.22 |                 10.34 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       434.38 |      1.55 |           0.08 |                  0.08 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (job pods ran shorter than scrape interval; series exists only while non-zero)
* TEST passed: NOPM contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey))
* TEST passed: Workflow as planned
connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                           483.21 |                            0.01 |                            0.00 |                              0.00 |
| mysql-1-1-2-1 |                                  1.00 |                           483.21 |                            0.01 |                            0.00 |                              0.00 |

#### Benchmarking phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                       1638500.11 |                            0.01 |                            0.00 |                              0.00 |
| mysql-1-1-2-1 |                                  1.00 |                       1675960.63 |                            0.01 |                            0.00 |                              0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: NOPM contains no 0 or NaN
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
* Type: hammerdb
* Duration: 3112s 
* Code: 1794699310
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 2 minutes. Ramp-up period is 2 minutes before measurements begin.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
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
  * disk:1059097
  * datadisk:34995
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
    * code:1794699310
* mysql-1-1-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1044881
  * datadisk:35311
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
    * code:1794699310
* mysql-1-1-3-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1045946
  * datadisk:35981
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
    * code:1794699310
* mysql-1-1-4-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1046214
  * datadisk:36337
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
    * code:1794699310
* mysql-1-2-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1044921
  * datadisk:37051
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
    * code:1794699310
* mysql-1-2-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1046272
  * datadisk:37387
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
    * code:1794699310
* mysql-1-2-3-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1047620
  * datadisk:38052
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
    * code:1794699310
* mysql-1-2-4-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1049357
  * datadisk:38400
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
    * code:1794699310

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MySQL-1

### Data Parameters of Reused Volumes
* MySQL-1: loading values of the volume: script=Schema, indexing=Checks

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794699310-f958744c4-bg8zm: 0
* bexhoma-sut-mysql-1-1794699310-78d985c867-gj77k: 0

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

| DBMS      |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |   16 |       65.00 |           5.00 |            0.00 |         55.00 |            5.00 |              0 |         8 |             | None           |             0 | False         |              886.15 | True                |
| MySQL-1-2 |                2 |   16 |       65.00 |           5.00 |            0.00 |         55.00 |            5.00 |              0 |         8 |             | None           |             0 | False         |              886.15 | True                |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   NOPM |    TPM |   efficiency |   duration |   errors |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|-------:|-------:|-------------:|-----------:|---------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 |        16 |  71608 | 166113 |         0.00 |          2 |        0 |
| mysql-1-1-2-1-1 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       1 |        16 | 147753 | 343876 |         0.00 |          2 |        0 |
| mysql-1-1-2-1-2 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       2 |        16 | 147497 | 343261 |         0.00 |          2 |        0 |
| mysql-1-1-3-1-1 | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       1 |         8 |  79662 | 184956 |         0.00 |          2 |        0 |
| mysql-1-1-3-1-2 | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       2 |         8 |  79536 | 184715 |         0.00 |          2 |        0 |
| mysql-1-1-4-1-1 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       1 |         8 | 159074 | 369350 |         0.00 |          2 |        0 |
| mysql-1-1-4-1-2 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       2 |         8 | 158884 | 368910 |         0.00 |          2 |        0 |
| mysql-1-1-4-1-3 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       3 |         8 | 158938 | 369042 |         0.00 |          2 |        0 |
| mysql-1-1-4-1-4 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       4 |         8 | 159031 | 369241 |         0.00 |          2 |        0 |
| mysql-1-2-1-1-1 | mysql-1-2-1 | mysql-1-2-1-1 |                2 |        1 |               1 |       1 |        16 |  76056 | 177175 |         0.00 |          2 |        0 |
| mysql-1-2-2-1-1 | mysql-1-2-2 | mysql-1-2-2-1 |                2 |        2 |               1 |       1 |        16 | 148324 | 344549 |         0.00 |          2 |        0 |
| mysql-1-2-2-1-2 | mysql-1-2-2 | mysql-1-2-2-1 |                2 |        2 |               1 |       2 |        16 | 148095 | 344007 |         0.00 |          2 |        0 |
| mysql-1-2-3-1-1 | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       1 |         8 |  75656 | 175726 |         0.00 |          2 |        0 |
| mysql-1-2-3-1-2 | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       2 |         8 |  75561 | 175466 |         0.00 |          2 |        0 |
| mysql-1-2-4-1-1 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       1 |         8 | 153897 | 358167 |         0.00 |          2 |        0 |
| mysql-1-2-4-1-2 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       2 |         8 | 154027 | 358495 |         0.00 |          2 |        0 |
| mysql-1-2-4-1-3 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       3 |         8 | 153940 | 358268 |         0.00 |          2 |        0 |
| mysql-1-2-4-1-4 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       4 |         8 | 153984 | 358409 |         0.00 |          2 |        0 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   efficiency |      NOPM |       TPM |   duration |   errors |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|-------------:|----------:|----------:|-----------:|---------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 |        16 |         0.00 |  71608.00 | 166113.00 |          2 |        0 |
| mysql-1-1-2 | mysql-1-1-2 |                1 |        2 |               1 |           2 |        32 |         0.00 | 147625.00 | 343568.50 |          2 |        0 |
| mysql-1-1-3 | mysql-1-1-3 |                1 |        3 |               1 |           2 |        16 |         0.00 |  79599.00 | 184835.50 |          2 |        0 |
| mysql-1-1-4 | mysql-1-1-4 |                1 |        4 |               1 |           4 |        32 |         0.00 | 158981.75 | 369135.75 |          2 |        0 |
| mysql-1-2-1 | mysql-1-2-1 |                2 |        1 |               1 |           1 |        16 |         0.00 |  76056.00 | 177175.00 |          2 |        0 |
| mysql-1-2-2 | mysql-1-2-2 |                2 |        2 |               1 |           2 |        32 |         0.00 | 148209.50 | 344278.00 |          2 |        0 |
| mysql-1-2-3 | mysql-1-2-3 |                2 |        3 |               1 |           2 |        16 |         0.00 |  75608.50 | 175596.00 |          2 |        0 |
| mysql-1-2-4 | mysql-1-2-4 |                2 |        4 |               1 |           4 |        32 |         0.00 | 153962.00 | 358334.75 |          2 |        0 |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       681.13 |      3.03 |           4.71 |                  6.54 |
| mysql-1-1-2-1 |      1360.31 |      6.07 |           5.70 |                 11.43 |
| mysql-1-1-3-1 |       867.06 |      4.05 |           6.18 |                 13.98 |
| mysql-1-1-4-1 |      1580.98 |      7.19 |           6.92 |                 18.69 |
| mysql-1-2-1-1 |       855.74 |      3.88 |           5.39 |                  7.29 |
| mysql-1-2-2-1 |      1500.16 |      6.87 |           6.32 |                 12.03 |
| mysql-1-2-3-1 |       763.03 |      3.67 |           6.67 |                 14.25 |
| mysql-1-2-4-1 |      1608.32 |      7.47 |           7.43 |                 19.14 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       303.80 |      1.55 |           0.08 |                  0.08 |
| mysql-1-1-2-1 |       582.42 |      2.93 |           0.08 |                  0.08 |
| mysql-1-1-3-1 |       311.84 |      1.48 |           0.05 |                  0.05 |
| mysql-1-1-4-1 |       564.26 |      2.39 |           0.05 |                  0.05 |
| mysql-1-2-1-1 |       238.87 |      1.26 |           0.08 |                  0.08 |
| mysql-1-2-2-1 |       520.98 |      2.27 |           0.08 |                  0.08 |
| mysql-1-2-3-1 |       268.64 |      1.18 |           0.05 |                  0.05 |
| mysql-1-2-4-1 |       550.32 |      2.64 |           0.05 |                  0.05 |

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
* TEST passed: Loading completed without failures
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
* Duration: 2493s 
* Code: 1794702462
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
  * Experiment uses bexhoma version 0.11.17.
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1197901
  * datadisk:34750
  * volume_size:1.8T
  * volume_used:1.2T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794702462
* mysql-2-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1197890
  * datadisk:34722
  * volume_size:1.8T
  * volume_used:1.2T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794702462
* mysql-3-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1197901
  * datadisk:34750
  * volume_size:1.8T
  * volume_used:1.2T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794702462
* mysql-4-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1197901
  * datadisk:34722
  * volume_size:1.8T
  * volume_used:1.2T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794702462

### Ingestion
* MySQL-1: 4 of 4 units ok
* MySQL-2: 8 of 8 units ok
* MySQL-3: 4 of 4 units ok
* MySQL-4: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794702462-7cb84bc6d9-qk24g: 0
* bexhoma-sut-mysql-2-1794702462-6c6c49695f-tpzwp: 0
* bexhoma-sut-mysql-3-1794702462-7fb9f858b9-d927n: 0
* bexhoma-sut-mysql-4-1794702462-5ddbcb7f95-v5zcs: 0

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

| connection      |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| mysql-1-1-0-1-1 |             1.00 |      8.00 |   256.00 |        4.00 |     0.00 |                          255.77 |               977453.00 |            250000.00 |                              1242.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-2 |             1.00 |      8.00 |   256.00 |        4.00 |     0.00 |                          255.77 |               977434.00 |            250000.00 |                              1241.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-3 |             1.00 |      8.00 |   256.00 |        4.00 |     0.00 |                          255.74 |               977550.00 |            250000.00 |                              1269.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-4 |             1.00 |      8.00 |   256.00 |        4.00 |     0.00 |                          255.75 |               977535.00 |            250000.00 |                              1197.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-1 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.90 |               977292.00 |            125000.00 |                              1322.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-2 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.90 |               977299.00 |            125000.00 |                              1363.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-3 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.91 |               977256.00 |            125000.00 |                              1312.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-4 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.90 |               977296.00 |            125000.00 |                              1298.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-5 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.89 |               977430.00 |            125000.00 |                              1326.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-6 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.89 |               977382.00 |            125000.00 |                              1332.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-7 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.90 |               977306.00 |            125000.00 |                              1336.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-8 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.89 |               977383.00 |            125000.00 |                              1329.00 | 1.00 |                3.68 |
| mysql-3-1-0-1-1 |             1.00 |     16.00 |   256.00 |        4.00 |     0.00 |                          255.61 |               978071.00 |            250000.00 |                              1325.00 | 1.00 |                3.68 |
| mysql-3-1-0-1-2 |             1.00 |     16.00 |   256.00 |        4.00 |     0.00 |                          255.60 |               978109.00 |            250000.00 |                              1386.00 | 1.00 |                3.68 |
| mysql-3-1-0-1-3 |             1.00 |     16.00 |   256.00 |        4.00 |     0.00 |                          255.56 |               978251.00 |            250000.00 |                              1399.00 | 1.00 |                3.68 |
| mysql-3-1-0-1-4 |             1.00 |     16.00 |   256.00 |        4.00 |     0.00 |                          255.62 |               978011.00 |            250000.00 |                              1335.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-1 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.83 |               977846.00 |            125000.00 |                              1442.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-2 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.82 |               977945.00 |            125000.00 |                              1373.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-3 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.82 |               977957.00 |            125000.00 |                              1394.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-4 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.84 |               977775.00 |            125000.00 |                              1392.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-5 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.84 |               977809.00 |            125000.00 |                              1392.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-6 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.83 |               977890.00 |            125000.00 |                              1353.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-7 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.82 |               977972.00 |            125000.00 |                              1368.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-8 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.81 |               977999.00 |            125000.00 |                              1373.00 | 1.00 |                3.68 |

#### Per Run

| DBMS      |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1 |             1.00 |     32.00 |  1024.00 |        4.00 |     0.00 | 1.00 |                3.68 |                         1023.03 |               977550.00 |           1000000.00 |                              1237.25 |
| MySQL-2-1 |             1.00 |     32.00 |  1024.00 |        8.00 |     0.00 | 1.00 |                3.68 |                         1023.20 |               977430.00 |           1000000.00 |                              1327.25 |
| MySQL-3-1 |             1.00 |     64.00 |  1024.00 |        4.00 |     0.00 | 1.00 |                3.68 |                         1022.38 |               978251.00 |           1000000.00 |                              1361.25 |
| MySQL-4-1 |             1.00 |     64.00 |  1024.00 |        8.00 |     0.00 | 1.00 |                3.68 |                         1022.60 |               977999.00 |           1000000.00 |                              1385.88 |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1020.96 |               979472.00 |             499891 |                            1193.00 |               500109 |                              4415.00 |
| mysql-2-1-1-1-1 | mysql-2-1-1 | mysql-2-1-1-1 |                1 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1020.61 |               979806.00 |             499712 |                            1198.00 |               500288 |                              4391.00 |
| mysql-3-1-1-1-1 | mysql-3-1-1 | mysql-3-1-1-1 |                1 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1021.46 |               978991.00 |             499652 |                            1186.00 |               500348 |                              4391.00 |
| mysql-4-1-1-1-1 | mysql-4-1-1 | mysql-4-1-1-1 |                1 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1021.21 |               979226.00 |             500122 |                            1202.00 |               499878 |                              4391.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1020.96 |               979472.00 |             499891 |                            1193.00 |               500109 |                              4415.00 |
| mysql-2-1-1 | mysql-2-1-1 |                1 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1020.61 |               979806.00 |             499712 |                            1198.00 |               500288 |                              4391.00 |
| mysql-3-1-1 | mysql-3-1-1 |                1 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1021.46 |               978991.00 |             499652 |                            1186.00 |               500348 |                              4391.00 |
| mysql-4-1-1 | mysql-4-1-1 |                1 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1021.21 |               979226.00 |             500122 |                            1202.00 |               499878 |                              4391.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
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
* Duration: 3795s 
* Code: 1794704973
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
  * Experiment uses bexhoma version 0.11.17.
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1044579
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
    * code:1794704973
* mysql-1-2-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1045213
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
    * code:1794704973

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MySQL-1-2

### Data Parameters of Reused Volumes
* MySQL-1: DDL values of the volume: row_format=DYNAMIC, collation=utf8mb4_0900_ai_ci
* MySQL-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### Ingestion
* MySQL-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794704973-77dbd5c9cb-2ftlr: 0
* bexhoma-sut-mysql-1-1794704973-67bd7d948b-cz5t2: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MySQL-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MySQL-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| mysql-1-1-0-1-1 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.82 |               977974.00 |            125000.00 |                              2343.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-2 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.83 |               977882.00 |            125000.00 |                              2955.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-3 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.83 |               977882.00 |            125000.00 |                              2275.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-4 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.83 |               977876.00 |            125000.00 |                              2233.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-5 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.80 |               978092.00 |            125000.00 |                              2309.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-6 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.84 |               977781.00 |            125000.00 |                              2487.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-7 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.82 |               977909.00 |            125000.00 |                              2555.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-8 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.84 |               977821.00 |            125000.00 |                              2493.00 | 1.00 |                3.68 |

#### Per Run

| DBMS      |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1 |             1.00 |     64.00 |  1024.00 |        8.00 |     0.00 | 1.00 |                3.68 |                         1022.60 |               978092.00 |           1000000.00 |                              2456.25 |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1020.68 |               979735.00 |             499611 |                            2565.00 |               500389 |                              6835.00 |
| mysql-1-2-1-1-1 | mysql-1-2-1 | mysql-1-2-1-1 |                2 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1022.08 |               978397.00 |             500596 |                            1884.00 |               499404 |                             10479.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1020.68 |               979735.00 |             499611 |                            2565.00 |               500389 |                              6835.00 |
| mysql-1-2-1 | mysql-1-2-1 |                2 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1022.08 |               978397.00 |             500596 |                            1884.00 |               499404 |                             10479.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
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
* Duration: 6878s 
* Code: 1794708786
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
  * Experiment uses bexhoma version 0.11.17.
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1045210
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
    * code:1794708786
* mysql-1-1-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1045209
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
    * code:1794708786
* mysql-1-1-3-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1045196
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
    * code:1794708786
* mysql-1-1-4-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1046009
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
    * code:1794708786
* mysql-1-2-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1046824
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
    * code:1794708786
* mysql-1-2-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1046827
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
    * code:1794708786
* mysql-1-2-3-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1046829
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
    * code:1794708786
* mysql-1-2-4-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1046833
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
    * code:1794708786

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MySQL-1

### Data Parameters of Reused Volumes
* MySQL-1: DDL values of the volume: row_format=DYNAMIC, collation=utf8mb4_0900_ai_ci
* MySQL-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794708786-6678755dd4-llmk5: 0
* bexhoma-sut-mysql-1-1794708786-68b7954975-kt9pj: 0

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

| connection       | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1-1-1  | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1021.90 |               978567.00 |             500452 |                            1744.00 |               499548 |                              7235.00 |
| mysql-1-1-2-1-1  | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       1 |        64 |     1024 |        0 |                         1017.22 |               491535.00 |             250249 |                            1506.00 |               249751 |                              6831.00 |
| mysql-1-1-2-1-2  | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       2 |        64 |     1024 |        0 |                         1015.72 |               492262.00 |             250137 |                            1495.00 |               249863 |                              6919.00 |
| mysql-1-1-3-1-1  | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       1 |         8 |      128 |        0 |                          127.87 |               977585.00 |              62872 |                            1780.00 |                62128 |                              7291.00 |
| mysql-1-1-3-1-2  | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       2 |         8 |      128 |        0 |                          127.84 |               977763.00 |              62568 |                            1661.00 |                62432 |                              7387.00 |
| mysql-1-1-3-1-3  | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       3 |         8 |      128 |        0 |                          127.82 |               977968.00 |              62540 |                            1693.00 |                62460 |                              7415.00 |
| mysql-1-1-3-1-4  | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       4 |         8 |      128 |        0 |                          127.87 |               977554.00 |              62548 |                            1690.00 |                62452 |                              7283.00 |
| mysql-1-1-3-1-5  | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       5 |         8 |      128 |        0 |                          127.80 |               978084.00 |              62577 |                            1776.00 |                62423 |                              7183.00 |
| mysql-1-1-3-1-6  | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       6 |         8 |      128 |        0 |                          127.83 |               977824.00 |              62307 |                            1843.00 |                62693 |                              7459.00 |
| mysql-1-1-3-1-7  | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       7 |         8 |      128 |        0 |                          127.84 |               977804.00 |              62505 |                            1755.00 |                62495 |                              7503.00 |
| mysql-1-1-3-1-8  | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       8 |         8 |      128 |        0 |                          127.87 |               977536.00 |              62754 |                            1757.00 |                62246 |                              7479.00 |
| mysql-1-1-4-1-1  | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       1 |         8 |      128 |        0 |                          127.74 |               489282.00 |              31199 |                            1583.00 |                31301 |                              6783.00 |
| mysql-1-1-4-1-2  | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       2 |         8 |      128 |        0 |                          127.72 |               489358.00 |              31389 |                            1606.00 |                31111 |                              6763.00 |
| mysql-1-1-4-1-3  | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       3 |         8 |      128 |        0 |                          127.75 |               489233.00 |              31195 |                            1595.00 |                31305 |                              6823.00 |
| mysql-1-1-4-1-4  | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       4 |         8 |      128 |        0 |                          127.75 |               489254.00 |              31403 |                            1627.00 |                31097 |                              6707.00 |
| mysql-1-1-4-1-5  | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       5 |         8 |      128 |        0 |                          127.74 |               489294.00 |              30959 |                            1662.00 |                31541 |                              6811.00 |
| mysql-1-1-4-1-6  | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       6 |         8 |      128 |        0 |                          127.75 |               489230.00 |              31418 |                            1657.00 |                31082 |                              6763.00 |
| mysql-1-1-4-1-7  | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       7 |         8 |      128 |        0 |                          127.74 |               489290.00 |              31215 |                            1584.00 |                31285 |                              6735.00 |
| mysql-1-1-4-1-8  | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       8 |         8 |      128 |        0 |                          127.74 |               489293.00 |              31055 |                            1600.00 |                31445 |                              6627.00 |
| mysql-1-1-4-1-9  | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       9 |         8 |      128 |        0 |                          127.74 |               489286.00 |              31303 |                            1660.00 |                31197 |                              6787.00 |
| mysql-1-1-4-1-10 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |      10 |         8 |      128 |        0 |                          127.75 |               489242.00 |              31545 |                            1605.00 |                30955 |                              6699.00 |
| mysql-1-1-4-1-11 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |      11 |         8 |      128 |        0 |                          127.75 |               489226.00 |              31167 |                            1557.00 |                31333 |                              6675.00 |
| mysql-1-1-4-1-12 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |      12 |         8 |      128 |        0 |                          127.71 |               489388.00 |              31235 |                            1676.00 |                31265 |                              6699.00 |
| mysql-1-1-4-1-13 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |      13 |         8 |      128 |        0 |                          127.74 |               489273.00 |              31144 |                            1695.00 |                31356 |                              6767.00 |
| mysql-1-1-4-1-14 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |      14 |         8 |      128 |        0 |                          127.75 |               489239.00 |              31358 |                            1610.00 |                31142 |                              6739.00 |
| mysql-1-1-4-1-15 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |      15 |         8 |      128 |        0 |                          127.75 |               489222.00 |              31339 |                            1576.00 |                31161 |                              6571.00 |
| mysql-1-1-4-1-16 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |      16 |         8 |      128 |        0 |                          127.75 |               489235.00 |              31014 |                            1620.00 |                31486 |                              6863.00 |
| mysql-1-2-1-1-1  | mysql-1-2-1 | mysql-1-2-1-1 |                2 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1021.67 |               978788.00 |             499502 |                            2113.00 |               500498 |                              7243.00 |
| mysql-1-2-2-1-1  | mysql-1-2-2 | mysql-1-2-2-1 |                2 |        2 |               1 |       1 |        64 |     1024 |        0 |                         1016.97 |               491655.00 |             250219 |                            1498.00 |               249781 |                              6843.00 |
| mysql-1-2-2-1-2  | mysql-1-2-2 | mysql-1-2-2-1 |                2 |        2 |               1 |       2 |        64 |     1024 |        0 |                         1018.09 |               491114.00 |             249679 |                            1455.00 |               250321 |                              6851.00 |
| mysql-1-2-3-1-1  | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       1 |         8 |      128 |        0 |                          127.81 |               978039.00 |              62418 |                            1642.00 |                62582 |                              6691.00 |
| mysql-1-2-3-1-2  | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       2 |         8 |      128 |        0 |                          127.84 |               977761.00 |              62028 |                            1572.00 |                62972 |                              6515.00 |
| mysql-1-2-3-1-3  | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       3 |         8 |      128 |        0 |                          127.83 |               977826.00 |              62227 |                            1727.00 |                62773 |                              6703.00 |
| mysql-1-2-3-1-4  | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       4 |         8 |      128 |        0 |                          127.84 |               977751.00 |              62515 |                            1671.00 |                62485 |                              6455.00 |
| mysql-1-2-3-1-5  | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       5 |         8 |      128 |        0 |                          127.83 |               977844.00 |              62271 |                            1613.00 |                62729 |                              6451.00 |
| mysql-1-2-3-1-6  | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       6 |         8 |      128 |        0 |                          127.80 |               978056.00 |              62572 |                            1658.00 |                62428 |                              6567.00 |
| mysql-1-2-3-1-7  | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       7 |         8 |      128 |        0 |                          127.82 |               977915.00 |              62481 |                            1596.00 |                62519 |                              6839.00 |
| mysql-1-2-3-1-8  | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       8 |         8 |      128 |        0 |                          127.84 |               977770.00 |              62439 |                            1589.00 |                62561 |                              6603.00 |
| mysql-1-2-4-1-1  | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       1 |         8 |      128 |        0 |                          127.75 |               489224.00 |              31185 |                            1703.00 |                31315 |                              7067.00 |
| mysql-1-2-4-1-2  | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       2 |         8 |      128 |        0 |                          127.73 |               489299.00 |              31232 |                            1615.00 |                31268 |                              7103.00 |
| mysql-1-2-4-1-3  | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       3 |         8 |      128 |        0 |                          127.76 |               489195.00 |              31330 |                            1612.00 |                31170 |                              6819.00 |
| mysql-1-2-4-1-4  | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       4 |         8 |      128 |        0 |                          127.73 |               489301.00 |              31271 |                            1622.00 |                31229 |                              7075.00 |
| mysql-1-2-4-1-5  | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       5 |         8 |      128 |        0 |                          127.74 |               489294.00 |              31222 |                            1570.00 |                31278 |                              7011.00 |
| mysql-1-2-4-1-6  | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       6 |         8 |      128 |        0 |                          127.76 |               489188.00 |              31228 |                            1627.00 |                31272 |                              6891.00 |
| mysql-1-2-4-1-7  | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       7 |         8 |      128 |        0 |                          127.74 |               489257.00 |              31321 |                            1646.00 |                31179 |                              6907.00 |
| mysql-1-2-4-1-8  | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       8 |         8 |      128 |        0 |                          127.74 |               489284.00 |              31432 |                            1597.00 |                31068 |                              6959.00 |
| mysql-1-2-4-1-9  | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       9 |         8 |      128 |        0 |                          127.74 |               489274.00 |              31396 |                            1579.00 |                31104 |                              6987.00 |
| mysql-1-2-4-1-10 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |      10 |         8 |      128 |        0 |                          127.75 |               489230.00 |              31318 |                            1642.00 |                31182 |                              7003.00 |
| mysql-1-2-4-1-11 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |      11 |         8 |      128 |        0 |                          127.72 |               489351.00 |              31151 |                            1675.00 |                31349 |                              6979.00 |
| mysql-1-2-4-1-12 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |      12 |         8 |      128 |        0 |                          127.77 |               489173.00 |              31170 |                            1646.00 |                31330 |                              6927.00 |
| mysql-1-2-4-1-13 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |      13 |         8 |      128 |        0 |                          127.72 |               489357.00 |              31221 |                            1682.00 |                31279 |                              7083.00 |
| mysql-1-2-4-1-14 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |      14 |         8 |      128 |        0 |                          127.75 |               489231.00 |              31317 |                            1624.00 |                31183 |                              6963.00 |
| mysql-1-2-4-1-15 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |      15 |         8 |      128 |        0 |                          127.73 |               489332.00 |              31306 |                            1592.00 |                31194 |                              7011.00 |
| mysql-1-2-4-1-16 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |      16 |         8 |      128 |        0 |                          127.74 |               489290.00 |              31212 |                            1583.00 |                31288 |                              7031.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1021.90 |               978567.00 |             500452 |                            1744.00 |               499548 |                              7235.00 |
| mysql-1-1-2 | mysql-1-1-2 |                1 |        2 |               1 |           2 |       128 |     2048 |        0 |                         2032.94 |               492262.00 |             500386 |                            1506.00 |               499614 |                              6919.00 |
| mysql-1-1-3 | mysql-1-1-3 |                1 |        3 |               1 |           8 |        64 |     1024 |        0 |                         1022.74 |               978084.00 |             500671 |                            1843.00 |               499329 |                              7503.00 |
| mysql-1-1-4 | mysql-1-1-4 |                1 |        4 |               1 |          16 |       128 |     2048 |        0 |                         2043.85 |               489388.00 |             499938 |                            1695.00 |               500062 |                              6863.00 |
| mysql-1-2-1 | mysql-1-2-1 |                2 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1021.67 |               978788.00 |             499502 |                            2113.00 |               500498 |                              7243.00 |
| mysql-1-2-2 | mysql-1-2-2 |                2 |        2 |               1 |           2 |       128 |     2048 |        0 |                         2035.07 |               491655.00 |             499898 |                            1498.00 |               500102 |                              6851.00 |
| mysql-1-2-3 | mysql-1-2-3 |                2 |        3 |               1 |           8 |        64 |     1024 |        0 |                         1022.63 |               978056.00 |             498951 |                            1727.00 |               501049 |                              6839.00 |
| mysql-1-2-4 | mysql-1-2-4 |                2 |        4 |               1 |          16 |       128 |     2048 |        0 |                         2043.87 |               489357.00 |             500312 |                            1703.00 |               499688 |                              7103.00 |

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MySQL-1)
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loading completed without failures
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
* Duration: 1378s 
* Code: 1794715697
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
  * Experiment uses bexhoma version 0.11.17.
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1046837
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
    * code:1794715697

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MySQL-1

### Data Parameters of Reused Volumes
* MySQL-1: DDL values of the volume: row_format=DYNAMIC, collation=utf8mb4_0900_ai_ci
* MySQL-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794715697-57f6f85456-rnclb: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (8 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (8 pods)

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   [SCAN].Return=OK |   [SCAN].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-------------------:|-----------------------------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 |         8 |      128 |        0 |                          127.82 |               977965.00 |                 6276 |                              8431.00 |             118724 |                            5943.00 |
| mysql-1-1-1-1-2 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       2 |         8 |      128 |        0 |                          127.83 |               977830.00 |                 6289 |                              8591.00 |             118711 |                            5975.00 |
| mysql-1-1-1-1-3 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       3 |         8 |      128 |        0 |                          127.80 |               978092.00 |                 6206 |                              8407.00 |             118794 |                            5883.00 |
| mysql-1-1-1-1-4 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       4 |         8 |      128 |        0 |                          127.82 |               977942.00 |                 6326 |                              8351.00 |             118674 |                            5827.00 |
| mysql-1-1-1-1-5 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       5 |         8 |      128 |        0 |                          127.83 |               977868.00 |                 6245 |                              8231.00 |             118755 |                            5847.00 |
| mysql-1-1-1-1-6 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       6 |         8 |      128 |        0 |                          127.83 |               977840.00 |                 6281 |                              8743.00 |             118719 |                            6015.00 |
| mysql-1-1-1-1-7 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       7 |         8 |      128 |        0 |                          127.84 |               977779.00 |                 6327 |                              8495.00 |             118673 |                            5915.00 |
| mysql-1-1-1-1-8 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       8 |         8 |      128 |        0 |                          127.83 |               977860.00 |                 6251 |                              8107.00 |             118749 |                            6131.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   [SCAN].Return=OK |   [SCAN].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-------------------:|-----------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           8 |        64 |     1024 |        0 |                         1022.60 |               978092.00 |                50201 |                              8743.00 |             949799 |                            6131.00 |

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MySQL-1)
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
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
* Duration: 2361s 
* Code: 1794717092
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
  * Experiment uses bexhoma version 0.11.17.
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1046832
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
    * code:1794717092
* mysql-1-1-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1046826
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
    * code:1794717092

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MySQL-1

### Data Parameters of Reused Volumes
* MySQL-1: DDL values of the volume: row_format=DYNAMIC, collation=utf8mb4_0900_ai_ci
* MySQL-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794717092-7885b86cd9-9hmr7: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: ycsb (8 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: ycsb (8 pods)

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1021.47 |               978982.00 |             500027 |                            2085.00 |               499973 |                              7283.00 |
| mysql-1-1-2-1-1 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       1 |         8 |      128 |        0 |                          127.88 |               977477.00 |              62459 |                            1700.00 |                62541 |                              6839.00 |
| mysql-1-1-2-1-2 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       2 |         8 |      128 |        0 |                          127.88 |               977471.00 |              62607 |                            1634.00 |                62393 |                              6655.00 |
| mysql-1-1-2-1-3 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       3 |         8 |      128 |        0 |                          127.88 |               977514.00 |              62485 |                            1731.00 |                62515 |                              6699.00 |
| mysql-1-1-2-1-4 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       4 |         8 |      128 |        0 |                          127.88 |               977459.00 |              62229 |                            1614.00 |                62771 |                              6799.00 |
| mysql-1-1-2-1-5 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       5 |         8 |      128 |        0 |                          127.87 |               977525.00 |              62544 |                            1617.00 |                62456 |                              6803.00 |
| mysql-1-1-2-1-6 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       6 |         8 |      128 |        0 |                          127.88 |               977492.00 |              62521 |                            1709.00 |                62479 |                              6835.00 |
| mysql-1-1-2-1-7 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       7 |         8 |      128 |        0 |                          127.88 |               977484.00 |              62490 |                            1683.00 |                62510 |                              6647.00 |
| mysql-1-1-2-1-8 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       8 |         8 |      128 |        0 |                          127.88 |               977450.00 |              62265 |                            1665.00 |                62735 |                              6731.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1021.47 |               978982.00 |             500027 |                            2085.00 |               499973 |                              7283.00 |
| mysql-1-1-2 | mysql-1-1-2 |                1 |        2 |               1 |           8 |        64 |     1024 |        0 |                         1023.03 |               977525.00 |             499600 |                            1731.00 |               500400 |                              6839.00 |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       262.84 |      0.33 |           4.70 |                  4.95 |
| mysql-1-1-2-1 |       255.74 |      0.31 |           4.73 |                  5.23 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       517.01 |      3.97 |           0.37 |                  0.37 |
| mysql-1-1-2-1 |       545.68 |      1.84 |           0.13 |                  0.14 |

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
* TEST passed: Loading completed without failures
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
