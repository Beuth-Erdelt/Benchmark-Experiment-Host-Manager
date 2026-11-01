# Example: Benchmark MariaDB ColumnStore

MariaDB ColumnStore is the columnar storage engine of MariaDB [1], under the name `MariaDBCS` in bexhoma.
Bexhoma runs TPC-H, TPC-DS and SSB against it, on a single node.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

The template [deploymenttemplate-MariaDBCS.yml](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-MariaDBCS.yml) uses the official image `mariadb:12.3.3`, the same server as the template of MariaDB, and installs the plugin `mariadb-plugin-columnstore` at every start.
So the pods need access to `archive.mariadb.org` and the Ubuntu mirrors.
Queries run over JDBC, loaders and init scripts use the `mariadb` client.
See [DBMS](DBMS.html#mariadb-columnstore) for the configuration.

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. MariaDB ColumnStore: https://mariadb.com/docs/analytics/mariadb-columnstore
1. MariaDB in Docker: https://hub.docker.com/_/mariadb
1. TPC-H: https://www.tpc.org/tpch/
1. TPC-DS: https://www.tpc.org/tpcds/
1. Star Schema Benchmark: https://www.cs.umb.edu/~poneil/StarSchemaB.PDF
1. Orchestrating DBMS Benchmarking in the Cloud with Kubernetes: https://doi.org/10.1007/978-3-030-94437-7_6


## Perform TPC-H Benchmark

The test scripts [`scripts/test-docs-mariadbcs.sh`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-mariadbcs.sh) and [`scripts/test-docs-mariadbcs.ps1`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-mariadbcs.ps1) run all examples of this page, one after the other.

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
  run &>$LOG_DIR/docs_tpch_mariadbcs_1.log
```

This
* starts a clean instance of MariaDB and of MariaDB ColumnStore (`-dbms`)
  * with a limit of 16 GiB RAM each (`-rr`, `-lr`)
  * data on a persistent volume of 20 GiB (`-rss`) of the storage class `$BEXHOMA_STORAGE_CLASS` (`-rst`), removed first if it exists (`-rsr`)
* creates the TPC-H schema
* loads the data
  * MariaDB with 8 loader pods (`-nlp`)
  * MariaDBCS with one loader pod, whatever `-nlp` says, see [Loading](#loading)
* runs the post-load scripts: indexes (`-xii`), constraints (`-xic`) and statistics (`-xis`) for MariaDB. ColumnStore has no keys and no secondary indexes, so only the statistics do something for MariaDBCS
* runs the check script (row counts, sizes)
* runs 1 stream of the 22 TPC-H queries and stores their result sets (`-xdt`)
* repeats the benchmark once more (`-nc 2`): bexhoma restarts the SUT, which finds the data on the volume and does not load again
* runs the reset scripts before each round (`-ar`)
* monitors the SUT (`-m`)
* tests if results match workflow (`-tr`)
* removes the SUT at the end (`-ks no`)
* shows a summary

MariaDB runs next to MariaDBCS to compare the result sets of both, see [Compare Results](#compare-results).

### Status

You can watch the status while benchmark is running via `bexhoma status`.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e <code>` (removes everything that is related to the experiment `<code>`).

## Evaluate Results

At the end of a benchmark you will see a summary like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_mariadbcs_1_summary.md" target="_blank" rel="noopener">docs_tpch_mariadbcs_1.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 1060s 
* Code: 1793487653
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.11.
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
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:749051
  * datadisk:1962
  * volume_size:20G
  * volume_used:2.0G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793487653
* mariadb-1-2-1-1-1 uses docker image mariadb:12.3.3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:546583
  * datadisk:1963
  * volume_size:20G
  * volume_used:2.0G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793487653
* mariadbcs-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:748673
  * datadisk:512
  * volume_size:20G
  * volume_used:673M
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793487653
* mariadbcs-1-2-1-1-1 uses docker image mariadb:12.3.3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:545337
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
    * code:1793487653

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MariaDB-1-2, MariaDBCS-1-2

### Data Parameters of Reused Volumes
* MariaDB-1: DDL values of the volume: engine=InnoDB, histograms=off
* MariaDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics
* MariaDBCS-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1793487653-59778bb9cf-lsf5s: 0
* bexhoma-sut-mariadb-1-1793487653-9f7cc4758-tctfz: 0
* bexhoma-sut-mariadbcs-1-1793487653-7764779dc-f6t7q: 0
* bexhoma-sut-mariadbcs-1-1793487653-5d8d5866b-89nk5: 0

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

|               |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:--------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1   |                1 |    1 |       84.00 |           6.00 |           12.00 |         20.00 |           36.00 |              8 |           0 |             | None           |             0 | False         |               42.86 | False               |
| MariaDB-1-2   |                2 |    1 |       84.00 |           6.00 |           12.00 |         20.00 |           36.00 |              8 |           0 |             | None           |             0 | False         |               42.86 | True                |
| MariaDBCS-1-1 |                1 |    1 |      100.00 |          10.00 |            0.00 |         65.00 |           19.00 |              1 |           0 |             | None           |             0 | False         |               36.00 | False               |
| MariaDBCS-1-2 |                2 |    1 |      100.00 |          10.00 |            0.00 |         65.00 |           19.00 |              1 |           0 |             | None           |             0 | False         |               36.00 | True                |

### Benchmarking

#### Per Connection

| DBMS                | configuration   | phase           | job               |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                 |
|:--------------------|:----------------|:----------------|:------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:--------------------|
| mariadb-1-1-1-1-1   | MariaDB-1       | mariadb-1-1-1   | mariadb-1-1-1-1   |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         94 |            0.99 |             3713.88 |            842.55 |          -1 | mariadb-1-1-1-1-1   |
| mariadb-1-2-1-1-1   | MariaDB-1       | mariadb-1-2-1   | mariadb-1-2-1-1   |                2 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         89 |            0.94 |             4121.25 |            889.89 |          -1 | mariadb-1-2-1-1-1   |
| mariadbcs-1-1-1-1-1 | MariaDBCS-1     | mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         24 |            0.71 |             5272.56 |           3300.00 |          -1 | mariadbcs-1-1-1-1-1 |
| mariadbcs-1-2-1-1-1 | MariaDBCS-1     | mariadbcs-1-2-1 | mariadbcs-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         32 |            0.99 |             3672.97 |           2475.00 |          -1 | mariadbcs-1-2-1-1-1 |

#### Per Phase

|                 | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1   | mariadb-1-1-1   |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         94 |            0.99 |             3713.88 |            842.55 |          -1 |
| mariadb-1-2-1   | mariadb-1-2-1   |                2 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         89 |            0.94 |             4121.25 |            889.89 |          -1 |
| mariadbcs-1-1-1 | mariadbcs-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         24 |            0.71 |             5272.56 |           3300.00 |          -1 |
| mariadbcs-1-2-1 | mariadbcs-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         32 |            0.99 |             3672.97 |           2475.00 |          -1 |

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
| mariadb-1-1-1   | mariadb-1-1-1-1   |                1 |        1 |               1 |         5.00 |                |
| mariadb-1-2-1   | mariadb-1-2-1-1   |                2 |        1 |               1 |         4.00 |                |
| mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |         5.00 |                |
| mariadbcs-1-2-1 | mariadbcs-1-2-1-1 |                2 |        1 |               1 |         6.00 |                |

### Latency of Timer Execution [ms]
| Queries                                             |   mariadb-1-1-1-1-1 |   mariadb-1-2-1-1-1 |   mariadbcs-1-1-1-1-1 |   mariadbcs-1-2-1-1-1 |
|:----------------------------------------------------|--------------------:|--------------------:|----------------------:|----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |             6696.95 |             7779.54 |                982.33 |               1435.12 |
| Minimum Cost Supplier Query (TPC-H Q2)              |              398.59 |              438.20 |               2748.69 |               3029.67 |
| Shipping Priority (TPC-H Q3)                        |             2403.78 |             1403.04 |               1244.10 |               1572.55 |
| Order Priority Checking Query (TPC-H Q4)            |              315.58 |              414.60 |                445.11 |                955.26 |
| Local Supplier Volume (TPC-H Q5)                    |              802.55 |              840.57 |                675.43 |                877.49 |
| Forecasting Revenue Change (TPC-H Q6)               |              776.85 |              853.83 |                 46.60 |                 65.75 |
| Volume Shipping Query (TPC-H Q7)                    |             1432.54 |              978.74 |               1391.23 |               1361.85 |
| National Market Share (TPC-H Q8)                    |             1498.65 |             1578.94 |                841.08 |                949.96 |
| Product Type Profit Measure (TPC-H Q9)              |             1766.16 |             1576.30 |               1054.60 |               1493.85 |
| Returned Item Reporting Query (TPC-H Q10)           |              707.92 |              712.54 |                842.14 |               1387.22 |
| Important Stock Identification (TPC-H Q11)          |              103.56 |              106.50 |                754.39 |                943.99 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             3069.94 |             2503.49 |                415.11 |               1042.15 |
| Customer Distribution (TPC-H Q13)                   |             2641.26 |             2416.61 |               1112.14 |               2175.47 |
| Promotion Effect Query (TPC-H Q14)                  |            10447.27 |             9623.03 |                300.90 |                659.25 |
| Top Supplier Query (TPC-H Q15)                      |             2441.82 |             1754.10 |                392.21 |                492.35 |
| Parts/Supplier Relationship (TPC-H Q16)             |              471.55 |              159.33 |                739.61 |                931.59 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               49.36 |               44.80 |                692.49 |               1094.92 |
| Large Volume Customer (TPC-H Q18)                   |             2500.83 |             2466.37 |                747.91 |               1088.62 |
| Discounted Revenue (TPC-H Q19)                      |               85.27 |               73.41 |                436.88 |                558.38 |
| Potential Part Promotion (TPC-H Q20)                |              215.13 |              169.96 |               1375.86 |               1140.60 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            51258.72 |            47935.68 |               1268.81 |               1891.17 |
| Global Sales Opportunity Query (TPC-H Q22)          |              126.85 |              180.47 |                384.89 |                685.14 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   |        93.59 |      2.38 |           1.68 |                  1.69 |
| mariadbcs-1-1-1-1 |        77.75 |      1.49 |           3.65 |                  4.28 |

### Loading phase: component data generator

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   | n/a          |      0.00 |           0.00 |                  0.00 |
| mariadbcs-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   | n/a          |      0.00 |           0.01 |                  0.01 |
| mariadbcs-1-1-1-1 | 1.07         |      0.02 |           0.01 |                  0.73 |

### Benchmarking phase: SUT deployment

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   | 87.10        |      1.00 |           2.04 |                  2.05 |
| mariadb-1-2-1-1   | 72.30        |      1.00 |           1.88 |                  1.88 |
| mariadbcs-1-1-1-1 | n/a          |      0.17 |           5.20 |                  5.90 |
| mariadbcs-1-2-1-1 | n/a          |      2.17 |           4.28 |                  4.47 |

### Benchmarking phase: component benchmarker

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   | 11.46        |      0.35 |           0.30 |                  0.30 |
| mariadb-1-2-1-1   | 15.37        |      0.10 |           0.32 |                  0.32 |
| mariadbcs-1-1-1-1 | n/a          |      0.00 |           0.35 |                  0.35 |
| mariadbcs-1-2-1-1 | n/a          |      0.41 |           0.32 |                  0.32 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-2-1-1 (bexhoma-metrics-mariadb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-2-1-1 (bexhoma-metrics-mariadb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
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

To see the summary again you can simply call `bexhoma summary -e <code>` with the experiment code.

### Compare Results

`-xdt` stores the result sets per connection, and the test `SQL warnings` compares those of all connections of the experiment.
So a run with MariaDB and MariaDBCS together shows if ColumnStore returns the same rows.
Row counts of the check scripts are worth a look too, in the file `bexhoma-loading-mariadbcs-1-checkschema-*.stdout.log` of the result folder.

At SF 1 all queries of TPC-H and SSB, normal and flat, gave the same results on both, and 98 of the 99 queries of TPC-DS.
For 30 queries of TPC-DS this needs a variant of the query, see below.

### Detailed Evaluation

Results are transformed into pandas DataFrames and can be inspected in detail.
See for example
* [Jupyter Notebooks](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/evaluator_dbmsbenchmarker/notebooks/)

You can connect to an evaluation server locally by `bexhoma jupyter`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888


## Loading

MariaDBCS uses the loader images of MariaDB: the loader pod sends the data with `LOAD DATA LOCAL`, and the server passes it on to `cpimport`.

It always runs with one loader pod.
Concurrent `LOAD DATA` into one table fail with `ERROR 1030 ... from storage engine ColumnStore`, and the loader script goes on, so rows would be missing without any test failing.

`mariadbd` parses the data on one core, which limits the speed.
`cpimport` run directly in the SUT is much faster, but only works as a pull: the SUT would read the raw files itself, which is a different path than the sending loader pods of the other DBMS and not comparable.
See [DBMS](DBMS.html#mariadb-columnstore) for the numbers.


## Perform TPC-DS Benchmark

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
  run &>$LOG_DIR/docs_tpcds_mariadbcs_1.log
```

All 99 queries of TPC-DS run on ColumnStore, 30 of them with a variant named `MariaDBCS`:

* 19 queries are refused by ColumnStore as they are, for example because it has no `INTERSECT` and no `EXCEPT`.
* 11 queries would crash ColumnStore 25.10.6 or return wrong rows without an error.

The test `SQL warnings` fails in this run because of Q33: the sums of all groups are the same on both, but on MariaDB `ORDER BY total_sales` means an inner column, so `LIMIT 100` cuts one other row.

See [TPC-DS queries](Queries-TPC-DS.html) for the rewrites and [DBMS](DBMS.html#mariadb-columnstore) for the reasons.

The RAM limit is 32 GiB here, since memory depends on the number of cores of the node: ColumnStore starts threads per core.
16 GiB are enough on nodes with 96 or 128 cores, but on a node with 224 cores the SUT was killed at that limit.

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_mariadbcs_1_summary.md" target="_blank" rel="noopener">docs_tpcds_mariadbcs_1.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 1661s 
* Code: 1793491593
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1800. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.11.
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
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:669958
  * datadisk:4582
  * volume_size:30G
  * volume_used:4.5G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:32Gi
  * limits_memory:32Gi
  * resources_total: 4.0 CPU, 32.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 32.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793491593
* mariadb-1-2-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:670525
  * datadisk:4583
  * volume_size:30G
  * volume_used:4.5G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:32Gi
  * limits_memory:32Gi
  * resources_total: 4.0 CPU, 32.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 32.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793491593
* mariadbcs-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:668393
  * datadisk:579
  * volume_size:30G
  * volume_used:740M
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:32Gi
  * limits_memory:32Gi
  * resources_total: 4.0 CPU, 32.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 32.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793491593
* mariadbcs-1-2-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:669961
  * datadisk:579
  * volume_size:30G
  * volume_used:740M
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:32Gi
  * limits_memory:32Gi
  * resources_total: 4.0 CPU, 32.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 32.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793491593

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MariaDB-1-2, MariaDBCS-1-2

### Data Parameters of Reused Volumes
* MariaDB-1: DDL values of the volume: histograms=off
* MariaDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics
* MariaDBCS-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1793491593-db65856ff-cwr6x: 0
* bexhoma-sut-mariadb-1-1793491593-86cbdb5855-7px2t: 0
* bexhoma-sut-mariadbcs-1-1793491593-7c8955767f-zb7z2: 0
* bexhoma-sut-mariadbcs-1-1793491593-59b479fbf4-r9mk7: 0

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
| MariaDB-1-1   |                1 |    1 |      224.00 |           3.00 |            0.00 |         96.00 |          124.00 |              1 |           0 |             | None           |             0 | False         |               16.07 | False               |
| MariaDB-1-2   |                2 |    1 |      224.00 |           3.00 |            0.00 |         96.00 |          124.00 |              1 |           0 |             | None           |             0 | False         |               16.07 | True                |
| MariaDBCS-1-1 |                1 |    1 |      171.00 |          20.00 |            0.00 |        110.00 |           38.00 |              1 |           0 |             | None           |             0 | False         |               21.05 | False               |
| MariaDBCS-1-2 |                2 |    1 |      171.00 |          20.00 |            0.00 |        110.00 |           38.00 |              1 |           0 |             | None           |             0 | False         |               21.05 | True                |

### Benchmarking

#### Per Connection

| DBMS                | configuration   | phase           | job               |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                 |
|:--------------------|:----------------|:----------------|:------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:--------------------|
| mariadb-1-1-1-1-1   | MariaDB-1       | mariadb-1-1-1   | mariadb-1-1-1-1   |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        361 |            0.81 |             4457.06 |            987.26 |          -1 | mariadb-1-1-1-1-1   |
| mariadb-1-2-1-1-1   | MariaDB-1       | mariadb-1-2-1   | mariadb-1-2-1-1   |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        329 |            0.71 |             5064.35 |           1083.28 |          -1 | mariadb-1-2-1-1-1   |
| mariadbcs-1-1-1-1-1 | MariaDBCS-1     | mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        191 |            0.86 |             4177.89 |           1865.97 |          -1 | mariadbcs-1-1-1-1-1 |
| mariadbcs-1-2-1-1-1 | MariaDBCS-1     | mariadbcs-1-2-1 | mariadbcs-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        135 |            0.86 |             4191.89 |           2640.00 |          -1 | mariadbcs-1-2-1-1-1 |

#### Per Phase

|                 | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1   | mariadb-1-1-1   |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        361 |            0.81 |             4457.06 |            987.26 |          -1 |
| mariadb-1-2-1   | mariadb-1-2-1   |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        329 |            0.71 |             5064.35 |           1083.28 |          -1 |
| mariadbcs-1-1-1 | mariadbcs-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        191 |            0.86 |             4177.89 |           1865.97 |          -1 |
| mariadbcs-1-2-1 | mariadbcs-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        135 |            0.86 |             4191.89 |           2640.00 |          -1 |

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
| mariadb-1-1-1   | mariadb-1-1-1-1   |                1 |        1 |               1 |         5.00 |                |
| mariadb-1-2-1   | mariadb-1-2-1-1   |                2 |        1 |               1 |         5.00 |                |
| mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |        14.00 |                |
| mariadbcs-1-2-1 | mariadbcs-1-2-1-1 |                2 |        1 |               1 |        16.00 |                |

### Latency of Timer Execution [ms]
| Queries       |   mariadb-1-1-1-1-1 |   mariadb-1-2-1-1-1 |   mariadbcs-1-1-1-1-1 |   mariadbcs-1-2-1-1-1 |
|:--------------|--------------------:|--------------------:|----------------------:|----------------------:|
| TPC-DS Q1     |                7.80 |               11.29 |               2140.50 |               2248.36 |
| TPC-DS Q2     |             4210.45 |             4045.53 |               3160.66 |               2780.29 |
| TPC-DS Q3     |                6.02 |              126.76 |               1198.57 |               1444.68 |
| TPC-DS Q4     |            10234.37 |             9366.39 |               1603.55 |               1524.93 |
| TPC-DS Q5     |             8434.43 |             7499.46 |               4674.08 |               3954.73 |
| TPC-DS Q6     |             1161.67 |              587.42 |               1198.57 |               1178.53 |
| TPC-DS Q7     |             3243.62 |             9226.52 |               2121.16 |               1980.66 |
| TPC-DS Q8     |              308.42 |              249.66 |                667.62 |                628.78 |
| TPC-DS Q9     |             4081.96 |             3761.25 |                414.42 |                286.33 |
| TPC-DS Q10    |               86.14 |               68.05 |                752.13 |                958.73 |
| TPC-DS Q11    |             7135.07 |             7104.86 |               1028.58 |               1000.69 |
| TPC-DS Q12    |              284.89 |              187.97 |                597.36 |                532.95 |
| TPC-DS Q13    |              897.10 |              680.93 |               1425.67 |               1597.19 |
| TPC-DS Q14a+b |            48403.13 |            42567.54 |               5690.58 |               5400.66 |
| TPC-DS Q15    |              129.80 |              115.35 |                685.77 |                648.88 |
| TPC-DS Q16    |             8025.39 |             7150.09 |                652.66 |                717.19 |
| TPC-DS Q17    |              585.98 |              520.22 |               1407.62 |               1309.36 |
| TPC-DS Q18    |             1829.73 |             1592.24 |               1476.71 |               1405.60 |
| TPC-DS Q19    |              200.92 |              427.90 |               1024.85 |                816.95 |
| TPC-DS Q20    |              387.07 |              344.27 |                685.44 |                444.18 |
| TPC-DS Q21    |             3974.51 |             2148.13 |               1400.10 |               1938.98 |
| TPC-DS Q22    |             9179.48 |            22049.74 |               1133.49 |               1294.31 |
| TPC-DS Q23a+b |            46180.34 |            42878.79 |               3430.52 |               3035.66 |
| TPC-DS Q24a+b |               22.29 |               22.18 |               1435.80 |               1278.80 |
| TPC-DS Q25    |              136.40 |              135.57 |               1013.02 |               1426.87 |
| TPC-DS Q26    |             1130.26 |              652.02 |                859.75 |                733.70 |
| TPC-DS Q27    |             3005.67 |             2631.04 |               1221.73 |                956.44 |
| TPC-DS Q28    |             2923.36 |             2555.29 |                309.73 |                409.29 |
| TPC-DS Q29    |               82.96 |               67.86 |               1201.69 |               1331.50 |
| TPC-DS Q30    |               81.67 |               76.95 |                862.75 |                900.70 |
| TPC-DS Q31    |             1055.23 |             1071.13 |               1037.36 |               1215.96 |
| TPC-DS Q32    |               10.20 |                5.27 |                911.81 |                537.82 |
| TPC-DS Q33    |              460.44 |              117.26 |                770.58 |                808.65 |
| TPC-DS Q34    |             3284.84 |             2487.78 |                259.47 |                258.47 |
| TPC-DS Q35    |              979.03 |             1000.48 |                672.07 |                700.99 |
| TPC-DS Q36    |             2397.54 |             2148.39 |                596.40 |                657.09 |
| TPC-DS Q37    |             4052.32 |             3223.43 |                351.99 |                487.08 |
| TPC-DS Q38    |             6812.18 |             5536.44 |                801.56 |                703.48 |
| TPC-DS Q39a+b |             1107.81 |             1055.70 |               1767.23 |               1651.23 |
| TPC-DS Q40    |              552.91 |              141.97 |               1092.46 |                850.29 |
| TPC-DS Q41    |              399.81 |              351.53 |                370.12 |                343.88 |
| TPC-DS Q42    |              222.39 |              162.10 |                427.13 |                426.81 |
| TPC-DS Q43    |              820.60 |              930.28 |                301.78 |                268.44 |
| TPC-DS Q44    |                1.34 |                1.94 |                334.21 |                331.14 |
| TPC-DS Q45    |              108.49 |              181.20 |                515.70 |                539.97 |
| TPC-DS Q46    |             3310.38 |             3023.87 |                302.38 |                369.80 |
| TPC-DS Q47    |            13630.66 |            13330.59 |               1377.28 |               1215.36 |
| TPC-DS Q48    |              903.12 |              867.39 |                841.17 |                827.37 |
| TPC-DS Q49    |               98.93 |               91.76 |                672.84 |                655.08 |
| TPC-DS Q50    |               65.90 |               22.40 |                686.95 |                756.77 |
| TPC-DS Q51    |             6917.41 |             6916.95 |               2059.40 |               1849.04 |
| TPC-DS Q52    |              204.68 |              163.91 |                455.81 |                446.26 |
| TPC-DS Q53    |              124.96 |               95.87 |                622.50 |                669.26 |
| TPC-DS Q54    |              948.80 |              918.25 |                639.13 |                595.46 |
| TPC-DS Q55    |              213.63 |              166.66 |                430.40 |                437.67 |
| TPC-DS Q56    |              142.42 |              121.32 |                928.48 |                972.95 |
| TPC-DS Q57    |             4900.90 |             4648.30 |                924.97 |               1122.00 |
| TPC-DS Q58    |             5219.11 |             4582.37 |                932.87 |                783.84 |
| TPC-DS Q59    |             7938.60 |             7025.93 |               1345.55 |                988.67 |
| TPC-DS Q60    |              546.95 |              479.61 |               1036.27 |                978.46 |
| TPC-DS Q61    |              288.87 |              252.30 |                230.61 |                262.74 |
| TPC-DS Q62    |             1661.51 |             1290.99 |               1178.64 |               1030.62 |
| TPC-DS Q63    |              115.42 |              102.48 |                531.83 |                530.87 |
| TPC-DS Q64    |              572.75 |              445.36 |               3072.96 |               3450.59 |
| TPC-DS Q65    |             6078.83 |             4611.30 |                630.94 |                638.04 |
| TPC-DS Q66    |             1340.08 |              977.29 |               1240.37 |               1177.22 |
| TPC-DS Q67    |             6346.71 |             5448.04 |               3332.29 |               2811.09 |
| TPC-DS Q68    |             2782.26 |             2614.16 |                330.00 |                298.15 |
| TPC-DS Q69    |              310.28 |              296.53 |                931.83 |                930.14 |
| TPC-DS Q70    |             7630.35 |             6287.73 |                985.95 |               1032.10 |
| TPC-DS Q71    |              398.94 |              343.30 |                425.66 |                485.06 |
| TPC-DS Q72    |             1163.08 |              635.70 |               1345.24 |               1346.23 |
| TPC-DS Q73    |             2383.20 |             2291.33 |                346.92 |                244.59 |
| TPC-DS Q74    |             5441.24 |             4381.35 |                878.93 |                922.78 |
| TPC-DS Q75    |             4745.16 |             4113.66 |               1205.45 |               1288.34 |
| TPC-DS Q76    |              833.66 |              618.38 |                501.82 |                685.09 |
| TPC-DS Q77    |             6359.65 |             4831.07 |               1046.35 |               1005.64 |
| TPC-DS Q78    |             5043.77 |             4402.88 |               1612.30 |               1778.79 |
| TPC-DS Q79    |             3452.59 |             2692.47 |                859.67 |                804.41 |
| TPC-DS Q80    |              498.11 |              486.60 |               1122.36 |               1144.77 |
| TPC-DS Q81    |              225.42 |              172.83 |                897.61 |                856.10 |
| TPC-DS Q82    |             3641.08 |             3018.67 |                742.61 |                836.96 |
| TPC-DS Q83    |              951.80 |             1089.77 |                733.01 |                719.76 |
| TPC-DS Q84    |               52.18 |               38.64 |                594.60 |                608.23 |
| TPC-DS Q85    |              121.74 |               95.66 |               2450.60 |               2513.66 |
| TPC-DS Q86    |              725.87 |              619.49 |                468.27 |                520.74 |
| TPC-DS Q87    |             7112.84 |             5523.84 |                646.71 |                671.07 |
| TPC-DS Q88    |            11892.37 |             9835.96 |               1206.42 |               1249.03 |
| TPC-DS Q89    |             1193.88 |              988.00 |                679.06 |                544.93 |
| TPC-DS Q90    |              333.48 |              122.64 |                423.78 |                456.18 |
| TPC-DS Q91    |               20.13 |               14.15 |                796.09 |               1219.43 |
| TPC-DS Q92    |                5.49 |                6.26 |                434.24 |                492.77 |
| TPC-DS Q93    |               45.96 |               38.23 |                468.97 |                476.56 |
| TPC-DS Q94    |              734.40 |              363.38 |               1362.14 |                847.26 |
| TPC-DS Q95    |              682.03 |              663.40 |               1050.58 |               1037.88 |
| TPC-DS Q96    |              662.27 |              818.38 |                427.09 |                455.76 |
| TPC-DS Q97    |             4926.07 |             4413.00 |                570.17 |                671.09 |
| TPC-DS Q98    |              879.53 |              770.80 |                507.33 |                978.12 |
| TPC-DS Q99    |             2745.82 |             2795.67 |               1110.58 |                978.89 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

|                     |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:--------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| mariadb-1-1-1-1-1   |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| mariadb-1-2-1-1-1   |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| mariadbcs-1-1-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   |       211.73 |      1.17 |           4.08 |                  4.19 |
| mariadbcs-1-1-1-1 |       154.41 |      1.35 |           9.40 |                 10.16 |

### Loading phase: component data generator

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   | n/a          |      0.00 |           0.00 |                  0.00 |
| mariadbcs-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   |         1.11 |      0.02 |           0.00 |                  0.00 |
| mariadbcs-1-1-1-1 |         1.12 |      0.01 |           0.01 |                  0.01 |

### Benchmarking phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   |       297.09 |      1.00 |           4.48 |                  4.49 |
| mariadb-1-2-1-1   |       281.56 |      1.00 |           2.77 |                  2.77 |
| mariadbcs-1-1-1-1 |       704.24 |      8.16 |          16.45 |                 17.22 |
| mariadbcs-1-2-1-1 |       895.36 |     14.54 |          11.72 |                 11.92 |

### Benchmarking phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   |        13.16 |      0.30 |           0.32 |                  0.32 |
| mariadb-1-2-1-1   |        12.90 |      0.02 |           0.29 |                  0.30 |
| mariadbcs-1-1-1-1 |        12.86 |      0.03 |           0.30 |                  0.30 |
| mariadbcs-1-2-1-1 |        13.88 |      0.30 |           0.32 |                  0.32 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
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
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: series exists only while non-zero)
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
* TEST failed: SQL warnings (result mismatch)
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
* TEST passed: Reset scripts ran without errors
```

</details>


## Perform SSB Benchmark

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
  run &>$LOG_DIR/docs_ssb_mariadbcs_1.log
```

This runs the 13 queries of the star schema benchmark, see [Example: SSB](Example-SSB.md).

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ssb_mariadbcs_1_summary.md" target="_blank" rel="noopener">docs_ssb_mariadbcs_1.log</a></summary>

```markdown
## Show Summary

### Workload
SSB Queries SF=1
* Type: ssb
* Duration: 568s 
* Code: 1793490780
* This includes the 13 queries of the Star Schema Benchmark (O'Neil et al., revision 3, 2009) with the constants of the specification (Q2.3: brand 'MFGR#2239', as used by ClickHouse and Doris; the specification's text and SQL disagree there).
* This experiment compares run time and resource consumption of SSB queries in different DBMS.
  * Schema is the star schema (-xsv normal).
  * SSB (SF=1) data is loaded and benchmark is executed.
  * Queries use the constants of the specification (-xqv spec).
  * Query ordering is Q1.1 - Q4.3.
  * Timeout per query is 1800. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Import sets statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.11.
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
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:554974
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
    * code:1793490780
* mariadbcs-1-2-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:669596
  * datadisk:298
  * volume_size:20G
  * volume_used:459M
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793490780

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MariaDBCS-1-2

### Data Parameters of Reused Volumes
* MariaDBCS-1: loading values of the volume: script=Schema, indexing=Statistics

### SUT Container Restarts
* bexhoma-sut-mariadbcs-1-1793490780-5675cc657d-7jgdw: 0
* bexhoma-sut-mariadbcs-1-1793490780-58974d5579-qsjl2: 0

### Workflow

#### Actual

* DBMS MariaDBCS-1 - Experiment 1 Client 1: ssb (1 pods)
* DBMS MariaDBCS-1 - Experiment 2 Client 1: ssb (1 pods)

#### Planned

* DBMS MariaDBCS-1 - Experiment 1 Client 1: ssb (1 pods)
* DBMS MariaDBCS-1 - Experiment 2 Client 1: ssb (1 pods)

### Loading

#### Per Run

|               |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:--------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDBCS-1-1 |                1 |    1 |       56.00 |           9.00 |            0.00 |         32.00 |           14.00 |              1 |           0 |             | None           |             0 | False         |               64.29 | False               |
| MariaDBCS-1-2 |                2 |    1 |       56.00 |           9.00 |            0.00 |         32.00 |           14.00 |              1 |           0 |             | None           |             0 | False         |               64.29 | True                |

### Benchmarking

#### Per Connection

| DBMS                | configuration   | phase           | job               |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                 |
|:--------------------|:----------------|:----------------|:------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:--------------------|
| mariadbcs-1-1-1-1-1 | MariaDBCS-1     | mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |         14 |            0.73 |             4950.02 |           3342.86 |          -1 | mariadbcs-1-1-1-1-1 |
| mariadbcs-1-2-1-1-1 | MariaDBCS-1     | mariadbcs-1-2-1 | mariadbcs-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               13 |                  13 |         10 |            0.62 |             5772.08 |           4680.00 |          -1 | mariadbcs-1-2-1-1-1 |

#### Per Phase

|                 | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadbcs-1-1-1 | mariadbcs-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |         14 |            0.73 |             4950.02 |           3342.86 |          -1 |
| mariadbcs-1-2-1 | mariadbcs-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               13 |                  13 |         10 |            0.62 |             5772.08 |           4680.00 |          -1 |

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
| mariadbcs-1-2-1 | mariadbcs-1-2-1-1 |                2 |        1 |               1 |         5.00 |                |

### Latency of Timer Execution [ms]
| Queries                                                                                |   mariadbcs-1-1-1-1-1 |   mariadbcs-1-2-1-1-1 |
|:---------------------------------------------------------------------------------------|----------------------:|----------------------:|
| Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)                 |               1455.77 |               1223.73 |
| Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)                |                205.42 |                202.91 |
| Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)                 |                223.41 |                179.85 |
| Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)  |               1769.19 |               1347.91 |
| Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)       |                859.46 |                720.11 |
| Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)                     |                649.89 |                599.59 |
| Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)      |               1161.46 |                965.23 |
| Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)        |                769.36 |                671.52 |
| Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)         |                669.34 |                569.24 |
| Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)     |                609.13 |                583.55 |
| Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1) |                885.06 |                721.61 |
| Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)            |                843.58 |                747.86 |
| Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)     |                886.69 |                715.51 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadbcs-1-1-1-1 |        66.74 |      1.69 |           1.92 |                  2.20 |

