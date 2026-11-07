# Example: Benchmark ClickHouse

This example shows how to benchmark ClickHouse with TPC-H and TPC-DS, as a single server and as a cluster managed by bexhoma.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

[ClickHouse](https://clickhouse.com/docs) is a column-store DBMS for analytical workloads.
Bexhoma runs it in two installations:

* **ClickHouse**: one server (the SUT).
* **ClickHouseCluster**: one coordinator (the SUT) and `-nw` shards (a stateful set of workers, one replica per shard).

Both use the official image `clickhouse/clickhouse-server` (26.8, LTS).
Queries run over JDBC (HTTP interface), loaders and init scripts use `clickhouse-client` (native protocol).

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. [ClickHouse](https://clickhouse.com/docs)
1. [ClickHouse in Docker](https://hub.docker.com/r/clickhouse/clickhouse-server)
1. [Distributed table engine](https://clickhouse.com/docs/engines/table-engines/special/distributed)
1. [ClickHouse Keeper](https://clickhouse.com/docs/guides/sre/keeper/clickhouse-keeper)
1. [TPC-H](https://www.tpc.org/tpch/)
1. [TPC-DS](https://www.tpc.org/tpcds/)
1. [Orchestrating DBMS Benchmarking in the Cloud with Kubernetes](https://doi.org/10.1007/978-3-030-94437-7_6)
1. [A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools](https://doi.org/10.1007/978-3-031-68031-1_9)
1. Test script of this page: [test-docs-clickhouse.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-clickhouse.sh), [test-docs-clickhouse.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-clickhouse.ps1)


## Perform TPC-H Benchmark

You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker36"
BEXHOMA_NODE_LOAD="cl-worker38"
BEXHOMA_NODE_BENCHMARK="cl-worker38"
BEXHOMA_NODES_WORKER="cl-worker36+cl-worker37+cl-worker29"
LOG_DIR="./logs_tests"
BEXHOMA_MS=10
BEXHOMA_STORAGE_CLASS="nvme"

mkdir -p $LOG_DIR
```

For performing the experiment we can run the [tpch file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpch.py).

Example:
```bash
bexhoma tpch \
  -dbms ClickHouse \
  -sf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -xdt \
  -ms $BEXHOMA_MS \
  -tr \
  -lc 16 \
  -rc 16 \
  -lr 64Gi \
  -rr 64Gi \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -ks no \
  run &>$LOG_DIR/docs_tpch_clickhouse.log
```

This
* starts a clean instance of ClickHouse (`-dbms`)
  * with 16 CPUs and 64 GiB RAM (`-rc`, `-lc`, `-rr`, `-lr`)
  * data directory inside the container
* creates the TPC-H schema (MergeTree tables, sorted by their primary key)
* starts 8 loader pods (`-nlp`)
  * with a data generator (init container) each, which generates a share of TPC-H data of SF=1 (`-sf`)
  * and a loading container each, which sends the flat files with `clickhouse-client` (`INSERT ... FORMAT CSV`)
* runs the check script (row counts, parts, sizes)
* runs 1 stream of the 22 TPC-H queries (`-ne`) and measures the data transfer volume per query (`-xdt`)
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

The code `1792777036` is the unique identifier of the experiment.
You can find the number also in the output of the benchmark script.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1792777036` (removes everything that is related to experiment `1792777036`).

### Evaluate Results

At the end of a benchmark you will see a summary like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_clickhouse_summary.md" target="_blank" rel="noopener">docs_tpch_clickhouse.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 326s 
* Code: 1793706475
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Data transfer volume per query is also measured.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * Experiment is limited to DBMS ['ClickHouse'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 16 CPU and 64Gi RAM. CPU limit is 16. RAM limit is 64Gi.

### Connections
* clickhouse-1-1-1-1-1 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:797150
  * datadisk:800
  * volume_size:1.8T
  * volume_used:779G
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793706475

### SUT Container Restarts
* bexhoma-sut-clickhouse-1-1793706475-7cbfff88d-zhxjs: 0

### Workflow

#### Actual

* DBMS ClickHouse-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS ClickHouse-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| ClickHouse-1-1 |                1 |    1 |       47.00 |           1.00 |           33.00 |          5.00 |            1.00 |              8 |           0 |             | None           |             0 | False         |               76.60 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| clickhouse-1-1-1-1-1 | ClickHouse-1    | clickhouse-1-1-1 | clickhouse-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         10 |            0.06 |            68924.39 |           7920.00 |          -1 | clickhouse-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| clickhouse-1-1-1 | clickhouse-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         10 |            0.06 |            68924.39 |           7920.00 |          -1 |

#### Query Completion per Phase

| phase            |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:-----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| clickhouse-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   clickhouse-1-1-1-1-1 |
|:----------------------------------------------------|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                  98.11 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                  59.53 |
| Shipping Priority (TPC-H Q3)                        |                  47.22 |
| Order Priority Checking Query (TPC-H Q4)            |                 157.23 |
| Local Supplier Volume (TPC-H Q5)                    |                  51.23 |
| Forecasting Revenue Change (TPC-H Q6)               |                  19.50 |
| Volume Shipping Query (TPC-H Q7)                    |                  68.53 |
| National Market Share (TPC-H Q8)                    |                  51.25 |
| Product Type Profit Measure (TPC-H Q9)              |                  63.16 |
| Returned Item Reporting Query (TPC-H Q10)           |                  68.88 |
| Important Stock Identification (TPC-H Q11)          |                  25.50 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                  33.94 |
| Customer Distribution (TPC-H Q13)                   |                  42.00 |
| Promotion Effect Query (TPC-H Q14)                  |                  29.93 |
| Top Supplier Query (TPC-H Q15)                      |                  39.84 |
| Parts/Supplier Relationship (TPC-H Q16)             |                  35.79 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                  33.05 |
| Large Volume Customer (TPC-H Q18)                   |                  77.16 |
| Discounted Revenue (TPC-H Q19)                      |                  41.40 |
| Potential Part Promotion (TPC-H Q20)                |                  44.64 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 415.50 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  30.98 |

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

To see the summary again you can simply call `bexhoma summary -e 1792777036` with the experiment code.

Results are transformed into pandas DataFrames and can be inspected in detail.
See for example the [Jupyter notebooks](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/notebooks/), in particular [Collector-TPC-H.ipynb](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/notebooks/Collector-TPC-H.ipynb).

You can connect to an evaluation server locally by `bexhoma jupyter`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888


## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).
Metrics are sampled every few seconds, so the benchmarking phase should take at least a minute.
At SF=1, the 22 queries take about 10 seconds on ClickHouse and at SF=10 about 14 seconds, so this run uses SF=10 (`-sf`) and runs each query 10 times (`-xqr`).
At SF=1 the loaders also finish within a few seconds, shorter than the scrape interval of 30 seconds; their CPU utilization (a rate over two scrapes) is then missing, and the test `Monitoring metrics missing` fails for that metric only.

For a cluster, monitoring sums the metrics of coordinator and shards (components SUT and worker).

```bash
bexhoma tpch \
  -dbms ClickHouse \
  -sf 10 \
  -nc 1 \
  -ne 1 \
  -xqr 10 \
  -nlp 8 \
  -xdt \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lc 16 \
  -rc 16 \
  -lr 64Gi \
  -rr 64Gi \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -ks no \
  run &>$LOG_DIR/docs_tpch_clickhouse_monitoring.log
```

### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_clickhouse_monitoring_summary.md" target="_blank" rel="noopener">docs_tpch_clickhouse_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=10
* Type: tpch
* Duration: 513s 
* Code: 1793713001
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Data transfer volume per query is also measured.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['ClickHouse'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Each query is repeated 10 times.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 16 CPU and 64Gi RAM. CPU limit is 16. RAM limit is 64Gi.

### Connections
* clickhouse-1-1-1-1-1 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:800451
  * datadisk:10610
  * volume_size:1.8T
  * volume_used:782G
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793713001

### SUT Container Restarts
* bexhoma-sut-clickhouse-1-1793713001-5c9478d797-h66s5: 0

### Workflow

#### Actual

* DBMS ClickHouse-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS ClickHouse-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| ClickHouse-1-1 |                1 |   10 |       68.00 |           1.00 |           39.00 |         22.00 |            0.00 |              8 |           0 |             | None           |             0 | False         |              529.41 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| clickhouse-1-1-1-1-1 | ClickHouse-1    | clickhouse-1-1-1 | clickhouse-1-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |                 220 |        152 |            0.21 |           201461.63 |          52105.26 |          -1 | clickhouse-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| clickhouse-1-1-1 | clickhouse-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |                 220 |        152 |            0.21 |           201461.63 |          52105.26 |          -1 |

#### Query Completion per Phase

| phase            |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:-----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| clickhouse-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   clickhouse-1-1-1-1-1 |
|:----------------------------------------------------|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                 240.78 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 123.78 |
| Shipping Priority (TPC-H Q3)                        |                 138.95 |
| Order Priority Checking Query (TPC-H Q4)            |                1791.87 |
| Local Supplier Volume (TPC-H Q5)                    |                 201.49 |
| Forecasting Revenue Change (TPC-H Q6)               |                  65.48 |
| Volume Shipping Query (TPC-H Q7)                    |                 159.02 |
| National Market Share (TPC-H Q8)                    |                 167.87 |
| Product Type Profit Measure (TPC-H Q9)              |                 248.83 |
| Returned Item Reporting Query (TPC-H Q10)           |                 185.10 |
| Important Stock Identification (TPC-H Q11)          |                  61.46 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 131.88 |
| Customer Distribution (TPC-H Q13)                   |                 205.47 |
| Promotion Effect Query (TPC-H Q14)                  |                 103.65 |
| Top Supplier Query (TPC-H Q15)                      |                 121.12 |
| Parts/Supplier Relationship (TPC-H Q16)             |                  92.92 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                 211.26 |
| Large Volume Customer (TPC-H Q18)                   |                 252.19 |
| Discounted Revenue (TPC-H Q19)                      |                 206.38 |
| Potential Part Promotion (TPC-H Q20)                |                 112.69 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                5454.96 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 147.68 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 |       106.13 |      2.50 |           3.57 |                 11.29 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 | n/a          |      0.19 |           0.00 |                  0.90 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 |       507.71 |      5.35 |           3.38 |                 13.81 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 |        58.02 |      0.80 |           0.65 |                  0.69 |

### Missing Monitoring Metrics
* CPU Utilization [CPUs] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Queries [queries/s] |   Running Queries [count] |   Failed Queries [count] |   Rows Read [rows/s] |   Data Read, uncompressed [MiB/s] |
|:-------------------|----------------------:|--------------------------:|-------------------------:|---------------------:|----------------------------------:|
| clickhouse-1-1-1-1 |                  0.22 |                      1.00 |                     0.00 |            346032.58 |                             46.77 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Queries [queries/s] |   Running Queries [count] |   Failed Queries [count] |   Rows Read [rows/s] |   Data Read, uncompressed [MiB/s] |
|:-------------------|----------------------:|--------------------------:|-------------------------:|---------------------:|----------------------------------:|
| clickhouse-1-1-1-1 |                  0.96 |                      1.00 |                     0.00 |          51654452.07 |                           1195.60 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
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

### Application Metrics

Collecting application metrics for ClickHouse is supported and included in the run above.
It is activated by `-ma`: ClickHouse has its own Prometheus endpoint (port 9363), so there is no exporter sidecar.
The metric set `clickhouse` contains queries per second, running queries, failed queries, rows and data read per second, rows inserted per second, memory tracked by ClickHouse, running merges and the number of parts of MergeTree tables.
See [Metrics](Example-Metrics.html) for application metrics of all DBMS.


## Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.
With repetitions (`-nc`), `-rsr` removes an existing volume only before the first repetition and later repetitions reuse it without loading; `-rsrp` removes it before every repetition. See [Concepts](Concepts.html).

```bash
bexhoma tpch \
  -dbms ClickHouse \
  -sf 10 \
  -nc 2 \
  -ne 1 \
  -nlp 8 \
  -xdt \
  -m \
  -ma \
  -ms $BEXHOMA_MS \
  -tr \
  -lc 16 \
  -rc 16 \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -ks no \
  run &>$LOG_DIR/docs_tpch_clickhouse_storage.log
```

This
* puts the data directory on a persistent volume of 50 GiB (`-rss`) of the storage class `$BEXHOMA_STORAGE_CLASS` (`-rst`), removed first if it exists (`-rsr`)
* repeats the benchmark once more (`-nc 2`): bexhoma restarts the SUT, which finds the data on the volume and does not load again
* monitors the SUT (`-m`) and collects ClickHouse's own metrics (`-ma`)

### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_clickhouse_storage_summary.md" target="_blank" rel="noopener">docs_tpch_clickhouse_storage.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=10
* Type: tpch
* Duration: 587s 
* Code: 1793791936
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Data transfer volume per query is also measured.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by sidecar containers.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['ClickHouse'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 16 CPU and 64Gi RAM. CPU limit is 16. RAM limit is 64Gi.

### Connections
* clickhouse-1-1-1-1-1 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:741613
  * datadisk:11652
  * volume_size:49G
  * volume_used:12G
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793791936
* clickhouse-1-2-1-1-1 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:848574
  * datadisk:11690
  * volume_size:49G
  * volume_used:12G
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793791936

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: ClickHouse-1-2

### Data Parameters of Reused Volumes
* ClickHouse-1: DDL values of the volume: order_orders=key, order_lineitem=key, partition_orders=none, partition_lineitem=none, index_granularity=8192, wide_parts=default, low_cardinality=off, codec=default
* ClickHouse-1: loading values of the volume: script=Schema, indexing=Checks

### SUT Container Restarts
* bexhoma-sut-clickhouse-1-1793791936-65cf9698b7-d87st: 0
* bexhoma-sut-clickhouse-1-1793791936-5dd8cfc9cf-z6zth: 0

### Workflow

#### Actual

* DBMS ClickHouse-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS ClickHouse-1 - Experiment 2 Client 1: tpch (1 pods)

#### Planned

* DBMS ClickHouse-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS ClickHouse-1 - Experiment 2 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| ClickHouse-1-1 |                1 |   10 |       49.00 |           2.00 |           23.00 |         18.00 |            2.00 |              8 |           0 |             | None           |             0 | False         |              734.69 | False               |
| ClickHouse-1-2 |                2 |   10 |       49.00 |           2.00 |           23.00 |         18.00 |            2.00 |              8 |           0 |             | None           |             0 | False         |              734.69 | True                |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| clickhouse-1-1-1-1-1 | ClickHouse-1    | clickhouse-1-1-1 | clickhouse-1-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |                  22 |         21 |            0.22 |           195585.00 |          37714.29 |          -1 | clickhouse-1-1-1-1-1 |
| clickhouse-1-2-1-1-1 | ClickHouse-1    | clickhouse-1-2-1 | clickhouse-1-2-1-1 |                2 |        1 |               1 |           1 | 10.00 |               22 |                  22 |         30 |            0.34 |           145159.34 |          26400.00 |          -1 | clickhouse-1-2-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| clickhouse-1-1-1 | clickhouse-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |                  22 |         21 |            0.22 |           195585.00 |          37714.29 |          -1 |
| clickhouse-1-2-1 | clickhouse-1-2-1 |                2 |        1 |               1 |           1 | 10.00 |               22 |                  22 |         30 |            0.34 |           145159.34 |          26400.00 |          -1 |

#### Query Completion per Phase

| phase            |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:-----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| clickhouse-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| clickhouse-1-2-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   clickhouse-1-1-1-1-1 |   clickhouse-1-2-1-1-1 |
|:----------------------------------------------------|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                 300.05 |                 789.08 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 120.97 |                 242.15 |
| Shipping Priority (TPC-H Q3)                        |                 158.83 |                 295.95 |
| Order Priority Checking Query (TPC-H Q4)            |                1758.34 |                1802.68 |
| Local Supplier Volume (TPC-H Q5)                    |                 142.99 |                 321.99 |
| Forecasting Revenue Change (TPC-H Q6)               |                  61.89 |                  72.70 |
| Volume Shipping Query (TPC-H Q7)                    |                 163.28 |                 192.26 |
| National Market Share (TPC-H Q8)                    |                 170.19 |                 328.43 |
| Product Type Profit Measure (TPC-H Q9)              |                 263.93 |                 308.22 |
| Returned Item Reporting Query (TPC-H Q10)           |                 205.01 |                 260.86 |
| Important Stock Identification (TPC-H Q11)          |                  47.43 |                  66.97 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 123.70 |                 248.13 |
| Customer Distribution (TPC-H Q13)                   |                 296.53 |                 254.80 |
| Promotion Effect Query (TPC-H Q14)                  |                  86.09 |                  78.16 |
| Top Supplier Query (TPC-H Q15)                      |                 131.15 |                 133.73 |
| Parts/Supplier Relationship (TPC-H Q16)             |                  74.07 |                  88.62 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                 104.64 |                 122.55 |
| Large Volume Customer (TPC-H Q18)                   |                 257.79 |                 272.96 |
| Discounted Revenue (TPC-H Q19)                      |                 164.87 |                 309.66 |
| Potential Part Promotion (TPC-H Q20)                |                  93.40 |                 107.22 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                5071.91 |                5311.89 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 163.25 |                 169.98 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 |        95.99 |      2.72 |           0.82 |                 12.19 |

### Loading phase: component data generator

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: SUT deployment

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 | n/a          |      0.10 |           0.80 |                 12.18 |
| clickhouse-1-2-1-1 | n/a          |      2.77 |           1.57 |                  3.85 |

### Benchmarking phase: component benchmarker

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 | n/a          |      0.00 |           0.35 |                  0.35 |
| clickhouse-1-2-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |

### Missing Monitoring Metrics
* CPU Utilization [CPUs] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection clickhouse-1-2-1-1 (bexhoma-metrics-clickhouse-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection clickhouse-1-2-1-1 (bexhoma-metrics-clickhouse-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-2-1-1 (bexhoma-metrics-clickhouse-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-2-1-1 (bexhoma-metrics-clickhouse-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Queries [queries/s] |   Running Queries [count] |   Failed Queries [count] |   Rows Read [rows/s] |   Data Read, uncompressed [MiB/s] |
|:-------------------|----------------------:|--------------------------:|-------------------------:|---------------------:|----------------------------------:|
| clickhouse-1-1-1-1 |                  0.24 |                      0.00 |                     0.00 |            362580.82 |                             49.06 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Queries [queries/s] |   Running Queries [count] |   Failed Queries [count] |   Rows Read [rows/s] |   Data Read, uncompressed [MiB/s] |
|:-------------------|----------------------:|--------------------------:|-------------------------:|---------------------:|----------------------------------:|
| clickhouse-1-1-1-1 |                  0.26 |                      0.00 |                     0.00 |           3652961.13 |                            122.50 |
| clickhouse-1-2-1-1 |                  0.04 |                      0.00 |                     0.00 |           2575372.70 |                             65.16 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Benchmarking phase: SUT deployment contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Benchmarking phase: component benchmarker contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Monitoring metrics missing (data pre-existing; job pods ran shorter than scrape interval; phase shorter than scrape interval; series exists only while non-zero)
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


## Variants

### Cluster

```bash
bexhoma tpch \
  -dbms ClickHouseCluster \
  -nw 3 \
  -sf 10 \
  -nc 2 \
  -ne 1 \
  -nlp 8 \
  -xdt \
  -m \
  -ma \
  -ms $BEXHOMA_MS \
  -tr \
  -lc 16 \
  -rc 16 \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -rnw $BEXHOMA_NODES_WORKER \
  -ks no \
  run &>$LOG_DIR/docs_tpch_clickhouse_cluster.log
```

This runs the benchmark of [Persistent Storage](#persistent-storage) against a cluster of a coordinator and 3 shards (`-nw`) on the nodes `$BEXHOMA_NODES_WORKER` (`-rnw`, one shard per node).
The coordinator and every shard get 16 CPUs, 64 GiB RAM and a volume of 50 GiB.



#### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_clickhouse_cluster_summary.md" target="_blank" rel="noopener">docs_tpch_clickhouse_cluster.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=10
* Type: tpch
* Duration: 642s 
* Code: 1793781303
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * Dimensions of ClickHouseCluster are a full copy on every node (-xdim replicated).
  * TPC-H (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Data transfer volume per query is also measured.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by sidecar containers.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['ClickHouseCluster'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 16 CPU and 64Gi RAM. CPU limit is 16. RAM limit is 64Gi.

### Connections
* clickhousecluster-1-1-1-1-1 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:793435
  * datadisk:1390
  * volume_size:49G
  * volume_used:1.4G
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * worker 0
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:602235
    * datadisk:3585
    * volume_size:49G
    * volume_used:3.6G
    * cpu_list:0-127
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:605346
    * datadisk:3638
    * volume_size:49G
    * volume_used:3.6G
    * cpu_list:0-127
  * worker 2
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:793435
    * datadisk:3639
    * volume_size:49G
    * volume_used:3.6G
    * cpu_list:0-223
  * resources_total: 64.0 CPU, 256.0 GiB RAM requested in 4 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
    * worker: 3 x, 48.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793781303
    * BEXHOMA_WORKERS:3
* clickhousecluster-1-2-1-1-1 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:793436
  * datadisk:1448
  * volume_size:49G
  * volume_used:1.5G
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * worker 0
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:602230
    * datadisk:3652
    * volume_size:49G
    * volume_used:3.6G
    * cpu_list:0-127
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:605345
    * datadisk:3703
    * volume_size:49G
    * volume_used:3.7G
    * cpu_list:0-127
  * worker 2
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:793436
    * datadisk:3708
    * volume_size:49G
    * volume_used:3.7G
    * cpu_list:0-223
  * resources_total: 64.0 CPU, 256.0 GiB RAM requested in 4 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
    * worker: 3 x, 48.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793781303
    * BEXHOMA_WORKERS:3

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: ClickHouseCluster-1-2

### Data Parameters of Reused Volumes
* ClickHouseCluster-1: DDL values of the volume: order_orders=key, order_lineitem=key, partition_orders=none, partition_lineitem=none, index_granularity=8192, wide_parts=default, low_cardinality=off, codec=default
* ClickHouseCluster-1: loading values of the volume: script=Schema, indexing=Checks

### SUT Container Restarts
* bexhoma-sut-clickhousecluster-1-1793781303-6486b4d69-c7nzb: 0
* bx-w-clickhousecluster-nvme-tpch-10-0: 0
* bx-w-clickhousecluster-nvme-tpch-10-1: 0
* bx-w-clickhousecluster-nvme-tpch-10-2: 0
* bexhoma-sut-clickhousecluster-1-1793781303-77f7996c84-mwdhd: 0

### Workflow

#### Actual

* DBMS ClickHouseCluster-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS ClickHouseCluster-1 - Experiment 2 Client 1: tpch (1 pods)

#### Planned

* DBMS ClickHouseCluster-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS ClickHouseCluster-1 - Experiment 2 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                       |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| ClickHouseCluster-1-1 |                1 |   10 |       55.00 |           4.00 |           25.00 |         18.00 |            3.00 |              8 |           0 |             | None           |             0 | False         |              654.55 | False               |
| ClickHouseCluster-1-2 |                2 |   10 |       55.00 |           4.00 |           25.00 |         18.00 |            3.00 |              8 |           0 |             | None           |             0 | False         |              654.55 | True                |

### Benchmarking

#### Per Connection

| DBMS                        | configuration       | phase                   | job                       |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                         |
|:----------------------------|:--------------------|:------------------------|:--------------------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------------------|
| clickhousecluster-1-1-1-1-1 | ClickHouseCluster-1 | clickhousecluster-1-1-1 | clickhousecluster-1-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |                  22 |         46 |            0.72 |            62413.74 |          17217.39 |          -1 | clickhousecluster-1-1-1-1-1 |
| clickhousecluster-1-2-1-1-1 | ClickHouseCluster-1 | clickhousecluster-1-2-1 | clickhousecluster-1-2-1-1 |                2 |        1 |               1 |           1 | 10.00 |               22 |                  22 |         45 |            0.72 |            58904.07 |          17600.00 |          -1 | clickhousecluster-1-2-1-1-1 |

#### Per Phase

|                         | phase                   |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------------|:------------------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| clickhousecluster-1-1-1 | clickhousecluster-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |                  22 |         46 |            0.72 |            62413.74 |          17217.39 |          -1 |
| clickhousecluster-1-2-1 | clickhousecluster-1-2-1 |                2 |        1 |               1 |           1 | 10.00 |               22 |                  22 |         45 |            0.72 |            58904.07 |          17600.00 |          -1 |

#### Query Completion per Phase

| phase                   |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:------------------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| clickhousecluster-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| clickhousecluster-1-2-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   clickhousecluster-1-1-1-1-1 |   clickhousecluster-1-2-1-1-1 |
|:----------------------------------------------------|------------------------------:|------------------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                        318.76 |                        461.70 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                        273.04 |                        276.71 |
| Shipping Priority (TPC-H Q3)                        |                        830.16 |                        852.19 |
| Order Priority Checking Query (TPC-H Q4)            |                       3582.79 |                       3598.60 |
| Local Supplier Volume (TPC-H Q5)                    |                       1216.21 |                       1528.88 |
| Forecasting Revenue Change (TPC-H Q6)               |                        156.54 |                        101.03 |
| Volume Shipping Query (TPC-H Q7)                    |                        727.03 |                        614.77 |
| National Market Share (TPC-H Q8)                    |                       1390.53 |                       1340.63 |
| Product Type Profit Measure (TPC-H Q9)              |                       1906.16 |                       1943.61 |
| Returned Item Reporting Query (TPC-H Q10)           |                        564.26 |                        649.15 |
| Important Stock Identification (TPC-H Q11)          |                         47.97 |                         64.16 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                       4743.12 |                       4677.76 |
| Customer Distribution (TPC-H Q13)                   |                        832.27 |                        829.45 |
| Promotion Effect Query (TPC-H Q14)                  |                        135.26 |                        155.99 |
| Top Supplier Query (TPC-H Q15)                      |                        220.24 |                        213.31 |
| Parts/Supplier Relationship (TPC-H Q16)             |                         67.29 |                        116.04 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                        571.53 |                        630.29 |
| Large Volume Customer (TPC-H Q18)                   |                       2993.06 |                       2607.68 |
| Discounted Revenue (TPC-H Q19)                      |                        270.41 |                        344.05 |
| Potential Part Promotion (TPC-H Q20)                |                        203.28 |                        204.94 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                      17766.56 |                      17527.07 |
| Global Sales Opportunity Query (TPC-H Q22)          |                        162.62 |                        160.71 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |        73.05 |      2.22 |           0.72 |                  1.97 |

### Loading phase: component worker

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |       176.96 |      4.29 |           5.24 |                 12.77 |

### Loading phase: component data generator

| DBMS                      | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|:-------------|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS                      | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|:-------------|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 | n/a          |      1.43 |           1.58 |                  2.51 |

### Benchmarking phase: SUT deployment

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |        72.92 |      1.99 |           1.91 |                  3.18 |
| clickhousecluster-1-2-1-1 |         6.62 |      0.54 |           2.39 |                  2.61 |

### Benchmarking phase: component worker

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |       246.25 |      7.34 |           7.40 |                 18.06 |
| clickhousecluster-1-2-1-1 |       155.74 |      5.57 |           6.04 |                  8.73 |

### Benchmarking phase: component benchmarker

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |        21.11 |      0.00 |           0.40 |                  0.40 |
| clickhousecluster-1-2-1-1 |        18.53 |      0.65 |           0.34 |                  0.34 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS                      |   Queries [queries/s] |   Running Queries [count] |   Failed Queries [count] |   Rows Read [rows/s] |   Data Read, uncompressed [MiB/s] |
|:--------------------------|----------------------:|--------------------------:|-------------------------:|---------------------:|----------------------------------:|
| clickhousecluster-1-1-1-1 |                  0.76 |                      3.00 |                     0.00 |            862148.70 |                            115.07 |

#### Benchmarking phase: component worker

| DBMS                      |   Queries [queries/s] |   Running Queries [count] |   Failed Queries [count] |   Rows Read [rows/s] |   Data Read, uncompressed [MiB/s] |
|:--------------------------|----------------------:|--------------------------:|-------------------------:|---------------------:|----------------------------------:|
| clickhousecluster-1-1-1-1 |                  1.35 |                      6.00 |                     0.00 |          12454578.06 |                            359.17 |
| clickhousecluster-1-2-1-1 |                  0.65 |                      8.00 |                     0.00 |          18172384.55 |                            355.09 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
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


## Technical Details

### Configuration of Bexhoma

In `cluster.config` there is a section:

```python
'ClickHouse': {
    'loadData': 'clickhouse-client --multiquery < {scriptname}',
    'template': {
        'version': '26.8',
        'alias': 'Columnwise-B',
        'docker_alias': 'Columnwise-B',
        'dialect': 'Clickhouse',
        'JDBC': {
            'auth': ['default', ''],
            'driver': 'com.clickhouse.jdbc.Driver',
            'jar': 'clickhouse-jdbc-0.11.0-all-dependencies.jar',
            'url': 'jdbc:clickhouse://{serverip}:9091/default',
            'database': 'default',
            'explain': ['EXPLAIN {query}'],
        }
    },
    'logfile': '/var/log/clickhouse-server/clickhouse-server.log',
    'datadir': '/var/lib/clickhouse/',
    'priceperhourdollar': 0.0,
    'monitor': {...},
},
```

`ClickHouseCluster` is the same, plus `'attachWorker': ''` (the shards are in the configuration of every pod, `remote_servers`, there is nothing to register) and the monitor component `worker`, which scrapes coordinator and shards (the metrics are totals of the cluster).
The JDBC jar is the variant with all dependencies; the smaller `-all` jar lacks slf4j-api, and the driver class does not load without it.
DBMS-Benchmarker reads `UInt64` results (e.g. of `count()`), which the driver returns as `java.math.BigInteger`, since v0.15.4.

### Deployment

* Single server: [deploymenttemplate-ClickHouse.yml](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-ClickHouse.yml), official image `clickhouse/clickhouse-server:26.8.34.13` (LTS).
* Clients use the HTTP interface (JDBC, service port 9091 → 8123); loaders and init scripts use the native protocol (`clickhouse-client`, port 9000, service port `port-sut-native`).
* `CLICKHOUSE_SKIP_USER_SETUP=1` keeps user `default` without password and with network access; without it the image restricts `default` to localhost.
* Instead of `privileged`, the container gets the capabilities `SYS_NICE`, `IPC_LOCK` and `NET_ADMIN` (thread priorities, mlock, per-query OS metrics).
* At start, the container writes two files:
  * `config.d/bexhoma.xml`: ClickHouse's own Prometheus endpoint on port 9363 (application metrics, `-ma`).
  * `users.d/bexhoma.xml`: settings of profile `default` for SQL-standard results, see below.
* Cluster: [deploymenttemplate-ClickHouseCluster.yml](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-ClickHouseCluster.yml), image, ports, capabilities and settings as the single server; in addition:
  * At start, every pod writes the cluster `bexhoma` (`remote_servers`, one shard per worker, from `BEXHOMA_WORKER_LIST_SPACE`).
  * The coordinator runs a single-node ClickHouse Keeper (port 9181, service port `port-sut-keeper`), which `ON CLUSTER` statements need; the workers reach it through the SUT service.
  * The coordinator sets `distributed_product_mode = global`.
  * A worker is ready when it has a session with the Keeper (readiness probe on `system.zookeeper`). Workers start before the Keeper and retry every 5 s, so with `/ping` as probe the first `ON CLUSTER` statement would time out.
  * Workers set the macros `{shard}` (pod ordinal) and `{replica}` (pod name) for later `ReplicatedMergeTree` setups.

### Settings for Standard SQL

The templates set these settings for user `default`, since TPC-H and TPC-DS expect standard SQL results:

| Setting | Value | Without it |
|---|---|---|
| `join_use_nulls` | 1 | an outer join fills unmatched columns with 0 or `''` instead of NULL (wrong counts in TPC-H Q13) |
| `union_default_mode` | `DISTINCT` | a plain `UNION` is a syntax error |
| `cast_keep_nullable` | 1 | `CAST` of a NULL fails |
| `allow_lossy_numeric_supertype` | 1 | `CASE`/`COALESCE` over Decimal and Float has no common type |

`prefer_column_name_to_alias` is not set: it would also apply to `ORDER BY`, where standard SQL resolves the alias of the select list first.

### Schema and Scripts

* [TPC-H ClickHouse](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch/ClickHouse), [TPC-H ClickHouseCluster](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch/ClickHouseCluster)
* [TPC-DS ClickHouse](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpcds/ClickHouse), [TPC-DS ClickHouseCluster](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpcds/ClickHouseCluster)

Tables are MergeTree in database `default`; the sorting key is the primary key of the benchmark, which also is ClickHouse's sparse primary index.
There are no secondary indexes, constraints or statistics, so `-xii`, `-xic` and `-xis` have no scripts.
CHAR/VARCHAR are `String` (`FixedString` pads with `\0`, not blanks).
TPC-DS columns without `NOT NULL` are `Nullable` (empty fields load as NULL), dates are `Date32` (TPC-DS dates start in 1900).
The loaders (`bexhoma/loader_tpch_clickhouse`, `bexhoma/loader_tpcds_clickhouse`) send each flat file with `INSERT INTO <table> FORMAT CSV` (delimiter `|`, double quotes are data).

In the cluster, a distributed table is a MergeTree table `<name>_local` on every shard (`ON CLUSTER bexhoma`, columns and sorting key as ClickHouse) and a Distributed table `<name>` on the coordinator and on every shard; rows are spread by the first column of the sorting key.
A replicated table is a `ReplicatedMergeTree` on every shard and on the coordinator, all replicas of one table.
A Distributed table uses `distributed_foreground_insert=1`, so the load time includes sending the rows to the shards.

DDL parameters (`-xddl`, see [DDL parameters](DBMS.md#ddl-parameters--xddl)), the same for ClickHouse and ClickHouseCluster; the dimension placement of TPC-H in the cluster is `-xdim`:

| Key | Benchmarks | Values | Default | Effect |
|---|---|---|---|---|
| `order_orders` | TPC-H | `key`, `date` | `key` | sort key (= primary index) of orders: by key, or by date first so date ranges (Q3-Q5, Q7-Q10, Q12) skip granules |
| `order_lineitem` | TPC-H | `key`, `date` | `key` | sort key (= primary index) of lineitem: by key, or by ship date first so date ranges (Q1, Q6, Q7, Q14, Q15, Q20) skip granules |
| `partition_orders` | TPC-H | `none`, `year`, `month` | `none` | partitions of orders by order date: queries with a date range skip whole partitions; more partitions mean more parts per insert block |
| `partition_lineitem` | TPC-H | `none`, `year`, `month` | `none` | partitions of lineitem by ship date: queries with a ship date range (Q1, Q6, Q14, Q15, Q20) skip whole partitions; more partitions mean more parts per insert block |
| `index_granularity` | TPC-H | integer | `8192` | rows per granule (= entry of the sparse primary index) of orders and lineitem (ClickHouse default 8192): smaller granules skip more precisely, the index grows |
| `wide_parts` | TPC-H | `default`, `wide`, `compact` | `default` | part format of orders and lineitem by min_bytes_for_wide_part: default (10 MiB: small parts compact, one file; larger parts wide, a file per column), wide (every part), compact (every part up to 1 TiB); parallel loaders write many small parts |
| `low_cardinality` | TPC-H | `off`, `on` | `off` | dictionary encoding of the string columns with few distinct values (flags, modes, priorities, segments, brands, types, containers, nation and region names): faster filters and GROUP BY |
| `codec` | TPC-H | `default`, `zstd1`, `zstd3` | `default` | compression of all columns of orders and lineitem (default: the server setting, LZ4): bytes read vs. CPU per scan |


### Query Variants

The query files have variants with the key `Clickhouse` where ClickHouse differs from standard SQL, and where a query has a correlated subquery, which ClickHouse cannot run on Distributed tables.
Every variant returns the same result as the original query.

* TPC-H: Q2, Q4, Q11, Q14, Q17, Q20, Q21, Q22 (see [TPC-H Queries](Queries-TPC-H.html))
* TPC-DS: Q1, Q6, Q10, Q16, Q30, Q32, Q35, Q41, Q47, Q49, Q57, Q58, Q66, Q69, Q81, Q92, Q94

| Reason | Rewrite | Queries |
|---|---|---|
| correlated subquery (ClickHouseCluster) | `EXISTS` as `IN`, `NOT EXISTS` as `NOT IN` over non-NULL keys, a correlated aggregate as a join to a derived table grouped by the key | TPC-H Q4, Q17, Q21, Q22; TPC-DS Q1, Q6, Q10, Q16, Q30, Q32, Q35, Q41, Q69, Q81, Q92, Q94 |
| the name of a selected `t.col` is `t.col`, not `col` | alias, or address the column as `` `t.col` `` | TPC-DS Q47, Q57, Q58 |
| `ORDER BY` directly after a parenthesized `UNION` | the `UNION` as a subquery | TPC-DS Q49 |
| an alias is visible in its own select list (`sum(x) as x`) | qualify the column of the subquery | TPC-DS Q66 |

In TPC-DS Q1 the parameter `AGG_FIELD` names columns in lower case: ClickHouse identifiers are case-sensitive.

### Load Durability

`-xld` has no effect on ClickHouse: there are no durability scripts for it.

### Reset Scripts

With `-ar`, the reset runs before each benchmarking round:

1. Statistics: n/a (no optimizer statistics unless declared per column)
2. Persist: `reset-flush.sh`: `sync` (an `INSERT` writes its parts without fsync); in the cluster first `SYSTEM FLUSH DISTRIBUTED` on every Distributed table and `SYSTEM SYNC REPLICA ON CLUSTER` on every replicated table (`reset-<benchmark>.sql`, coordinator), then `reset-flush.sh` in every worker (`set_script_target('workers')`)
3. Counters: n/a (`system.events` cannot be reset)

See [Reset scripts](DBMS.md#reset-scripts--ar) for the reset contract.
There is no test run for ClickHouse in [Test: Reset Scripts](Test-Reset.md) yet.


## TPC-DS

For performing the experiment we can run the [tpcds file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpcds.py).

```bash
bexhoma tpcds \
  -dbms ClickHouse \
  -sf 3 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -xdt \
  -m \
  -ma \
  -ms $BEXHOMA_MS \
  -tr \
  -lc 16 \
  -rc 16 \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -ks no \
  run &>$LOG_DIR/docs_tpcds_clickhouse.log
```

The TPC-DS schema declares the columns without `NOT NULL` as `Nullable`, so empty fields of the flat files load as NULL.
Dates are `Date32`, since TPC-DS dates start in 1900.

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_clickhouse_summary.md" target="_blank" rel="noopener">docs_tpcds_clickhouse.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 385s 
* Code: 1793782014
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Data transfer volume per query is also measured.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by sidecar containers.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['ClickHouse'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 16 CPU and 64Gi RAM. CPU limit is 16. RAM limit is 64Gi.

### Connections
* clickhouse-1-1-1-1-1 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:793442
  * datadisk:2318
  * volume_size:49G
  * volume_used:2.3G
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793782014

### SUT Container Restarts
* bexhoma-sut-clickhouse-1-1793782014-576dbd67f7-vb4bk: 0

### Workflow

#### Actual

* DBMS ClickHouse-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS ClickHouse-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| ClickHouse-1-1 |                1 |    3 |       55.00 |           2.00 |            0.00 |         38.00 |            2.00 |              8 |           0 |             | None           |             0 | False         |              196.36 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| clickhouse-1-1-1-1-1 | ClickHouse-1    | clickhouse-1-1-1 | clickhouse-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |         37 |            0.09 |           136468.18 |          28897.30 |          -1 | clickhouse-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| clickhouse-1-1-1 | clickhouse-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |         37 |            0.09 |           136468.18 |          28897.30 |          -1 |

#### Query Completion per Phase

| phase            |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:-----------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| clickhouse-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   clickhouse-1-1-1-1-1 |
|:--------------|-----------------------:|
| TPC-DS Q1     |                  70.74 |
| TPC-DS Q2     |                  71.54 |
| TPC-DS Q3     |                  22.17 |
| TPC-DS Q4     |                 696.76 |
| TPC-DS Q5     |                  67.75 |
| TPC-DS Q6     |                  48.24 |
| TPC-DS Q7     |                  61.20 |
| TPC-DS Q8     |                  66.98 |
| TPC-DS Q9     |                 153.93 |
| TPC-DS Q10    |                  66.49 |
| TPC-DS Q11    |                 652.70 |
| TPC-DS Q12    |                  26.90 |
| TPC-DS Q13    |                  73.49 |
| TPC-DS Q14a+b |                2961.67 |
| TPC-DS Q15    |                  48.65 |
| TPC-DS Q16    |                  74.76 |
| TPC-DS Q17    |                  72.38 |
| TPC-DS Q18    |                  66.57 |
| TPC-DS Q19    |                  31.87 |
| TPC-DS Q20    |                  26.36 |
| TPC-DS Q21    |                  30.17 |
| TPC-DS Q22    |                 111.99 |
| TPC-DS Q23a+b |                1153.70 |
| TPC-DS Q24a+b |                 350.81 |
| TPC-DS Q25    |                  60.53 |
| TPC-DS Q26    |                  42.89 |
| TPC-DS Q27    |                  81.80 |
| TPC-DS Q28    |                 114.29 |
| TPC-DS Q29    |                  66.38 |
| TPC-DS Q30    |                  85.56 |
| TPC-DS Q31    |                 161.73 |
| TPC-DS Q32    |                  31.45 |
| TPC-DS Q33    |                  49.71 |
| TPC-DS Q34    |                  27.27 |
| TPC-DS Q35    |                  67.35 |
| TPC-DS Q36    |                  50.63 |
| TPC-DS Q37    |                  36.91 |
| TPC-DS Q38    |                 286.22 |
| TPC-DS Q39a+b |                 171.01 |
| TPC-DS Q40    |                  28.92 |
| TPC-DS Q41    |                  20.50 |
| TPC-DS Q42    |                  20.48 |
| TPC-DS Q43    |                  17.69 |
| TPC-DS Q44    |                  59.13 |
| TPC-DS Q45    |                  40.69 |
| TPC-DS Q46    |                  62.45 |
| TPC-DS Q47    |                 290.35 |
| TPC-DS Q48    |                  70.00 |
| TPC-DS Q49    |                  69.63 |
| TPC-DS Q50    |                  44.37 |
| TPC-DS Q51    |                 215.76 |
| TPC-DS Q52    |                  21.19 |
| TPC-DS Q53    |                  34.04 |
| TPC-DS Q54    |                  51.91 |
| TPC-DS Q55    |                  19.04 |
| TPC-DS Q56    |                  68.87 |
| TPC-DS Q57    |                 182.09 |
| TPC-DS Q58    |                  61.47 |
| TPC-DS Q59    |                 100.70 |
| TPC-DS Q60    |                  45.83 |
| TPC-DS Q61    |                  18.38 |
| TPC-DS Q62    |                  30.18 |
| TPC-DS Q63    |                  72.92 |
| TPC-DS Q64    |                 852.19 |
| TPC-DS Q65    |                 134.71 |
| TPC-DS Q66    |                 215.81 |
| TPC-DS Q67    |                1344.98 |
| TPC-DS Q68    |                  35.83 |
| TPC-DS Q69    |                  57.36 |
| TPC-DS Q70    |                  58.47 |
| TPC-DS Q71    |                  43.70 |
| TPC-DS Q72    |                1517.13 |
| TPC-DS Q73    |                  27.67 |
| TPC-DS Q74    |                 474.13 |
| TPC-DS Q75    |                 266.33 |
| TPC-DS Q76    |                  41.42 |
| TPC-DS Q77    |                  79.80 |
| TPC-DS Q78    |                 181.69 |
| TPC-DS Q79    |                  65.34 |
| TPC-DS Q80    |                 128.54 |
| TPC-DS Q81    |                 153.42 |
| TPC-DS Q82    |                  61.27 |
| TPC-DS Q83    |                 124.08 |
| TPC-DS Q84    |                  72.45 |
| TPC-DS Q85    |                 186.66 |
| TPC-DS Q86    |                  28.50 |
| TPC-DS Q87    |                 273.93 |
| TPC-DS Q88    |                 146.14 |
| TPC-DS Q89    |                  28.68 |
| TPC-DS Q90    |                  28.77 |
| TPC-DS Q91    |                  33.97 |
| TPC-DS Q92    |                  26.15 |
| TPC-DS Q93    |                  58.12 |
| TPC-DS Q94    |                  71.96 |
| TPC-DS Q95    |                 292.67 |
| TPC-DS Q96    |                  22.88 |
| TPC-DS Q97    |                  73.77 |
| TPC-DS Q98    |                  37.28 |
| TPC-DS Q99    |                  84.80 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 |        38.13 |      0.46 |           0.95 |                  2.71 |

### Loading phase: component data generator

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 |        18.48 |      0.00 |           0.01 |                  1.02 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 |        32.64 |      0.98 |           2.21 |                  4.49 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 |        18.71 |      0.97 |           0.35 |                  0.35 |

### Missing Monitoring Metrics
* Memory Usage, Working Set [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Queries [queries/s] |   Running Queries [count] |   Failed Queries [count] |   Rows Read [rows/s] |   Data Read, uncompressed [MiB/s] |
|:-------------------|----------------------:|--------------------------:|-------------------------:|---------------------:|----------------------------------:|
| clickhouse-1-1-1-1 |                  0.26 |                      1.00 |                     0.00 |            191579.49 |                             11.36 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Queries [queries/s] |   Running Queries [count] |   Failed Queries [count] |   Rows Read [rows/s] |   Data Read, uncompressed [MiB/s] |
|:-------------------|----------------------:|--------------------------:|-------------------------:|---------------------:|----------------------------------:|
| clickhouse-1-1-1-1 |                  0.43 |                      0.00 |                     0.00 |           4227672.05 |                             65.33 |

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
* TEST skipped: Monitoring metrics missing (data pre-existing; job pods ran shorter than scrape interval; series exists only while non-zero)
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

The same for the cluster:

```bash
bexhoma tpcds \
  -dbms ClickHouseCluster \
  -nw 3 \
  -sf 3 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -xdt \
  -m \
  -ma \
  -ms $BEXHOMA_MS \
  -tr \
  -lc 16 \
  -rc 16 \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -rnw $BEXHOMA_NODES_WORKER \
  -ks no \
  run &>$LOG_DIR/docs_tpcds_clickhouse_cluster.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_clickhouse_cluster_summary.md" target="_blank" rel="noopener">docs_tpcds_clickhouse_cluster.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 554s 
* Code: 1793782488
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Data transfer volume per query is also measured.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by sidecar containers.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['ClickHouseCluster'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 16 CPU and 64Gi RAM. CPU limit is 16. RAM limit is 64Gi.

### Connections
* clickhousecluster-1-1-1-1-1 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:793448
  * datadisk:153
  * volume_size:49G
  * volume_used:153M
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * worker 0
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:602227
    * datadisk:444
    * volume_size:49G
    * volume_used:444M
    * cpu_list:0-127
  * worker 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:793448
    * datadisk:830
    * volume_size:49G
    * volume_used:830M
    * cpu_list:0-223
  * worker 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:605346
    * datadisk:633
    * volume_size:49G
    * volume_used:633M
    * cpu_list:0-127
  * resources_total: 64.0 CPU, 256.0 GiB RAM requested in 4 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
    * worker: 3 x, 48.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793782488
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-clickhousecluster-1-1793782488-69dd989978-xbsqs: 0
* bx-w-clickhousecluster-nvme-tpcds-3-0: 0
* bx-w-clickhousecluster-nvme-tpcds-3-1: 0
* bx-w-clickhousecluster-nvme-tpcds-3-2: 0

### Workflow

#### Actual

* DBMS ClickHouseCluster-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS ClickHouseCluster-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                       |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| ClickHouseCluster-1-1 |                1 |    3 |       50.00 |           7.00 |            1.00 |         31.00 |            2.00 |              8 |           0 |             | None           |             0 | False         |              216.00 | False               |

### Benchmarking

#### Per Connection

| DBMS                        | configuration       | phase                   | job                       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                         |
|:----------------------------|:--------------------|:------------------------|:--------------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------------------|
| clickhousecluster-1-1-1-1-1 | ClickHouseCluster-1 | clickhousecluster-1-1-1 | clickhousecluster-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |        185 |            0.63 |            17782.07 |           5779.46 |          -1 | clickhousecluster-1-1-1-1-1 |

#### Per Phase

|                         | phase                   |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------------|:------------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| clickhousecluster-1-1-1 | clickhousecluster-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |        185 |            0.63 |            17782.07 |           5779.46 |          -1 |

#### Query Completion per Phase

| phase                   |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:------------------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| clickhousecluster-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   clickhousecluster-1-1-1-1-1 |
|:--------------|------------------------------:|
| TPC-DS Q1     |                        194.14 |
| TPC-DS Q2     |                        224.01 |
| TPC-DS Q3     |                        777.81 |
| TPC-DS Q4     |                      47363.72 |
| TPC-DS Q5     |                        515.27 |
| TPC-DS Q6     |                       1528.94 |
| TPC-DS Q7     |                        980.41 |
| TPC-DS Q8     |                        262.61 |
| TPC-DS Q9     |                        426.21 |
| TPC-DS Q10    |                       2001.50 |
| TPC-DS Q11    |                      11933.61 |
| TPC-DS Q12    |                        176.24 |
| TPC-DS Q13    |                        740.61 |
| TPC-DS Q14a+b |                       3912.35 |
| TPC-DS Q15    |                        216.40 |
| TPC-DS Q16    |                        326.33 |
| TPC-DS Q17    |                       1682.86 |
| TPC-DS Q18    |                       1085.19 |
| TPC-DS Q19    |                       2100.22 |
| TPC-DS Q20    |                        175.20 |
| TPC-DS Q21    |                        162.82 |
| TPC-DS Q22    |                        223.94 |
| TPC-DS Q23a+b |                       6624.36 |
| TPC-DS Q24a+b |                       2061.91 |
| TPC-DS Q25    |                       1737.64 |
| TPC-DS Q26    |                        763.98 |
| TPC-DS Q27    |                        806.66 |
| TPC-DS Q28    |                        385.67 |
| TPC-DS Q29    |                       1776.55 |
| TPC-DS Q30    |                        354.57 |
| TPC-DS Q31    |                       1384.93 |
| TPC-DS Q32    |                        175.47 |
| TPC-DS Q33    |                        225.24 |
| TPC-DS Q34    |                        123.77 |
| TPC-DS Q35    |                       1351.23 |
| TPC-DS Q36    |                        173.53 |
| TPC-DS Q37    |                       1947.52 |
| TPC-DS Q38    |                        623.56 |
| TPC-DS Q39a+b |                       1337.77 |
| TPC-DS Q40    |                        264.70 |
| TPC-DS Q41    |                         66.97 |
| TPC-DS Q42    |                        897.51 |
| TPC-DS Q43    |                        696.05 |
| TPC-DS Q44    |                         84.95 |
| TPC-DS Q45    |                        274.25 |
| TPC-DS Q46    |                        185.58 |
| TPC-DS Q47    |                       7704.11 |
| TPC-DS Q48    |                        656.17 |
| TPC-DS Q49    |                        342.47 |
| TPC-DS Q50    |                        551.57 |
| TPC-DS Q51    |                        438.20 |
| TPC-DS Q52    |                        853.32 |
| TPC-DS Q53    |                       1255.39 |
| TPC-DS Q54    |                        372.40 |
| TPC-DS Q55    |                        744.27 |
| TPC-DS Q56    |                        247.06 |
| TPC-DS Q57    |                       4298.12 |
| TPC-DS Q58    |                        306.27 |
| TPC-DS Q59    |                        483.67 |
| TPC-DS Q60    |                        302.65 |
| TPC-DS Q61    |                        401.03 |
| TPC-DS Q62    |                        134.73 |
| TPC-DS Q63    |                       1103.66 |
| TPC-DS Q64    |                       9721.62 |
| TPC-DS Q65    |                        644.84 |
| TPC-DS Q66    |                        604.82 |
| TPC-DS Q67    |                       1528.49 |
| TPC-DS Q68    |                        192.14 |
| TPC-DS Q69    |                       1665.21 |
| TPC-DS Q70    |                        373.10 |
| TPC-DS Q71    |                        354.96 |
| TPC-DS Q72    |                       8476.05 |
| TPC-DS Q73    |                        127.25 |
| TPC-DS Q74    |                       9988.71 |
| TPC-DS Q75    |                       1221.97 |
| TPC-DS Q76    |                        182.76 |
| TPC-DS Q77    |                        278.43 |
| TPC-DS Q78    |                       1145.74 |
| TPC-DS Q79    |                        175.50 |
| TPC-DS Q80    |                        706.44 |
| TPC-DS Q81    |                        289.70 |
| TPC-DS Q82    |                       1792.85 |
| TPC-DS Q83    |                        363.01 |
| TPC-DS Q84    |                        436.05 |
| TPC-DS Q85    |                       1757.49 |
| TPC-DS Q86    |                        105.58 |
| TPC-DS Q87    |                        654.51 |
| TPC-DS Q88    |                        901.63 |
| TPC-DS Q89    |                       1767.60 |
| TPC-DS Q90    |                        153.76 |
| TPC-DS Q91    |                        628.22 |
| TPC-DS Q92    |                        155.22 |
| TPC-DS Q93    |                        326.50 |
| TPC-DS Q94    |                        277.23 |
| TPC-DS Q95    |                       1746.25 |
| TPC-DS Q96    |                         91.87 |
| TPC-DS Q97    |                        356.07 |
| TPC-DS Q98    |                        178.71 |
| TPC-DS Q99    |                        155.95 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |        22.87 |      0.36 |           0.51 |                  0.55 |

### Loading phase: component worker

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |        95.81 |      1.29 |           1.54 |                  2.99 |

### Loading phase: component data generator

| DBMS                      | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|:-------------|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS                      | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|:-------------|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 | n/a          |         0 |           1.22 |                  3.42 |

### Benchmarking phase: SUT deployment

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |       275.58 |      2.30 |           3.41 |                  3.48 |

### Benchmarking phase: component worker

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |       963.11 |      9.22 |           7.08 |                  9.01 |

### Benchmarking phase: component benchmarker

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |        23.06 |      0.10 |           0.36 |                  0.37 |

### Missing Monitoring Metrics
* Memory Usage, Working Set [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS                      |   Queries [queries/s] |   Running Queries [count] |   Failed Queries [count] |   Rows Read [rows/s] |   Data Read, uncompressed [MiB/s] |
|:--------------------------|----------------------:|--------------------------:|-------------------------:|---------------------:|----------------------------------:|
| clickhousecluster-1-1-1-1 |                  1.68 |                      1.00 |                     0.00 |            543399.81 |                             32.27 |

#### Benchmarking phase: component worker

| DBMS                      |   Queries [queries/s] |   Running Queries [count] |   Failed Queries [count] |   Rows Read [rows/s] |   Data Read, uncompressed [MiB/s] |
|:--------------------------|----------------------:|--------------------------:|-------------------------:|---------------------:|----------------------------------:|
| clickhousecluster-1-1-1-1 |                  9.86 |                      5.00 |                     0.00 |          58005847.42 |                           1142.15 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (data pre-existing; job pods ran shorter than scrape interval; series exists only while non-zero)
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
For ClickHouse, a loader image of its own is used: RF1 is applied with `INSERT INTO ... FORMAT CSV` and RF2 with lightweight `DELETE` statements in chunks of 10000 order keys.
Here, 3 query streams run in parallel with a refresh stream of 3 RF1+RF2 pairs.

```bash
bexhoma tpch   -dbms ClickHouse   -sf 1   -nlp 8   -ne 3   -xrs 3   -ms $BEXHOMA_MS   -tr   -lc 16   -rc 16   -lr 64Gi   -rr 64Gi   -rss 50Gi   -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK   -ks no   run &>$LOG_DIR/docs_tpch_clickhouse_refresh.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_clickhouse_refresh_summary.md" target="_blank" rel="noopener">docs_tpch_clickhouse_refresh.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 351s 
* Code: 1794003999
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * A TPC-H refresh stream (RF1+RF2) runs in parallel, with 3 pair(s) applied per round.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.13.
  * Experiment is limited to DBMS ['ClickHouse'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [3] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 16 CPU and 64Gi RAM. CPU limit is 16. RAM limit is 64Gi.

### Connections
* clickhouse-1-1-1-1-1 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:877365
  * datadisk:821
  * volume_size:1.8T
  * volume_used:857G
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794003999
* clickhouse-1-1-1-1-2 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:877365
  * datadisk:821
  * volume_size:1.8T
  * volume_used:857G
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794003999
* clickhouse-1-1-1-1-3 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:877365
  * datadisk:821
  * volume_size:1.8T
  * volume_used:857G
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794003999

### SUT Container Restarts
* bexhoma-sut-clickhouse-1-1794003999-597587d64-2bp22: 0

### Workflow

#### Actual

* DBMS ClickHouse-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

#### Planned

* DBMS ClickHouse-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| ClickHouse-1-1 |                1 |    1 |       30.00 |           3.00 |           13.00 |          6.00 |            2.00 |              8 |           0 |             | None           |             0 | False         |              120.00 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| clickhouse-1-1-1-1-1 | ClickHouse-1    | clickhouse-1-1-1 | clickhouse-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |          5 |            0.06 |            64063.12 |          15840.00 |          -1 | clickhouse-1-1-1-1-1 |
| clickhouse-1-1-1-1-2 | ClickHouse-1    | clickhouse-1-1-1 | clickhouse-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |          4 |            0.05 |            66571.64 |          19800.00 |          -1 | clickhouse-1-1-1-1-2 |
| clickhouse-1-1-1-1-3 | ClickHouse-1    | clickhouse-1-1-1 | clickhouse-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |          7 |            0.05 |            68221.84 |          11314.29 |          -1 | clickhouse-1-1-1-1-3 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| clickhouse-1-1-1 | clickhouse-1-1-1 |                1 |        1 |               1 |           3 | 1.00 |               66 |                  66 |          7 |            0.05 |            66263.38 |          33942.86 |          -1 |

#### Query Completion per Phase

| phase            |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:-----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| clickhouse-1-1-1 |      3 | 3/3                                 | 3/3                                      | 3/3                            | 3/3                                        | 3/3                                | 3/3                                     | 3/3                                | 3/3                                | 3/3                                      | 3/3                                         | 3/3                                          | 3/3                                             | 3/3                                 | 3/3                                  | 3/3                              | 3/3                                       | 3/3                                        | 3/3                                 | 3/3                              | 3/3                                    | 3/3                                                   | 3/3                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### tpch_refresh

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count | benchmark_begin     | benchmark_end       |   benchmark_duration |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|:--------------------|:--------------------|---------------------:|
| clickhouse-1-1-1-2-1 | clickhouse-1-1-1 | clickhouse-1-1-1-2 |                1 |        1 |               2 |           1 | 2026-11-06 23:31:51 | 2026-11-06 23:31:53 |                    2 |

### Latency of Timer Execution [ms]
| Queries                                             |   clickhouse-1-1-1-1-1 |   clickhouse-1-1-1-1-2 |   clickhouse-1-1-1-1-3 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                 162.68 |                  78.00 |                 159.67 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                  59.13 |                  62.32 |                  63.86 |
| Shipping Priority (TPC-H Q3)                        |                  49.53 |                  49.28 |                  62.75 |
| Order Priority Checking Query (TPC-H Q4)            |                 184.63 |                 185.34 |                 171.16 |
| Local Supplier Volume (TPC-H Q5)                    |                  71.61 |                  72.71 |                  42.37 |
| Forecasting Revenue Change (TPC-H Q6)               |                  17.22 |                  18.27 |                  20.90 |
| Volume Shipping Query (TPC-H Q7)                    |                  40.82 |                  50.72 |                  53.90 |
| National Market Share (TPC-H Q8)                    |                  50.53 |                  47.31 |                  54.60 |
| Product Type Profit Measure (TPC-H Q9)              |                  65.58 |                  66.29 |                  63.41 |
| Returned Item Reporting Query (TPC-H Q10)           |                  83.99 |                  85.88 |                  62.51 |
| Important Stock Identification (TPC-H Q11)          |                  47.43 |                  23.36 |                  24.62 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                  34.89 |                  31.68 |                  34.21 |
| Customer Distribution (TPC-H Q13)                   |                  42.33 |                  39.09 |                  36.52 |
| Promotion Effect Query (TPC-H Q14)                  |                  30.75 |                  32.16 |                  33.20 |
| Top Supplier Query (TPC-H Q15)                      |                  54.27 |                  38.18 |                  44.13 |
| Parts/Supplier Relationship (TPC-H Q16)             |                  36.05 |                  34.31 |                  33.16 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                  30.92 |                  31.14 |                  50.01 |
| Large Volume Customer (TPC-H Q18)                   |                  43.48 |                  44.39 |                  42.37 |
| Discounted Revenue (TPC-H Q19)                      |                  46.70 |                 198.89 |                  42.01 |
| Potential Part Promotion (TPC-H Q20)                |                  43.94 |                  42.36 |                  43.83 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 384.71 |                 392.70 |                 396.14 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  56.50 |                  29.78 |                  29.87 |

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

On ClickHouseCluster, `orders` and `lineitem` are Distributed tables on top of `<name>_local` tables on the shards.
RF1 inserts through the Distributed tables, which route the rows to the shards by order key.
A Distributed table cannot be deleted from, and the coordinator has no `_local` tables, so RF2 reads the shards of the cluster from `system.clusters` and deletes on each of them.
This holds for both placements of the dimension tables (`-xdim replicated` and `-xdim distributed`).

```bash
bexhoma tpch \
  -dbms ClickHouseCluster \
  -nw 3 \
  -sf 1 \
  -nlp 8 \
  -ne 3 \
  -xrs 3 \
  -ms $BEXHOMA_MS \
  -tr \
  -lc 16 \
  -rc 16 \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rnw $BEXHOMA_NODES_WORKER \
  -ks no \
  run &>$LOG_DIR/docs_tpch_clickhouse_cluster_refresh.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_clickhouse_cluster_refresh_summary.md" target="_blank" rel="noopener">docs_tpch_clickhouse_cluster_refresh.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 378s 
* Code: 1794046827
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * Dimensions of ClickHouseCluster are a full copy on every node (-xdim replicated).
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * A TPC-H refresh stream (RF1+RF2) runs in parallel, with 3 pair(s) applied per round.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.13.
  * Experiment is limited to DBMS ['ClickHouseCluster'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [3] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 16 CPU and 64Gi RAM. CPU limit is 16. RAM limit is 64Gi.

### Connections
* clickhousecluster-1-1-1-1-1 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806763
  * datadisk:260
  * volume_size:49G
  * volume_used:260M
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * worker 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:204881
    * datadisk:363
    * volume_size:49G
    * volume_used:363M
    * cpu_list:0-127
  * worker 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:806763
    * datadisk:365
    * volume_size:49G
    * volume_used:365M
    * cpu_list:0-223
  * worker 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:716994
    * datadisk:366
    * volume_size:49G
    * volume_used:366M
    * cpu_list:0-127
  * resources_total: 64.0 CPU, 256.0 GiB RAM requested in 4 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
    * worker: 3 x, 48.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794046827
    * BEXHOMA_WORKERS:3
* clickhousecluster-1-1-1-1-2 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806763
  * datadisk:260
  * volume_size:49G
  * volume_used:260M
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * worker 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:204881
    * datadisk:363
    * volume_size:49G
    * volume_used:363M
    * cpu_list:0-127
  * worker 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:806763
    * datadisk:365
    * volume_size:49G
    * volume_used:365M
    * cpu_list:0-223
  * worker 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:716994
    * datadisk:366
    * volume_size:49G
    * volume_used:366M
    * cpu_list:0-127
  * resources_total: 64.0 CPU, 256.0 GiB RAM requested in 4 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
    * worker: 3 x, 48.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794046827
    * BEXHOMA_WORKERS:3
* clickhousecluster-1-1-1-1-3 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806763
  * datadisk:260
  * volume_size:49G
  * volume_used:260M
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * worker 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:204881
    * datadisk:363
    * volume_size:49G
    * volume_used:363M
    * cpu_list:0-127
  * worker 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:806763
    * datadisk:365
    * volume_size:49G
    * volume_used:365M
    * cpu_list:0-223
  * worker 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:716994
    * datadisk:366
    * volume_size:49G
    * volume_used:366M
    * cpu_list:0-127
  * resources_total: 64.0 CPU, 256.0 GiB RAM requested in 4 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
    * worker: 3 x, 48.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794046827
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-clickhousecluster-1-1794046827-65cf5965fb-b2hpz: 0
* bx-w-chc-nvme-tpch-1-0: 0
* bx-w-chc-nvme-tpch-1-1: 0
* bx-w-chc-nvme-tpch-1-2: 0

### Workflow

#### Actual

* DBMS ClickHouseCluster-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

#### Planned

* DBMS ClickHouseCluster-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

### Loading

#### Per Run

|                       |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| ClickHouseCluster-1-1 |                1 |    1 |       42.00 |           6.00 |           19.00 |          4.00 |            4.00 |              8 |           0 |             | None           |             0 | False         |               85.71 | False               |

### Benchmarking

#### Per Connection

| DBMS                        | configuration       | phase                   | job                       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                         |
|:----------------------------|:--------------------|:------------------------|:--------------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------------------|
| clickhousecluster-1-1-1-1-1 | ClickHouseCluster-1 | clickhousecluster-1-1-1 | clickhousecluster-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         15 |            0.18 |            19585.92 |           5280.00 |          -1 | clickhousecluster-1-1-1-1-1 |
| clickhousecluster-1-1-1-1-2 | ClickHouseCluster-1 | clickhousecluster-1-1-1 | clickhousecluster-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         15 |            0.18 |            19784.66 |           5280.00 |          -1 | clickhousecluster-1-1-1-1-2 |
| clickhousecluster-1-1-1-1-3 | ClickHouseCluster-1 | clickhousecluster-1-1-1 | clickhousecluster-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         11 |            0.17 |            21765.33 |           7200.00 |          -1 | clickhousecluster-1-1-1-1-3 |

#### Per Phase

|                         | phase                   |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------------|:------------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| clickhousecluster-1-1-1 | clickhousecluster-1-1-1 |                1 |        1 |               1 |           3 | 1.00 |               66 |                  66 |         15 |            0.18 |            20355.38 |          15840.00 |          -1 |

#### Query Completion per Phase

| phase                   |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:------------------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| clickhousecluster-1-1-1 |      3 | 3/3                                 | 3/3                                      | 3/3                            | 3/3                                        | 3/3                                | 3/3                                     | 3/3                                | 3/3                                | 3/3                                      | 3/3                                         | 3/3                                          | 3/3                                             | 3/3                                 | 3/3                                  | 3/3                              | 3/3                                       | 3/3                                        | 3/3                                 | 3/3                              | 3/3                                    | 3/3                                                   | 3/3                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### tpch_refresh

| connection                  | phase                   | job                       |   experiment_run |   client |   benchmark_run |   pod_count | benchmark_begin     | benchmark_end       |   benchmark_duration |
|:----------------------------|:------------------------|:--------------------------|-----------------:|---------:|----------------:|------------:|:--------------------|:--------------------|---------------------:|
| clickhousecluster-1-1-1-2-1 | clickhousecluster-1-1-1 | clickhousecluster-1-1-1-2 |                1 |        1 |               2 |           1 | 2026-11-07 11:25:48 | 2026-11-07 11:25:52 |                    4 |

### Latency of Timer Execution [ms]
| Queries                                             |   clickhousecluster-1-1-1-1-1 |   clickhousecluster-1-1-1-1-2 |   clickhousecluster-1-1-1-1-3 |
|:----------------------------------------------------|------------------------------:|------------------------------:|------------------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                        376.71 |                        350.05 |                        169.41 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                         58.84 |                         57.51 |                         59.31 |
| Shipping Priority (TPC-H Q3)                        |                        173.43 |                        160.29 |                        190.05 |
| Order Priority Checking Query (TPC-H Q4)            |                        441.88 |                        460.00 |                        497.05 |
| Local Supplier Volume (TPC-H Q5)                    |                        251.26 |                        237.73 |                        239.10 |
| Forecasting Revenue Change (TPC-H Q6)               |                         47.32 |                         41.68 |                         40.30 |
| Volume Shipping Query (TPC-H Q7)                    |                        187.00 |                        179.50 |                        195.26 |
| National Market Share (TPC-H Q8)                    |                        270.96 |                        255.49 |                        286.57 |
| Product Type Profit Measure (TPC-H Q9)              |                        692.45 |                        364.00 |                        337.55 |
| Returned Item Reporting Query (TPC-H Q10)           |                        161.97 |                        196.28 |                        156.98 |
| Important Stock Identification (TPC-H Q11)          |                         43.34 |                         36.17 |                         24.28 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                        721.44 |                        704.82 |                        699.53 |
| Customer Distribution (TPC-H Q13)                   |                        197.80 |                        173.50 |                        160.53 |
| Promotion Effect Query (TPC-H Q14)                  |                         80.34 |                        146.05 |                         66.68 |
| Top Supplier Query (TPC-H Q15)                      |                        103.50 |                        218.87 |                        177.25 |
| Parts/Supplier Relationship (TPC-H Q16)             |                         39.32 |                         45.42 |                         34.52 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                        230.92 |                        228.89 |                        268.67 |
| Large Volume Customer (TPC-H Q18)                   |                        646.33 |                        374.27 |                        570.03 |
| Discounted Revenue (TPC-H Q19)                      |                        134.60 |                        141.74 |                        136.37 |
| Potential Part Promotion (TPC-H Q20)                |                        125.75 |                        146.76 |                        117.44 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                       2656.43 |                       2391.39 |                       2285.32 |
| Global Sales Opportunity Query (TPC-H Q22)          |                         42.02 |                         39.75 |                         38.00 |

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

## SSB

The Star Schema Benchmark runs on ClickHouse and ClickHouseCluster, too, see [Example: SSB](Example-SSB.md).
