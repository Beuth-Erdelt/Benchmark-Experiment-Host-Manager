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
* Duration: 301s 
* Code: 1795693895
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
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
  * RAM:1081742733312
  * CPU:AMD EPYC 7502 32-Core Processor
  * Cores:128
  * host:6.8.0-146-generic
  * node:cl-worker29
  * disk:710428
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
    * code:1795693895

### Ingestion
* MonetDB-1: 50 of 50 units ok

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1795693895-748695df89-f852x: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |    1 |       62.00 |           2.00 |           18.00 |         13.00 |           19.00 |              8 |         0 |             | None           |             0 | False         |               58.06 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         11 |            0.10 |            40445.35 |           7200.00 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         11 |            0.10 |            40445.35 |           7200.00 |          -1 |

#### Query Completion per Phase

| phase         |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:--------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   monetdb-1-1-1-1-1 |
|:----------------------------------------------------|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |              880.99 |
| Minimum Cost Supplier Query (TPC-H Q2)              |               30.11 |
| Shipping Priority (TPC-H Q3)                        |               93.31 |
| Order Priority Checking Query (TPC-H Q4)            |              142.51 |
| Local Supplier Volume (TPC-H Q5)                    |               60.21 |
| Forecasting Revenue Change (TPC-H Q6)               |               25.89 |
| Volume Shipping Query (TPC-H Q7)                    |               66.91 |
| National Market Share (TPC-H Q8)                    |              319.16 |
| Product Type Profit Measure (TPC-H Q9)              |               79.64 |
| Returned Item Reporting Query (TPC-H Q10)           |              154.91 |
| Important Stock Identification (TPC-H Q11)          |               19.83 |
| Shipping Modes and Order Priority (TPC-H Q12)       |               49.23 |
| Customer Distribution (TPC-H Q13)                   |              340.61 |
| Promotion Effect Query (TPC-H Q14)                  |               33.53 |
| Top Supplier Query (TPC-H Q15)                      |               34.30 |
| Parts/Supplier Relationship (TPC-H Q16)             |               87.39 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               49.10 |
| Large Volume Customer (TPC-H Q18)                   |              195.23 |
| Discounted Revenue (TPC-H Q19)                      |               73.10 |
| Potential Part Promotion (TPC-H Q20)                |               35.09 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |             1578.31 |
| Global Sales Opportunity Query (TPC-H Q22)          |               41.09 |

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
* TEST passed: SUT pods not replaced
* TEST passed: Host information complete
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
* TEST passed: Results of all benchmarker pods
* TEST passed: Benchmarker pods without errors

Test successful!
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
* Duration: 1669s 
* Code: 1795694220
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=30) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 3600.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
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
  * RAM:1081742733312
  * CPU:AMD EPYC 7502 32-Core Processor
  * Cores:128
  * host:6.8.0-146-generic
  * node:cl-worker29
  * disk:765100
  * datadisk:57618
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795694220

### Ingestion
* MonetDB-1: 50 of 50 units ok

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1795694220-f69457f8b-99bhr: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |   30 |     1337.00 |           1.00 |          199.00 |        358.00 |          776.00 |              8 |         0 |             | None           |             0 | False         |               80.78 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 30.00 |               22 |                  22 |        116 |            2.00 |            58984.47 |          20482.76 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               22 |                  22 |        116 |            2.00 |            58984.47 |          20482.76 |          -1 |

#### Query Completion per Phase