### Loading phase: component data generator

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadbcs-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadbcs-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: SUT deployment

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadbcs-1-1-1-1 | n/a          |      0.02 |           3.19 |                  3.68 |
| mariadbcs-1-2-1-1 | n/a          |      0.10 |           0.30 |                  0.49 |

### Benchmarking phase: component benchmarker

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadbcs-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| mariadbcs-1-2-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |

### Missing Monitoring Metrics
* Memory Usage incl. Page Cache [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Memory Usage, Working Set [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Utilization [CPUs] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU System Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU User Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Network Rx Total [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Network Tx Total [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage incl. Page Cache [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Memory Usage incl. Page Cache [MiB] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Memory Usage, Working Set [MiB] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttled Time [s] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization Time [s] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU User Time [s] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU System Time [s] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Network Tx Total [MiB] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Network Rx Total [MiB] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
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
  run &>$LOG_DIR/docs_ssb_mariadbcs_2.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ssb_mariadbcs_2_summary.md" target="_blank" rel="noopener">docs_ssb_mariadbcs_2.log</a></summary>

```markdown
## Show Summary

### Workload
SSB Queries SF=1
* Type: ssb
* Duration: 540s 
* Code: 1793491402
* This includes the 13 queries of the Star Schema Benchmark (O'Neil et al., revision 3, 2009) with the constants of the specification (Q2.3: brand 'MFGR#2239', as used by ClickHouse and Doris; the specification's text and SQL disagree there). The queries read the denormalized table lineorder_flat; year, month and week come from lo_orderdate.
* This experiment compares run time and resource consumption of SSB queries in different DBMS.
  * Schema is the flat table lineorder_flat (-xsv flat).
  * SSB (SF=1) data is loaded and benchmark is executed.
  * Queries use the constants of the specification (-xqv spec).
  * Query ordering is Q1.1 - Q4.3.
  * Timeout per query is 1800. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Import sets statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.11.
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
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:669929
  * datadisk:797
  * volume_size:20G
  * volume_used:959M
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793491402
* mariadbcs-1-2-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:670149
  * datadisk:797
  * volume_size:20G
  * volume_used:959M
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793491402

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MariaDBCS-1-2

### Data Parameters of Reused Volumes
* MariaDBCS-1: loading values of the volume: script=Schema_flat, indexing=Statistics_flat

### SUT Container Restarts
* bexhoma-sut-mariadbcs-1-1793491402-66d9b795c4-sth5z: 0
* bexhoma-sut-mariadbcs-1-1793491402-697cb9f897-f5287: 0

### Workflow

#### Actual

* DBMS MariaDBCS-1 - Experiment 1 Client 1: ssb (1 pods)
* DBMS MariaDBCS-1 - Experiment 2 Client 1: ssb (1 pods)

#### Planned

* DBMS MariaDBCS-1 - Experiment 1 Client 1: ssb (1 pods)
* DBMS MariaDBCS-1 - Experiment 2 Client 1: ssb (1 pods)

### Loading

#### Per Run

|               |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:--------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDBCS-1-1 |                1 |    1 |       61.00 |           3.00 |            0.00 |         51.00 |            5.00 |              1 |           0 |             | None           |             0 | False         |               59.02 | False               |
| MariaDBCS-1-2 |                2 |    1 |       61.00 |           3.00 |            0.00 |         51.00 |            5.00 |              1 |           0 |             | None           |             0 | False         |               59.02 | True                |

### Benchmarking

#### Per Connection

| DBMS                | configuration   | phase           | job               |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                 |
|:--------------------|:----------------|:----------------|:------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:--------------------|
| mariadbcs-1-1-1-1-1 | MariaDBCS-1     | mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |         10 |            0.25 |            14473.89 |           4680.00 |          -1 | mariadbcs-1-1-1-1-1 |
| mariadbcs-1-2-1-1-1 | MariaDBCS-1     | mariadbcs-1-2-1 | mariadbcs-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          9 |            0.28 |            12707.34 |           5200.00 |          -1 | mariadbcs-1-2-1-1-1 |

#### Per Phase

|                 | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadbcs-1-1-1 | mariadbcs-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |         10 |            0.25 |            14473.89 |           4680.00 |          -1 |
| mariadbcs-1-2-1 | mariadbcs-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          9 |            0.28 |            12707.34 |           5200.00 |          -1 |

#### Query Completion per Phase

| phase           |   pods | Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)   | Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)   | Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)   | Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)   | Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)   | Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)   | Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)   | Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)   | Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)   | Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)   | Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1)   | Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)   | Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)   | complete   |
|:----------------|-------:|:-------------------------------------------------------------------------|:--------------------------------------------------------------------------|:-------------------------------------------------------------------------|:----------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|:---------------------------------------------------------------------|:------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|:---------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------|:------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------|
| mariadbcs-1-1-1 |      1 | 1/1                                                                      | 1/1                                                                       | 1/1                                                                      | 1/1                                                                                     | 1/1                                                                                | 1/1                                                                  | 1/1                                                                                 | 1/1                                                                               | 1/1                                                                              | 1/1                                                                                  | 1/1                                                                                      | 1/1                                                                           | 1/1                                                                                  | yes        |
| mariadbcs-1-2-1 |      1 | 1/1                                                                      | 1/1                                                                       | 1/1                                                                      | 1/1                                                                                     | 1/1                                                                                | 1/1                                                                  | 1/1                                                                                 | 1/1                                                                               | 1/1                                                                              | 1/1                                                                                  | 1/1                                                                                      | 1/1                                                                           | 1/1                                                                                  | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

#### Reset

| phase           | job               |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:----------------|:------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |         1.00 |                |
| mariadbcs-1-2-1 | mariadbcs-1-2-1-1 |                2 |        1 |               1 |         1.00 |                |

### Latency of Timer Execution [ms]
| Queries                                                                                |   mariadbcs-1-1-1-1-1 |   mariadbcs-1-2-1-1-1 |
|:---------------------------------------------------------------------------------------|----------------------:|----------------------:|
| Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)                 |                632.72 |                628.96 |
| Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)                |                 27.96 |                 17.88 |
| Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)                 |                 17.41 |                 35.57 |
| Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)  |                509.10 |                623.35 |
| Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)       |                522.34 |                741.88 |
| Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)                     |                370.28 |                422.51 |
| Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)      |                536.17 |                555.79 |
| Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)        |                521.72 |                562.26 |
| Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)         |                170.35 |                205.73 |
| Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)     |                 90.67 |                 89.04 |
| Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1) |                515.32 |                554.63 |
| Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)            |                383.37 |                379.24 |
| Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)     |                538.53 |                804.75 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadbcs-1-1-1-1 |        98.19 |      2.04 |           2.15 |                  3.03 |

### Loading phase: component data generator

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadbcs-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadbcs-1-1-1-1 |         1.55 |      0.03 |           0.00 |                  0.00 |

### Benchmarking phase: SUT deployment

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadbcs-1-1-1-1 | n/a          |      0.07 |           3.65 |                  4.62 |
| mariadbcs-1-2-1-1 | n/a          |      1.17 |           1.72 |                  1.91 |

### Benchmarking phase: component benchmarker

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadbcs-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| mariadbcs-1-2-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Memory Usage incl. Page Cache [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Memory Usage, Working Set [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Utilization [CPUs] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU User Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU System Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Utilization Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Network Tx Total [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Network Rx Total [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage incl. Page Cache [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Memory Usage incl. Page Cache [MiB] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Utilization [CPUs] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization Time [s] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU User Time [s] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU System Time [s] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttled Time [s] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* Network Rx Total [MiB] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* Network Tx Total [MiB] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
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


## Monitoring

[Monitoring](Monitoring.html) can be activated for the DBMS only (`-m`) or for all components (`-mc`).
ColumnStore has no Prometheus exporter in bexhoma, so there are no application metrics (`-ma`).
