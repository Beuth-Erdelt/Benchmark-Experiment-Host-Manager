# Example: Benchmark MariaDB ColumnStore

This example shows how to benchmark MariaDB ColumnStore with TPC-H, TPC-DS and SSB on a single node.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

[MariaDB ColumnStore](https://mariadb.com/docs/analytics/mariadb-columnstore) is the columnar storage engine of MariaDB, GPL-2.0, under the name `MariaDBCS` in bexhoma.
The template uses the official image `mariadb:12.3.3`, the same server as the template of MariaDB, and installs the plugin `mariadb-plugin-columnstore` at every start.
So the pods need access to `archive.mariadb.org` and the Ubuntu mirrors.
Queries run over JDBC, loaders and init scripts use the `mariadb` client.

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. [MariaDB ColumnStore](https://mariadb.com/docs/analytics/mariadb-columnstore)
1. [MariaDB in Docker](https://hub.docker.com/_/mariadb)
1. [TPC-H](https://www.tpc.org/tpch/)
1. [TPC-DS](https://www.tpc.org/tpcds/)
1. [Star Schema Benchmark](https://www.cs.umb.edu/~poneil/StarSchemaB.PDF)
1. [Orchestrating DBMS Benchmarking in the Cloud with Kubernetes](https://doi.org/10.1007/978-3-030-94437-7_6)
1. [A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools](https://doi.org/10.1007/978-3-031-68031-1_9)
1. Test script of this page: [test-docs-mariadbcs.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-mariadbcs.sh), [test-docs-mariadbcs.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-mariadbcs.ps1)


## Perform TPC-H Benchmark

```bash
LOG_DIR="./logs_tests"
BEXHOMA_MS=10
BEXHOMA_STORAGE_CLASS="nvme"

mkdir -p $LOG_DIR
```

For performing the experiment we can run the [tpch file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpch.py).

Example:
```bash
bexhoma tpch \
  -dbms MariaDBCS \
  -sf 1 \
  -nlp 8 \
  -xis \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 16Gi \
  -rr 16Gi \
  -nc 1 \
  -ks no \
  run &>$LOG_DIR/docs_tpch_mariadbcs.log
```

This
* starts a clean instance of MariaDB ColumnStore (`-dbms`)
  * with a limit of 16 GiB RAM (`-rr`, `-lr`)
  * data directory inside the container
* creates the TPC-H schema
* loads the data with one loader pod, whatever `-nlp` says, see [Loading](#loading)
* computes statistics (`-xis`); ColumnStore has no keys and no secondary indexes
* runs the check script (row counts, sizes)
* runs 1 stream of the 22 TPC-H queries
* tests if results match workflow (`-tr`)
* removes the SUT at the end (`-ks no`)
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
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_mariadbcs_summary.md" target="_blank" rel="noopener">docs_tpch_mariadbcs.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 466s 
* Code: 1794817279
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Import sets statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * Experiment is limited to DBMS ['MariaDBCS'].
  * Import is handled by 8 processes (pods).
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM. RAM limit is 16Gi.

### Connections
* mariadbcs-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:1077381263360
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-137-generic
  * node:cl-worker27
  * disk:902996
  * datadisk:512
  * cpu_list:0-255
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794817279

### Ingestion
* MariaDBCS-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-mariadbcs-1-1794817279-7f45847dbf-xmqb8: 0

### Workflow

#### Actual

* DBMS MariaDBCS-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MariaDBCS-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

| DBMS          |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:--------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDBCS-1-1 |                1 |    1 |      129.00 |           4.00 |            0.00 |         98.00 |           15.00 |              1 |         0 |             | None           |             0 | False         |               27.91 | False               |

### Benchmarking

#### Per Connection

| connection          | phase           | job               |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadbcs-1-1-1-1-1 | mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         28 |            0.81 |             4453.60 |           2828.57 |          -1 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadbcs-1-1-1 | mariadbcs-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         28 |            0.81 |             4453.60 |           2828.57 |          -1 |

#### Query Completion per Phase

| phase           |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| mariadbcs-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   mariadbcs-1-1-1-1-1 |
|:----------------------------------------------------|----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |               1243.39 |
| Minimum Cost Supplier Query (TPC-H Q2)              |               3783.25 |
| Shipping Priority (TPC-H Q3)                        |               1604.69 |
| Order Priority Checking Query (TPC-H Q4)            |                604.23 |
| Local Supplier Volume (TPC-H Q5)                    |                961.91 |
| Forecasting Revenue Change (TPC-H Q6)               |                 25.87 |
| Volume Shipping Query (TPC-H Q7)                    |               1495.47 |
| National Market Share (TPC-H Q8)                    |               1123.19 |
| Product Type Profit Measure (TPC-H Q9)              |               1620.30 |
| Returned Item Reporting Query (TPC-H Q10)           |                961.63 |
| Important Stock Identification (TPC-H Q11)          |                943.88 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                521.90 |
| Customer Distribution (TPC-H Q13)                   |               1493.14 |
| Promotion Effect Query (TPC-H Q14)                  |                370.13 |
| Top Supplier Query (TPC-H Q15)                      |                357.18 |
| Parts/Supplier Relationship (TPC-H Q16)             |                903.33 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                750.56 |
| Large Volume Customer (TPC-H Q18)                   |                745.73 |
| Discounted Revenue (TPC-H Q19)                      |                438.47 |
| Potential Part Promotion (TPC-H Q20)                |               1145.20 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |               2109.27 |
| Global Sales Opportunity Query (TPC-H Q22)          |                599.13 |

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
At SF=1, the 22 queries take about 25 seconds on ColumnStore, so this run uses SF=10 (`-sf`), with a RAM limit of 64 GiB (at 16 GiB the SUT was OOM-killed at SF=10).
ColumnStore has no Prometheus exporter in bexhoma, so there are no application metrics (`-ma`).

```bash
bexhoma tpch \
  -dbms MariaDBCS \
  -sf 10 \
  -nlp 8 \
  -xis \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -nc 1 \
  -ks no \
  run &>$LOG_DIR/docs_tpch_mariadbcs_monitoring.log
```

### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_mariadbcs_monitoring_summary.md" target="_blank" rel="noopener">docs_tpch_mariadbcs_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=10
* Type: tpch
* Duration: 1087s 
* Code: 1794817775
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Import sets statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MariaDBCS'].
  * Import is handled by 8 processes (pods).
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mariadbcs-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:1077381263360
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-137-generic
  * node:cl-worker27
  * disk:909497
  * datadisk:4531
  * cpu_list:0-255
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794817775

### Ingestion
* MariaDBCS-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-mariadbcs-1-1794817775-7657444dc7-hbfvw: 0

### Workflow

#### Actual

* DBMS MariaDBCS-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MariaDBCS-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

| DBMS          |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:--------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDBCS-1-1 |                1 |   10 |      747.00 |           4.00 |            0.00 |        714.00 |           21.00 |              1 |         0 |             | None           |             0 | False         |               48.19 | False               |

### Benchmarking

#### Per Connection

| connection          | phase           | job               |   experiment_run |   client |   benchmark_run |   child |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadbcs-1-1-1-1-1 | mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |       1 | 10.00 |               22 |                  22 |         90 |            2.74 |            13131.66 |           8800.00 |          -1 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadbcs-1-1-1 | mariadbcs-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |                  22 |         90 |            2.74 |            13131.66 |           8800.00 |          -1 |

#### Query Completion per Phase

| phase           |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| mariadbcs-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   mariadbcs-1-1-1-1-1 |
|:----------------------------------------------------|----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |               3303.77 |
| Minimum Cost Supplier Query (TPC-H Q2)              |               4396.74 |
| Shipping Priority (TPC-H Q3)                        |               2198.75 |
| Order Priority Checking Query (TPC-H Q4)            |               5563.13 |
| Local Supplier Volume (TPC-H Q5)                    |               1919.73 |
| Forecasting Revenue Change (TPC-H Q6)               |                671.14 |
| Volume Shipping Query (TPC-H Q7)                    |              10830.87 |
| National Market Share (TPC-H Q8)                    |               1658.93 |
| Product Type Profit Measure (TPC-H Q9)              |               5301.58 |
| Returned Item Reporting Query (TPC-H Q10)           |               4893.75 |
| Important Stock Identification (TPC-H Q11)          |               1105.09 |
| Shipping Modes and Order Priority (TPC-H Q12)       |               1495.39 |
| Customer Distribution (TPC-H Q13)                   |              12915.39 |
| Promotion Effect Query (TPC-H Q14)                  |               1062.06 |
| Top Supplier Query (TPC-H Q15)                      |                639.77 |
| Parts/Supplier Relationship (TPC-H Q16)             |               1204.71 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               3672.33 |
| Large Volume Customer (TPC-H Q18)                   |               2964.53 |
| Discounted Revenue (TPC-H Q19)                      |               1012.88 |
| Potential Part Promotion (TPC-H Q20)                |               6922.03 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |              11384.01 |
| Global Sales Opportunity Query (TPC-H Q22)          |               2667.45 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadbcs-1-1-1-1 |      1174.54 |      6.52 |           6.14 |                 10.73 |

### Loading phase: component data generator

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadbcs-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadbcs-1-1-1-1 |        17.82 |      0.07 |           0.03 |                 10.39 |

### Benchmarking phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadbcs-1-1-1-1 |      1495.69 |     22.40 |          16.67 |                 20.77 |

### Benchmarking phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadbcs-1-1-1-1 |        11.93 |      0.37 |           0.38 |                  0.39 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loading.log, expected: series exists only while non-zero)

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


## Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.
With repetitions (`-nc`), `-rsr` removes an existing volume only before the first repetition and later repetitions reuse it without loading; `-rsrp` removes it before every repetition. See [Concepts](Concepts.html).

```bash
bexhoma tpch \
  -dbms MariaDB MariaDBCS \
  -sf 1 \
  -nlp 8 \
  -xii \
  -xic \
  -xis \
  -xdt \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 16Gi \
  -rr 16Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 20Gi \
  -rsr \
  -nc 2 \
  -ar \
  -ks no \
  run &>$LOG_DIR/docs_tpch_mariadbcs_storage.log
```

This
* starts a clean instance of MariaDB and of MariaDB ColumnStore (`-dbms`)
  * data on a persistent volume of 20 GiB (`-rss`) of the storage class `$BEXHOMA_STORAGE_CLASS` (`-rst`), removed first if it exists (`-rsr`)
* loads MariaDB with 8 loader pods (`-nlp`), MariaDBCS with one
* runs the post-load scripts: indexes (`-xii`), constraints (`-xic`) and statistics (`-xis`) for MariaDB; only the statistics do something for MariaDBCS
* runs 1 stream of the 22 TPC-H queries and stores their result sets (`-xdt`)
* repeats the benchmark once more (`-nc 2`): bexhoma restarts the SUT, which finds the data on the volume and does not load again
* runs the reset scripts before each round (`-ar`)
* monitors the SUT (`-m`)

### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_mariadbcs_storage_summary.md" target="_blank" rel="noopener">docs_tpch_mariadbcs_storage.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 1155s 
* Code: 1794818916
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MariaDB', 'MariaDBCS'].
  * Import is handled by 8 processes (pods).
  * Database is persisted to disk of type nvme and size 20Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM. RAM limit is 16Gi.

### Connections
* mariadb-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:1077381263360
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-137-generic
  * node:cl-worker27
  * disk:904691
  * datadisk:1962
  * volume_size:20G
  * volume_used:2.0G
  * cpu_list:0-255
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794818916
* mariadb-1-2-1-1-1 uses docker image mariadb:12.3.3
  * RAM:1077381263360
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-137-generic
  * node:cl-worker27
  * disk:905341
  * datadisk:1963
  * volume_size:20G
  * volume_used:2.0G
  * cpu_list:0-255
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794818916
* mariadbcs-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:1077381263360
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-137-generic
  * node:cl-worker27
  * disk:904886
  * datadisk:512
  * volume_size:20G
  * volume_used:673M
  * cpu_list:0-255
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794818916
* mariadbcs-1-2-1-1-1 uses docker image mariadb:12.3.3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:642528
  * datadisk:511
  * volume_size:20G
  * volume_used:673M
  * cpu_list:0-127
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794818916

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MariaDB-1-2, MariaDBCS-1-2

### Data Parameters of Reused Volumes
* MariaDB-1: DDL values of the volume: engine=InnoDB, histograms=off
* MariaDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics
* MariaDBCS-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### Ingestion
* MariaDB-1: 50 of 50 units ok
* MariaDBCS-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1794818916-75869b58f5-89pnm: 0
* bexhoma-sut-mariadb-1-1794818916-7464bb8dd-jwt79: 0
* bexhoma-sut-mariadbcs-1-1794818916-5897c48f87-xbhkr: 0
* bexhoma-sut-mariadbcs-1-1794818916-77b46c88d6-qxz6s: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS MariaDBCS-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MariaDBCS-1 - Experiment 2 Client 1: tpch (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS MariaDBCS-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MariaDBCS-1 - Experiment 2 Client 1: tpch (1 pods)

### Loading

#### Per Run

| DBMS          |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:--------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1   |                1 |    1 |       93.00 |           4.00 |            7.00 |         25.00 |           46.00 |              8 |         0 |             | None           |             0 | False         |               38.71 | False               |
| MariaDB-1-2   |                2 |    1 |       93.00 |           4.00 |            7.00 |         25.00 |           46.00 |              8 |         0 |             | None           |             0 | False         |               38.71 | True                |
| MariaDBCS-1-1 |                1 |    1 |      120.00 |           6.00 |            0.00 |         93.00 |           19.00 |              1 |         0 |             | None           |             0 | False         |               30.00 | False               |
| MariaDBCS-1-2 |                2 |    1 |      120.00 |           6.00 |            0.00 |         93.00 |           19.00 |              1 |         0 |             | None           |             0 | False         |               30.00 | True                |

### Benchmarking

#### Per Connection

| connection          | phase           | job               |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1-1-1   | mariadb-1-1-1   | mariadb-1-1-1-1   |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |        142 |            1.48 |             2556.84 |            557.75 |          -1 |
| mariadb-1-2-1-1-1   | mariadb-1-2-1   | mariadb-1-2-1-1   |                2 |        1 |               1 |       1 | 1.00 |               22 |                  22 |        136 |            1.47 |             2578.25 |            582.35 |          -1 |
| mariadbcs-1-1-1-1-1 | mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         29 |            0.85 |             4317.20 |           2731.03 |          -1 |
| mariadbcs-1-2-1-1-1 | mariadbcs-1-2-1 | mariadbcs-1-2-1-1 |                2 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         28 |            0.74 |             4954.38 |           2828.57 |          -1 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1   | mariadb-1-1-1   |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |        142 |            1.48 |             2556.84 |            557.75 |          -1 |
| mariadb-1-2-1   | mariadb-1-2-1   |                2 |        1 |               1 |           1 | 1.00 |               22 |                  22 |        136 |            1.47 |             2578.25 |            582.35 |          -1 |
| mariadbcs-1-1-1 | mariadbcs-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         29 |            0.85 |             4317.20 |           2731.03 |          -1 |
| mariadbcs-1-2-1 | mariadbcs-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         28 |            0.74 |             4954.38 |           2828.57 |          -1 |

#### Query Completion per Phase

| phase           |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| mariadb-1-1-1   |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| mariadb-1-2-1   |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| mariadbcs-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| mariadbcs-1-2-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

#### Reset

| phase           | job               |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:----------------|:------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| mariadb-1-1-1   | mariadb-1-1-1-1   |                1 |        1 |               1 |         4.00 |                |
| mariadb-1-2-1   | mariadb-1-2-1-1   |                2 |        1 |               1 |         3.00 |                |
| mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |         6.00 |                |
| mariadbcs-1-2-1 | mariadbcs-1-2-1-1 |                2 |        1 |               1 |         4.00 |                |

### Latency of Timer Execution [ms]
| Queries                                             |   mariadb-1-1-1-1-1 |   mariadb-1-2-1-1-1 |   mariadbcs-1-1-1-1-1 |   mariadbcs-1-2-1-1-1 |
|:----------------------------------------------------|--------------------:|--------------------:|----------------------:|----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |            11022.79 |            10719.29 |               1363.19 |               1246.51 |
| Minimum Cost Supplier Query (TPC-H Q2)              |              680.47 |              617.17 |               3695.81 |               2628.41 |
| Shipping Priority (TPC-H Q3)                        |             2291.96 |             2516.05 |               1577.51 |               1249.79 |
| Order Priority Checking Query (TPC-H Q4)            |              490.40 |              553.88 |                621.07 |                794.99 |
| Local Supplier Volume (TPC-H Q5)                    |             1235.03 |             1282.49 |                881.65 |                689.05 |
| Forecasting Revenue Change (TPC-H Q6)               |             1471.17 |             1632.84 |                 25.99 |                 45.21 |
| Volume Shipping Query (TPC-H Q7)                    |             1542.33 |             1423.74 |               1476.84 |               1108.10 |
| National Market Share (TPC-H Q8)                    |             2557.94 |             2365.60 |               1171.23 |                838.80 |
| Product Type Profit Measure (TPC-H Q9)              |             2435.26 |             2342.47 |               1585.62 |               1110.25 |
| Returned Item Reporting Query (TPC-H Q10)           |             1061.81 |             1138.54 |               1193.10 |               1090.24 |
| Important Stock Identification (TPC-H Q11)          |              164.32 |              228.01 |                962.61 |                696.86 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             4336.65 |             4473.23 |                590.34 |                423.13 |
| Customer Distribution (TPC-H Q13)                   |             3861.14 |             3491.90 |               1522.52 |               2091.82 |
| Promotion Effect Query (TPC-H Q14)                  |            17252.14 |            13983.37 |                395.87 |                327.83 |
| Top Supplier Query (TPC-H Q15)                      |             3128.26 |             2989.20 |                339.52 |                313.06 |
| Parts/Supplier Relationship (TPC-H Q16)             |              253.28 |              254.22 |               1015.39 |                753.89 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               72.42 |               82.87 |                781.31 |                745.76 |
| Large Volume Customer (TPC-H Q18)                   |             4518.37 |             4218.28 |                843.15 |                783.33 |
| Discounted Revenue (TPC-H Q19)                      |              181.32 |              157.12 |                488.44 |                408.52 |
| Potential Part Promotion (TPC-H Q20)                |              362.84 |              346.56 |               1314.86 |                880.33 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            76893.26 |            77246.15 |               1737.36 |               1363.99 |
| Global Sales Opportunity Query (TPC-H Q22)          |              191.04 |              160.31 |                571.97 |                569.70 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   |       151.43 |      4.79 |           2.03 |                  2.04 |
| mariadbcs-1-1-1-1 |       115.68 |      1.44 |           3.27 |                  3.70 |

### Loading phase: component data generator

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   | n/a          |      0.00 |           0.00 |                  0.00 |
| mariadbcs-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   | n/a          |      0.00 |           0.02 |                  0.29 |
| mariadbcs-1-1-1-1 | 2.17         |      0.02 |           0.01 |                  1.02 |

### Benchmarking phase: SUT deployment

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   | 116.56       |      1.00 |           2.05 |                  2.06 |
| mariadb-1-2-1-1   | 129.20       |      1.00 |           1.88 |                  1.88 |
| mariadbcs-1-1-1-1 | n/a          |      0.32 |           5.59 |                  6.29 |
| mariadbcs-1-2-1-1 | n/a          |      5.93 |           3.85 |                  4.04 |

### Benchmarking phase: component benchmarker

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   | 13.14        |      0.34 |           0.31 |                  0.32 |
| mariadb-1-2-1-1   | 13.64        |      0.07 |           0.33 |                  0.34 |
| mariadbcs-1-1-1-1 | n/a          |      0.00 |           0.27 |                  0.28 |
| mariadbcs-1-2-1-1 | n/a          |      0.00 |           0.31 |                  0.32 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-2-1-1 (bexhoma-metrics-mariadb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-2-1-1 (bexhoma-metrics-mariadb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)

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
* TEST skipped: Monitoring metrics missing (data pre-existing; job pods ran shorter than scrape interval; phase shorter than scrape interval; series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
* TEST passed: Reset scripts ran without errors
```

</details>

### Compare Results

MariaDB runs next to MariaDBCS in this example to compare the result sets of both.
`-xdt` stores the result sets per connection, and the test `SQL warnings` compares those of all connections of the experiment.
So a run with MariaDB and MariaDBCS together shows if ColumnStore returns the same rows.
The stored numbers are rounded first, to `precision` of the query: in TPC-DS and SSB to whole numbers, so differences below that do not show.
Row counts of the check scripts are worth a look too, in the file `bexhoma-loading-mariadbcs-1-checkschema-*.stdout.log` of the result folder.

At SF 1 all queries of TPC-H and SSB, normal and flat, gave the same results on both, and the 99 queries of TPC-DS.
For 28 queries of TPC-DS this needs a variant of the query, see below.


## Refresh Stream

`-xrs N` runs the TPC-H refresh functions RF1 (insert new orders) and RF2 (delete old orders) as an additional job next to the query streams, see [TPC-H](Example-TPC-H.md#refresh-stream).
For MariaDBCS, the loader image of MariaDB is used: RF1 is applied with `LOAD DATA LOCAL INFILE` and RF2 with a temporary table and a `DELETE` joined to it, against tables with `ENGINE = ColumnStore`.
Here, 3 query streams run in parallel with a refresh stream of 3 RF1+RF2 pairs.

```bash
bexhoma tpch \
  -dbms MariaDBCS \
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
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_mariadbcs_refresh.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_mariadbcs_refresh_summary.md" target="_blank" rel="noopener">docs_tpch_mariadbcs_refresh.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 324s 
* Code: 1794836745
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * A TPC-H refresh stream (RF1+RF2) runs in parallel, with 3 pair(s) applied per round.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * Experiment is limited to DBMS ['MariaDBCS'].
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
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mariadbcs-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1269418
  * datadisk:512
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794836745
* mariadbcs-1-1-1-1-2 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1269418
  * datadisk:512
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794836745
* mariadbcs-1-1-1-1-3 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1269418
  * datadisk:512
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794836745

### Ingestion
* MariaDBCS-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-mariadbcs-1-1794836745-588794b647-5fjnx: 0

### Workflow

#### Actual

* DBMS MariaDBCS-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

#### Planned

* DBMS MariaDBCS-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

### Loading

#### Per Run

| DBMS          |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:--------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDBCS-1-1 |                1 |    1 |       83.00 |           4.00 |            0.00 |         64.00 |           13.00 |              1 |         0 |             | None           |             0 | False         |               43.37 | False               |

### Benchmarking

#### Per Connection

| connection          | phase           | job               |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadbcs-1-1-1-1-1 | mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         49 |            1.35 |             2667.69 |           1616.33 |          -1 |
| mariadbcs-1-1-1-1-2 | mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |       2 | 1.00 |               22 |                  22 |         40 |            1.37 |             2624.58 |           1980.00 |          -1 |
| mariadbcs-1-1-1-1-3 | mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |       3 | 1.00 |               22 |                  22 |         40 |            1.34 |             2679.09 |           1980.00 |          -1 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadbcs-1-1-1 | mariadbcs-1-1-1 |                1 |        1 |               1 |           3 | 1.00 |               66 |                  66 |         49 |            1.35 |             2657.01 |           4848.98 |          -1 |

#### Query Completion per Phase

| phase           |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| mariadbcs-1-1-1 |      3 | 3/3                                 | 3/3                                      | 3/3                            | 3/3                                        | 3/3                                | 3/3                                     | 3/3                                | 3/3                                | 3/3                                      | 3/3                                         | 3/3                                          | 3/3                                             | 3/3                                 | 3/3                                  | 3/3                              | 3/3                                       | 3/3                                        | 3/3                                 | 3/3                              | 3/3                                    | 3/3                                                   | 3/3                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### tpch_refresh

| connection          | phase           | job               |   experiment_run |   client |   benchmark_run |   pod_count | benchmark_begin     | benchmark_end       |   benchmark_duration |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|------------:|:--------------------|:--------------------|---------------------:|
| mariadbcs-1-1-1-2-1 | mariadbcs-1-1-1 | mariadbcs-1-1-1-2 |                1 |        1 |               2 |           1 | 2026-11-16 14:50:11 | 2026-11-16 14:50:44 |                   33 |

### Latency of Timer Execution [ms]
| Queries                                             |   mariadbcs-1-1-1-1-1 |   mariadbcs-1-1-1-1-2 |   mariadbcs-1-1-1-1-3 |
|:----------------------------------------------------|----------------------:|----------------------:|----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |               1184.68 |               1174.08 |               1202.26 |
| Minimum Cost Supplier Query (TPC-H Q2)              |               3536.83 |               3721.85 |               3681.23 |
| Shipping Priority (TPC-H Q3)                        |               1438.91 |               1465.45 |               1501.46 |
| Order Priority Checking Query (TPC-H Q4)            |               1513.13 |                519.01 |                536.59 |
| Local Supplier Volume (TPC-H Q5)                    |               3096.54 |               4177.24 |               4185.02 |
| Forecasting Revenue Change (TPC-H Q6)               |                577.29 |                609.55 |                630.98 |
| Volume Shipping Query (TPC-H Q7)                    |               3606.63 |               3807.16 |               3781.70 |
| National Market Share (TPC-H Q8)                    |               2027.40 |               2105.09 |               2153.19 |
| Product Type Profit Measure (TPC-H Q9)              |              10034.32 |               4235.13 |               4235.78 |
| Returned Item Reporting Query (TPC-H Q10)           |               9372.67 |               2981.79 |               2907.86 |
| Important Stock Identification (TPC-H Q11)          |               2320.75 |               1832.35 |               1865.52 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                998.17 |                682.91 |                669.87 |
| Customer Distribution (TPC-H Q13)                   |               1311.11 |                644.14 |                577.23 |
| Promotion Effect Query (TPC-H Q14)                  |                730.14 |               1230.44 |               1161.65 |
| Top Supplier Query (TPC-H Q15)                      |                391.53 |               1165.70 |               1117.27 |
| Parts/Supplier Relationship (TPC-H Q16)             |                740.35 |               1462.22 |               1776.61 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                773.17 |                994.00 |                772.99 |
| Large Volume Customer (TPC-H Q18)                   |                644.49 |               1681.21 |               1818.31 |
| Discounted Revenue (TPC-H Q19)                      |                446.30 |                395.17 |                410.91 |
| Potential Part Promotion (TPC-H Q20)                |                906.37 |               1590.65 |               1474.72 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |               1311.23 |               1318.59 |               1363.58 |
| Global Sales Opportunity Query (TPC-H Q22)          |                383.45 |                521.35 |                364.64 |

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

`MariaDBCS` uses the connection of MariaDB: JDBC with the MariaDB driver, `loadData` with the `mariadb` client, see [DBMS](DBMS.md#mariadb).

### Deployment

The template [deploymenttemplate-MariaDBCS.yml](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-MariaDBCS.yml) runs the official image `mariadb:12.3.3`, without a derived image.
The image `mariadb/columnstore` is stale (23.02.4).
The container command does what the package script cannot do in a container, which has no systemd:

| Point | Handling | Without it |
|---|---|---|
| Plugin | `apt-get install mariadb-plugin-columnstore` at every start (25.10.6, about 30 s), from the repository of the image, so the version follows the image tag | pods need access to `archive.mariadb.org` and the Ubuntu mirrors, else the SUT does not start |
| Daemons | workernode, controllernode, PrimProc, WriteEngineServer, DMLProc and DDLProc start before the server | writes fail with `ERROR 1815 ... DBRM is read only!` |
| Catalog | on the first start `dbbuilder 7`, `syscatalog_mysql.sql`, `install_mcs_mysql.sh` and `columnstore_info.sql`; a file on the volume marks them as done | no system catalog, no functions |
| Memory | `SystemConfig CGroup` points to `/tmp/mcs-cgroup`, a copy of the cgroup of the container with the number of cores added, so `NumBlocksPct` (`MCS_NUM_BLOCKS_PCT`, 20) and `TotalUmMemory` (`MCS_TOTAL_UM_MEMORY`, `65%`) apply to the memory limit of the pod | ColumnStore sizes by the RAM of the node and the pod is killed. With the cgroup of the container itself, `cpuset.cpus` is empty and ColumnStore runs on one core |
| Storage | `/var/lib/columnstore` and `/var/lib/mysql` are `subPath`s of one volume | the server's catalog is lost at a restart, while the data stays |
| Shared memory | `/dev/shm` is an `emptyDir` in memory, 2 GiB | BRM is held there; Kubernetes gives 64 MiB by default |
| Restart | `mcs-loadbrm.py` before the daemons, `mcs-savebrm.py` at `SIGTERM` | the extent map of the data is lost |
| Probes | `SELECT COUNT(*) FROM calpontsys.systable` | a plain `SELECT` is answered without the daemons |
| Logs | `rsyslogd` writes `/var/log/mariadb/columnstore/` | the daemons log via syslog only |
| `PrimProc` | restarted when it dies, with `ColumnStore: PrimProc died, restarting it` in the log of the SUT | all later queries fail, and the container looks healthy |

Set the shares per run with `--set deployment[bexhoma-deployment-mariadbcs].container[dbms].env.MCS_NUM_BLOCKS_PCT=30`.
Server options work as for MariaDB, `--set deployment[bexhoma-deployment-mariadbcs].container[dbms].max_connections=2000`.

### Loading

**Loading** uses the loader images of MariaDB: `LOAD DATA LOCAL` is passed to `cpimport`.
It always runs with one loader pod, and `-nlp` is ignored.
Concurrent `LOAD DATA` into one table fail with `ERROR 1030 ... from storage engine ColumnStore` before `cpimport` starts, and the loader script goes on, so rows would be missing without any test failing.
`cpimport` itself works in parallel, and loads of one table run one after the other anyway.
The limit of this path is `mariadbd`, which parses the file on one core: `lineitem` at SF 10 takes 495 s.

**Note: `cpimport` is only possible as a pull, so bexhoma does not use it.**
`cpimport` run in the SUT on the same file takes 55 s, but then the SUT reads the raw files itself, which is a different path than the sending loader pods of all other DBMS and not comparable.
A sending `cpimport` does not work: in a separate container with the plugin and the configuration of the SUT, `cpimport -m 1` reaches `WriteEngineServer`, the BRM controller and ExeMgr, and then fails with `MCS-2006: 'tpch.push_t' does not exist in Columnstore`, also with data on stdin, while the same call in the SUT works.
So loading times of MariaDBCS are not the best the DBMS can do.

### Schema and Scripts

Scripts: [TPC-H](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch/MariaDBCS), [TPC-DS](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpcds/MariaDBCS), [SSB](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ssb/MariaDBCS).
The columns are those of MariaDB with `ENGINE = ColumnStore`.
ColumnStore has no primary keys, foreign keys or secondary indexes, so `-xii` and `-xic` run scripts without statements.
`checkschema` reports the sizes with `columnstore_info`.
The TPC-H refresh stream (`-xrs`) is available, see [Refresh Stream](#refresh-stream).

### Queries

**Queries** run with dialect `MySQL`; the variants named `MariaDBCS` and `MariaDB` apply on top, as connection names start with them.
TPC-H (22) and SSB (13) run completely.
Compared with the result sets of MariaDB at SF 1 (`-xdt`, same run), all queries of TPC-H and SSB (normal and flat) are identical.
The numbers are compared as bexhoma stores them, rounded to `precision` of the query: whole numbers in TPC-DS and SSB.
All 99 queries of TPC-DS run, 28 of them with a `MariaDBCS` variant. Their results are the same. The test `SQL warnings` fails because of Q39: it has columns of the same name, so the comparison cannot sort its rows.

Without 11 of the variants ColumnStore 25.10.6 gives wrong results or fails, some of them without an error:

| Queries | Variant | Without it |
|---|---|---|
| Q47, Q57 | `lag()` and `lead()` in the CTE `v1` instead of two self joins of it, the final filter as `HAVING` of an outer `GROUP BY` | The instances of the CTE get mixed up, `nsum` equals `sum_sales`. A `WHERE` on a CTE also reaches its window functions: `with v as (select d_moy, d_dom, count(*) over (partition by d_moy) c from date_dim where d_year = 2000) select max(c) from v where d_dom <= 2` gives 2 instead of 31 |
| Q72 | The days of a week as CTE `date_pairs` | The join with `d_date_sk + off.k` over the derived table of offsets of the MariaDB variant gives no rows and no error; the main text ends in `MCS-2001` (memory of the join) |
| Q93 | Inner joins | `LEFT JOIN` with a filter on the outer table in `WHERE` keeps the rows without a match: 90,919 groups instead of 7,164 |
| Q18, Q22, Q27, Q36, Q67, Q70, Q86 | Rollup emulated with `UNION ALL` | `GROUP BY ... WITH ROLLUP` directly on a table kills `PrimProc` with a segmentation fault in `funcexp::FuncExp::evaluate`, also on 1,305 rows; very small tables do not show it. On a derived table it runs, but gives wrong results |

The other 17 variants are for queries that ColumnStore refuses as they are, see [TPC-DS queries](Queries-TPC-DS.html) for the rewrites:

| Queries | Result |
|---|---|
| Q28, Q61, Q77, Q88, Q90 | `MCS-1000: 'sub-query' and 'sub-query' are not joined` |
| Q10, Q35, Q45 | `MCS-3033: Correlated subquery within OR operator` |
| Q6, Q23, Q44 | `MCS-3022: Scalar subquery within a function` |
| Q8, Q14, Q38, Q87 | `INTERSECT`, `EXCEPT` are not supported |
| Q9 | `MCS-3016: Function or Operator with sub query on the SELECT clause` |
| Q21 | `MCS-1001: Function 'float_typecast' isn't supported` |


Memory depends on the number of cores of the node, since ColumnStore starts threads per core.
TPC-DS at SF 1 fits 16 Gi on nodes with 96 or 128 cores. On a node with 224 cores the SUT was killed at the limit of 16 Gi in Q18 (`OOMKilled`, `ExeMgr has allocated too much memory`), 32 Gi are enough there, with a peak of 14 GiB.
When `PrimProc` dies, queries fail at once with `MCS-2033` until it is back after about 3 s, so many queries of a stream are lost.

### Load Durability

There are no durability scripts, so `-xld` has no effect.

### Reset Scripts

With `-ar`, the reset runs before each benchmarking round:

1. Statistics: `ANALYZE TABLE`
2. Persist: n/a (no dirty pages to flush)
3. Counters: n/a (the check scripts read no ColumnStore counter)

See [Reset scripts](DBMS.md#reset-scripts--ar) for the reset contract.
There is no test run for MariaDBCS in [Test: Reset Scripts](Test-Reset.md) yet; the runs on this page use `-ar`.


## TPC-DS

For performing the experiment we can run the [tpcds file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpcds.py).

```bash
bexhoma tpcds \
  -dbms MariaDB MariaDBCS \
  -sf 1 \
  -xii \
  -xic \
  -xis \
  -xdt \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 32Gi \
  -rr 32Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 30Gi \
  -rsr \
  -nc 2 \
  -ar \
  -ks no \
  run &>$LOG_DIR/docs_tpcds_mariadbcs.log
```

All 99 queries of TPC-DS run on ColumnStore, 28 of them with a variant named `MariaDBCS`, see [Queries](#queries):

* 17 queries are refused by ColumnStore as they are, for example because it has no `INTERSECT` and no `EXCEPT`.
* 11 queries would crash ColumnStore 25.10.6 or return wrong rows without an error.

The test `SQL warnings` fails in this run because of Q39: it returns columns with the same name, so the comparison cannot sort its rows. The stored results of Q39 are the same on both.

The RAM limit is 32 GiB here, since memory depends on the number of cores of the node: ColumnStore starts threads per core.
16 GiB are enough on nodes with 96 or 128 cores, but on a node with 224 cores the SUT was killed at that limit.

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_mariadbcs_summary.md" target="_blank" rel="noopener">docs_tpcds_mariadbcs.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 1708s 
* Code: 1793820455
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1800. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MariaDB', 'MariaDBCS'].
  * Import is handled by 1 processes (pods).
  * Database is persisted to disk of type nvme and size 30Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 32Gi RAM. RAM limit is 32Gi.

### Connections
* mariadb-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:614198
  * datadisk:4569
  * volume_size:30G
  * volume_used:4.5G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:32Gi
  * limits_memory:32Gi
  * resources_total: 4.0 CPU, 32.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 32.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793820455
* mariadb-1-2-1-1-1 uses docker image mariadb:12.3.3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:611695
  * datadisk:4570
  * volume_size:30G
  * volume_used:4.5G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:32Gi
  * limits_memory:32Gi
  * resources_total: 4.0 CPU, 32.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 32.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793820455
* mariadbcs-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:613073
  * datadisk:579
  * volume_size:30G
  * volume_used:740M
  * cpu_list:0-127
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:32Gi
  * limits_memory:32Gi
  * resources_total: 4.0 CPU, 32.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 32.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793820455
* mariadbcs-1-2-1-1-1 uses docker image mariadb:12.3.3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:614197
  * datadisk:579
  * volume_size:30G
  * volume_used:740M
  * cpu_list:0-127
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:32Gi
  * limits_memory:32Gi
  * resources_total: 4.0 CPU, 32.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 32.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793820455

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MariaDB-1-2, MariaDBCS-1-2

### Data Parameters of Reused Volumes
* MariaDB-1: DDL values of the volume: histograms=off
* MariaDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics
* MariaDBCS-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1793820455-9fdf78fc5-p5wp8: 0
* bexhoma-sut-mariadb-1-1793820455-6bbc8867c8-srcbx: 0
* bexhoma-sut-mariadbcs-1-1793820455-5796fb4c9f-sbrdm: 0
* bexhoma-sut-mariadbcs-1-1793820455-854dff5c45-7tjdl: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: tpcds (1 pods)
* DBMS MariaDBCS-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MariaDBCS-1 - Experiment 2 Client 1: tpcds (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: tpcds (1 pods)
* DBMS MariaDBCS-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MariaDBCS-1 - Experiment 2 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|               |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:--------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1   |                1 |    1 |      268.00 |           3.00 |            0.00 |        132.00 |          132.00 |              1 |           0 |             | None           |             0 | False         |               13.43 | False               |
| MariaDB-1-2   |                2 |    1 |      268.00 |           3.00 |            0.00 |        132.00 |          132.00 |              1 |           0 |             | None           |             0 | False         |               13.43 | True                |
| MariaDBCS-1-1 |                1 |    1 |      188.00 |          19.00 |            0.00 |        128.00 |           33.00 |              1 |           0 |             | None           |             0 | False         |               19.15 | False               |
| MariaDBCS-1-2 |                2 |    1 |      188.00 |          19.00 |            0.00 |        128.00 |           33.00 |              1 |           0 |             | None           |             0 | False         |               19.15 | True                |

### Benchmarking

#### Per Connection

| DBMS                | configuration   | phase           | job               |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                 |
|:--------------------|:----------------|:----------------|:------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:--------------------|
| mariadb-1-1-1-1-1   | MariaDB-1       | mariadb-1-1-1   | mariadb-1-1-1-1   |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        357 |            0.78 |             4681.10 |            998.32 |          -1 | mariadb-1-1-1-1-1   |
| mariadb-1-2-1-1-1   | MariaDB-1       | mariadb-1-2-1   | mariadb-1-2-1-1   |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        322 |            0.70 |             5208.43 |           1106.83 |          -1 | mariadb-1-2-1-1-1   |
| mariadbcs-1-1-1-1-1 | MariaDBCS-1     | mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        136 |            0.97 |             3726.42 |           2620.59 |          -1 | mariadbcs-1-1-1-1-1 |
| mariadbcs-1-2-1-1-1 | MariaDBCS-1     | mariadbcs-1-2-1 | mariadbcs-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        124 |            0.84 |             4317.79 |           2874.19 |          -1 | mariadbcs-1-2-1-1-1 |

#### Per Phase

|                 | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1   | mariadb-1-1-1   |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        357 |            0.78 |             4681.10 |            998.32 |          -1 |
| mariadb-1-2-1   | mariadb-1-2-1   |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        322 |            0.70 |             5208.43 |           1106.83 |          -1 |
| mariadbcs-1-1-1 | mariadbcs-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        136 |            0.97 |             3726.42 |           2620.59 |          -1 |
| mariadbcs-1-2-1 | mariadbcs-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        124 |            0.84 |             4317.79 |           2874.19 |          -1 |

#### Query Completion per Phase

| phase           |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:----------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mariadb-1-1-1   |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| mariadb-1-2-1   |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| mariadbcs-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| mariadbcs-1-2-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

#### Reset

| phase           | job               |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:----------------|:------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| mariadb-1-1-1   | mariadb-1-1-1-1   |                1 |        1 |               1 |         4.00 |                |
| mariadb-1-2-1   | mariadb-1-2-1-1   |                2 |        1 |               1 |         4.00 |                |
| mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |        13.00 |                |
| mariadbcs-1-2-1 | mariadbcs-1-2-1-1 |                2 |        1 |               1 |        13.00 |                |

### Latency of Timer Execution [ms]
| Queries       |   mariadb-1-1-1-1-1 |   mariadb-1-2-1-1-1 |   mariadbcs-1-1-1-1-1 |   mariadbcs-1-2-1-1-1 |
|:--------------|--------------------:|--------------------:|----------------------:|----------------------:|
| TPC-DS Q1     |               11.94 |              188.99 |               1813.62 |               1897.57 |
| TPC-DS Q2     |             4862.01 |             5348.51 |               4420.18 |               4295.18 |
| TPC-DS Q3     |                7.12 |               12.42 |               1185.00 |               1105.28 |
| TPC-DS Q4     |             9041.50 |             9483.16 |               2154.44 |               1462.74 |
| TPC-DS Q5     |             6920.39 |             7031.27 |               5307.79 |               4350.17 |
| TPC-DS Q6     |              853.34 |              586.57 |               1205.89 |                974.64 |
| TPC-DS Q7     |             2744.20 |             9542.42 |               1710.79 |               1406.01 |
| TPC-DS Q8     |              306.14 |              296.22 |                832.35 |                705.44 |
| TPC-DS Q9     |             3483.26 |             3380.84 |                498.58 |                400.88 |
| TPC-DS Q10    |               44.85 |               64.97 |                948.60 |                813.11 |
| TPC-DS Q11    |             6102.81 |             6146.52 |               1162.05 |                911.74 |
| TPC-DS Q12    |              189.30 |              195.33 |                687.51 |                573.91 |
| TPC-DS Q13    |              842.82 |              836.48 |               1609.24 |               1463.87 |
| TPC-DS Q14a+b |            44086.14 |            42052.22 |               6842.62 |               5901.67 |
| TPC-DS Q15    |              115.50 |              116.70 |                793.93 |                654.16 |
| TPC-DS Q16    |             8363.18 |             8232.55 |                945.06 |                781.23 |
| TPC-DS Q17    |             1162.12 |              528.43 |               1414.63 |               1167.76 |
| TPC-DS Q18    |             2674.80 |             1495.64 |               1733.62 |               1070.89 |
| TPC-DS Q19    |              186.97 |              188.15 |               1001.85 |                727.88 |
| TPC-DS Q20    |              359.46 |              351.63 |                630.55 |                488.53 |
| TPC-DS Q21    |              876.21 |             3790.03 |               1482.28 |               1199.23 |
| TPC-DS Q22    |            13588.25 |             8552.66 |               1769.53 |               1467.53 |
| TPC-DS Q23a+b |            51020.05 |            51614.56 |               3451.83 |               3181.17 |
| TPC-DS Q24a+b |               28.96 |               22.53 |               4482.60 |               5146.02 |
| TPC-DS Q25    |              132.30 |              120.51 |               1252.99 |               1014.68 |
| TPC-DS Q26    |              691.66 |              730.41 |                841.76 |                728.00 |
| TPC-DS Q27    |             2870.27 |             2594.16 |                939.61 |                848.13 |
| TPC-DS Q28    |             2849.70 |             2734.24 |                386.25 |                411.70 |
| TPC-DS Q29    |               87.49 |               77.37 |               1247.30 |               1301.19 |
| TPC-DS Q30    |               30.92 |               34.12 |                866.05 |                846.65 |
| TPC-DS Q31    |             1153.30 |             1048.50 |                841.43 |                859.84 |
| TPC-DS Q32    |                3.89 |                3.20 |                293.02 |                284.98 |
| TPC-DS Q33    |              146.69 |              152.86 |                686.92 |                742.03 |
| TPC-DS Q34    |             2465.21 |             2533.34 |                219.88 |                262.06 |
| TPC-DS Q35    |              944.88 |              948.69 |                831.51 |                820.74 |
| TPC-DS Q36    |             2258.71 |             2203.08 |                642.32 |                655.68 |
| TPC-DS Q37    |             3088.52 |             3109.38 |                385.54 |                388.55 |
| TPC-DS Q38    |             5826.96 |             5474.35 |                794.45 |                714.78 |
| TPC-DS Q39a+b |             1014.09 |              997.35 |               1779.67 |               1786.01 |
| TPC-DS Q40    |              221.23 |              137.15 |                769.21 |                748.91 |
| TPC-DS Q41    |              357.90 |              338.86 |                448.26 |                359.93 |
| TPC-DS Q42    |              189.33 |              179.76 |                367.48 |                380.75 |
| TPC-DS Q43    |              937.63 |              862.68 |                409.70 |                299.79 |
| TPC-DS Q44    |                1.60 |                1.17 |                365.08 |                196.25 |
| TPC-DS Q45    |              116.67 |              100.53 |                581.93 |                465.48 |
| TPC-DS Q46    |             3320.44 |             2829.17 |                405.44 |                312.80 |
| TPC-DS Q47    |            15345.93 |            13073.77 |               1601.87 |               1352.04 |
| TPC-DS Q48    |             1164.88 |              915.71 |               1210.66 |               1107.02 |
| TPC-DS Q49    |              102.86 |               98.98 |                793.05 |                542.39 |
| TPC-DS Q50    |               22.13 |               19.97 |                790.96 |                678.69 |
| TPC-DS Q51    |             7360.81 |             6240.52 |               3494.53 |               2981.28 |
| TPC-DS Q52    |              253.67 |              197.25 |                523.16 |                424.19 |
| TPC-DS Q53    |              143.87 |              121.57 |                701.65 |                586.63 |
| TPC-DS Q54    |             1006.73 |              871.38 |                755.14 |                597.31 |
| TPC-DS Q55    |              204.33 |              172.26 |                413.05 |                414.26 |
| TPC-DS Q56    |              331.12 |              257.12 |                949.53 |                856.30 |
| TPC-DS Q57    |             6381.10 |             5293.93 |               1223.35 |               1150.62 |
| TPC-DS Q58    |             7747.64 |             4473.01 |                718.13 |                593.02 |
| TPC-DS Q59    |             8518.77 |             7055.56 |               1440.12 |               1271.93 |
| TPC-DS Q60    |              372.33 |              294.59 |               1111.50 |                821.64 |
| TPC-DS Q61    |              358.50 |              274.32 |                367.67 |                242.84 |
| TPC-DS Q62    |             1535.87 |             1335.88 |               1212.92 |                888.84 |
| TPC-DS Q63    |              185.33 |              118.29 |                603.78 |                544.83 |
| TPC-DS Q64    |              489.43 |              434.96 |               4010.56 |               3337.16 |
| TPC-DS Q65    |             5294.92 |             4573.20 |                651.42 |                559.23 |
| TPC-DS Q66    |             1003.58 |              912.91 |               1565.93 |               1235.97 |
| TPC-DS Q67    |             5886.39 |             5249.99 |               4688.98 |               4031.68 |
| TPC-DS Q68    |             2573.42 |             2444.88 |                390.34 |                365.04 |
| TPC-DS Q69    |              391.18 |              297.50 |               1097.90 |                835.84 |
| TPC-DS Q70    |             7371.71 |             6214.07 |               1365.36 |               1138.13 |
| TPC-DS Q71    |              689.22 |              389.79 |                712.23 |                605.22 |
| TPC-DS Q72    |             1243.01 |              641.08 |               1787.93 |               1425.05 |
| TPC-DS Q73    |             3936.79 |             2285.60 |                300.45 |                213.31 |
| TPC-DS Q74    |             7720.94 |             4635.00 |               1060.18 |                753.70 |
| TPC-DS Q75    |             6921.24 |             4222.33 |               1344.43 |               1384.81 |
| TPC-DS Q76    |              752.96 |              363.08 |                822.96 |                599.28 |
| TPC-DS Q77    |             9539.58 |             4873.79 |               1170.37 |               1161.33 |
| TPC-DS Q78    |             6625.87 |             4473.00 |               1871.59 |               1685.79 |
| TPC-DS Q79    |             3580.72 |             2739.29 |                917.00 |               1131.59 |
| TPC-DS Q80    |              434.97 |              421.86 |               1431.34 |               1487.49 |
| TPC-DS Q81    |              169.09 |              152.76 |                905.99 |                944.42 |
| TPC-DS Q82    |             4190.50 |             3194.28 |                872.65 |                827.77 |
| TPC-DS Q83    |              756.82 |              775.22 |                877.08 |                908.91 |
| TPC-DS Q84    |               38.90 |               39.59 |                719.84 |                748.24 |
| TPC-DS Q85    |              136.26 |              129.24 |               2889.39 |               2748.12 |
| TPC-DS Q86    |              656.80 |              666.07 |                628.04 |                488.75 |
| TPC-DS Q87    |             5652.67 |             5574.04 |               1033.29 |                889.05 |
| TPC-DS Q88    |            17805.64 |             7320.45 |               1406.33 |                795.14 |
| TPC-DS Q89    |             1164.69 |             1091.34 |                296.96 |                269.29 |
| TPC-DS Q90    |              112.14 |               88.12 |                481.21 |                362.69 |
| TPC-DS Q91    |               18.83 |               11.93 |                968.37 |                824.69 |
| TPC-DS Q92    |                4.90 |                5.09 |                536.90 |                457.71 |
| TPC-DS Q93    |               67.31 |               60.67 |                564.33 |                476.53 |
| TPC-DS Q94    |              393.67 |              377.54 |                923.16 |                760.81 |
| TPC-DS Q95    |              614.67 |              596.15 |               1057.41 |                838.62 |
| TPC-DS Q96    |             1978.26 |              685.95 |                524.58 |                412.91 |
| TPC-DS Q97    |             4273.66 |             4354.91 |                889.50 |                833.45 |
| TPC-DS Q98    |              700.19 |              691.98 |                716.33 |                594.80 |
| TPC-DS Q99    |             2638.00 |             2659.91 |                979.63 |                871.13 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   |       286.87 |      1.25 |           3.88 |                  3.97 |
| mariadbcs-1-1-1-1 |       249.02 |      1.92 |           5.46 |                  6.23 |

### Loading phase: component data generator

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   | n/a          |      0.00 |           0.00 |                  0.00 |
| mariadbcs-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   |         2.31 |      0.03 |           0.00 |                  0.00 |
| mariadbcs-1-1-1-1 |         3.35 |      0.04 |           0.01 |                  1.01 |

### Benchmarking phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   |       327.60 |      1.00 |           4.24 |                  4.26 |
| mariadb-1-2-1-1   |       271.84 |      1.00 |           3.61 |                  3.61 |
| mariadbcs-1-1-1-1 |       821.65 |      9.17 |          11.14 |                 11.91 |
| mariadbcs-1-2-1-1 |       790.18 |     11.10 |          10.31 |                 10.50 |

### Benchmarking phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   |        20.23 |      0.04 |           0.32 |                  0.32 |
| mariadb-1-2-1-1   |        19.70 |      0.47 |           0.31 |                  0.32 |
| mariadbcs-1-1-1-1 |        19.40 |      0.07 |           0.31 |                  0.31 |
| mariadbcs-1-2-1-1 |        19.51 |      0.39 |           0.28 |                  0.29 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-2-1-1 (bexhoma-metrics-mariadb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-2-1-1 (bexhoma-metrics-mariadb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)

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
* TEST passed: Reset scripts ran without errors
```

</details>


## SSB

For performing the experiment we can run the [ssb file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/ssb.py).

```bash
bexhoma ssb \
  -dbms MariaDBCS \
  -sf 1 \
  -xis \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 16Gi \
  -rr 16Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 20Gi \
  -rsr \
  -nc 2 \
  -ar \
  -ks no \
  run &>$LOG_DIR/docs_ssb_mariadbcs.log
```

This runs the 13 queries of the star schema benchmark, see [Example: SSB](Example-SSB.md).

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ssb_mariadbcs_summary.md" target="_blank" rel="noopener">docs_ssb_mariadbcs.log</a></summary>

```markdown
## Show Summary

### Workload
SSB Queries SF=1
* Type: ssb
* Duration: 539s 
* Code: 1794822683
* This includes the 13 queries of the Star Schema Benchmark (O'Neil et al., revision 3, 2009) with the constants of the specification (Q2.3: brand 'MFGR#2239', as used by ClickHouse and Doris; the specification's text and SQL disagree there).
* This experiment compares run time and resource consumption of SSB queries in different DBMS.
  * Schema is the star schema (-xsv normal).
  * SSB (SF=1) data is loaded and benchmark is executed.
  * Queries use the constants of the specification (-xqv spec).
  * Query ordering is Q1.1 - Q4.3.
  * Timeout per query is 1800. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Import sets statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MariaDBCS'].
  * Import is handled by 1 processes (pods).
  * Database is persisted to disk of type nvme and size 20Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM. RAM limit is 16Gi.

### Connections
* mariadbcs-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:1077381263360
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-137-generic
  * node:cl-worker27
  * disk:906137
  * datadisk:298
  * volume_size:20G
  * volume_used:459M
  * cpu_list:0-255
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794822683
* mariadbcs-1-2-1-1-1 uses docker image mariadb:12.3.3
  * RAM:1081742753792
  * CPU:AMD EPYC 7502 32-Core Processor
  * Cores:128
  * host:6.8.0-146-generic
  * node:cl-worker29
  * disk:1390286
  * datadisk:298
  * volume_size:20G
  * volume_used:459M
  * cpu_list:0-127
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794822683

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MariaDBCS-1-2

### Data Parameters of Reused Volumes
* MariaDBCS-1: loading values of the volume: script=Schema, indexing=Statistics

### Ingestion
* MariaDBCS-1: 5 of 5 units ok

### SUT Container Restarts
* bexhoma-sut-mariadbcs-1-1794822683-6b87fd794-gvxpn: 0
* bexhoma-sut-mariadbcs-1-1794822683-66769bc89b-m5tdj: 0

### Workflow

#### Actual

* DBMS MariaDBCS-1 - Experiment 1 Client 1: ssb (1 pods)
* DBMS MariaDBCS-1 - Experiment 2 Client 1: ssb (1 pods)

#### Planned

* DBMS MariaDBCS-1 - Experiment 1 Client 1: ssb (1 pods)
* DBMS MariaDBCS-1 - Experiment 2 Client 1: ssb (1 pods)

### Loading

#### Per Run

| DBMS          |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:--------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDBCS-1-1 |                1 |    1 |       72.00 |           6.00 |            0.00 |         48.00 |           12.00 |              1 |         0 |             | None           |             0 | False         |               50.00 | False               |
| MariaDBCS-1-2 |                2 |    1 |       72.00 |           6.00 |            0.00 |         48.00 |           12.00 |              1 |         0 |             | None           |             0 | False         |               50.00 | True                |

### Benchmarking

#### Per Connection

| connection          | phase           | job               |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadbcs-1-1-1-1-1 | mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               13 |                  13 |         14 |            0.80 |             4508.99 |           3342.86 |          -1 |
| mariadbcs-1-2-1-1-1 | mariadbcs-1-2-1 | mariadbcs-1-2-1-1 |                2 |        1 |               1 |       1 | 1.00 |               13 |                  13 |          9 |            0.56 |             6393.14 |           5200.00 |          -1 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadbcs-1-1-1 | mariadbcs-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |         14 |            0.80 |             4508.99 |           3342.86 |          -1 |
| mariadbcs-1-2-1 | mariadbcs-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          9 |            0.56 |             6393.14 |           5200.00 |          -1 |

#### Query Completion per Phase

| phase           |   pods | Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)   | Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)   | Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)   | Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)   | Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)   | Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)   | Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)   | Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)   | Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)   | Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)   | Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1)   | Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)   | Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)   | complete   |
|:----------------|-------:|:-------------------------------------------------------------------------|:--------------------------------------------------------------------------|:-------------------------------------------------------------------------|:----------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|:---------------------------------------------------------------------|:------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|:---------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------|:------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------|
| mariadbcs-1-1-1 |      1 | 1/1                                                                      | 1/1                                                                       | 1/1                                                                      | 1/1                                                                                     | 1/1                                                                                | 1/1                                                                  | 1/1                                                                                 | 1/1                                                                               | 1/1                                                                              | 1/1                                                                                  | 1/1                                                                                      | 1/1                                                                           | 1/1                                                                                  | yes        |
| mariadbcs-1-2-1 |      1 | 1/1                                                                      | 1/1                                                                       | 1/1                                                                      | 1/1                                                                                     | 1/1                                                                                | 1/1                                                                  | 1/1                                                                                 | 1/1                                                                               | 1/1                                                                              | 1/1                                                                                  | 1/1                                                                                      | 1/1                                                                           | 1/1                                                                                  | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

#### Reset

| phase           | job               |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:----------------|:------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |         4.00 |                |
| mariadbcs-1-2-1 | mariadbcs-1-2-1-1 |                2 |        1 |               1 |         4.00 |                |

### Latency of Timer Execution [ms]
| Queries                                                                                |   mariadbcs-1-1-1-1-1 |   mariadbcs-1-2-1-1-1 |
|:---------------------------------------------------------------------------------------|----------------------:|----------------------:|
| Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)                 |               1481.19 |               1065.62 |
| Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)                |                212.45 |                167.55 |
| Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)                 |                250.02 |                206.98 |
| Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)  |               1726.05 |               1342.26 |
| Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)       |               1103.21 |                673.43 |
| Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)                     |                773.51 |                510.95 |
| Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)      |               1260.77 |                953.49 |
| Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)        |                816.55 |                568.86 |
| Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)         |                728.60 |                483.93 |
| Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)     |                733.30 |                505.69 |
| Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1) |                923.16 |                650.50 |
| Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)            |                918.51 |                658.14 |
| Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)     |                991.12 |                590.05 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadbcs-1-1-1-1 |        72.81 |      1.24 |           4.69 |                  5.18 |

