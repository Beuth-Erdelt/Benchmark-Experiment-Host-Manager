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

The experiment is run with the [tpch file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpch.py).

Example:
```bash
bexhoma tpch \
  -dbms MariaDB \
  -sf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -nbp 1 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
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
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_mariadb_summary.md" target="_blank" rel="noopener">docs_tpch_mariadb.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 512s 
* Code: 1795659706
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
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* mariadb-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:676083
  * datadisk:1962
  * volume_size:1.8T
  * volume_used:661G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795659706

### Ingestion
* MariaDB-1: 50 of 50 units ok

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1795659706-749668698-5rlkb: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |    1 |       79.00 |           2.00 |           27.00 |         16.00 |           23.00 |              8 |         0 |             |                |             0 | False         |               45.57 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         93 |            1.00 |             3813.97 |            851.61 |           0 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         93 |            1.00 |             3813.97 |            851.61 |           0 |

#### Query Completion per Phase

| phase         |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:--------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| mariadb-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   mariadb-1-1-1-1-1 |
|:----------------------------------------------------|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |             5994.13 |
| Minimum Cost Supplier Query (TPC-H Q2)              |             1113.77 |
| Shipping Priority (TPC-H Q3)                        |             1193.99 |
| Order Priority Checking Query (TPC-H Q4)            |              301.20 |
| Local Supplier Volume (TPC-H Q5)                    |              734.51 |
| Forecasting Revenue Change (TPC-H Q6)               |              729.63 |
| Volume Shipping Query (TPC-H Q7)                    |              863.81 |
| National Market Share (TPC-H Q8)                    |             1415.23 |
| Product Type Profit Measure (TPC-H Q9)              |             1397.45 |
| Returned Item Reporting Query (TPC-H Q10)           |              922.07 |
| Important Stock Identification (TPC-H Q11)          |              274.88 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             2694.02 |
| Customer Distribution (TPC-H Q13)                   |             2369.43 |
| Promotion Effect Query (TPC-H Q14)                  |             9605.40 |
| Top Supplier Query (TPC-H Q15)                      |             1635.49 |
| Parts/Supplier Relationship (TPC-H Q16)             |              154.29 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               59.09 |
| Large Volume Customer (TPC-H Q18)                   |             2934.44 |
| Discounted Revenue (TPC-H Q19)                      |              111.62 |
| Potential Part Promotion (TPC-H Q20)                |              386.61 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            46823.45 |
| Global Sales Opportunity Query (TPC-H Q22)          |               92.97 |

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

```bash
bexhoma tpch \
  -dbms MariaDB \
  -sf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -nbp 1 \
  -xii -xic -xis \
  -xdt \
  -m \
  -ms $BEXHOMA_MS \
  -t 1200 \
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
* Duration: 555s 
* Code: 1795660248
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
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* mariadb-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:624490
  * datadisk:1970
  * volume_size:1.8T
  * volume_used:610G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795660248

### Ingestion
* MariaDB-1: 50 of 50 units ok

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1795660248-5878c4fcc5-lk8rh: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |    1 |       70.00 |           2.00 |           22.00 |         16.00 |           21.00 |              8 |         0 |             |                |             0 | False         |               51.43 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |        100 |            0.97 |             3945.36 |            792.00 |           0 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |        100 |            0.97 |             3945.36 |            792.00 |           0 |

#### Query Completion per Phase

| phase         |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:--------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| mariadb-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   mariadb-1-1-1-1-1 |
|:----------------------------------------------------|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |             6325.58 |
| Minimum Cost Supplier Query (TPC-H Q2)              |              447.33 |
| Shipping Priority (TPC-H Q3)                        |             2014.06 |
| Order Priority Checking Query (TPC-H Q4)            |              337.06 |
| Local Supplier Volume (TPC-H Q5)                    |              756.80 |
| Forecasting Revenue Change (TPC-H Q6)               |             1518.19 |
| Volume Shipping Query (TPC-H Q7)                    |             1014.77 |
| National Market Share (TPC-H Q8)                    |             1665.75 |
| Product Type Profit Measure (TPC-H Q9)              |             2105.75 |
| Returned Item Reporting Query (TPC-H Q10)           |              771.61 |
| Important Stock Identification (TPC-H Q11)          |              108.04 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             2559.35 |
| Customer Distribution (TPC-H Q13)                   |             2314.49 |
| Promotion Effect Query (TPC-H Q14)                  |             9052.93 |
| Top Supplier Query (TPC-H Q15)                      |             1755.82 |
| Parts/Supplier Relationship (TPC-H Q16)             |              228.37 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               57.47 |
| Large Volume Customer (TPC-H Q18)                   |             2466.51 |
| Discounted Revenue (TPC-H Q19)                      |               80.25 |
| Potential Part Promotion (TPC-H Q20)                |              167.88 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            52938.78 |
| Global Sales Opportunity Query (TPC-H Q22)          |               93.62 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |        92.26 |      2.65 |           1.69 |                  1.70 |

### Loading phase: component data generator

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |        61.01 |      0.97 |           2.05 |                  2.06 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |        17.37 |      0.09 |           0.32 |                  0.32 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
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
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: SUT pods not replaced
* TEST passed: Host information complete
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Monitoring returned data
* TEST skipped: Monitoring metrics missing (data pre-existing; job pods ran shorter than scrape interval; series exists only while non-zero)
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

This is a throughput test: one round with 1 stream and one with 2 parallel streams (`-ne 1,2`), repeated (`-nc 2`), so the second repetition runs on the loaded volume:

```bash
bexhoma tpch \
  -dbms MariaDB \
  -sf 1 \
  -nc 2 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 8 \
  -nbp 1 \
  -xii -xic -xis \
  -xdt \
  -m \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -lr 128Gi \
  -rr 128Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
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
* Duration: 1223s 
* Code: 1795660850
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
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* mariadb-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:622524
  * datadisk:1962
  * volume_size:49G
  * volume_used:2.0G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795660850
* mariadb-1-1-2-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:622525
  * datadisk:1962
  * volume_size:49G
  * volume_used:2.0G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795660850
* mariadb-1-1-2-1-2 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:622525
  * datadisk:1962
  * volume_size:49G
  * volume_used:2.0G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795660850
* mariadb-1-2-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:622526
  * datadisk:1963
  * volume_size:49G
  * volume_used:2.0G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795660850
* mariadb-1-2-2-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:622527
  * datadisk:1963
  * volume_size:49G
  * volume_used:2.0G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795660850
* mariadb-1-2-2-1-2 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:622527
  * datadisk:1963
  * volume_size:49G
  * volume_used:2.0G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795660850

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MariaDB-1-2

### Data Parameters of Reused Volumes
* MariaDB-1: DDL values of the volume: engine=InnoDB, histograms=off, row_format=default
* MariaDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### Ingestion
* MariaDB-1: 50 of 50 units ok

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1795660850-77d4df7856-x6gn9: 0
* bexhoma-sut-mariadb-1-1795660850-6d97b4bb7-stxks: 0

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

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |    1 |       76.00 |           2.00 |           23.00 |         19.00 |           24.00 |              8 |         0 |             |                |             0 | False         |               47.37 | False               |
| MariaDB-1-2 |                2 |    1 |       76.00 |           2.00 |           23.00 |         19.00 |           24.00 |              8 |         0 |             |                |             0 | False         |               47.37 | True                |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         97 |            0.95 |             3989.60 |            816.49 |           0 |
| mariadb-1-1-2-1-1 | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |       1 | 1.00 |               22 |                  22 |        105 |            1.07 |             3526.18 |            754.29 |           0 |
| mariadb-1-1-2-1-2 | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |       2 | 1.00 |               22 |                  22 |        103 |            1.00 |             3839.15 |            768.93 |           0 |
| mariadb-1-2-1-1-1 | mariadb-1-2-1 | mariadb-1-2-1-1 |                2 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         91 |            0.88 |             4364.27 |            870.33 |           0 |
| mariadb-1-2-2-1-1 | mariadb-1-2-2 | mariadb-1-2-2-1 |                2 |        2 |               1 |       1 | 1.00 |               22 |                  22 |        105 |            1.11 |             3485.46 |            754.29 |           0 |
| mariadb-1-2-2-1-2 | mariadb-1-2-2 | mariadb-1-2-2-1 |                2 |        2 |               1 |       2 | 1.00 |               22 |                  22 |        102 |            1.01 |             3743.62 |            776.47 |           0 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         97 |            0.95 |             3989.60 |            816.49 |           0 |
| mariadb-1-1-2 | mariadb-1-1-2 |                1 |        2 |               1 |           2 | 1.00 |               44 |                  44 |        105 |            1.04 |             3679.34 |           1508.57 |           0 |
| mariadb-1-2-1 | mariadb-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         91 |            0.88 |             4364.27 |            870.33 |           0 |
| mariadb-1-2-2 | mariadb-1-2-2 |                2 |        2 |               1 |           2 | 1.00 |               44 |                  44 |        105 |            1.06 |             3612.24 |           1508.57 |           0 |

#### Query Completion per Phase

| phase         |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:--------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| mariadb-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| mariadb-1-1-2 |      2 | 2/2                                 | 2/2                                      | 2/2                            | 2/2                                        | 2/2                                | 2/2                                     | 2/2                                | 2/2                                | 2/2                                      | 2/2                                         | 2/2                                          | 2/2                                             | 2/2                                 | 2/2                                  | 2/2                              | 2/2                                       | 2/2                                        | 2/2                                 | 2/2                              | 2/2                                    | 2/2                                                   | 2/2                                          | yes        |
| mariadb-1-2-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| mariadb-1-2-2 |      2 | 2/2                                 | 2/2                                      | 2/2                            | 2/2                                        | 2/2                                | 2/2                                     | 2/2                                | 2/2                                | 2/2                                      | 2/2                                         | 2/2                                          | 2/2                                             | 2/2                                 | 2/2                                  | 2/2                              | 2/2                                       | 2/2                                        | 2/2                                 | 2/2                              | 2/2                                    | 2/2                                                   | 2/2                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   mariadb-1-1-1-1-1 |   mariadb-1-1-2-1-1 |   mariadb-1-1-2-1-2 |   mariadb-1-2-1-1-1 |   mariadb-1-2-2-1-1 |   mariadb-1-2-2-1-2 |
|:----------------------------------------------------|--------------------:|--------------------:|--------------------:|--------------------:|--------------------:|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |             5927.35 |             6436.70 |             6604.48 |             6560.02 |             5925.32 |             6486.22 |
| Minimum Cost Supplier Query (TPC-H Q2)              |              413.41 |              482.19 |              389.15 |              427.85 |              329.74 |              404.33 |
| Shipping Priority (TPC-H Q3)                        |             1586.76 |             1732.53 |             1663.12 |             1438.42 |             1239.18 |             2054.08 |
| Order Priority Checking Query (TPC-H Q4)            |              425.79 |              424.10 |              412.67 |              288.13 |              754.09 |              339.19 |
| Local Supplier Volume (TPC-H Q5)                    |              784.61 |             1786.37 |             1762.71 |             1359.88 |             1116.96 |              779.82 |
| Forecasting Revenue Change (TPC-H Q6)               |              756.76 |              803.21 |              812.30 |              769.06 |              785.43 |              703.35 |
| Volume Shipping Query (TPC-H Q7)                    |              842.34 |             1006.04 |             1057.94 |              912.02 |              909.20 |             1048.20 |
| National Market Share (TPC-H Q8)                    |             1384.68 |             2132.31 |             2097.74 |             1439.95 |             1847.38 |             1701.46 |
| Product Type Profit Measure (TPC-H Q9)              |             1877.22 |             1794.40 |             1794.51 |             1469.76 |             1565.77 |             1948.51 |
| Returned Item Reporting Query (TPC-H Q10)           |              687.72 |             1209.55 |              978.99 |              728.37 |             1614.79 |              888.37 |
| Important Stock Identification (TPC-H Q11)          |              106.93 |               84.08 |              108.14 |              105.49 |              259.62 |              101.68 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             2511.46 |             3577.12 |             3076.81 |             2554.46 |             2673.90 |             2662.00 |
| Customer Distribution (TPC-H Q13)                   |             2775.00 |             3694.20 |             3607.06 |             2377.39 |             3686.92 |             3612.88 |
| Promotion Effect Query (TPC-H Q14)                  |             9724.18 |            11670.98 |            11486.47 |             9272.35 |            10162.33 |             9975.50 |
| Top Supplier Query (TPC-H Q15)                      |             1698.52 |             1731.39 |             1682.38 |             1657.20 |             1649.01 |             1687.92 |
| Parts/Supplier Relationship (TPC-H Q16)             |              324.61 |              284.50 |              149.88 |              155.70 |              165.66 |              276.22 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               69.78 |               51.46 |               46.00 |               45.03 |               45.91 |               48.58 |
| Large Volume Customer (TPC-H Q18)                   |             2785.59 |             2366.35 |             2528.29 |             2353.48 |             3077.54 |             3146.51 |
| Discounted Revenue (TPC-H Q19)                      |               87.00 |               96.16 |               73.85 |               71.92 |              159.28 |               93.86 |
| Potential Part Promotion (TPC-H Q20)                |              199.46 |              315.57 |              166.38 |              159.17 |              397.38 |              394.31 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            52759.56 |            52101.96 |            53857.79 |            46221.37 |            58383.39 |            56879.84 |
| Global Sales Opportunity Query (TPC-H Q22)          |               99.08 |               84.19 |               92.21 |               98.47 |               80.71 |               93.40 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |        92.96 |      1.95 |           1.68 |                  1.69 |
| mariadb-1-1-2-1 |        92.96 |      1.95 |           1.68 |                  1.69 |

### Loading phase: component data generator

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |
| mariadb-1-1-2-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 | n/a          |         0 |           0.00 |                  0.10 |
| mariadb-1-1-2-1 | n/a          |         0 |           0.00 |                  0.10 |

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |        60.58 |      0.97 |           2.03 |                  2.04 |
| mariadb-1-1-2-1 |       182.69 |      2.00 |           2.05 |                  2.06 |
| mariadb-1-2-1-1 |        63.67 |      1.00 |           1.88 |                  1.88 |
| mariadb-1-2-2-1 |       115.66 |      2.00 |           1.88 |                  1.89 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |        18.80 |      0.45 |           0.34 |                  0.34 |
| mariadb-1-1-2-1 |        34.45 |      0.43 |           0.31 |                  0.32 |
| mariadb-1-2-1-1 |        16.36 |      0.44 |           0.31 |                  0.32 |
| mariadb-1-2-2-1 |        34.23 |      0.19 |           0.34 |                  0.34 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loading.log, expected: series exists only while non-zero)
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
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: SUT pods not replaced
* TEST passed: Host information complete
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Monitoring returned data
* TEST skipped: Monitoring metrics missing (data pre-existing; job pods ran shorter than scrape interval; series exists only while non-zero)
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
  -ma \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -lr 128Gi \
  -rr 128Gi \
  -rss 150Gi \
  -rst ramdisk \
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
* Duration: 1705s 
* Code: 1795662167
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MariaDB'].
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
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* mariadb-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:622531
  * datadisk:17657
  * volume_size:128G
  * volume_used:18G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795662167

### Ingestion
* MariaDB-1: 50 of 50 units ok

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1795662167-576f84bc9c-cbhmd: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |   10 |      355.00 |           2.00 |           15.00 |        127.00 |          200.00 |              8 |         0 |             |                |             0 | False         |              101.41 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       1 | 10.00 |               22 |                  22 |       1018 |           11.48 |             3183.17 |            778.00 |           0 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |                  22 |       1018 |           11.48 |             3183.17 |            778.00 |           0 |

#### Query Completion per Phase

| phase         |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:--------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| mariadb-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   mariadb-1-1-1-1-1 |
|:----------------------------------------------------|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |            63284.13 |
| Minimum Cost Supplier Query (TPC-H Q2)              |             4551.47 |
| Shipping Priority (TPC-H Q3)                        |            18792.19 |
| Order Priority Checking Query (TPC-H Q4)            |             4557.77 |
| Local Supplier Volume (TPC-H Q5)                    |            11579.40 |
| Forecasting Revenue Change (TPC-H Q6)               |            10983.86 |
| Volume Shipping Query (TPC-H Q7)                    |            12613.39 |
| National Market Share (TPC-H Q8)                    |            20038.41 |
| Product Type Profit Measure (TPC-H Q9)              |            24881.82 |
| Returned Item Reporting Query (TPC-H Q10)           |             8544.50 |
| Important Stock Identification (TPC-H Q11)          |             1619.46 |
| Shipping Modes and Order Priority (TPC-H Q12)       |            27700.21 |
| Customer Distribution (TPC-H Q13)                   |            32800.86 |
| Promotion Effect Query (TPC-H Q14)                  |           153886.73 |
| Top Supplier Query (TPC-H Q15)                      |            19499.14 |
| Parts/Supplier Relationship (TPC-H Q16)             |             2359.58 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |              601.50 |
| Large Volume Customer (TPC-H Q18)                   |            32435.19 |
| Discounted Revenue (TPC-H Q19)                      |             1416.77 |
| Potential Part Promotion (TPC-H Q20)                |             3143.39 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |           549636.32 |
| Global Sales Opportunity Query (TPC-H Q22)          |             1786.61 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |      1063.19 |      7.62 |          25.73 |                 25.73 |

### Loading phase: component data generator

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |        30.58 |      0.30 |           0.01 |                  1.31 |

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |      1011.54 |      1.29 |          25.81 |                 25.81 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |        20.76 |      0.07 |           0.32 |                  0.32 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loading.log, expected: series exists only while non-zero)

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


## Refresh Stream

`-xrs N` runs the TPC-H refresh functions RF1 (insert new orders) and RF2 (delete old orders) as an additional job next to the query streams, see [TPC-H](Example-TPC-H.md#refresh-stream).
For MariaDB, the loader image applies RF1 with `LOAD DATA LOCAL INFILE` and RF2 with a temporary table and a `DELETE` joined to it.
Here, 3 query streams run in parallel with a refresh stream of 3 RF1+RF2 pairs.

```bash
bexhoma tpch \
  -dbms MariaDB \
  -sf 1 \
  -ne 3 \
  -xrs 3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -ms $BEXHOMA_MS \
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
* Duration: 554s 
* Code: 1795693313
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
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* mariadb-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:638093
  * datadisk:1962
  * volume_size:1.8T
  * volume_used:624G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795693313
