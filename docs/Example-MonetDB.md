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

For performing the experiment we can run the [tpch file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpch.py).

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
* starts 8 loader pods (`-nlp`) with 8 threads each (`-nlt`)
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
* Duration: 293s 
* Code: 1793713047
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
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
  * RAM:540590821376
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-137-generic
  * node:cl-worker23
  * disk:1289451
  * datadisk:2937
  * cpu_list:0-95
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793713047

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1793713047-7468bdc589-5fpwp: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |    1 |       69.00 |           0.00 |           29.00 |         11.00 |           16.00 |              8 |           0 |             | None           |             0 | False         |               52.17 | False               |

### Benchmarking

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| monetdb-1-1-1-1-1 | MonetDB-1       | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         10 |            0.07 |            58983.69 |           7920.00 |          -1 | monetdb-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         10 |            0.07 |            58983.69 |           7920.00 |          -1 |

#### Query Completion per Phase

| phase         |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:--------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   monetdb-1-1-1-1-1 |
|:----------------------------------------------------|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |              747.37 |
| Minimum Cost Supplier Query (TPC-H Q2)              |               17.68 |
| Shipping Priority (TPC-H Q3)                        |               51.82 |
| Order Priority Checking Query (TPC-H Q4)            |              103.65 |
| Local Supplier Volume (TPC-H Q5)                    |               41.57 |
| Forecasting Revenue Change (TPC-H Q6)               |               15.97 |
| Volume Shipping Query (TPC-H Q7)                    |               43.86 |
| National Market Share (TPC-H Q8)                    |              248.23 |
| Product Type Profit Measure (TPC-H Q9)              |               48.59 |
| Returned Item Reporting Query (TPC-H Q10)           |               80.83 |
| Important Stock Identification (TPC-H Q11)          |               14.32 |
| Shipping Modes and Order Priority (TPC-H Q12)       |               33.29 |
| Customer Distribution (TPC-H Q13)                   |              292.59 |
| Promotion Effect Query (TPC-H Q14)                  |               24.20 |
| Top Supplier Query (TPC-H Q15)                      |               22.29 |
| Parts/Supplier Relationship (TPC-H Q16)             |               46.39 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               34.04 |
| Large Volume Customer (TPC-H Q18)                   |              124.60 |
| Discounted Revenue (TPC-H Q19)                      |               52.11 |
| Potential Part Promotion (TPC-H Q20)                |               34.56 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |             1299.22 |
| Global Sales Opportunity Query (TPC-H Q22)          |               27.47 |

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

To see the summary again you can simply call `bexhoma summary -e <code>` with the experiment code.

Results are transformed into pandas DataFrames and can be inspected in detail.
See for example the [Jupyter notebooks](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/notebooks/), in particular [Collector-TPC-H.ipynb](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/notebooks/Collector-TPC-H.ipynb).

You can connect to an evaluation server locally by `bexhoma jupyter`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888


## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).
Metrics are sampled every few seconds, so the benchmarking phase should take at least a minute.
The 22 queries take about 270 s at SF=100, so this run uses SF=30 (`-sf`), with 256 GiB RAM.
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
* Duration: 1429s 
* Code: 1793713358
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=30) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 3600.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
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
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:848663
  * datadisk:58896
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793713358

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1793713358-569b579f7d-4qqh7: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |   30 |      999.00 |           1.00 |           22.00 |        503.00 |          468.00 |              8 |           0 |             | None           |             0 | False         |              108.11 | False               |

### Benchmarking

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| monetdb-1-1-1-1-1 | MonetDB-1       | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               22 |                  22 |        237 |            1.55 |            76288.91 |          10025.32 |          -1 | monetdb-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               22 |                  22 |        237 |            1.55 |            76288.91 |          10025.32 |          -1 |

#### Query Completion per Phase

| phase         |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:--------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   monetdb-1-1-1-1-1 |
|:----------------------------------------------------|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |            13216.42 |
| Minimum Cost Supplier Query (TPC-H Q2)              |              432.39 |
| Shipping Priority (TPC-H Q3)                        |             1101.31 |
| Order Priority Checking Query (TPC-H Q4)            |             2151.00 |
| Local Supplier Volume (TPC-H Q5)                    |              824.25 |
| Forecasting Revenue Change (TPC-H Q6)               |              582.26 |
| Volume Shipping Query (TPC-H Q7)                    |             1376.09 |
| National Market Share (TPC-H Q8)                    |             6524.04 |
| Product Type Profit Measure (TPC-H Q9)              |             1176.40 |
| Returned Item Reporting Query (TPC-H Q10)           |             2077.53 |
| Important Stock Identification (TPC-H Q11)          |              214.75 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             1449.14 |
| Customer Distribution (TPC-H Q13)                   |             5355.52 |
| Promotion Effect Query (TPC-H Q14)                  |              638.89 |
| Top Supplier Query (TPC-H Q15)                      |              426.54 |
| Parts/Supplier Relationship (TPC-H Q16)             |              996.61 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |              724.32 |
| Large Volume Customer (TPC-H Q18)                   |             1993.88 |
| Discounted Revenue (TPC-H Q19)                      |              366.72 |
| Potential Part Promotion (TPC-H Q20)                |              604.18 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |           186033.53 |
| Global Sales Opportunity Query (TPC-H Q22)          |              545.39 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      2280.73 |      4.63 |          57.91 |                 59.25 |

### Loading phase: component data generator

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |       488.18 |      1.26 |           0.01 |                  3.96 |

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |       385.24 |      3.88 |          77.52 |                 78.86 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        19.78 |      0.23 |           0.37 |                  0.37 |

### Missing Monitoring Metrics
* CPU Utilization [CPUs] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loader.log, expected: series exists only while non-zero)

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


## Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.
With repetitions (`-nc`), `-rsr` removes an existing volume only before the first repetition and later repetitions reuse it without loading; `-rsrp` removes it before every repetition. See [Concepts](Concepts.html).

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
* Duration: 494s 
* Code: 1793715774
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
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
  * RAM:540590792704
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-146-generic
  * node:cl-worker25
  * disk:131939
  * datadisk:2937
  * volume_size:49G
  * volume_used:2.9G
  * cpu_list:0-95
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793715774
* monetdb-1-2-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:540590792704
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-146-generic
  * node:cl-worker25
  * disk:131779
  * datadisk:1417
  * volume_size:49G
  * volume_used:1.4G
  * cpu_list:0-95
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793715774

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MonetDB-1-2