### Loading phase: component data generator

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadbcs-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadbcs-1-1-1-1 |         1.85 |      0.06 |           0.01 |                  0.56 |

### Benchmarking phase: SUT deployment

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadbcs-1-1-1-1 | n/a          |      0.25 |           4.65 |                  5.14 |
| mariadbcs-1-2-1-1 | n/a          |      1.29 |           0.26 |                  0.45 |

### Benchmarking phase: component benchmarker

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadbcs-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| mariadbcs-1-2-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |

### Missing Monitoring Metrics
* CPU Utilization [CPUs] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage incl. Page Cache [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)

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
* TEST skipped: Benchmarking phase: SUT deployment contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Benchmarking phase: component benchmarker contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Monitoring metrics missing (data pre-existing; phase shorter than scrape interval; series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
* TEST passed: Reset scripts ran without errors
```

</details>

### Flat Schema

With `-xsv flat` there is one denormalized table `lineorder_flat`, which suits a columnar engine.

```bash
bexhoma ssb \
  -dbms MariaDBCS \
  -sf 1 \
  -xsv flat \
  -xis \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 16Gi \
  -rr 16Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 20Gi \
  -rsr \
  -nc 2 \
  -ar \
  -ks no \
  run &>$LOG_DIR/docs_ssb_mariadbcs_flat.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ssb_mariadbcs_flat_summary.md" target="_blank" rel="noopener">docs_ssb_mariadbcs_flat.log</a></summary>

```markdown
## Show Summary

### Workload
SSB Queries SF=1
* Type: ssb
* Duration: 623s 
* Code: 1794823279
* This includes the 13 queries of the Star Schema Benchmark (O'Neil et al., revision 3, 2009) with the constants of the specification (Q2.3: brand 'MFGR#2239', as used by ClickHouse and Doris; the specification's text and SQL disagree there). The queries read the denormalized table lineorder_flat; year, month and week come from lo_orderdate.
* This experiment compares run time and resource consumption of SSB queries in different DBMS.
  * Schema is the flat table lineorder_flat (-xsv flat).
  * SSB (SF=1) data is loaded and benchmark is executed.
  * Queries use the constants of the specification (-xqv spec).
  * Query ordering is Q1.1 - Q4.3.
  * Timeout per query is 1800. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Import sets statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MariaDBCS'].
  * Import is handled by 1 processes (pods).
  * Database is persisted to disk of type nvme and size 20Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM. RAM limit is 16Gi.

### Connections
* mariadbcs-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:1077381263360
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-137-generic
  * node:cl-worker27
  * disk:906316
  * datadisk:798
  * volume_size:20G
  * volume_used:959M
  * cpu_list:0-255
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794823279
* mariadbcs-1-2-1-1-1 uses docker image mariadb:12.3.3
  * RAM:1077381263360
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-137-generic
  * node:cl-worker27
  * disk:906315
  * datadisk:798
  * volume_size:20G
  * volume_used:959M
  * cpu_list:0-255
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794823279

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MariaDBCS-1-2

### Data Parameters of Reused Volumes
* MariaDBCS-1: loading values of the volume: script=Schema_flat, indexing=Statistics_flat

### Ingestion
* MariaDBCS-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-mariadbcs-1-1794823279-564fbbfbf8-65jbm: 0
* bexhoma-sut-mariadbcs-1-1794823279-77cf7774b4-ngq8c: 0

### Workflow

#### Actual

* DBMS MariaDBCS-1 - Experiment 1 Client 1: ssb (1 pods)
* DBMS MariaDBCS-1 - Experiment 2 Client 1: ssb (1 pods)

#### Planned

* DBMS MariaDBCS-1 - Experiment 1 Client 1: ssb (1 pods)
* DBMS MariaDBCS-1 - Experiment 2 Client 1: ssb (1 pods)

### Loading

#### Per Run

| DBMS          |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:--------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDBCS-1-1 |                1 |    1 |      118.00 |           4.00 |            0.00 |        105.00 |            8.00 |              1 |         0 |             | None           |             0 | False         |               30.51 | False               |
| MariaDBCS-1-2 |                2 |    1 |      118.00 |           4.00 |            0.00 |        105.00 |            8.00 |              1 |         0 |             | None           |             0 | False         |               30.51 | True                |

### Benchmarking

#### Per Connection

| connection          | phase           | job               |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadbcs-1-1-1-1-1 | mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               13 |                  13 |          8 |            0.30 |            12065.51 |           5850.00 |          -1 |
| mariadbcs-1-2-1-1-1 | mariadbcs-1-2-1 | mariadbcs-1-2-1-1 |                2 |        1 |               1 |       1 | 1.00 |               13 |                  13 |         10 |            0.31 |            11697.67 |           4680.00 |          -1 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadbcs-1-1-1 | mariadbcs-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          8 |            0.30 |            12065.51 |           5850.00 |          -1 |
| mariadbcs-1-2-1 | mariadbcs-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               13 |                  13 |         10 |            0.31 |            11697.67 |           4680.00 |          -1 |

#### Query Completion per Phase

| phase           |   pods | Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)   | Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)   | Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)   | Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)   | Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)   | Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)   | Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)   | Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)   | Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)   | Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)   | Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1)   | Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)   | Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)   | complete   |
|:----------------|-------:|:-------------------------------------------------------------------------|:--------------------------------------------------------------------------|:-------------------------------------------------------------------------|:----------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|:---------------------------------------------------------------------|:------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|:---------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------|:------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------|
| mariadbcs-1-1-1 |      1 | 1/1                                                                      | 1/1                                                                       | 1/1                                                                      | 1/1                                                                                     | 1/1                                                                                | 1/1                                                                  | 1/1                                                                                 | 1/1                                                                               | 1/1                                                                              | 1/1                                                                                  | 1/1                                                                                      | 1/1                                                                           | 1/1                                                                                  | yes        |
| mariadbcs-1-2-1 |      1 | 1/1                                                                      | 1/1                                                                       | 1/1                                                                      | 1/1                                                                                     | 1/1                                                                                | 1/1                                                                  | 1/1                                                                                 | 1/1                                                                               | 1/1                                                                              | 1/1                                                                                  | 1/1                                                                                      | 1/1                                                                           | 1/1                                                                                  | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

#### Reset

| phase           | job               |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:----------------|:------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |         2.00 |                |
| mariadbcs-1-2-1 | mariadbcs-1-2-1-1 |                2 |        1 |               1 |         2.00 |                |

### Latency of Timer Execution [ms]
| Queries                                                                                |   mariadbcs-1-1-1-1-1 |   mariadbcs-1-2-1-1-1 |
|:---------------------------------------------------------------------------------------|----------------------:|----------------------:|
| Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)                 |                866.53 |                845.45 |
| Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)                |                 24.03 |                 33.06 |
| Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)                 |                 20.91 |                 18.99 |
| Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)  |                634.02 |                669.85 |
| Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)       |                664.76 |                648.76 |
| Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)                     |                499.78 |                549.22 |
| Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)      |                721.28 |                751.42 |
| Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)        |                701.63 |                598.65 |
| Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)         |                210.15 |                214.55 |
| Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)     |                 77.56 |                 80.49 |
| Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1) |                631.56 |                726.73 |
| Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)            |                472.95 |                498.74 |
| Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)     |                657.41 |                623.07 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadbcs-1-1-1-1 |       154.23 |      1.79 |           2.24 |                  2.96 |

### Loading phase: component data generator

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadbcs-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadbcs-1-1-1-1 |         5.01 |      0.07 |           0.01 |                  1.95 |

### Benchmarking phase: SUT deployment

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadbcs-1-1-1-1 | n/a          |      0.24 |           3.89 |                  4.87 |
| mariadbcs-1-2-1-1 | n/a          |      1.42 |           1.63 |                  1.82 |

### Benchmarking phase: component benchmarker

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadbcs-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| mariadbcs-1-2-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |

### Missing Monitoring Metrics
* Memory Usage, Working Set [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Utilization [CPUs] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Memory Usage incl. Page Cache [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU System Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU User Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Utilization Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Network Tx Total [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Network Rx Total [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Memory Usage incl. Page Cache [MiB] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttled Time [s] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization Time [s] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU User Time [s] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU System Time [s] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* Network Tx Total [MiB] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Network Rx Total [MiB] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)

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
* TEST skipped: Benchmarking phase: SUT deployment contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Benchmarking phase: component benchmarker contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Monitoring metrics missing (data pre-existing; phase shorter than scrape interval; series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
* TEST passed: Reset scripts ran without errors
```

</details>