* mariadb-1-1-1-1-2 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:638093
  * datadisk:1962
  * volume_size:1.8T
  * volume_used:624G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795693313
* mariadb-1-1-1-1-3 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:638093
  * datadisk:1962
  * volume_size:1.8T
  * volume_used:624G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795693313

### Ingestion
* MariaDB-1: 50 of 50 units ok

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1795693313-557d99595d-dxhnx: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |    1 |       65.00 |           2.00 |           17.00 |         15.00 |           20.00 |              8 |         0 |             |                |             0 | False         |               55.38 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |        109 |            1.10 |             3282.71 |            726.61 |           0 |
| mariadb-1-1-1-1-2 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       2 | 1.00 |               22 |                  22 |        106 |            1.08 |             3341.63 |            747.17 |           0 |
| mariadb-1-1-1-1-3 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       3 | 1.00 |               22 |                  22 |        110 |            1.08 |             3347.59 |            720.00 |           0 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           3 | 1.00 |               66 |                  66 |        110 |            1.08 |             3323.85 |           2160.00 |           0 |

#### Query Completion per Phase

| phase         |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:--------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| mariadb-1-1-1 |      3 | 3/3                                 | 3/3                                      | 3/3                            | 3/3                                        | 3/3                                | 3/3                                     | 3/3                                | 3/3                                | 3/3                                      | 3/3                                         | 3/3                                          | 3/3                                             | 3/3                                 | 3/3                                  | 3/3                              | 3/3                                       | 3/3                                        | 3/3                                 | 3/3                              | 3/3                                    | 3/3                                                   | 3/3                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### tpch_refresh

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count | benchmark_begin     | benchmark_end       |   benchmark_duration |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|:--------------------|:--------------------|---------------------:|
| mariadb-1-1-1-2-1 | mariadb-1-1-1 | mariadb-1-1-1-2 |                1 |        1 |               2 |           1 | 2026-11-26 12:48:51 | 2026-11-26 12:48:55 |                    4 |

### Latency of Timer Execution [ms]
| Queries                                             |   mariadb-1-1-1-1-1 |   mariadb-1-1-1-1-2 |   mariadb-1-1-1-1-3 |
|:----------------------------------------------------|--------------------:|--------------------:|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |             6976.21 |             6999.00 |             7373.88 |
| Minimum Cost Supplier Query (TPC-H Q2)              |              542.71 |              601.78 |              488.85 |
| Shipping Priority (TPC-H Q3)                        |             2273.77 |             2370.45 |             2333.11 |
| Order Priority Checking Query (TPC-H Q4)            |              418.51 |              415.21 |              327.99 |
| Local Supplier Volume (TPC-H Q5)                    |             1393.66 |             1339.80 |             1393.94 |
| Forecasting Revenue Change (TPC-H Q6)               |             1414.63 |              960.86 |             1385.51 |
| Volume Shipping Query (TPC-H Q7)                    |             1184.25 |             1338.05 |             1282.05 |
| National Market Share (TPC-H Q8)                    |             2261.48 |             2193.17 |             2425.84 |
| Product Type Profit Measure (TPC-H Q9)              |             1768.98 |             1743.70 |             2023.09 |
| Returned Item Reporting Query (TPC-H Q10)           |              711.08 |              734.83 |              761.15 |
| Important Stock Identification (TPC-H Q11)          |               86.60 |              115.47 |              234.59 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             3037.83 |             3044.53 |             3158.50 |
| Customer Distribution (TPC-H Q13)                   |             3754.39 |             3572.22 |             3741.11 |
| Promotion Effect Query (TPC-H Q14)                  |            12258.12 |            12307.37 |            12795.21 |
| Top Supplier Query (TPC-H Q15)                      |             2469.73 |             2110.76 |             1697.10 |
| Parts/Supplier Relationship (TPC-H Q16)             |              144.89 |              299.43 |              146.38 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               52.40 |               44.20 |               44.36 |
| Large Volume Customer (TPC-H Q18)                   |             5250.55 |             3161.72 |             5438.48 |
| Discounted Revenue (TPC-H Q19)                      |              130.51 |               67.84 |               73.74 |
| Potential Part Promotion (TPC-H Q20)                |              422.98 |              151.39 |              173.13 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            59044.79 |            58804.50 |            59611.80 |
| Global Sales Opportunity Query (TPC-H Q22)          |               81.88 |              311.09 |              119.91 |

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
| `row_format` | YCSB, TPC-H, TPC-DS, SSB | `default`, `DYNAMIC`, `COMPRESSED` | `default` | InnoDB row format of the tables (TPC-H: only with `engine=InnoDB`) (default: innodb_default_row_format, DYNAMIC): COMPRESSED stores pages zlib-compressed: less I/O, more CPU |
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

The experiment is run with the [tpcds file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpcds.py).

### Power Test

```bash
bexhoma tpcds \
  -dbms MariaDB \
  -sf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -nbp 1 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
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
* Duration: 862s 
* Code: 1795663925
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
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
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* mariadb-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:627012
  * datadisk:4466
  * volume_size:1.8T
  * volume_used:613G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795663925

### Ingestion
* MariaDB-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1795663925-5c5f98b88c-cz2j9: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |    1 |      167.00 |           2.00 |            0.00 |         70.00 |           85.00 |              8 |         0 |             | None           |             0 | False         |               21.56 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               99 |                  99 |        318 |            0.66 |             5573.67 |           1120.75 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        318 |            0.66 |             5573.67 |           1120.75 |          -1 |

#### Query Completion per Phase

| phase         |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:--------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mariadb-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   mariadb-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |               15.31 |
| TPC-DS Q2     |             4217.99 |
| TPC-DS Q3     |               16.69 |
| TPC-DS Q4     |             8648.62 |
| TPC-DS Q5     |             6689.09 |
| TPC-DS Q6     |              759.85 |
| TPC-DS Q7     |             2620.08 |
| TPC-DS Q8     |              775.71 |
| TPC-DS Q9     |             3400.15 |
| TPC-DS Q10    |               73.77 |
| TPC-DS Q11    |             6740.60 |
| TPC-DS Q12    |              189.48 |
| TPC-DS Q13    |             1643.16 |
| TPC-DS Q14a+b |            44059.91 |
| TPC-DS Q15    |              130.55 |
| TPC-DS Q16    |             7382.76 |
| TPC-DS Q17    |              593.03 |
| TPC-DS Q18    |             1429.04 |
| TPC-DS Q19    |              168.56 |
| TPC-DS Q20    |              341.19 |
| TPC-DS Q21    |              854.00 |
| TPC-DS Q22    |            13745.41 |
| TPC-DS Q23a+b |            43839.49 |
| TPC-DS Q24a+b |               23.05 |
| TPC-DS Q25    |              116.48 |
| TPC-DS Q26    |              605.35 |
| TPC-DS Q27    |             2452.32 |
| TPC-DS Q28    |             2594.18 |
| TPC-DS Q29    |               65.07 |
| TPC-DS Q30    |               75.80 |
| TPC-DS Q31    |             1058.50 |
| TPC-DS Q32    |                5.87 |
| TPC-DS Q33    |              129.12 |
| TPC-DS Q34    |             2268.53 |
| TPC-DS Q35    |              837.20 |
| TPC-DS Q36    |             2186.00 |
| TPC-DS Q37    |             3289.76 |
| TPC-DS Q38    |             5333.36 |
| TPC-DS Q39a+b |             1252.60 |
| TPC-DS Q40    |              150.65 |
| TPC-DS Q41    |              450.10 |
| TPC-DS Q42    |              166.59 |
| TPC-DS Q43    |              777.94 |
| TPC-DS Q44    |                1.73 |
| TPC-DS Q45    |               92.63 |
| TPC-DS Q46    |             3119.65 |
| TPC-DS Q47    |            12453.77 |
| TPC-DS Q48    |              849.21 |
| TPC-DS Q49    |               96.15 |
| TPC-DS Q50    |               21.43 |
| TPC-DS Q51    |             6319.71 |
| TPC-DS Q52    |              170.47 |
| TPC-DS Q53    |              106.70 |
| TPC-DS Q54    |              904.79 |
| TPC-DS Q55    |              164.97 |
| TPC-DS Q56    |              112.36 |
| TPC-DS Q57    |             5036.64 |
| TPC-DS Q58    |             4688.03 |
| TPC-DS Q59    |             7091.12 |
| TPC-DS Q60    |              542.80 |
| TPC-DS Q61    |              271.98 |
| TPC-DS Q62    |             1323.43 |
| TPC-DS Q63    |              119.70 |
| TPC-DS Q64    |              443.75 |
| TPC-DS Q65    |             5519.51 |
| TPC-DS Q66    |              931.28 |
| TPC-DS Q67    |             6322.63 |
| TPC-DS Q68    |             2399.98 |
| TPC-DS Q69    |                1.87 |
| TPC-DS Q70    |             6289.80 |
| TPC-DS Q71    |              395.80 |
| TPC-DS Q72    |              615.05 |
| TPC-DS Q73    |             2113.40 |
| TPC-DS Q74    |             4831.56 |
| TPC-DS Q75    |             4416.22 |
| TPC-DS Q76    |              345.37 |
| TPC-DS Q77    |             4904.66 |
| TPC-DS Q78    |             4135.71 |
| TPC-DS Q79    |             2399.52 |
| TPC-DS Q80    |              382.24 |
| TPC-DS Q81    |              151.32 |
| TPC-DS Q82    |             2932.95 |
| TPC-DS Q83    |              705.39 |
| TPC-DS Q84    |               43.26 |
| TPC-DS Q85    |               97.09 |
| TPC-DS Q86    |              623.12 |
| TPC-DS Q87    |             5648.93 |
| TPC-DS Q88    |             7385.40 |
| TPC-DS Q89    |             1492.66 |
| TPC-DS Q90    |              318.75 |
| TPC-DS Q91    |               13.00 |
| TPC-DS Q92    |                6.38 |
| TPC-DS Q93    |               33.38 |
| TPC-DS Q94    |              354.79 |
| TPC-DS Q95    |              566.92 |
| TPC-DS Q96    |              489.73 |
| TPC-DS Q97    |             4965.17 |
| TPC-DS Q98    |              694.91 |
| TPC-DS Q99    |             2507.00 |

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

```bash
bexhoma tpcds \
  -dbms MariaDB \
  -sf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -nbp 1 \
  -xii -xic -xis \
  -xdt \
  -m \
  -ms $BEXHOMA_MS \
  -t 1200 \
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
* Duration: 855s 
* Code: 1795664861
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
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
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* mariadb-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:627014
  * datadisk:4474
  * volume_size:1.8T
  * volume_used:613G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795664861

