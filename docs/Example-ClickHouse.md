# Example: Benchmark ClickHouse

ClickHouse is a column-store DBMS for analytical workloads [1].
Bexhoma runs TPC-H and TPC-DS against it in two installations:

* **ClickHouse**: one server (the SUT).
* **ClickHouseCluster**: one coordinator (the SUT) and `-nw` shards (a stateful set of workers, one replica per shard).

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

Both use the official image `clickhouse/clickhouse-server` (26.8, LTS) and the templates [deploymenttemplate-ClickHouse.yml](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-ClickHouse.yml) and [deploymenttemplate-ClickHouseCluster.yml](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-ClickHouseCluster.yml).
Queries run over JDBC (HTTP interface), loaders and init scripts use `clickhouse-client` (native protocol).
See [DBMS](DBMS.html#clickhouse) for the configuration.

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. ClickHouse: https://clickhouse.com/docs
1. ClickHouse in Docker: https://hub.docker.com/r/clickhouse/clickhouse-server
1. Distributed table engine: https://clickhouse.com/docs/engines/table-engines/special/distributed
1. ClickHouse Keeper: https://clickhouse.com/docs/guides/sre/keeper/clickhouse-keeper
1. TPC-H: https://www.tpc.org/tpch/
1. TPC-DS: https://www.tpc.org/tpcds/
1. Orchestrating DBMS Benchmarking in the Cloud with Kubernetes: https://doi.org/10.1007/978-3-030-94437-7_6


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
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ks no \
  run &>$LOG_DIR/docs_tpch_clickhouse_1.log
```

This
* starts a clean instance of ClickHouse (`-dbms`)
  * with 16 CPUs and 64 GiB RAM (`-rc`, `-lc`, `-rr`, `-lr`)
  * data directory on a persistent volume of 50 GiB (`-rss`) of the storage class `$BEXHOMA_STORAGE_CLASS` (`-rst`), removed first if it exists (`-rsr`)
* creates the TPC-H schema (MergeTree tables, sorted by their primary key)
* starts 8 loader pods (`-nlp`)
  * with a data generator (init container) each, which generates a share of TPC-H data of SF=1 (`-sf`)
  * and a loading container each, which sends the flat files with `clickhouse-client` (`INSERT ... FORMAT CSV`)
* runs the check script (row counts, parts, sizes)
* runs 1 stream of the 22 TPC-H queries (`-ne`)
* repeats the benchmark once more (`-nc 2`): bexhoma restarts the SUT, which finds the data on the volume and does not load again
* monitors the SUT (`-m`) and collects ClickHouse's own metrics (`-ma`)
* tests if results match workflow (`-tr`)
* removes the SUT at the end (`-ks no`)
* shows a summary

### Status

You can watch the status while benchmark is running via `bexhoma status`.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1792777036` (removes everything that is related to experiment `1792777036`).

## Evaluate Results

At the end of a benchmark you will see a summary like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_clickhouse_1_summary.md" target="_blank" rel="noopener">docs_tpch_clickhouse_1.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 739s 
* Code: 1792777036
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Data transfer volume per query is also measured.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.8.
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
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:958485
  * datadisk:822
  * volume_size:49G
  * volume_used:822M
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792777036
* clickhouse-1-2-1-1-1 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:958485
  * datadisk:864
  * volume_size:49G
  * volume_used:864M
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792777036

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: ClickHouse-1-2

### SUT Container Restarts
* bexhoma-sut-clickhouse-1-1792777036-5f7588d64c-xjl2q: 0
* bexhoma-sut-clickhouse-1-1792777036-b4f76c66b-4smsw: 0

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
| ClickHouse-1-1 |                1 |    1 |       41.00 |           6.00 |           20.00 |          5.00 |            6.00 |              8 |           0 |             | None           |             0 | False         |               87.80 | False               |
| ClickHouse-1-2 |                2 |    1 |       41.00 |           6.00 |           20.00 |          5.00 |            6.00 |              8 |           0 |             | None           |             0 | False         |               87.80 | True                |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| clickhouse-1-1-1-1-1 | ClickHouse-1    | clickhouse-1-1-1 | clickhouse-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |          9 |            0.06 |            74679.86 |           8800.00 |          -1 | clickhouse-1-1-1-1-1 |
| clickhouse-1-2-1-1-1 | ClickHouse-1    | clickhouse-1-2-1 | clickhouse-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |                  22 |          8 |            0.07 |            60955.95 |           9900.00 |          -1 | clickhouse-1-2-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| clickhouse-1-1-1 | clickhouse-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |          9 |            0.06 |            74679.86 |           8800.00 |          -1 |
| clickhouse-1-2-1 | clickhouse-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |                  22 |          8 |            0.07 |            60955.95 |           9900.00 |          -1 |

#### Query Completion per Phase

| phase            |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:-----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| clickhouse-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| clickhouse-1-2-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   clickhouse-1-1-1-1-1 |   clickhouse-1-2-1-1-1 |
|:----------------------------------------------------|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                 141.84 |                 184.80 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                  53.72 |                  97.91 |
| Shipping Priority (TPC-H Q3)                        |                  43.16 |                  79.68 |
| Order Priority Checking Query (TPC-H Q4)            |                 155.03 |                 172.81 |
| Local Supplier Volume (TPC-H Q5)                    |                  44.95 |                  60.96 |
| Forecasting Revenue Change (TPC-H Q6)               |                  16.70 |                  16.03 |
| Volume Shipping Query (TPC-H Q7)                    |                  59.99 |                  60.11 |
| National Market Share (TPC-H Q8)                    |                  44.31 |                  57.70 |
| Product Type Profit Measure (TPC-H Q9)              |                  57.44 |                  60.57 |
| Returned Item Reporting Query (TPC-H Q10)           |                  68.55 |                  88.47 |
| Important Stock Identification (TPC-H Q11)          |                  22.90 |                  31.17 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                  30.69 |                  45.63 |
| Customer Distribution (TPC-H Q13)                   |                  41.24 |                  64.50 |
| Promotion Effect Query (TPC-H Q14)                  |                  27.10 |                  30.07 |
| Top Supplier Query (TPC-H Q15)                      |                  33.98 |                  36.43 |
| Parts/Supplier Relationship (TPC-H Q16)             |                  28.90 |                  36.28 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                  29.91 |                  32.86 |
| Large Volume Customer (TPC-H Q18)                   |                  61.50 |                  72.04 |
| Discounted Revenue (TPC-H Q19)                      |                  44.94 |                  56.17 |
| Potential Part Promotion (TPC-H Q20)                |                  39.30 |                  38.95 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 371.27 |                 376.58 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  28.66 |                  28.89 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 |        25.60 |      0.25 |           0.40 |                  1.18 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 |         1.42 |      0.00 |           0.04 |                  0.04 |

### Benchmarking phase: SUT deployment

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 | n/a          |      0.16 |           0.77 |                  1.58 |
| clickhouse-1-2-1-1 | n/a          |      0.19 |           0.34 |                  0.43 |

### Benchmarking phase: component benchmarker

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| clickhouse-1-2-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |

### Missing Monitoring Metrics
* Memory Usage, Working Set [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Memory Usage incl. Page Cache [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Utilization Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttled Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU User Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU System Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Memory Usage incl. Page Cache [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log)
* CPU Throttling Rate [s/s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection clickhouse-1-2-1-1 (bexhoma-metrics-clickhouse-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection clickhouse-1-2-1-1 (bexhoma-metrics-clickhouse-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-2-1-1 (bexhoma-metrics-clickhouse-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-2-1-1 (bexhoma-metrics-clickhouse-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Queries [queries/s] |   Running Queries [count] |   Failed Queries [count] |   Rows Read [rows/s] |   Data Read, uncompressed [MiB/s] |
|:-------------------|----------------------:|--------------------------:|-------------------------:|---------------------:|----------------------------------:|
| clickhouse-1-1-1-1 |                  0.23 |                      0.00 |                     0.00 |             37447.64 |                              4.77 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Queries [queries/s] |   Running Queries [count] |   Failed Queries [count] |   Rows Read [rows/s] |   Data Read, uncompressed [MiB/s] |
|:-------------------|----------------------:|--------------------------:|-------------------------:|---------------------:|----------------------------------:|
| clickhouse-1-1-1-1 |                  0.21 |                      0.00 |                     0.00 |             35650.97 |                              4.33 |
| clickhouse-1-2-1-1 |                  0.00 |                      0.00 |                     0.00 |              1397.81 |                              0.04 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Benchmarking phase: SUT deployment contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Benchmarking phase: component benchmarker contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST failed: Monitoring metrics missing
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

### Detailed Evaluation

Results are transformed into pandas DataFrames and can be inspected in detail.
See for example
* [Jupyter Notebooks](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/evaluator_dbmsbenchmarker/notebooks/)

You can connect to an evaluation server locally by `bexhoma jupyter`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888


## Monitoring

[Monitoring](Monitoring.html) can be activated for the DBMS only (`-m`) or for all components (`-mc`).
`-ma` adds application metrics: ClickHouse has its own Prometheus endpoint (port 9363), so there is no exporter sidecar.
The metric set `clickhouse` contains queries per second, running queries, failed queries, rows and data read per second, rows inserted per second, memory tracked by ClickHouse, running merges and the number of parts of MergeTree tables.

At SF=1 the loaders finish within a few seconds, shorter than the scrape interval of 30 seconds.
Their CPU utilization (a rate over two scrapes) is then missing, and the test `Monitoring metrics missing` fails for that metric only; a larger scaling factor gives the loaders a measurable phase.


## ClickHouse as a Cluster

```bash
bexhoma tpch \
  -dbms ClickHouseCluster \
  -nw 3 \
  -sf 1 \
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
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK -rnw $BEXHOMA_NODES_WORKER \
  -ks no \
  run &>$LOG_DIR/docs_tpch_clickhouse_2.log
```

This runs the same benchmark against a cluster of a coordinator and 3 shards (`-nw`) on the nodes `$BEXHOMA_NODES_WORKER` (`-rnw`, one shard per node).
The coordinator and every shard get 16 CPUs, 64 GiB RAM and a volume of 50 GiB.

* At start, every pod writes the cluster `bexhoma` into its configuration (`remote_servers`, one shard per worker).
* The coordinator is not a shard. It is the entry point of the benchmarker and the loaders, and it runs a single-node ClickHouse Keeper, which `ON CLUSTER` statements need.
* A worker is ready when it has a session with the Keeper. Bexhoma runs the init scripts only when all workers are ready.
* `orders` and `lineitem` are a MergeTree table `<name>_local` on every shard and a Distributed table `<name>` on the coordinator and on every shard. The loaders write into the Distributed tables, which pass the rows on to the shards before the `INSERT` returns, so the loading time includes them.
* The dimensions are a `ReplicatedMergeTree` on every shard and on the coordinator (`-xdim replicated`, default): Keeper copies the parts the loaders write on the coordinator to the shards, and a join with `orders`/`lineitem` runs on each shard against its local copy. With `-xdim distributed`, `part`, `partsupp`, `supplier` and `customer` are Distributed tables like `orders` (scripts in `ClickHouseCluster/distributed`, volume `tpch-distributed-<SF>`); `nation` and `region` are replicated in both. TPC-DS has no variant: every table is distributed.
* Queries read the tables on the coordinator. A Distributed table inside a join or `IN` is read once and sent to all shards (`distributed_product_mode = global`), which is correct for every sharding key.
* The check script waits for the replicas, fails if a node holds other rows of a replicated table than the coordinator, and reports rows, parts and sizes per table and node.
* Monitoring sums the metrics of coordinator and shards (components SUT and worker).

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_clickhouse_2_summary.md" target="_blank" rel="noopener">docs_tpch_clickhouse_2.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 918s 
* Code: 1792777045
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Data transfer volume per query is also measured.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.8.
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
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:958486
  * datadisk:169
  * volume_size:49G
  * volume_used:169M
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:958486
    * datadisk:329
    * volume_size:49G
    * volume_used:329M
    * cpu_list:0-223
  * worker 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:471929
    * datadisk:327
    * volume_size:49G
    * volume_used:327M
    * cpu_list:0-127
  * worker 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:350156
    * datadisk:329
    * volume_size:49G
    * volume_used:329M
    * cpu_list:0-127
  * resources_total: 64.0 CPU, 256.0 GiB RAM requested in 4 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
    * worker: 3 x, 48.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792777045
    * BEXHOMA_WORKERS:3
* clickhousecluster-1-2-1-1-1 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:958485
  * datadisk:208
  * volume_size:49G
  * volume_used:208M
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:958486
    * datadisk:378
    * volume_size:49G
    * volume_used:380M
    * cpu_list:0-223
  * worker 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:471929
    * datadisk:374
    * volume_size:49G
    * volume_used:374M
    * cpu_list:0-127
  * worker 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:350155
    * datadisk:390
    * volume_size:49G
    * volume_used:390M
    * cpu_list:0-127
  * resources_total: 64.0 CPU, 256.0 GiB RAM requested in 4 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
    * worker: 3 x, 48.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792777045
    * BEXHOMA_WORKERS:3

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: ClickHouseCluster-1-2

### SUT Container Restarts
* bexhoma-sut-clickhousecluster-1-1792777045-89c8dbc74-k9g96: 0
* bexhoma-worker-clickhousecluster-nvme-tpch-1-0: 0
* bexhoma-worker-clickhousecluster-nvme-tpch-1-1: 0
* bexhoma-worker-clickhousecluster-nvme-tpch-1-2: 0
* bexhoma-sut-clickhousecluster-1-1792777045-7675d6f964-blmqf: 0

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
| ClickHouseCluster-1-1 |                1 |    1 |       56.00 |           6.00 |           37.00 |          4.00 |            6.00 |              8 |           0 |             | None           |             0 | False         |               64.29 | False               |
| ClickHouseCluster-1-2 |                2 |    1 |       56.00 |           6.00 |           37.00 |          4.00 |            6.00 |              8 |           0 |             | None           |             0 | False         |               64.29 | True                |

### Benchmarking

#### Per Connection

| DBMS                        | configuration       | phase                   | job                       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                         |
|:----------------------------|:--------------------|:------------------------|:--------------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------------------|
| clickhousecluster-1-1-1-1-1 | ClickHouseCluster-1 | clickhousecluster-1-1-1 | clickhousecluster-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         25 |            0.47 |             8250.98 |           3168.00 |          -1 | clickhousecluster-1-1-1-1-1 |
| clickhousecluster-1-2-1-1-1 | ClickHouseCluster-1 | clickhousecluster-1-2-1 | clickhousecluster-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         22 |            0.49 |             7899.68 |           3600.00 |          -1 | clickhousecluster-1-2-1-1-1 |

#### Per Phase

|                         | phase                   |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------------|:------------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| clickhousecluster-1-1-1 | clickhousecluster-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         25 |            0.47 |             8250.98 |           3168.00 |          -1 |
| clickhousecluster-1-2-1 | clickhousecluster-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         22 |            0.49 |             7899.68 |           3600.00 |          -1 |

#### Query Completion per Phase

| phase                   |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:------------------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| clickhousecluster-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| clickhousecluster-1-2-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   clickhousecluster-1-1-1-1-1 |   clickhousecluster-1-2-1-1-1 |
|:----------------------------------------------------|------------------------------:|------------------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                        125.85 |                        307.76 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                        669.37 |                        749.49 |
| Shipping Priority (TPC-H Q3)                        |                        836.56 |                       1076.55 |
| Order Priority Checking Query (TPC-H Q4)            |                        414.28 |                        431.09 |
| Local Supplier Volume (TPC-H Q5)                    |                       1765.53 |                       1501.83 |
| Forecasting Revenue Change (TPC-H Q6)               |                         42.02 |                         37.35 |
| Volume Shipping Query (TPC-H Q7)                    |                       1940.70 |                       1850.15 |
| National Market Share (TPC-H Q8)                    |                       3225.95 |                       2895.72 |
| Product Type Profit Measure (TPC-H Q9)              |                       2668.09 |                       2503.39 |
| Returned Item Reporting Query (TPC-H Q10)           |                       1225.07 |                       1222.27 |
| Important Stock Identification (TPC-H Q11)          |                        125.14 |                        120.95 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                        579.87 |                        554.69 |
| Customer Distribution (TPC-H Q13)                   |                        552.30 |                        581.57 |
| Promotion Effect Query (TPC-H Q14)                  |                        122.49 |                        119.40 |
| Top Supplier Query (TPC-H Q15)                      |                        168.91 |                        161.66 |
| Parts/Supplier Relationship (TPC-H Q16)             |                        172.49 |                        161.42 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                        248.92 |                        284.02 |
| Large Volume Customer (TPC-H Q18)                   |                        696.36 |                        692.37 |
| Discounted Revenue (TPC-H Q19)                      |                        170.15 |                        170.72 |
| Potential Part Promotion (TPC-H Q20)                |                        449.38 |                        438.12 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                       1349.58 |                       1556.96 |
| Global Sales Opportunity Query (TPC-H Q22)          |                        104.93 |                        113.09 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |        21.25 |      0.30 |           0.49 |                  0.55 |

### Loading phase: component worker

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |        99.20 |      0.93 |           1.21 |                  2.14 |

### Loading phase: component data generator

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |         0.88 |      0.00 |           0.00 |                  0.00 |

### Benchmarking phase: SUT deployment

| DBMS                      | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|:-------------|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 | n/a          |      0.36 |           1.00 |                  1.08 |
| clickhousecluster-1-2-1-1 | n/a          |      0.10 |           0.39 |                  0.50 |

### Benchmarking phase: component worker

| DBMS                      | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|:-------------|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 | n/a          |      0.98 |           2.18 |                  3.18 |
| clickhousecluster-1-2-1-1 | n/a          |      1.32 |           2.09 |                  2.60 |

### Benchmarking phase: component benchmarker

| DBMS                      | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|:-------------|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| clickhousecluster-1-2-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |

### Missing Monitoring Metrics
* CPU Utilization [CPUs] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log)
* CPU Throttling Rate [s/s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection clickhousecluster-1-2-1-1 (bexhoma-metrics-clickhousecluster-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection clickhousecluster-1-2-1-1 (bexhoma-metrics-clickhousecluster-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection clickhousecluster-1-2-1-1 (bexhoma-metrics-clickhousecluster-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Memory Usage incl. Page Cache [MiB] for connection clickhousecluster-1-2-1-1 (bexhoma-metrics-clickhousecluster-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttled Time [s] for connection clickhousecluster-1-2-1-1 (bexhoma-metrics-clickhousecluster-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization Time [s] for connection clickhousecluster-1-2-1-1 (bexhoma-metrics-clickhousecluster-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU System Time [s] for connection clickhousecluster-1-2-1-1 (bexhoma-metrics-clickhousecluster-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU User Time [s] for connection clickhousecluster-1-2-1-1 (bexhoma-metrics-clickhousecluster-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Network Rx Total [MiB] for connection clickhousecluster-1-2-1-1 (bexhoma-metrics-clickhousecluster-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Network Tx Total [MiB] for connection clickhousecluster-1-2-1-1 (bexhoma-metrics-clickhousecluster-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-2-1-1 (bexhoma-metrics-clickhousecluster-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-2-1-1 (bexhoma-metrics-clickhousecluster-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS                      |   Queries [queries/s] |   Running Queries [count] |   Failed Queries [count] |   Rows Read [rows/s] |   Data Read, uncompressed [MiB/s] |
|:--------------------------|----------------------:|--------------------------:|-------------------------:|---------------------:|----------------------------------:|
| clickhousecluster-1-1-1-1 |                  1.22 |                      1.00 |                     0.00 |            108039.41 |                             13.71 |

#### Benchmarking phase: component worker

| DBMS                      |   Queries [queries/s] |   Running Queries [count] |   Failed Queries [count] |   Rows Read [rows/s] |   Data Read, uncompressed [MiB/s] |
|:--------------------------|----------------------:|--------------------------:|-------------------------:|---------------------:|----------------------------------:|
| clickhousecluster-1-1-1-1 |                  1.50 |                      3.00 |                     0.00 |           1253816.81 |                             42.21 |
| clickhousecluster-1-2-1-1 |                  0.52 |                      2.00 |                     0.00 |           1403891.74 |                             35.47 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Benchmarking phase: SUT deployment contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Benchmarking phase: component worker contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Benchmarking phase: component benchmarker contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST failed: Monitoring metrics missing
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


## Perform TPC-DS Benchmark

For performing the experiment we can run the [tpcds file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpcds.py).

```bash
bexhoma tpcds \
  -dbms ClickHouse \
  -sf 1 \
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
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ks no \
  run &>$LOG_DIR/docs_tpcds_clickhouse_1.log
```

The TPC-DS schema declares the columns without `NOT NULL` as `Nullable`, so empty fields of the flat files load as NULL.
Dates are `Date32`, since TPC-DS dates start in 1900.

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_clickhouse_1_summary.md" target="_blank" rel="noopener">docs_tpcds_clickhouse_1.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 515s 
* Code: 1792778126
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Data transfer volume per query is also measured.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.8.
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
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:958498
  * datadisk:676
  * volume_size:49G
  * volume_used:676M
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792778126

### SUT Container Restarts
* bexhoma-sut-clickhouse-1-1792778126-6d6998dd57-nrlmc: 0

### Workflow

#### Actual

* DBMS ClickHouse-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS ClickHouse-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| ClickHouse-1-1 |                1 |    1 |       46.00 |           8.00 |            1.00 |         22.00 |            5.00 |              8 |           0 |             | None           |             0 | False         |               78.26 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| clickhouse-1-1-1-1-1 | ClickHouse-1    | clickhouse-1-1-1 | clickhouse-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |         23 |            0.06 |            71798.80 |          15495.65 |          -1 | clickhouse-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| clickhouse-1-1-1 | clickhouse-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |         23 |            0.06 |            71798.80 |          15495.65 |          -1 |

#### Query Completion per Phase

| phase            |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:-----------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| clickhouse-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   clickhouse-1-1-1-1-1 |
|:--------------|-----------------------:|
| TPC-DS Q1     |                  74.48 |
| TPC-DS Q2     |                  56.78 |
| TPC-DS Q3     |                  22.87 |
| TPC-DS Q4     |                 329.29 |
| TPC-DS Q5     |                  51.54 |
| TPC-DS Q6     |                  37.52 |
| TPC-DS Q7     |                  40.22 |
| TPC-DS Q8     |                  57.63 |
| TPC-DS Q9     |                 114.73 |
| TPC-DS Q10    |                  67.51 |
| TPC-DS Q11    |                 280.74 |
| TPC-DS Q12    |                  22.93 |
| TPC-DS Q13    |                  55.76 |
| TPC-DS Q14a+b |                 955.72 |
| TPC-DS Q15    |                  39.48 |
| TPC-DS Q16    |                  42.35 |
| TPC-DS Q17    |                  47.85 |
| TPC-DS Q18    |                  53.00 |
| TPC-DS Q19    |                  26.72 |
| TPC-DS Q20    |                  20.39 |
| TPC-DS Q21    |                  25.74 |
| TPC-DS Q22    |                  57.89 |
| TPC-DS Q23a+b |                1848.74 |
| TPC-DS Q24a+b |                 137.97 |
| TPC-DS Q25    |                  39.36 |
| TPC-DS Q26    |                  32.27 |
| TPC-DS Q27    |                  34.06 |
| TPC-DS Q28    |                  95.01 |
| TPC-DS Q29    |                  46.39 |
| TPC-DS Q30    |                  69.97 |
| TPC-DS Q31    |                 120.54 |
| TPC-DS Q32    |                  29.45 |
| TPC-DS Q33    |                  37.81 |
| TPC-DS Q34    |                  28.67 |
| TPC-DS Q35    |                  62.43 |
| TPC-DS Q36    |                  15.85 |
| TPC-DS Q37    |                  14.14 |
| TPC-DS Q38    |                 114.68 |
| TPC-DS Q39a+b |                 160.85 |
| TPC-DS Q40    |                  20.21 |
| TPC-DS Q41    |                  15.89 |
| TPC-DS Q42    |                  14.74 |
| TPC-DS Q43    |                  12.66 |
| TPC-DS Q44    |                  23.30 |
| TPC-DS Q45    |                  30.12 |
| TPC-DS Q46    |                  38.16 |
| TPC-DS Q47    |                 164.73 |
| TPC-DS Q48    |                  48.38 |
| TPC-DS Q49    |                  47.35 |
| TPC-DS Q50    |                  27.09 |
| TPC-DS Q51    |                 109.74 |
| TPC-DS Q52    |                  16.58 |
| TPC-DS Q53    |                  25.76 |
| TPC-DS Q54    |                  40.39 |
| TPC-DS Q55    |                  14.80 |
| TPC-DS Q56    |                  53.48 |
| TPC-DS Q57    |                 140.38 |
| TPC-DS Q58    |                  48.34 |
| TPC-DS Q59    |                  86.38 |
| TPC-DS Q60    |                  38.39 |
| TPC-DS Q61    |                  18.26 |
| TPC-DS Q62    |                  19.67 |
| TPC-DS Q63    |                  36.21 |
| TPC-DS Q64    |                 279.73 |
| TPC-DS Q65    |                  61.89 |
| TPC-DS Q66    |                 193.68 |
| TPC-DS Q67    |                 338.64 |
| TPC-DS Q68    |                  29.77 |
| TPC-DS Q69    |                  61.53 |
| TPC-DS Q70    |                  47.76 |
| TPC-DS Q71    |                  29.53 |
| TPC-DS Q72    |                 202.96 |
| TPC-DS Q73    |                  22.16 |
| TPC-DS Q74    |                 201.31 |
| TPC-DS Q75    |                 107.36 |
| TPC-DS Q76    |                  31.70 |
| TPC-DS Q77    |                  78.72 |
| TPC-DS Q78    |                 107.88 |
| TPC-DS Q79    |                  45.18 |
| TPC-DS Q80    |                  45.30 |
| TPC-DS Q81    |                  44.23 |
| TPC-DS Q82    |                  25.98 |
| TPC-DS Q83    |                  49.51 |
| TPC-DS Q84    |                  12.69 |
| TPC-DS Q85    |                 105.95 |
| TPC-DS Q86    |                  22.33 |
| TPC-DS Q87    |                 101.41 |
| TPC-DS Q88    |                 106.55 |
| TPC-DS Q89    |                  23.92 |
| TPC-DS Q90    |                  19.88 |
| TPC-DS Q91    |                  27.63 |
| TPC-DS Q92    |                  20.37 |
| TPC-DS Q93    |                  34.97 |
| TPC-DS Q94    |                  34.86 |
| TPC-DS Q95    |                 130.81 |
| TPC-DS Q96    |                  15.91 |
| TPC-DS Q97    |                  52.02 |
| TPC-DS Q98    |                  23.96 |
| TPC-DS Q99    |                  26.72 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 |        25.96 |      0.29 |           0.65 |                  1.20 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 |         2.83 |      0.07 |           0.01 |                  0.01 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 |         6.02 |      0.00 |           0.44 |                  0.74 |

### Benchmarking phase: SUT deployment

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 | n/a          |      0.08 |           0.45 |                  1.12 |

### Benchmarking phase: component benchmarker

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 | n/a          |         0 |           0.35 |                  0.35 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log)
* CPU Throttling Rate [s/s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Queries [queries/s] |   Running Queries [count] |   Failed Queries [count] |   Rows Read [rows/s] |   Data Read, uncompressed [MiB/s] |
|:-------------------|----------------------:|--------------------------:|-------------------------:|---------------------:|----------------------------------:|
| clickhouse-1-1-1-1 |                  0.24 |                      2.00 |                     0.00 |             76775.64 |                              4.24 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Queries [queries/s] |   Running Queries [count] |   Failed Queries [count] |   Rows Read [rows/s] |   Data Read, uncompressed [MiB/s] |
|:-------------------|----------------------:|--------------------------:|-------------------------:|---------------------:|----------------------------------:|
| clickhouse-1-1-1-1 |                  0.42 |                      1.00 |                     0.00 |           1599556.97 |                             25.80 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component data generator contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Benchmarking phase: SUT deployment contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Benchmarking phase: component benchmarker contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST failed: Monitoring metrics missing
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
  -sf 1 \
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
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK -rnw $BEXHOMA_NODES_WORKER \
  -ks no \
  run &>$LOG_DIR/docs_tpcds_clickhouse_2.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_clickhouse_2_summary.md" target="_blank" rel="noopener">docs_tpcds_clickhouse_2.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 639s 
* Code: 1792778136
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Data transfer volume per query is also measured.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.8.
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
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:958498
  * datadisk:172
  * volume_size:49G
  * volume_used:172M
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:958498
    * datadisk:225
    * volume_size:49G
    * volume_used:226M
    * cpu_list:0-223
  * worker 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:472175
    * datadisk:354
    * volume_size:49G
    * volume_used:354M
    * cpu_list:0-127
  * worker 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:350158
    * datadisk:291
    * volume_size:49G
    * volume_used:291M
    * cpu_list:0-127
  * resources_total: 64.0 CPU, 256.0 GiB RAM requested in 4 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
    * worker: 3 x, 48.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792778136
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-clickhousecluster-1-1792778136-7f679756c-cgn9c: 0
* bexhoma-worker-clickhousecluster-nvme-tpcds-1-0: 0
* bexhoma-worker-clickhousecluster-nvme-tpcds-1-1: 0
* bexhoma-worker-clickhousecluster-nvme-tpcds-1-2: 0

### Workflow

#### Actual

* DBMS ClickHouseCluster-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS ClickHouseCluster-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                       |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| ClickHouseCluster-1-1 |                1 |    1 |       53.00 |          16.00 |            1.00 |         14.00 |            5.00 |              8 |           0 |             | None           |             0 | False         |               67.92 | False               |

### Benchmarking

#### Per Connection

| DBMS                        | configuration       | phase                   | job                       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                         |
|:----------------------------|:--------------------|:------------------------|:--------------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------------------|
| clickhousecluster-1-1-1-1-1 | ClickHouseCluster-1 | clickhousecluster-1-1-1 | clickhousecluster-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        112 |            0.43 |             8535.91 |           3182.14 |          -1 | clickhousecluster-1-1-1-1-1 |

#### Per Phase

|                         | phase                   |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------------|:------------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| clickhousecluster-1-1-1 | clickhousecluster-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        112 |            0.43 |             8535.91 |           3182.14 |          -1 |

#### Query Completion per Phase

| phase                   |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:------------------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| clickhousecluster-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   clickhousecluster-1-1-1-1-1 |
|:--------------|------------------------------:|
| TPC-DS Q1     |                        203.56 |
| TPC-DS Q2     |                       2233.75 |
| TPC-DS Q3     |                        378.04 |
| TPC-DS Q4     |                      16257.28 |
| TPC-DS Q5     |                        277.68 |
| TPC-DS Q6     |                        645.06 |
| TPC-DS Q7     |                        754.81 |
| TPC-DS Q8     |                        226.60 |
| TPC-DS Q9     |                        317.15 |
| TPC-DS Q10    |                       1731.29 |
| TPC-DS Q11    |                       4922.21 |
| TPC-DS Q12    |                        119.16 |
| TPC-DS Q13    |                        698.35 |
| TPC-DS Q14a+b |                       8152.53 |
| TPC-DS Q15    |                        178.21 |
| TPC-DS Q16    |                        235.85 |
| TPC-DS Q17    |                        800.89 |
| TPC-DS Q18    |                       1054.75 |
| TPC-DS Q19    |                        775.05 |
| TPC-DS Q20    |                        146.58 |
| TPC-DS Q21    |                        123.49 |
| TPC-DS Q22    |                        180.00 |
| TPC-DS Q23a+b |                       2538.06 |
| TPC-DS Q24a+b |                       1157.43 |
| TPC-DS Q25    |                        791.71 |
| TPC-DS Q26    |                        782.09 |
| TPC-DS Q27    |                        650.71 |
| TPC-DS Q28    |                        219.04 |
| TPC-DS Q29    |                        738.53 |
| TPC-DS Q30    |                        293.03 |
| TPC-DS Q31    |                       1035.12 |
| TPC-DS Q32    |                        163.49 |
| TPC-DS Q33    |                        215.84 |
| TPC-DS Q34    |                        120.47 |
| TPC-DS Q35    |                       1156.79 |
| TPC-DS Q36    |                         94.13 |
| TPC-DS Q37    |                        891.66 |
| TPC-DS Q38    |                        377.54 |
| TPC-DS Q39a+b |                       1007.35 |
| TPC-DS Q40    |                        180.36 |
| TPC-DS Q41    |                         60.94 |
| TPC-DS Q42    |                        312.53 |
| TPC-DS Q43    |                        282.64 |
| TPC-DS Q44    |                         64.33 |
| TPC-DS Q45    |                        188.30 |
| TPC-DS Q46    |                        152.83 |
| TPC-DS Q47    |                       2686.37 |
| TPC-DS Q48    |                        560.90 |
| TPC-DS Q49    |                        225.97 |
| TPC-DS Q50    |                        285.70 |
| TPC-DS Q51    |                        320.33 |
| TPC-DS Q52    |                        362.30 |
| TPC-DS Q53    |                        464.61 |
| TPC-DS Q54    |                        241.39 |
| TPC-DS Q55    |                        334.75 |
| TPC-DS Q56    |                        200.84 |
| TPC-DS Q57    |                       1538.44 |
| TPC-DS Q58    |                        272.91 |
| TPC-DS Q59    |                        318.00 |
| TPC-DS Q60    |                        200.77 |
| TPC-DS Q61    |                        310.68 |
| TPC-DS Q62    |                        128.23 |
| TPC-DS Q63    |                        505.89 |
| TPC-DS Q64    |                       6879.08 |
| TPC-DS Q65    |                        410.44 |
| TPC-DS Q66    |                        532.38 |
| TPC-DS Q67    |                        553.10 |
| TPC-DS Q68    |                        173.22 |
| TPC-DS Q69    |                       1531.05 |
| TPC-DS Q70    |                        247.91 |
| TPC-DS Q71    |                        242.08 |
| TPC-DS Q72    |                       5149.27 |
| TPC-DS Q73    |                        126.50 |
| TPC-DS Q74    |                       3982.77 |
| TPC-DS Q75    |                        721.56 |
| TPC-DS Q76    |                        139.54 |
| TPC-DS Q77    |                        289.41 |
| TPC-DS Q78    |                        701.44 |
| TPC-DS Q79    |                        182.54 |
| TPC-DS Q80    |                        439.49 |
| TPC-DS Q81    |                        243.04 |
| TPC-DS Q82    |                        912.08 |
| TPC-DS Q83    |                        339.73 |
| TPC-DS Q84    |                        343.09 |
| TPC-DS Q85    |                       1657.09 |
| TPC-DS Q86    |                        108.40 |
| TPC-DS Q87    |                        375.06 |
| TPC-DS Q88    |                        787.69 |
| TPC-DS Q89    |                        498.33 |
| TPC-DS Q90    |                        146.02 |
| TPC-DS Q91    |                        528.01 |
| TPC-DS Q92    |                        143.65 |
| TPC-DS Q93    |                        161.73 |
| TPC-DS Q94    |                        230.09 |
| TPC-DS Q95    |                       1005.21 |
| TPC-DS Q96    |                         88.72 |
| TPC-DS Q97    |                        276.92 |
| TPC-DS Q98    |                        143.64 |
| TPC-DS Q99    |                        127.26 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |        24.03 |      0.18 |           0.41 |                  0.47 |

### Loading phase: component worker

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |       116.13 |      0.81 |           1.72 |                  2.11 |

### Loading phase: component data generator

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |         1.36 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |         0.65 |      0.00 |           0.00 |                  0.00 |

### Benchmarking phase: SUT deployment

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |       101.11 |      1.38 |           1.10 |                  1.20 |

### Benchmarking phase: component worker

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |       534.47 |      6.21 |           5.41 |                  6.40 |

### Benchmarking phase: component benchmarker

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |        23.25 |      0.14 |           0.34 |                  0.34 |

### Missing Monitoring Metrics
* CPU Utilization [CPUs] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log)
* CPU Throttled Time [s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS                      |   Queries [queries/s] |   Running Queries [count] |   Failed Queries [count] |   Rows Read [rows/s] |   Data Read, uncompressed [MiB/s] |
|:--------------------------|----------------------:|--------------------------:|-------------------------:|---------------------:|----------------------------------:|
| clickhousecluster-1-1-1-1 |                  1.68 |                      1.00 |                     0.00 |            228768.26 |                             12.64 |

#### Benchmarking phase: component worker

| DBMS                      |   Queries [queries/s] |   Running Queries [count] |   Failed Queries [count] |   Rows Read [rows/s] |   Data Read, uncompressed [MiB/s] |
|:--------------------------|----------------------:|--------------------------:|-------------------------:|---------------------:|----------------------------------:|
| clickhousecluster-1-1-1-1 |                 10.31 |                      2.00 |                     0.00 |          23900254.22 |                            480.73 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component data generator contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST failed: Monitoring metrics missing
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


## ClickHouse Example Explained

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

`ClickHouseCluster` is the same, plus `'attachWorker': ''`: the shards are in the configuration of every pod (`remote_servers`), there is nothing to register.
The JDBC jar is the variant with all dependencies; the smaller `-all` jar lacks slf4j-api, and the driver class does not load without it.
DBMS-Benchmarker reads `UInt64` results (e.g. of `count()`), which the driver returns as `java.math.BigInteger`, since v0.15.4.

### Settings for Standard SQL

The templates set these settings for user `default`, since TPC-H and TPC-DS expect standard SQL results:

| Setting | Value | Without it |
|---|---|---|
| `join_use_nulls` | 1 | an outer join fills unmatched columns with 0 or `''` instead of NULL (wrong counts in TPC-H Q13) |
| `union_default_mode` | `DISTINCT` | a plain `UNION` is a syntax error |
| `cast_keep_nullable` | 1 | `CAST` of a NULL fails |
| `allow_lossy_numeric_supertype` | 1 | `CASE`/`COALESCE` over Decimal and Float has no common type |
| `distributed_product_mode` | `global` (cluster only) | a join of two Distributed tables is refused (or, with `local`, wrong for tables that are not sharded alike) |

### Schema SQL Files

* [TPC-H ClickHouse](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch/ClickHouse), [TPC-H ClickHouseCluster](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch/ClickHouseCluster)
* [TPC-DS ClickHouse](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpcds/ClickHouse), [TPC-DS ClickHouseCluster](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpcds/ClickHouseCluster)

MergeTree needs a sorting key at creation; it is the primary key of the benchmark, which also is ClickHouse's sparse primary index.
There are no secondary indexes, constraints or statistics, so `-xii`, `-xic` and `-xis` have no scripts.

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