### Data Parameters of Reused Volumes
* MonetDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1793715774-58d649c877-bsnxz: 0
* bexhoma-sut-monetdb-1-1793715774-7d97987947-7wbt8: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 1: tpch (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 1: tpch (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |    1 |       57.00 |           1.00 |           27.00 |          9.00 |           16.00 |              8 |           0 |             | None           |             0 | False         |               63.16 | False               |
| MonetDB-1-2 |                2 |    1 |       57.00 |           1.00 |           27.00 |          9.00 |           16.00 |              8 |           0 |             | None           |             0 | False         |               63.16 | True                |

### Benchmarking

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| monetdb-1-1-1-1-1 | MonetDB-1       | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         21 |            0.08 |            57485.56 |           3771.43 |          -1 | monetdb-1-1-1-1-1 |
| monetdb-1-2-1-1-1 | MonetDB-1       | monetdb-1-2-1 | monetdb-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         34 |            0.07 |            65513.36 |           2329.41 |          -1 | monetdb-1-2-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         21 |            0.08 |            57485.56 |           3771.43 |          -1 |
| monetdb-1-2-1 | monetdb-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         34 |            0.07 |            65513.36 |           2329.41 |          -1 |

#### Query Completion per Phase

| phase         |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:--------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| monetdb-1-2-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   monetdb-1-1-1-1-1 |   monetdb-1-2-1-1-1 |
|:----------------------------------------------------|--------------------:|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |              718.36 |              724.21 |
| Minimum Cost Supplier Query (TPC-H Q2)              |               19.09 |               17.87 |
| Shipping Priority (TPC-H Q3)                        |               53.56 |               58.25 |
| Order Priority Checking Query (TPC-H Q4)            |              108.71 |              105.18 |
| Local Supplier Volume (TPC-H Q5)                    |               42.27 |               36.60 |
| Forecasting Revenue Change (TPC-H Q6)               |               17.90 |               13.50 |
| Volume Shipping Query (TPC-H Q7)                    |               48.39 |               39.39 |
| National Market Share (TPC-H Q8)                    |              284.56 |              244.40 |
| Product Type Profit Measure (TPC-H Q9)              |               48.88 |               42.33 |
| Returned Item Reporting Query (TPC-H Q10)           |               84.10 |               84.62 |
| Important Stock Identification (TPC-H Q11)          |               16.10 |                8.80 |
| Shipping Modes and Order Priority (TPC-H Q12)       |               34.24 |               27.31 |
| Customer Distribution (TPC-H Q13)                   |              274.31 |              248.81 |
| Promotion Effect Query (TPC-H Q14)                  |               23.65 |               18.06 |
| Top Supplier Query (TPC-H Q15)                      |               21.66 |               18.59 |
| Parts/Supplier Relationship (TPC-H Q16)             |               43.73 |               45.11 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               38.50 |               32.12 |
| Large Volume Customer (TPC-H Q18)                   |              151.81 |              119.45 |
| Discounted Revenue (TPC-H Q19)                      |               56.85 |               46.90 |
| Potential Part Promotion (TPC-H Q20)                |               28.90 |               33.11 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |             1165.84 |             1122.92 |
| Global Sales Opportunity Query (TPC-H Q22)          |               26.04 |               23.26 |

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


## Refresh Stream

`-xrs N` runs the TPC-H refresh functions RF1 (insert new orders) and RF2 (delete old orders) as an additional job next to the query streams, see [TPC-H](Example-TPC-H.md#refresh-stream).
For MonetDB, the loader image applies RF1 with `COPY ... FROM STDIN` in `mclient` and RF2 in one piped `mclient` session, so the temporary table lives across the statements.
Here, 3 query streams run in parallel with a refresh stream of 3 RF1+RF2 pairs.

```bash
bexhoma tpch \
  -dbms MonetDB \
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
  -lc 16 \
  -rc 16 \
  -lr 64Gi \
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
* Duration: 336s 
* Code: 1793810055
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
  * disk:608609
  * datadisk:2936
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793810055
* monetdb-1-1-1-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081742753792
  * CPU:AMD EPYC 7502 32-Core Processor
  * Cores:128
  * host:6.8.0-146-generic
  * node:cl-worker29
  * disk:608609
  * datadisk:2936
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793810055
* monetdb-1-1-1-1-3 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081742753792
  * CPU:AMD EPYC 7502 32-Core Processor
  * Cores:128
  * host:6.8.0-146-generic
  * node:cl-worker29
  * disk:608609
  * datadisk:2936
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793810055

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1793810055-6f96ff747c-7jgdr: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |    1 |       65.00 |           2.00 |           25.00 |         14.00 |           18.00 |              8 |           0 |             | None           |             0 | False         |               55.38 | False               |

### Benchmarking

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| monetdb-1-1-1-1-1 | MonetDB-1       | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         16 |            0.11 |            32362.35 |           4950.00 |          -1 | monetdb-1-1-1-1-1 |
| monetdb-1-1-1-1-2 | MonetDB-1       | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         12 |            0.09 |            39335.00 |           6600.00 |          -1 | monetdb-1-1-1-1-2 |
| monetdb-1-1-1-1-3 | MonetDB-1       | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         12 |            0.11 |            32837.04 |           6600.00 |          -1 | monetdb-1-1-1-1-3 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           3 | 1.00 |               66 |                  66 |         16 |            0.10 |            34705.19 |          14850.00 |          -1 |

#### Query Completion per Phase

| phase         |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:--------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| monetdb-1-1-1 |      3 | 3/3                                 | 3/3                                      | 3/3                            | 3/3                                        | 3/3                                | 3/3                                     | 3/3                                | 3/3                                | 3/3                                      | 3/3                                         | 3/3                                          | 3/3                                             | 3/3                                 | 3/3                                  | 3/3                              | 3/3                                       | 3/3                                        | 3/3                                 | 3/3                              | 3/3                                    | 3/3                                                   | 3/3                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### tpch_refresh

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count | benchmark_begin     | benchmark_end       |   benchmark_duration |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|:--------------------|:--------------------|---------------------:|
| monetdb-1-1-1-2-1 | monetdb-1-1-1 | monetdb-1-1-1-2 |                1 |        1 |               2 |           1 | 2026-11-04 17:38:44 | 2026-11-04 17:38:46 |                    2 |

### Latency of Timer Execution [ms]
| Queries                                             |   monetdb-1-1-1-1-1 |   monetdb-1-1-1-1-2 |   monetdb-1-1-1-1-3 |
|:----------------------------------------------------|--------------------:|--------------------:|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |             1772.03 |             1722.57 |             1551.41 |
| Minimum Cost Supplier Query (TPC-H Q2)              |               24.32 |               34.54 |               77.87 |
| Shipping Priority (TPC-H Q3)                        |               98.14 |               88.43 |               89.54 |
| Order Priority Checking Query (TPC-H Q4)            |              136.73 |              138.53 |              169.95 |
| Local Supplier Volume (TPC-H Q5)                    |               69.67 |               63.91 |               61.95 |
| Forecasting Revenue Change (TPC-H Q6)               |               30.09 |               25.18 |               25.82 |
| Volume Shipping Query (TPC-H Q7)                    |               66.06 |               67.72 |               73.05 |
| National Market Share (TPC-H Q8)                    |              206.25 |              206.99 |              326.55 |
| Product Type Profit Measure (TPC-H Q9)              |               76.53 |               97.02 |               75.02 |
| Returned Item Reporting Query (TPC-H Q10)           |              175.81 |              144.31 |              148.64 |
| Important Stock Identification (TPC-H Q11)          |               22.17 |               20.95 |               18.15 |
| Shipping Modes and Order Priority (TPC-H Q12)       |               49.40 |               46.98 |               50.53 |
| Customer Distribution (TPC-H Q13)                   |              798.53 |              353.84 |              371.49 |
| Promotion Effect Query (TPC-H Q14)                  |              605.32 |               31.07 |               36.80 |
| Top Supplier Query (TPC-H Q15)                      |               49.13 |               32.31 |               33.75 |
| Parts/Supplier Relationship (TPC-H Q16)             |               96.60 |               87.62 |               88.12 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               63.18 |               56.37 |               49.67 |
| Large Volume Customer (TPC-H Q18)                   |              178.61 |              196.04 |              146.40 |
| Discounted Revenue (TPC-H Q19)                      |               67.10 |               61.99 |               98.97 |
| Potential Part Promotion (TPC-H Q20)                |               34.72 |               31.03 |               46.48 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |             1766.20 |             2401.45 |             1817.58 |
| Global Sales Opportunity Query (TPC-H Q22)          |               40.19 |               39.56 |              426.25 |

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
'MonetDB': {
    'abbreviation': 'mo',
    'loadData': "cd /home/monetdb;printf 'user=monetdb\npassword=monetdb\n' > .monetdb;mclient demo < {scriptname}",
    'template': {
        'version': '11.37.11',
        'alias': 'Columnwise',
        'docker_alias': 'Columnwise',
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

At first we generate TPC-H data at SF=100 (`-sf`) with 8 parallel generators (`-nlp`).
The generated data is stored at the shared disk `data`.
Moreover the data is loaded into an instance of MonetDB using again 8 parallel loaders.
Afterwards the script creates contraints (`-xic`) and indexes (`-xii`) and updates table statistics (`-xis`).
The database is located in another shared disk of storageClass shared (`-rst`) and of size 1000Gi (`-rss`).

The script also runs a power test (`-ne` set to 1) with timeout 1200s (`-t`) and data transfer activated (`-xdt`) once (`-nc` set to 1).
To avoid conflicts with other experiments we set a maximum of 1 DBMS per time (`-ms`).
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
  -lr 256Gi \
  -rr 256Gi \
  -rss 1000Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_monetdb_sf100.log
```

### Status Data Disk

You can watch the status of the data disk via `bexhoma data`.

In the following example output we see we have generated TPC-H at SF=100 using 8 generators.
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

In the following example output we see all components of bexhoma are up and running.
The cluster stores a MonetDB database corresponding to TPC-H of SF=100.
The disk is of storageClass shared and of size 1000Gi and 210G of that space is used.
It took about 7000s to build this database.
Currently no DBMS is running.

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
* Duration: 4626s 
* Code: 1792696012
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=100) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 3600.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.8.
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
  * disk:400113
  * datadisk:192979
  * volume_size:984G
  * volume_used:189G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792696012

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1792696012-585f4496f7-tjp58: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |  100 |     4049.00 |           3.00 |          625.00 |       1516.00 |         1903.00 |              8 |           0 |             | None           |             0 | False         |               88.91 | False               |

### Benchmarking

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| monetdb-1-1-1-1-1 | MonetDB-1       | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               22 |                  22 |        271 |            5.50 |            69656.77 |          29225.09 |          -1 | monetdb-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               22 |                  22 |        271 |            5.50 |            69656.77 |          29225.09 |          -1 |

#### Query Completion per Phase

| phase         |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:--------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   monetdb-1-1-1-1-1 |
|:----------------------------------------------------|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |            59178.56 |
| Minimum Cost Supplier Query (TPC-H Q2)              |              767.62 |
| Shipping Priority (TPC-H Q3)                        |            10389.37 |
| Order Priority Checking Query (TPC-H Q4)            |            10243.12 |
| Local Supplier Volume (TPC-H Q5)                    |             4531.42 |
| Forecasting Revenue Change (TPC-H Q6)               |             2102.39 |
| Volume Shipping Query (TPC-H Q7)                    |             8552.25 |
| National Market Share (TPC-H Q8)                    |            16194.20 |
| Product Type Profit Measure (TPC-H Q9)              |             8322.72 |
| Returned Item Reporting Query (TPC-H Q10)           |             8067.26 |
| Important Stock Identification (TPC-H Q11)          |             1037.99 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             1732.52 |
| Customer Distribution (TPC-H Q13)                   |            29117.39 |
| Promotion Effect Query (TPC-H Q14)                  |              876.19 |
| Top Supplier Query (TPC-H Q15)                      |             2610.50 |
| Parts/Supplier Relationship (TPC-H Q16)             |             5223.69 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |             2117.18 |
| Large Volume Customer (TPC-H Q18)                   |             9585.92 |
| Discounted Revenue (TPC-H Q19)                      |             1357.35 |
| Potential Part Promotion (TPC-H Q20)                |             2991.43 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            65671.78 |
| Global Sales Opportunity Query (TPC-H Q22)          |             3404.76 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |     15532.70 |     12.01 |         189.10 |                189.10 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      4529.90 |      8.00 |           5.31 |                 16.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      1611.18 |      2.03 |           0.00 |                  7.46 |

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |       890.94 |      6.77 |         252.96 |                252.97 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        26.96 |      0.39 |           0.43 |                  0.44 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loader.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component data generator contains no 0 or NaN in CPU [CPUs]
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

We now start a new instance of MonetDB and mount the existing database: we use the prepared database on the shared disk.
We then run two power tests, one after the other (`-ne 1,1`), and shut down the DBMS.
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
  -lr 256Gi \
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
* Duration: 2177s 
* Code: 1792700729
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=100) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 3600.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.8.
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
  * disk:400114
  * datadisk:192979
  * volume_size:984G
  * volume_used:189G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1792700729
* monetdb-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:400115
  * datadisk:189789
  * volume_size:984G
  * volume_used:186G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1792700729
* monetdb-1-2-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:400116
  * datadisk:189789
  * volume_size:984G
  * volume_used:186G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1792700729
* monetdb-1-2-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:400117
  * datadisk:189789
  * volume_size:984G
  * volume_used:186G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1792700729

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MonetDB-1

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1792700729-5587574c76-7564d: 0
* bexhoma-sut-monetdb-1-1792700729-69dd4b5589-bczzw: 0

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

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |  100 |     4049.00 |           3.00 |          625.00 |       1516.00 |         1903.00 |              0 |           0 |             | None           |             0 | False         |               88.91 | True                |
| MonetDB-1-2 |                2 |  100 |     4049.00 |           3.00 |          625.00 |       1516.00 |         1903.00 |              0 |           0 |             | None           |             0 | False         |               88.91 | True                |

### Benchmarking

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| monetdb-1-1-1-1-1 | MonetDB-1       | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               22 |                  22 |        523 |            9.80 |            38440.40 |          15143.40 |          -1 | monetdb-1-1-1-1-1 |
| monetdb-1-1-2-1-1 | MonetDB-1       | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |           1 | 100.00 |               22 |                  22 |        290 |            5.56 |            68565.29 |          27310.34 |          -1 | monetdb-1-1-2-1-1 |
| monetdb-1-2-1-1-1 | MonetDB-1       | monetdb-1-2-1 | monetdb-1-2-1-1 |                2 |        1 |               1 |           1 | 100.00 |               22 |                  22 |        495 |            9.84 |            38183.73 |          16000.00 |          -1 | monetdb-1-2-1-1-1 |
| monetdb-1-2-2-1-1 | MonetDB-1       | monetdb-1-2-2 | monetdb-1-2-2-1 |                2 |        2 |               1 |           1 | 100.00 |               22 |                  22 |        290 |            5.59 |            68493.37 |          27310.34 |          -1 | monetdb-1-2-2-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               22 |                  22 |        523 |            9.80 |            38440.40 |          15143.40 |          -1 |
| monetdb-1-1-2 | monetdb-1-1-2 |                1 |        2 |               1 |           1 | 100.00 |               22 |                  22 |        290 |            5.56 |            68565.29 |          27310.34 |          -1 |
| monetdb-1-2-1 | monetdb-1-2-1 |                2 |        1 |               1 |           1 | 100.00 |               22 |                  22 |        495 |            9.84 |            38183.73 |          16000.00 |          -1 |
| monetdb-1-2-2 | monetdb-1-2-2 |                2 |        2 |               1 |           1 | 100.00 |               22 |                  22 |        290 |            5.59 |            68493.37 |          27310.34 |          -1 |

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
| Pricing Summary Report (TPC-H Q1)                   |           129158.08 |            81724.98 |           116291.17 |            80236.46 |
| Minimum Cost Supplier Query (TPC-H Q2)              |             5973.25 |              769.55 |             6360.14 |              749.29 |
| Shipping Priority (TPC-H Q3)                        |            31056.22 |             7210.89 |            33344.37 |             6352.36 |
| Order Priority Checking Query (TPC-H Q4)            |            20718.16 |            11677.00 |            19192.29 |             9681.22 |
| Local Supplier Volume (TPC-H Q5)                    |             7524.05 |             3426.95 |             6804.40 |             3386.01 |
| Forecasting Revenue Change (TPC-H Q6)               |             1436.78 |             1247.47 |             1997.99 |             1258.33 |
| Volume Shipping Query (TPC-H Q7)                    |             8798.00 |             7796.90 |             9693.94 |             8170.82 |
| National Market Share (TPC-H Q8)                    |            34117.01 |            14720.91 |            36872.15 |            14659.25 |
| Product Type Profit Measure (TPC-H Q9)              |            12715.11 |             5313.92 |            12565.85 |             7655.70 |
| Returned Item Reporting Query (TPC-H Q10)           |            16307.11 |             7631.41 |            14358.80 |             9163.40 |
| Important Stock Identification (TPC-H Q11)          |             1759.74 |             1211.57 |             1737.07 |              968.44 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             2066.97 |             2079.55 |             1916.75 |             2197.20 |
| Customer Distribution (TPC-H Q13)                   |            72758.45 |            30983.30 |            64832.53 |            33840.36 |
| Promotion Effect Query (TPC-H Q14)                  |              959.17 |              934.57 |              961.58 |              939.73 |
| Top Supplier Query (TPC-H Q15)                      |             3461.90 |             2083.27 |             3161.58 |             3524.23 |
| Parts/Supplier Relationship (TPC-H Q16)             |             5484.16 |             5118.23 |             5340.22 |             5918.79 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |            33492.83 |             2044.06 |            31482.94 |             2214.70 |
| Large Volume Customer (TPC-H Q18)                   |            14788.82 |            10128.70 |            14642.92 |            10423.87 |
| Discounted Revenue (TPC-H Q19)                      |             1781.91 |             4265.45 |             2387.13 |             1986.92 |
| Potential Part Promotion (TPC-H Q20)                |             4512.43 |             4439.15 |             4811.18 |             3721.02 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            91620.85 |            62894.24 |            84435.42 |            62242.37 |
| Global Sales Opportunity Query (TPC-H Q22)          |             4021.89 |             3457.70 |             4210.12 |             3602.87 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      1314.71 |      5.70 |         104.77 |                104.77 |
| monetdb-1-1-2-1 |       846.62 |      5.82 |         179.83 |                179.83 |
| monetdb-1-2-1-1 |      1307.44 |      6.81 |         111.95 |                111.95 |
| monetdb-1-2-2-1 |       834.35 |      5.37 |         179.80 |                179.80 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        28.51 |      0.41 |           0.37 |                  0.38 |
| monetdb-1-1-2-1 |        28.40 |      0.20 |           0.38 |                  0.39 |
| monetdb-1-2-1-1 |        26.42 |      0.91 |           0.39 |                  0.40 |
| monetdb-1-2-2-1 |        28.58 |      0.27 |           0.38 |                  0.39 |

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MonetDB-1)
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

We now start a new instance of MonetDB and mount the existing database: we use the prepared database on the shared disk.
We then run two power tests, one after the other, and then a throughput test with 3 parallel driver (`-ne 1,1,3`). and shut down the DBMS.


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
  -lr 256Gi \
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
* Duration: 1844s 
* Code: 1792703031
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=100) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 3600.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.8.
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
  * disk:400352
  * datadisk:189789
  * volume_size:984G
  * volume_used:186G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1792703031
* monetdb-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:400353
  * datadisk:189789
  * volume_size:984G
  * volume_used:186G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1792703031
* monetdb-1-1-3-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:400353
  * datadisk:189789
  * volume_size:984G
  * volume_used:186G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1792703031
* monetdb-1-1-3-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:400353
  * datadisk:189789
  * volume_size:984G
  * volume_used:186G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1792703031
* monetdb-1-1-3-1-3 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:400353
  * datadisk:189789
  * volume_size:984G
  * volume_used:186G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1792703031

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MonetDB-1

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1792703031-7688c97c7d-vn6cz: 0

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

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |  100 |     4049.00 |           3.00 |          625.00 |       1516.00 |         1903.00 |              0 |           0 |             | None           |             0 | False         |               88.91 | True                |