### Ingestion
* MariaDB-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1795664861-6b5684bf8d-nmg5t: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |    1 |      168.00 |           2.00 |            1.00 |         68.00 |           87.00 |              8 |         0 |             | None           |             0 | False         |               21.43 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               99 |                  99 |        328 |            0.72 |             5109.24 |           1086.59 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        328 |            0.72 |             5109.24 |           1086.59 |          -1 |

#### Query Completion per Phase

| phase         |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:--------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mariadb-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   mariadb-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |               12.19 |
| TPC-DS Q2     |             3417.31 |
| TPC-DS Q3     |                9.80 |
| TPC-DS Q4     |             8941.68 |
| TPC-DS Q5     |             6522.19 |
| TPC-DS Q6     |              723.74 |
| TPC-DS Q7     |             2432.99 |
| TPC-DS Q8     |              267.87 |
| TPC-DS Q9     |             3513.09 |
| TPC-DS Q10    |               27.84 |
| TPC-DS Q11    |             6261.11 |
| TPC-DS Q12    |              188.40 |
| TPC-DS Q13    |              735.16 |
| TPC-DS Q14a+b |            41446.45 |
| TPC-DS Q15    |              126.08 |
| TPC-DS Q16    |             8492.95 |
| TPC-DS Q17    |              560.41 |
| TPC-DS Q18    |             1407.97 |
| TPC-DS Q19    |              178.61 |
| TPC-DS Q20    |              336.33 |
| TPC-DS Q21    |             1153.38 |
| TPC-DS Q22    |            12703.13 |
| TPC-DS Q23a+b |            44113.54 |
| TPC-DS Q24a+b |               24.84 |
| TPC-DS Q25    |              108.04 |
| TPC-DS Q26    |              592.84 |
| TPC-DS Q27    |             2435.00 |
| TPC-DS Q28    |             3071.95 |
| TPC-DS Q29    |               39.55 |
| TPC-DS Q30    |               28.22 |
| TPC-DS Q31    |              986.32 |
| TPC-DS Q32    |                4.44 |
| TPC-DS Q33    |              105.85 |
| TPC-DS Q34    |             2653.38 |
| TPC-DS Q35    |              957.79 |
| TPC-DS Q36    |             2249.64 |
| TPC-DS Q37    |             3417.64 |
| TPC-DS Q38    |             5525.85 |
| TPC-DS Q39a+b |              886.72 |
| TPC-DS Q40    |              130.88 |
| TPC-DS Q41    |              391.01 |
| TPC-DS Q42    |              160.21 |
| TPC-DS Q43    |              761.86 |
| TPC-DS Q44    |             1672.27 |
| TPC-DS Q45    |               97.58 |
| TPC-DS Q46    |             2728.61 |
| TPC-DS Q47    |            15716.48 |
| TPC-DS Q48    |              859.77 |
| TPC-DS Q49    |               90.74 |
| TPC-DS Q50    |               20.74 |
| TPC-DS Q51    |             7520.86 |
| TPC-DS Q52    |              192.22 |
| TPC-DS Q53    |              101.02 |
| TPC-DS Q54    |              917.89 |
| TPC-DS Q55    |              175.13 |
| TPC-DS Q56    |              245.90 |
| TPC-DS Q57    |             4401.55 |
| TPC-DS Q58    |             4693.09 |
| TPC-DS Q59    |             7122.01 |
| TPC-DS Q60    |              304.42 |
| TPC-DS Q61    |              250.29 |
| TPC-DS Q62    |             1289.95 |
| TPC-DS Q63    |              119.33 |
| TPC-DS Q64    |             1730.22 |
| TPC-DS Q65    |             4540.27 |
| TPC-DS Q66    |             1113.13 |
| TPC-DS Q67    |             5154.27 |
| TPC-DS Q68    |             2645.15 |
| TPC-DS Q69    |               27.67 |
| TPC-DS Q70    |             6468.30 |
| TPC-DS Q71    |              341.05 |
| TPC-DS Q72    |              591.54 |
| TPC-DS Q73    |             2386.28 |
| TPC-DS Q74    |             4395.53 |
| TPC-DS Q75    |             4536.32 |
| TPC-DS Q76    |              638.95 |
| TPC-DS Q77    |             5362.09 |
| TPC-DS Q78    |             4929.15 |
| TPC-DS Q79    |             2549.44 |
| TPC-DS Q80    |              382.21 |
| TPC-DS Q81    |              152.57 |
| TPC-DS Q82    |             3103.85 |
| TPC-DS Q83    |              861.87 |
| TPC-DS Q84    |               46.01 |
| TPC-DS Q85    |               96.99 |
| TPC-DS Q86    |              639.97 |
| TPC-DS Q87    |             5305.61 |
| TPC-DS Q88    |            19228.69 |
| TPC-DS Q89    |             1277.48 |
| TPC-DS Q90    |              102.21 |
| TPC-DS Q91    |               15.43 |
| TPC-DS Q92    |                4.42 |
| TPC-DS Q93    |               36.34 |
| TPC-DS Q94    |              375.83 |
| TPC-DS Q95    |             1666.53 |
| TPC-DS Q96    |             1962.52 |
| TPC-DS Q97    |             4949.80 |
| TPC-DS Q98    |              826.57 |
| TPC-DS Q99    |             2517.11 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |       245.63 |      3.19 |           3.67 |                  3.82 |

### Loading phase: component data generator

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |         4.54 |      0.07 |           0.01 |                  0.40 |

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |       303.69 |      1.00 |           4.35 |                  4.36 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |        19.52 |      0.05 |           0.29 |                  0.30 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loading.log, expected: series exists only while non-zero)

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

### Throughput Test on Persistent Storage

