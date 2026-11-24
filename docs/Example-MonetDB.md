# Example: Benchmark MonetDB

This example shows how to benchmark MonetDB with TPC-H and TPC-DS on a single node, at small and large scaling factors.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

[MonetDB](https://www.monetdb.org/) is a column-store DBMS for analytical workloads.
Bexhoma runs it on a single node for TPC-H, TPC-DS and SSB.
MonetDB is not available for YCSB, Benchbase and HammerDB.

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. [MonetDB](https://www.monetdb.org/)
1. [TPC-H](https://www.tpc.org/tpch/)
1. [TPC-DS](https://www.tpc.org/tpcds/)
1. [Orchestrating DBMS Benchmarking in the Cloud with Kubernetes](https://doi.org/10.1007/978-3-030-94437-7_6)
1. [A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools](https://doi.org/10.1007/978-3-031-68031-1_9)
1. Test script of this page: [test-docs-monetdb.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-monetdb.sh), [test-docs-monetdb.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-monetdb.ps1)


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

The experiment is run with the [tpch file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpch.py).

Example:
```bash
bexhoma tpch \
  -dbms MonetDB \
  -sf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -lc 16 \
  -lr 64Gi \
  -rc 16 \
  -rr 64Gi \
  -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_monetdb.log
```

This
* starts a clean instance of MonetDB (`-dbms`) with 16 CPUs and 64 GiB RAM (`-rc`, `-lc`, `-rr`, `-lr`)
  * data directory inside a Docker container
* creates the TPC-H schema
* starts 8 loader pods (`-nlp`); `-nlt 8` is ignored: the TPC-H loader uses one connection per pod, and bexhoma says so in the log
  * with a data generator (init container) each, which generates a share of TPC-H data of SF=1 (`-sf`)
  * and a loading container each, which loads the data into the DBMS
* creates indexes (`-xii`), constraints (`-xic`) and statistics (`-xis`)
* runs 1 stream of the 22 TPC-H queries (`-ne`) with a timeout of 1200 s per query (`-t`), measuring the data transfer volume per query (`-xdt`)
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
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_monetdb_summary.md" target="_blank" rel="noopener">docs_tpch_monetdb.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 339s 
* Code: 1794658880
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
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * SUT requests 16 CPU and 64Gi RAM. CPU limit is 16. RAM limit is 64Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:575856
  * datadisk:2937
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794658880

### Ingestion
* MonetDB-1: 50 of 50 units ok

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1794658880-f598f57-484w2: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |    1 |       67.00 |           3.00 |           24.00 |         21.00 |           15.00 |              8 |         0 |             | None           |             0 | False         |               53.73 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         11 |            0.14 |            29330.44 |           7200.00 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         11 |            0.14 |            29330.44 |           7200.00 |          -1 |

#### Query Completion per Phase

| phase         |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:--------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   monetdb-1-1-1-1-1 |
|:----------------------------------------------------|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |              960.56 |
| Minimum Cost Supplier Query (TPC-H Q2)              |               41.18 |
| Shipping Priority (TPC-H Q3)                        |              136.21 |
| Order Priority Checking Query (TPC-H Q4)            |              173.37 |
| Local Supplier Volume (TPC-H Q5)                    |              134.05 |
| Forecasting Revenue Change (TPC-H Q6)               |               41.61 |
| Volume Shipping Query (TPC-H Q7)                    |              109.38 |
| National Market Share (TPC-H Q8)                    |              241.45 |
| Product Type Profit Measure (TPC-H Q9)              |              119.02 |
| Returned Item Reporting Query (TPC-H Q10)           |              149.70 |
| Important Stock Identification (TPC-H Q11)          |               25.51 |
| Shipping Modes and Order Priority (TPC-H Q12)       |               73.22 |
| Customer Distribution (TPC-H Q13)                   |              376.71 |
| Promotion Effect Query (TPC-H Q14)                  |               55.01 |
| Top Supplier Query (TPC-H Q15)                      |               55.12 |
| Parts/Supplier Relationship (TPC-H Q16)             |              120.78 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               82.41 |
| Large Volume Customer (TPC-H Q18)                   |              209.00 |
| Discounted Revenue (TPC-H Q19)                      |              120.94 |
| Potential Part Promotion (TPC-H Q20)                |               51.64 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |             1903.59 |
| Global Sales Opportunity Query (TPC-H Q22)          |               70.09 |

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

[Monitoring](Monitoring.md) can be activated for DBMS only (`-m`) or for all components (`-mc`).
Metrics are sampled every few seconds, so the benchmarking phase should take at least a minute.
This run uses SF=30 (`-sf`), with 256 GiB RAM.
There are no application metrics for MonetDB.

```bash
bexhoma tpch \
  -dbms MonetDB \
  -sf 30 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 3600 \
  -lc 16 \
  -lr 256Gi \
  -rc 16 \
  -rr 256Gi \
  -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_monetdb_monitoring.log
```

### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_monetdb_monitoring_summary.md" target="_blank" rel="noopener">docs_tpch_monetdb_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=30
* Type: tpch
* Duration: 1388s 
* Code: 1794659251
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=30) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 3600.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * SUT requests 16 CPU and 256Gi RAM. CPU limit is 16. RAM limit is 256Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:631796
  * datadisk:58896
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794659251

### Ingestion
* MonetDB-1: 50 of 50 units ok

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1794659251-5c64ff9474-49j5t: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |   30 |     1046.00 |           3.00 |           21.00 |        589.00 |          428.00 |              8 |         0 |             | None           |             0 | False         |              103.25 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 30.00 |               22 |                  22 |         97 |            2.12 |            54079.62 |          24494.85 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               22 |                  22 |         97 |            2.12 |            54079.62 |          24494.85 |          -1 |

#### Query Completion per Phase

| phase         |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:--------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   monetdb-1-1-1-1-1 |
|:----------------------------------------------------|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |            15703.19 |
| Minimum Cost Supplier Query (TPC-H Q2)              |              435.77 |
| Shipping Priority (TPC-H Q3)                        |             2356.65 |
| Order Priority Checking Query (TPC-H Q4)            |             3985.52 |
| Local Supplier Volume (TPC-H Q5)                    |             1744.71 |
| Forecasting Revenue Change (TPC-H Q6)               |             1366.32 |
| Volume Shipping Query (TPC-H Q7)                    |             2997.36 |
| National Market Share (TPC-H Q8)                    |             5919.72 |
| Product Type Profit Measure (TPC-H Q9)              |             2843.02 |
| Returned Item Reporting Query (TPC-H Q10)           |             2797.21 |
| Important Stock Identification (TPC-H Q11)          |              477.98 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             1215.99 |
| Customer Distribution (TPC-H Q13)                   |             8381.65 |
| Promotion Effect Query (TPC-H Q14)                  |              332.03 |
| Top Supplier Query (TPC-H Q15)                      |              785.57 |
| Parts/Supplier Relationship (TPC-H Q16)             |             1791.51 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |              908.42 |
| Large Volume Customer (TPC-H Q18)                   |             3570.92 |
| Discounted Revenue (TPC-H Q19)                      |              493.76 |
| Potential Part Promotion (TPC-H Q20)                |             1473.69 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            27964.70 |
| Global Sales Opportunity Query (TPC-H Q22)          |             1249.92 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      5140.06 |     11.62 |          57.94 |                 59.28 |

### Loading phase: component data generator

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |       545.89 |      1.58 |           0.01 |                  3.96 |

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |       325.13 |      6.34 |          63.64 |                 64.99 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        19.27 |      0.21 |           0.34 |                  0.35 |

### Missing Monitoring Metrics
* CPU Utilization [CPUs] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loader.log, expected: series exists only while non-zero)

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
With repetitions (`-nc`), `-rsr` removes an existing volume only before the first repetition and later repetitions reuse it without loading; `-rsrp` removes it before every repetition. See [Concepts](Concepts.md).

```bash
bexhoma tpch \
  -dbms MonetDB \
  -sf 1 \
  -nc 2 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -lc 16 \
  -lr 64Gi \
  -rc 16 \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_monetdb_storage.log
```

The experiment is repeated (`-nc 2`): the second repetition finds the data on the volume and does not load again.

### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_monetdb_storage_summary.md" target="_blank" rel="noopener">docs_tpch_monetdb_storage.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 566s 
* Code: 1794660700
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
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * SUT requests 16 CPU and 64Gi RAM. CPU limit is 16. RAM limit is 64Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:572896
  * datadisk:2937
  * volume_size:49G
  * volume_used:2.9G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794660700
* monetdb-1-2-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:572896
  * datadisk:1417
  * volume_size:49G
  * volume_used:1.4G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794660700

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MonetDB-1-2

### Data Parameters of Reused Volumes
* MonetDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### Ingestion
* MonetDB-1: 50 of 50 units ok

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1794660700-7c45799d99-d8zq7: 0
* bexhoma-sut-monetdb-1-1794660700-845dd57644-ns7cn: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 1: tpch (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 1: tpch (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |    1 |       71.00 |           5.00 |           24.00 |         22.00 |           16.00 |              8 |         0 |             | None           |             0 | False         |               50.70 | False               |
| MonetDB-1-2 |                2 |    1 |       71.00 |           5.00 |           24.00 |         22.00 |           16.00 |              8 |         0 |             | None           |             0 | False         |               50.70 | True                |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         13 |            0.15 |            26944.11 |           6092.31 |          -1 |
| monetdb-1-2-1-1-1 | monetdb-1-2-1 | monetdb-1-2-1-1 |                2 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         37 |            0.14 |            29723.08 |           2140.54 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         13 |            0.15 |            26944.11 |           6092.31 |          -1 |
| monetdb-1-2-1 | monetdb-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         37 |            0.14 |            29723.08 |           2140.54 |          -1 |

#### Query Completion per Phase

| phase         |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:--------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| monetdb-1-2-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   monetdb-1-1-1-1-1 |   monetdb-1-2-1-1-1 |
|:----------------------------------------------------|--------------------:|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |              962.63 |              949.42 |
| Minimum Cost Supplier Query (TPC-H Q2)              |               48.10 |               43.72 |
| Shipping Priority (TPC-H Q3)                        |              144.35 |              161.91 |
| Order Priority Checking Query (TPC-H Q4)            |              180.11 |              193.09 |
| Local Supplier Volume (TPC-H Q5)                    |              124.37 |              107.06 |
| Forecasting Revenue Change (TPC-H Q6)               |               43.45 |               29.81 |
| Volume Shipping Query (TPC-H Q7)                    |              111.51 |               80.56 |
| National Market Share (TPC-H Q8)                    |              387.69 |              334.12 |
| Product Type Profit Measure (TPC-H Q9)              |              121.23 |              110.51 |
| Returned Item Reporting Query (TPC-H Q10)           |              207.21 |              199.16 |
| Important Stock Identification (TPC-H Q11)          |               25.20 |               27.83 |
| Shipping Modes and Order Priority (TPC-H Q12)       |               88.30 |               73.53 |
| Customer Distribution (TPC-H Q13)                   |              374.90 |              372.22 |
| Promotion Effect Query (TPC-H Q14)                  |               55.77 |               39.54 |
| Top Supplier Query (TPC-H Q15)                      |               57.47 |               47.88 |
| Parts/Supplier Relationship (TPC-H Q16)             |              112.98 |              122.50 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               95.48 |               91.59 |
| Large Volume Customer (TPC-H Q18)                   |              289.23 |              220.85 |
| Discounted Revenue (TPC-H Q19)                      |              123.67 |               95.57 |
| Potential Part Promotion (TPC-H Q20)                |               49.93 |               72.56 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |             2583.29 |             1786.66 |
| Global Sales Opportunity Query (TPC-H Q22)          |               62.40 |               62.34 |

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


## Refresh Stream

`-xrs N` runs the TPC-H refresh functions RF1 (insert new orders) and RF2 (delete old orders) as an additional job next to the query streams, see [TPC-H](Example-TPC-H.md#refresh-stream).
For MonetDB, the loader image applies RF1 with `COPY ... FROM STDIN` in `mclient` and RF2 in one piped `mclient` session, so the temporary table lives across the statements.
Here, 3 query streams run in parallel with a refresh stream of 3 RF1+RF2 pairs.

```bash
bexhoma tpch \
  -dbms MonetDB \
  -sf 1 \
  -ne 3 \
  -xrs 3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -ms $BEXHOMA_MS \
  -tr \
  -lc 16 \
  -lr 64Gi \
  -rc 16 \
  -rr 64Gi \
  -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_monetdb_refresh.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_monetdb_refresh_summary.md" target="_blank" rel="noopener">docs_tpch_monetdb_refresh.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 319s 
* Code: 1794683398
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
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [3] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 16 CPU and 64Gi RAM. CPU limit is 16. RAM limit is 64Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081742753792
  * CPU:AMD EPYC 7502 32-Core Processor
  * Cores:128
  * host:6.8.0-146-generic
  * node:cl-worker29
  * disk:1384228
  * datadisk:2937
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794683398
* monetdb-1-1-1-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081742753792
  * CPU:AMD EPYC 7502 32-Core Processor
  * Cores:128
  * host:6.8.0-146-generic
  * node:cl-worker29
  * disk:1384228
  * datadisk:2937
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794683398
* monetdb-1-1-1-1-3 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081742753792
  * CPU:AMD EPYC 7502 32-Core Processor
  * Cores:128
  * host:6.8.0-146-generic
  * node:cl-worker29
  * disk:1384228
  * datadisk:2937
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794683398

### Ingestion
* MonetDB-1: 50 of 50 units ok

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1794683398-65cf8f89c-7q2lv: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |    1 |       61.00 |           3.00 |           18.00 |         15.00 |           20.00 |              8 |         0 |             | None           |             0 | False         |               59.02 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         11 |            0.11 |            33744.24 |           7200.00 |          -1 |
| monetdb-1-1-1-1-2 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       2 | 1.00 |               22 |                  22 |         11 |            0.11 |            34046.18 |           7200.00 |          -1 |
| monetdb-1-1-1-1-3 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       3 | 1.00 |               22 |                  22 |         11 |            0.10 |            35937.91 |           7200.00 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           3 | 1.00 |               66 |                  66 |         11 |            0.10 |            34562.64 |          21600.00 |          -1 |

#### Query Completion per Phase

| phase         |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:--------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| monetdb-1-1-1 |      3 | 3/3                                 | 3/3                                      | 3/3                            | 3/3                                        | 3/3                                | 3/3                                     | 3/3                                | 3/3                                | 3/3                                      | 3/3                                         | 3/3                                          | 3/3                                             | 3/3                                 | 3/3                                  | 3/3                              | 3/3                                       | 3/3                                        | 3/3                                 | 3/3                              | 3/3                                    | 3/3                                                   | 3/3                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### tpch_refresh

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count | benchmark_begin     | benchmark_end       |   benchmark_duration |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|:--------------------|:--------------------|---------------------:|
| monetdb-1-1-1-2-1 | monetdb-1-1-1 | monetdb-1-1-1-2 |                1 |        1 |               2 |           1 | 2026-11-14 20:14:39 | 2026-11-14 20:14:41 |                    2 |

### Latency of Timer Execution [ms]
| Queries                                             |   monetdb-1-1-1-1-1 |   monetdb-1-1-1-1-2 |   monetdb-1-1-1-1-3 |
|:----------------------------------------------------|--------------------:|--------------------:|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |             1455.87 |             1241.92 |             1318.81 |
| Minimum Cost Supplier Query (TPC-H Q2)              |               32.17 |               31.93 |               24.97 |
| Shipping Priority (TPC-H Q3)                        |               95.23 |               91.47 |              140.48 |
| Order Priority Checking Query (TPC-H Q4)            |              143.04 |              165.59 |              198.73 |
| Local Supplier Volume (TPC-H Q5)                    |               97.34 |               71.93 |               75.13 |
| Forecasting Revenue Change (TPC-H Q6)               |               25.58 |               24.63 |               25.28 |
| Volume Shipping Query (TPC-H Q7)                    |              133.47 |               70.98 |               70.32 |
| National Market Share (TPC-H Q8)                    |              194.06 |              194.69 |              314.34 |
| Product Type Profit Measure (TPC-H Q9)              |               83.00 |              147.62 |              109.96 |
| Returned Item Reporting Query (TPC-H Q10)           |              175.57 |              139.64 |              167.14 |
| Important Stock Identification (TPC-H Q11)          |               18.18 |               19.72 |               21.19 |
| Shipping Modes and Order Priority (TPC-H Q12)       |               54.28 |               47.90 |               50.28 |
| Customer Distribution (TPC-H Q13)                   |              403.71 |              340.12 |              352.92 |
| Promotion Effect Query (TPC-H Q14)                  |               32.84 |               37.84 |               34.76 |
| Top Supplier Query (TPC-H Q15)                      |               35.54 |               43.35 |               43.92 |
| Parts/Supplier Relationship (TPC-H Q16)             |               89.79 |               98.16 |              101.15 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               40.57 |               45.32 |               47.05 |
| Large Volume Customer (TPC-H Q18)                   |              567.51 |              147.88 |              166.15 |
| Discounted Revenue (TPC-H Q19)                      |              164.66 |               69.59 |               61.29 |
| Potential Part Promotion (TPC-H Q20)                |               65.44 |              250.20 |               35.51 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |             1479.59 |             1527.94 |             1505.55 |
| Global Sales Opportunity Query (TPC-H Q22)          |               45.19 |              122.10 |               98.45 |

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
'MonetDB': {
    'abbreviation': 'mo',
    'loadData': "cd /home/monetdb;printf 'user=monetdb\npassword=monetdb\n' > .monetdb;mclient demo < {scriptname}",
    'template': {
        'version': '11.37.11',
        'alias': 'Columnwise-A',
        'docker_alias': 'CW-A',
        'JDBC': {
            'auth': ['monetdb', 'monetdb'],
            'driver': 'org.monetdb.jdbc.MonetDriver',
            'jar': 'monetdb-jdbc-12.2.jre8.jar',
            'url': 'jdbc:monetdb://{serverip}:9091/demo?so_timeout={timeout_ms}',
            'database': 'demo',
            'explain': ['PLAN {query}'],
        }
    },
    'logfile': '/var/monetdb5/dbfarm/merovingian.log',
    'datadir': '/var/monetdb5/',
    'priceperhourdollar': 0.0,
},
```

where
* `abbreviation`: short name in the names of volumes
* `loadData`: first writes a `.monetdb` credentials file into the container home directory, then pipes the script to `mclient`
* `JDBC`: used to configure DBMSBenchmarker; `so_timeout` is set to the timeout of the queries (`-t`)

There is no `monitor` section: MonetDB has no application metrics.

### Deployment

* [deploymenttemplate-MonetDB.yml](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-MonetDB.yml): one SUT pod.

### Schema and Scripts

DDL scripts per benchmark:
- [TPC-H](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch/MonetDB)
- [TPC-DS](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpcds/MonetDB)
- [SSB](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ssb/MonetDB)

MonetDB sets primary keys and foreign key constraints after import and no other indexes.

### Load Durability

`-xld` has no effect on MonetDB: there are no durability scripts for it.

### Reset Scripts

With `-ar`, the reset runs before each benchmarking round:

1. Statistics: `ANALYZE`
2. Persist: n/a (the write-ahead log is applied in the background; no call to force it)
3. Counters: n/a

See [Reset scripts](DBMS.md#reset-scripts--ar) for the reset contract and [Test: Reset Scripts](Test-Reset.md) for the test runs, with results for [TPC-H](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_tpch_monetdb_summary.md), [TPC-DS](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_tpcds_monetdb_summary.md).


## TPC-H at SF 100

This example shows how to run Q1-Q22 derived from TPC-H in MonetDB at SF=100.
It covers the power and the throughput test.
The refresh stream is not included.

> The query file is derived from the TPC-H and as such is not comparable to published TPC-H results, as the query file results do not comply with the TPC-H Specification.

Official TPC-H benchmark - http://www.tpc.org/tpch




### Generate and Load Data

First, the script generates TPC-H data at SF=100 (`-sf`) with 8 parallel generators (`-nlp`).
The generated data is stored at the shared disk `data`.
Moreover the data is loaded into an instance of MonetDB using again 8 parallel loaders.
Afterwards the script creates contraints (`-xic`) and indexes (`-xii`) and updates table statistics (`-xis`).
The database is located in another shared disk of storageClass shared (`-rst`) and of size 1000Gi (`-rss`).

The script also runs a power test (`-ne` set to 1) with timeout 1200s (`-t`) and data transfer activated (`-xdt`) once (`-nc` set to 1).
To avoid conflicts with other experiments, it runs at most 1 DBMS at a time (`-ms`).
Monitoring is activated (`-m`) for all components (`-mc`).
The components, that is the SUT (`-rnn`) and the loader (`-rnl`) and the benchmark driver (`-rnb`), are fixed to specific nodes in the cluster.

```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"
BEXHOMA_MS=1
BEXHOMA_STORAGE_CLASS="shared"

mkdir -p $LOG_DIR

bexhoma tpch \
  -dbms MonetDB \
  -sf 100 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 3600 \
  -lc 16 \
  -lr 256Gi \
  -rc 16 \
  -rr 256Gi \
  -rsr \
  -rss 1000Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_monetdb_sf100.log
```

### Status Data Disk

You can watch the status of the data disk via `bexhoma data`.

The following example output shows TPC-H data at SF=100 from 8 generators.
The data set is split into 8 parts, each of about 14G size.
In total the data set has a size of 106G.

```bash
14G     /data/tpch/SF100/8/8
14G     /data/tpch/SF100/8/3
14G     /data/tpch/SF100/8/2
14G     /data/tpch/SF100/8/4
14G     /data/tpch/SF100/8/1
14G     /data/tpch/SF100/8/5
14G     /data/tpch/SF100/8/7
14G     /data/tpch/SF100/8/6
106G    /data/tpch/SF100/8
106G    /data/tpch/SF100
```

### Status Database and Benchmark

You can watch the status of experiments via `bexhoma status`.

The following example output shows all components of bexhoma up and running.
The cluster stores a MonetDB database corresponding to TPC-H of SF=100.
The disk is of storageClass shared and of size 1000Gi and 210G of that space is used.
No DBMS is running.

```bash
Dashboard: Running
Message Queue: Running
Data directory: Running
Result directory: Running
Cluster Prometheus: Running
+------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| Volumes                            | configuration   | experiment   | loaded [s]   |   timeLoading [s] | dbms       | storage_class_name   | storage   | status   | size   | used   |
+====================================+=================+==============+==============+===================+============+======================+===========+==========+========+========+
| bexhoma-storage-monetdb-tpch-100   | monetdb         | tpch-100     | True         |              7061 | MonetDB    | shared               | 300Gi     | Bound    | 300G   | 210G   |
+------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
```

### Summary of Results

At the end of a benchmark you will see a summary like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_monetdb_sf100_summary.md" target="_blank" rel="noopener">docs_tpch_monetdb_sf100.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=100
* Type: tpch
* Duration: 4554s 
* Code: 1794661304
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=100) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 3600.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * Database is persisted to disk of type nvme and size 1000Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * SUT requests 16 CPU and 256Gi RAM. CPU limit is 16. RAM limit is 256Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:571748
  * datadisk:193625
  * volume_size:984G
  * volume_used:190G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794661304

### Ingestion
* MonetDB-1: 50 of 50 units ok

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1794661304-59b54b5bd6-7smwq: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |  100 |     3963.00 |           5.00 |           22.00 |       1753.00 |         2179.00 |              8 |         0 |             | None           |             0 | False         |               90.84 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |     SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 100.00 |               22 |                  22 |        329 |            6.82 |            56067.45 |          24072.95 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               22 |                  22 |        329 |            6.82 |            56067.45 |          24072.95 |          -1 |

#### Query Completion per Phase

| phase         |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:--------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   monetdb-1-1-1-1-1 |
|:----------------------------------------------------|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |            84425.00 |
| Minimum Cost Supplier Query (TPC-H Q2)              |             1040.14 |
| Shipping Priority (TPC-H Q3)                        |            10542.14 |
| Order Priority Checking Query (TPC-H Q4)            |            12299.68 |
| Local Supplier Volume (TPC-H Q5)                    |             5367.06 |
| Forecasting Revenue Change (TPC-H Q6)               |             2070.95 |
| Volume Shipping Query (TPC-H Q7)                    |            11026.18 |
| National Market Share (TPC-H Q8)                    |            21669.41 |
| Product Type Profit Measure (TPC-H Q9)              |             8173.95 |
| Returned Item Reporting Query (TPC-H Q10)           |            10739.68 |
| Important Stock Identification (TPC-H Q11)          |             1008.57 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             2184.73 |
| Customer Distribution (TPC-H Q13)                   |            30426.44 |
| Promotion Effect Query (TPC-H Q14)                  |             1365.66 |
| Top Supplier Query (TPC-H Q15)                      |             3324.29 |
| Parts/Supplier Relationship (TPC-H Q16)             |             5905.87 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |             2849.38 |
| Large Volume Customer (TPC-H Q18)                   |            11297.59 |
| Discounted Revenue (TPC-H Q19)                      |             1769.41 |
| Potential Part Promotion (TPC-H Q20)                |             4717.74 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            74920.76 |
| Global Sales Opportunity Query (TPC-H Q22)          |             6087.67 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |     16003.52 |     13.65 |         189.80 |                189.81 |

### Loading phase: component data generator

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      1568.70 |      1.56 |           0.03 |                 13.29 |

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      1095.30 |      7.12 |         208.12 |                256.00 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        27.33 |      0.21 |           0.42 |                  0.43 |

### Missing Monitoring Metrics
* Memory Usage, Working Set [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loader.log, expected: series exists only while non-zero)

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

To see the summary again you can simply call `bexhoma summary -e 1708411664` with the experiment code.

### List local results

You can inspect a preview list of results via `bexhoma localresults`.

```bash
+------------+----------------------+------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+-------------+---------------------+
|   index    |         name         |                                                                                           info |                       intro                       | queries | connections |         time        |
+------------+----------------------+------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+-------------+---------------------+
| 1708411664 | TPC-H Queries SF=100 | This experiment compares run time and resource consumption of TPC-H queries in different DBMS. |    This includes the reading queries of TPC-H.    |    22   |      28     | 2024-02-20 11:37:30 |
|            |                      |                                TPC-H data is loaded from a filesystem using several processes. |                                                   |         |             |                     |
|            |                      |                                                             Import is limited to DBMS MonetDB. |                                                   |         |             |                     |
|            |                      |                                                              Import is handled by 1 processes. |                                                   |         |             |                     |
|            |                      |                                                               Loading is fixed to cl-worker19. |                                                   |         |             |                     |
|            |                      |                                                          Benchmarking is fixed to cl-worker19. |                                                   |         |             |                     |
+------------+----------------------+------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+-------------+---------------------+
```

### Perform Benchmark - Power Test

This starts a new instance of MonetDB on the prepared database of the shared disk.
It runs two power tests, one after the other (`-ne 1,1`), and shuts down the DBMS.
This is repeated 2 times (`-nc`).


```bash
mkdir -p ./logs/
BEXHOMA_MS=1
BEXHOMA_STORAGE_CLASS="shared"

BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"

bexhoma tpch \
  -dbms MonetDB \
  -sf 100 \
  -nc 2 \
  -ne 1,1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 3600 \
  -lc 16 \
  -lr 256Gi \
  -rc 16 \
  -rr 256Gi \
  -rss 1000Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_monetdb_sf100_repeated.log
```

### Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_monetdb_sf100_repeated_summary.md" target="_blank" rel="noopener">docs_tpch_monetdb_sf100_repeated.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=100
* Type: tpch
* Duration: 2206s 
* Code: 1794665935
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=100) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 3600.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * Database is persisted to disk of type nvme and size 1000Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * SUT requests 16 CPU and 256Gi RAM. CPU limit is 16. RAM limit is 256Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:574831
  * datadisk:198530
  * volume_size:984G
  * volume_used:194G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1794665935
* monetdb-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:574501
  * datadisk:195342
  * volume_size:984G
  * volume_used:191G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1794665935
* monetdb-1-2-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:574184
  * datadisk:195342
  * volume_size:984G
  * volume_used:191G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1794665935
* monetdb-1-2-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:574171
  * datadisk:195342
  * volume_size:984G
  * volume_used:191G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1794665935

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MonetDB-1

### Data Parameters of Reused Volumes
* MonetDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1794665935-69547fb664-6g7ch: 0
* bexhoma-sut-monetdb-1-1794665935-5d56566789-wb94c: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 2: tpch (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 2: tpch (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |  100 |     3963.00 |           5.00 |           22.00 |       1753.00 |         2179.00 |              0 |         0 |             | None           |             0 | False         |               90.84 | True                |
| MonetDB-1-2 |                2 |  100 |     3963.00 |           5.00 |           22.00 |       1753.00 |         2179.00 |              0 |         0 |             | None           |             0 | False         |               90.84 | True                |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |     SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 100.00 |               22 |                  22 |        483 |            9.01 |            41750.15 |          16397.52 |          -1 |
| monetdb-1-1-2-1-1 | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |       1 | 100.00 |               22 |                  22 |        321 |            6.48 |            59287.19 |          24672.90 |          -1 |
| monetdb-1-2-1-1-1 | monetdb-1-2-1 | monetdb-1-2-1-1 |                2 |        1 |               1 |       1 | 100.00 |               22 |                  22 |        645 |           12.92 |            28916.92 |          12279.07 |          -1 |
| monetdb-1-2-2-1-1 | monetdb-1-2-2 | monetdb-1-2-2-1 |                2 |        2 |               1 |       1 | 100.00 |               22 |                  22 |        325 |            6.50 |            58738.14 |          24369.23 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               22 |                  22 |        483 |            9.01 |            41750.15 |          16397.52 |          -1 |
| monetdb-1-1-2 | monetdb-1-1-2 |                1 |        2 |               1 |           1 | 100.00 |               22 |                  22 |        321 |            6.48 |            59287.19 |          24672.90 |          -1 |
| monetdb-1-2-1 | monetdb-1-2-1 |                2 |        1 |               1 |           1 | 100.00 |               22 |                  22 |        645 |           12.92 |            28916.92 |          12279.07 |          -1 |
| monetdb-1-2-2 | monetdb-1-2-2 |                2 |        2 |               1 |           1 | 100.00 |               22 |                  22 |        325 |            6.50 |            58738.14 |          24369.23 |          -1 |

#### Query Completion per Phase

| phase         |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:--------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| monetdb-1-1-2 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| monetdb-1-2-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| monetdb-1-2-2 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   monetdb-1-1-1-1-1 |   monetdb-1-1-2-1-1 |   monetdb-1-2-1-1-1 |   monetdb-1-2-2-1-1 |
|:----------------------------------------------------|--------------------:|--------------------:|--------------------:|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |           117995.88 |            92470.27 |           146275.94 |           104550.09 |
| Minimum Cost Supplier Query (TPC-H Q2)              |             5777.35 |              986.58 |             9761.06 |              825.04 |
| Shipping Priority (TPC-H Q3)                        |            20806.76 |             7049.35 |            36761.09 |             7191.89 |
| Order Priority Checking Query (TPC-H Q4)            |            18074.84 |             9966.42 |            25197.21 |            10292.87 |
| Local Supplier Volume (TPC-H Q5)                    |             6589.73 |             7347.92 |            12238.54 |             9499.77 |
| Forecasting Revenue Change (TPC-H Q6)               |             1917.67 |             1782.88 |             2117.49 |             1833.36 |
| Volume Shipping Query (TPC-H Q7)                    |             6459.77 |             8828.39 |             8475.90 |             9190.21 |
| National Market Share (TPC-H Q8)                    |            40980.54 |            14233.34 |            67192.49 |            13961.93 |
| Product Type Profit Measure (TPC-H Q9)              |             9635.18 |             8097.81 |            17582.99 |             6146.33 |
| Returned Item Reporting Query (TPC-H Q10)           |            16223.34 |            14688.22 |            19669.80 |            12408.62 |
| Important Stock Identification (TPC-H Q11)          |             1760.98 |             1055.57 |             2441.04 |             1056.41 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             1758.23 |             2679.54 |             3018.58 |             2300.37 |
| Customer Distribution (TPC-H Q13)                   |            54705.39 |            34864.97 |            98116.35 |            30101.02 |
| Promotion Effect Query (TPC-H Q14)                  |              851.77 |             1153.36 |             1175.24 |             1119.44 |
| Top Supplier Query (TPC-H Q15)                      |             3063.52 |             3415.22 |             6228.81 |             2982.16 |
| Parts/Supplier Relationship (TPC-H Q16)             |             5256.18 |             5720.37 |             6147.03 |             5831.57 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |            41532.39 |             2919.25 |            36921.24 |             2893.52 |
| Large Volume Customer (TPC-H Q18)                   |            12001.05 |            11625.48 |            15793.34 |            11950.04 |
| Discounted Revenue (TPC-H Q19)                      |             1507.68 |             1651.99 |             2626.83 |             3656.43 |
| Potential Part Promotion (TPC-H Q20)                |             4867.77 |             4743.54 |             7527.01 |             4472.30 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            88404.51 |            64603.98 |            95587.04 |            62052.40 |
| Global Sales Opportunity Query (TPC-H Q22)          |             3811.28 |             3573.45 |             5121.88 |             3863.54 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      1453.75 |     13.86 |         114.56 |                114.56 |
| monetdb-1-1-2-1 |      1008.80 |      6.94 |         195.84 |                195.84 |
| monetdb-1-2-1-1 |      1722.90 |      6.91 |         113.97 |                113.97 |
| monetdb-1-2-2-1 |      1054.07 |     10.89 |         194.43 |                194.44 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        29.29 |      0.28 |           0.45 |                  0.46 |
| monetdb-1-1-2-1 |        28.24 |      0.20 |           0.41 |                  0.42 |
| monetdb-1-2-1-1 |        28.13 |      0.40 |           0.39 |                  0.41 |
| monetdb-1-2-2-1 |        26.13 |      0.47 |           0.42 |                  0.43 |

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MonetDB-1)
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: No monitoring metrics missing
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

### Perform Benchmark - Throughput Test

This starts a new instance of MonetDB on the prepared database of the shared disk.
It runs two power tests, one after the other, then a throughput test with 3 parallel drivers (`-ne 1,1,3`), and shuts down the DBMS.


```bash
mkdir -p ./logs/
BEXHOMA_MS=1
BEXHOMA_STORAGE_CLASS="shared"

BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"

bexhoma tpch \
  -dbms MonetDB \
  -sf 100 \
  -nc 1 \
  -ne 1,1,3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 3600 \
  -lc 16 \
  -lr 256Gi \
  -rc 16 \
  -rr 256Gi \
  -rss 1000Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_monetdb_sf100_throughput.log
```

### Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_monetdb_sf100_throughput_summary.md" target="_blank" rel="noopener">docs_tpch_monetdb_sf100_throughput.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=100
* Type: tpch
* Duration: 2182s 
* Code: 1794668223
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=100) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 3600.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * Database is persisted to disk of type nvme and size 1000Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 1, 3] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * SUT requests 16 CPU and 256Gi RAM. CPU limit is 16. RAM limit is 256Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:575865
  * datadisk:195342
  * volume_size:984G
  * volume_used:191G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1794668223
* monetdb-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:584558
  * datadisk:195342
  * volume_size:984G
  * volume_used:191G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1794668223
* monetdb-1-1-3-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:573372
  * datadisk:195342
  * volume_size:984G
  * volume_used:191G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1794668223
* monetdb-1-1-3-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:573372
  * datadisk:195342
  * volume_size:984G
  * volume_used:191G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1794668223
* monetdb-1-1-3-1-3 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:573372
  * datadisk:195342
  * volume_size:984G
  * volume_used:191G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1794668223

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MonetDB-1

### Data Parameters of Reused Volumes
* MonetDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1794668223-868c9d6698-mcgb5: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 3: tpch (3 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 3: tpch (3 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |  100 |     3963.00 |           5.00 |           22.00 |       1753.00 |         2179.00 |              0 |         0 |             | None           |             0 | False         |               90.84 | True                |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |     SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 100.00 |               22 |                  22 |        668 |           12.18 |            30614.54 |          11856.29 |          -1 |
| monetdb-1-1-2-1-1 | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |       1 | 100.00 |               22 |                  22 |        339 |            6.18 |            61674.11 |          23362.83 |          -1 |
| monetdb-1-1-3-1-1 | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |       1 | 100.00 |               22 |                  22 |        893 |           14.97 |            24810.40 |           8868.98 |          -1 |
| monetdb-1-1-3-1-2 | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |       2 | 100.00 |               22 |                  22 |        853 |           13.27 |            28236.90 |           9284.88 |          -1 |
| monetdb-1-1-3-1-3 | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |       3 | 100.00 |               22 |                  22 |        883 |           15.46 |            24712.46 |           8969.42 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               22 |                  22 |        668 |           12.18 |            30614.54 |          11856.29 |          -1 |
| monetdb-1-1-2 | monetdb-1-1-2 |                1 |        2 |               1 |           1 | 100.00 |               22 |                  22 |        339 |            6.18 |            61674.11 |          23362.83 |          -1 |
| monetdb-1-1-3 | monetdb-1-1-3 |                1 |        3 |               1 |           3 | 100.00 |               66 |                  66 |        893 |           14.53 |            25869.56 |          26606.94 |          -1 |

#### Query Completion per Phase

| phase         |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:--------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| monetdb-1-1-2 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| monetdb-1-1-3 |      3 | 3/3                                 | 3/3                                      | 3/3                            | 3/3                                        | 3/3                                | 3/3                                     | 3/3                                | 3/3                                | 3/3                                      | 3/3                                         | 3/3                                          | 3/3                                             | 3/3                                 | 3/3                                  | 3/3                              | 3/3                                       | 3/3                                        | 3/3                                 | 3/3                              | 3/3                                    | 3/3                                                   | 3/3                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   monetdb-1-1-1-1-1 |   monetdb-1-1-2-1-1 |   monetdb-1-1-3-1-1 |   monetdb-1-1-3-1-2 |   monetdb-1-1-3-1-3 |
|:----------------------------------------------------|--------------------:|--------------------:|--------------------:|--------------------:|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |           154045.20 |           108857.02 |           356690.13 |           385596.16 |           369442.43 |
| Minimum Cost Supplier Query (TPC-H Q2)              |            11194.49 |              873.83 |             4200.71 |              812.21 |             8098.29 |
| Shipping Priority (TPC-H Q3)                        |            36067.75 |             7410.09 |            38733.65 |            12735.95 |            21417.69 |
| Order Priority Checking Query (TPC-H Q4)            |            24287.67 |            10598.70 |            14173.51 |            16881.08 |            16390.00 |
| Local Supplier Volume (TPC-H Q5)                    |            12147.91 |             5402.49 |            10400.92 |             9357.54 |            10013.62 |
| Forecasting Revenue Change (TPC-H Q6)               |             1391.62 |             2232.63 |             5649.61 |             5495.35 |             5313.60 |
| Volume Shipping Query (TPC-H Q7)                    |             6564.15 |             5819.48 |            12174.28 |            10590.92 |            13018.51 |
| National Market Share (TPC-H Q8)                    |            69531.56 |            18536.40 |            55704.21 |            56368.33 |            54384.78 |
| Product Type Profit Measure (TPC-H Q9)              |            18688.47 |             5136.99 |            24809.34 |            25747.92 |            24914.46 |
| Returned Item Reporting Query (TPC-H Q10)           |            21279.34 |            13546.32 |            13077.47 |            13507.67 |            16062.81 |
| Important Stock Identification (TPC-H Q11)          |             2527.30 |             1078.84 |             3436.18 |             2554.70 |              956.99 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             2973.70 |             1992.39 |             5431.99 |             5696.83 |             6107.58 |
| Customer Distribution (TPC-H Q13)                   |           100139.20 |            33828.70 |            95869.63 |            98526.28 |            91777.43 |
| Promotion Effect Query (TPC-H Q14)                  |              849.85 |             1347.30 |             2272.35 |             3247.22 |             2264.52 |
| Top Supplier Query (TPC-H Q15)                      |             3454.18 |             3148.02 |             5842.88 |             3873.65 |             9300.24 |
| Parts/Supplier Relationship (TPC-H Q16)             |             5783.66 |             5692.48 |             6959.53 |             7207.31 |             7378.18 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |            37248.35 |             2518.00 |            43250.75 |            42158.81 |            42879.06 |
| Large Volume Customer (TPC-H Q18)                   |            16672.61 |            12614.35 |            23322.11 |            26683.48 |            22801.29 |
| Discounted Revenue (TPC-H Q19)                      |             2399.61 |             1726.48 |             3501.65 |             3485.62 |             3747.26 |
| Potential Part Promotion (TPC-H Q20)                |             7238.10 |             4297.67 |            13829.20 |             9923.88 |            15059.59 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |           110983.94 |            69695.95 |           133333.23 |            89799.88 |           120567.07 |
| Global Sales Opportunity Query (TPC-H Q22)          |             4984.14 |             3683.31 |             3146.32 |             6407.67 |             4477.42 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      1599.04 |      7.16 |         113.97 |                113.97 |
| monetdb-1-1-2-1 |       948.98 |      6.12 |         195.87 |                195.87 |
| monetdb-1-1-3-1 |      4181.35 |     14.44 |         255.55 |                256.00 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        27.41 |      0.33 |           0.39 |                  0.40 |
| monetdb-1-1-2-1 |        27.97 |      0.19 |           0.46 |                  0.47 |
| monetdb-1-1-3-1 |        87.70 |      1.71 |           0.40 |                  0.41 |

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MonetDB-1)
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: No monitoring metrics missing
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

The loading times for both instances of loading are the same, since both relate to the same process of ingesting into the database.
Note the added section about `volume_size` and `volume_used` in the connections section.


## TPC-DS

The experiment is run with the [tpcds file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpcds.py).

### Power Test

```bash
bexhoma tpcds \
  -dbms MonetDB \
  -sf 3 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 1 \
  -nbp 1 \
  -xii -xic -xis \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_monetdb.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_monetdb_summary.md" target="_blank" rel="noopener">docs_tpcds_monetdb.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 725s 
* Code: 1794670484
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1181103
  * datadisk:12129
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794670484

### Ingestion
* MonetDB-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1794670484-7667447b4d-rzpb9: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |    3 |      439.00 |           2.00 |            1.00 |        367.00 |           61.00 |              8 |         0 |             | None           |             0 | False         |               24.60 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 3.00 |               99 |                  99 |         25 |            0.09 |           124434.42 |          42768.00 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |         25 |            0.09 |           124434.42 |          42768.00 |          -1 |

#### Query Completion per Phase

| phase         |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:--------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   monetdb-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |               37.61 |
| TPC-DS Q2     |              136.78 |
| TPC-DS Q3     |               34.20 |
| TPC-DS Q4     |             1148.98 |
| TPC-DS Q5     |              125.32 |
| TPC-DS Q6     |               49.93 |
| TPC-DS Q7     |               52.21 |
| TPC-DS Q8     |               35.46 |
| TPC-DS Q9     |              101.16 |
| TPC-DS Q10    |               25.78 |
| TPC-DS Q11    |              523.77 |
| TPC-DS Q12    |               24.47 |
| TPC-DS Q13    |               73.80 |
| TPC-DS Q14a+b |             2635.56 |
| TPC-DS Q15    |               20.24 |
| TPC-DS Q16    |              116.58 |
| TPC-DS Q17    |              180.64 |
| TPC-DS Q18    |              108.55 |
| TPC-DS Q19    |               57.60 |
| TPC-DS Q20    |               29.93 |
| TPC-DS Q21    |              132.29 |
| TPC-DS Q22    |             1130.18 |
| TPC-DS Q23a+b |             2577.24 |
| TPC-DS Q24a+b |              297.26 |
| TPC-DS Q25    |              194.84 |
| TPC-DS Q26    |               29.70 |
| TPC-DS Q27    |              160.72 |
| TPC-DS Q28    |               93.53 |
| TPC-DS Q29    |              191.20 |
| TPC-DS Q30    |               20.43 |
| TPC-DS Q31    |              282.19 |
| TPC-DS Q32    |               21.77 |
| TPC-DS Q33    |               35.30 |
| TPC-DS Q34    |               49.97 |
| TPC-DS Q35    |              146.36 |
| TPC-DS Q36    |              304.90 |
| TPC-DS Q37    |              100.68 |
| TPC-DS Q38    |              334.01 |
| TPC-DS Q39a+b |             1273.27 |
| TPC-DS Q40    |               78.88 |
| TPC-DS Q41    |                6.24 |
| TPC-DS Q42    |               35.37 |
| TPC-DS Q43    |               67.32 |
| TPC-DS Q44    |               52.35 |
| TPC-DS Q45    |               15.14 |
| TPC-DS Q46    |               60.27 |
| TPC-DS Q47    |              194.24 |
| TPC-DS Q48    |               46.14 |
| TPC-DS Q49    |              122.59 |
| TPC-DS Q50    |              143.70 |
| TPC-DS Q51    |              439.98 |
| TPC-DS Q52    |               38.75 |
| TPC-DS Q53    |               35.58 |
| TPC-DS Q54    |               27.44 |
| TPC-DS Q55    |               17.49 |
| TPC-DS Q56    |               74.77 |
| TPC-DS Q57    |              108.10 |
| TPC-DS Q58    |              132.58 |
| TPC-DS Q59    |              198.70 |
| TPC-DS Q60    |               42.88 |
| TPC-DS Q61    |               70.42 |
| TPC-DS Q62    |               33.17 |
| TPC-DS Q63    |               57.45 |
| TPC-DS Q64    |              754.42 |
| TPC-DS Q65    |              136.45 |
| TPC-DS Q66    |               40.32 |
| TPC-DS Q67    |              426.82 |
| TPC-DS Q68    |               75.63 |
| TPC-DS Q69    |               23.68 |
| TPC-DS Q70    |               73.13 |
| TPC-DS Q71    |               36.53 |
| TPC-DS Q72    |              197.88 |
| TPC-DS Q73    |               36.44 |
| TPC-DS Q74    |              179.51 |
| TPC-DS Q75    |              495.31 |
| TPC-DS Q76    |               61.60 |
| TPC-DS Q77    |               82.66 |
| TPC-DS Q78    |              784.36 |
| TPC-DS Q79    |               63.51 |
| TPC-DS Q80    |              553.74 |
| TPC-DS Q81    |               34.07 |
| TPC-DS Q82    |              190.27 |
| TPC-DS Q83    |               24.81 |
| TPC-DS Q84    |               74.16 |
| TPC-DS Q85    |               32.67 |
| TPC-DS Q86    |               26.40 |
| TPC-DS Q87    |              283.36 |
| TPC-DS Q88    |               86.13 |
| TPC-DS Q89    |               48.40 |
| TPC-DS Q90    |                9.88 |
| TPC-DS Q91    |               14.49 |
| TPC-DS Q92    |               15.00 |
| TPC-DS Q93    |              131.11 |
| TPC-DS Q94    |               33.53 |
| TPC-DS Q95    |              427.35 |
| TPC-DS Q96    |               15.13 |
| TPC-DS Q97    |              238.72 |
| TPC-DS Q98    |               48.24 |
| TPC-DS Q99    |               40.33 |

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

At SF=3 the benchmarking phase is shorter than the minute that monitoring needs; see [TPC-DS at SF 30](#tpc-ds-at-sf-30) for a longer run.

```bash
bexhoma tpcds \
  -dbms MonetDB \
  -sf 3 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 1 \
  -nbp 1 \
  -xii -xic -xis \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_monetdb_monitoring.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_monetdb_monitoring_summary.md" target="_blank" rel="noopener">docs_tpcds_monetdb_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 713s 
* Code: 1794671328
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1158899
  * datadisk:12125
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794671328

### Ingestion
* MonetDB-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1794671328-56564cf857-pk9x5: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |    3 |      394.00 |           3.00 |            1.00 |        321.00 |           61.00 |              8 |         0 |             | None           |             0 | False         |               27.41 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 3.00 |               99 |                  99 |         37 |            0.09 |           116832.22 |          28897.30 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |         37 |            0.09 |           116832.22 |          28897.30 |          -1 |

#### Query Completion per Phase

| phase         |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:--------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   monetdb-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |               40.55 |
| TPC-DS Q2     |              147.89 |
| TPC-DS Q3     |               35.01 |
| TPC-DS Q4     |             1151.68 |
| TPC-DS Q5     |              125.37 |
| TPC-DS Q6     |               59.07 |
| TPC-DS Q7     |               51.47 |
| TPC-DS Q8     |               46.24 |
| TPC-DS Q9     |              101.28 |
| TPC-DS Q10    |               57.59 |
| TPC-DS Q11    |              945.99 |
| TPC-DS Q12    |               26.47 |
| TPC-DS Q13    |               67.12 |
| TPC-DS Q14a+b |             2549.63 |
| TPC-DS Q15    |               26.76 |
| TPC-DS Q16    |              129.42 |
| TPC-DS Q17    |              168.26 |
| TPC-DS Q18    |              252.28 |
| TPC-DS Q19    |               93.43 |
| TPC-DS Q20    |               38.60 |
| TPC-DS Q21    |              194.28 |
| TPC-DS Q22    |             1103.17 |
| TPC-DS Q23a+b |             3301.79 |
| TPC-DS Q24a+b |              247.66 |
| TPC-DS Q25    |              220.26 |
| TPC-DS Q26    |               37.23 |
| TPC-DS Q27    |              159.74 |
| TPC-DS Q28    |               96.92 |
| TPC-DS Q29    |              187.33 |
| TPC-DS Q30    |               24.03 |
| TPC-DS Q31    |              173.95 |
| TPC-DS Q32    |               35.12 |
| TPC-DS Q33    |               28.86 |
| TPC-DS Q34    |               37.46 |
| TPC-DS Q35    |               76.43 |
| TPC-DS Q36    |              154.94 |
| TPC-DS Q37    |              115.65 |
| TPC-DS Q38    |              409.93 |
| TPC-DS Q39a+b |             1304.21 |
| TPC-DS Q40    |               78.95 |
| TPC-DS Q41    |                5.87 |
| TPC-DS Q42    |               34.56 |
| TPC-DS Q43    |               76.14 |
| TPC-DS Q44    |               68.81 |
| TPC-DS Q45    |               19.65 |
| TPC-DS Q46    |               59.02 |
| TPC-DS Q47    |              210.91 |
| TPC-DS Q48    |               50.18 |
| TPC-DS Q49    |              109.65 |
| TPC-DS Q50    |              150.72 |
| TPC-DS Q51    |              613.01 |
| TPC-DS Q52    |               40.39 |
| TPC-DS Q53    |               47.11 |
| TPC-DS Q54    |               46.80 |
| TPC-DS Q55    |               30.38 |
| TPC-DS Q56    |               47.03 |
| TPC-DS Q57    |               65.00 |
| TPC-DS Q58    |               67.72 |
| TPC-DS Q59    |              131.16 |
| TPC-DS Q60    |               32.48 |
| TPC-DS Q61    |               51.09 |
| TPC-DS Q62    |               29.69 |
| TPC-DS Q63    |               35.11 |
| TPC-DS Q64    |              455.32 |
| TPC-DS Q65    |              147.56 |
| TPC-DS Q66    |               47.06 |
| TPC-DS Q67    |              514.06 |
| TPC-DS Q68    |               62.23 |
| TPC-DS Q69    |               34.90 |
| TPC-DS Q70    |               98.13 |
| TPC-DS Q71    |               37.96 |
| TPC-DS Q72    |              403.32 |
| TPC-DS Q73    |               54.74 |
| TPC-DS Q74    |              734.96 |
| TPC-DS Q75    |              518.65 |
| TPC-DS Q76    |               51.52 |
| TPC-DS Q77    |               81.56 |
| TPC-DS Q78    |              853.73 |
| TPC-DS Q79    |               61.81 |
| TPC-DS Q80    |             1002.85 |
| TPC-DS Q81    |               26.03 |
| TPC-DS Q82    |              181.73 |
| TPC-DS Q83    |               14.17 |
| TPC-DS Q84    |               40.48 |
| TPC-DS Q85    |               28.36 |
| TPC-DS Q86    |               35.22 |
| TPC-DS Q87    |              211.68 |
| TPC-DS Q88    |               94.08 |
| TPC-DS Q89    |               70.94 |
| TPC-DS Q90    |               14.48 |
| TPC-DS Q91    |               15.86 |
| TPC-DS Q92    |               17.09 |
| TPC-DS Q93    |              147.32 |
| TPC-DS Q94    |               34.11 |
| TPC-DS Q95    |              483.32 |
| TPC-DS Q96    |               16.49 |
| TPC-DS Q97    |              252.83 |
| TPC-DS Q98    |               50.81 |
| TPC-DS Q99    |               60.46 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |       324.40 |      1.14 |          10.27 |                 12.15 |

### Loading phase: component data generator

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        42.35 |      0.18 |           0.01 |                  2.65 |

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        56.06 |      1.44 |          14.73 |                 16.61 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        12.98 |      0.50 |           0.30 |                  0.30 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loading.log, expected: series exists only while non-zero)

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

### Throughput Test on Persistent Storage

```bash
bexhoma tpcds \
  -dbms MonetDB \
  -sf 3 \
  -nc 2 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 1 \
  -nbp 1 \
  -xii -xic -xis \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_monetdb_storage.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_monetdb_storage_summary.md" target="_blank" rel="noopener">docs_tpcds_monetdb_storage.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 1218s 
* Code: 1794672202
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1146791
  * datadisk:12126
  * volume_size:49G
  * volume_used:12G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794672202
* monetdb-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1146792
  * datadisk:12347
  * volume_size:49G
  * volume_used:13G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794672202
* monetdb-1-1-2-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1146792
  * datadisk:12347
  * volume_size:49G
  * volume_used:13G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794672202
* monetdb-1-2-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1146788
  * datadisk:10226
  * volume_size:49G
  * volume_used:10G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794672202
* monetdb-1-2-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1146789
  * datadisk:10400
  * volume_size:49G
  * volume_used:11G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794672202
* monetdb-1-2-2-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1146789
  * datadisk:10400
  * volume_size:49G
  * volume_used:11G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794672202

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MonetDB-1-2

### Data Parameters of Reused Volumes
* MonetDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### Ingestion
* MonetDB-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1794672202-56b9b78596-wqsql: 0
* bexhoma-sut-monetdb-1-1794672202-669b88d7f4-wmvng: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpcds (2 pods)
* DBMS MonetDB-1 - Experiment 2 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 2: tpcds (2 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpcds (2 pods)
* DBMS MonetDB-1 - Experiment 2 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 2: tpcds (2 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |    3 |      394.00 |           5.00 |            1.00 |        316.00 |           64.00 |              8 |         0 |             | None           |             0 | False         |               27.41 | False               |
| MonetDB-1-2 |                2 |    3 |      394.00 |           5.00 |            1.00 |        316.00 |           64.00 |              8 |         0 |             | None           |             0 | False         |               27.41 | True                |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 3.00 |               99 |                  99 |         29 |            0.09 |           125508.57 |          36868.97 |          -1 |
| monetdb-1-1-2-1-1 | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |       1 | 3.00 |               99 |                  99 |         27 |            0.09 |           124088.29 |          39600.00 |          -1 |
| monetdb-1-1-2-1-2 | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |       2 | 3.00 |               99 |                  99 |         32 |            0.08 |           130495.46 |          33412.50 |          -1 |
| monetdb-1-2-1-1-1 | monetdb-1-2-1 | monetdb-1-2-1-1 |                2 |        1 |               1 |       1 | 3.00 |               99 |                  99 |         56 |            0.12 |            89607.54 |          19092.86 |          -1 |
| monetdb-1-2-2-1-1 | monetdb-1-2-2 | monetdb-1-2-2-1 |                2 |        2 |               1 |       1 | 3.00 |               99 |                  99 |         28 |            0.09 |           124310.61 |          38185.71 |          -1 |
| monetdb-1-2-2-1-2 | monetdb-1-2-2 | monetdb-1-2-2-1 |                2 |        2 |               1 |       2 | 3.00 |               99 |                  99 |         28 |            0.09 |           123857.20 |          38185.71 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |         29 |            0.09 |           125508.57 |          36868.97 |          -1 |
| monetdb-1-1-2 | monetdb-1-1-2 |                1 |        2 |               1 |           2 | 3.00 |              198 |                 198 |         32 |            0.08 |           127251.55 |          66825.00 |          -1 |
| monetdb-1-2-1 | monetdb-1-2-1 |                2 |        1 |               1 |           1 | 3.00 |               99 |                  99 |         56 |            0.12 |            89607.54 |          19092.86 |          -1 |
| monetdb-1-2-2 | monetdb-1-2-2 |                2 |        2 |               1 |           2 | 3.00 |              198 |                 198 |         28 |            0.09 |           124083.70 |          76371.43 |          -1 |

#### Query Completion per Phase

| phase         |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:--------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| monetdb-1-1-2 |      2 | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | yes        |
| monetdb-1-2-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| monetdb-1-2-2 |      2 | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   monetdb-1-1-1-1-1 |   monetdb-1-1-2-1-1 |   monetdb-1-1-2-1-2 |   monetdb-1-2-1-1-1 |   monetdb-1-2-2-1-1 |   monetdb-1-2-2-1-2 |
|:--------------|--------------------:|--------------------:|--------------------:|--------------------:|--------------------:|--------------------:|
| TPC-DS Q1     |               37.18 |               35.10 |               35.81 |              161.19 |               48.72 |               33.27 |
| TPC-DS Q2     |              258.10 |              145.74 |              123.75 |              619.32 |              104.12 |              126.34 |
| TPC-DS Q3     |               32.55 |               31.93 |               35.88 |              875.35 |               35.42 |               28.13 |
| TPC-DS Q4     |             1224.83 |             1688.29 |             1362.29 |             3099.13 |             1200.90 |             1245.69 |
| TPC-DS Q5     |              139.81 |              217.89 |              251.91 |             2771.03 |              116.09 |              128.96 |
| TPC-DS Q6     |              121.49 |               47.58 |               84.30 |               63.71 |               48.08 |               49.65 |
| TPC-DS Q7     |               76.55 |               57.89 |               62.35 |             1675.95 |               52.23 |               71.11 |
| TPC-DS Q8     |               41.08 |               31.31 |               33.07 |               46.41 |               35.99 |               34.59 |
| TPC-DS Q9     |              104.84 |              112.49 |              124.89 |              367.18 |              104.02 |              111.95 |
| TPC-DS Q10    |               27.95 |               33.86 |               22.83 |             5344.10 |               43.05 |               26.65 |
| TPC-DS Q11    |              545.52 |              530.23 |              546.47 |              531.64 |              619.61 |              577.55 |
| TPC-DS Q12    |               26.17 |               20.98 |               17.05 |               53.79 |               19.32 |               18.09 |
| TPC-DS Q13    |               71.66 |               70.43 |               71.96 |               93.10 |               87.52 |               80.18 |
| TPC-DS Q14a+b |             2781.14 |             2435.95 |             2227.78 |             2625.35 |             2862.70 |             2739.44 |
| TPC-DS Q15    |               22.57 |               23.19 |               24.07 |               24.56 |               36.06 |               24.23 |
| TPC-DS Q16    |              124.36 |              132.40 |              125.88 |              286.75 |              209.05 |              153.19 |
| TPC-DS Q17    |              182.06 |              164.91 |              150.09 |              230.30 |              173.11 |              231.44 |
| TPC-DS Q18    |              105.37 |               80.72 |               78.04 |              106.06 |              101.72 |               90.04 |
| TPC-DS Q19    |               61.06 |               53.23 |               50.64 |               62.00 |               68.81 |               56.21 |
| TPC-DS Q20    |               24.21 |               23.74 |               21.50 |               31.02 |               24.69 |               24.61 |
| TPC-DS Q21    |              128.07 |              123.08 |              119.31 |             2287.06 |              118.20 |              115.68 |
| TPC-DS Q22    |             1000.68 |             1120.40 |             1291.85 |             1642.42 |             1153.87 |             1186.29 |
| TPC-DS Q23a+b |             3183.20 |             3355.05 |             3242.71 |             2642.15 |             3073.66 |             3500.54 |
| TPC-DS Q24a+b |              275.38 |              549.21 |              301.41 |              299.92 |              277.20 |              569.81 |
| TPC-DS Q25    |              209.13 |              191.69 |              202.67 |              193.70 |              190.62 |              219.82 |
| TPC-DS Q26    |               32.95 |               33.56 |               33.81 |               31.77 |               34.10 |               29.63 |
| TPC-DS Q27    |              225.41 |              170.25 |              153.19 |              175.88 |              228.26 |              185.36 |
| TPC-DS Q28    |              106.82 |              105.53 |               96.26 |               86.91 |              163.19 |               98.35 |
| TPC-DS Q29    |              195.85 |              211.58 |              170.73 |              181.10 |              417.33 |              182.42 |
| TPC-DS Q30    |               17.30 |               21.57 |               16.05 |               31.99 |               21.13 |               13.90 |
| TPC-DS Q31    |              330.84 |              205.17 |              143.34 |              185.59 |              305.61 |              176.48 |
| TPC-DS Q32    |               27.12 |               40.02 |               27.59 |               24.71 |               25.11 |               28.08 |
| TPC-DS Q33    |               47.08 |               37.36 |               29.71 |               34.55 |               29.35 |               30.72 |
| TPC-DS Q34    |               38.34 |               38.91 |               37.27 |               39.58 |               37.78 |               39.91 |
| TPC-DS Q35    |               74.98 |               84.41 |               82.10 |              100.45 |               84.19 |               97.29 |
| TPC-DS Q36    |              148.99 |              156.55 |              129.00 |              148.95 |              181.33 |              138.12 |
| TPC-DS Q37    |              131.53 |               81.29 |               72.81 |              173.16 |               66.26 |               65.39 |
| TPC-DS Q38    |              221.97 |              200.26 |              183.82 |              214.36 |              210.50 |              239.55 |
| TPC-DS Q39a+b |             1236.25 |             1151.81 |             1574.89 |             1251.28 |             1210.00 |             1277.11 |
| TPC-DS Q40    |               80.19 |               84.13 |               90.34 |               40.32 |               34.61 |               38.13 |
| TPC-DS Q41    |                4.26 |                8.96 |                5.08 |                6.72 |                7.53 |               10.47 |
| TPC-DS Q42    |               28.19 |               44.82 |               34.32 |               33.77 |               26.28 |               40.14 |
| TPC-DS Q43    |               88.02 |              115.62 |               90.71 |               74.59 |               68.62 |              105.06 |
| TPC-DS Q44    |               89.09 |              151.49 |               85.36 |              713.01 |               86.19 |              174.81 |
| TPC-DS Q45    |               15.84 |               18.56 |               19.56 |               14.77 |               14.84 |               19.64 |
| TPC-DS Q46    |               58.79 |               94.28 |               56.19 |               70.02 |               53.80 |              109.87 |
| TPC-DS Q47    |              179.05 |              260.14 |              183.41 |              192.46 |              406.57 |              369.04 |
| TPC-DS Q48    |               48.16 |               50.46 |               66.88 |               48.30 |               95.63 |               55.75 |
| TPC-DS Q49    |              201.47 |              145.30 |              111.36 |              323.06 |              236.67 |              108.20 |
| TPC-DS Q50    |              198.04 |              142.76 |              141.78 |              146.73 |              217.63 |              151.50 |
| TPC-DS Q51    |              438.04 |              484.35 |              566.46 |              475.78 |              491.37 |              580.12 |
| TPC-DS Q52    |               32.58 |               43.45 |               42.78 |               37.74 |               37.74 |               28.23 |
| TPC-DS Q53    |               35.08 |               26.01 |               43.37 |               35.15 |               28.82 |               34.18 |
| TPC-DS Q54    |               29.34 |               26.96 |               30.53 |               27.33 |               30.42 |               36.34 |
| TPC-DS Q55    |               28.92 |               27.22 |               43.04 |               23.46 |               26.30 |               26.55 |
| TPC-DS Q56    |               30.51 |               25.88 |               33.28 |               50.30 |               28.24 |               29.18 |
| TPC-DS Q57    |               68.73 |               73.46 |               76.41 |               70.49 |               82.99 |               77.11 |
| TPC-DS Q58    |               74.45 |               46.39 |               70.92 |               62.73 |               55.94 |               39.31 |
| TPC-DS Q59    |              123.19 |              140.32 |              139.29 |              128.96 |              134.56 |              127.51 |
| TPC-DS Q60    |               31.32 |               30.77 |               31.16 |               30.46 |               27.01 |               31.04 |
| TPC-DS Q61    |               54.89 |               60.39 |               53.72 |               54.66 |               61.56 |               58.15 |
| TPC-DS Q62    |               30.08 |               26.54 |               26.35 |               30.44 |               32.12 |               27.72 |
| TPC-DS Q63    |               31.51 |               36.92 |               26.46 |               34.79 |               53.89 |               42.71 |
| TPC-DS Q64    |              442.37 |              326.04 |              317.33 |              425.19 |              338.63 |              499.09 |
| TPC-DS Q65    |              134.96 |              116.01 |              139.48 |              135.69 |              304.11 |              129.26 |
| TPC-DS Q66    |               41.69 |               40.61 |               38.54 |               50.58 |               57.55 |               41.40 |
| TPC-DS Q67    |              523.41 |              558.37 |              502.10 |              481.10 |              476.01 |              519.11 |
| TPC-DS Q68    |               69.28 |               95.16 |               71.13 |               69.64 |               59.95 |               78.31 |
| TPC-DS Q69    |               33.57 |               49.22 |               37.49 |               40.76 |               32.31 |               33.10 |
| TPC-DS Q70    |               79.94 |               77.78 |               83.09 |              171.94 |               94.97 |               76.02 |
| TPC-DS Q71    |               37.75 |               41.77 |               37.62 |               68.29 |               41.30 |               41.63 |
| TPC-DS Q72    |              222.96 |              215.50 |              196.42 |              456.50 |              222.00 |              218.95 |
| TPC-DS Q73    |               39.20 |               57.56 |               60.51 |               48.08 |               31.48 |               42.38 |
| TPC-DS Q74    |              158.73 |              150.56 |              354.10 |              297.57 |              154.46 |              170.80 |
| TPC-DS Q75    |              512.72 |              474.20 |              751.81 |              659.65 |              565.25 |              612.98 |
| TPC-DS Q76    |               58.64 |               64.92 |               60.56 |              683.78 |               59.82 |               54.01 |
| TPC-DS Q77    |              160.23 |               90.61 |              154.03 |               92.54 |               88.08 |               91.38 |
| TPC-DS Q78    |              862.31 |              795.43 |              813.15 |              934.29 |             1131.68 |             1133.20 |
| TPC-DS Q79    |               61.87 |               60.14 |               58.32 |               61.28 |              104.83 |               71.08 |
| TPC-DS Q80    |              533.03 |              548.80 |              503.30 |              541.89 |              684.53 |              616.25 |
| TPC-DS Q81    |               25.03 |               41.05 |               15.06 |               27.45 |               21.63 |               17.21 |
| TPC-DS Q82    |              173.51 |              146.44 |               99.01 |              191.57 |               98.00 |               90.91 |
| TPC-DS Q83    |                9.98 |               11.99 |                9.40 |               14.30 |               10.13 |               13.38 |
| TPC-DS Q84    |               50.76 |                9.33 |                8.73 |               45.22 |                9.79 |                9.72 |
| TPC-DS Q85    |               53.37 |               37.30 |               43.42 |               33.44 |               29.19 |               34.16 |
| TPC-DS Q86    |               29.28 |               40.94 |               91.70 |               36.32 |               22.03 |               31.32 |
| TPC-DS Q87    |              237.90 |              505.39 |              394.36 |              221.03 |              245.96 |              226.31 |
| TPC-DS Q88    |              103.29 |              136.04 |              121.51 |               92.66 |              105.56 |              109.79 |
| TPC-DS Q89    |               44.20 |               63.13 |               47.25 |               46.69 |               46.98 |               51.51 |
| TPC-DS Q90    |                9.13 |               12.36 |                9.42 |               10.40 |               10.30 |                9.32 |
| TPC-DS Q91    |               14.30 |               16.44 |               15.74 |               16.76 |               12.72 |               16.51 |
| TPC-DS Q92    |               13.18 |               14.64 |               15.28 |               15.39 |               10.69 |               13.74 |
| TPC-DS Q93    |              130.03 |              134.88 |              110.64 |              140.55 |              134.82 |              192.63 |
| TPC-DS Q94    |               31.45 |               36.37 |               28.96 |               30.79 |               31.07 |               58.86 |
| TPC-DS Q95    |              446.43 |              454.51 |              423.09 |              580.56 |              499.23 |              585.63 |
| TPC-DS Q96    |               13.43 |               12.64 |               13.73 |               17.27 |               31.17 |              119.00 |
| TPC-DS Q97    |              342.32 |              240.63 |              243.16 |              619.91 |              562.72 |              548.24 |
| TPC-DS Q98    |               48.19 |               49.19 |               51.03 |               46.15 |               53.41 |               46.14 |
| TPC-DS Q99    |               42.62 |               68.96 |               37.79 |               37.74 |               67.55 |               63.33 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |       315.13 |      1.42 |           9.30 |                 11.18 |
| monetdb-1-1-2-1 |       315.13 |      1.42 |           9.30 |                 11.18 |

### Loading phase: component data generator

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |
| monetdb-1-1-2-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        38.95 |      0.18 |           0.01 |                  2.65 |
| monetdb-1-1-2-1 |        38.95 |      0.18 |           0.01 |                  2.65 |

### Benchmarking phase: SUT deployment

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 | n/a          |      2.63 |          14.49 |                 16.36 |
| monetdb-1-1-2-1 | n/a          |      8.11 |          20.98 |                 22.86 |
| monetdb-1-2-1-1 | 66.08        |      4.16 |           8.65 |                  8.66 |
| monetdb-1-2-2-1 | n/a          |      3.09 |          11.85 |                 11.86 |

### Benchmarking phase: component benchmarker

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| monetdb-1-1-2-1 | n/a          |      0.00 |           0.30 |                  0.31 |
| monetdb-1-2-1-1 | 12.76        |      0.45 |           0.27 |                  0.28 |
| monetdb-1-2-2-1 | n/a          |      0.00 |           0.32 |                  0.32 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-2-1-1 (bexhoma-metrics-monetdb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-2-1-1 (bexhoma-metrics-monetdb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection monetdb-1-2-2-1 (bexhoma-metrics-monetdb-1-2-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection monetdb-1-2-2-1 (bexhoma-metrics-monetdb-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-2-2-1 (bexhoma-metrics-monetdb-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-2-2-1 (bexhoma-metrics-monetdb-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)

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
* TEST skipped: Monitoring metrics missing (data pre-existing; phase shorter than scrape interval; series exists only while non-zero)
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


## TPC-DS at SF 30

This example shows how to run Q1-Q99 derived from TPC-DS in MonetDB at SF=30.
It covers the power and the throughput test.
The refresh stream is not included.

> The query file is derived from the TPC-DS and as such is not comparable to published TPC-DS results, as the query file results do not comply with the TPC-DS specification.

Official TPC-DS benchmark - http://www.tpc.org/tpcds




### Generate and Load Data

First, the script generates TPC-DS data at SF=30 (`-sf`) with 8 parallel generators (`-nlp`).
The generated data is stored at the shared disk `data`.
Moreover the data is loaded into an instance of MonetDB using again 8 parallel loaders.
Afterwards the script creates contraints (`-xic`) and indexes (`-xii`) and updates table statistics (`-xis`).
The database is located in a persistent volume of storageClass nvme (`-rst`) and of size 3000Gi (`-rss`).
Storage is cleaned if it has existed (`-rsr`).

The script also runs a power test (`-ne` set to 1) with timeout 14400s (`-t`) and data transfer activated (`-xdt`) once (`-nc` set to 1).
To avoid conflicts with other experiments, it runs at most 1 DBMS at a time (`-ms`).
Monitoring is activated (`-m`) for all components (`-mc`).
A node is requested that has 900Gi RAM (`-rr`), the RAM limit is 1024Gi (`-lr`).

```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"
BEXHOMA_MS=1
BEXHOMA_STORAGE_CLASS="shared"

mkdir -p $LOG_DIR

bexhoma tpcds \
  -dbms MonetDB \
  -sf 30 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 14400 \
  -lr 1024Gi \
  -rr 900Gi \
  -rsr \
  -rss 3000Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  run &>$LOG_DIR/docs_tpcds_monetdb_sf30.log
```


### Status Database and Benchmark

You can watch the status of experiments via `bexhoma status`.

The following example output shows all components of bexhoma up and running.
The cluster stores a MonetDB database corresponding to TPC-DS of SF=30.
The disk is of storageClass nvme and of size 3000Gi and 156G of that space is used.
No DBMS is running.

```bash
Dashboard: Running
Message Queue: Running
Data directory: Running
Result directory: Running
Cluster Prometheus: Running
+-----------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| Volumes                                 | configuration   | experiment   | loaded [s]   |   timeLoading [s] | dbms       | storage_class_name   | storage   | status   | size   | used   |
+=========================================+=================+==============+==============+===================+============+======================+===========+==========+========+========+
| bexhoma-storage-monetdb-tpcds-30        | monetdb         | tpcds-30     | True         |              4019 | MonetDB    | shared               | 300Gi     | Bound    | 1000G  | 156G   |
+-----------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
```

### Summary of Results

At the end of a benchmark you will see a summary like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_monetdb_sf30_summary.md" target="_blank" rel="noopener">docs_tpcds_monetdb_sf30.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=30
* Type: tpcds
* Duration: 2030s 
* Code: 1794673629
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=30) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 14400.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Database is persisted to disk of type nvme and size 3000Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * SUT requests 4 CPU and 900Gi RAM. RAM limit is 1024Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1146776
  * datadisk:75634
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794673629

### Ingestion
* MonetDB-1: 81 of 81 units ok

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1794673629-7b69967f6b-bflxk: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |   30 |      982.00 |           4.00 |            1.00 |        444.00 |          505.00 |              8 |         0 |             | None           |             0 | False         |              109.98 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 30.00 |               99 |                  99 |        715 |            0.60 |           188817.67 |          14953.85 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        715 |            0.60 |           188817.67 |          14953.85 |          -1 |

#### Query Completion per Phase

| phase         |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:--------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   monetdb-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |              344.50 |
| TPC-DS Q2     |             1404.63 |
| TPC-DS Q3     |              153.11 |
| TPC-DS Q4     |            14979.51 |
| TPC-DS Q5     |             1594.31 |
| TPC-DS Q6     |              312.43 |
| TPC-DS Q7     |              163.96 |
| TPC-DS Q8     |              316.47 |
| TPC-DS Q9     |              516.93 |
| TPC-DS Q10    |              127.75 |
| TPC-DS Q11    |             6501.86 |
| TPC-DS Q12    |              169.03 |
| TPC-DS Q13    |              291.75 |
| TPC-DS Q14a+b |            30549.51 |
| TPC-DS Q15    |              117.45 |
| TPC-DS Q16    |            44094.99 |
| TPC-DS Q17    |             2504.89 |
| TPC-DS Q18    |              875.23 |
| TPC-DS Q19    |              145.79 |
| TPC-DS Q20    |              106.35 |
| TPC-DS Q21    |              106.16 |
| TPC-DS Q22    |             1072.74 |
| TPC-DS Q23a+b |            55509.59 |
| TPC-DS Q24a+b |            15103.81 |
| TPC-DS Q25    |             2451.96 |
| TPC-DS Q26    |              212.85 |
| TPC-DS Q27    |             1733.39 |
| TPC-DS Q28    |              530.00 |
| TPC-DS Q29    |             2658.62 |
| TPC-DS Q30    |               75.15 |
| TPC-DS Q31    |             1635.91 |
| TPC-DS Q32    |              140.21 |
| TPC-DS Q33    |              105.42 |
| TPC-DS Q34    |              112.15 |
| TPC-DS Q35    |             1058.56 |
| TPC-DS Q36    |             1662.52 |
| TPC-DS Q37    |              428.55 |
| TPC-DS Q38    |             2674.65 |
| TPC-DS Q39a+b |             1328.05 |
| TPC-DS Q40    |              997.76 |
| TPC-DS Q41    |                6.44 |
| TPC-DS Q42    |               66.01 |
| TPC-DS Q43    |              215.70 |
| TPC-DS Q44    |              200.79 |
| TPC-DS Q45    |              132.17 |
| TPC-DS Q46    |              184.97 |
| TPC-DS Q47    |              854.18 |
| TPC-DS Q48    |              312.40 |
| TPC-DS Q49    |             1829.13 |
| TPC-DS Q50    |              546.15 |
| TPC-DS Q51    |             2373.02 |
| TPC-DS Q52    |               91.42 |
| TPC-DS Q53    |               88.34 |
| TPC-DS Q54    |               86.02 |
| TPC-DS Q55    |               87.68 |
| TPC-DS Q56    |              131.61 |
| TPC-DS Q57    |              133.72 |
| TPC-DS Q58    |              592.70 |
| TPC-DS Q59    |             1021.67 |
| TPC-DS Q60    |              131.13 |
| TPC-DS Q61    |              157.81 |
| TPC-DS Q62    |              255.67 |
| TPC-DS Q63    |               91.47 |
| TPC-DS Q64    |             4437.89 |
| TPC-DS Q65    |             1042.17 |
| TPC-DS Q66    |              443.92 |
| TPC-DS Q67    |             5805.50 |
| TPC-DS Q68    |              216.00 |
| TPC-DS Q69    |              282.71 |
| TPC-DS Q70    |             1960.61 |
| TPC-DS Q71    |              182.45 |
| TPC-DS Q72    |             1226.11 |
| TPC-DS Q73    |               84.67 |
| TPC-DS Q74    |             2138.86 |
| TPC-DS Q75    |             5713.68 |
| TPC-DS Q76    |              327.81 |
| TPC-DS Q77    |              833.19 |
| TPC-DS Q78    |            12827.66 |
| TPC-DS Q79    |              233.28 |
| TPC-DS Q80    |             9224.26 |
| TPC-DS Q81    |              157.30 |
| TPC-DS Q82    |              469.84 |
| TPC-DS Q83    |               64.69 |
| TPC-DS Q84    |               32.09 |
| TPC-DS Q85    |              300.17 |
| TPC-DS Q86    |              324.64 |
| TPC-DS Q87    |             2946.91 |
| TPC-DS Q88    |              434.57 |
| TPC-DS Q89    |              128.40 |
| TPC-DS Q90    |               72.19 |
| TPC-DS Q91    |               31.62 |
| TPC-DS Q92    |              168.68 |
| TPC-DS Q93    |             2217.33 |
| TPC-DS Q94    |            38106.47 |
| TPC-DS Q95    |           384652.14 |
| TPC-DS Q96    |              759.86 |
| TPC-DS Q97    |             4023.20 |
| TPC-DS Q98    |              503.38 |
| TPC-DS Q99    |              418.69 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      2884.49 |      7.51 |          71.47 |                 71.48 |

### Loading phase: component data generator

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |       235.22 |      0.67 |           0.03 |                  6.65 |

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |     15481.85 |    188.69 |        1021.67 |               1023.88 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        34.52 |      0.43 |           0.37 |                  0.38 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loading.log, expected: series exists only while non-zero)

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

### Perform Benchmark - Power Test

This starts a new instance of MonetDB on the prepared database of the shared disk.
It runs two power tests, one after the other (`-ne 1,1`), and shuts down the DBMS.
This is repeated 2 times (`-nc`).

```bash
bexhoma tpcds \
  -dbms MonetDB \
  -sf 30 \
  -nc 2 \
  -ne 1,1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 14400 \
  -lr 1024Gi \
  -rr 900Gi \
  -rss 3000Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  run &>$LOG_DIR/docs_tpcds_monetdb_sf30_repeated.log
```

### Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_monetdb_sf30_repeated_summary.md" target="_blank" rel="noopener">docs_tpcds_monetdb_sf30_repeated.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=30
* Type: tpcds
* Duration: 3358s 
* Code: 1794675789
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=30) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 14400.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Database is persisted to disk of type nvme and size 3000Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * SUT requests 4 CPU and 900Gi RAM. RAM limit is 1024Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1146783
  * datadisk:76869
  * volume_size:2.9T
  * volume_used:76G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1794675789
* monetdb-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1146788
  * datadisk:75446
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1794675789
* monetdb-1-2-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1039860
  * datadisk:75446
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1794675789
* monetdb-1-2-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1039856
  * datadisk:75446
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1794675789

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MonetDB-1

### Data Parameters of Reused Volumes
* MonetDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1794675789-58f7d97bb7-lq6mv: 0
* bexhoma-sut-monetdb-1-1794675789-55d8dbd698-2d8md: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 2: tpcds (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 2: tpcds (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |   30 |      982.00 |           4.00 |            1.00 |        444.00 |          505.00 |              0 |         0 |             | None           |             0 | False         |              109.98 | True                |
| MonetDB-1-2 |                2 |   30 |      982.00 |           4.00 |            1.00 |        444.00 |          505.00 |              0 |         0 |             | None           |             0 | False         |              109.98 | True                |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 30.00 |               99 |                  99 |        741 |            0.91 |           122877.19 |          14429.15 |          -1 |
| monetdb-1-1-2-1-1 | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |       1 | 30.00 |               99 |                  99 |        696 |            0.78 |           143633.03 |          15362.07 |          -1 |
| monetdb-1-2-1-1-1 | monetdb-1-2-1 | monetdb-1-2-1-1 |                2 |        1 |               1 |       1 | 30.00 |               99 |                  99 |        750 |            0.93 |           120342.74 |          14256.00 |          -1 |
| monetdb-1-2-2-1-1 | monetdb-1-2-2 | monetdb-1-2-2-1 |                2 |        2 |               1 |       1 | 30.00 |               99 |                  99 |        675 |            0.75 |           147519.87 |          15840.00 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        741 |            0.91 |           122877.19 |          14429.15 |          -1 |
| monetdb-1-1-2 | monetdb-1-1-2 |                1 |        2 |               1 |           1 | 30.00 |               99 |                  99 |        696 |            0.78 |           143633.03 |          15362.07 |          -1 |
| monetdb-1-2-1 | monetdb-1-2-1 |                2 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        750 |            0.93 |           120342.74 |          14256.00 |          -1 |
| monetdb-1-2-2 | monetdb-1-2-2 |                2 |        2 |               1 |           1 | 30.00 |               99 |                  99 |        675 |            0.75 |           147519.87 |          15840.00 |          -1 |

#### Query Completion per Phase

| phase         |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:--------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| monetdb-1-1-2 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| monetdb-1-2-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| monetdb-1-2-2 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   monetdb-1-1-1-1-1 |   monetdb-1-1-2-1-1 |   monetdb-1-2-1-1-1 |   monetdb-1-2-2-1-1 |
|:--------------|--------------------:|--------------------:|--------------------:|--------------------:|
| TPC-DS Q1     |             1520.60 |              753.56 |             1498.16 |              467.91 |
| TPC-DS Q2     |             3758.46 |             1948.68 |             3625.04 |             1796.82 |
| TPC-DS Q3     |             2723.16 |              190.88 |             2702.49 |              168.81 |
| TPC-DS Q4     |            25845.06 |            17485.13 |            24105.61 |            16377.45 |
| TPC-DS Q5     |            20301.87 |             1981.75 |            20054.88 |             2173.60 |
| TPC-DS Q6     |              593.81 |              320.14 |              672.25 |              338.27 |
| TPC-DS Q7     |             5552.67 |             1309.56 |             5162.08 |             1084.75 |
| TPC-DS Q8     |             4158.76 |              747.99 |             4152.70 |              371.97 |
| TPC-DS Q9     |             1329.24 |              587.48 |             1303.79 |              583.94 |
| TPC-DS Q10    |            21608.31 |              537.24 |            21097.26 |              515.96 |
| TPC-DS Q11    |             6589.46 |             7585.14 |             6988.97 |             7153.09 |
| TPC-DS Q12    |              232.16 |              189.89 |              247.94 |              165.77 |
| TPC-DS Q13    |              442.69 |              617.10 |              435.04 |              535.71 |
| TPC-DS Q14a+b |            32312.80 |            35696.16 |            31237.11 |            31948.09 |
| TPC-DS Q15    |              177.01 |              138.96 |              191.14 |              129.15 |
| TPC-DS Q16    |            47067.28 |            45981.59 |            46951.03 |            41575.96 |
| TPC-DS Q17    |             3762.53 |             4215.28 |             3834.14 |             3391.36 |
| TPC-DS Q18    |             2237.21 |             2099.96 |             2123.51 |             2192.56 |
| TPC-DS Q19    |              155.34 |              179.92 |              189.81 |              200.37 |
| TPC-DS Q20    |              120.82 |               93.42 |              121.42 |              144.73 |
| TPC-DS Q21    |             2316.78 |              182.44 |             2421.56 |              172.18 |
| TPC-DS Q22    |             1858.85 |             2016.38 |             2041.51 |             1848.72 |
| TPC-DS Q23a+b |            49878.70 |            61993.02 |            56051.27 |            52383.81 |
| TPC-DS Q24a+b |            14649.21 |            16095.33 |            15127.94 |            16586.26 |
| TPC-DS Q25    |             1383.22 |             1846.37 |             1594.89 |             1491.38 |
| TPC-DS Q26    |              166.11 |              179.25 |              172.06 |              181.41 |
| TPC-DS Q27    |             1311.29 |             1450.39 |             1273.45 |             1628.09 |
| TPC-DS Q28    |              612.32 |              662.50 |              628.73 |              879.19 |
| TPC-DS Q29    |             2192.09 |             2940.10 |             2413.55 |             2308.50 |
| TPC-DS Q30    |              100.44 |              114.43 |              115.25 |              114.13 |
| TPC-DS Q31    |             2437.72 |             2371.13 |             2425.69 |             2493.08 |
| TPC-DS Q32    |              182.12 |              139.98 |              130.28 |              421.40 |
| TPC-DS Q33    |              132.50 |              231.94 |              140.73 |              149.80 |
| TPC-DS Q34    |              430.44 |              217.56 |              327.86 |              120.83 |
| TPC-DS Q35    |              791.92 |             1063.91 |              774.33 |             1446.14 |
| TPC-DS Q36    |             1414.32 |             1746.39 |             1592.88 |             1410.01 |
| TPC-DS Q37    |              448.33 |              680.75 |              430.21 |              436.51 |
| TPC-DS Q38    |             2413.78 |             2489.00 |             2584.69 |             2624.39 |
| TPC-DS Q39a+b |             1383.55 |             1409.20 |             1729.79 |             2159.44 |
| TPC-DS Q40    |              417.22 |             1016.85 |              423.98 |              593.51 |
| TPC-DS Q41    |                6.18 |                7.30 |                5.87 |                5.74 |
| TPC-DS Q42    |               93.76 |               68.73 |               88.41 |              112.35 |
| TPC-DS Q43    |              207.46 |              222.41 |              231.86 |              218.55 |
| TPC-DS Q44    |              352.07 |              403.62 |              401.81 |              372.29 |
| TPC-DS Q45    |              131.27 |              138.91 |              133.94 |              138.99 |
| TPC-DS Q46    |              213.27 |              220.86 |              211.85 |              195.68 |
| TPC-DS Q47    |             1240.86 |             1059.69 |              924.56 |              792.56 |
| TPC-DS Q48    |              214.24 |              225.53 |              393.13 |              213.18 |
| TPC-DS Q49    |             4444.50 |             1735.30 |             4520.38 |             1656.74 |
| TPC-DS Q50    |              582.90 |              593.52 |              600.44 |              580.73 |
| TPC-DS Q51    |             2371.52 |             2831.48 |             2547.56 |             2361.98 |
| TPC-DS Q52    |              102.92 |               73.35 |              123.79 |              109.33 |
| TPC-DS Q53    |               98.40 |               93.31 |               88.69 |              229.27 |
| TPC-DS Q54    |               97.63 |               92.47 |               91.61 |               98.68 |
| TPC-DS Q55    |               81.08 |               68.87 |               86.46 |               81.52 |
| TPC-DS Q56    |              217.54 |              111.89 |              150.64 |              152.10 |
| TPC-DS Q57    |              152.03 |              152.60 |              157.61 |              148.39 |
| TPC-DS Q58    |              542.38 |              558.01 |              639.17 |              555.10 |
| TPC-DS Q59    |             1183.12 |             1248.98 |             1208.45 |             1137.45 |
| TPC-DS Q60    |              221.05 |              254.75 |              294.42 |              181.26 |
| TPC-DS Q61    |              205.72 |              172.19 |              170.73 |              163.86 |
| TPC-DS Q62    |              441.41 |              449.45 |              446.59 |              448.58 |
| TPC-DS Q63    |              105.12 |               85.83 |              116.65 |               95.20 |
| TPC-DS Q64    |             5170.89 |             5102.78 |             5372.41 |             5114.38 |
| TPC-DS Q65    |             1089.41 |             1125.06 |             1204.28 |             1043.89 |
| TPC-DS Q66    |             1036.22 |             1085.61 |             1073.02 |             1061.04 |
| TPC-DS Q67    |             5712.38 |             6107.77 |             6251.74 |             5468.87 |
| TPC-DS Q68    |              254.93 |              212.22 |              200.91 |              225.53 |
| TPC-DS Q69    |              461.56 |              371.55 |              543.80 |              421.79 |
| TPC-DS Q70    |             2122.33 |             1439.39 |             1626.18 |             1554.81 |
| TPC-DS Q71    |              372.23 |              537.98 |              337.75 |              493.50 |
| TPC-DS Q72    |             2346.87 |             2464.61 |             2382.61 |             2777.02 |
| TPC-DS Q73    |              103.16 |              171.76 |               87.80 |               95.35 |
| TPC-DS Q74    |             7558.86 |             8550.53 |             7605.52 |             7501.90 |
| TPC-DS Q75    |             6737.16 |             7615.59 |             7033.98 |             6548.43 |
| TPC-DS Q76    |             6326.69 |             7838.32 |             8260.98 |             6575.71 |
| TPC-DS Q77    |             1394.09 |             1281.33 |             1226.03 |             1566.90 |
| TPC-DS Q78    |            13276.33 |            13835.36 |            12753.75 |            14010.89 |
| TPC-DS Q79    |              265.66 |              295.49 |              259.84 |              289.90 |
| TPC-DS Q80    |             7541.55 |             7740.58 |             7504.16 |             7849.43 |
| TPC-DS Q81    |              155.97 |              156.98 |              159.04 |              155.56 |
| TPC-DS Q82    |              462.88 |              455.52 |              490.10 |              455.57 |
| TPC-DS Q83    |              288.23 |              278.88 |              285.50 |              201.57 |
| TPC-DS Q84    |               58.34 |               61.31 |               52.46 |               47.86 |
| TPC-DS Q85    |              303.12 |              299.01 |              695.28 |              314.54 |
| TPC-DS Q86    |              329.24 |              317.55 |              313.71 |              313.37 |
| TPC-DS Q87    |             2738.01 |             3330.32 |             2996.22 |             2718.96 |
| TPC-DS Q88    |              706.70 |              426.35 |              652.17 |              578.13 |
| TPC-DS Q89    |              137.03 |              151.43 |              129.41 |              173.22 |
| TPC-DS Q90    |               81.87 |              121.48 |               81.53 |              135.53 |
| TPC-DS Q91    |               38.84 |               45.03 |               35.73 |               39.28 |
| TPC-DS Q92    |              144.41 |              116.30 |              149.41 |              162.65 |
| TPC-DS Q93    |             1937.97 |             2261.58 |             2154.32 |             1902.04 |
| TPC-DS Q94    |            38996.86 |            40529.56 |            40799.57 |            40739.16 |
| TPC-DS Q95    |           322376.48 |           316144.33 |           322758.33 |           325531.95 |
| TPC-DS Q96    |              810.56 |              753.61 |              749.64 |              794.59 |
| TPC-DS Q97    |             3951.48 |             4109.38 |             4430.46 |             4210.38 |
| TPC-DS Q98    |              469.63 |              472.74 |              482.24 |              476.22 |
| TPC-DS Q99    |              399.97 |              552.01 |              394.35 |              405.42 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |     11291.41 |    166.87 |        1011.30 |               1023.68 |
| monetdb-1-1-2-1 |     10819.98 |    112.99 |         996.47 |               1023.95 |
| monetdb-1-2-1-1 |     10588.06 |    148.43 |         959.05 |               1023.97 |
| monetdb-1-2-2-1 |     10924.01 |    149.65 |         977.58 |               1023.99 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        31.82 |      0.18 |           0.36 |                  0.36 |
| monetdb-1-1-2-1 |        33.89 |      0.15 |           0.37 |                  0.38 |
| monetdb-1-2-1-1 |        34.05 |      0.46 |           0.38 |                  0.38 |
| monetdb-1-2-2-1 |        32.99 |      0.54 |           0.40 |                  0.40 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-2-1-1 (bexhoma-metrics-monetdb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-2-1-1 (bexhoma-metrics-monetdb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-2-2-1 (bexhoma-metrics-monetdb-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-2-2-1 (bexhoma-metrics-monetdb-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MonetDB-1)
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
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

### Perform Benchmark - Throughput Test

This starts a new instance of MonetDB on the prepared database of the shared disk.
It runs two power tests, one after the other, then a throughput test with 3 parallel drivers (`-ne 1,1,3`), and shuts down the DBMS.


```bash
bexhoma tpcds \
  -dbms MonetDB \
  -sf 30 \
  -nc 1 \
  -ne 1,1,3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 14400 \
  -lr 1024Gi \
  -rr 900Gi \
  -rss 3000Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  run &>$LOG_DIR/docs_tpcds_monetdb_sf30_throughput.log
```

### Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_monetdb_sf30_throughput_summary.md" target="_blank" rel="noopener">docs_tpcds_monetdb_sf30_throughput.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=30
* Type: tpcds
* Duration: 3957s 
* Code: 1794679292
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=30) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 14400.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Database is persisted to disk of type nvme and size 3000Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 1, 3] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * SUT requests 4 CPU and 900Gi RAM. RAM limit is 1024Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1041487
  * datadisk:75446
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1794679292
* monetdb-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1041501
  * datadisk:75446
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1794679292
* monetdb-1-1-3-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1041507
  * datadisk:75446
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1794679292
* monetdb-1-1-3-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1041507
  * datadisk:75446
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1794679292
* monetdb-1-1-3-1-3 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1041507
  * datadisk:75446
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1794679292

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MonetDB-1

### Data Parameters of Reused Volumes
* MonetDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1794679292-845c86f48c-ht4pr: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 3: tpcds (3 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 3: tpcds (3 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |   30 |      982.00 |           4.00 |            1.00 |        444.00 |          505.00 |              0 |         0 |             | None           |             0 | False         |              109.98 | True                |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 30.00 |               99 |                  99 |        814 |            0.88 |           126416.63 |          13135.14 |          -1 |
| monetdb-1-1-2-1-1 | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |       1 | 30.00 |               99 |                  99 |        726 |            0.74 |           151474.64 |          14727.27 |          -1 |
| monetdb-1-1-3-1-1 | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |       1 | 30.00 |               99 |                  99 |       1140 |            1.17 |            94355.48 |           9378.95 |          -1 |
| monetdb-1-1-3-1-2 | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |       2 | 30.00 |               99 |                  99 |       2040 |            0.88 |           128193.48 |           5241.18 |          -1 |
| monetdb-1-1-3-1-3 | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |       3 | 30.00 |               99 |                  99 |       2084 |            0.87 |           129387.12 |           5130.52 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        814 |            0.88 |           126416.63 |          13135.14 |          -1 |
| monetdb-1-1-2 | monetdb-1-1-2 |                1 |        2 |               1 |           1 | 30.00 |               99 |                  99 |        726 |            0.74 |           151474.64 |          14727.27 |          -1 |
| monetdb-1-1-3 | monetdb-1-1-3 |                1 |        3 |               1 |           3 | 30.00 |              297 |                 297 |       2084 |            0.96 |           116102.45 |          15391.55 |          -1 |

#### Query Completion per Phase

| phase         |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:--------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| monetdb-1-1-2 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| monetdb-1-1-3 |      3 | 3/3         | 3/3         | 3/3         | 3/3         | 3/3         | 3/3         | 3/3         | 3/3         | 3/3         | 3/3          | 3/3          | 3/3          | 3/3          | 3/3             | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3             | 3/3             | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3             | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   monetdb-1-1-1-1-1 |   monetdb-1-1-2-1-1 |   monetdb-1-1-3-1-1 |   monetdb-1-1-3-1-2 |   monetdb-1-1-3-1-3 |
|:--------------|--------------------:|--------------------:|--------------------:|--------------------:|--------------------:|
| TPC-DS Q1     |             1149.39 |              222.39 |              331.54 |              204.77 |              180.88 |
| TPC-DS Q2     |             4098.29 |             2399.26 |             3992.24 |             4240.45 |             3579.75 |
| TPC-DS Q3     |             2526.82 |              188.52 |              130.48 |              621.85 |              261.11 |
| TPC-DS Q4     |            26296.42 |            17066.69 |            20358.81 |            17489.68 |            21436.64 |
| TPC-DS Q5     |            17989.41 |             2683.29 |             2723.71 |             5092.41 |             1888.42 |
| TPC-DS Q6     |              620.89 |              313.44 |             1204.53 |             1499.28 |             1313.88 |
| TPC-DS Q7     |             4123.94 |              957.50 |             1067.64 |              594.84 |             1233.18 |
| TPC-DS Q8     |             3667.21 |              360.98 |              412.09 |              421.35 |              408.80 |
| TPC-DS Q9     |             1253.40 |              572.36 |             1534.41 |             1741.65 |             1559.92 |
| TPC-DS Q10    |            20032.75 |              541.81 |              641.84 |              371.83 |              636.32 |
| TPC-DS Q11    |             7260.67 |             6633.16 |             7714.30 |             7418.39 |             8634.37 |
| TPC-DS Q12    |              243.21 |              165.07 |              709.46 |              436.30 |               94.10 |
| TPC-DS Q13    |              650.36 |              523.97 |              281.67 |              984.78 |              323.06 |
| TPC-DS Q14a+b |            36384.77 |            34542.22 |            36824.16 |            37557.80 |            36830.24 |
| TPC-DS Q15    |              175.12 |              130.80 |              291.93 |              170.68 |              261.53 |
| TPC-DS Q16    |            49407.70 |            43480.53 |            41105.25 |           152446.03 |           141309.73 |
| TPC-DS Q17    |             4199.07 |             3349.20 |             3935.52 |             2737.31 |             6194.97 |
| TPC-DS Q18    |             2140.05 |             2219.25 |             3168.71 |              972.44 |             3366.62 |
| TPC-DS Q19    |              192.39 |              166.39 |             6520.34 |              254.66 |             1483.46 |
| TPC-DS Q20    |              140.34 |              109.19 |             7300.27 |              135.39 |              120.71 |
| TPC-DS Q21    |             2206.38 |              165.48 |             4169.25 |              117.18 |              103.55 |
| TPC-DS Q22    |             1851.06 |             2215.58 |             4936.64 |             1178.68 |             1270.64 |
| TPC-DS Q23a+b |            53875.75 |            49119.01 |            99026.34 |            58936.57 |            55950.63 |
| TPC-DS Q24a+b |            14693.95 |            16385.50 |             9672.09 |             8123.41 |             9392.61 |
| TPC-DS Q25    |             2460.11 |             2276.47 |             3645.82 |             3663.49 |             3698.39 |
| TPC-DS Q26    |              164.92 |              229.50 |              185.54 |              313.05 |              222.76 |
| TPC-DS Q27    |             1462.95 |             1384.73 |             1862.83 |             1823.32 |             1751.79 |
| TPC-DS Q28    |              832.85 |              645.94 |              708.73 |              621.98 |             1292.59 |
| TPC-DS Q29    |             2192.46 |             2994.26 |             3074.08 |             2677.72 |             3780.36 |
| TPC-DS Q30    |              103.14 |              113.68 |              110.50 |              145.95 |              494.98 |
| TPC-DS Q31    |             2286.92 |             2171.23 |             2198.14 |             1683.16 |             2773.80 |
| TPC-DS Q32    |              184.83 |              168.96 |              107.59 |              237.45 |              180.25 |
| TPC-DS Q33    |              146.96 |              240.13 |              132.24 |              118.34 |              118.60 |
| TPC-DS Q34    |              322.31 |              195.76 |              239.90 |              105.24 |              109.71 |
| TPC-DS Q35    |              802.47 |              824.29 |              714.01 |              730.26 |             1047.36 |
| TPC-DS Q36    |             1431.24 |             1341.62 |             1334.82 |             1684.14 |             1387.60 |
| TPC-DS Q37    |              427.25 |              432.61 |              396.00 |              524.16 |              413.31 |
| TPC-DS Q38    |             3089.72 |             2735.95 |             2478.05 |             2866.13 |             2967.04 |
| TPC-DS Q39a+b |             1193.56 |             1184.14 |             1303.47 |             1294.36 |             1132.69 |
| TPC-DS Q40    |              414.58 |              594.11 |              695.24 |              426.67 |              327.49 |
| TPC-DS Q41    |                6.57 |                6.05 |                5.78 |                5.09 |                5.57 |
| TPC-DS Q42    |              118.55 |              114.15 |               87.99 |               68.37 |               88.44 |
| TPC-DS Q43    |              213.76 |              209.26 |              202.80 |              221.90 |              239.79 |
| TPC-DS Q44    |              247.27 |              352.07 |              225.85 |              244.24 |              239.87 |
| TPC-DS Q45    |              132.07 |              173.90 |              128.58 |              141.56 |              177.45 |
| TPC-DS Q46    |              233.33 |              199.43 |              184.22 |              197.99 |              208.74 |
| TPC-DS Q47    |              941.51 |              892.04 |             1020.62 |             1048.30 |             1046.56 |
| TPC-DS Q48    |              218.16 |              209.70 |              379.98 |              215.13 |              384.65 |
| TPC-DS Q49    |             4295.28 |             1634.39 |             1663.86 |             1566.72 |             1056.68 |
| TPC-DS Q50    |              553.82 |              573.99 |              600.55 |              728.85 |              606.64 |
| TPC-DS Q51    |             2751.18 |             2560.43 |             2940.82 |             3133.39 |             2902.03 |
| TPC-DS Q52    |              122.94 |              113.21 |              176.24 |              115.45 |               85.41 |
| TPC-DS Q53    |               96.48 |               91.63 |               91.27 |              136.64 |              173.43 |
| TPC-DS Q54    |               88.46 |               91.55 |              103.09 |               92.38 |              220.84 |
| TPC-DS Q55    |               72.72 |               87.09 |              567.48 |               78.31 |               94.43 |
| TPC-DS Q56    |              152.63 |              123.40 |              754.51 |              106.98 |              139.82 |
| TPC-DS Q57    |              146.16 |              138.90 |             1652.59 |              161.77 |              203.87 |
| TPC-DS Q58    |              645.67 |              631.84 |             1497.06 |              534.49 |              575.88 |
| TPC-DS Q59    |             1298.21 |             1145.81 |             2101.68 |              639.85 |              819.59 |
| TPC-DS Q60    |              169.81 |              186.76 |             1488.67 |              382.25 |              276.40 |
| TPC-DS Q61    |              167.18 |              171.89 |              412.90 |              344.60 |              162.94 |
| TPC-DS Q62    |              442.43 |              445.91 |             3505.07 |              322.26 |              301.99 |
| TPC-DS Q63    |               93.14 |               91.62 |               95.17 |              120.60 |              115.30 |
| TPC-DS Q64    |             4895.80 |             5521.34 |             7788.78 |             2337.21 |             2794.97 |
| TPC-DS Q65    |             1194.72 |             1111.47 |             2156.08 |             1563.49 |             1164.16 |
| TPC-DS Q66    |             1229.27 |             1300.59 |             1236.84 |              341.30 |              379.16 |
| TPC-DS Q67    |             6008.78 |             6239.05 |             6463.88 |             7729.61 |             6680.92 |
| TPC-DS Q68    |              230.20 |              219.54 |              237.51 |              308.86 |              209.71 |
| TPC-DS Q69    |              373.81 |              394.64 |              414.44 |              245.30 |              319.98 |
| TPC-DS Q70    |             1363.06 |             2301.16 |             1910.34 |             1392.28 |             2254.23 |
| TPC-DS Q71    |              355.79 |              501.88 |              499.70 |              180.92 |              198.46 |
| TPC-DS Q72    |             2287.26 |             2440.33 |             2822.94 |             1055.79 |             1492.78 |
| TPC-DS Q73    |               90.23 |               93.17 |               96.79 |              104.45 |               99.08 |
| TPC-DS Q74    |             1842.48 |             2297.63 |             2523.29 |             3095.26 |             2059.40 |
| TPC-DS Q75    |             7530.87 |             6224.35 |             7718.65 |             6935.77 |             7339.98 |
| TPC-DS Q76    |             2722.48 |             3797.37 |             3394.68 |              168.79 |              192.97 |
| TPC-DS Q77    |             1164.21 |             1260.77 |             1225.51 |              823.67 |             1394.25 |
| TPC-DS Q78    |            13008.62 |            13408.43 |            15091.84 |            15567.01 |            15777.29 |
| TPC-DS Q79    |              204.67 |              222.12 |              213.64 |              222.56 |              251.22 |
| TPC-DS Q80    |             7624.48 |             8157.56 |            11548.96 |             9329.94 |             9420.39 |
| TPC-DS Q81    |              138.62 |              187.36 |              152.87 |              140.64 |              179.04 |
| TPC-DS Q82    |              519.76 |              520.54 |              647.44 |              464.95 |              702.05 |
| TPC-DS Q83    |              240.25 |              279.73 |              236.86 |               41.80 |               40.49 |
| TPC-DS Q84    |               55.48 |               91.26 |               45.11 |               37.23 |               37.02 |
| TPC-DS Q85    |              303.62 |              297.09 |              331.93 |              437.14 |              502.20 |
| TPC-DS Q86    |              311.72 |              417.34 |              342.05 |              568.14 |              271.23 |
| TPC-DS Q87    |             3142.68 |             3180.62 |             3298.18 |             4526.51 |             3766.11 |
| TPC-DS Q88    |              636.79 |              415.95 |             1239.84 |             4593.62 |             7244.82 |
| TPC-DS Q89    |              149.41 |              126.76 |              238.75 |             4866.10 |             1182.02 |
| TPC-DS Q90    |               80.49 |              122.18 |              145.12 |             5308.67 |             2641.44 |
| TPC-DS Q91    |               42.45 |               34.97 |               73.03 |              572.01 |             1460.31 |
| TPC-DS Q92    |              144.83 |              152.49 |              161.55 |             4552.95 |             7583.19 |
| TPC-DS Q93    |             2381.77 |             2114.31 |             2279.27 |             2539.06 |             5488.89 |
| TPC-DS Q94    |            36115.61 |            39463.79 |            40896.94 |           111356.87 |            76512.86 |
| TPC-DS Q95    |           399319.62 |           381848.61 |           621033.50 |          1482120.49 |          1566279.01 |
| TPC-DS Q96    |              768.22 |              747.25 |            30167.79 |              935.21 |               42.34 |
| TPC-DS Q97    |             4009.56 |             4133.86 |            22779.51 |             6489.72 |             3723.90 |
| TPC-DS Q98    |              472.44 |              568.24 |            17245.83 |              579.22 |              150.04 |
| TPC-DS Q99    |              422.85 |              428.18 |            12237.65 |              497.36 |              254.88 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |     14080.86 |    166.90 |         979.71 |               1023.95 |
| monetdb-1-1-2-1 |     13123.52 |    188.05 |         967.96 |               1023.98 |
| monetdb-1-1-3-1 |     41891.04 |    187.08 |        1014.89 |               1024.00 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        32.78 |      0.26 |           0.35 |                  0.36 |
| monetdb-1-1-2-1 |        30.22 |      0.17 |           0.36 |                  0.37 |
| monetdb-1-1-3-1 |        99.70 |      0.65 |           0.38 |                  0.38 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-3-1 (bexhoma-metrics-monetdb-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-3-1 (bexhoma-metrics-monetdb-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MonetDB-1)
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
 TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
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


## SSB

The Star Schema Benchmark runs on MonetDB, too, see [Example: SSB](Example-SSB.md).