### Benchmarking

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| monetdb-1-1-1-1-1 | MonetDB-1       | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               22 |                  22 |        501 |            9.59 |            39427.75 |          15808.38 |          -1 | monetdb-1-1-1-1-1 |
| monetdb-1-1-2-1-1 | MonetDB-1       | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |           1 | 100.00 |               22 |                  22 |        285 |            5.54 |            69254.80 |          27789.47 |          -1 | monetdb-1-1-2-1-1 |
| monetdb-1-1-3-1-1 | MonetDB-1       | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |           1 | 100.00 |               22 |                  22 |        735 |           11.41 |            32645.75 |          10775.51 |          -1 | monetdb-1-1-3-1-1 |
| monetdb-1-1-3-1-2 | MonetDB-1       | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |           1 | 100.00 |               22 |                  22 |        707 |           10.40 |            36170.68 |          11202.26 |          -1 | monetdb-1-1-3-1-2 |
| monetdb-1-1-3-1-3 | MonetDB-1       | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |           1 | 100.00 |               22 |                  22 |        735 |           10.62 |            35256.16 |          10775.51 |          -1 | monetdb-1-1-3-1-3 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               22 |                  22 |        501 |            9.59 |            39427.75 |          15808.38 |          -1 |
| monetdb-1-1-2 | monetdb-1-1-2 |                1 |        2 |               1 |           1 | 100.00 |               22 |                  22 |        285 |            5.54 |            69254.80 |          27789.47 |          -1 |
| monetdb-1-1-3 | monetdb-1-1-3 |                1 |        3 |               1 |           3 | 100.00 |               66 |                  66 |        735 |           10.80 |            34658.21 |          32326.53 |          -1 |

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
| Pricing Summary Report (TPC-H Q1)                   |           123593.19 |            82493.97 |           242477.23 |           280557.77 |           303223.47 |
| Minimum Cost Supplier Query (TPC-H Q2)              |             6166.08 |              756.08 |             2766.08 |              992.89 |             2474.83 |
| Shipping Priority (TPC-H Q3)                        |            27654.10 |             6609.17 |            15377.18 |            11636.23 |             5885.00 |
| Order Priority Checking Query (TPC-H Q4)            |            19151.72 |             9309.01 |            18439.99 |            20870.04 |            19020.08 |
| Local Supplier Volume (TPC-H Q5)                    |             8167.57 |             4000.59 |            15817.75 |             4540.23 |             6139.46 |
| Forecasting Revenue Change (TPC-H Q6)               |             1525.93 |             1329.24 |             2542.73 |             1194.99 |             2097.08 |
| Volume Shipping Query (TPC-H Q7)                    |             9488.60 |             7152.02 |             7087.30 |             8717.71 |             6206.58 |
| National Market Share (TPC-H Q8)                    |            32840.20 |            14784.17 |            57978.51 |            32681.31 |            16441.44 |
| Product Type Profit Measure (TPC-H Q9)              |            10475.01 |             6898.54 |            24990.49 |            25040.02 |            25415.99 |
| Returned Item Reporting Query (TPC-H Q10)           |            16321.02 |             7923.70 |            10270.17 |            11152.60 |            11023.98 |
| Important Stock Identification (TPC-H Q11)          |             1667.69 |              922.72 |             2429.95 |             1843.65 |             2202.92 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             1975.03 |             2225.48 |             4158.96 |             4367.67 |             3957.51 |
| Customer Distribution (TPC-H Q13)                   |            64603.70 |            31683.81 |            66565.99 |            62799.55 |            60771.62 |
| Promotion Effect Query (TPC-H Q14)                  |              940.89 |              971.77 |              931.31 |             1612.69 |             1832.51 |
| Top Supplier Query (TPC-H Q15)                      |             3075.77 |             2434.23 |             2343.10 |             4786.99 |             6938.34 |
| Parts/Supplier Relationship (TPC-H Q16)             |             5291.48 |             5157.91 |             5872.79 |             5415.66 |             6151.33 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |            32097.47 |             2274.72 |            33909.25 |            34370.92 |            34108.25 |
| Large Volume Customer (TPC-H Q18)                   |            15290.59 |            11607.48 |            22100.82 |            19609.20 |            21624.55 |
| Discounted Revenue (TPC-H Q19)                      |             1625.98 |             3600.20 |             2938.84 |             1980.84 |             2767.66 |
| Potential Part Promotion (TPC-H Q20)                |             5331.31 |             3158.77 |             7611.46 |            11146.84 |             8379.14 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            89302.48 |            59651.82 |           167124.53 |           137456.51 |           166387.15 |
| Global Sales Opportunity Query (TPC-H Q22)          |             4075.50 |             3343.64 |             4413.43 |             7135.58 |             4341.11 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      1178.15 |      8.48 |         111.67 |                111.68 |
| monetdb-1-1-2-1 |       827.71 |      6.81 |         178.16 |                178.16 |
| monetdb-1-1-3-1 |      3475.99 |     10.93 |         252.82 |                255.98 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        28.52 |      0.40 |           0.39 |                  0.41 |
| monetdb-1-1-2-1 |        27.22 |      0.40 |           0.40 |                  0.42 |
| monetdb-1-1-3-1 |        88.34 |      1.31 |           0.45 |                  0.46 |

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MonetDB-1)
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

For performing the experiment we can run the [tpcds file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpcds.py).

### Power Test

```bash
bexhoma tpcds \
  -dbms MonetDB \
  -sf 3 \
  -nlp 8 \
  -nlt 1 \
  -xii -xic -xis \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
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
* Duration: 812s 
* Code: 1782552004
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.2.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * Database uses ephemeral storage of size 30Gi.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MonetDB-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP1
  * RAM:540590804992
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-124-generic
  * node:cl-worker24
  * disk:144619
  * cpu_list:0-95
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782552004

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1782552004-5c996dfb7c-wd4v6: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MonetDB-1-1 |                1 |    3 |      654.00 |          14.00 |            1.00 |        185.00 |          447.00 |              8 |           0 |             | None           |             0 | False         |               16.51 |

### Execution

#### Per Connection

|                   | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MonetDB-1-1-1-1-1 | MonetDB-1       | MonetDB-1-1-1 | MonetDB-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |         34 |            0.10 |           104905.69 |          31447.06 |          -1 | MonetDB-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MonetDB-1-1-1 | MonetDB-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |         34 |            0.10 |           104905.69 |          31447.06 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   MonetDB-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |               54.86 |
| TPC-DS Q2     |              209.02 |
| TPC-DS Q3     |               48.00 |
| TPC-DS Q4     |             1971.25 |
| TPC-DS Q5     |              148.98 |
| TPC-DS Q6     |               59.29 |
| TPC-DS Q7     |               69.35 |
| TPC-DS Q8     |               32.75 |
| TPC-DS Q9     |              129.60 |
| TPC-DS Q10    |               48.36 |
| TPC-DS Q11    |              931.53 |
| TPC-DS Q12    |               22.02 |
| TPC-DS Q13    |              102.36 |
| TPC-DS Q14a+b |             4524.03 |
| TPC-DS Q15    |               29.51 |
| TPC-DS Q16    |              179.23 |
| TPC-DS Q17    |              188.79 |
| TPC-DS Q18    |              103.31 |
| TPC-DS Q19    |               69.30 |
| TPC-DS Q20    |               28.38 |
| TPC-DS Q21    |               63.45 |
| TPC-DS Q22    |             1542.90 |
| TPC-DS Q23a+b |             4430.20 |
| TPC-DS Q24a+b |              257.63 |
| TPC-DS Q25    |              246.42 |
| TPC-DS Q26    |               44.24 |
| TPC-DS Q27    |              173.61 |
| TPC-DS Q28    |              117.85 |
| TPC-DS Q29    |              265.82 |
| TPC-DS Q30    |               23.41 |
| TPC-DS Q31    |              299.83 |
| TPC-DS Q32    |               25.34 |
| TPC-DS Q33    |               31.68 |
| TPC-DS Q34    |               47.38 |
| TPC-DS Q35    |              140.97 |
| TPC-DS Q36    |              190.23 |
| TPC-DS Q37    |               47.09 |
| TPC-DS Q38    |              317.58 |
| TPC-DS Q39a+b |             2405.50 |
| TPC-DS Q40    |               84.39 |
| TPC-DS Q41    |                8.07 |
| TPC-DS Q42    |               34.15 |
| TPC-DS Q43    |               90.39 |
| TPC-DS Q44    |               63.12 |
| TPC-DS Q45    |               33.01 |
| TPC-DS Q46    |               71.48 |
| TPC-DS Q47    |              268.98 |
| TPC-DS Q48    |               74.90 |
| TPC-DS Q49    |              158.44 |
| TPC-DS Q50    |              172.03 |
| TPC-DS Q51    |              726.73 |
| TPC-DS Q52    |               34.32 |
| TPC-DS Q53    |               34.13 |
| TPC-DS Q54    |               39.24 |
| TPC-DS Q55    |               27.84 |
| TPC-DS Q56    |               27.85 |
| TPC-DS Q57    |               98.63 |
| TPC-DS Q58    |              145.24 |
| TPC-DS Q59    |              134.58 |
| TPC-DS Q60    |               36.69 |
| TPC-DS Q61    |               68.46 |
| TPC-DS Q62    |               30.11 |
| TPC-DS Q63    |               33.63 |
| TPC-DS Q64    |              552.20 |
| TPC-DS Q65    |              225.18 |
| TPC-DS Q66    |              183.05 |
| TPC-DS Q67    |              807.36 |
| TPC-DS Q68    |               77.33 |
| TPC-DS Q69    |               40.74 |
| TPC-DS Q70    |              278.28 |
| TPC-DS Q71    |               49.01 |
| TPC-DS Q72    |              184.12 |
| TPC-DS Q73    |               31.17 |
| TPC-DS Q74    |              912.41 |
| TPC-DS Q75    |              828.82 |
| TPC-DS Q76    |               58.75 |
| TPC-DS Q77    |               95.79 |
| TPC-DS Q78    |             1790.85 |
| TPC-DS Q79    |               79.57 |
| TPC-DS Q80    |             1042.49 |
| TPC-DS Q81    |               21.07 |
| TPC-DS Q82    |               42.47 |
| TPC-DS Q83    |               11.62 |
| TPC-DS Q84    |                9.66 |
| TPC-DS Q85    |              149.28 |
| TPC-DS Q86    |               44.46 |
| TPC-DS Q87    |              373.37 |
| TPC-DS Q88    |               99.66 |
| TPC-DS Q89    |               56.99 |
| TPC-DS Q90    |               10.69 |
| TPC-DS Q91    |               16.97 |
| TPC-DS Q92    |               13.81 |
| TPC-DS Q93    |              183.97 |
| TPC-DS Q94    |               53.36 |
| TPC-DS Q95    |              788.74 |
| TPC-DS Q96    |               18.60 |
| TPC-DS Q97    |              362.71 |
| TPC-DS Q98    |               61.70 |
| TPC-DS Q99    |               55.50 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```

</details>

### Monitoring