```bash
bexhoma tpcds \
  -dbms MariaDB \
  -sf 1 \
  -nc 2 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 8 \
  -nbp 1 \
  -xii -xic -xis \
  -xdt \
  -m \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -lr 128Gi \
  -rr 128Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
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
* Duration: 2416s 
* Code: 1795665821
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
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
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* mariadb-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:659363
  * datadisk:4474
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
    * code:1795665821
* mariadb-1-1-2-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:660934
  * datadisk:4474
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
    * code:1795665821
* mariadb-1-1-2-1-2 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:660934
  * datadisk:4474
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
    * code:1795665821
* mariadb-1-2-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:655442
  * datadisk:4475
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
    * code:1795665821
* mariadb-1-2-2-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:661743
  * datadisk:4475
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
    * code:1795665821
* mariadb-1-2-2-1-2 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:661743
  * datadisk:4475
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
    * code:1795665821

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MariaDB-1-2

### Data Parameters of Reused Volumes
* MariaDB-1: DDL values of the volume: histograms=off, row_format=default
* MariaDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### Ingestion
* MariaDB-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1795665821-6ffb7b8bf6-vcts7: 0
* bexhoma-sut-mariadb-1-1795665821-747854cf4f-tjsr7: 0

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

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |    1 |      199.00 |           3.00 |            1.00 |         83.00 |           99.00 |              8 |         0 |             | None           |             0 | False         |               18.09 | False               |
| MariaDB-1-2 |                2 |    1 |      199.00 |           3.00 |            1.00 |         83.00 |           99.00 |              8 |         0 |             | None           |             0 | False         |               18.09 | True                |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               99 |                  99 |        313 |            0.67 |             5433.47 |           1138.66 |          -1 |
| mariadb-1-1-2-1-1 | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |       1 | 1.00 |               99 |                  99 |        360 |            0.75 |             4882.83 |            990.00 |          -1 |
| mariadb-1-1-2-1-2 | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |       2 | 1.00 |               99 |                  99 |        359 |            0.76 |             4787.43 |            992.76 |          -1 |
| mariadb-1-2-1-1-1 | mariadb-1-2-1 | mariadb-1-2-1-1 |                2 |        1 |               1 |       1 | 1.00 |               99 |                  99 |        316 |            0.71 |             5134.18 |           1127.85 |          -1 |
| mariadb-1-2-2-1-1 | mariadb-1-2-2 | mariadb-1-2-2-1 |                2 |        2 |               1 |       1 | 1.00 |               99 |                  99 |        355 |            0.75 |             4886.83 |           1003.94 |          -1 |
| mariadb-1-2-2-1-2 | mariadb-1-2-2 | mariadb-1-2-2-1 |                2 |        2 |               1 |       2 | 1.00 |               99 |                  99 |        357 |            0.74 |             4920.38 |            998.32 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        313 |            0.67 |             5433.47 |           1138.66 |          -1 |
| mariadb-1-1-2 | mariadb-1-1-2 |                1 |        2 |               1 |           2 | 1.00 |              198 |                 198 |        360 |            0.76 |             4834.89 |           1980.00 |          -1 |
| mariadb-1-2-1 | mariadb-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        316 |            0.71 |             5134.18 |           1127.85 |          -1 |
| mariadb-1-2-2 | mariadb-1-2-2 |                2 |        2 |               1 |           2 | 1.00 |              198 |                 198 |        357 |            0.75 |             4903.58 |           1996.64 |          -1 |

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
| TPC-DS Q1     |               14.08 |               13.71 |               19.26 |               32.66 |               13.51 |               16.93 |
| TPC-DS Q2     |             4275.47 |             3546.06 |             3421.15 |             8470.97 |             3551.90 |             3468.31 |
| TPC-DS Q3     |                7.08 |                6.80 |                7.12 |              127.27 |                9.02 |                6.65 |
| TPC-DS Q4     |            10564.03 |            10695.56 |             9754.36 |             9094.98 |             9705.47 |             9599.33 |
| TPC-DS Q5     |             6728.93 |             8674.65 |             9436.74 |             7396.29 |             8768.31 |             8876.69 |
| TPC-DS Q6     |              738.24 |              911.67 |              987.60 |              735.01 |              835.76 |              863.26 |
| TPC-DS Q7     |             2580.26 |             3644.36 |             3641.18 |             2675.24 |             3622.21 |             3707.53 |
| TPC-DS Q8     |              241.24 |              306.50 |              308.63 |              237.31 |              254.05 |              300.12 |
| TPC-DS Q9     |             3743.97 |             3879.15 |             3880.65 |             3298.68 |             3287.63 |             3324.41 |
| TPC-DS Q10    |               41.40 |               50.09 |               49.88 |               75.28 |               41.97 |               31.41 |
| TPC-DS Q11    |             6375.61 |             7044.11 |             6943.23 |             6137.07 |             7764.49 |             7755.25 |
| TPC-DS Q12    |              188.67 |              212.43 |              215.22 |              187.68 |              243.67 |              249.50 |
| TPC-DS Q13    |              708.61 |             1218.89 |              917.86 |              760.56 |              951.38 |              943.42 |
| TPC-DS Q14a+b |            37609.07 |            40772.02 |            41146.17 |            37493.70 |            45439.57 |            43867.15 |
| TPC-DS Q15    |              111.90 |              137.24 |              135.98 |              114.91 |              388.67 |              125.46 |
| TPC-DS Q16    |             7536.59 |             8851.75 |             8656.16 |             7043.00 |             8752.46 |             9203.39 |
| TPC-DS Q17    |              504.68 |              679.52 |              678.89 |              526.15 |              491.66 |              567.12 |
| TPC-DS Q18    |             1883.87 |             2552.16 |             2540.04 |             1420.81 |             2471.35 |             1442.73 |
| TPC-DS Q19    |              174.45 |              156.85 |              169.49 |              167.67 |              372.40 |              197.42 |
| TPC-DS Q20    |              344.99 |              480.02 |              482.33 |              340.94 |              366.99 |              346.26 |
| TPC-DS Q21    |             3719.30 |             4229.88 |             4229.29 |             4111.81 |             3590.73 |             4834.34 |
| TPC-DS Q22    |             8753.02 |            12455.45 |            12359.97 |             8349.77 |            10933.99 |            11435.49 |
| TPC-DS Q23a+b |            46539.96 |            55032.00 |            54195.02 |            44242.95 |            51645.85 |            52585.75 |
| TPC-DS Q24a+b |               22.82 |               21.26 |               23.28 |               22.39 |               22.64 |               20.34 |
| TPC-DS Q25    |              115.47 |              100.73 |              109.33 |              116.97 |              142.56 |              120.75 |
| TPC-DS Q26    |              644.90 |             1144.91 |              626.50 |              632.45 |              814.91 |              810.84 |
| TPC-DS Q27    |             2730.12 |             3336.41 |             3535.12 |             2457.91 |             3572.19 |             3490.13 |
| TPC-DS Q28    |             2613.22 |             3174.24 |             2942.90 |             2542.87 |             2739.41 |             2732.14 |
| TPC-DS Q29    |               64.99 |               63.90 |               73.38 |               72.06 |               58.27 |               70.57 |
| TPC-DS Q30    |               29.24 |               24.15 |               27.04 |               31.55 |               35.64 |               35.25 |
| TPC-DS Q31    |             1307.47 |              964.97 |             1024.54 |             1012.44 |             1113.87 |             1109.69 |
| TPC-DS Q32    |                4.81 |                4.62 |                4.59 |                4.75 |                4.88 |                4.95 |
| TPC-DS Q33    |              120.26 |              106.35 |              119.02 |              119.83 |               98.14 |              111.25 |
| TPC-DS Q34    |             2384.68 |             3779.30 |             3751.48 |             3130.67 |             2969.98 |             2983.51 |
| TPC-DS Q35    |              835.09 |              853.67 |              851.79 |              872.38 |              820.37 |              827.41 |
| TPC-DS Q36    |             2554.54 |             2606.26 |             2621.14 |             2267.46 |             2813.86 |             2775.78 |
| TPC-DS Q37    |             2985.37 |             3591.15 |             3606.50 |             4270.84 |             3394.80 |             3575.11 |
| TPC-DS Q38    |             7061.56 |             6884.00 |             6828.29 |             6187.75 |             7354.12 |             6422.68 |
| TPC-DS Q39a+b |              967.33 |             1625.30 |             2184.24 |              972.16 |              970.41 |             1275.92 |
| TPC-DS Q40    |              137.33 |              164.31 |              161.27 |              134.27 |              127.91 |              131.83 |
| TPC-DS Q41    |              359.08 |              362.91 |              394.00 |              361.82 |              359.89 |              366.86 |
| TPC-DS Q42    |              167.39 |              165.24 |              170.18 |              169.14 |              161.08 |              169.52 |
| TPC-DS Q43    |              792.39 |              887.45 |              937.90 |              800.99 |              771.55 |              790.61 |
| TPC-DS Q44    |                1.81 |                1.34 |                1.34 |                1.48 |                1.62 |                1.62 |
| TPC-DS Q45    |               94.99 |               93.75 |               96.12 |              121.57 |               95.60 |               95.40 |
| TPC-DS Q46    |             3903.16 |             3979.82 |             3518.72 |             2726.31 |             3431.75 |             3239.96 |
| TPC-DS Q47    |            12009.19 |            15759.48 |            16690.15 |            14107.89 |            14805.87 |            14723.69 |
| TPC-DS Q48    |             1077.31 |             1575.30 |             1129.18 |              855.55 |              829.84 |              861.51 |
| TPC-DS Q49    |               84.34 |               81.56 |              267.82 |               96.02 |               87.29 |               91.43 |
| TPC-DS Q50    |               20.81 |               19.62 |               53.89 |               20.36 |               19.27 |               23.49 |
| TPC-DS Q51    |             6704.16 |             7720.11 |             7779.43 |             6248.71 |             8170.85 |             7135.29 |
| TPC-DS Q52    |              161.63 |              142.80 |              160.29 |              158.64 |              165.20 |              547.88 |
| TPC-DS Q53    |              105.25 |              108.75 |              105.64 |              106.43 |              106.52 |              161.45 |
| TPC-DS Q54    |             1094.47 |              847.55 |              871.72 |              921.75 |              861.09 |              901.81 |
| TPC-DS Q55    |              502.13 |              517.09 |              161.90 |              157.08 |              187.59 |              182.91 |
| TPC-DS Q56    |              106.23 |              115.11 |              109.81 |              112.01 |               99.34 |              107.38 |
| TPC-DS Q57    |             6238.87 |             5873.71 |             6516.56 |             5061.04 |             6402.16 |             6491.09 |
| TPC-DS Q58    |             4889.01 |             6470.34 |             5542.29 |             5040.17 |             5965.59 |             5953.03 |
| TPC-DS Q59    |             7773.47 |             9565.32 |             8512.53 |             6855.92 |             8792.16 |             9095.91 |
| TPC-DS Q60    |              535.33 |              501.01 |              684.04 |              521.94 |              493.79 |              491.54 |
| TPC-DS Q61    |              261.41 |              267.02 |              266.65 |              270.51 |              353.52 |              256.13 |
| TPC-DS Q62    |             1291.97 |             2321.46 |             1552.85 |             1332.88 |             1566.55 |             1409.81 |
| TPC-DS Q63    |              126.25 |              410.25 |              122.47 |              121.92 |              156.03 |              124.96 |
| TPC-DS Q64    |              525.79 |              506.70 |              465.51 |              503.25 |              491.20 |             1277.59 |
| TPC-DS Q65    |             4596.42 |             6462.47 |             5886.88 |             4402.34 |             5922.86 |             5746.69 |
| TPC-DS Q66    |             1205.58 |              919.06 |              829.31 |             1320.95 |              858.37 |             1655.80 |
| TPC-DS Q67    |             5146.15 |             6103.36 |             7226.85 |             5526.19 |             6074.55 |             6464.65 |
| TPC-DS Q68    |             2384.87 |             3902.11 |             2677.94 |             2718.47 |             2995.87 |             3016.55 |
| TPC-DS Q69    |              287.64 |              299.39 |              310.09 |              326.90 |              254.85 |              268.17 |
| TPC-DS Q70    |             6449.48 |             7869.16 |             8712.44 |             7211.49 |             8164.43 |             8748.46 |
| TPC-DS Q71    |              331.38 |              383.11 |              348.26 |              408.20 |              406.89 |              407.75 |
| TPC-DS Q72    |              623.96 |              584.18 |              601.28 |              617.32 |              740.44 |              742.76 |
| TPC-DS Q73    |             2441.44 |             2121.50 |             3518.89 |             2124.01 |             2966.74 |             2989.59 |
| TPC-DS Q74    |             4552.44 |             5108.69 |             5411.59 |             4480.74 |             5375.62 |             5375.31 |
| TPC-DS Q75    |             4613.53 |             4511.65 |             4931.42 |             5337.39 |             4593.23 |             4593.62 |
| TPC-DS Q76    |              335.78 |              369.25 |              343.50 |              367.04 |              436.85 |              437.94 |
| TPC-DS Q77    |             5534.00 |             5914.75 |             6378.82 |             5804.53 |             6820.47 |             6820.43 |
| TPC-DS Q78    |             4629.71 |             5242.44 |             5402.91 |             5161.64 |             4780.13 |             4736.96 |
| TPC-DS Q79    |             2424.74 |             3423.38 |             3102.10 |             2793.72 |             3241.27 |             3258.87 |
| TPC-DS Q80    |              385.30 |              381.84 |              629.31 |              415.75 |              578.86 |              578.98 |
| TPC-DS Q81    |              153.66 |              151.11 |              155.91 |              155.66 |              174.26 |              171.81 |
| TPC-DS Q82    |             3465.91 |             2994.81 |             3161.99 |             2983.94 |             4106.12 |             4599.71 |
| TPC-DS Q83    |              703.07 |             2008.57 |              700.31 |              801.45 |              756.72 |              738.67 |
| TPC-DS Q84    |               41.89 |               40.61 |               39.46 |               74.22 |               43.57 |               32.89 |
| TPC-DS Q85    |               96.85 |              104.17 |               96.99 |              187.22 |               97.09 |              107.23 |
| TPC-DS Q86    |              622.61 |              839.97 |             1977.62 |              737.41 |              721.18 |              777.51 |
| TPC-DS Q87    |             6104.86 |             6517.10 |             6956.44 |             6022.51 |             6915.50 |             7608.49 |
| TPC-DS Q88    |             7008.17 |             7155.43 |             7134.99 |             7945.30 |             7446.22 |             7985.41 |
| TPC-DS Q89    |             1088.75 |             1491.54 |             1057.06 |             1010.89 |             1107.02 |             2093.29 |
| TPC-DS Q90    |              100.50 |               77.82 |               81.21 |              108.77 |               86.11 |               80.37 |
| TPC-DS Q91    |               12.02 |               10.07 |               12.86 |               16.68 |               14.46 |                9.59 |
| TPC-DS Q92    |                6.58 |                6.53 |                6.12 |                6.55 |               19.78 |                6.53 |
| TPC-DS Q93    |               34.44 |               25.54 |               74.23 |               33.03 |               78.61 |               27.59 |
| TPC-DS Q94    |              366.89 |              369.40 |              635.44 |              364.41 |              394.89 |              362.70 |
| TPC-DS Q95    |              582.66 |              618.51 |              587.29 |              580.89 |              603.49 |              620.25 |
| TPC-DS Q96    |              499.86 |              488.72 |              477.93 |              488.19 |              656.95 |              494.45 |
| TPC-DS Q97    |             4052.31 |             5136.06 |             5257.23 |             4641.42 |             6209.73 |             6085.27 |
| TPC-DS Q98    |              705.18 |              783.53 |              866.84 |              677.43 |              699.17 |              687.47 |
| TPC-DS Q99    |             2926.51 |             3320.68 |             3499.82 |             2563.32 |             2915.84 |             3765.53 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |       269.21 |      4.96 |           4.20 |                  4.21 |
| mariadb-1-1-2-1 |       269.21 |      4.96 |           4.20 |                  4.21 |

### Loading phase: component data generator

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |
| mariadb-1-1-2-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |         3.91 |      0.06 |           0.01 |                  0.76 |
| mariadb-1-1-2-1 |         3.91 |      0.06 |           0.01 |                  0.76 |

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |       274.91 |      1.00 |           4.45 |                  4.46 |
| mariadb-1-1-2-1 |       638.15 |      2.00 |           4.48 |                  4.49 |
| mariadb-1-2-1-1 |       286.19 |      0.99 |           2.60 |                  2.60 |
| mariadb-1-2-2-1 |       614.68 |      2.00 |           2.90 |                  2.91 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |        19.61 |      0.04 |           0.31 |                  0.32 |
| mariadb-1-1-2-1 |        42.81 |      1.13 |           0.34 |                  0.34 |
| mariadb-1-2-1-1 |        19.22 |      0.04 |           0.33 |                  0.34 |
| mariadb-1-2-2-1 |        42.02 |      1.37 |           0.30 |                  0.31 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-2-1 (bexhoma-metrics-mariadb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-2-1 (bexhoma-metrics-mariadb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-2-1-1 (bexhoma-metrics-mariadb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-2-1-1 (bexhoma-metrics-mariadb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-2-2-1 (bexhoma-metrics-mariadb-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-2-2-1 (bexhoma-metrics-mariadb-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)

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


## Benchbase's TPC-C

See [Example: Benchbase](Example-Benchbase.md) for the parameters.

### Simple

```bash
bexhoma benchbase \
  -dbms MariaDB \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 8 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 160 \
  -ms $BEXHOMA_MS \
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
* Duration: 684s 
* Code: 1795668440
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
  * Experiment is limited to DBMS ['MariaDB'].
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mariadb', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mariadb-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:672268
  * datadisk:1895
  * volume_size:1.8T
  * volume_used:657G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795668440