| phase         |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:--------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   monetdb-1-1-1-1-1 |
|:----------------------------------------------------|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |            20396.93 |
| Minimum Cost Supplier Query (TPC-H Q2)              |              306.26 |
| Shipping Priority (TPC-H Q3)                        |             2225.72 |
| Order Priority Checking Query (TPC-H Q4)            |             3225.38 |
| Local Supplier Volume (TPC-H Q5)                    |             1237.12 |
| Forecasting Revenue Change (TPC-H Q6)               |              561.76 |
| Volume Shipping Query (TPC-H Q7)                    |             2475.55 |
| National Market Share (TPC-H Q8)                    |             8646.45 |
| Product Type Profit Measure (TPC-H Q9)              |             1907.33 |
| Returned Item Reporting Query (TPC-H Q10)           |             4595.14 |
| Important Stock Identification (TPC-H Q11)          |              334.21 |
| Shipping Modes and Order Priority (TPC-H Q12)       |              673.67 |
| Customer Distribution (TPC-H Q13)                   |            11412.21 |
| Promotion Effect Query (TPC-H Q14)                  |              333.18 |
| Top Supplier Query (TPC-H Q15)                      |              957.66 |
| Parts/Supplier Relationship (TPC-H Q16)             |             1839.29 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |             1022.00 |
| Large Volume Customer (TPC-H Q18)                   |             2931.94 |
| Discounted Revenue (TPC-H Q19)                      |              661.98 |
| Potential Part Promotion (TPC-H Q20)                |              947.64 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            37193.94 |
| Global Sales Opportunity Query (TPC-H Q22)          |              975.56 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      4632.11 |     16.00 |          57.17 |                 57.17 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      1265.92 |      8.00 |           0.31 |                  7.38 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |       379.27 |      1.72 |           0.00 |                  0.00 |

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |       278.92 |      3.47 |          75.77 |                 75.77 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        22.85 |      0.46 |           0.36 |                  0.37 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
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
* TEST passed: SUT pods not replaced
* TEST passed: Host information complete
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component data generator contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Monitoring returned data
* TEST skipped: Monitoring metrics missing (data pre-existing; series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
* TEST passed: Results of all benchmarker pods
* TEST passed: Benchmarker pods without errors

Test successful!
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
* Duration: 540s 
* Code: 1795695942
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
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
  * RAM:1081742733312
  * CPU:AMD EPYC 7502 32-Core Processor
  * Cores:128
  * host:6.8.0-146-generic
  * node:cl-worker29
  * disk:708157
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
    * code:1795695942
* monetdb-1-2-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081742733312
  * CPU:AMD EPYC 7502 32-Core Processor
  * Cores:128
  * host:6.8.0-146-generic
  * node:cl-worker29
  * disk:707488
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
    * code:1795695942

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MonetDB-1-2

### Data Parameters of Reused Volumes
* MonetDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### Ingestion
* MonetDB-1: 50 of 50 units ok

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1795695942-6bcff796f7-jrsf5: 0
* bexhoma-sut-monetdb-1-1795695942-7bc554f8bf-lw7vt: 0

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
| MonetDB-1-1 |                1 |    1 |       63.00 |           3.00 |           19.00 |         13.00 |           18.00 |              8 |         0 |             | None           |             0 | False         |               57.14 | False               |
| MonetDB-1-2 |                2 |    1 |       63.00 |           3.00 |           19.00 |         13.00 |           18.00 |              8 |         0 |             | None           |             0 | False         |               57.14 | True                |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         12 |            0.11 |            38478.21 |           6600.00 |          -1 |
| monetdb-1-2-1-1-1 | monetdb-1-2-1 | monetdb-1-2-1-1 |                2 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         40 |            0.10 |            40913.80 |           1980.00 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         12 |            0.11 |            38478.21 |           6600.00 |          -1 |
| monetdb-1-2-1 | monetdb-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         40 |            0.10 |            40913.80 |           1980.00 |          -1 |

#### Query Completion per Phase

| phase         |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:--------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| monetdb-1-2-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   monetdb-1-1-1-1-1 |   monetdb-1-2-1-1-1 |
|:----------------------------------------------------|--------------------:|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |             1064.88 |              932.41 |
| Minimum Cost Supplier Query (TPC-H Q2)              |               30.43 |               32.64 |
| Shipping Priority (TPC-H Q3)                        |               91.51 |              104.69 |
| Order Priority Checking Query (TPC-H Q4)            |              143.42 |              148.33 |
| Local Supplier Volume (TPC-H Q5)                    |               68.67 |               67.75 |
| Forecasting Revenue Change (TPC-H Q6)               |               26.11 |               24.04 |
| Volume Shipping Query (TPC-H Q7)                    |               68.86 |               66.62 |
| National Market Share (TPC-H Q8)                    |              313.61 |              278.48 |
| Product Type Profit Measure (TPC-H Q9)              |               83.48 |               71.52 |
| Returned Item Reporting Query (TPC-H Q10)           |              153.17 |              165.67 |
| Important Stock Identification (TPC-H Q11)          |               19.57 |               15.32 |
| Shipping Modes and Order Priority (TPC-H Q12)       |               49.85 |               44.11 |
| Customer Distribution (TPC-H Q13)                   |              351.39 |              359.36 |
| Promotion Effect Query (TPC-H Q14)                  |               34.04 |               30.96 |
| Top Supplier Query (TPC-H Q15)                      |               35.12 |               32.07 |
| Parts/Supplier Relationship (TPC-H Q16)             |               80.60 |               88.11 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               56.99 |               51.74 |
| Large Volume Customer (TPC-H Q18)                   |              207.80 |              206.19 |
| Discounted Revenue (TPC-H Q19)                      |               77.67 |               68.40 |
| Potential Part Promotion (TPC-H Q20)                |               34.83 |               55.88 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |             1818.50 |             1038.36 |
| Global Sales Opportunity Query (TPC-H Q22)          |               57.09 |               39.37 |

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
* TEST passed: SUT pods not replaced
* TEST passed: Host information complete
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
* TEST passed: Results of all benchmarker pods
* TEST passed: Benchmarker pods without errors

Test successful!
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
* Duration: 302s 
* Code: 1795709263
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * A TPC-H refresh stream (RF1+RF2) runs in parallel, with 3 pair(s) applied per round.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [3] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * SUT requests 16 CPU and 64Gi RAM. CPU limit is 16. RAM limit is 64Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081742733312
  * CPU:AMD EPYC 7502 32-Core Processor
  * Cores:128
  * host:6.8.0-146-generic
  * node:cl-worker29
  * disk:735008
  * datadisk:2938
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795709263
* monetdb-1-1-1-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081742733312
  * CPU:AMD EPYC 7502 32-Core Processor
  * Cores:128
  * host:6.8.0-146-generic
  * node:cl-worker29
  * disk:735008
  * datadisk:2938
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795709263
* monetdb-1-1-1-1-3 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081742733312
  * CPU:AMD EPYC 7502 32-Core Processor
  * Cores:128
  * host:6.8.0-146-generic
  * node:cl-worker29
  * disk:735008
  * datadisk:2938
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795709263

### Ingestion
* MonetDB-1: 50 of 50 units ok

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1795709263-7747564d87-gkdpg: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |    1 |       65.00 |           2.00 |           21.00 |         14.00 |           18.00 |              8 |         0 |             | None           |             0 | False         |               55.38 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         10 |            0.11 |            33251.53 |           7920.00 |          -1 |
| monetdb-1-1-1-1-2 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       2 | 1.00 |               22 |                  22 |         10 |            0.10 |            35797.60 |           7920.00 |          -1 |
| monetdb-1-1-1-1-3 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       3 | 1.00 |               22 |                  22 |          8 |            0.11 |            33042.42 |           9900.00 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           3 | 1.00 |               66 |                  66 |         10 |            0.11 |            34007.85 |          23760.00 |          -1 |

#### Query Completion per Phase

| phase         |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:--------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| monetdb-1-1-1 |      3 | 3/3                                 | 3/3                                      | 3/3                            | 3/3                                        | 3/3                                | 3/3                                     | 3/3                                | 3/3                                | 3/3                                      | 3/3                                         | 3/3                                          | 3/3                                             | 3/3                                 | 3/3                                  | 3/3                              | 3/3                                       | 3/3                                        | 3/3                                 | 3/3                              | 3/3                                    | 3/3                                                   | 3/3                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### tpch_refresh

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count | benchmark_begin     | benchmark_end       |   benchmark_duration |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|:--------------------|:--------------------|---------------------:|
| monetdb-1-1-1-2-1 | monetdb-1-1-1 | monetdb-1-1-1-2 |                1 |        1 |               2 |           1 | 2026-11-26 17:12:18 | 2026-11-26 17:12:20 |                    2 |

### Latency of Timer Execution [ms]
| Queries                                             |   monetdb-1-1-1-1-1 |   monetdb-1-1-1-1-2 |   monetdb-1-1-1-1-3 |
|:----------------------------------------------------|--------------------:|--------------------:|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |             1304.67 |             1528.93 |             1470.80 |
| Minimum Cost Supplier Query (TPC-H Q2)              |              314.02 |               27.72 |               35.55 |
| Shipping Priority (TPC-H Q3)                        |              101.83 |               89.01 |              107.16 |
| Order Priority Checking Query (TPC-H Q4)            |              194.23 |              144.39 |              143.36 |
| Local Supplier Volume (TPC-H Q5)                    |               72.42 |               85.87 |               76.31 |
| Forecasting Revenue Change (TPC-H Q6)               |               26.80 |               24.21 |               25.77 |
| Volume Shipping Query (TPC-H Q7)                    |               77.52 |               71.01 |               98.03 |
| National Market Share (TPC-H Q8)                    |              216.19 |              190.20 |              330.28 |
| Product Type Profit Measure (TPC-H Q9)              |               77.62 |               81.24 |               92.34 |
| Returned Item Reporting Query (TPC-H Q10)           |              142.77 |              129.70 |              141.59 |
| Important Stock Identification (TPC-H Q11)          |               16.83 |               20.52 |               27.93 |
| Shipping Modes and Order Priority (TPC-H Q12)       |               50.87 |               50.76 |               50.87 |
| Customer Distribution (TPC-H Q13)                   |              334.70 |              350.76 |              359.96 |
| Promotion Effect Query (TPC-H Q14)                  |               34.57 |               33.66 |               34.92 |
| Top Supplier Query (TPC-H Q15)                      |               38.31 |               35.50 |               38.31 |
| Parts/Supplier Relationship (TPC-H Q16)             |               85.28 |               80.92 |               97.06 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               57.98 |               45.37 |               54.04 |
| Large Volume Customer (TPC-H Q18)                   |              168.02 |              190.30 |              186.04 |
| Discounted Revenue (TPC-H Q19)                      |               82.85 |               71.81 |               66.35 |
| Potential Part Promotion (TPC-H Q20)                |               34.56 |              174.72 |               32.98 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |             4026.73 |             4016.22 |             1449.75 |
| Global Sales Opportunity Query (TPC-H Q22)          |               54.04 |               45.72 |              465.62 |

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
* TEST passed: SUT pods not replaced
* TEST passed: Host information complete
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
* TEST passed: Results of all benchmarker pods
* TEST passed: Benchmarker pods without errors

Test successful!
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
Monitoring is activated (`-m`) for the SUT.
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
* Duration: 682s 
* Code: 1795697129
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
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
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:649072
  * datadisk:12124
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795697129

### Ingestion
* MonetDB-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1795697129-6648d55c88-vc2k8: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |    3 |      396.00 |           2.00 |            1.00 |        324.00 |           58.00 |              8 |         0 |             | None           |             0 | False         |               27.27 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 3.00 |               99 |                  99 |         41 |            0.09 |           123928.75 |          26078.05 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |         41 |            0.09 |           123928.75 |          26078.05 |          -1 |

#### Query Completion per Phase

| phase         |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:--------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   monetdb-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |               38.54 |
| TPC-DS Q2     |              294.23 |
| TPC-DS Q3     |               47.11 |
| TPC-DS Q4     |             1488.11 |
| TPC-DS Q5     |              143.63 |
| TPC-DS Q6     |               54.51 |
| TPC-DS Q7     |               56.91 |
| TPC-DS Q8     |               40.30 |
| TPC-DS Q9     |              107.29 |
| TPC-DS Q10    |               29.21 |
| TPC-DS Q11    |              528.91 |
| TPC-DS Q12    |               35.93 |
| TPC-DS Q13    |              122.93 |
| TPC-DS Q14a+b |             2552.39 |
| TPC-DS Q15    |               27.06 |
| TPC-DS Q16    |              124.98 |
| TPC-DS Q17    |              196.75 |
| TPC-DS Q18    |              100.22 |
| TPC-DS Q19    |               55.59 |
| TPC-DS Q20    |               64.63 |
| TPC-DS Q21    |              174.46 |
| TPC-DS Q22    |             1152.87 |
| TPC-DS Q23a+b |             1857.30 |
| TPC-DS Q24a+b |              339.46 |
| TPC-DS Q25    |              184.71 |
| TPC-DS Q26    |               29.99 |
| TPC-DS Q27    |              303.52 |
| TPC-DS Q28    |              186.15 |
| TPC-DS Q29    |              363.80 |
| TPC-DS Q30    |               21.56 |
| TPC-DS Q31    |              252.35 |
| TPC-DS Q32    |               25.70 |
| TPC-DS Q33    |               28.09 |
| TPC-DS Q34    |               38.14 |
| TPC-DS Q35    |               78.54 |
| TPC-DS Q36    |              140.84 |
| TPC-DS Q37    |              121.46 |
| TPC-DS Q38    |              217.34 |
| TPC-DS Q39a+b |             1008.98 |
| TPC-DS Q40    |               87.37 |
| TPC-DS Q41    |                9.81 |
| TPC-DS Q42    |               88.43 |
| TPC-DS Q43    |              114.73 |
| TPC-DS Q44    |              163.93 |
| TPC-DS Q45    |               16.18 |
| TPC-DS Q46    |               57.22 |
| TPC-DS Q47    |              193.59 |
| TPC-DS Q48    |               49.49 |
| TPC-DS Q49    |              121.77 |
| TPC-DS Q50    |              132.44 |
| TPC-DS Q51    |              437.61 |
| TPC-DS Q52    |               28.63 |
| TPC-DS Q53    |               32.74 |
| TPC-DS Q54    |               28.50 |
| TPC-DS Q55    |               33.13 |
| TPC-DS Q56    |               36.96 |
| TPC-DS Q57    |               72.26 |
| TPC-DS Q58    |               64.58 |
| TPC-DS Q59    |              125.64 |
| TPC-DS Q60    |               30.36 |
| TPC-DS Q61    |               49.74 |
| TPC-DS Q62    |               26.94 |
| TPC-DS Q63    |               32.71 |
| TPC-DS Q64    |              495.50 |
| TPC-DS Q65    |              114.16 |
| TPC-DS Q66    |               36.65 |
| TPC-DS Q67    |              429.70 |
| TPC-DS Q68    |               64.42 |
| TPC-DS Q69    |               23.43 |
| TPC-DS Q70    |               76.22 |
| TPC-DS Q71    |               39.45 |
| TPC-DS Q72    |              194.67 |
| TPC-DS Q73    |               36.96 |
| TPC-DS Q74    |              178.01 |
| TPC-DS Q75    |              458.79 |
| TPC-DS Q76    |               53.30 |
| TPC-DS Q77    |               92.70 |
| TPC-DS Q78    |              804.05 |
| TPC-DS Q79    |               59.96 |
| TPC-DS Q80    |              537.45 |
| TPC-DS Q81    |               29.70 |
| TPC-DS Q82    |              143.43 |
| TPC-DS Q83    |               15.03 |
| TPC-DS Q84    |               41.00 |
| TPC-DS Q85    |               35.66 |
| TPC-DS Q86    |               34.51 |
| TPC-DS Q87    |              198.40 |
| TPC-DS Q88    |              107.51 |
| TPC-DS Q89    |               45.08 |
| TPC-DS Q90    |                8.86 |
| TPC-DS Q91    |               13.91 |
| TPC-DS Q92    |               13.12 |
| TPC-DS Q93    |              117.46 |
| TPC-DS Q94    |               28.82 |
| TPC-DS Q95    |              450.16 |
| TPC-DS Q96    |               12.63 |
| TPC-DS Q97    |              228.94 |
| TPC-DS Q98    |               46.55 |
| TPC-DS Q99    |               41.88 |

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
* TEST passed: SUT pods not replaced
* TEST passed: Host information complete
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
* TEST passed: Results of all benchmarker pods
* TEST passed: Benchmarker pods without errors

Test successful!
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
  -ms $BEXHOMA_MS \
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
* Duration: 673s 
* Code: 1795697879
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
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
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:648960
  * datadisk:12126
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795697879

### Ingestion
* MonetDB-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1795697879-5f8fd5476f-ptlpm: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |    3 |      408.00 |           1.00 |            1.00 |        333.00 |           64.00 |              8 |         0 |             | None           |             0 | False         |               26.47 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 3.00 |               99 |                  99 |         32 |            0.09 |           122861.42 |          33412.50 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |         32 |            0.09 |           122861.42 |          33412.50 |          -1 |

#### Query Completion per Phase

| phase         |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:--------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   monetdb-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |               50.62 |
| TPC-DS Q2     |              301.59 |
| TPC-DS Q3     |               34.79 |
| TPC-DS Q4     |             1118.11 |
| TPC-DS Q5     |              135.40 |
| TPC-DS Q6     |               47.08 |
| TPC-DS Q7     |               52.43 |
| TPC-DS Q8     |               40.95 |
| TPC-DS Q9     |              103.25 |
| TPC-DS Q10    |               27.37 |
| TPC-DS Q11    |              527.48 |
| TPC-DS Q12    |               25.62 |
| TPC-DS Q13    |               86.47 |
| TPC-DS Q14a+b |             2965.01 |
| TPC-DS Q15    |               34.10 |
| TPC-DS Q16    |              114.96 |
| TPC-DS Q17    |              216.89 |
| TPC-DS Q18    |              101.26 |
| TPC-DS Q19    |               59.72 |
| TPC-DS Q20    |               27.41 |
| TPC-DS Q21    |              110.52 |
| TPC-DS Q22    |              976.03 |
| TPC-DS Q23a+b |             3198.66 |
| TPC-DS Q24a+b |              285.96 |
| TPC-DS Q25    |              143.49 |
| TPC-DS Q26    |               33.43 |
| TPC-DS Q27    |              141.72 |
| TPC-DS Q28    |               80.21 |
| TPC-DS Q29    |              144.24 |
| TPC-DS Q30    |               18.08 |
| TPC-DS Q31    |              186.17 |
| TPC-DS Q32    |               21.68 |
| TPC-DS Q33    |               31.97 |
| TPC-DS Q34    |               36.60 |
| TPC-DS Q35    |               95.22 |
| TPC-DS Q36    |              369.49 |
| TPC-DS Q37    |              104.10 |
| TPC-DS Q38    |              199.89 |
| TPC-DS Q39a+b |             1158.90 |
| TPC-DS Q40    |               68.40 |
| TPC-DS Q41    |                7.86 |
| TPC-DS Q42    |               38.33 |
| TPC-DS Q43    |               73.59 |
| TPC-DS Q44    |               53.50 |
| TPC-DS Q45    |               16.44 |
| TPC-DS Q46    |               58.62 |
| TPC-DS Q47    |              204.64 |
| TPC-DS Q48    |               55.68 |
| TPC-DS Q49    |              137.90 |
| TPC-DS Q50    |              157.10 |
| TPC-DS Q51    |              466.79 |
| TPC-DS Q52    |               30.65 |
| TPC-DS Q53    |               42.62 |
| TPC-DS Q54    |               34.25 |
| TPC-DS Q55    |               26.68 |
| TPC-DS Q56    |               45.19 |
| TPC-DS Q57    |              142.15 |
| TPC-DS Q58    |              168.87 |
| TPC-DS Q59    |              182.96 |
| TPC-DS Q60    |               27.79 |
| TPC-DS Q61    |               46.82 |
| TPC-DS Q62    |               29.59 |
| TPC-DS Q63    |               34.07 |
| TPC-DS Q64    |              474.32 |
| TPC-DS Q65    |              147.02 |
| TPC-DS Q66    |               39.10 |
| TPC-DS Q67    |              451.76 |
| TPC-DS Q68    |               69.30 |
| TPC-DS Q69    |               33.69 |
| TPC-DS Q70    |               79.90 |
| TPC-DS Q71    |               42.67 |
| TPC-DS Q72    |              226.07 |
| TPC-DS Q73    |               34.22 |
| TPC-DS Q74    |              187.76 |
| TPC-DS Q75    |              494.37 |
| TPC-DS Q76    |               47.81 |
| TPC-DS Q77    |               92.61 |
| TPC-DS Q78    |              892.08 |
| TPC-DS Q79    |               77.73 |
| TPC-DS Q80    |             1038.25 |
| TPC-DS Q81    |               54.69 |
| TPC-DS Q82    |              239.38 |
| TPC-DS Q83    |               13.81 |
| TPC-DS Q84    |               51.39 |
| TPC-DS Q85    |               29.38 |
| TPC-DS Q86    |               23.96 |
| TPC-DS Q87    |              245.81 |
| TPC-DS Q88    |               96.45 |
| TPC-DS Q89    |               47.73 |
| TPC-DS Q90    |                9.24 |
| TPC-DS Q91    |               16.00 |
| TPC-DS Q92    |               13.80 |
| TPC-DS Q93    |              155.05 |
| TPC-DS Q94    |               34.50 |
| TPC-DS Q95    |              472.92 |
| TPC-DS Q96    |               20.17 |
| TPC-DS Q97    |              221.39 |
| TPC-DS Q98    |               72.97 |
| TPC-DS Q99    |               58.14 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |       331.01 |      1.06 |          10.09 |                 11.97 |

### Loading phase: component data generator

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        54.40 |      0.20 |           0.01 |                  2.65 |

### Benchmarking phase: SUT deployment

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 | n/a          |      2.74 |          14.33 |                 16.21 |

### Benchmarking phase: component benchmarker

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 | n/a          |         0 |           0.30 |                  0.30 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
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
* TEST passed: SUT pods not replaced
* TEST passed: Host information complete
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Benchmarking phase: SUT deployment contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Benchmarking phase: component benchmarker contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST passed: Monitoring returned data
* TEST skipped: Monitoring metrics missing (data pre-existing; phase shorter than scrape interval; series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
* TEST passed: Results of all benchmarker pods
* TEST passed: Benchmarker pods without errors

Test successful!
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
  -ms $BEXHOMA_MS \
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
* Duration: 1144s 
* Code: 1795698644
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
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
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:637000
  * datadisk:12121
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
    * code:1795698644
* monetdb-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:637000
  * datadisk:12345
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
    * code:1795698644
* monetdb-1-1-2-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:637000
  * datadisk:12345
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
    * code:1795698644
* monetdb-1-2-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:637001
  * datadisk:10224
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
    * code:1795698644
* monetdb-1-2-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:637002
  * datadisk:10398
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
    * code:1795698644
* monetdb-1-2-2-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:637002
  * datadisk:10398
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
    * code:1795698644

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MonetDB-1-2

### Data Parameters of Reused Volumes
* MonetDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### Ingestion
* MonetDB-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1795698644-ff6465448-c5f4h: 0
* bexhoma-sut-monetdb-1-1795698644-7bc6bf6946-sr88d: 0

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
| MonetDB-1-1 |                1 |    3 |      365.00 |           2.00 |            1.00 |        295.00 |           56.00 |              8 |         0 |             | None           |             0 | False         |               29.59 | False               |
| MonetDB-1-2 |                2 |    3 |      365.00 |           2.00 |            1.00 |        295.00 |           56.00 |              8 |         0 |             | None           |             0 | False         |               29.59 | True                |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 3.00 |               99 |                  99 |         34 |            0.09 |           117806.71 |          31447.06 |          -1 |
| monetdb-1-1-2-1-1 | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |       1 | 3.00 |               99 |                  99 |         32 |            0.09 |           119296.26 |          33412.50 |          -1 |
| monetdb-1-1-2-1-2 | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |       2 | 3.00 |               99 |                  99 |         33 |            0.09 |           125871.28 |          32400.00 |          -1 |
| monetdb-1-2-1-1-1 | monetdb-1-2-1 | monetdb-1-2-1-1 |                2 |        1 |               1 |       1 | 3.00 |               99 |                  99 |         64 |            0.11 |            94010.03 |          16706.25 |          -1 |
| monetdb-1-2-2-1-1 | monetdb-1-2-2 | monetdb-1-2-2-1 |                2 |        2 |               1 |       1 | 3.00 |               99 |                  99 |         49 |            0.08 |           137093.93 |          21820.41 |          -1 |
| monetdb-1-2-2-1-2 | monetdb-1-2-2 | monetdb-1-2-2-1 |                2 |        2 |               1 |       2 | 3.00 |               99 |                  99 |         42 |            0.08 |           132371.56 |          25457.14 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |         34 |            0.09 |           117806.71 |          31447.06 |          -1 |
| monetdb-1-1-2 | monetdb-1-1-2 |                1 |        2 |               1 |           2 | 3.00 |              198 |                 198 |         33 |            0.09 |           122539.68 |          64800.00 |          -1 |
| monetdb-1-2-1 | monetdb-1-2-1 |                2 |        1 |               1 |           1 | 3.00 |               99 |                  99 |         64 |            0.11 |            94010.03 |          16706.25 |          -1 |
| monetdb-1-2-2 | monetdb-1-2-2 |                2 |        2 |               1 |           2 | 3.00 |              198 |                 198 |         49 |            0.08 |           134712.05 |          43640.82 |          -1 |

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
| TPC-DS Q1     |              183.70 |               52.40 |              187.95 |              339.08 |               36.28 |              185.55 |
| TPC-DS Q2     |              152.28 |              250.88 |              112.42 |              557.37 |              116.15 |              133.47 |
| TPC-DS Q3     |               32.23 |               58.84 |               33.83 |              793.25 |               38.60 |               26.53 |
| TPC-DS Q4     |             1845.73 |             1298.96 |             1176.34 |             3115.71 |             1169.68 |             1210.02 |
| TPC-DS Q5     |              158.04 |              113.91 |              113.40 |             3098.89 |              120.26 |              107.90 |
| TPC-DS Q6     |               48.25 |               45.81 |               43.38 |              197.61 |               51.08 |               45.22 |
| TPC-DS Q7     |               51.25 |               58.29 |               47.99 |             1617.73 |               56.97 |               52.41 |
| TPC-DS Q8     |               43.49 |               39.60 |               36.49 |               53.48 |               45.88 |               31.45 |
| TPC-DS Q9     |              101.33 |              101.13 |              107.10 |              349.33 |              148.36 |              129.68 |
| TPC-DS Q10    |               27.87 |               28.04 |               36.99 |             5382.62 |               49.25 |               52.95 |
| TPC-DS Q11    |              660.29 |              533.21 |              570.13 |              630.92 |              674.98 |              660.82 |
| TPC-DS Q12    |               22.77 |               25.13 |               30.09 |               46.90 |               29.77 |               28.88 |
| TPC-DS Q13    |               71.71 |               67.64 |               88.25 |               92.16 |               94.74 |               90.73 |
| TPC-DS Q14a+b |             2746.04 |             2258.98 |             2763.90 |             2749.86 |             2172.73 |             2160.95 |
| TPC-DS Q15    |               23.85 |               53.89 |               35.25 |               34.63 |               28.79 |               24.55 |
| TPC-DS Q16    |              115.98 |              205.67 |              149.02 |              362.49 |              122.03 |              122.81 |
| TPC-DS Q17    |              165.43 |              283.18 |              172.42 |              468.69 |              172.28 |              158.59 |
| TPC-DS Q18    |              104.78 |              219.47 |              107.65 |              121.94 |               83.40 |              116.45 |
| TPC-DS Q19    |               54.02 |               84.23 |               49.63 |               58.20 |               61.48 |               59.69 |
| TPC-DS Q20    |               27.96 |               37.33 |               23.84 |               28.61 |               29.17 |               23.58 |
| TPC-DS Q21    |              105.11 |              120.47 |              116.67 |             2241.24 |               99.41 |              112.09 |
| TPC-DS Q22    |              935.29 |              929.38 |              970.07 |             1716.17 |              948.42 |              947.69 |
| TPC-DS Q23a+b |             3016.14 |             2545.62 |             2683.23 |             2618.61 |             3311.36 |             2639.02 |
| TPC-DS Q24a+b |              511.93 |              272.31 |              348.89 |              298.36 |              410.76 |              257.31 |
| TPC-DS Q25    |              311.70 |              185.32 |              187.51 |              190.01 |              191.71 |              193.95 |
| TPC-DS Q26    |               31.80 |               30.90 |               61.16 |               36.33 |               33.91 |               74.48 |
| TPC-DS Q27    |              193.54 |              153.78 |              205.69 |              187.25 |              148.04 |              500.38 |
| TPC-DS Q28    |               86.22 |               97.12 |              142.11 |               87.55 |               87.55 |              194.67 |
| TPC-DS Q29    |              201.40 |              211.51 |              329.28 |              173.77 |              167.37 |              372.62 |
| TPC-DS Q30    |               18.07 |               18.07 |               22.75 |               27.29 |               20.18 |               15.76 |
| TPC-DS Q31    |              169.38 |              421.85 |              344.88 |              163.89 |              154.83 |              131.37 |
| TPC-DS Q32    |               20.23 |               32.36 |               24.43 |               22.61 |               21.18 |               26.59 |
| TPC-DS Q33    |               40.70 |               46.44 |               29.21 |               32.26 |               28.03 |               36.27 |
| TPC-DS Q34    |               36.42 |               51.22 |               56.61 |               41.49 |               39.08 |               44.22 |
| TPC-DS Q35    |               88.97 |              203.90 |               79.48 |               94.12 |               85.32 |               75.59 |
| TPC-DS Q36    |              174.31 |              318.26 |              136.29 |              162.69 |              147.32 |              171.55 |
| TPC-DS Q37    |              138.42 |              139.10 |               79.10 |              136.44 |               78.43 |              105.62 |
| TPC-DS Q38    |              215.54 |              302.70 |              250.74 |              220.64 |              274.29 |              183.30 |
| TPC-DS Q39a+b |             1611.85 |              998.83 |             1012.83 |             1037.51 |              897.14 |              892.91 |
| TPC-DS Q40    |              148.26 |               88.57 |               89.41 |               37.57 |               36.51 |               37.62 |
| TPC-DS Q41    |                8.50 |               10.30 |                4.97 |                3.57 |               10.90 |                6.06 |
| TPC-DS Q42    |               30.77 |               38.05 |               27.64 |               28.64 |               28.45 |               30.71 |
| TPC-DS Q43    |               63.95 |               69.48 |               74.18 |               69.55 |               69.79 |               70.86 |
| TPC-DS Q44    |               48.98 |               49.11 |               52.10 |               49.07 |               48.52 |               49.32 |
| TPC-DS Q45    |               17.44 |               13.10 |               15.14 |               20.45 |               16.44 |               21.74 |
| TPC-DS Q46    |               54.44 |               55.15 |               97.22 |               60.92 |               62.86 |               67.81 |
| TPC-DS Q47    |              219.62 |              210.87 |              208.58 |              204.45 |              188.73 |              204.89 |
| TPC-DS Q48    |               52.26 |               59.53 |               54.30 |               58.03 |               56.69 |               53.08 |
| TPC-DS Q49    |              125.35 |              112.31 |              105.31 |              323.45 |              114.56 |              111.00 |
| TPC-DS Q50    |              131.75 |              148.99 |              165.40 |              153.73 |              135.22 |              144.30 |
| TPC-DS Q51    |              512.55 |              493.41 |              809.67 |              883.55 |              508.64 |              474.22 |
| TPC-DS Q52    |               34.16 |               40.33 |               48.54 |               31.58 |               29.94 |               25.95 |
| TPC-DS Q53    |               36.84 |               29.23 |               48.70 |               35.51 |               30.53 |               33.79 |
| TPC-DS Q54    |               90.57 |               30.00 |               55.87 |               27.36 |               29.71 |               31.87 |
| TPC-DS Q55    |               28.18 |               33.44 |               32.00 |               26.26 |               28.58 |               26.28 |
| TPC-DS Q56    |               47.94 |               27.52 |               51.08 |               57.90 |               31.21 |               30.14 |
| TPC-DS Q57    |              140.84 |               72.58 |               69.84 |               65.61 |              142.17 |               73.63 |
| TPC-DS Q58    |              133.31 |              166.67 |               44.30 |               83.16 |               76.79 |               44.36 |
| TPC-DS Q59    |              184.81 |              211.88 |              123.45 |              127.61 |              118.33 |              126.70 |
| TPC-DS Q60    |               28.43 |               51.09 |               33.68 |               27.19 |               32.20 |               25.73 |
| TPC-DS Q61    |               85.11 |              105.40 |               54.54 |               52.40 |               65.88 |               48.53 |
| TPC-DS Q62    |               34.17 |               34.22 |               33.39 |               32.79 |               28.59 |               27.53 |
| TPC-DS Q63    |               34.22 |               26.09 |               29.48 |               30.46 |               29.87 |               27.51 |
| TPC-DS Q64    |              445.78 |              313.34 |              295.02 |              475.25 |              298.81 |              313.24 |
| TPC-DS Q65    |              124.72 |              116.39 |              117.57 |              116.09 |              140.73 |              134.39 |
| TPC-DS Q66    |               46.85 |               47.18 |               55.52 |               46.26 |               38.49 |               56.92 |
| TPC-DS Q67    |              460.98 |              475.53 |              458.72 |              472.40 |              550.92 |              483.58 |
| TPC-DS Q68    |               70.87 |               84.69 |               86.10 |               61.03 |               63.87 |               74.07 |
| TPC-DS Q69    |               19.67 |               18.79 |               23.23 |               20.76 |               16.65 |               16.29 |
| TPC-DS Q70    |               93.72 |               85.90 |               69.20 |               89.99 |               69.74 |               97.47 |
| TPC-DS Q71    |               40.35 |               46.46 |               47.35 |               51.64 |               45.41 |               42.17 |
| TPC-DS Q72    |              211.61 |              189.66 |              206.65 |              295.70 |              187.80 |              194.34 |
| TPC-DS Q73    |               32.82 |               36.29 |               32.37 |               33.76 |               33.98 |               35.92 |
| TPC-DS Q74    |              178.34 |              169.10 |              166.10 |              143.86 |              175.77 |              155.51 |
| TPC-DS Q75    |              554.76 |              496.50 |              476.49 |              469.80 |              451.59 |             1230.08 |
| TPC-DS Q76    |               69.07 |               57.42 |               49.47 |              620.02 |               54.35 |              104.13 |
| TPC-DS Q77    |               88.72 |               81.25 |               92.38 |               82.09 |               85.70 |               88.69 |
| TPC-DS Q78    |              907.74 |              771.48 |              873.49 |              822.10 |              739.51 |              755.98 |
| TPC-DS Q79    |               60.33 |               73.02 |               67.49 |               56.38 |               62.31 |               67.58 |
| TPC-DS Q80    |              584.46 |              890.68 |             1291.91 |              520.94 |              608.33 |              553.76 |
| TPC-DS Q81    |               31.87 |               31.89 |               28.99 |               32.94 |               42.35 |               26.22 |
| TPC-DS Q82    |              333.53 |              109.77 |              100.66 |              164.13 |              128.96 |               77.40 |
| TPC-DS Q83    |               22.99 |               14.04 |                9.60 |               11.98 |               14.53 |               10.66 |
| TPC-DS Q84    |               53.46 |               19.77 |               10.04 |               37.70 |                9.24 |               10.08 |
| TPC-DS Q85    |               48.17 |               44.89 |               28.61 |               30.25 |               27.50 |               32.11 |
| TPC-DS Q86    |               50.55 |               25.55 |               28.00 |               26.02 |               24.14 |               25.40 |
| TPC-DS Q87    |              267.44 |              224.72 |              222.45 |              203.91 |              202.24 |              200.73 |
| TPC-DS Q88    |               89.05 |               83.05 |               92.73 |              147.24 |               87.53 |               94.89 |
| TPC-DS Q89    |               45.96 |               47.97 |               47.56 |               73.58 |               45.26 |               49.67 |
| TPC-DS Q90    |               10.72 |                9.60 |               11.11 |               15.92 |                8.43 |               10.08 |
| TPC-DS Q91    |               15.71 |               14.09 |               16.35 |               17.54 |               14.03 |               16.09 |
| TPC-DS Q92    |               20.43 |               19.63 |               15.82 |               18.78 |               12.44 |               16.41 |
| TPC-DS Q93    |              137.84 |              134.38 |              139.17 |              139.87 |              132.48 |              109.75 |
| TPC-DS Q94    |               36.06 |               32.14 |               31.36 |               32.14 |               28.21 |               29.35 |
| TPC-DS Q95    |              481.86 |              460.12 |              484.11 |              474.26 |              419.48 |              444.62 |
| TPC-DS Q96    |               15.84 |               20.49 |               20.15 |               14.11 |               13.34 |               12.53 |
| TPC-DS Q97    |              241.26 |              233.05 |              249.85 |              234.99 |              272.12 |              244.61 |
| TPC-DS Q98    |               47.34 |               52.29 |               43.67 |               41.60 |               46.65 |               46.25 |
| TPC-DS Q99    |               41.15 |               47.02 |               44.54 |               38.11 |               36.39 |               39.34 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |       298.37 |      1.54 |           7.38 |                  8.38 |
| monetdb-1-1-2-1 |       298.37 |      1.54 |           7.38 |                  8.38 |

### Loading phase: component data generator

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |
| monetdb-1-1-2-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        32.42 |      0.15 |           0.01 |                  2.65 |
| monetdb-1-1-2-1 |        32.42 |      0.15 |           0.01 |                  2.65 |

### Benchmarking phase: SUT deployment

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 | n/a          |      3.98 |          15.73 |                 17.61 |
| monetdb-1-1-2-1 | n/a          |      2.74 |          19.25 |                 21.13 |
| monetdb-1-2-1-1 | 77.68        |     10.16 |           7.98 |                  7.98 |
| monetdb-1-2-2-1 | 239.50       |      7.88 |          13.97 |                 13.98 |

### Benchmarking phase: component benchmarker

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 | n/a          |      0.00 |           0.28 |                  0.28 |
| monetdb-1-1-2-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| monetdb-1-2-1-1 | 14.34        |      0.04 |           0.29 |                  0.29 |
| monetdb-1-2-2-1 | 28.56        |      1.17 |           0.31 |                  0.32 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
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
* CPU Throttling Rate [s/s] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-2-1-1 (bexhoma-metrics-monetdb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-2-1-1 (bexhoma-metrics-monetdb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
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
* TEST passed: SUT pods not replaced
* TEST passed: Host information complete
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Monitoring returned data
* TEST skipped: Monitoring metrics missing (data pre-existing; phase shorter than scrape interval; series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
* TEST passed: Results of all benchmarker pods
* TEST passed: Benchmarker pods without errors

Test successful!
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
Monitoring is activated (`-m`) for the SUT.
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
* Duration: 2705s 
* Code: 1795699946
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=30) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 14400.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
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
  * disk:641228
  * datadisk:75453
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
    * code:1795699946

### Ingestion
* MonetDB-1: 81 of 81 units ok

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1795699946-849799f656-6jzpp: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |   30 |     1661.00 |           3.00 |          717.00 |        409.00 |          527.00 |              8 |         0 |             | None           |             0 | False         |               65.02 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 30.00 |               99 |                  99 |        770 |            0.64 |           176944.41 |          13885.71 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        770 |            0.64 |           176944.41 |          13885.71 |          -1 |

#### Query Completion per Phase

| phase         |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:--------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   monetdb-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |              333.65 |
| TPC-DS Q2     |             1444.14 |
| TPC-DS Q3     |               98.29 |
| TPC-DS Q4     |            16417.19 |
| TPC-DS Q5     |             2143.36 |
| TPC-DS Q6     |              329.95 |
| TPC-DS Q7     |              156.22 |
| TPC-DS Q8     |              322.83 |
| TPC-DS Q9     |              601.32 |
| TPC-DS Q10    |              118.31 |
| TPC-DS Q11    |             7008.07 |
| TPC-DS Q12    |              150.44 |
| TPC-DS Q13    |              295.29 |
| TPC-DS Q14a+b |            32984.47 |
| TPC-DS Q15    |              150.40 |
| TPC-DS Q16    |            47186.66 |
| TPC-DS Q17    |             2739.83 |
| TPC-DS Q18    |             1014.14 |
| TPC-DS Q19    |              176.68 |
| TPC-DS Q20    |              118.36 |
| TPC-DS Q21    |              115.94 |
| TPC-DS Q22    |             1279.83 |
| TPC-DS Q23a+b |            43291.70 |
| TPC-DS Q24a+b |            15477.31 |
| TPC-DS Q25    |             1613.78 |
| TPC-DS Q26    |              169.17 |
| TPC-DS Q27    |             1714.16 |
| TPC-DS Q28    |              585.17 |
| TPC-DS Q29    |             2415.37 |
| TPC-DS Q30    |               82.10 |
| TPC-DS Q31    |             1898.51 |
| TPC-DS Q32    |              130.59 |
| TPC-DS Q33    |              119.00 |
| TPC-DS Q34    |              241.79 |
| TPC-DS Q35    |              783.34 |
| TPC-DS Q36    |             1398.99 |
| TPC-DS Q37    |              467.53 |
| TPC-DS Q38    |             3050.11 |
| TPC-DS Q39a+b |             1222.87 |
| TPC-DS Q40    |             1032.24 |
| TPC-DS Q41    |                5.22 |
| TPC-DS Q42    |              118.39 |
| TPC-DS Q43    |              431.37 |
| TPC-DS Q44    |              245.65 |
| TPC-DS Q45    |              128.47 |
| TPC-DS Q46    |              200.28 |
| TPC-DS Q47    |              883.60 |
| TPC-DS Q48    |              234.82 |
| TPC-DS Q49    |             1164.14 |
| TPC-DS Q50    |              581.60 |
| TPC-DS Q51    |             3323.06 |
| TPC-DS Q52    |               77.42 |
| TPC-DS Q53    |              100.96 |
| TPC-DS Q54    |               99.67 |
| TPC-DS Q55    |               67.40 |
| TPC-DS Q56    |              171.66 |
| TPC-DS Q57    |              142.86 |
| TPC-DS Q58    |              575.34 |
| TPC-DS Q59    |             1108.30 |
| TPC-DS Q60    |              157.97 |
| TPC-DS Q61    |              409.05 |
| TPC-DS Q62    |              280.64 |
| TPC-DS Q63    |               96.57 |
| TPC-DS Q64    |             4889.03 |
| TPC-DS Q65    |             1284.79 |
| TPC-DS Q66    |              414.29 |
| TPC-DS Q67    |             6740.96 |
| TPC-DS Q68    |              214.18 |
| TPC-DS Q69    |              451.69 |
| TPC-DS Q70    |             1697.82 |
| TPC-DS Q71    |              184.65 |
| TPC-DS Q72    |             1292.65 |
| TPC-DS Q73    |              100.00 |
| TPC-DS Q74    |             2875.23 |
| TPC-DS Q75    |             7024.69 |
| TPC-DS Q76    |              410.25 |
| TPC-DS Q77    |              915.15 |
| TPC-DS Q78    |            14088.62 |
| TPC-DS Q79    |              233.55 |
| TPC-DS Q80    |             8790.73 |
| TPC-DS Q81    |              137.17 |
| TPC-DS Q82    |              474.89 |
| TPC-DS Q83    |               56.15 |
| TPC-DS Q84    |               31.01 |
| TPC-DS Q85    |              309.61 |
| TPC-DS Q86    |              331.17 |
| TPC-DS Q87    |             3972.36 |
| TPC-DS Q88    |              466.65 |
| TPC-DS Q89    |              156.83 |
| TPC-DS Q90    |               91.06 |
| TPC-DS Q91    |               31.93 |
| TPC-DS Q92    |              139.71 |
| TPC-DS Q93    |             2166.66 |
| TPC-DS Q94    |            40731.30 |
| TPC-DS Q95    |           432418.40 |
| TPC-DS Q96    |              789.19 |
| TPC-DS Q97    |             4456.90 |
| TPC-DS Q98    |              704.90 |
| TPC-DS Q99    |              421.26 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      3053.48 |      8.33 |          71.54 |                 71.55 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      5493.07 |      8.00 |           0.02 |                  6.16 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |       290.73 |      0.91 |           0.00 |                  0.00 |

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |     12391.79 |    128.96 |         982.14 |               1023.86 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        33.34 |      0.23 |           0.37 |                  0.38 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
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
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: SUT pods not replaced
* TEST passed: Host information complete
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component data generator contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Monitoring returned data
* TEST skipped: Monitoring metrics missing (data pre-existing; series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
* TEST passed: Results of all benchmarker pods
* TEST passed: Benchmarker pods without errors

Test successful!
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
* Duration: 3502s 
* Code: 1795702762
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=30) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 14400.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
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
  * disk:643772
  * datadisk:76689
  * volume_size:2.9T
  * volume_used:75G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1795702762
* monetdb-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:642168
  * datadisk:75265
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1795702762
* monetdb-1-2-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:641737
  * datadisk:75265
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1795702762
* monetdb-1-2-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:639207
  * datadisk:75265
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1795702762

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MonetDB-1

### Data Parameters of Reused Volumes
* MonetDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1795702762-9d94b448f-9xdpp: 0
* bexhoma-sut-monetdb-1-1795702762-6dd8db8d9d-5q6md: 0

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
| MonetDB-1-1 |                1 |   30 |     1661.00 |           3.00 |          717.00 |        409.00 |          527.00 |              0 |         0 |             | None           |             0 | False         |               65.02 | True                |
| MonetDB-1-2 |                2 |   30 |     1661.00 |           3.00 |          717.00 |        409.00 |          527.00 |              0 |         0 |             | None           |             0 | False         |               65.02 | True                |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 30.00 |               99 |                  99 |        771 |            0.95 |           117837.71 |          13867.70 |          -1 |
| monetdb-1-1-2-1-1 | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |       1 | 30.00 |               99 |                  99 |        719 |            0.82 |           136575.06 |          14870.65 |          -1 |
| monetdb-1-2-1-1-1 | monetdb-1-2-1 | monetdb-1-2-1-1 |                2 |        1 |               1 |       1 | 30.00 |               99 |                  99 |        798 |            1.03 |           108551.75 |          13398.50 |          -1 |
| monetdb-1-2-2-1-1 | monetdb-1-2-2 | monetdb-1-2-2-1 |                2 |        2 |               1 |       1 | 30.00 |               99 |                  99 |        717 |            0.81 |           138212.18 |          14912.13 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        771 |            0.95 |           117837.71 |          13867.70 |          -1 |
| monetdb-1-1-2 | monetdb-1-1-2 |                1 |        2 |               1 |           1 | 30.00 |               99 |                  99 |        719 |            0.82 |           136575.06 |          14870.65 |          -1 |
| monetdb-1-2-1 | monetdb-1-2-1 |                2 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        798 |            1.03 |           108551.75 |          13398.50 |          -1 |
| monetdb-1-2-2 | monetdb-1-2-2 |                2 |        2 |               1 |           1 | 30.00 |               99 |                  99 |        717 |            0.81 |           138212.18 |          14912.13 |          -1 |

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
| TPC-DS Q1     |             1341.55 |              457.58 |             1466.27 |              492.45 |
| TPC-DS Q2     |             3327.24 |             1795.05 |             4345.79 |             2037.65 |
| TPC-DS Q3     |             2372.47 |              173.34 |             2508.90 |              187.09 |
| TPC-DS Q4     |            26658.60 |            19834.84 |            28360.69 |            18496.05 |
| TPC-DS Q5     |            16215.78 |             2001.10 |            19088.98 |             2175.34 |
| TPC-DS Q6     |              673.90 |              367.80 |              622.67 |              307.93 |
| TPC-DS Q7     |             4054.13 |             1221.24 |             4985.37 |             1065.23 |
| TPC-DS Q8     |             3354.97 |              385.98 |             3589.07 |              441.56 |
| TPC-DS Q9     |             1165.48 |              637.42 |             1308.58 |              834.01 |
| TPC-DS Q10    |            17725.51 |              429.41 |            19037.93 |              541.14 |
| TPC-DS Q11    |             6800.44 |             8105.68 |             8608.68 |             6991.31 |
| TPC-DS Q12    |              226.26 |              165.82 |              265.34 |              146.97 |
| TPC-DS Q13    |              432.15 |              569.31 |              492.89 |              551.05 |
| TPC-DS Q14a+b |            33704.96 |            37053.90 |            35515.44 |            33793.78 |
| TPC-DS Q15    |              166.92 |              131.16 |              148.05 |              135.22 |
| TPC-DS Q16    |            47236.20 |            47699.86 |            48986.56 |            45405.35 |
| TPC-DS Q17    |             3849.59 |             4092.80 |             3647.47 |             3043.41 |
| TPC-DS Q18    |             1871.48 |             1940.15 |             2151.98 |             1929.26 |
| TPC-DS Q19    |              172.44 |              162.84 |              171.82 |              150.49 |
| TPC-DS Q20    |              117.20 |              116.97 |              295.35 |              201.11 |
| TPC-DS Q21    |             1959.42 |              173.33 |             2112.45 |              217.82 |
| TPC-DS Q22    |             1794.56 |             2690.07 |             1861.05 |             1771.92 |
| TPC-DS Q23a+b |            49866.66 |            57020.41 |            60009.82 |            60594.55 |
| TPC-DS Q24a+b |            16962.81 |            18471.33 |            17230.67 |            19046.27 |
| TPC-DS Q25    |             2333.17 |             2716.17 |             2704.10 |             2490.68 |
| TPC-DS Q26    |              176.77 |              188.45 |              198.33 |              248.19 |
| TPC-DS Q27    |             1378.83 |             1471.78 |             1368.34 |             1343.16 |
| TPC-DS Q28    |              735.71 |              718.39 |              731.72 |              682.62 |
| TPC-DS Q29    |             2604.81 |             2962.37 |             3015.00 |             2346.12 |
| TPC-DS Q30    |              109.19 |              124.83 |              130.78 |              168.30 |
| TPC-DS Q31    |             2155.48 |             2264.06 |             2330.90 |             2853.49 |
| TPC-DS Q32    |              139.96 |              292.83 |              128.76 |              190.71 |
| TPC-DS Q33    |              136.83 |              179.44 |              529.23 |              165.57 |
| TPC-DS Q34    |              316.06 |              187.14 |              458.31 |              118.44 |
| TPC-DS Q35    |              757.17 |              862.43 |              786.79 |              709.77 |
| TPC-DS Q36    |             1598.95 |             1532.74 |             1343.08 |             1707.02 |
| TPC-DS Q37    |             2719.54 |             2935.28 |             2643.71 |             2198.11 |
| TPC-DS Q38    |             2380.79 |             2590.87 |             3098.64 |             3325.73 |
| TPC-DS Q39a+b |             1384.50 |             1984.19 |             1510.90 |             1423.37 |
| TPC-DS Q40    |              421.32 |              626.37 |              452.23 |              600.99 |
| TPC-DS Q41    |                5.29 |                5.82 |                5.31 |                5.31 |
| TPC-DS Q42    |              121.65 |               93.93 |              107.77 |              114.41 |
| TPC-DS Q43    |              424.10 |              328.03 |              506.25 |              298.11 |
| TPC-DS Q44    |            12716.99 |             8041.71 |             8875.68 |             7020.22 |
| TPC-DS Q45    |              223.55 |              140.39 |              138.93 |              152.83 |
| TPC-DS Q46    |              205.59 |              190.33 |              196.51 |              201.83 |
| TPC-DS Q47    |              885.26 |              841.54 |              875.81 |              930.27 |
| TPC-DS Q48    |              216.69 |              213.44 |              227.78 |              206.97 |
| TPC-DS Q49    |             4942.85 |             1622.64 |             4378.04 |             1574.21 |
| TPC-DS Q50    |              578.53 |              606.88 |              716.37 |              561.23 |
| TPC-DS Q51    |             2431.98 |             2924.44 |             2481.23 |             3123.50 |
| TPC-DS Q52    |               78.72 |              122.31 |              121.19 |              117.48 |
| TPC-DS Q53    |               97.03 |               93.47 |              101.66 |              104.05 |
| TPC-DS Q54    |              110.69 |               94.72 |               95.02 |               92.85 |
| TPC-DS Q55    |               78.47 |               85.60 |               72.80 |               60.95 |
| TPC-DS Q56    |              170.05 |              165.54 |              161.24 |              165.81 |
| TPC-DS Q57    |              146.48 |              141.21 |              133.72 |              134.95 |
| TPC-DS Q58    |              565.49 |              570.51 |              541.22 |              547.10 |
| TPC-DS Q59    |             1131.95 |             1822.94 |             1104.47 |             1622.14 |
| TPC-DS Q60    |              157.22 |              194.21 |              309.44 |              180.55 |
| TPC-DS Q61    |              172.42 |              167.21 |              360.76 |              161.85 |
| TPC-DS Q62    |              428.73 |              438.94 |              488.07 |              398.00 |
| TPC-DS Q63    |               97.05 |              108.67 |              129.82 |              103.59 |
| TPC-DS Q64    |             5527.41 |             5250.18 |             5100.00 |             4968.52 |
| TPC-DS Q65    |             1558.48 |             1098.69 |             1927.09 |             1793.00 |
| TPC-DS Q66    |             1053.24 |             1191.68 |             1138.66 |              786.34 |
| TPC-DS Q67    |             5646.54 |             6126.75 |             6303.18 |             6355.68 |
| TPC-DS Q68    |              226.16 |              220.89 |              216.29 |              231.24 |
| TPC-DS Q69    |              357.69 |              410.72 |              358.09 |              413.99 |
| TPC-DS Q70    |             1474.54 |             1941.71 |             1495.80 |             1439.32 |
| TPC-DS Q71    |              332.01 |              669.27 |              355.53 |              494.77 |
| TPC-DS Q72    |             2193.22 |             2989.87 |             2299.82 |             2384.52 |
| TPC-DS Q73    |              151.09 |               94.00 |              133.17 |               89.06 |
| TPC-DS Q74    |             1977.55 |             1976.69 |             1862.36 |             1960.16 |
| TPC-DS Q75    |             5732.53 |             5664.71 |             6692.33 |             5368.69 |
| TPC-DS Q76    |             6003.63 |             8145.53 |             7236.00 |             8947.07 |
| TPC-DS Q77    |             1147.99 |             1090.03 |             1231.93 |             1094.46 |
| TPC-DS Q78    |            14220.92 |            13961.64 |            15077.46 |            15397.31 |
| TPC-DS Q79    |              238.90 |              838.41 |              236.96 |              227.66 |
| TPC-DS Q80    |             8542.04 |             9035.39 |             8656.02 |            10295.32 |
| TPC-DS Q81    |              337.52 |              196.31 |              148.08 |              304.02 |
| TPC-DS Q82    |              582.28 |              449.08 |              434.97 |              528.29 |
| TPC-DS Q83    |              233.06 |              222.09 |              276.19 |              286.97 |
| TPC-DS Q84    |               49.75 |               45.02 |               50.74 |               51.42 |
| TPC-DS Q85    |              306.90 |              541.34 |              303.50 |              306.63 |
| TPC-DS Q86    |              306.00 |              334.28 |              561.39 |              350.29 |
| TPC-DS Q87    |             3824.84 |             3111.18 |             3239.08 |             3156.44 |
| TPC-DS Q88    |              631.59 |              414.88 |              639.76 |              513.38 |
| TPC-DS Q89    |              141.95 |              157.84 |              243.46 |              216.53 |
| TPC-DS Q90    |               76.05 |               99.97 |              159.59 |              213.05 |
| TPC-DS Q91    |               41.71 |               39.21 |               56.26 |               48.09 |
| TPC-DS Q92    |              141.15 |              137.72 |              146.34 |              140.02 |
| TPC-DS Q93    |             2074.16 |             2472.96 |             2053.36 |             2104.73 |
| TPC-DS Q94    |            37779.85 |            41184.29 |            42187.57 |            42167.14 |
| TPC-DS Q95    |           344096.87 |           326893.35 |           339482.62 |           329777.05 |
| TPC-DS Q96    |              825.21 |              756.14 |              806.36 |              783.42 |
| TPC-DS Q97    |             4489.78 |             4528.22 |             4943.42 |             5092.56 |
| TPC-DS Q98    |              491.55 |              482.09 |              479.94 |              587.42 |
| TPC-DS Q99    |              606.72 |              417.05 |              395.45 |              411.05 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |     14053.35 |    190.63 |         955.89 |               1023.98 |
| monetdb-1-1-2-1 |     12287.45 |    170.61 |         961.30 |               1023.99 |
| monetdb-1-2-1-1 |     10997.14 |    134.56 |        1001.81 |               1023.90 |
| monetdb-1-2-2-1 |     11750.81 |    173.82 |        1011.21 |               1023.97 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        32.40 |      0.19 |           0.40 |                  0.41 |
| monetdb-1-1-2-1 |        31.90 |      0.19 |           0.38 |                  0.39 |
| monetdb-1-2-1-1 |        33.52 |      0.35 |           0.38 |                  0.39 |
| monetdb-1-2-2-1 |        31.35 |      0.53 |           0.37 |                  0.37 |

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
* TEST passed: SUT pods not replaced
* TEST passed: Host information complete
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Monitoring returned data
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
* TEST passed: Results of all benchmarker pods
* TEST passed: Benchmarker pods without errors

Test successful!
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
* Duration: 2686s 
* Code: 1795706405
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=30) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 14400.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
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
  * disk:643805
  * datadisk:75265
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1795706405
* monetdb-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:639984
  * datadisk:75265
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1795706405
* monetdb-1-1-3-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:645548
  * datadisk:75265
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1795706405
* monetdb-1-1-3-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:645548
  * datadisk:75265
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1795706405
* monetdb-1-1-3-1-3 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:645548
  * datadisk:75265
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1795706405

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MonetDB-1

### Data Parameters of Reused Volumes
* MonetDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1795706405-b4967bc7-l7975: 0

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
| MonetDB-1-1 |                1 |   30 |     1661.00 |           3.00 |          717.00 |        409.00 |          527.00 |              0 |         0 |             | None           |             0 | False         |               65.02 | True                |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 30.00 |               99 |                  99 |        586 |            0.91 |           124029.69 |          18245.73 |          -1 |
| monetdb-1-1-2-1-1 | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |       1 | 30.00 |               99 |                  99 |        469 |            0.59 |           195900.16 |          22797.44 |          -1 |
| monetdb-1-1-3-1-1 | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |       1 | 30.00 |               99 |                  99 |       1319 |            0.99 |           115285.95 |           8106.14 |          -1 |
| monetdb-1-1-3-1-2 | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |       2 | 30.00 |               99 |                  99 |        807 |            0.87 |           127683.25 |          13249.07 |          -1 |
| monetdb-1-1-3-1-3 | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |       3 | 30.00 |               99 |                  99 |       1297 |            0.84 |           133534.09 |           8243.64 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        586 |            0.91 |           124029.69 |          18245.73 |          -1 |
| monetdb-1-1-2 | monetdb-1-1-2 |                1 |        2 |               1 |           1 | 30.00 |               99 |                  99 |        469 |            0.59 |           195900.16 |          22797.44 |          -1 |
| monetdb-1-1-3 | monetdb-1-1-3 |                1 |        3 |               1 |           3 | 30.00 |              297 |                 297 |       1319 |            0.90 |           125266.27 |          24318.42 |          -1 |

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
| TPC-DS Q1     |             1645.35 |              273.54 |              380.22 |              251.66 |              370.66 |
| TPC-DS Q2     |             3903.88 |             1304.30 |             2405.47 |             2214.67 |             3253.38 |
| TPC-DS Q3     |             2801.76 |              102.73 |              161.59 |              296.76 |              751.11 |
| TPC-DS Q4     |            26666.79 |            15832.68 |            17428.28 |            19769.40 |            20219.14 |
| TPC-DS Q5     |            20011.86 |             1338.21 |             1972.81 |             2379.15 |             1497.47 |
| TPC-DS Q6     |              582.26 |              322.24 |             1881.25 |              358.90 |              582.30 |
| TPC-DS Q7     |             5468.17 |              156.34 |              212.73 |              170.69 |              163.40 |
| TPC-DS Q8     |             3898.33 |              452.18 |              502.99 |              313.21 |             1426.66 |
| TPC-DS Q9     |             2055.07 |              780.75 |              667.31 |              579.37 |              661.46 |
| TPC-DS Q10    |            20023.43 |              263.34 |              307.50 |              150.93 |              125.08 |
| TPC-DS Q11    |             7899.54 |             7215.97 |             8509.99 |             8931.45 |             9460.57 |
| TPC-DS Q12    |              199.59 |              123.29 |              129.86 |              234.97 |              170.36 |
| TPC-DS Q13    |              712.69 |              290.08 |              314.83 |              297.51 |              323.34 |
| TPC-DS Q14a+b |            33103.83 |            37379.67 |            37968.19 |            35963.21 |            31181.96 |
| TPC-DS Q15    |              159.25 |              115.85 |              122.59 |              271.02 |              724.24 |
| TPC-DS Q16    |            54392.79 |            44198.13 |            68219.98 |            38602.28 |           115060.74 |
| TPC-DS Q17    |             3511.94 |             1945.84 |             2650.81 |             2983.99 |             1965.36 |
| TPC-DS Q18    |             2492.88 |              895.06 |             2059.55 |             1177.61 |             1870.40 |
| TPC-DS Q19    |              162.06 |              147.51 |             9739.66 |             1853.71 |              515.61 |
| TPC-DS Q20    |              141.74 |               98.48 |             4163.64 |             4628.49 |              210.50 |
| TPC-DS Q21    |             2417.29 |               97.70 |            13075.72 |             7062.53 |              157.03 |
| TPC-DS Q22    |             1748.29 |             1022.27 |             3769.80 |             4676.51 |             2070.71 |
| TPC-DS Q23a+b |            43521.62 |            40745.92 |            56824.29 |            54378.96 |            54443.68 |
| TPC-DS Q24a+b |            16408.96 |            15867.02 |             6422.72 |             7412.16 |             9843.29 |
| TPC-DS Q25    |             2374.24 |             3299.29 |             3071.41 |             3266.83 |             3329.82 |
| TPC-DS Q26    |              201.12 |              178.13 |              152.79 |              230.33 |              236.40 |
| TPC-DS Q27    |             1424.44 |             1362.44 |             1699.40 |             1922.11 |             1792.36 |
| TPC-DS Q28    |              841.73 |              915.04 |             1064.02 |              613.15 |              596.80 |
| TPC-DS Q29    |             2198.98 |             2305.96 |             4034.69 |             2695.66 |             2309.93 |
| TPC-DS Q30    |               79.77 |               33.61 |               81.22 |               67.04 |               36.22 |
| TPC-DS Q31    |             2222.65 |             1559.56 |             3675.19 |             1811.92 |             1726.32 |
| TPC-DS Q32    |              131.45 |              170.19 |              101.26 |              161.23 |              274.06 |
| TPC-DS Q33    |              283.27 |              294.86 |              108.29 |              150.24 |              187.13 |
| TPC-DS Q34    |              562.47 |              199.60 |              103.89 |              106.18 |              180.44 |
| TPC-DS Q35    |              853.32 |             1135.12 |             1332.15 |             1023.68 |             1266.19 |
| TPC-DS Q36    |             1740.72 |             1365.59 |             2294.18 |             1433.29 |             1393.72 |
| TPC-DS Q37    |              493.85 |              404.17 |              484.19 |              398.07 |              471.75 |
| TPC-DS Q38    |             2565.12 |             3591.71 |             2966.03 |             2616.26 |             3699.51 |
| TPC-DS Q39a+b |             1527.72 |             1006.96 |             2205.56 |             1346.52 |             1382.88 |
| TPC-DS Q40    |              757.05 |              320.46 |              394.36 |              376.37 |              372.17 |
| TPC-DS Q41    |                9.46 |                4.73 |                6.50 |                8.90 |                6.19 |
| TPC-DS Q42    |               77.29 |              106.61 |               88.88 |              243.64 |              102.00 |
| TPC-DS Q43    |              226.43 |              211.51 |              220.03 |              267.09 |              225.87 |
| TPC-DS Q44    |              210.15 |              206.47 |              216.81 |              300.88 |              255.28 |
| TPC-DS Q45    |              114.25 |              126.39 |              124.77 |              148.09 |              468.87 |
| TPC-DS Q46    |              212.04 |              427.63 |              184.45 |              325.52 |              327.57 |
| TPC-DS Q47    |             1770.76 |             1567.64 |             1661.68 |             1585.53 |             1189.33 |
| TPC-DS Q48    |              217.30 |              217.69 |              228.83 |              222.13 |              227.02 |
| TPC-DS Q49    |             4220.23 |             1068.95 |             1027.50 |             1072.10 |             1151.30 |
| TPC-DS Q50    |              788.73 |              559.92 |              794.58 |              595.93 |             1587.23 |
| TPC-DS Q51    |             3051.08 |             2402.60 |             3460.45 |             3041.54 |             3592.43 |
| TPC-DS Q52    |               70.44 |              101.55 |              108.00 |              105.52 |               98.04 |
| TPC-DS Q53    |              105.25 |               88.60 |              165.12 |               95.74 |               99.18 |
| TPC-DS Q54    |               91.52 |               93.96 |              212.95 |               89.30 |              104.16 |
| TPC-DS Q55    |               81.46 |              126.98 |               99.58 |               69.58 |              109.05 |
| TPC-DS Q56    |              226.53 |              346.56 |              129.03 |              126.53 |              132.11 |
| TPC-DS Q57    |              150.57 |              149.10 |              156.60 |              144.11 |              143.01 |
| TPC-DS Q58    |              567.36 |              553.42 |              890.14 |              512.42 |              544.73 |
| TPC-DS Q59    |             1771.96 |             1100.28 |              800.02 |             1350.37 |             1012.20 |
| TPC-DS Q60    |              192.71 |              146.10 |              357.38 |              248.91 |              228.11 |
| TPC-DS Q61    |              169.02 |              162.27 |              170.24 |              162.72 |              175.63 |
| TPC-DS Q62    |              434.24 |              255.74 |              300.02 |              294.38 |              280.63 |
| TPC-DS Q63    |               93.79 |               94.60 |              113.27 |              104.81 |               96.91 |
| TPC-DS Q64    |             6294.05 |             2098.46 |             2465.25 |             2239.46 |             1998.91 |
| TPC-DS Q65    |             1074.66 |             1513.63 |             1591.66 |             2459.38 |             1397.31 |
| TPC-DS Q66    |             1377.92 |              465.52 |              563.10 |             1438.66 |              309.60 |
| TPC-DS Q67    |             5366.73 |             6589.77 |             7359.14 |             9172.77 |             6557.15 |
| TPC-DS Q68    |              202.29 |              225.25 |              255.66 |             1141.14 |              225.55 |
| TPC-DS Q69    |              393.05 |              291.61 |              254.47 |              738.23 |              272.32 |
| TPC-DS Q70    |             1612.28 |             1530.74 |             2067.41 |             3620.04 |             2045.11 |
| TPC-DS Q71    |              369.18 |              206.37 |              187.57 |              762.26 |              177.09 |
| TPC-DS Q72    |             2458.17 |             1257.39 |             1128.52 |             1241.27 |             1243.45 |
| TPC-DS Q73    |              110.11 |              106.28 |              124.88 |               90.47 |              127.54 |
| TPC-DS Q74    |             1929.06 |             2163.57 |             2885.84 |             2913.32 |             8064.88 |
| TPC-DS Q75    |             7144.33 |             5107.53 |             6155.60 |             7314.37 |            10287.90 |
| TPC-DS Q76    |             7605.38 |              338.85 |             6750.61 |              349.96 |             3119.89 |
| TPC-DS Q77    |             1312.48 |              850.09 |              988.38 |              724.70 |             1430.54 |
| TPC-DS Q78    |            14103.03 |            14352.84 |            15856.57 |            15829.34 |            18335.19 |
| TPC-DS Q79    |              458.44 |              207.36 |             8405.20 |              248.26 |             9115.69 |
| TPC-DS Q80    |             9461.90 |             7142.30 |            12800.06 |            11171.75 |            32766.41 |
| TPC-DS Q81    |              169.87 |              139.93 |             2381.76 |              216.04 |              194.63 |
| TPC-DS Q82    |              454.92 |              427.72 |             3939.07 |              469.03 |              776.38 |
| TPC-DS Q83    |              278.93 |               37.54 |              708.05 |               44.69 |               50.31 |
| TPC-DS Q84    |               45.67 |               31.12 |              564.49 |               33.32 |               35.32 |
| TPC-DS Q85    |              294.45 |              288.95 |            14797.58 |              349.04 |              382.69 |
| TPC-DS Q86    |              321.41 |              326.83 |             1912.14 |              462.14 |              442.97 |
| TPC-DS Q87    |             3062.27 |             2704.27 |             5082.77 |             3350.51 |             4247.65 |
| TPC-DS Q88    |              922.43 |              420.11 |              598.47 |              447.82 |              578.42 |
| TPC-DS Q89    |              274.59 |              144.19 |              197.53 |              158.48 |              197.49 |
| TPC-DS Q90    |              112.24 |              161.76 |               88.54 |               69.18 |              100.81 |
| TPC-DS Q91    |               43.50 |               37.74 |               35.07 |               25.16 |               34.69 |
| TPC-DS Q92    |              138.95 |              149.68 |              199.24 |              167.10 |              164.39 |
| TPC-DS Q93    |             1937.95 |             1958.77 |             2650.99 |             2017.23 |             5881.83 |
| TPC-DS Q94    |            40344.93 |            39050.91 |            58848.42 |            43032.19 |            82239.04 |
| TPC-DS Q95    |           154901.75 |           144690.75 |           846252.94 |           371377.03 |           774551.96 |
| TPC-DS Q96    |               34.71 |               35.19 |               40.28 |            22004.81 |             1232.27 |
| TPC-DS Q97    |             3038.02 |             3939.22 |             4022.85 |            24152.03 |             7738.19 |
| TPC-DS Q98    |              155.67 |              162.58 |              153.01 |            12873.86 |              706.29 |
| TPC-DS Q99    |              264.11 |              259.22 |              328.48 |             9354.10 |              898.75 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      8934.28 |     90.22 |         854.20 |                854.21 |
| monetdb-1-1-2-1 |      7939.16 |    102.68 |         813.03 |                813.04 |
| monetdb-1-1-3-1 |     24374.84 |    121.34 |        1005.09 |               1024.00 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        30.96 |      0.31 |           0.38 |                  0.39 |
| monetdb-1-1-2-1 |        31.41 |      0.26 |           0.35 |                  0.36 |
| monetdb-1-1-3-1 |        88.25 |      1.02 |           0.79 |                  0.80 |

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
* TEST passed: SUT pods not replaced
* TEST passed: Host information complete
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Monitoring returned data
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
* TEST passed: Results of all benchmarker pods
* TEST passed: Benchmarker pods without errors

Test successful!
```

</details>


## SSB

The Star Schema Benchmark runs on MonetDB, too, see [Example: SSB](Example-SSB.md).