At SF=3 the 99 queries take about 35 s, so this is shorter than the minute that monitoring needs; see [TPC-DS at SF 30](#tpc-ds-at-sf-30) for a longer run.

```bash
bexhoma tpcds \
  -dbms MonetDB \
  -sf 3 \
  -nlp 8 \
  -nlt 1 \
  -xii -xic -xis \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
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
* Duration: 851s 
* Code: 1782552906
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * Database uses ephemeral storage of size 30Gi.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MonetDB-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP1
  * RAM:540590804992
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-124-generic
  * node:cl-worker24
  * disk:145493
  * cpu_list:0-95
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782552906

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1782552906-68b7dfbc8d-6tfmh: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MonetDB-1-1 |                1 |    3 |      609.00 |           6.00 |            1.00 |        163.00 |          431.00 |              8 |           0 |             | None           |             0 | False         |               17.73 |

### Execution

#### Per Connection

|                   | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MonetDB-1-1-1-1-1 | MonetDB-1       | MonetDB-1-1-1 | MonetDB-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |         33 |            0.10 |           106426.81 |          32400.00 |          -1 | MonetDB-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MonetDB-1-1-1 | MonetDB-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |         33 |            0.10 |           106426.81 |          32400.00 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   MonetDB-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |               49.66 |
| TPC-DS Q2     |              212.79 |
| TPC-DS Q3     |               49.18 |
| TPC-DS Q4     |             1940.56 |
| TPC-DS Q5     |              154.15 |
| TPC-DS Q6     |               61.13 |
| TPC-DS Q7     |               65.65 |
| TPC-DS Q8     |               30.64 |
| TPC-DS Q9     |              126.67 |
| TPC-DS Q10    |               51.22 |
| TPC-DS Q11    |              943.33 |
| TPC-DS Q12    |               20.98 |
| TPC-DS Q13    |               98.89 |
| TPC-DS Q14a+b |             4880.73 |
| TPC-DS Q15    |               36.63 |
| TPC-DS Q16    |              164.85 |
| TPC-DS Q17    |              179.46 |
| TPC-DS Q18    |               98.87 |
| TPC-DS Q19    |               67.41 |
| TPC-DS Q20    |               27.32 |
| TPC-DS Q21    |               62.00 |
| TPC-DS Q22    |             1527.16 |
| TPC-DS Q23a+b |             4248.51 |
| TPC-DS Q24a+b |              258.72 |
| TPC-DS Q25    |              162.29 |
| TPC-DS Q26    |               41.07 |
| TPC-DS Q27    |              171.67 |
| TPC-DS Q28    |              120.18 |
| TPC-DS Q29    |              244.89 |
| TPC-DS Q30    |               22.01 |
| TPC-DS Q31    |              299.47 |
| TPC-DS Q32    |               22.50 |
| TPC-DS Q33    |               31.41 |
| TPC-DS Q34    |               46.36 |
| TPC-DS Q35    |              129.07 |
| TPC-DS Q36    |              197.30 |
| TPC-DS Q37    |               44.87 |
| TPC-DS Q38    |              287.26 |
| TPC-DS Q39a+b |             2459.20 |
| TPC-DS Q40    |               85.07 |
| TPC-DS Q41    |                4.93 |
| TPC-DS Q42    |               33.72 |
| TPC-DS Q43    |               92.25 |
| TPC-DS Q44    |               80.96 |
| TPC-DS Q45    |               30.56 |
| TPC-DS Q46    |               74.57 |
| TPC-DS Q47    |              300.76 |
| TPC-DS Q48    |               73.36 |
| TPC-DS Q49    |              170.34 |
| TPC-DS Q50    |              194.34 |
| TPC-DS Q51    |              736.53 |
| TPC-DS Q52    |               34.56 |
| TPC-DS Q53    |               32.25 |
| TPC-DS Q54    |               39.01 |
| TPC-DS Q55    |               24.29 |
| TPC-DS Q56    |               30.98 |
| TPC-DS Q57    |               89.37 |
| TPC-DS Q58    |              181.14 |
| TPC-DS Q59    |              132.64 |
| TPC-DS Q60    |               29.34 |
| TPC-DS Q61    |               68.41 |
| TPC-DS Q62    |               29.15 |
| TPC-DS Q63    |               32.50 |
| TPC-DS Q64    |              518.04 |
| TPC-DS Q65    |              209.89 |
| TPC-DS Q66    |              187.58 |
| TPC-DS Q67    |              737.45 |
| TPC-DS Q68    |               74.40 |
| TPC-DS Q69    |               46.68 |
| TPC-DS Q70    |              229.30 |
| TPC-DS Q71    |               50.04 |
| TPC-DS Q72    |              168.39 |
| TPC-DS Q73    |               30.35 |
| TPC-DS Q74    |              232.17 |
| TPC-DS Q75    |              835.34 |
| TPC-DS Q76    |              242.43 |
| TPC-DS Q77    |              122.10 |
| TPC-DS Q78    |             1818.65 |
| TPC-DS Q79    |               73.30 |
| TPC-DS Q80    |              915.01 |
| TPC-DS Q81    |               30.50 |
| TPC-DS Q82    |               55.53 |
| TPC-DS Q83    |                9.17 |
| TPC-DS Q84    |               10.31 |
| TPC-DS Q85    |              164.30 |
| TPC-DS Q86    |               43.47 |
| TPC-DS Q87    |              337.60 |
| TPC-DS Q88    |               98.23 |
| TPC-DS Q89    |               55.26 |
| TPC-DS Q90    |               10.75 |
| TPC-DS Q91    |               18.40 |
| TPC-DS Q92    |               13.46 |
| TPC-DS Q93    |              168.71 |
| TPC-DS Q94    |               49.15 |
| TPC-DS Q95    |              782.70 |
| TPC-DS Q96    |               16.58 |
| TPC-DS Q97    |              389.19 |
| TPC-DS Q98    |               61.43 |
| TPC-DS Q99    |               56.24 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |       330.33 |      2.55 |           4.53 |                  6.05 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |         0.24 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |        26.43 |      0.24 |           0.01 |                  2.21 |

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |        86.74 |      4.41 |          10.46 |                 12.00 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |         0.02 |      0.00 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
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

### Throughput Test on Persistent Storage

```bash
bexhoma tpcds \
  -dbms MonetDB \
  -sf 3 \
  -nlp 8 \
  -nlt 1 \
  -xii -xic -xis \
  -nc 2 \
  -ne 1,2 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rsr \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_monetdb_storage.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_monetdb_storage_summary.md" target="_blank" rel="noopener">docs_tpcds_monetdb_storage.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=3
    Type: tpcds
    Duration: 995s 
    Code: 1728675428
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Import sets indexes and constraints after loading and recomputes statistics.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MonetDB'].
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
MonetDB-BHT-8-1-1-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:249634108
    datadisk:5486698
    volume_size:100G
    volume_used:5.3G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-1-2-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:249634108
    datadisk:5558770
    volume_size:100G
    volume_used:5.3G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-1-2-2 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:249634108
    datadisk:5558770
    volume_size:100G
    volume_used:5.3G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-2-1-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:249634108
    datadisk:5558771
    volume_size:100G
    volume_used:5.4G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-2-2-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:249634108
    datadisk:5558197
    volume_size:100G
    volume_used:5.4G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-2-2-2 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:249634108
    datadisk:5558197
    volume_size:100G
    volume_used:5.4G
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
            MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-1-2-1  MonetDB-BHT-8-1-2-2  MonetDB-BHT-8-2-1-1  MonetDB-BHT-8-2-2-1  MonetDB-BHT-8-2-2-2
TPC-DS Q1                  True                 True                 True                 True                 True                False
TPC-DS Q25                 True                 True                 True                 True                 True                False
TPC-DS Q34                 True                 True                 True                 True                 True                False
TPC-DS Q43                 True                 True                 True                 True                 True                False
TPC-DS Q44                 True                 True                 True                 True                 True                False
TPC-DS Q46                 True                 True                 True                 True                 True                False
TPC-DS Q54                 True                 True                 True                 True                 True                False
TPC-DS Q68                 True                 True                 True                 True                 True                False
TPC-DS Q73                 True                 True                 True                 True                 True                False

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-1-2-1  MonetDB-BHT-8-1-2-2  MonetDB-BHT-8-2-1-1  MonetDB-BHT-8-2-2-1  MonetDB-BHT-8-2-2-2
TPC-DS Q1                  1457.90                55.71                52.77              1036.26                53.04                64.40
TPC-DS Q2                  8897.17               433.92               417.83              6701.04               416.75               425.14
TPC-DS Q3                  2492.94                43.05                33.73              1810.61                40.69                38.67
TPC-DS Q4                 12439.46              3795.57              3938.42             10047.81              4018.64              3859.93
TPC-DS Q5                  6301.59               740.40               634.56              3798.51               689.95               622.01
TPC-DS Q6                   582.82               217.37               175.64               486.61               155.69               150.46
TPC-DS Q7                  2761.20                96.81                82.15              2552.40                86.28               122.09
TPC-DS Q8                  1220.89               128.82               120.85              1012.07                95.54               119.90
TPC-DS Q9                   635.23               230.87               222.55               513.18               195.19               176.37
TPC-DS Q10                 1944.22                66.97                74.34              1442.27                64.76               115.25
TPC-DS Q11                 1995.57              1960.02              1840.68              1973.40              1940.35              1893.88
TPC-DS Q12                  901.53                37.77                39.34               811.98                32.13                36.08
TPC-DS Q13                  298.44               184.98               173.74               196.24               136.51               151.76
TPC-DS Q14a+b              7875.23              7310.76              6835.78              6959.55              6064.90              5986.83
TPC-DS Q15                  317.83                40.80                36.44               183.75                33.21                57.51
TPC-DS Q16                 1582.59               280.60               283.50              1249.30               284.59               274.86
TPC-DS Q17                 1246.26               329.36               365.05              1072.00               312.44               437.02
TPC-DS Q18                  949.22               220.84               266.57              1394.53               223.82               229.80
TPC-DS Q19                  163.75                82.94                77.59               125.20                81.99                86.57
TPC-DS Q20                   58.07                52.46                51.33                52.19                48.89                50.37
TPC-DS Q21                 7896.30                66.97                93.68              5718.54                93.54               103.29
TPC-DS Q22                 2789.12              2970.36              2736.95              2785.88              2820.73              2821.87
TPC-DS Q23a+b              6467.52              6817.87              7425.04              6773.74              6912.46              6692.53
TPC-DS Q24a+b               786.52               360.59               328.72               930.28               354.57               310.32
TPC-DS Q25                  390.95               382.50               379.47               832.69               378.67               372.53
TPC-DS Q26                  414.53                62.61               113.07               230.80                60.97               153.19
TPC-DS Q27                  391.67               336.29               388.75               485.71               368.16               340.48
TPC-DS Q28                  810.17               195.01               184.20               651.45               175.24               175.50
TPC-DS Q29                  348.06               408.32               421.04               349.08               362.12               466.38
TPC-DS Q30                  256.94                51.04                48.23               135.65                65.69                32.77
TPC-DS Q31                  853.96               411.53               457.30               899.25               449.57               464.16
TPC-DS Q32                   39.75                39.67                40.41                64.72                34.82                34.99
TPC-DS Q33                  158.07                56.13                49.50                92.59                53.07                53.46
TPC-DS Q34                  667.98                44.71                44.78               439.87                45.05                51.55
TPC-DS Q35                  193.79               227.84               208.86               223.47               218.79               191.00
TPC-DS Q37                  183.74                66.45               108.31               363.26                65.78                62.99
TPC-DS Q38                  559.49               612.53               612.32               649.48               577.21               605.82
TPC-DS Q39a+b              2795.62              2621.09              2604.48              2728.80              2441.65              2736.29
TPC-DS Q40                  454.41                84.46                95.53               672.49                81.85                82.76
TPC-DS Q41                    8.78                12.81                 8.59                 9.38                 9.06                 8.77
TPC-DS Q42                   36.26                38.52                89.67                37.75                50.32                46.54
TPC-DS Q43                   99.81               105.60                94.91               101.64               105.66               116.34
TPC-DS Q44                   67.60                65.70                80.38                70.85                78.03                63.74
TPC-DS Q45                   36.77                48.37                41.96                39.58                41.19                41.62
TPC-DS Q46                  293.60               112.61                80.49               126.50                72.92               107.04
TPC-DS Q47                  652.86               629.48               689.78               665.06               646.98               666.18
TPC-DS Q48                  129.64               126.69               134.31               453.37               129.62               150.58
TPC-DS Q49                  994.84               254.84               265.41               631.35               224.06               234.91
TPC-DS Q50                  411.80               257.95               239.26               331.69               232.09               340.69
TPC-DS Q51                 1810.95              1761.45              1819.17              1792.25              1836.54              1803.62
TPC-DS Q52                   38.61                37.25                37.28                73.31                36.40                38.77
TPC-DS Q53                   63.88                57.65                57.54                66.58                56.20                70.13
TPC-DS Q54                  295.37                36.98                43.54               232.27                41.14                46.92
TPC-DS Q55                   36.21                29.34                29.12                30.14                29.58                34.00
TPC-DS Q56                   65.69                45.06                46.22                42.60                57.03                43.49
TPC-DS Q57                  258.10               182.61               187.59               196.75               187.37               228.58
TPC-DS Q58                  120.90               118.55               131.27               118.36               118.08               142.61
TPC-DS Q59                  279.80               517.06               524.65               249.02               256.63               260.00
TPC-DS Q60                  173.97                58.92                58.14               182.61                62.58                60.17
TPC-DS Q61                  132.04                67.16                66.30                91.42               167.82                64.46
TPC-DS Q62                  729.19               283.22               281.48               559.81                52.02                46.38
TPC-DS Q63                   54.77                76.32                74.40                53.21                50.57                62.17
TPC-DS Q64                 1324.58               643.39               614.00              1151.97               582.28               597.60
TPC-DS Q65                  411.61               419.52               409.04               397.73               425.15               440.10
TPC-DS Q66                 1267.26               538.76               627.83               716.93               306.93               279.70
TPC-DS Q67                 2420.32              2473.85              2260.13              2270.07              2176.51              2418.12
TPC-DS Q68                  733.11                79.67                72.15               235.31                76.59                73.66
TPC-DS Q69                  286.03                71.44                76.99                80.09                76.24                83.76
TPC-DS Q71                  493.94                60.72                72.69               104.31                64.92               420.97
TPC-DS Q72                 2568.27              3801.24              3849.62              2638.45              3913.62              2981.85
TPC-DS Q73                   52.42                42.56                42.55                42.67                44.51                44.01
TPC-DS Q74                  553.73               613.68               598.28               553.55               564.35               579.13
TPC-DS Q75                 4278.21              2325.02              2354.85              3556.34              2403.58              2328.77
TPC-DS Q76                   72.60                76.63                73.81                67.52                83.05                72.04
TPC-DS Q77                  413.48               173.82               180.13               350.36               180.41               188.84
TPC-DS Q78                 3199.09              3134.83              3575.71              3106.40              2970.40              3732.60
TPC-DS Q79                  211.67                88.75                85.18               174.57                78.34                83.01
TPC-DS Q80                 2100.88              2233.29              2029.86              2173.84              2227.43              2372.94
TPC-DS Q81                  192.89                33.27                60.99                99.19                34.15                32.81
TPC-DS Q82                  544.84                69.25                72.32               437.80                76.63                67.48
TPC-DS Q83                  133.69                21.77                21.10               176.84                21.54                22.19
TPC-DS Q84                  335.91                16.58                14.86               364.21                16.59                15.92
TPC-DS Q85                  198.42                70.18                74.61                86.76                95.47                82.30
TPC-DS Q87                  750.08               777.95               754.70               755.24               754.57               751.73
TPC-DS Q88                  789.86               191.05               199.44               504.00               180.22               205.46
TPC-DS Q89                   83.55                81.68                75.47                77.83                80.40                75.74
TPC-DS Q90                  746.61                22.87                20.18               423.59                20.78                32.37
TPC-DS Q91                  189.19                26.79                25.40                69.64                27.00                27.08
TPC-DS Q92                   27.13                25.20                24.32                24.93                25.59                26.29
TPC-DS Q93                  353.73               446.38               438.20               335.19               328.46               317.22
TPC-DS Q94                  441.25                63.27                65.71               295.77                67.04                62.92
TPC-DS Q95                  200.01               255.47               252.36               193.54               186.92               208.63
TPC-DS Q96                   25.11                25.25                24.40                24.63                24.59                25.76
TPC-DS Q97                  888.44               955.01               970.64               865.66              1030.15               947.86
TPC-DS Q98                   85.35                83.53                86.75                86.76                87.75                89.26
TPC-DS Q99                   91.98               101.54                94.49                94.38                97.89                90.17

### Loading [s]
                     timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1-1           1.0          275.0         5.0      105.0     393.0
MonetDB-BHT-8-1-2-1           1.0          275.0         5.0      105.0     393.0
MonetDB-BHT-8-1-2-2           1.0          275.0         5.0      105.0     393.0
MonetDB-BHT-8-2-1-1           1.0          275.0         5.0      105.0     393.0
MonetDB-BHT-8-2-2-1           1.0          275.0         5.0      105.0     393.0
MonetDB-BHT-8-2-2-2           1.0          275.0         5.0      105.0     393.0

### Geometric Mean of Medians of Timer Run [s]
                     Geo Times [s]
DBMS                              
MonetDB-BHT-8-1-1-1           0.43
MonetDB-BHT-8-1-2-1           0.18
MonetDB-BHT-8-1-2-2           0.18
MonetDB-BHT-8-2-1-1           0.38
MonetDB-BHT-8-2-2-1           0.17
MonetDB-BHT-8-2-2-2           0.18

### Power@Size
                     Power@Size [~Q/h]
DBMS                                  
MonetDB-BHT-8-1-1-1           25917.90
MonetDB-BHT-8-1-2-1           64333.08
MonetDB-BHT-8-1-2-2           63407.94
MonetDB-BHT-8-2-1-1           30183.86
MonetDB-BHT-8-2-2-1           67882.00
MonetDB-BHT-8-2-2-2           64231.37

### Throughput@Size
                                                time [s]  count  SF  Throughput@Size [~GB/h]
DBMS              SF num_experiment num_client                                              
MonetDB-BHT-8-1-1 3  1              1                129      1   3                  1841.86
MonetDB-BHT-8-1-2 3  1              2                 68      2   3                  6988.24
MonetDB-BHT-8-2-1 3  2              1                114      1   3                  2084.21
MonetDB-BHT-8-2-2 3  2              2                 65      2   3                  7310.77

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1, 2], [1, 2]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1, 2], [1, 2]]