### Ingestion
* MariaDB-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1795668440-6b5956d78-4kpnp: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: benchbase (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: benchbase (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |   16 |       77.00 |           1.00 |            0.00 |         73.00 |            3.00 |              1 |         1 |             | None           |             0 | False         |              748.05 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       1 |       160 |     8192 |          -1 | 300.00 |        0 |                        7793.90 |                     7664.14 |         0.00 |                                                      66438.00 |                                              18899.00 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 |       160 |     8192 |          -1 | 300.00 |        0 |                        7793.90 |                     7664.14 |         0.00 |                                                      66438.00 |                                              18899.00 |

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
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
* TEST passed: Every pod ran for the configured time
* TEST passed: Results of all benchmarker pods
* TEST passed: Benchmarker pods without errors

Test successful!
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
  -xnbf 8 \
  -nc 2 \
  -ne 1 \
  -nbp 1 \
  -nbt 160 \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
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
* Duration: 866s 
* Code: 1795669136
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 1 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
  * Experiment is limited to DBMS ['MariaDB'].
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mariadb', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mariadb-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:626546
  * datadisk:1880
  * volume_size:49G
  * volume_used:1.9G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795669136
* mariadb-1-2-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:628180
  * datadisk:2333
  * volume_size:49G
  * volume_used:2.3G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795669136

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MariaDB-1-2

### Data Parameters of Reused Volumes
* MariaDB-1: loading values of the volume: script=Schema, indexing=Checks

### Ingestion
* MariaDB-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1795669136-5c7fdb788-6q4bv: 0
* bexhoma-sut-mariadb-1-1795669136-674574565-jspdz: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: benchbase (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: benchbase (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |   16 |      108.00 |           2.00 |            0.00 |        101.00 |            5.00 |              1 |         1 |             | None           |             0 | False         |              533.33 | False               |
| MariaDB-1-2 |                2 |   16 |      108.00 |           2.00 |            0.00 |        101.00 |            5.00 |              1 |         1 |             | None           |             0 | False         |              533.33 | True                |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       1 |       160 |     8192 |          -1 |  60.00 |        0 |                        6238.82 |                     6142.57 |         0.00 |                                                      90582.00 |                                              24699.00 |
| mariadb-1-2-1-1-1 | mariadb-1-2-1 | mariadb-1-2-1-1 |                2 |        1 |               1 |       1 |       160 |     8192 |          -1 |  60.00 |        0 |                        5653.57 |                     5564.55 |         0.00 |                                                      99876.00 |                                              27233.00 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 |       160 |     8192 |          -1 |  60.00 |        0 |                        6238.82 |                     6142.57 |         0.00 |                                                      90582.00 |                                              24699.00 |
| mariadb-1-2-1 | mariadb-1-2-1 |                2 |        1 |               1 |           1 |       160 |     8192 |          -1 |  60.00 |        0 |                        5653.57 |                     5564.55 |         0.00 |                                                      99876.00 |                                              27233.00 |

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
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
* TEST passed: Every pod ran for the configured time
* TEST passed: Results of all benchmarker pods
* TEST passed: Benchmarker pods without errors

Test successful!
```

</details>

### Monitoring

```bash
bexhoma benchbase \
  -dbms MariaDB \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 8 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 160 \
  -m \
  -ms $BEXHOMA_MS \
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
* Duration: 688s 
* Code: 1795670010
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MariaDB'].
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mariadb', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mariadb-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:624433
  * datadisk:1896
  * volume_size:1.8T
  * volume_used:610G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795670010

### Ingestion
* MariaDB-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1795670010-66945cddb7-tfmh2: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: benchbase (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: benchbase (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |   16 |       85.00 |           2.00 |            0.00 |         81.00 |            2.00 |              1 |         1 |             | None           |             0 | False         |              677.65 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       1 |       160 |     8192 |          -1 | 300.00 |        0 |                        8083.46 |                     7961.13 |         0.00 |                                                      57082.00 |                                              15231.00 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 |       160 |     8192 |          -1 | 300.00 |        0 |                        8083.46 |                     7961.13 |         0.00 |                                                      57082.00 |                                              15231.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |       138.25 |      3.00 |           2.51 |                  2.52 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |       748.08 |     15.36 |           0.27 |                  0.27 |

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |      8931.83 |     42.97 |           4.39 |                  4.40 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |      2728.36 |     10.71 |           1.02 |                  1.02 |

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
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: SUT pods not replaced
* TEST passed: Host information complete
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Monitoring returned data
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
* TEST passed: Every pod ran for the configured time
* TEST passed: Results of all benchmarker pods
* TEST passed: Benchmarker pods without errors

Test successful!
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
  -xnbf 8 \
  -nc 2 \
  -ne 1,2 \
  -nbp 1,2 \
  -nbt 160 \
  -m \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
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
* Duration: 1831s 
* Code: 1795670726
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 2 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MariaDB'].
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mariadb', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mariadb-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:622539
  * datadisk:2556
  * volume_size:49G
  * volume_used:2.5G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1795670726
* mariadb-1-1-2-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:623779
  * datadisk:3004
  * volume_size:49G
  * volume_used:3.0G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1795670726
* mariadb-1-1-3-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:627793
  * datadisk:3246
  * volume_size:49G
  * volume_used:3.2G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1795670726
* mariadb-1-1-4-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:632434
  * datadisk:3622
  * volume_size:49G
  * volume_used:3.6G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1795670726
* mariadb-1-2-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:634751
  * datadisk:4027
  * volume_size:49G
  * volume_used:4.0G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1795670726
* mariadb-1-2-2-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:635309
  * datadisk:4367
  * volume_size:49G
  * volume_used:4.3G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1795670726
* mariadb-1-2-3-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:636273
  * datadisk:4683
  * volume_size:49G
  * volume_used:4.6G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1795670726
* mariadb-1-2-4-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:638248
  * datadisk:4975
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
    * code:1795670726

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MariaDB-1

### Data Parameters of Reused Volumes
* MariaDB-1: loading values of the volume: script=Schema, indexing=Checks

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1795670726-5fbdf5f845-hkr8g: 0
* bexhoma-sut-mariadb-1-1795670726-87cc9674-l4g8z: 0

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

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |   16 |      108.00 |           2.00 |            0.00 |        101.00 |            5.00 |              0 |         1 |             | None           |             0 | False         |              533.33 | True                |
| MariaDB-1-2 |                2 |   16 |      108.00 |           2.00 |            0.00 |        101.00 |            5.00 |              0 |         1 |             | None           |             0 | False         |              533.33 | True                |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       1 |       160 |     8192 |          -1 | 120.00 |        0 |                        5737.37 |                     5645.31 |         0.00 |                                                      94767.00 |                                              27101.00 |
| mariadb-1-1-2-1-1 | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |       1 |       160 |     8192 |          -1 | 120.00 |        0 |                        1548.57 |                     1527.37 |         0.00 |                                                     459234.00 |                                             102953.00 |
| mariadb-1-1-2-1-2 | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |       2 |       160 |     8192 |          -1 | 120.00 |        0 |                        1524.20 |                     1503.52 |         0.00 |                                                     459680.00 |                                             104872.00 |
| mariadb-1-1-3-1-1 | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        3 |               1 |       1 |        80 |     4096 |          -1 | 120.00 |        0 |                        2283.01 |                     2249.59 |         0.00 |                                                      92808.00 |                                              34804.00 |
| mariadb-1-1-3-1-2 | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        3 |               1 |       2 |        80 |     4096 |          -1 | 120.00 |        0 |                        2282.15 |                     2249.57 |         0.00 |                                                      92560.00 |                                              34962.00 |
| mariadb-1-1-4-1-1 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       1 |        80 |     4096 |          -1 | 120.00 |        0 |                        1120.12 |                     1104.53 |         0.00 |                                                     198876.00 |                                              71281.00 |
| mariadb-1-1-4-1-2 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       2 |        80 |     4096 |          -1 | 120.00 |        0 |                        1112.70 |                     1097.66 |         0.00 |                                                     199930.00 |                                              71858.00 |
| mariadb-1-1-4-1-3 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       3 |        80 |     4096 |          -1 | 120.00 |        0 |                        1111.29 |                     1095.78 |         0.00 |                                                     199695.00 |                                              71940.00 |
| mariadb-1-1-4-1-4 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       4 |        80 |     4096 |          -1 | 120.00 |        0 |                        1118.60 |                     1102.92 |         0.00 |                                                     199336.00 |                                              71394.00 |
| mariadb-1-2-1-1-1 | mariadb-1-2-1 | mariadb-1-2-1-1 |                2 |        1 |               1 |       1 |       160 |     8192 |          -1 | 120.00 |        0 |                        4358.23 |                     4287.80 |         0.00 |                                                     106951.00 |                                              35760.00 |
| mariadb-1-2-2-1-1 | mariadb-1-2-2 | mariadb-1-2-2-1 |                2 |        2 |               1 |       1 |       160 |     8192 |          -1 | 120.00 |        0 |                        2032.81 |                     2004.40 |         0.00 |                                                     208037.00 |                                              78566.00 |
| mariadb-1-2-2-1-2 | mariadb-1-2-2 | mariadb-1-2-2-1 |                2 |        2 |               1 |       2 |       160 |     8192 |          -1 | 120.00 |        0 |                        2006.29 |                     1978.19 |         0.00 |                                                     209780.00 |                                              79656.00 |
| mariadb-1-2-3-1-1 | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        3 |               1 |       1 |        80 |     4096 |          -1 | 120.00 |        0 |                        1883.75 |                     1856.62 |         0.00 |                                                     111719.00 |                                              42200.00 |
| mariadb-1-2-3-1-2 | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        3 |               1 |       2 |        80 |     4096 |          -1 | 120.00 |        0 |                        1893.09 |                     1866.13 |         0.00 |                                                     111294.00 |                                              42171.00 |
| mariadb-1-2-4-1-1 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       1 |        80 |     4096 |          -1 | 120.00 |        0 |                         979.02 |                      966.17 |         0.00 |                                                     224888.00 |                                              80962.00 |
| mariadb-1-2-4-1-2 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       2 |        80 |     4096 |          -1 | 120.00 |        0 |                         973.14 |                      959.57 |         0.00 |                                                     225762.00 |                                              82132.00 |
| mariadb-1-2-4-1-3 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       3 |        80 |     4096 |          -1 | 120.00 |        0 |                         966.44 |                      953.71 |         0.00 |                                                     225727.00 |                                              82698.00 |
| mariadb-1-2-4-1-4 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       4 |        80 |     4096 |          -1 | 120.00 |        0 |                         971.52 |                      958.47 |         0.00 |                                                     225834.00 |                                              82142.00 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 |       160 |     8192 |          -1 | 120.00 |        0 |                        5737.37 |                     5645.31 |         0.00 |                                                      94767.00 |                                              27101.00 |
| mariadb-1-1-2 | mariadb-1-1-2 |                1 |        2 |               1 |           2 |       320 |    16384 |          -1 | 120.00 |        0 |                        3072.77 |                     3030.90 |         0.00 |                                                     459680.00 |                                             103912.50 |
| mariadb-1-1-3 | mariadb-1-1-3 |                1 |        3 |               1 |           2 |       160 |     8192 |          -1 | 120.00 |        0 |                        4565.15 |                     4499.16 |         0.00 |                                                      92808.00 |                                              34883.00 |
| mariadb-1-1-4 | mariadb-1-1-4 |                1 |        4 |               1 |           4 |       320 |    16384 |          -1 | 120.00 |        0 |                        4462.71 |                     4400.89 |         0.00 |                                                     199930.00 |                                              71618.25 |
| mariadb-1-2-1 | mariadb-1-2-1 |                2 |        1 |               1 |           1 |       160 |     8192 |          -1 | 120.00 |        0 |                        4358.23 |                     4287.80 |         0.00 |                                                     106951.00 |                                              35760.00 |
| mariadb-1-2-2 | mariadb-1-2-2 |                2 |        2 |               1 |           2 |       320 |    16384 |          -1 | 120.00 |        0 |                        4039.10 |                     3982.59 |         0.00 |                                                     209780.00 |                                              79111.00 |
| mariadb-1-2-3 | mariadb-1-2-3 |                2 |        3 |               1 |           2 |       160 |     8192 |          -1 | 120.00 |        0 |                        3776.84 |                     3722.75 |         0.00 |                                                     111719.00 |                                              42185.50 |
| mariadb-1-2-4 | mariadb-1-2-4 |                2 |        4 |               1 |           4 |       320 |    16384 |          -1 | 120.00 |        0 |                        3890.12 |                     3837.90 |         0.00 |                                                     225834.00 |                                              81983.50 |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |      4347.08 |     37.16 |           3.62 |                  3.62 |
| mariadb-1-1-2-1 |      1381.71 |     13.41 |           4.00 |                  4.00 |
| mariadb-1-1-3-1 |      1848.77 |     16.53 |           4.43 |                  4.43 |
| mariadb-1-1-4-1 |      1437.54 |     14.23 |           4.79 |                  4.79 |
| mariadb-1-2-1-1 |      3338.82 |     36.33 |           4.87 |                  4.87 |
| mariadb-1-2-2-1 |      1624.80 |     15.19 |           5.46 |                  5.47 |
| mariadb-1-2-3-1 |      1535.38 |     13.58 |           5.70 |                  5.70 |
| mariadb-1-2-4-1 |      1275.78 |     13.15 |           6.05 |                  6.05 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |       861.05 |      8.28 |           1.16 |                  1.16 |
| mariadb-1-1-2-1 |       551.54 |      8.23 |           0.91 |                  0.91 |
| mariadb-1-1-3-1 |       699.17 |      7.03 |           0.67 |                  0.67 |
| mariadb-1-1-4-1 |       684.81 |      9.42 |           0.61 |                  0.61 |
| mariadb-1-2-1-1 |       564.93 |      7.02 |           0.98 |                  0.98 |
| mariadb-1-2-2-1 |       735.56 |      7.29 |           0.78 |                  0.78 |
| mariadb-1-2-3-1 |       648.78 |      7.10 |           0.66 |                  0.66 |
| mariadb-1-2-4-1 |       648.94 |      7.84 |           0.60 |                  0.60 |

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
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: SUT pods not replaced
* TEST passed: Host information complete
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Monitoring returned data
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
* TEST passed: Every pod ran for the configured time
* TEST passed: Results of all benchmarker pods
* TEST passed: Benchmarker pods without errors

Test successful!
```

</details>


## HammerDB's TPC-C

See [Example: HammerDB](Example-HammerDB.md) for the parameters.

### Simple

```bash
bexhoma hammerdb \
  -dbms MariaDB \
  -sf 16 \
  -nc 1 \
  -ne 1 \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -ms $BEXHOMA_MS \
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
* Type: hammerdb
* Duration: 813s 
* Code: 1795672583
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Ramp-up period is 2 minutes before measurements begin.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mariadb', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mariadb-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:626809
  * datadisk:1673
  * volume_size:1.8T
  * volume_used:613G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795672583

### Ingestion
* MariaDB-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1795672583-64667fbcc7-q8g5q: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: hammerdb (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: hammerdb (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |   16 |       65.00 |           2.00 |            0.00 |         60.00 |            3.00 |              1 |         8 |             | None           |             0 | False         |              886.15 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   threads |   NOPM |    TPM |   efficiency |   duration |   errors |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|-------:|-------:|-------------:|-----------:|---------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       1 |        16 | 187331 | 435792 |         0.00 |          5 |        0 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   efficiency |      NOPM |       TPM |   duration |   errors |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|----------:|-------------:|----------:|----------:|-----------:|---------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 |        16 |         0.00 | 187331.00 | 435792.00 |          5 |        0 |

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
* TEST passed: NOPM contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey))
* TEST passed: Workflow as planned
* TEST passed: No virtual user FINISHED FAILED
* TEST passed: Every pod ran for the configured time
* TEST passed: Results of all benchmarker pods
* TEST passed: Benchmarker pods without errors

Test successful!
```

</details>

### Monitoring on Persistent Storage

```bash
bexhoma hammerdb \
  -dbms MariaDB \
  -sf 16 \
  -nc 1 \
  -ne 1 \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -m \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hammerdb_mariadb_monitoring.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hammerdb_mariadb_monitoring_summary.md" target="_blank" rel="noopener">docs_hammerdb_mariadb_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: hammerdb
* Duration: 796s 
* Code: 1795673404
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Ramp-up period is 2 minutes before measurements begin.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
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
  * disk:624066
  * datadisk:1734
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
    * code:1795673404

### Ingestion
* MariaDB-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1795673404-f9c5594dd-6h4f5: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: hammerdb (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: hammerdb (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |   16 |       60.00 |           3.00 |            0.00 |         55.00 |            2.00 |              1 |         8 |             | None           |             0 | False         |              960.00 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   threads |   NOPM |    TPM |   efficiency |   duration |   errors |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|-------:|-------:|-------------:|-----------:|---------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       1 |        16 | 105248 | 244157 |         0.00 |          5 |        0 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   efficiency |      NOPM |       TPM |   duration |   errors |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|----------:|-------------:|----------:|----------:|-----------:|---------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 |        16 |         0.00 | 105248.00 | 244157.00 |          5 |        0 |

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |        78.51 |      1.70 |           2.58 |                  2.59 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |       233.00 |      5.77 |           0.10 |                  0.10 |

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |      1648.17 |      4.21 |           3.34 |                  3.35 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |       537.89 |      1.48 |           0.08 |                  0.08 |

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
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: SUT pods not replaced
* TEST passed: Host information complete
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Monitoring returned data
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: NOPM contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey))
* TEST passed: Workflow as planned
* TEST passed: No virtual user FINISHED FAILED
* TEST passed: Every pod ran for the configured time
* TEST passed: Results of all benchmarker pods
* TEST passed: Benchmarker pods without errors

Test successful!
```

</details>

### Scaling the Clients

1 and 2 benchmarker pods (`-nbp 1,2`) and 1 and 2 rounds (`-ne 1,2`), on the volume loaded by the monitoring run.

```bash
bexhoma hammerdb \
  -dbms MariaDB \
  -sf 16 \
  -xsd 2 \
  -nc 2 \
  -ne 1,2 \
  -nlt 8 \
  -nbp 1,2 \
  -nbt 16 \
  -m \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hammerdb_mariadb_scale.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hammerdb_mariadb_scale_summary.md" target="_blank" rel="noopener">docs_hammerdb_mariadb_scale.log</a></summary>

```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: hammerdb
* Duration: 2836s 
* Code: 1795674239
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 2 minutes. Ramp-up period is 2 minutes before measurements begin.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
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
  * disk:661607
  * datadisk:2498
  * volume_size:49G
  * volume_used:2.5G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1795674239
* mariadb-1-1-2-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:662765
  * datadisk:2875
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
    * code:1795674239
* mariadb-1-1-3-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:628201
  * datadisk:3437
  * volume_size:49G
  * volume_used:3.4G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1795674239
* mariadb-1-1-4-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:629785
  * datadisk:3878
  * volume_size:49G
  * volume_used:3.8G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1795674239
* mariadb-1-2-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:632956
  * datadisk:4160
  * volume_size:49G
  * volume_used:4.1G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1795674239
* mariadb-1-2-2-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:667251
  * datadisk:4606
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
    * code:1795674239
* mariadb-1-2-3-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:670760
  * datadisk:5197
  * volume_size:49G
  * volume_used:5.1G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1795674239
* mariadb-1-2-4-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:636759
  * datadisk:5598
  * volume_size:49G
  * volume_used:5.5G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1795674239

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MariaDB-1

### Data Parameters of Reused Volumes
* MariaDB-1: loading values of the volume: script=Schema, indexing=Checks

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1795674239-7648779df9-62mf6: 0
* bexhoma-sut-mariadb-1-1795674239-b5c899666-d7clw: 0

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

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |   16 |       60.00 |           3.00 |            0.00 |         55.00 |            2.00 |              0 |         8 |             | None           |             0 | False         |              960.00 | True                |
| MariaDB-1-2 |                2 |   16 |       60.00 |           3.00 |            0.00 |         55.00 |            2.00 |              0 |         8 |             | None           |             0 | False         |              960.00 | True                |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   threads |   NOPM |    TPM |   efficiency |   duration |   errors |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|-------:|-------:|-------------:|-----------:|---------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       1 |        16 |  91323 | 211863 |         0.00 |          2 |        0 |
| mariadb-1-1-2-1-1 | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |       1 |        16 | 142930 | 331074 |         0.00 |          2 |        0 |
| mariadb-1-1-2-1-2 | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |       2 |        16 | 142661 | 330428 |         0.00 |          2 |        0 |
| mariadb-1-1-3-1-1 | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        3 |               1 |       1 |         8 | 107098 | 248334 |         0.00 |          2 |        0 |
| mariadb-1-1-3-1-2 | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        3 |               1 |       2 |         8 | 107014 | 248153 |         0.00 |          2 |        0 |
| mariadb-1-1-4-1-1 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       1 |         8 |  51058 | 119097 |         0.00 |          2 |        0 |
| mariadb-1-1-4-1-2 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       2 |         8 |  51683 | 120600 |         0.00 |          2 |        0 |
| mariadb-1-1-4-1-3 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       3 |         8 |  51835 | 120947 |         0.00 |          2 |        0 |
| mariadb-1-1-4-1-4 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       4 |         8 |  51409 | 119949 |         0.00 |          2 |        0 |
| mariadb-1-2-1-1-1 | mariadb-1-2-1 | mariadb-1-2-1-1 |                2 |        1 |               1 |       1 |        16 | 109324 | 253203 |         0.00 |          2 |        0 |
| mariadb-1-2-2-1-1 | mariadb-1-2-2 | mariadb-1-2-2-1 |                2 |        2 |               1 |       1 |        16 | 148032 | 343860 |         0.00 |          2 |        0 |
| mariadb-1-2-2-1-2 | mariadb-1-2-2 | mariadb-1-2-2-1 |                2 |        2 |               1 |       2 |        16 | 147802 | 343412 |         0.00 |          2 |        0 |
| mariadb-1-2-3-1-1 | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        3 |               1 |       1 |         8 |  98731 | 228447 |         0.00 |          2 |        0 |
| mariadb-1-2-3-1-2 | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        3 |               1 |       2 |         8 |  98941 | 228939 |         0.00 |          2 |        0 |
| mariadb-1-2-4-1-1 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       1 |         8 | 149793 | 347558 |         0.00 |          2 |        0 |
| mariadb-1-2-4-1-2 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       2 |         8 | 149803 | 347613 |         0.00 |          2 |        0 |
| mariadb-1-2-4-1-3 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       3 |         8 | 149773 | 347584 |         0.00 |          2 |        0 |
| mariadb-1-2-4-1-4 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       4 |         8 | 149873 | 347762 |         0.00 |          2 |        0 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   efficiency |      NOPM |       TPM |   duration |   errors |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|----------:|-------------:|----------:|----------:|-----------:|---------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 |        16 |         0.00 |  91323.00 | 211863.00 |          2 |        0 |
| mariadb-1-1-2 | mariadb-1-1-2 |                1 |        2 |               1 |           2 |        32 |         0.00 | 142795.50 | 330751.00 |          2 |        0 |
| mariadb-1-1-3 | mariadb-1-1-3 |                1 |        3 |               1 |           2 |        16 |         0.00 | 107056.00 | 248243.50 |          2 |        0 |
| mariadb-1-1-4 | mariadb-1-1-4 |                1 |        4 |               1 |           4 |        32 |         0.00 |  51496.25 | 120148.25 |          2 |        0 |
| mariadb-1-2-1 | mariadb-1-2-1 |                2 |        1 |               1 |           1 |        16 |         0.00 | 109324.00 | 253203.00 |          2 |        0 |
| mariadb-1-2-2 | mariadb-1-2-2 |                2 |        2 |               1 |           2 |        32 |         0.00 | 147917.00 | 343636.00 |          2 |        0 |
| mariadb-1-2-3 | mariadb-1-2-3 |                2 |        3 |               1 |           2 |        16 |         0.00 |  98836.00 | 228693.00 |          2 |        0 |
| mariadb-1-2-4 | mariadb-1-2-4 |                2 |        4 |               1 |           4 |        32 |         0.00 | 149810.50 | 347629.25 |          2 |        0 |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |      1115.29 |      4.92 |           3.36 |                  3.37 |
| mariadb-1-1-2-1 |      1822.76 |      8.14 |           3.98 |                  3.99 |
| mariadb-1-1-3-1 |      1062.80 |      4.98 |           4.39 |                  4.39 |
| mariadb-1-1-4-1 |      1110.37 |      7.84 |           4.71 |                  4.71 |
| mariadb-1-2-1-1 |      1297.89 |      5.83 |           5.00 |                  5.01 |
| mariadb-1-2-2-1 |      1959.19 |      8.81 |           5.64 |                  5.64 |
| mariadb-1-2-3-1 |      1353.88 |      5.85 |           6.05 |                  6.05 |
| mariadb-1-2-4-1 |      2046.26 |      9.14 |           6.64 |                  6.65 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |       324.28 |      1.47 |           0.08 |                  0.08 |
| mariadb-1-1-2-1 |       461.69 |      2.20 |           0.08 |                  0.08 |
| mariadb-1-1-3-1 |       300.29 |      1.43 |           0.05 |                  0.05 |
| mariadb-1-1-4-1 |       256.89 |      2.06 |           0.05 |                  0.05 |
| mariadb-1-2-1-1 |       205.59 |      0.96 |           0.08 |                  0.08 |
| mariadb-1-2-2-1 |       282.44 |      1.36 |           0.08 |                  0.08 |
| mariadb-1-2-3-1 |       128.02 |      0.63 |           0.05 |                  0.05 |
| mariadb-1-2-4-1 |       327.44 |      1.49 |           0.05 |                  0.05 |

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
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: SUT pods not replaced
* TEST passed: Host information complete
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Monitoring returned data
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: NOPM contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey))
* TEST passed: Workflow as planned
* TEST passed: No virtual user FINISHED FAILED
* TEST passed: Every pod ran for the configured time
* TEST passed: Results of all benchmarker pods
* TEST passed: Benchmarker pods without errors

Test successful!
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
  -xnbf 1 \
  -xnlf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 4,8 \
  -nlt 32,64 \
  -nbp 1 \
  -nbt 64 \
  -ms $BEXHOMA_MS \
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
* Duration: 2353s 
* Code: 1795677107
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
  * Experiment uses bexhoma version 0.12.4.
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mariadb', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mariadb-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:648478
  * datadisk:1794
  * volume_size:1.8T
  * volume_used:634G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795677107
* mariadb-2-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:648478
  * datadisk:1770
  * volume_size:1.8T
  * volume_used:634G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795677107
* mariadb-3-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:648478
  * datadisk:1794
  * volume_size:1.8T
  * volume_used:634G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795677107
* mariadb-4-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:648478
  * datadisk:1770
  * volume_size:1.8T
  * volume_used:634G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795677107

### Ingestion
* MariaDB-1: 4 of 4 units ok
* MariaDB-2: 8 of 8 units ok
* MariaDB-3: 4 of 4 units ok
* MariaDB-4: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1795677107-6567db57b9-rwnn4: 0
* bexhoma-sut-mariadb-2-1795677107-5fcff59977-q2djh: 0
* bexhoma-sut-mariadb-3-1795677107-6ddd46f697-zm6t7: 0
* bexhoma-sut-mariadb-4-1795677107-5b7b8ddd97-jfd9q: 0

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

| connection        |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| mariadb-1-1-0-1-1 |             1.00 |      8.00 |   256.00 |        4.00 |     0.00 |                          255.93 |               976815.00 |            250000.00 |                              4971.00 | 1.00 |                3.69 |
| mariadb-1-1-0-1-2 |             1.00 |      8.00 |   256.00 |        4.00 |     0.00 |                          255.93 |               976812.00 |            250000.00 |                              4843.00 | 1.00 |                3.69 |
| mariadb-1-1-0-1-3 |             1.00 |      8.00 |   256.00 |        4.00 |     0.00 |                          255.93 |               976827.00 |            250000.00 |                              4915.00 | 1.00 |                3.69 |
| mariadb-1-1-0-1-4 |             1.00 |      8.00 |   256.00 |        4.00 |     0.00 |                          255.93 |               976836.00 |            250000.00 |                              5059.00 | 1.00 |                3.69 |
| mariadb-2-1-0-1-1 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.97 |               976810.00 |            125000.00 |                              4839.00 | 1.00 |                3.69 |
| mariadb-2-1-0-1-2 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.97 |               976802.00 |            125000.00 |                              4947.00 | 1.00 |                3.69 |
| mariadb-2-1-0-1-3 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.97 |               976812.00 |            125000.00 |                              5195.00 | 1.00 |                3.69 |
| mariadb-2-1-0-1-4 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.97 |               976823.00 |            125000.00 |                              5155.00 | 1.00 |                3.69 |
| mariadb-2-1-0-1-5 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.97 |               976815.00 |            125000.00 |                              5299.00 | 1.00 |                3.69 |
| mariadb-2-1-0-1-6 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.97 |               976812.00 |            125000.00 |                              5307.00 | 1.00 |                3.69 |
| mariadb-2-1-0-1-7 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.97 |               976820.00 |            125000.00 |                              5007.00 | 1.00 |                3.69 |
| mariadb-2-1-0-1-8 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.97 |               976798.00 |            125000.00 |                              5235.00 | 1.00 |                3.69 |
| mariadb-3-1-0-1-1 |             1.00 |     16.00 |   256.00 |        4.00 |     0.00 |                          255.92 |               976871.00 |            250000.00 |                              5255.00 | 1.00 |                3.69 |
| mariadb-3-1-0-1-2 |             1.00 |     16.00 |   256.00 |        4.00 |     0.00 |                          255.92 |               976880.00 |            250000.00 |                              5159.00 | 1.00 |                3.69 |
| mariadb-3-1-0-1-3 |             1.00 |     16.00 |   256.00 |        4.00 |     0.00 |                          255.92 |               976869.00 |            250000.00 |                              5055.00 | 1.00 |                3.69 |
| mariadb-3-1-0-1-4 |             1.00 |     16.00 |   256.00 |        4.00 |     0.00 |                          255.92 |               976853.00 |            250000.00 |                              4991.00 | 1.00 |                3.69 |
| mariadb-4-1-0-1-1 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.96 |               976856.00 |            125000.00 |                              5071.00 | 1.00 |                3.69 |
| mariadb-4-1-0-1-2 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.96 |               976831.00 |            125000.00 |                              5287.00 | 1.00 |                3.69 |
| mariadb-4-1-0-1-3 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.96 |               976833.00 |            125000.00 |                              5243.00 | 1.00 |                3.69 |
| mariadb-4-1-0-1-4 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.96 |               976846.00 |            125000.00 |                              5007.00 | 1.00 |                3.69 |
| mariadb-4-1-0-1-5 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.96 |               976847.00 |            125000.00 |                              5079.00 | 1.00 |                3.69 |
| mariadb-4-1-0-1-6 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.96 |               976881.00 |            125000.00 |                              5123.00 | 1.00 |                3.69 |
| mariadb-4-1-0-1-7 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.96 |               976841.00 |            125000.00 |                              5199.00 | 1.00 |                3.69 |
| mariadb-4-1-0-1-8 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.96 |               976852.00 |            125000.00 |                              5147.00 | 1.00 |                3.69 |

#### Per Run

| DBMS        |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:------------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MariaDB-1-1 |             1.00 |     32.00 |  1024.00 |        4.00 |     0.00 | 1.00 |                3.69 |                         1023.73 |               976836.00 |           1000000.00 |                              4947.00 |
| MariaDB-2-1 |             1.00 |     32.00 |  1024.00 |        8.00 |     0.00 | 1.00 |                3.69 |                         1023.74 |               976823.00 |           1000000.00 |                              5123.00 |
| MariaDB-3-1 |             1.00 |     64.00 |  1024.00 |        4.00 |     0.00 | 1.00 |                3.69 |                         1023.68 |               976880.00 |           1000000.00 |                              5115.00 |
| MariaDB-4-1 |             1.00 |     64.00 |  1024.00 |        8.00 |     0.00 | 1.00 |                3.69 |                         1023.70 |               976881.00 |           1000000.00 |                              5144.50 |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1023.31 |               977221.00 |             500288 |                            1275.00 |               499712 |                              2847.00 |
| mariadb-2-1-1-1-1 | mariadb-2-1-1 | mariadb-2-1-1-1 |                1 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1023.23 |               977299.00 |             500826 |                            1303.00 |               499174 |                              2825.00 |
| mariadb-3-1-1-1-1 | mariadb-3-1-1 | mariadb-3-1-1-1 |                1 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1023.28 |               977245.00 |             499197 |                            1371.00 |               500803 |                              2945.00 |
| mariadb-4-1-1-1-1 | mariadb-4-1-1 | mariadb-4-1-1-1 |                1 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1023.34 |               977194.00 |             500238 |                            1245.00 |               499762 |                              2801.00 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1023.31 |               977221.00 |             500288 |                            1275.00 |               499712 |                              2847.00 |
| mariadb-2-1-1 | mariadb-2-1-1 |                1 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1023.23 |               977299.00 |             500826 |                            1303.00 |               499174 |                              2825.00 |
| mariadb-3-1-1 | mariadb-3-1-1 |                1 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1023.28 |               977245.00 |             499197 |                            1371.00 |               500803 |                              2945.00 |
| mariadb-4-1-1 | mariadb-4-1-1 |                1 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1023.34 |               977194.00 |             500238 |                            1245.00 |               499762 |                              2801.00 |

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
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
* TEST passed: Execution Phase: every pod ran its configured operations
* TEST passed: Results of all benchmarker pods
* TEST passed: Benchmarker pods without errors

Test successful!
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
  -xnbf 1 \
  -xnlf 1 \
  -nc 2 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
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
* Duration: 3571s 
* Code: 1795679472
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
  * Experiment uses bexhoma version 0.12.4.
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mariadb', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mariadb-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:622570
  * datadisk:1774
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
    * code:1795679472
* mariadb-1-2-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:622782
  * datadisk:1774
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
    * code:1795679472

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MariaDB-1-2

### Data Parameters of Reused Volumes
* MariaDB-1: DDL values of the volume: row_format=default, collation=default
* MariaDB-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### Ingestion
* MariaDB-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1795679472-9965769b6-q67r5: 0
* bexhoma-sut-mariadb-1-1795679472-5f686d59b9-d9lmf: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection        |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| mariadb-1-1-0-1-1 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.95 |               976954.00 |            125000.00 |                              6467.00 | 1.00 |                3.68 |
| mariadb-1-1-0-1-2 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.95 |               976954.00 |            125000.00 |                              6319.00 | 1.00 |                3.68 |
| mariadb-1-1-0-1-3 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.91 |               977217.00 |            125000.00 |                              6463.00 | 1.00 |                3.68 |
| mariadb-1-1-0-1-4 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.93 |               977131.00 |            125000.00 |                              5707.00 | 1.00 |                3.68 |
| mariadb-1-1-0-1-5 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.94 |               977027.00 |            125000.00 |                              6107.00 | 1.00 |                3.68 |
| mariadb-1-1-0-1-6 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.96 |               976897.00 |            125000.00 |                              6099.00 | 1.00 |                3.69 |
| mariadb-1-1-0-1-7 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.94 |               977034.00 |            125000.00 |                              6007.00 | 1.00 |                3.68 |
| mariadb-1-1-0-1-8 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.92 |               977152.00 |            125000.00 |                              6235.00 | 1.00 |                3.68 |

#### Per Run

| DBMS        |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:------------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MariaDB-1-1 |             1.00 |     64.00 |  1024.00 |        8.00 |     0.00 | 1.00 |                3.68 |                         1023.49 |               977217.00 |           1000000.00 |                              6175.50 |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1023.29 |               977241.00 |             499426 |                            1063.00 |               500574 |                              5563.00 |
| mariadb-1-2-1-1-1 | mariadb-1-2-1 | mariadb-1-2-1-1 |                2 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1023.53 |               977013.00 |             500644 |                             990.00 |               499356 |                              4747.00 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1023.29 |               977241.00 |             499426 |                            1063.00 |               500574 |                              5563.00 |
| mariadb-1-2-1 | mariadb-1-2-1 |                2 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1023.53 |               977013.00 |             500644 |                             990.00 |               499356 |                              4747.00 |

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
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
* TEST passed: Execution Phase: every pod ran its configured operations
* TEST passed: Results of all benchmarker pods
* TEST passed: Benchmarker pods without errors

Test successful!
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
  -xnbf 1 \
  -xnlf 1 \
  -nc 2 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1,8 \
  -nbt 64 \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
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
* Duration: 6700s 
* Code: 1795683054
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
  * Experiment uses bexhoma version 0.12.4.
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mariadb', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mariadb-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:622529
  * datadisk:1774
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
    * code:1795683054
* mariadb-1-1-2-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:768498
  * datadisk:1774
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
    * code:1795683054
* mariadb-1-1-3-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:772513
  * datadisk:1774
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
    * code:1795683054
* mariadb-1-1-4-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:774234
  * datadisk:1774
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
    * code:1795683054
* mariadb-1-2-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:635284
  * datadisk:1774
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
    * code:1795683054
* mariadb-1-2-2-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:636100
  * datadisk:1774
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
    * code:1795683054
* mariadb-1-2-3-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:636103
  * datadisk:1774
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
    * code:1795683054
* mariadb-1-2-4-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:636304
  * datadisk:1774
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
    * code:1795683054

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MariaDB-1

### Data Parameters of Reused Volumes
* MariaDB-1: DDL values of the volume: row_format=default, collation=default
* MariaDB-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1795683054-6556cdb4b7-9gslz: 0
* bexhoma-sut-mariadb-1-1795683054-84d6f98fb-swhf2: 0

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

| connection         | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mariadb-1-1-1-1-1  | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1023.39 |               977140.00 |             500398 |                            1252.00 |               499602 |                              4267.00 |
| mariadb-1-1-2-1-1  | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |       1 |        64 |     1024 |        0 |                         1022.59 |               488955.00 |             249919 |                            1089.00 |               250081 |                              4171.00 |
| mariadb-1-1-2-1-2  | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |       2 |        64 |     1024 |        0 |                         1022.63 |               488935.00 |             250493 |                            1092.00 |               249507 |                              4099.00 |
| mariadb-1-1-3-1-1  | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        3 |               1 |       1 |         8 |      128 |        0 |                          127.95 |               976924.00 |              62704 |                            1151.00 |                62296 |                              3887.00 |
| mariadb-1-1-3-1-2  | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        3 |               1 |       2 |         8 |      128 |        0 |                          127.96 |               976903.00 |              62635 |                            1165.00 |                62365 |                              3781.00 |
| mariadb-1-1-3-1-3  | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        3 |               1 |       3 |         8 |      128 |        0 |                          127.95 |               976918.00 |              62579 |                            1157.00 |                62421 |                              3737.00 |
| mariadb-1-1-3-1-4  | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        3 |               1 |       4 |         8 |      128 |        0 |                          127.96 |               976887.00 |              62644 |                            1170.00 |                62356 |                              3843.00 |
| mariadb-1-1-3-1-5  | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        3 |               1 |       5 |         8 |      128 |        0 |                          127.96 |               976894.00 |              62316 |                            1116.00 |                62684 |                              3811.00 |
| mariadb-1-1-3-1-6  | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        3 |               1 |       6 |         8 |      128 |        0 |                          127.96 |               976905.00 |              62818 |                            1181.00 |                62182 |                              3895.00 |
| mariadb-1-1-3-1-7  | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        3 |               1 |       7 |         8 |      128 |        0 |                          127.95 |               976912.00 |              62410 |                            1152.00 |                62590 |                              3859.00 |
| mariadb-1-1-3-1-8  | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        3 |               1 |       8 |         8 |      128 |        0 |                          127.95 |               976928.00 |              62159 |                            1154.00 |                62841 |                              3861.00 |
| mariadb-1-1-4-1-1  | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       1 |         8 |      128 |        0 |                          127.90 |               488673.00 |              31345 |                            1205.00 |                31155 |                              4243.00 |
| mariadb-1-1-4-1-2  | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       2 |         8 |      128 |        0 |                          127.90 |               488667.00 |              31230 |                            1163.00 |                31270 |                              4315.00 |
| mariadb-1-1-4-1-3  | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       3 |         8 |      128 |        0 |                          127.90 |               488653.00 |              31107 |                            1268.00 |                31393 |                              4243.00 |
| mariadb-1-1-4-1-4  | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       4 |         8 |      128 |        0 |                          127.90 |               488647.00 |              31243 |                            1220.00 |                31257 |                              4443.00 |
| mariadb-1-1-4-1-5  | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       5 |         8 |      128 |        0 |                          127.90 |               488674.00 |              31201 |                            1233.00 |                31299 |                              4187.00 |
| mariadb-1-1-4-1-6  | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       6 |         8 |      128 |        0 |                          127.91 |               488627.00 |              31411 |                            1224.00 |                31089 |                              4351.00 |
| mariadb-1-1-4-1-7  | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       7 |         8 |      128 |        0 |                          127.90 |               488647.00 |              31346 |                            1233.00 |                31154 |                              4355.00 |
| mariadb-1-1-4-1-8  | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       8 |         8 |      128 |        0 |                          127.90 |               488669.00 |              31222 |                            1228.00 |                31278 |                              4131.00 |
| mariadb-1-1-4-1-9  | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       9 |         8 |      128 |        0 |                          127.91 |               488640.00 |              31325 |                            1203.00 |                31175 |                              4187.00 |
| mariadb-1-1-4-1-10 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |      10 |         8 |      128 |        0 |                          127.90 |               488655.00 |              31314 |                            1201.00 |                31186 |                              4311.00 |
| mariadb-1-1-4-1-11 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |      11 |         8 |      128 |        0 |                          127.90 |               488657.00 |              31285 |                            1227.00 |                31215 |                              4163.00 |
| mariadb-1-1-4-1-12 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |      12 |         8 |      128 |        0 |                          127.90 |               488657.00 |              31203 |                            1227.00 |                31297 |                              4399.00 |
| mariadb-1-1-4-1-13 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |      13 |         8 |      128 |        0 |                          127.90 |               488644.00 |              31074 |                            1173.00 |                31426 |                              4175.00 |
| mariadb-1-1-4-1-14 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |      14 |         8 |      128 |        0 |                          127.91 |               488636.00 |              31398 |                            1212.00 |                31102 |                              4383.00 |
| mariadb-1-1-4-1-15 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |      15 |         8 |      128 |        0 |                          127.90 |               488662.00 |              31270 |                            1235.00 |                31230 |                              4299.00 |
| mariadb-1-1-4-1-16 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |      16 |         8 |      128 |        0 |                          127.90 |               488667.00 |              31186 |                            1253.00 |                31314 |                              4279.00 |
| mariadb-1-2-1-1-1  | mariadb-1-2-1 | mariadb-1-2-1-1 |                2 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1023.36 |               977177.00 |             499560 |                            1221.00 |               500440 |                              3723.00 |
| mariadb-1-2-2-1-1  | mariadb-1-2-2 | mariadb-1-2-2-1 |                2 |        2 |               1 |       1 |        64 |     1024 |        0 |                         1022.99 |               488761.00 |             250098 |                            1151.00 |               249902 |                              3991.00 |
| mariadb-1-2-2-1-2  | mariadb-1-2-2 | mariadb-1-2-2-1 |                2 |        2 |               1 |       2 |        64 |     1024 |        0 |                         1023.02 |               488750.00 |             249469 |                            1153.00 |               250531 |                              4001.00 |
| mariadb-1-2-3-1-1  | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        3 |               1 |       1 |         8 |      128 |        0 |                          127.96 |               976838.00 |              62415 |                            1221.00 |                62585 |                              3647.00 |
| mariadb-1-2-3-1-2  | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        3 |               1 |       2 |         8 |      128 |        0 |                          127.96 |               976852.00 |              62482 |                            1211.00 |                62518 |                              3845.00 |
| mariadb-1-2-3-1-3  | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        3 |               1 |       3 |         8 |      128 |        0 |                          127.96 |               976853.00 |              62496 |                            1213.00 |                62504 |                              3789.00 |
| mariadb-1-2-3-1-4  | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        3 |               1 |       4 |         8 |      128 |        0 |                          127.96 |               976859.00 |              62539 |                            1222.00 |                62461 |                              3665.00 |
| mariadb-1-2-3-1-5  | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        3 |               1 |       5 |         8 |      128 |        0 |                          127.97 |               976829.00 |              62476 |                            1208.00 |                62524 |                              3553.00 |
| mariadb-1-2-3-1-6  | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        3 |               1 |       6 |         8 |      128 |        0 |                          127.96 |               976843.00 |              62510 |                            1219.00 |                62490 |                              3625.00 |
| mariadb-1-2-3-1-7  | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        3 |               1 |       7 |         8 |      128 |        0 |                          127.96 |               976847.00 |              62495 |                            1229.00 |                62505 |                              3917.00 |
| mariadb-1-2-3-1-8  | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        3 |               1 |       8 |         8 |      128 |        0 |                          127.96 |               976839.00 |              62602 |                            1215.00 |                62398 |                              3765.00 |
| mariadb-1-2-4-1-1  | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       1 |         8 |      128 |        0 |                          127.91 |               488621.00 |              31157 |                            1224.00 |                31343 |                              3663.00 |
| mariadb-1-2-4-1-2  | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       2 |         8 |      128 |        0 |                          127.90 |               488650.00 |              31157 |                            1227.00 |                31343 |                              3575.00 |
| mariadb-1-2-4-1-3  | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       3 |         8 |      128 |        0 |                          127.90 |               488648.00 |              31348 |                            1170.00 |                31152 |                              3659.00 |
| mariadb-1-2-4-1-4  | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       4 |         8 |      128 |        0 |                          127.90 |               488663.00 |              31104 |                            1209.00 |                31396 |                              3775.00 |
| mariadb-1-2-4-1-5  | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       5 |         8 |      128 |        0 |                          127.90 |               488659.00 |              31247 |                            1219.00 |                31253 |                              3645.00 |
| mariadb-1-2-4-1-6  | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       6 |         8 |      128 |        0 |                          127.91 |               488641.00 |              31356 |                            1214.00 |                31144 |                              3633.00 |
| mariadb-1-2-4-1-7  | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       7 |         8 |      128 |        0 |                          127.89 |               488684.00 |              31357 |                            1219.00 |                31143 |                              3739.00 |
| mariadb-1-2-4-1-8  | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       8 |         8 |      128 |        0 |                          127.90 |               488650.00 |              31298 |                            1198.00 |                31202 |                              3741.00 |
| mariadb-1-2-4-1-9  | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       9 |         8 |      128 |        0 |                          127.90 |               488664.00 |              31117 |                            1212.00 |                31383 |                              3603.00 |
| mariadb-1-2-4-1-10 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |      10 |         8 |      128 |        0 |                          127.90 |               488661.00 |              31289 |                            1231.00 |                31211 |                              3625.00 |
| mariadb-1-2-4-1-11 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |      11 |         8 |      128 |        0 |                          127.90 |               488656.00 |              31450 |                            1184.00 |                31050 |                              3655.00 |
| mariadb-1-2-4-1-12 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |      12 |         8 |      128 |        0 |                          127.90 |               488658.00 |              31205 |                            1245.00 |                31295 |                              3697.00 |
| mariadb-1-2-4-1-13 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |      13 |         8 |      128 |        0 |                          127.90 |               488644.00 |              31119 |                            1225.00 |                31381 |                              3667.00 |
| mariadb-1-2-4-1-14 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |      14 |         8 |      128 |        0 |                          127.89 |               488694.00 |              31271 |                            1207.00 |                31229 |                              3681.00 |
| mariadb-1-2-4-1-15 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |      15 |         8 |      128 |        0 |                          127.89 |               488685.00 |              31305 |                            1211.00 |                31195 |                              3597.00 |
| mariadb-1-2-4-1-16 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |      16 |         8 |      128 |        0 |                          127.90 |               488672.00 |              31197 |                            1198.00 |                31303 |                              3595.00 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1023.39 |               977140.00 |             500398 |                            1252.00 |               499602 |                              4267.00 |
| mariadb-1-1-2 | mariadb-1-1-2 |                1 |        2 |               1 |           2 |       128 |     2048 |        0 |                         2045.22 |               488955.00 |             500412 |                            1092.00 |               499588 |                              4171.00 |
| mariadb-1-1-3 | mariadb-1-1-3 |                1 |        3 |               1 |           8 |        64 |     1024 |        0 |                         1023.64 |               976928.00 |             500265 |                            1181.00 |               499735 |                              3895.00 |
| mariadb-1-1-4 | mariadb-1-1-4 |                1 |        4 |               1 |          16 |       128 |     2048 |        0 |                         2046.43 |               488674.00 |             500160 |                            1268.00 |               499840 |                              4443.00 |
| mariadb-1-2-1 | mariadb-1-2-1 |                2 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1023.36 |               977177.00 |             499560 |                            1221.00 |               500440 |                              3723.00 |
| mariadb-1-2-2 | mariadb-1-2-2 |                2 |        2 |               1 |           2 |       128 |     2048 |        0 |                         2046.01 |               488761.00 |             499567 |                            1153.00 |               500433 |                              4001.00 |
| mariadb-1-2-3 | mariadb-1-2-3 |                2 |        3 |               1 |           8 |        64 |     1024 |        0 |                         1023.70 |               976859.00 |             500015 |                            1229.00 |               499985 |                              3917.00 |
| mariadb-1-2-4 | mariadb-1-2-4 |                2 |        4 |               1 |          16 |       128 |     2048 |        0 |                         2046.42 |               488694.00 |             499977 |                            1245.00 |               500023 |                              3775.00 |

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MariaDB-1)
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: SUT pods not replaced
* TEST passed: Host information complete
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
* TEST passed: Execution Phase: every pod ran its configured operations
* TEST passed: Results of all benchmarker pods
* TEST passed: Benchmarker pods without errors

Test successful!
```

</details>

### Workload E

```bash
bexhoma ycsb \
  -dbms MariaDB \
  -sf 1 \
  -xwl e \
  -xtb 1024 \
  -xnbf 1 \
  -xnlf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 8 \
  -nbt 64 \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
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
* Duration: 1244s 
* Code: 1795689780
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
  * Experiment uses bexhoma version 0.12.4.
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mariadb', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mariadb-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:636119
  * datadisk:1774
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
    * code:1795689780

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MariaDB-1

### Data Parameters of Reused Volumes
* MariaDB-1: DDL values of the volume: row_format=default, collation=default
* MariaDB-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1795689780-b98cb4d59-9wxl6: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: ycsb (8 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: ycsb (8 pods)

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   [SCAN].Return=OK |   [SCAN].99thPercentileLatency(us) |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-------------------:|-----------------------------------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       1 |         8 |      128 |        0 |                          127.95 |               976919.00 |                 6305 |                              3933.00 |             118695 |                            1581.00 |
| mariadb-1-1-1-1-2 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       2 |         8 |      128 |        0 |                          127.96 |               976902.00 |                 6259 |                              3911.00 |             118741 |                            1579.00 |
| mariadb-1-1-1-1-3 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       3 |         8 |      128 |        0 |                          127.95 |               976907.00 |                 6234 |                              3887.00 |             118766 |                            1545.00 |
| mariadb-1-1-1-1-4 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       4 |         8 |      128 |        0 |                          127.96 |               976873.00 |                 6308 |                              3757.00 |             118692 |                            1555.00 |
| mariadb-1-1-1-1-5 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       5 |         8 |      128 |        0 |                          127.96 |               976898.00 |                 6362 |                              3935.00 |             118638 |                            1553.00 |
| mariadb-1-1-1-1-6 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       6 |         8 |      128 |        0 |                          127.96 |               976896.00 |                 6208 |                              3935.00 |             118792 |                            1541.00 |
| mariadb-1-1-1-1-7 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       7 |         8 |      128 |        0 |                          127.96 |               976898.00 |                 6364 |                              3783.00 |             118636 |                            1560.00 |
| mariadb-1-1-1-1-8 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       8 |         8 |      128 |        0 |                          127.95 |               976925.00 |                 6409 |                              3753.00 |             118591 |                            1527.00 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   [SCAN].Return=OK |   [SCAN].99thPercentileLatency(us) |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-------------------:|-----------------------------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           8 |        64 |     1024 |        0 |                         1023.64 |               976925.00 |                50449 |                              3935.00 |             949551 |                            1581.00 |

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MariaDB-1)
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: SUT pods not replaced
* TEST passed: Host information complete
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
* TEST passed: Execution Phase: every pod ran its configured operations
* TEST passed: Results of all benchmarker pods
* TEST passed: Benchmarker pods without errors

Test successful!
```

</details>

### Monitoring

```bash
bexhoma ycsb \
  -dbms MariaDB \
  -sf 1 \
  -xwl a \
  -xtb 1024 \
  -xnbf 1 \
  -xnlf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1,8 \
  -nbt 64 \
  -m \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
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
* Duration: 2245s 
* Code: 1795691035
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
  * Experiment uses bexhoma version 0.12.4.
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mariadb', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mariadb-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:636131
  * datadisk:1855
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
    * code:1795691035
* mariadb-1-1-2-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:636135
  * datadisk:1855
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
    * code:1795691035

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MariaDB-1

### Data Parameters of Reused Volumes
* MariaDB-1: DDL values of the volume: row_format=default, collation=default
* MariaDB-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1795691035-54cd548cdb-x47wv: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: ycsb (8 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: ycsb (8 pods)

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1023.54 |               976997.00 |             500951 |                            1223.00 |               499049 |                              3515.00 |
| mariadb-1-1-2-1-1 | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |       1 |         8 |      128 |        0 |                          127.96 |               976873.00 |              62536 |                            1269.00 |                62464 |                              4099.00 |
| mariadb-1-1-2-1-2 | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |       2 |         8 |      128 |        0 |                          127.95 |               976922.00 |              62431 |                            1239.00 |                62569 |                              3941.00 |
| mariadb-1-1-2-1-3 | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |       3 |         8 |      128 |        0 |                          127.95 |               976923.00 |              62166 |                            1245.00 |                62834 |                              4057.00 |
| mariadb-1-1-2-1-4 | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |       4 |         8 |      128 |        0 |                          127.95 |               976916.00 |              62704 |                            1239.00 |                62296 |                              4087.00 |
| mariadb-1-1-2-1-5 | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |       5 |         8 |      128 |        0 |                          127.95 |               976907.00 |              62677 |                            1264.00 |                62323 |                              4223.00 |
| mariadb-1-1-2-1-6 | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |       6 |         8 |      128 |        0 |                          127.95 |               976910.00 |              62477 |                            1241.00 |                62523 |                              4175.00 |
| mariadb-1-1-2-1-7 | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |       7 |         8 |      128 |        0 |                          127.95 |               976917.00 |              62696 |                            1213.00 |                62304 |                              3985.00 |
| mariadb-1-1-2-1-8 | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |       8 |         8 |      128 |        0 |                          127.96 |               976892.00 |              62334 |                            1245.00 |                62666 |                              3979.00 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1023.54 |               976997.00 |             500951 |                            1223.00 |               499049 |                              3515.00 |
| mariadb-1-1-2 | mariadb-1-1-2 |                1 |        2 |               1 |           8 |        64 |     1024 |        0 |                         1023.64 |               976923.00 |             500021 |                            1269.00 |               499979 |                              4223.00 |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |       195.39 |      0.28 |           2.45 |                  2.45 |
| mariadb-1-1-2-1 |       201.47 |      0.27 |           2.45 |                  2.45 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |       295.41 |      0.59 |           0.19 |                  0.19 |
| mariadb-1-1-2-1 |       363.20 |      0.65 |           0.10 |                  0.10 |

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
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: SUT pods not replaced
* TEST passed: Host information complete
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Monitoring returned data
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
* TEST passed: Execution Phase: every pod ran its configured operations
* TEST passed: Results of all benchmarker pods
* TEST passed: Benchmarker pods without errors

Test successful!
```

</details>


## More

* SSB on MariaDB: see [Example: SSB](Example-SSB.md).