### Execution - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1-1      238.66     0.00          3.32                 8.23
MonetDB-BHT-8-1-2      565.72     9.99         16.86                22.39
MonetDB-BHT-8-2-1     1154.98     0.00          7.93                16.96
MonetDB-BHT-8-2-2      334.40     0.00          5.01                10.34

### Execution - Benchmarker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1-1       14.10     0.05          0.25                 0.26
MonetDB-BHT-8-1-2       34.05     0.33          0.75                 0.78
MonetDB-BHT-8-2-1       34.05     0.00          0.74                 0.77
MonetDB-BHT-8-2-2       27.37     0.00          0.73                 0.76

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

</details>


## TPC-DS at SF 30

This example shows how to run Q1-Q99 derived from TPC-DS in MonetDB at SF=30.
It covers the power and the throughput test.
The refresh stream is not included.

> The query file is derived from the TPC-DS and as such is not comparable to published TPC-DS results, as the query file results do not comply with the TPC-DS specification.

Official TPC-DS benchmark - http://www.tpc.org/tpcds




### Generate and Load Data

At first we generate TPC-DS data at SF=30 (`-sf`) with 8 parallel generators (`-nlp`).
The generated data is stored at the shared disk `data`.
Moreover the data is loaded into an instance of MonetDB using again 8 parallel loaders.
Afterwards the script creates contraints (`-xic`) and indexes (`-xii`) and updates table statistics (`-xis`).
The database is located in a persistent volume of storageClass nvme (`-rst`) and of size 3000Gi (`-rss`).
Storage is cleaned if it has existed (`-rsr`).

The script also runs a power test (`-ne` set to 1) with timeout 14400s (`-t`) and data transfer activated (`-xdt`) once (`-nc` set to 1).
To avoid conflicts with other experiments we set a maximum of 1 DBMS per time (`-ms`).
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

In the following example output we see all components of bexhoma are up and running.
The cluster stores a MonetDB database corresponding to TPC-DS of SF=30.
The disk is of storageClass nvme and of size 3000Gi and 156G of that space is used.
It took about 4000s to build this database.
Currently no DBMS is running.

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
* Duration: 1777s 
* Code: 1793885417
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=30) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 14400.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
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
  * disk:956520
  * datadisk:77050
  * volume_size:2.9T
  * volume_used:76G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793885417

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1793885417-776f984748-8jtc5: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |   30 |      941.00 |           2.00 |            1.00 |        420.00 |          499.00 |              8 |           0 |             | None           |             0 | False         |              114.77 | False               |

### Benchmarking

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| monetdb-1-1-1-1-1 | MonetDB-1       | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        631 |            0.63 |           176550.07 |          16944.53 |          -1 | monetdb-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        631 |            0.63 |           176550.07 |          16944.53 |          -1 |

#### Query Completion per Phase

| phase         |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:--------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   monetdb-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |              180.88 |
| TPC-DS Q2     |             1409.37 |
| TPC-DS Q3     |              155.70 |
| TPC-DS Q4     |            16552.23 |
| TPC-DS Q5     |             1590.20 |
| TPC-DS Q6     |              394.76 |
| TPC-DS Q7     |              196.08 |
| TPC-DS Q8     |              372.68 |
| TPC-DS Q9     |              524.59 |
| TPC-DS Q10    |              205.12 |
| TPC-DS Q11    |             7983.27 |
| TPC-DS Q12    |              182.21 |
| TPC-DS Q13    |              292.41 |
| TPC-DS Q14a+b |            32474.45 |
| TPC-DS Q15    |              145.77 |
| TPC-DS Q16    |            44913.28 |
| TPC-DS Q17    |             2197.77 |
| TPC-DS Q18    |              949.09 |
| TPC-DS Q19    |              165.57 |
| TPC-DS Q20    |              117.85 |
| TPC-DS Q21    |              108.39 |
| TPC-DS Q22    |             1130.22 |
| TPC-DS Q23a+b |            64499.17 |
| TPC-DS Q24a+b |            14520.96 |
| TPC-DS Q25    |             2294.79 |
| TPC-DS Q26    |              187.99 |
| TPC-DS Q27    |             1713.36 |
| TPC-DS Q28    |              557.36 |
| TPC-DS Q29    |             2478.94 |
| TPC-DS Q30    |               74.09 |
| TPC-DS Q31    |             1777.22 |
| TPC-DS Q32    |              154.45 |
| TPC-DS Q33    |              226.01 |
| TPC-DS Q34    |              174.49 |
| TPC-DS Q35    |              727.79 |
| TPC-DS Q36    |             1367.72 |
| TPC-DS Q37    |              438.19 |
| TPC-DS Q38    |             3314.59 |
| TPC-DS Q39a+b |             1218.93 |
| TPC-DS Q40    |              930.61 |
| TPC-DS Q41    |                7.18 |
| TPC-DS Q42    |              110.21 |
| TPC-DS Q43    |              215.28 |
| TPC-DS Q44    |              199.43 |
| TPC-DS Q45    |              133.90 |
| TPC-DS Q46    |              164.15 |
| TPC-DS Q47    |              900.22 |
| TPC-DS Q48    |              302.14 |
| TPC-DS Q49    |             1451.26 |
| TPC-DS Q50    |              606.57 |
| TPC-DS Q51    |             2648.03 |
| TPC-DS Q52    |              109.78 |
| TPC-DS Q53    |               97.01 |
| TPC-DS Q54    |               89.86 |
| TPC-DS Q55    |               55.99 |
| TPC-DS Q56    |              159.46 |
| TPC-DS Q57    |              139.98 |
| TPC-DS Q58    |              572.11 |
| TPC-DS Q59    |             1385.10 |
| TPC-DS Q60    |              178.05 |
| TPC-DS Q61    |              197.63 |
| TPC-DS Q62    |              267.68 |
| TPC-DS Q63    |              103.73 |
| TPC-DS Q64    |             4114.98 |
| TPC-DS Q65    |             1177.45 |
| TPC-DS Q66    |             1892.30 |
| TPC-DS Q67    |             5555.64 |
| TPC-DS Q68    |              539.04 |
| TPC-DS Q69    |              309.97 |
| TPC-DS Q70    |             1754.82 |
| TPC-DS Q71    |              347.15 |
| TPC-DS Q72    |             1183.09 |
| TPC-DS Q73    |               95.66 |
| TPC-DS Q74    |             2808.65 |
| TPC-DS Q75    |             5571.87 |
| TPC-DS Q76    |              329.29 |
| TPC-DS Q77    |              776.51 |
| TPC-DS Q78    |            14074.28 |
| TPC-DS Q79    |              174.33 |
| TPC-DS Q80    |             8011.76 |
| TPC-DS Q81    |               71.43 |
| TPC-DS Q82    |              490.37 |
| TPC-DS Q83    |              144.82 |
| TPC-DS Q84    |               36.47 |
| TPC-DS Q85    |              305.16 |
| TPC-DS Q86    |              308.50 |
| TPC-DS Q87    |             2774.09 |
| TPC-DS Q88    |              650.73 |
| TPC-DS Q89    |              178.77 |
| TPC-DS Q90    |               76.83 |
| TPC-DS Q91    |               26.58 |
| TPC-DS Q92    |              110.68 |
| TPC-DS Q93    |             2109.78 |
| TPC-DS Q94    |            38688.42 |
| TPC-DS Q95    |           286212.64 |
| TPC-DS Q96    |              767.06 |
| TPC-DS Q97    |             4237.08 |
| TPC-DS Q98    |              499.43 |
| TPC-DS Q99    |              412.61 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      2862.50 |      7.71 |          71.88 |                 73.34 |

### Loading phase: component data generator

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |       304.59 |      0.93 |           0.03 |                  9.94 |

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |     10844.25 |    164.22 |         947.97 |               1023.88 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        33.70 |      0.42 |           0.39 |                  0.40 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
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

We now start a new instance of MonetDB and mount the existing database: we use the prepared database on the shared disk.
We then run two power tests, one after the other (`-ne 1,1`), and shut down the DBMS.
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
* Duration: 3367s 
* Code: 1793887265
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=30) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 14400.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
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
  * disk:956526
  * datadisk:76803
  * volume_size:2.9T
  * volume_used:76G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1793887265
* monetdb-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:956532
  * datadisk:75380
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1793887265
* monetdb-1-2-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:956530
  * datadisk:75380
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1793887265
* monetdb-1-2-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:956734
  * datadisk:75380
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1793887265

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MonetDB-1

### Data Parameters of Reused Volumes
* MonetDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1793887265-b8dc746d8-dfgbq: 0
* bexhoma-sut-monetdb-1-1793887265-68fd4f5f49-rqts9: 0

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

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |   30 |      941.00 |           2.00 |            1.00 |        420.00 |          499.00 |              0 |           0 |             | None           |             0 | False         |              114.77 | True                |
| MonetDB-1-2 |                2 |   30 |      941.00 |           2.00 |            1.00 |        420.00 |          499.00 |              0 |           0 |             | None           |             0 | False         |              114.77 | True                |

### Benchmarking

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| monetdb-1-1-1-1-1 | MonetDB-1       | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        780 |            0.93 |           120010.43 |          13707.69 |          -1 | monetdb-1-1-1-1-1 |
| monetdb-1-1-2-1-1 | MonetDB-1       | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |           1 | 30.00 |               99 |                  99 |        704 |            0.76 |           147313.41 |          15187.50 |          -1 | monetdb-1-1-2-1-1 |
| monetdb-1-2-1-1-1 | MonetDB-1       | monetdb-1-2-1 | monetdb-1-2-1-1 |                2 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        797 |            0.90 |           124477.73 |          13415.31 |          -1 | monetdb-1-2-1-1-1 |
| monetdb-1-2-2-1-1 | MonetDB-1       | monetdb-1-2-2 | monetdb-1-2-2-1 |                2 |        2 |               1 |           1 | 30.00 |               99 |                  99 |        722 |            0.74 |           150423.07 |          14808.86 |          -1 | monetdb-1-2-2-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        780 |            0.93 |           120010.43 |          13707.69 |          -1 |
| monetdb-1-1-2 | monetdb-1-1-2 |                1 |        2 |               1 |           1 | 30.00 |               99 |                  99 |        704 |            0.76 |           147313.41 |          15187.50 |          -1 |
| monetdb-1-2-1 | monetdb-1-2-1 |                2 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        797 |            0.90 |           124477.73 |          13415.31 |          -1 |
| monetdb-1-2-2 | monetdb-1-2-2 |                2 |        2 |               1 |           1 | 30.00 |               99 |                  99 |        722 |            0.74 |           150423.07 |          14808.86 |          -1 |

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
| TPC-DS Q1     |             1218.56 |              320.19 |             1341.53 |              248.64 |
| TPC-DS Q2     |             4706.90 |             1713.52 |             4002.93 |             1616.56 |
| TPC-DS Q3     |             2263.11 |              133.30 |             2595.19 |              115.23 |
| TPC-DS Q4     |            26792.74 |            18441.67 |            24687.07 |            17222.13 |
| TPC-DS Q5     |            18697.68 |             2216.15 |            20245.41 |             2421.91 |
| TPC-DS Q6     |              581.39 |              578.02 |              528.25 |              319.17 |
| TPC-DS Q7     |             4988.84 |             1167.33 |             5699.93 |             1100.99 |
| TPC-DS Q8     |             3886.28 |              622.83 |             3850.25 |              677.19 |
| TPC-DS Q9     |              842.11 |              517.28 |              528.88 |              500.98 |
| TPC-DS Q10    |            19019.51 |              516.21 |            22459.87 |              483.57 |
| TPC-DS Q11    |             6981.28 |             7404.07 |             6347.73 |             6633.43 |
| TPC-DS Q12    |              236.24 |              177.62 |              246.30 |              147.77 |
| TPC-DS Q13    |              438.73 |              527.91 |              452.12 |              678.55 |
| TPC-DS Q14a+b |            36127.10 |            39039.60 |            33515.08 |            37178.50 |
| TPC-DS Q15    |              269.47 |              128.69 |              229.16 |              137.98 |
| TPC-DS Q16    |            49513.41 |            41732.07 |            47391.90 |            42231.85 |
| TPC-DS Q17    |             3454.03 |             3298.60 |             3410.47 |             3355.09 |
| TPC-DS Q18    |             2020.09 |             2141.90 |             2161.51 |             1936.76 |
| TPC-DS Q19    |              173.58 |              185.06 |              173.75 |              150.17 |
| TPC-DS Q20    |              129.48 |              117.37 |              130.46 |              100.12 |
| TPC-DS Q21    |             1994.86 |              158.72 |             2293.90 |              166.42 |
| TPC-DS Q22    |             2132.76 |             2200.13 |             1753.37 |             1756.56 |
| TPC-DS Q23a+b |            40832.35 |            34155.88 |            37910.48 |            35844.27 |
| TPC-DS Q24a+b |            15264.98 |            15632.94 |            14482.29 |            15840.84 |
| TPC-DS Q25    |             2409.62 |             2556.10 |             2548.54 |             2309.27 |
| TPC-DS Q26    |              167.58 |              193.64 |              178.48 |              175.81 |
| TPC-DS Q27    |             1815.14 |             1324.42 |             1414.02 |             1312.11 |
| TPC-DS Q28    |              626.33 |              624.22 |              678.40 |              611.42 |
| TPC-DS Q29    |             2449.05 |             2358.97 |             2194.25 |             2406.86 |
| TPC-DS Q30    |               97.74 |              120.85 |              127.99 |              130.64 |
| TPC-DS Q31    |             2587.74 |             2364.81 |             2306.97 |             2491.74 |
| TPC-DS Q32    |              217.58 |              191.24 |              169.12 |              183.82 |
| TPC-DS Q33    |              131.13 |              133.34 |              163.84 |              133.12 |
| TPC-DS Q34    |              308.76 |              151.11 |              320.95 |              107.63 |
| TPC-DS Q35    |              703.71 |              748.54 |              854.65 |              828.43 |
| TPC-DS Q36    |             1380.08 |             1597.01 |             1373.52 |             1319.51 |
| TPC-DS Q37    |             1926.69 |             2186.63 |             1930.82 |             1829.77 |
| TPC-DS Q38    |             3624.19 |             2380.92 |             2588.21 |             3249.27 |
| TPC-DS Q39a+b |             1200.05 |             1164.30 |             1160.61 |             1141.61 |
| TPC-DS Q40    |              419.74 |              646.77 |              424.76 |              658.66 |
| TPC-DS Q41    |                5.83 |                6.47 |                5.41 |                5.83 |
| TPC-DS Q42    |               98.51 |              123.33 |              101.34 |              103.50 |
| TPC-DS Q43    |              288.90 |              299.64 |              320.56 |              277.61 |
| TPC-DS Q44    |              349.77 |              410.41 |              369.79 |              377.21 |
| TPC-DS Q45    |              117.60 |              132.72 |              138.47 |              134.99 |
| TPC-DS Q46    |              211.12 |              197.65 |              198.48 |              190.28 |
| TPC-DS Q47    |             1928.94 |             1040.63 |              961.70 |              959.78 |
| TPC-DS Q48    |              240.79 |              212.98 |              214.73 |              209.84 |
| TPC-DS Q49    |             4004.94 |             1698.78 |             4459.10 |             1614.23 |
| TPC-DS Q50    |              590.77 |              574.89 |              576.93 |              580.66 |
| TPC-DS Q51    |             3063.47 |             2398.52 |             2413.79 |             2320.91 |
| TPC-DS Q52    |              122.58 |               86.34 |              108.81 |               97.07 |
| TPC-DS Q53    |               99.34 |               91.16 |               96.80 |               90.85 |
| TPC-DS Q54    |               84.69 |               85.24 |               82.26 |               85.14 |
| TPC-DS Q55    |               77.86 |               88.10 |               73.80 |               70.33 |
| TPC-DS Q56    |              162.76 |              143.08 |              159.44 |              508.33 |
| TPC-DS Q57    |              138.66 |              132.81 |              140.51 |              234.48 |
| TPC-DS Q58    |              583.22 |              554.61 |              597.58 |              619.65 |
| TPC-DS Q59    |             1438.88 |             1147.89 |             1024.17 |             1078.04 |
| TPC-DS Q60    |              159.95 |              166.96 |              175.29 |              160.49 |
| TPC-DS Q61    |              221.37 |              194.56 |              199.04 |              205.75 |
| TPC-DS Q62    |              446.15 |              455.88 |              432.13 |              461.76 |
| TPC-DS Q63    |               94.97 |               95.42 |               90.89 |              100.22 |
| TPC-DS Q64    |             4721.44 |             5441.91 |             4873.73 |             4680.40 |
| TPC-DS Q65    |             1291.98 |             1069.93 |             1055.59 |             1163.28 |
| TPC-DS Q66    |             2355.48 |             2648.01 |             2368.38 |             2913.24 |
| TPC-DS Q67    |             5952.91 |             5554.85 |             5524.58 |             5475.04 |
| TPC-DS Q68    |              389.02 |              378.51 |              399.48 |              426.65 |
| TPC-DS Q69    |              364.05 |              522.13 |              406.98 |              377.76 |
| TPC-DS Q70    |             1382.74 |             1410.26 |             1372.43 |             1335.22 |
| TPC-DS Q71    |              521.19 |              535.20 |              365.26 |              516.23 |
| TPC-DS Q72    |             2138.63 |             2550.72 |             2241.74 |             2388.29 |
| TPC-DS Q73    |              102.38 |               94.26 |               99.19 |              109.69 |
| TPC-DS Q74    |             1847.07 |             1848.15 |             1969.33 |             2879.52 |
| TPC-DS Q75    |             6360.78 |             6080.82 |             5400.97 |             5932.12 |
| TPC-DS Q76    |             8930.58 |            10444.16 |             6757.32 |             9915.69 |
| TPC-DS Q77    |             1086.60 |             1080.74 |             1157.00 |             1389.88 |
| TPC-DS Q78    |            13730.79 |            12163.30 |            12092.31 |            12399.54 |
| TPC-DS Q79    |              305.81 |              282.37 |              269.12 |              257.66 |
| TPC-DS Q80    |             8168.15 |             7490.11 |             7149.59 |             7108.41 |
| TPC-DS Q81    |               71.74 |               88.00 |               82.36 |               96.82 |
| TPC-DS Q82    |              430.50 |              459.79 |              430.53 |              405.97 |
| TPC-DS Q83    |              221.33 |              285.50 |              258.43 |              237.90 |
| TPC-DS Q84    |               66.72 |               65.29 |               53.60 |               48.04 |
| TPC-DS Q85    |              551.23 |              318.54 |              311.34 |              291.96 |
| TPC-DS Q86    |              302.62 |              311.59 |              338.13 |              301.21 |
| TPC-DS Q87    |             2766.91 |             2927.50 |             2754.86 |             2699.55 |
| TPC-DS Q88    |              752.56 |              424.88 |              667.01 |              418.51 |
| TPC-DS Q89    |              139.83 |              132.65 |              142.48 |              142.45 |
| TPC-DS Q90    |               86.73 |              132.48 |               89.54 |              129.01 |
| TPC-DS Q91    |               38.87 |               45.48 |               46.10 |               35.40 |
| TPC-DS Q92    |              140.88 |              165.08 |              161.72 |              155.64 |
| TPC-DS Q93    |             2014.81 |             1930.46 |             1929.81 |             2067.18 |
| TPC-DS Q94    |            40091.01 |            39132.88 |            37345.08 |            40179.47 |
| TPC-DS Q95    |           362510.78 |           362886.63 |           394968.74 |           383028.30 |
| TPC-DS Q96    |              776.78 |              773.53 |              751.87 |              835.58 |
| TPC-DS Q97    |             4704.73 |             4048.28 |             4619.13 |             4298.59 |
| TPC-DS Q98    |              522.29 |             1128.82 |              514.41 |              520.06 |
| TPC-DS Q99    |              412.85 |              401.07 |              397.34 |              400.94 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |     10892.34 |     95.01 |         987.90 |               1023.82 |
| monetdb-1-1-2-1 |     13136.71 |    156.74 |        1012.93 |               1023.78 |
| monetdb-1-2-1-1 |     13862.28 |    181.09 |        1013.14 |               1023.87 |
| monetdb-1-2-2-1 |     11994.80 |    109.91 |         975.63 |               1023.99 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        33.23 |      0.47 |           0.39 |                  0.40 |
| monetdb-1-1-2-1 |        33.94 |      0.46 |           0.37 |                  0.37 |
| monetdb-1-2-1-1 |        33.58 |      0.50 |           0.39 |                  0.40 |
| monetdb-1-2-2-1 |        33.35 |      0.46 |           0.37 |                  0.38 |

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

We now start a new instance of MonetDB and mount the existing database: we use the prepared database on the shared disk.
We then run two power tests, one after the other, and then a throughput test with 3 parallel driver (`-ne 1,1,3`). and shut down the DBMS.


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
* Duration: 1922s 
* Code: 1793890732
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=30) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 14400.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
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
  * disk:956544
  * datadisk:75380
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1793890732
* monetdb-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:956548
  * datadisk:75380
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1793890732
* monetdb-1-1-3-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:956553
  * datadisk:75380
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1793890732
* monetdb-1-1-3-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:956553
  * datadisk:75380
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1793890732
* monetdb-1-1-3-1-3 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:956553
  * datadisk:75380
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1793890732

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MonetDB-1

### Data Parameters of Reused Volumes
* MonetDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1793890732-65d46c6948-5lrbb: 0

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

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |   30 |      941.00 |           2.00 |            1.00 |        420.00 |          499.00 |              0 |           0 |             | None           |             0 | False         |              114.77 | True                |

### Benchmarking

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| monetdb-1-1-1-1-1 | MonetDB-1       | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        526 |            0.88 |           128495.99 |          20327.00 |          -1 | monetdb-1-1-1-1-1 |
| monetdb-1-1-2-1-1 | MonetDB-1       | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |           1 | 30.00 |               99 |                  99 |        442 |            0.58 |           199227.02 |          24190.05 |          -1 | monetdb-1-1-2-1-1 |
| monetdb-1-1-3-1-1 | MonetDB-1       | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |           1 | 30.00 |               99 |                  99 |        624 |            0.98 |           115591.85 |          17134.62 |          -1 | monetdb-1-1-3-1-1 |
| monetdb-1-1-3-1-2 | MonetDB-1       | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |           1 | 30.00 |               99 |                  99 |        717 |            0.75 |           153705.47 |          14912.13 |          -1 | monetdb-1-1-3-1-2 |
| monetdb-1-1-3-1-3 | MonetDB-1       | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |           1 | 30.00 |               99 |                  99 |        696 |            0.85 |           134542.56 |          15362.07 |          -1 | monetdb-1-1-3-1-3 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        526 |            0.88 |           128495.99 |          20327.00 |          -1 |
| monetdb-1-1-2 | monetdb-1-1-2 |                1 |        2 |               1 |           1 | 30.00 |               99 |                  99 |        442 |            0.58 |           199227.02 |          24190.05 |          -1 |
| monetdb-1-1-3 | monetdb-1-1-3 |                1 |        3 |               1 |           3 | 30.00 |              297 |                 297 |        717 |            0.86 |           133708.42 |          44736.40 |          -1 |

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
| TPC-DS Q1     |             1730.60 |              171.52 |              156.28 |              265.49 |              263.05 |
| TPC-DS Q2     |             4348.58 |             1279.38 |             1606.98 |             3170.63 |             2619.01 |
| TPC-DS Q3     |             2885.35 |              151.31 |              325.06 |              518.76 |              131.85 |
| TPC-DS Q4     |            26588.76 |            16589.00 |            17274.97 |            19848.55 |            18419.82 |
| TPC-DS Q5     |            19471.89 |             1691.39 |             1428.98 |             1530.38 |             2036.31 |
| TPC-DS Q6     |              604.13 |              310.81 |              500.21 |              277.40 |              336.52 |
| TPC-DS Q7     |             5380.11 |              187.69 |             1570.53 |              436.36 |              154.06 |
| TPC-DS Q8     |             3818.15 |              314.12 |              476.99 |              296.29 |              280.10 |
| TPC-DS Q9     |              734.80 |              533.63 |              659.94 |              887.68 |              580.13 |
| TPC-DS Q10    |            22119.81 |              124.65 |              232.57 |              141.90 |              306.29 |
| TPC-DS Q11    |             7120.58 |             7156.00 |             7535.94 |             8137.51 |             8007.76 |
| TPC-DS Q12    |              259.16 |              195.55 |              118.49 |              210.31 |              529.48 |
| TPC-DS Q13    |              524.70 |              286.18 |              285.03 |              589.51 |              486.63 |
| TPC-DS Q14a+b |            37099.72 |            30876.13 |            32172.15 |            32877.44 |            32436.89 |
| TPC-DS Q15    |              159.41 |              134.66 |              176.36 |              132.24 |              126.82 |
| TPC-DS Q16    |            50168.43 |            44857.42 |            43024.68 |           157812.98 |           133649.61 |
| TPC-DS Q17    |             3392.58 |             2781.61 |             4506.47 |             2602.14 |             8346.70 |
| TPC-DS Q18    |             2140.69 |              939.99 |            12464.75 |             1275.67 |            16269.12 |
| TPC-DS Q19    |              178.54 |              182.91 |             4684.41 |              257.00 |              159.43 |
| TPC-DS Q20    |              136.85 |              113.20 |            33348.68 |              183.03 |              170.34 |
| TPC-DS Q21    |             2341.05 |               99.09 |            22106.63 |              153.84 |              180.33 |
| TPC-DS Q22    |             1878.99 |              975.21 |            17535.60 |             1194.01 |             1244.55 |
| TPC-DS Q23a+b |            54445.99 |            57269.94 |            62973.68 |            65840.02 |            60235.09 |
| TPC-DS Q24a+b |            14043.62 |            16345.81 |             8062.14 |             9998.54 |             6268.13 |
| TPC-DS Q25    |             2346.58 |             2324.78 |             3006.12 |             2706.92 |             3957.40 |
| TPC-DS Q26    |              193.31 |              197.52 |              312.70 |              349.60 |              206.84 |
| TPC-DS Q27    |             1278.65 |             1331.81 |             1536.13 |             1344.30 |             2318.56 |
| TPC-DS Q28    |              605.77 |              521.83 |              648.36 |              644.20 |              991.21 |
| TPC-DS Q29    |             3074.86 |             2706.63 |             2655.41 |             2317.36 |             4124.96 |
| TPC-DS Q30    |              115.81 |               72.55 |               76.81 |               76.66 |               72.28 |
| TPC-DS Q31    |             2294.38 |             1570.12 |             1521.79 |             1892.54 |             2801.78 |
| TPC-DS Q32    |              155.54 |              174.52 |              120.28 |              174.12 |              183.98 |
| TPC-DS Q33    |              167.53 |              130.19 |              116.61 |              113.24 |              280.11 |
| TPC-DS Q34    |              314.55 |              103.82 |              107.96 |              102.61 |              136.43 |
| TPC-DS Q35    |              761.89 |              713.64 |              668.00 |              756.48 |             1035.97 |
| TPC-DS Q36    |             1639.83 |             1686.31 |             2284.08 |             2510.63 |             2134.45 |
| TPC-DS Q37    |             1481.15 |              491.47 |              363.70 |              420.82 |              986.60 |
| TPC-DS Q38    |             2510.38 |             2392.42 |             4282.34 |             2911.35 |             3011.97 |
| TPC-DS Q39a+b |             1370.26 |             1173.68 |             3208.96 |             1251.44 |             1286.13 |
| TPC-DS Q40    |              420.50 |              671.32 |              868.39 |              355.61 |              493.85 |
| TPC-DS Q41    |                5.38 |                7.51 |               81.99 |                9.49 |                6.81 |
| TPC-DS Q42    |              110.87 |               90.73 |              488.03 |               81.04 |              103.63 |
| TPC-DS Q43    |              313.64 |              207.70 |             1167.57 |              204.66 |              322.33 |
| TPC-DS Q44    |              227.91 |              221.17 |              408.42 |              244.55 |              215.78 |
| TPC-DS Q45    |              121.90 |              117.97 |              142.91 |              136.39 |              138.14 |
| TPC-DS Q46    |              215.92 |              199.34 |              812.10 |              225.82 |              238.88 |
| TPC-DS Q47    |              975.37 |             1056.26 |             4294.26 |             1739.29 |             1252.04 |
| TPC-DS Q48    |              217.78 |              213.51 |             3557.61 |              271.36 |              221.46 |
| TPC-DS Q49    |             4466.05 |             1033.19 |             2656.92 |             1736.34 |             1375.73 |
| TPC-DS Q50    |              604.91 |              578.55 |              633.72 |              652.69 |              924.45 |
| TPC-DS Q51    |             2270.52 |             2333.36 |             3082.19 |             2323.08 |             2570.38 |
| TPC-DS Q52    |              118.99 |               79.06 |              759.21 |              120.02 |               87.57 |
| TPC-DS Q53    |              145.09 |               88.03 |              274.84 |               85.09 |               91.85 |
| TPC-DS Q54    |              159.39 |               92.16 |              173.27 |               87.83 |               93.61 |
| TPC-DS Q55    |               97.41 |               71.55 |               92.39 |               80.60 |               87.05 |
| TPC-DS Q56    |              436.97 |              170.14 |              198.20 |              104.44 |              246.13 |
| TPC-DS Q57    |              281.35 |              135.77 |              141.73 |              134.77 |              227.91 |
| TPC-DS Q58    |              569.38 |              565.06 |              560.25 |              513.22 |              825.63 |
| TPC-DS Q59    |              998.43 |             1206.95 |              765.24 |              628.95 |              606.94 |
| TPC-DS Q60    |              166.97 |              136.14 |              120.98 |              194.90 |              132.29 |
| TPC-DS Q61    |              261.16 |              201.50 |              208.94 |              300.55 |              244.77 |
| TPC-DS Q62    |              447.76 |              268.72 |              293.73 |              379.71 |              270.70 |
| TPC-DS Q63    |              101.22 |               96.19 |              101.52 |              109.91 |              185.65 |
| TPC-DS Q64    |             6253.45 |             2464.46 |             3079.45 |             2374.45 |             2439.47 |
| TPC-DS Q65    |             1795.59 |             1714.25 |             1084.98 |             1040.56 |             1128.37 |
| TPC-DS Q66    |             2289.80 |             1682.44 |             1795.17 |             2299.04 |             1053.25 |
| TPC-DS Q67    |             5560.55 |             5594.07 |             5643.89 |             6562.13 |             6091.21 |
| TPC-DS Q68    |              515.00 |              521.21 |              439.44 |              258.64 |              429.43 |
| TPC-DS Q69    |               94.45 |              104.67 |               96.48 |              111.00 |              110.79 |
| TPC-DS Q70    |             1434.57 |             1439.26 |             1486.04 |             2097.38 |             1486.63 |
| TPC-DS Q71    |              353.05 |              183.76 |              178.15 |              182.46 |              872.01 |
| TPC-DS Q72    |             2339.64 |             1475.15 |             1086.45 |             1155.38 |             1033.56 |
| TPC-DS Q73    |               98.87 |               98.61 |               86.12 |               90.62 |              113.27 |
| TPC-DS Q74    |             2520.74 |             1861.18 |             2118.07 |             2094.24 |             2297.78 |
| TPC-DS Q75    |             6487.58 |             5848.43 |             6003.47 |             5578.15 |             6081.12 |
| TPC-DS Q76    |             1993.83 |              320.36 |              189.78 |              170.63 |              160.32 |
| TPC-DS Q77    |             1247.74 |              780.38 |              766.96 |              698.86 |              789.85 |
| TPC-DS Q78    |            12554.74 |            14208.19 |            13210.85 |            15795.93 |            15892.51 |
| TPC-DS Q79    |              267.77 |              248.80 |              257.03 |              248.29 |              235.56 |
| TPC-DS Q80    |             7282.42 |             8103.07 |             7540.67 |             9286.84 |             9356.26 |
| TPC-DS Q81    |              164.00 |              138.99 |              128.36 |              321.56 |              311.18 |
| TPC-DS Q82    |              438.61 |              449.80 |              822.27 |              412.73 |              378.60 |
| TPC-DS Q83    |              251.37 |               60.63 |               39.06 |               41.20 |               43.60 |
| TPC-DS Q84    |               46.78 |               40.50 |               34.38 |               43.41 |               44.49 |
| TPC-DS Q85    |              301.98 |              318.60 |              299.57 |              302.47 |              278.84 |
| TPC-DS Q86    |              308.54 |              333.65 |              346.50 |              280.50 |              285.89 |
| TPC-DS Q87    |             2790.49 |             2829.57 |             3350.04 |             5438.77 |             4050.00 |
| TPC-DS Q88    |              705.45 |              414.10 |              917.75 |            15204.61 |             9447.84 |
| TPC-DS Q89    |              142.73 |              273.12 |              176.95 |             4002.09 |            10594.10 |
| TPC-DS Q90    |               71.47 |               68.37 |               69.67 |              153.11 |              147.99 |
| TPC-DS Q91    |               60.93 |               26.55 |               39.78 |              337.49 |              339.87 |
| TPC-DS Q92    |              134.92 |              158.24 |              133.44 |             3243.37 |             2978.56 |
| TPC-DS Q93    |             2193.92 |             2078.71 |             2557.93 |            17678.94 |            18094.81 |
| TPC-DS Q94    |            40706.17 |            36277.09 |            39039.57 |            98735.00 |            50400.27 |
| TPC-DS Q95    |            49797.92 |            51272.42 |            51891.60 |            65517.21 |            87713.72 |
| TPC-DS Q96    |               34.29 |               61.65 |               86.84 |               39.34 |              345.63 |
| TPC-DS Q97    |             3845.98 |             3119.01 |             7736.77 |             3093.93 |             6243.94 |
| TPC-DS Q98    |              149.20 |              158.14 |            11320.54 |              145.57 |              479.36 |
| TPC-DS Q99    |              275.90 |              321.98 |            31634.47 |              254.64 |              778.45 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      6293.15 |     75.49 |         378.89 |                378.90 |
| monetdb-1-1-2-1 |      6751.14 |     91.66 |         360.63 |                360.64 |
| monetdb-1-1-3-1 |     20408.22 |    146.85 |         510.54 |                510.55 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        80.18 |      0.70 |           0.69 |                  0.73 |
| monetdb-1-1-2-1 |        85.24 |      0.76 |           0.72 |                  0.75 |
| monetdb-1-1-3-1 |       340.74 |      2.74 |           0.73 |                  0.76 |

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


## TPC-DS at SF 100

### Power Test

This loads TPC-DS at SF=100 into a persistent volume.

```bash
bexhoma tpcds \
  -dbms MonetDB \
  -sf 100 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rsr \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 1000Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_monetdb_sf100.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_monetdb_sf100_summary.md" target="_blank" rel="noopener">docs_tpcds_monetdb_sf100.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=100
    Type: tpcds
    Duration: 6331s 
    Code: 1728676629
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=100) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Import sets indexes and constraints after loading and recomputes statistics.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MonetDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 300Gi.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:249634108
    datadisk:162530732
    volume_size:300G
    volume_used:155G
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1
TPC-DS Q1               21540.10
TPC-DS Q2              234536.17
TPC-DS Q3               52161.56
TPC-DS Q4              383862.53
TPC-DS Q5              130445.75
TPC-DS Q6               12467.55
TPC-DS Q7               73421.64
TPC-DS Q8               47626.63
TPC-DS Q9               35999.02
TPC-DS Q10              13875.78
TPC-DS Q11              87521.23
TPC-DS Q12               2813.57
TPC-DS Q13               7253.94
TPC-DS Q14a+b          410993.67
TPC-DS Q15              11345.34
TPC-DS Q16              20444.94
TPC-DS Q17             112165.36
TPC-DS Q18              24168.99
TPC-DS Q19               5743.73
TPC-DS Q20               1023.79
TPC-DS Q21              91704.61
TPC-DS Q22              86337.22
TPC-DS Q23a+b         2736895.84
TPC-DS Q24a+b            6107.79
TPC-DS Q25              20943.89
TPC-DS Q26               1762.98
TPC-DS Q27              28616.77
TPC-DS Q28              24479.10
TPC-DS Q29              14225.98
TPC-DS Q30               2905.96
TPC-DS Q31              22703.53
TPC-DS Q32                535.63
TPC-DS Q33              14858.80
TPC-DS Q34               2961.26
TPC-DS Q35               7629.06
TPC-DS Q37              34972.06
TPC-DS Q38              29446.64
TPC-DS Q39a+b           79446.39
TPC-DS Q40               5005.79
TPC-DS Q41                340.97
TPC-DS Q42               2261.78
TPC-DS Q43               2160.14
TPC-DS Q44               3335.84
TPC-DS Q45               1007.63
TPC-DS Q46               2493.34
TPC-DS Q47               5878.41
TPC-DS Q48               1175.38
TPC-DS Q49              38294.50
TPC-DS Q50               3741.81
TPC-DS Q51              50318.14
TPC-DS Q52               1265.41
TPC-DS Q53               2107.47
TPC-DS Q54               7608.31
TPC-DS Q55               2060.64
TPC-DS Q56              12970.61
TPC-DS Q57               2303.47
TPC-DS Q58               5467.10
TPC-DS Q59              11463.27
TPC-DS Q60               3737.78
TPC-DS Q61               4874.03
TPC-DS Q62               3992.80
TPC-DS Q63                950.49
TPC-DS Q64              45759.04
TPC-DS Q65              25361.62
TPC-DS Q66              21174.82
TPC-DS Q67             112971.25
TPC-DS Q68               9680.79
TPC-DS Q69               3257.94
TPC-DS Q71               4878.81
TPC-DS Q72              32102.01
TPC-DS Q73                322.64
TPC-DS Q74              24826.16
TPC-DS Q75             187073.16
TPC-DS Q76              14043.38
TPC-DS Q77               8627.66
TPC-DS Q78             191797.32
TPC-DS Q79               5074.40
TPC-DS Q80             117303.11
TPC-DS Q81               2790.04
TPC-DS Q82              28911.03
TPC-DS Q83               1952.11
TPC-DS Q84                879.36
TPC-DS Q85               3602.37
TPC-DS Q87              59126.34
TPC-DS Q88               3332.16
TPC-DS Q89               3645.28
TPC-DS Q90               1185.67
TPC-DS Q91               1299.77
TPC-DS Q92               2001.95
TPC-DS Q93              28101.76
TPC-DS Q94               2069.09
TPC-DS Q95              18037.05
TPC-DS Q96                119.80
TPC-DS Q97              42468.49
TPC-DS Q98               3413.94
TPC-DS Q99               1930.03

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1        4023.0         1362.0         6.0     2703.0    8096.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1          10.34

### Power@Size
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           35243.87

### Throughput@Size
                                               time [s]  count   SF  Throughput@Size [~GB/h]
DBMS            SF  num_experiment num_client                                               
MonetDB-BHT-8-1 100 1              1               6117      1  100                  1294.75

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1]]

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1    20233.87     16.8        133.36               245.14

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       42.02     0.06          0.39                  0.4

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

</details>

### Throughput Test

1 and 5 parallel streams (`-ne 1,5`), repeated (`-nc 2`), on the loaded volume:

```bash
bexhoma tpcds \
  -dbms MonetDB \
  -sf 100 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -nc 2 \
  -ne 1,5 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 1000Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_monetdb_sf100_throughput.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_monetdb_sf100_throughput_summary.md" target="_blank" rel="noopener">docs_tpcds_monetdb_sf100_throughput.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=100
    Type: tpcds
    Duration: 20752s 
    Code: 1729497306
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=100) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Import sets indexes and constraints after loading and recomputes statistics.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MonetDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 300Gi.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 1, 5, 5] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250321764
    datadisk:288744504
    volume_size:300G
    volume_used:276G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-2-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322104
    datadisk:157561721
    volume_size:300G
    volume_used:151G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-3-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322276
    datadisk:157561721
    volume_size:300G
    volume_used:151G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-3-2 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322276
    datadisk:157561721
    volume_size:300G
    volume_used:151G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-3-3 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322276
    datadisk:157561721
    volume_size:300G
    volume_used:151G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-3-4 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322276
    datadisk:157561721
    volume_size:300G
    volume_used:151G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-3-5 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322276
    datadisk:157561721
    volume_size:300G
    volume_used:151G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-4-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322616
    datadisk:232899461
    volume_size:300G
    volume_used:223G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-4-2 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322616
    datadisk:232899461
    volume_size:300G
    volume_used:223G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-4-3 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322616
    datadisk:232899461
    volume_size:300G
    volume_used:223G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-4-4 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322616
    datadisk:232899461
    volume_size:300G
    volume_used:223G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-4-5 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322616
    datadisk:232899461
    volume_size:300G
    volume_used:223G
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
               MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-3-1  MonetDB-BHT-8-3-2  MonetDB-BHT-8-3-3  MonetDB-BHT-8-3-4  MonetDB-BHT-8-3-5  MonetDB-BHT-8-4-1  MonetDB-BHT-8-4-2  MonetDB-BHT-8-4-3  MonetDB-BHT-8-4-4  MonetDB-BHT-8-4-5
TPC-DS Q23a+b              False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q24a+b              False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q25                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q26                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q27                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q28                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q29                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q30                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q31                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q32                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q33                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q34                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q35                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q37                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q38                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q39a+b              False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q40                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q41                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q42                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q43                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q44                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q45                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q46                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q47                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q48                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q49                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q50                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q51                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q52                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q53                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q54                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q55                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q56                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q57                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q58                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q59                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q60                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q61                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q62                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q63                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q64                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q65                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q66                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q67                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q68                 False              False               True               True               True              False              False              False              False              False               True              False
TPC-DS Q69                 False              False               True               True               True              False              False              False              False              False               True              False
TPC-DS Q71                 False              False               True               True               True              False              False              False              False              False               True              False
TPC-DS Q72                 False              False               True               True               True              False              False              False              False              False               True              False
TPC-DS Q73                 False              False               True               True               True              False              False              False               True               True               True              False
TPC-DS Q74                 False              False               True               True               True              False              False              False               True               True               True              False
TPC-DS Q75                 False              False               True               True               True              False              False              False               True               True               True               True
TPC-DS Q76                 False              False               True               True               True              False              False               True               True               True               True               True
TPC-DS Q77                 False              False               True               True               True              False              False               True               True               True               True               True
TPC-DS Q78                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q79                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q80                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q81                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q82                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q83                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q84                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q85                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q87                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q88                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q89                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q90                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q91                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q92                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q93                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q94                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q95                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q96                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q97                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q98                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q99                 False              False               True               True               True               True               True               True               True               True               True               True

### Warnings (result mismatch)
            MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-3-1  MonetDB-BHT-8-3-2  MonetDB-BHT-8-3-3  MonetDB-BHT-8-3-4  MonetDB-BHT-8-3-5  MonetDB-BHT-8-4-1  MonetDB-BHT-8-4-2  MonetDB-BHT-8-4-3  MonetDB-BHT-8-4-4  MonetDB-BHT-8-4-5
TPC-DS Q1                True               True               True              False               True               True               True               True               True               True               True               True
TPC-DS Q34               True               True              False              False              False               True               True               True               True               True              False               True
TPC-DS Q46               True               True              False              False              False               True               True               True               True               True              False               True
TPC-DS Q54               True               True              False              False              False               True               True               True               True               True              False               True
TPC-DS Q68               True               True              False              False              False               True               True               True               True               True              False               True
TPC-DS Q69               True               True              False              False              False               True               True               True               True               True              False               True
TPC-DS Q71               True               True              False              False              False               True               True               True               True               True              False               True
TPC-DS Q72               True               True              False              False              False               True               True               True               True               True              False               True
TPC-DS Q73               True               True              False              False              False               True               True               True              False              False              False               True
TPC-DS Q74               True               True              False              False              False               True               True               True              False              False              False               True
TPC-DS Q75               True               True              False              False              False               True               True               True              False              False              False              False
TPC-DS Q76               True               True              False              False              False               True               True              False              False              False              False              False
TPC-DS Q77               True               True              False              False              False               True               True              False              False              False              False              False
TPC-DS Q78               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q79               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q80               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q81               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q82               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q83               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q84               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q85               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q87               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q88               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q89               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q90               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q91               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q92               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q93               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q94               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q95               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q96               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q97               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q98               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q99               True               True              False              False              False              False              False              False              False              False              False              False

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-3-1  MonetDB-BHT-8-3-2  MonetDB-BHT-8-3-3  MonetDB-BHT-8-3-4  MonetDB-BHT-8-3-5  MonetDB-BHT-8-4-1  MonetDB-BHT-8-4-2  MonetDB-BHT-8-4-3  MonetDB-BHT-8-4-4  MonetDB-BHT-8-4-5
TPC-DS Q1               27370.75            2398.34            3427.48            3548.13            2621.80            3349.98            2533.30           42994.62           43099.49           42921.18           42831.04           42908.51
TPC-DS Q2              290821.48           12968.89           42420.72           43545.27           43077.55           42017.09           43019.55          587520.51          587142.92          589163.04          587448.87          588656.35
TPC-DS Q3              113297.32            2534.75            2226.94            1311.94            2827.32            2754.30            2898.16          126104.75          126592.93          124695.38          126524.33          125210.92
TPC-DS Q4              419012.49          151417.82          841027.33          841979.72          771544.18          758497.43          987181.05          863825.28          842226.46          875548.69          841795.93          864986.88
TPC-DS Q5              152472.27           25913.86           38700.56           38704.71           75992.76           89474.50           35704.63          280847.09          302657.12          272871.72          309269.37          290256.00
TPC-DS Q6               10465.72            6148.11            8494.14            8372.64           20295.71           19794.75           10755.25           39960.65           38099.00           35536.35           36848.37           32571.94
TPC-DS Q7               85464.02            1717.00             656.49             659.43           14569.19           14941.80             779.82          125905.42          127393.38          126724.35          122928.01          123021.42
TPC-DS Q8               31537.49            2868.56           51567.86           50598.40           57879.85           57629.18            4131.33           37375.11           37821.85           37375.05           37374.59           37374.76
TPC-DS Q9               24558.10            2959.41            9601.51            7915.98            8954.79            8555.44            2609.90           39832.01           37006.15           39783.22           39745.52           39686.99
TPC-DS Q10               4798.43            1708.85           10055.94           12059.05           11024.65           11410.25            1068.77            8830.09           11203.75            8863.00            8856.28            8982.50
TPC-DS Q11              74948.80           74442.53          127970.28          129086.83          119531.67          127820.74           98889.67          128465.69          116448.46          123230.43          115624.77          126471.84
TPC-DS Q12               1922.56             586.98             489.47             429.42            8194.10             615.13             359.98             302.72             711.24            3474.69            1657.43             523.10
TPC-DS Q13               2705.39            1601.06            3541.62            2587.14            4190.26            3541.01             356.11             335.97            8615.20             375.12            8625.05             414.59
TPC-DS Q14a+b          331389.83          274582.58          495565.35          450771.53          450517.42          450518.97          498161.82          544996.30          520469.11          543487.22          534403.23          570664.29
TPC-DS Q15              11234.26            1133.29             539.39            3274.29            3533.18            3535.34             704.67             639.50           14143.56             606.52             869.53            1274.78
TPC-DS Q16              25139.98             863.51             783.43            5917.83            5936.80            5181.27             795.14           43898.62           57727.55           46832.57           57696.69           19303.74
TPC-DS Q17              57273.54           34438.89          136125.32          173456.87          179543.43          175108.63           85005.01          218938.52          223817.53          219048.18          220848.61          219440.73
TPC-DS Q18              26480.21            8663.66           22465.62           22848.76           15768.86           21216.73           21039.15           51344.16           46580.72           51222.66           49248.84           50783.59
TPC-DS Q19               2424.20            2259.17            6801.66            6127.00            6794.42            6798.48            6977.89            9677.23            9660.20            9704.29            9707.72            9694.76
TPC-DS Q20                941.11             498.07             859.07             876.10            1179.98            1178.25            1177.47             731.59             729.09             735.39             730.50             730.95
TPC-DS Q21             115406.12             950.95            6428.35            6422.47            6412.70            6404.55            6426.69          142631.61          142621.07          142619.30          142613.04          142602.51
TPC-DS Q22              91135.38           81955.21           97082.60          112905.33          112828.09          107411.61           97016.26           97696.66          110253.74           97281.24           91222.80          121667.95

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-2-1        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-3-1        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-3-2        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-3-3        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-3-4        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-3-5        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-4-1        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-4-2        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-4-3        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-4-4        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-4-5        4023.0         1362.0         6.0     2703.0    8096.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1          29.76
MonetDB-BHT-8-2-1           5.57
MonetDB-BHT-8-3-1          11.35
MonetDB-BHT-8-3-2          13.07
MonetDB-BHT-8-3-3          19.37
MonetDB-BHT-8-3-4          17.48
MonetDB-BHT-8-3-5           7.76
MonetDB-BHT-8-4-1          35.40
MonetDB-BHT-8-4-2          49.88
MonetDB-BHT-8-4-3          39.40
MonetDB-BHT-8-4-4          44.92
MonetDB-BHT-8-4-5          36.51

### Power@Size
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           12115.25
MonetDB-BHT-8-2-1           64912.63
MonetDB-BHT-8-3-1           31815.26
MonetDB-BHT-8-3-2           27619.23
MonetDB-BHT-8-3-3           18609.96
MonetDB-BHT-8-3-4           20642.87
MonetDB-BHT-8-3-5           46558.91
MonetDB-BHT-8-4-1           10194.85
MonetDB-BHT-8-4-2            7229.98
MonetDB-BHT-8-4-3            9147.06
MonetDB-BHT-8-4-4            8024.32
MonetDB-BHT-8-4-5            9884.43

### Throughput@Size
                                               time [s]  count   SF  Throughput@Size [~GB/h]
DBMS            SF  num_experiment num_client                                               
MonetDB-BHT-8-1 100 1              1               6889      1  100                  1149.66
MonetDB-BHT-8-2 100 1              2               3711      1  100                  2134.20
MonetDB-BHT-8-3 100 1              3               4040      5  100                  9801.98
MonetDB-BHT-8-4 100 1              4               5477      5  100                  7230.24

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1, 1, 5, 5]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1, 1, 5, 5]]

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1    21745.36    17.29        173.03               283.57
MonetDB-BHT-8-2    18120.57    20.21        188.28               290.39
MonetDB-BHT-8-3    43989.47    42.21        461.98               484.15
MonetDB-BHT-8-4    50356.12    45.19        457.93               484.00

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       39.84     0.10          0.38                 0.41
MonetDB-BHT-8-2       39.84     0.01          0.63                 0.66
MonetDB-BHT-8-3       80.27     0.03          1.58                 1.62
MonetDB-BHT-8-4      126.49     0.12          1.78                 1.82

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST failed: SQL errors
TEST failed: SQL warnings (result mismatch)
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

</details>


## SSB

The Star Schema Benchmark runs on MonetDB, too, see [Example: SSB](Example-SSB.md).
