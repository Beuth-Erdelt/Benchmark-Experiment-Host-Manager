# Benchmark: TPC-DS

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

TPC-DS does allow scaling data generation and ingestion, and scaling the benchmarking driver.
Scale-out can simulate distributed clients for the loading test and the throughput test [2].

This example shows how to benchmark 99 reading queries Q1-Q99 derived from TPC-DS in PostgreSQL.

> The query file is derived from the TPC-DS and as such is not comparable to published TPC-DS results, as the query file results do not comply with the TPC-DS Specification.

In particular we had to apply changes to the queries, because
* MySQL and MariaDB do not have a FULL OUTER JOIN (Q51, Q97, ...)
* MySQL and MariaDB do CASTing to INTEGER differently
* column names may differ if AS is not used
* MariaDB does not know GROUPING
* the DBMS do not sort in the same way when NULL comes into play

See [query file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/experiments/tpcds/queries-tpcds.config) for all details.

The schema of
* MonetDB: sets primary keys and foreign key constraints after import and no other indexes
* MySQL: sets primary keys before import, all foreign key constraints and indexes on foreign keys of fact tables and customer table after import
* MariaDB: sets primary keys before import, all foreign key constraints and indexes on foreign keys of fact tables and customer table after import
* PostgreSQL: sets primary keys before import, all foreign key constraints and indexes on foreign keys of fact tables and customer table after import

**MySQL is excluded currently because the treatment of NULL during INSERT is complicated.**



**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

For a comparison of multiple DBMS (PostgreSQL, MonetDB, MySQL, MariaDB) see [TestCases.md](TestCases.md#tpc-ds).

1. Official TPC-DS benchmark - http://www.tpc.org/tpcds
1. A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools: https://doi.org/10.1007/978-3-031-68031-1_9

## Perform Benchmark - Power Test

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

For performing the experiment we can run the [tpcds file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpcds.py).

Example:
```bash
bexhoma tpcds \
  -dbms PostgreSQL \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_postgresql.log
```

This
* starts a clean instance of PostgreSQL
  * fixed 64 Gi RAM (request `-rr` and limit `-lr`)
  * data directory inside a Docker container
* creates TPC-DS schema in the database
* starts 8 loader pods (`-nlp`)
  * with a data generator (init) container each
    * generating a portion of TPC-DS data of scaling factor 1 (`-sf`)
    * storing the data in a distributed filesystem (shared disk)
    * if data is already present: do nothing
  * with a loading container each
    * importing TPC-DS data from the distributed filesystem
    * loading uses 8 threads (`-nlt`)
* creates constraints (`-xic`) and indexes (`-xii`) and updates table statistics (`-xis`) after ingestion
* runs 1 stream of TPC-DS queries
  * data transfer is also measured (`-xdt`)
* shows a summary


### Status

You can watch the status while benchmark is running via `bexhoma status`

```bash
Dashboard: Running
Cluster Prometheus: Running
Message Queue: Running
Data directory: Running
Result directory: Running
+------------------+--------------+--------------+---------------+
| 1706255897       | sut          |   loaded [s] | loading       |
+==================+==============+==============+===============+
| MonetDB-BHT-8    | (1. Running) |       253.23 |               |
+------------------+--------------+--------------+---------------+
| MySQL-BHT-8-8    | (1. Running) |         0.61 | (8 Succeeded) |
+------------------+--------------+--------------+---------------+
| PostgreSQL-BHT-8 | (1. Running) |       219.08 |               |
+------------------+--------------+--------------+---------------+
```

The code `1706255897` is the unique identifier of the experiment.
You can find the number also in the output of `tpcds.py`.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1706255897` (removes everything that is related to experiment `1706255897`).

## Evaluate Results

At the end of a benchmark you will see a summary like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_postgresql_summary.md" target="_blank" rel="noopener">docs_tpcds_postgresql.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 644s 
* Code: 1792706072
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.8.
  * Experiment is limited to DBMS ['PostgreSQL'].
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'random_page_cost'}, '1.1'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_io_concurrency'}, '200'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'io_method'}, 'io_uring'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers_per_gather'}, '2'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers'}, '4'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_worker_processes'}, '6'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'shared_buffers'}, '20GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_cache_size'}, '48GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'work_mem'}, '1GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'maintenance_work_mem'}, '2GB')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:925980
  * datadisk:5790
  * volume_size:1.8T
  * volume_used:905G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792706072

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1792706072-65d8959f68-cgqvs: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    1 |      111.00 |           7.00 |            1.00 |         48.00 |           46.00 |              8 |           0 |             | None           |             0 | False         |               32.43 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        139 |            0.29 |            12895.84 |           2564.03 |          -1 | postgresql-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        139 |            0.29 |            12895.84 |           2564.03 |          -1 |

#### Query Completion per Phase

| phase            |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:-----------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   postgresql-1-1-1-1-1 |
|:--------------|-----------------------:|
| TPC-DS Q1     |                  88.28 |
| TPC-DS Q2     |                 340.51 |
| TPC-DS Q3     |                 107.24 |
| TPC-DS Q4     |                5467.84 |
| TPC-DS Q5     |                 460.07 |
| TPC-DS Q6     |               48918.24 |
| TPC-DS Q7     |                 332.60 |
| TPC-DS Q8     |                  47.66 |
| TPC-DS Q9     |                1790.64 |
| TPC-DS Q10    |                 864.76 |
| TPC-DS Q11    |                3085.13 |
| TPC-DS Q12    |                  55.09 |
| TPC-DS Q13    |                 480.44 |
| TPC-DS Q14a+b |                2093.20 |
| TPC-DS Q15    |                  95.99 |
| TPC-DS Q16    |                 193.63 |
| TPC-DS Q17    |                 251.80 |
| TPC-DS Q18    |                 328.83 |
| TPC-DS Q19    |                 123.08 |
| TPC-DS Q20    |                  80.23 |
| TPC-DS Q21    |                 238.83 |
| TPC-DS Q22    |                2626.50 |
| TPC-DS Q23a+b |                3478.71 |
| TPC-DS Q24a+b |                  99.43 |
| TPC-DS Q25    |                 244.57 |
| TPC-DS Q26    |                 176.93 |
| TPC-DS Q27    |                  38.81 |
| TPC-DS Q28    |                1306.78 |
| TPC-DS Q29    |                 280.61 |
| TPC-DS Q30    |                7554.42 |
| TPC-DS Q31    |                1284.91 |
| TPC-DS Q32    |                 191.26 |
| TPC-DS Q33    |                 304.13 |
| TPC-DS Q34    |                  16.74 |
| TPC-DS Q35    |                 943.19 |
| TPC-DS Q36    |                  17.30 |
| TPC-DS Q37    |                 319.06 |
| TPC-DS Q38    |                1037.58 |
| TPC-DS Q39a+b |                1966.76 |
| TPC-DS Q40    |                 112.82 |
| TPC-DS Q41    |                 747.59 |
| TPC-DS Q42    |                  88.22 |
| TPC-DS Q43    |                  18.68 |
| TPC-DS Q44    |                 382.89 |
| TPC-DS Q45    |                  73.83 |
| TPC-DS Q46    |                  23.40 |
| TPC-DS Q47    |                1082.10 |
| TPC-DS Q48    |                 471.26 |
| TPC-DS Q49    |                 423.42 |
| TPC-DS Q50    |                 371.05 |
| TPC-DS Q51    |                 689.56 |
| TPC-DS Q52    |                  83.89 |
| TPC-DS Q53    |                 104.79 |
| TPC-DS Q54    |                 240.11 |
| TPC-DS Q55    |                  79.91 |
| TPC-DS Q56    |                 317.23 |
| TPC-DS Q57    |                 678.38 |
| TPC-DS Q58    |                 297.73 |
| TPC-DS Q59    |                 414.16 |
| TPC-DS Q60    |                 299.59 |
| TPC-DS Q61    |                 105.49 |
| TPC-DS Q62    |                  94.48 |
| TPC-DS Q63    |                 108.41 |
| TPC-DS Q64    |                 585.76 |
| TPC-DS Q65    |                 487.11 |
| TPC-DS Q66    |                 169.35 |
| TPC-DS Q67    |                2084.54 |
| TPC-DS Q68    |                  29.90 |
| TPC-DS Q69    |                 252.22 |
| TPC-DS Q70    |                 327.57 |
| TPC-DS Q71    |                 230.42 |
| TPC-DS Q72    |                 762.51 |
| TPC-DS Q73    |                  19.18 |
| TPC-DS Q74    |                 821.89 |
| TPC-DS Q75    |                 569.80 |
| TPC-DS Q76    |                 135.02 |
| TPC-DS Q77    |                 268.52 |
| TPC-DS Q78    |                1054.83 |
| TPC-DS Q79    |                 102.90 |
| TPC-DS Q80    |                 354.11 |
| TPC-DS Q81    |                6077.83 |
| TPC-DS Q82    |                 346.84 |
| TPC-DS Q83    |                  64.56 |
| TPC-DS Q84    |                  17.23 |
| TPC-DS Q85    |                 258.96 |
| TPC-DS Q86    |                 176.41 |
| TPC-DS Q87    |                1053.92 |
| TPC-DS Q88    |                1927.63 |
| TPC-DS Q89    |                  16.95 |
| TPC-DS Q90    |                 101.42 |
| TPC-DS Q91    |                 118.69 |
| TPC-DS Q92    |                  45.67 |
| TPC-DS Q93    |                 242.92 |
| TPC-DS Q94    |                 125.16 |
| TPC-DS Q95    |                2497.27 |
| TPC-DS Q96    |                  94.55 |
| TPC-DS Q97    |                 324.61 |
| TPC-DS Q98    |                 134.87 |
| TPC-DS Q99    |                 158.17 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Loading measured in this experiment
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

This gives a survey about the errors and warnings (result set mismatch) and the latencies of execution per query.
Moreover the loading times (schema creation, ingestion and indexing), the geometric mean of query execution times and the TPC-DS metrics power and throughput are reported.
Please note that the results are not suitable for being published as official TPC-DS results.
In particular the refresh streams are missing.

To see the summary again you can simply call `bexhoma summary -e 1750150367` with the experiment code.

For a more detailed query-wise evaluation you can call `dbmsbenchmarker read -r ~/benchmarks/1750150367 -e yes`.

To inspect result sets you can call `python evaluate.py -r ~/benchmarks/ -e 1750150367 -q 4 resultsets` (here: for query 4).

To compare result sets you can call `dbmsinspect -r ~/benchmarks -c 1750150367 -q 4` (here: for query 4).
This shows the differences in result sets only.


### Detailed Evaluation

Results are transformed into pandas DataFrames and can be inspected in more detail.
Detailed evaluations can be done using DBMSBenchmarker
* [Dashboard](https://dbmsbenchmarker.readthedocs.io/en/latest/Dashboard.html)
* [Jupyter Notebooks](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/evaluator_dbmsbenchmarker/notebooks/)

You can connect to an evaluation server in the cluster by `bexhoma dashboard`.
This forwards ports, so you have
* a DBMSBenchmarker dashboard in browser at http://localhost:8050
* a Jupyter notebook server at http://localhost:8888 containing the example notebooks

You can connect to a local evaluation server by `bexhoma localdashboard`.
This forwards ports, so you have
* a DBMSBenchmarker dashboard in browser at http://localhost:8050

You can connect to a local jupyter server by `bexhoma jupyter`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888 containing the example notebooks


## Adjust Parameters

The script supports
* exact repetitions for statistical confidence
* variations to scan a large parameters space
* combine results for easy evaluation

There are various ways to change parameters.

### Manifests

The YAML manifests for the components can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/k8s

### SQL Scrips

The SQL scripts for pre and post ingestion can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpcds

### Dockerfiles

The Dockerfiles for the components can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/tpcds

### Command line

You maybe want to adjust some of the parameters that are set in the file: `python tpcds.py -h`

```bash
usage: tpcds.py [-h] [-aws] [-db] [-sl] [-ss] [-ar] [-cx CONTEXT]
                [-e EXPERIMENT] [-m] [-ma] [-mc] [-mm MONITORING_METRICS]
                [-ms MAX_SUT] [-mse MAX_SUT_EXPERIMENT]
                [-et EXPERIMENT_TIMEOUT] [-lt LOADING_TIMEOUT]
                [-nc NUM_CONFIG] [-ne NUM_QUERY_EXECUTORS] [-nw NUM_WORKER]
                [-nwr NUM_WORKER_REPLICAS] [-nws NUM_WORKER_SHARDS]
                [-nlp NUM_LOADING_PODS] [-nlt NUM_LOADING_THREADS]
                [-nbp NUM_BENCHMARKING_PODS] [-nbt NUM_BENCHMARKING_THREADS]
                [-sf SCALING_FACTOR] [-t TIMEOUT] [-lr LIMIT_RAM]
                [-lc LIMIT_CPU] [-rr REQUEST_RAM] [-rc REQUEST_CPU]
                [-rct REQUEST_CPU_TYPE] [-rg REQUEST_GPU]
                [-rgt REQUEST_GPU_TYPE] [-rst REQUEST_STORAGE_TYPE]
                [-rss REQUEST_STORAGE_SIZE] [-rsr] [-rsrp]
                [-rnn [REQUEST_NODE_NAME]] [-rnl [REQUEST_NODE_LOADING]]
                [-rnb [REQUEST_NODE_BENCHMARKING]]
                [-rnp [REQUEST_NODE_POOLING]] [-mtn MULTI_TENANT_NUM]
                [-mtb MULTI_TENANT_BY] [-mtv] [-tr] [-rp] [--set SETS]
                [-dbms [{PostgreSQL,MonetDB,MySQL,MariaDB} ...]]
                [-xlit LIMIT_IMPORT_TABLE] [-xdt] [-xqr NUM_RUN]
                [-xnls NUM_LOADING_SPLIT] [-xii] [-xic] [-xis] [-xcol] [-xrcp]
                [-xshq] [-xaq ACTIVE_QUERIES] [-xve] [-xse]
                {profiling,run,start,load,empty,summary}

Run TPC-DS benchmark queries against a DBMS in Kubernetes. Data is generated
on a shared distributed filesystem and loaded in parallel. Supports optional
index, constraint, and statistics creation; multi-stream query ordering.

positional arguments:
  {profiling,run,start,load,empty,summary}
                        experiment phase: profile import, run queries, start
                        SUT only, load data, empty tables, or summarize
                        results

options:
  -h, --help            show this help message and exit
  -aws, --aws           pin components to AWS EKS node groups
  -db, --debug          enable debug logging
  -sl, --skip-loading   skip data loading and start benchmarking immediately
  -ss, --skip-shutdown  keep SUT pods running after the experiment finishes
  -ar, --activate-reset
                        activate configured reset scripts (e.g.
                        CHECKPOINT/VACUUM) when set on a benchmarker entry;
                        off by default
  -cx, --context CONTEXT
                        kubectl context to use (default: current context)
  -e, --experiment EXPERIMENT
                        resume an existing experiment by its code
  -m, --monitoring      enable Prometheus monitoring for the SUT
  -ma, --monitoring-app
                        enable application-level metrics collection
  -mc, --monitoring-cluster
                        enable node-level monitoring for the entire cluster
  -mm, --monitoring-metrics MONITORING_METRICS
                        switch single cluster-wide hardware metrics of
                        cluster.config on or off for this experiment,
                        overriding their 'active' flag, e.g.
                        total_gpu_util=on,total_network_rx=off; needs -m or
                        -mc
  -ms, --max-sut MAX_SUT
                        maximum number of DBMS configurations to run in
                        parallel cluster-wide (default: no limit)
  -mse, --max-sut-experiment MAX_SUT_EXPERIMENT
                        maximum number of DBMS configurations in this
                        experiment to run in parallel (default: no limit)
  -et, --experiment-timeout EXPERIMENT_TIMEOUT
                        maximum wall-clock duration of the experiment in
                        minutes; when exceeded, the experiment is stopped and
                        all its components are removed from the cluster
                        (default: no limit)
  -lt, --loading-timeout LOADING_TIMEOUT
                        maximum loading duration per configuration in minutes;
                        captures diagnostics and removes the experiment when
                        exceeded (default: no limit)
  -nc, --num-config NUM_CONFIG
                        number of experiment repetitions per configuration
  -ne, --num-query-executors NUM_QUERY_EXECUTORS
                        comma-separated list of parallel client counts to
                        sweep
  -nw, --num-worker NUM_WORKER
                        number of worker nodes for distributed DBMS
  -nwr, --num-worker-replicas NUM_WORKER_REPLICAS
                        number of replicas per worker node
  -nws, --num-worker-shards NUM_WORKER_SHARDS
                        number of shards per worker node
  -nlp, --num-loading-pods NUM_LOADING_PODS
                        comma-separated list of total loader pod counts
  -nlt, --num-loading-threads NUM_LOADING_THREADS
                        comma-separated list of total loader threads (split
                        across pods)
  -nbp, --num-benchmarking-pods NUM_BENCHMARKING_PODS
                        comma-separated list of benchmarker pod counts
  -nbt, --num-benchmarking-threads NUM_BENCHMARKING_THREADS
                        total benchmarking threads, split evenly across pods
  -sf, --scaling-factor SCALING_FACTOR
                        scaling factor controlling dataset size
  -t, --timeout TIMEOUT
                        per-query timeout in seconds
  -lr, --limit-ram LIMIT_RAM
                        RAM limit for the SUT and worker pods (e.g. 64Gi; 0 =
                        no limit); comma-separated to sweep several settings
                        (e.g. 32Gi,64Gi), one configuration per entry
  -lc, --limit-cpu LIMIT_CPU
                        CPU limit for the SUT and worker pods (e.g. 4; 0 = no
                        limit); comma-separated to sweep, must then match the
                        length of any other swept resource list
  -rr, --request-ram REQUEST_RAM
                        RAM request for the SUT and worker pods (e.g. 16Gi);
                        comma-separated to sweep several settings (e.g.
                        32Gi,64Gi), one configuration per entry
  -rc, --request-cpu REQUEST_CPU
                        CPU request for the SUT and worker pods (e.g. 4);
                        comma-separated to sweep, must then match the length
                        of any other swept resource list
  -rct, --request-cpu-type REQUEST_CPU_TYPE
                        require SUT node to carry label cpu=<value>
  -rg, --request-gpu REQUEST_GPU
                        number of GPUs to request for the SUT pod
  -rgt, --request-gpu-type REQUEST_GPU_TYPE
                        require SUT node to carry label gpu=<value>
  -rst, --request-storage-type REQUEST_STORAGE_TYPE
                        storage class for the SUT persistent volume ('' or
                        unset = ephemeral, 'ramdisk' = in-memory; other values
                        must be declared for the active cluster context, see
                        cluster config 'storage_classes'); comma-separated to
                        sweep the class, one configuration per entry and
                        paired by position with -rc/-lc/-rr/-lr, an empty
                        entry meaning ephemeral
  -rss, --request-storage-size REQUEST_STORAGE_SIZE
                        size of the SUT persistent volume (e.g. 10Gi)
  -rsr, --request-storage-remove
                        delete any existing PVC for the SUT before starting
  -rsrp, --request-storage-remove-per-repetition
                        delete the PVC of the SUT before every repetition
                        (-nc), so each repetition loads into a fresh volume;
                        implies -rsr
  -rnn, --request-node-name [REQUEST_NODE_NAME]
                        pin the SUT pod to this Kubernetes node
  -rnl, --request-node-loading [REQUEST_NODE_LOADING]
                        pin loader pods to this Kubernetes node
  -rnb, --request-node-benchmarking [REQUEST_NODE_BENCHMARKING]
                        pin benchmarker pods to this Kubernetes node
  -rnp, --request-node-pooling [REQUEST_NODE_POOLING]
                        pin pooling pods to this Kubernetes node
  -mtn, --multi-tenant-num MULTI_TENANT_NUM
                        number of tenants for multi-tenant experiments
  -mtb, --multi-tenant-by MULTI_TENANT_BY
                        tenancy granularity: schema, database, or container
  -mtv, --multi-tenant-volume
                        allocate a separate persistent volume per tenant
  -tr, --test-result    validate that results meet basic correctness
                        requirements
  -rp, --report         also write a tiered Markdown summary report
                        (report/index.md + detail files) to the result folder
  --set SETS            override a deployment parameter, e.g.
                        deployment[bexhoma-deployment-postgres].container[dbms].
                        max_worker_processes=128
  -dbms, --dbms [{PostgreSQL,MonetDB,MySQL,MariaDB} ...]
                        one or more DBMS engines to test
  -xlit, --xlimit-import-table LIMIT_IMPORT_TABLE
                        import only this table (useful for partial re-loads)
  -xdt, --xdata-transfer
                        also measure data transfer volume per query
  -xqr, --xnum-query-runs NUM_RUN
                        number of times to repeat each query
  -xnls, --xnum-loading-split NUM_LOADING_SPLIT
                        number of parallel loader batches (total loaders ÷
                        this = batch size)
  -xii, --xinit-indexes
                        create indexes on all tables after loading
  -xic, --xinit-constraints
                        add primary-key and foreign-key constraints after
                        loading
  -xis, --xinit-statistics
                        run ANALYZE / UPDATE STATISTICS after loading
  -xcol, --xinit-columns
                        use columnar storage (Citus only)
  -xrcp, --xrecreate-parameter
                        regenerate random query parameters for each stream
  -xshq, --xshuffle-queries
                        shuffle query execution order independently per stream
  -xaq, --xactive-queries ACTIVE_QUERIES
                        comma-separated 1-based query numbers to run, e.g.
                        3,5,6,7 (all other queries are set inactive in the
                        query config uploaded to the cluster; unset = run all
                        queries as defined in the query config file)
  -xve, --xverbose-explain
                        run and print configured EXPLAIN statements after each
                        benchmark query (requires an 'explain' key in the DBMS
                        connection's JDBC config)
  -xse, --xstore-explain
                        run configured EXPLAIN statements after the first run
                        of each benchmark query and store the result in the
                        protocol (requires an 'explain' key in the DBMS
                        connection's JDBC config)
```

## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).

Example:
```bash
bexhoma tpcds \
  -dbms PostgreSQL \
  -sf 3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_postgresql_monitoring.log
```

If monitoring is activated, the summary also contains a section like this:

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_postgresql_monitoring_summary.md" target="_blank" rel="noopener">docs_tpcds_postgresql_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 1083s 
* Code: 1792706824
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.8.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'random_page_cost'}, '1.1'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_io_concurrency'}, '200'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'io_method'}, 'io_uring'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers_per_gather'}, '2'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers'}, '4'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_worker_processes'}, '6'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'shared_buffers'}, '20GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_cache_size'}, '48GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'work_mem'}, '1GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'maintenance_work_mem'}, '2GB')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:934115
  * datadisk:14221
  * volume_size:1.8T
  * volume_used:913G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792706824

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1792706824-67cb98dbcf-dhrb7: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    3 |      224.00 |           7.00 |            1.00 |        129.00 |           80.00 |              8 |           0 |             | None           |             0 | False         |               48.21 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |        480 |            0.72 |            15452.34 |           2227.50 |          -1 | postgresql-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |        480 |            0.72 |            15452.34 |           2227.50 |          -1 |

#### Query Completion per Phase

| phase            |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:-----------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   postgresql-1-1-1-1-1 |
|:--------------|-----------------------:|
| TPC-DS Q1     |                 268.68 |
| TPC-DS Q2     |                 852.04 |
| TPC-DS Q3     |                 267.53 |
| TPC-DS Q4     |               18790.49 |
| TPC-DS Q5     |                1945.32 |
| TPC-DS Q6     |              191781.12 |
| TPC-DS Q7     |                 536.04 |
| TPC-DS Q8     |                 101.16 |
| TPC-DS Q9     |                3106.06 |
| TPC-DS Q10    |                1171.31 |
| TPC-DS Q11    |               12645.56 |
| TPC-DS Q12    |                 136.51 |
| TPC-DS Q13    |                1076.39 |
| TPC-DS Q14a+b |                8189.43 |
| TPC-DS Q15    |                 271.01 |
| TPC-DS Q16    |                 378.28 |
| TPC-DS Q17    |                 618.49 |
| TPC-DS Q18    |                 571.55 |
| TPC-DS Q19    |                 386.71 |
| TPC-DS Q20    |                 239.11 |
| TPC-DS Q21    |                 522.68 |
| TPC-DS Q22    |                6517.24 |
| TPC-DS Q23a+b |               11431.01 |
| TPC-DS Q24a+b |                 804.63 |
| TPC-DS Q25    |                 582.42 |
| TPC-DS Q26    |                 412.87 |
| TPC-DS Q27    |                  38.76 |
| TPC-DS Q28    |                2246.84 |
| TPC-DS Q29    |                 682.64 |
| TPC-DS Q30    |               68805.99 |
| TPC-DS Q31    |                3529.78 |
| TPC-DS Q32    |                 190.56 |
| TPC-DS Q33    |                 632.73 |
| TPC-DS Q34    |                  39.84 |
| TPC-DS Q35    |                1379.12 |
| TPC-DS Q36    |                 762.93 |
| TPC-DS Q37    |                 718.13 |
| TPC-DS Q38    |                3798.56 |
| TPC-DS Q39a+b |                5078.84 |
| TPC-DS Q40    |                 245.53 |
| TPC-DS Q41    |                2225.17 |
| TPC-DS Q42    |                 250.24 |
| TPC-DS Q43    |                  46.09 |
| TPC-DS Q44    |                   1.53 |
| TPC-DS Q45    |                 178.62 |
| TPC-DS Q46    |                  60.12 |
| TPC-DS Q47    |                3186.03 |
| TPC-DS Q48    |                1059.91 |
| TPC-DS Q49    |                1036.49 |
| TPC-DS Q50    |                1445.45 |
| TPC-DS Q51    |                2413.15 |
| TPC-DS Q52    |                 245.60 |
| TPC-DS Q53    |                 329.50 |
| TPC-DS Q54    |                  59.66 |
| TPC-DS Q55    |                 234.49 |
| TPC-DS Q56    |                 759.89 |
| TPC-DS Q57    |                1551.90 |
| TPC-DS Q58    |                 724.48 |
| TPC-DS Q59    |                1196.92 |
| TPC-DS Q60    |                 669.22 |
| TPC-DS Q61    |                 108.41 |
| TPC-DS Q62    |                 245.98 |
| TPC-DS Q63    |                 313.26 |
| TPC-DS Q64    |                1211.09 |
| TPC-DS Q65    |                1472.33 |
| TPC-DS Q66    |                 523.86 |
| TPC-DS Q67    |                6750.41 |
| TPC-DS Q68    |                  65.35 |
| TPC-DS Q69    |                 686.83 |
| TPC-DS Q70    |                 901.14 |
| TPC-DS Q71    |                 671.47 |
| TPC-DS Q72    |                2043.43 |
| TPC-DS Q73    |                  37.03 |
| TPC-DS Q74    |                1930.37 |
| TPC-DS Q75    |                2698.08 |
| TPC-DS Q76    |                 413.77 |
| TPC-DS Q77    |                 602.41 |
| TPC-DS Q78    |                2490.14 |
| TPC-DS Q79    |                 409.39 |
| TPC-DS Q80    |                 795.55 |
| TPC-DS Q81    |               49292.95 |
| TPC-DS Q82    |                 937.28 |
| TPC-DS Q83    |                 139.95 |
| TPC-DS Q84    |                  94.15 |
| TPC-DS Q85    |                 396.84 |
| TPC-DS Q86    |                 466.69 |
| TPC-DS Q87    |                2848.38 |
| TPC-DS Q88    |                2863.19 |
| TPC-DS Q89    |                 307.25 |
| TPC-DS Q90    |                 273.10 |
| TPC-DS Q91    |                 140.40 |
| TPC-DS Q92    |                 139.63 |
| TPC-DS Q93    |                 825.50 |
| TPC-DS Q94    |                 325.84 |
| TPC-DS Q95    |                6316.65 |
| TPC-DS Q96    |                 244.11 |
| TPC-DS Q97    |                 907.85 |
| TPC-DS Q98    |                 394.68 |
| TPC-DS Q99    |                 480.34 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       253.55 |      3.46 |           6.37 |                 13.04 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |         0.72 |      0.00 |           0.01 |                  0.01 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        40.37 |      0.32 |           0.01 |                  2.21 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       564.75 |      1.97 |           6.54 |                 13.62 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        20.82 |      0.46 |           0.31 |                  0.32 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)

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

This gives a survey about CPU (in CPU seconds) and RAM usage (in Gb) during loading and execution of the benchmark.
MonetDB is fast, so we cannot see a lot (metrics are fetched every 30 seconds).


## Perform Benchmark - Throughput Test

For performing the experiment we can run the [tpcds file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpcds.py).

Example:
```bash
bexhoma tpcds \
  -dbms PostgreSQL \
  -sf 1 \
  -nc 1 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_postgresql_throughput.log
```

This runs 3 streams (`-ne`), the first one as a single stream and the following 2 in parallel.

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_postgresql_throughput_summary.md" target="_blank" rel="noopener">docs_tpcds_postgresql_throughput.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 924s 
* Code: 1792708107
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.8.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'random_page_cost'}, '1.1'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_io_concurrency'}, '200'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'io_method'}, 'io_uring'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers_per_gather'}, '2'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers'}, '4'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_worker_processes'}, '6'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'shared_buffers'}, '20GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_cache_size'}, '48GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'work_mem'}, '1GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'maintenance_work_mem'}, '2GB')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:925841
  * datadisk:5794
  * volume_size:1.8T
  * volume_used:905G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792708107
* postgresql-1-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:925843
  * datadisk:5794
  * volume_size:1.8T
  * volume_used:905G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792708107
* postgresql-1-1-2-1-2 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:925843
  * datadisk:5794
  * volume_size:1.8T
  * volume_used:905G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792708107

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1792708107-84cf9b955b-855vx: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpcds (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpcds (2 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    1 |      100.00 |           6.00 |            1.00 |         43.00 |           40.00 |              8 |           0 |             | None           |             0 | False         |               36.00 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        160 |            0.32 |            11645.48 |           2227.50 |          -1 | postgresql-1-1-1-1-1 |
| postgresql-1-1-2-1-1 | PostgreSQL-1    | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               99 |                  99 |        164 |            0.32 |            11379.37 |           2173.17 |          -1 | postgresql-1-1-2-1-1 |
| postgresql-1-1-2-1-2 | PostgreSQL-1    | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               99 |                  99 |        159 |            0.32 |            11387.77 |           2241.51 |          -1 | postgresql-1-1-2-1-2 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        160 |            0.32 |            11645.48 |           2227.50 |          -1 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        2 |               1 |           2 | 1.00 |              198 |                 198 |        164 |            0.32 |            11383.57 |           4346.34 |          -1 |

#### Query Completion per Phase

| phase            |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:-----------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| postgresql-1-1-2 |      2 | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   postgresql-1-1-1-1-1 |   postgresql-1-1-2-1-1 |   postgresql-1-1-2-1-2 |
|:--------------|-----------------------:|-----------------------:|-----------------------:|
| TPC-DS Q1     |                 391.40 |                  97.67 |                 441.61 |
| TPC-DS Q2     |                 333.13 |                 345.76 |                 345.76 |
| TPC-DS Q3     |                  97.23 |                  98.99 |                 107.71 |
| TPC-DS Q4     |                5379.31 |                5467.30 |                5438.00 |
| TPC-DS Q5     |                 476.68 |                 636.88 |                 636.44 |
| TPC-DS Q6     |               47658.71 |               50814.04 |               48169.94 |
| TPC-DS Q7     |                 323.51 |                 320.88 |                 322.18 |
| TPC-DS Q8     |                  47.12 |                  51.51 |                  47.60 |
| TPC-DS Q9     |                1789.15 |                1821.68 |                1826.34 |
| TPC-DS Q10    |                 875.50 |                 868.53 |                 898.50 |
| TPC-DS Q11    |                3041.75 |                3062.88 |                3234.48 |
| TPC-DS Q12    |                  56.76 |                  55.73 |                  61.42 |
| TPC-DS Q13    |                 476.07 |                 470.41 |                 483.25 |
| TPC-DS Q14a+b |                2162.14 |                2395.81 |                2420.20 |
| TPC-DS Q15    |                 103.16 |                 102.92 |                 104.42 |
| TPC-DS Q16    |                 187.54 |                 196.54 |                 185.30 |
| TPC-DS Q17    |                 248.18 |                 261.52 |                 264.95 |
| TPC-DS Q18    |                 328.97 |                 354.21 |                 322.18 |
| TPC-DS Q19    |                 121.46 |                 132.01 |                 122.58 |
| TPC-DS Q20    |                  79.60 |                  85.40 |                  80.03 |
| TPC-DS Q21    |                 236.14 |                 332.79 |                 244.76 |
| TPC-DS Q22    |                2722.02 |                2777.73 |                2612.50 |
| TPC-DS Q23a+b |                3761.90 |                3984.62 |                3592.24 |
| TPC-DS Q24a+b |                 574.97 |                 483.85 |                 488.04 |
| TPC-DS Q25    |                 264.87 |                 251.12 |                 258.42 |
| TPC-DS Q26    |                 195.10 |                 195.91 |                 203.09 |
| TPC-DS Q27    |                  41.72 |                  42.41 |                  41.41 |
| TPC-DS Q28    |                1317.54 |                1330.61 |                1357.25 |
| TPC-DS Q29    |                 280.36 |                 277.40 |                 278.16 |
| TPC-DS Q30    |                7669.54 |                7574.95 |                7584.00 |
| TPC-DS Q31    |                1381.16 |                1287.82 |                1305.37 |
| TPC-DS Q32    |                 143.38 |                 138.15 |                 145.05 |
| TPC-DS Q33    |                 323.02 |                 328.97 |                 323.56 |
| TPC-DS Q34    |                  17.97 |                  17.59 |                  20.61 |
| TPC-DS Q35    |                 956.96 |                 980.66 |                 942.37 |
| TPC-DS Q36    |                  19.34 |                  22.55 |                  17.77 |
| TPC-DS Q37    |                 330.94 |                 334.74 |                 324.89 |
| TPC-DS Q38    |                 999.47 |                1437.44 |                1001.64 |
| TPC-DS Q39a+b |                2003.78 |                2325.63 |                2071.85 |
| TPC-DS Q40    |                 109.94 |                 110.64 |                 104.01 |
| TPC-DS Q41    |                 816.17 |                 827.47 |                 761.81 |
| TPC-DS Q42    |                  87.37 |                  82.12 |                  88.91 |
| TPC-DS Q43    |                  22.89 |                  17.12 |                  20.04 |
| TPC-DS Q44    |                 385.38 |                 401.94 |                 391.54 |
| TPC-DS Q45    |                  75.49 |                  73.26 |                  74.58 |
| TPC-DS Q46    |                  24.97 |                  23.85 |                  33.55 |
| TPC-DS Q47    |                1041.93 |                1116.78 |                1068.21 |
| TPC-DS Q48    |                 507.97 |                 486.16 |                 486.80 |
| TPC-DS Q49    |                 439.10 |                 488.63 |                 419.82 |
| TPC-DS Q50    |                 384.80 |                 382.78 |                 369.53 |
| TPC-DS Q51    |                 742.13 |                 924.35 |                 858.04 |
| TPC-DS Q52    |                  88.73 |                  87.48 |                  89.67 |
| TPC-DS Q53    |                 110.59 |                 104.69 |                 110.18 |
| TPC-DS Q54    |                  70.81 |                  61.71 |                  55.97 |
| TPC-DS Q55    |                  84.32 |                  83.79 |                  83.01 |
| TPC-DS Q56    |                 287.77 |                 285.27 |                 268.62 |
| TPC-DS Q57    |                 640.66 |                 710.14 |                 694.98 |
| TPC-DS Q58    |                 316.72 |                 328.34 |                 301.99 |
| TPC-DS Q59    |                 425.92 |                 427.70 |                 411.96 |
| TPC-DS Q60    |                 328.00 |                 324.23 |                 309.52 |
| TPC-DS Q61    |                 105.83 |                 110.34 |                 107.48 |
| TPC-DS Q62    |                  95.22 |                  95.80 |                  89.76 |
| TPC-DS Q63    |                 114.69 |                 115.94 |                 103.12 |
| TPC-DS Q64    |                 599.72 |                 587.42 |                 595.72 |
| TPC-DS Q65    |                 504.19 |                 707.76 |                 540.20 |
| TPC-DS Q66    |                 169.02 |                 173.51 |                 166.43 |
| TPC-DS Q67    |                2088.65 |                2177.48 |                2083.48 |
| TPC-DS Q68    |                  35.25 |                  29.85 |                  29.37 |
| TPC-DS Q69    |                 299.23 |                 403.58 |                 382.98 |
| TPC-DS Q70    |                 346.20 |                 358.38 |                 525.05 |
| TPC-DS Q71    |                 262.64 |                 289.84 |                 257.85 |
| TPC-DS Q72    |                 763.98 |                 812.98 |                 770.80 |
| TPC-DS Q73    |                  22.25 |                  22.50 |                  19.51 |
| TPC-DS Q74    |                 920.61 |                 962.38 |                 928.48 |
| TPC-DS Q75    |                 578.30 |                 614.21 |                 586.16 |
| TPC-DS Q76    |                 222.73 |                 235.13 |                 366.93 |
| TPC-DS Q77    |                 288.42 |                 270.82 |                 280.77 |
| TPC-DS Q78    |                1065.69 |                1072.72 |                1034.25 |
| TPC-DS Q79    |                 157.68 |                 155.16 |                 156.51 |
| TPC-DS Q80    |                 362.85 |                 365.85 |                 371.13 |
| TPC-DS Q81    |               31421.22 |               31589.30 |               31448.59 |
| TPC-DS Q82    |                 344.95 |                 338.26 |                 346.72 |
| TPC-DS Q83    |                  64.16 |                  67.62 |                  68.52 |
| TPC-DS Q84    |                  66.95 |                  70.76 |                  70.08 |
| TPC-DS Q85    |                 265.68 |                 266.23 |                 272.46 |
| TPC-DS Q86    |                 177.83 |                 159.62 |                 163.62 |
| TPC-DS Q87    |                1114.59 |                1018.78 |                1094.30 |
| TPC-DS Q88    |                1985.77 |                1950.95 |                1956.44 |
| TPC-DS Q89    |                 112.94 |                 116.12 |                 227.50 |
| TPC-DS Q90    |                  98.45 |                  93.09 |                  92.93 |
| TPC-DS Q91    |                 119.27 |                 119.57 |                 123.53 |
| TPC-DS Q92    |                  45.79 |                  47.15 |                  51.38 |
| TPC-DS Q93    |                 239.68 |                 467.64 |                 304.20 |
| TPC-DS Q94    |                 130.40 |                 121.94 |                 125.35 |
| TPC-DS Q95    |                2755.35 |                2593.97 |                2633.09 |
| TPC-DS Q96    |                  93.57 |                  97.98 |                  92.22 |
| TPC-DS Q97    |                 325.73 |                 333.63 |                 328.48 |
| TPC-DS Q98    |                 132.10 |                 266.12 |                 132.61 |
| TPC-DS Q99    |                 156.55 |                 156.24 |                 162.25 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

|                      |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:---------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| postgresql-1-1-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| postgresql-1-1-2-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST failed: SQL warnings (result mismatch)
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
```

</details>

All executions use the same database, so loading times are the same.

Per default, all 3 streams use the same random parameters (like YEAR in Q1) and run in ordering Q1-Q99.
You can change this via
* `-xrcp`: Each stream has it's own random parameters
* `-xshq`: Use the ordering per stream as required by the TPC-DS specification

## Reset Scripts

With `-ar`, a reset script runs before each benchmarking round (statistics, persist, counters; e.g. `VACUUM ANALYZE`, `CHECKPOINT` and a statistics reset for PostgreSQL), so every stream starts from a comparable state.
See [Reset scripts](DBMS.md#reset-scripts--ar) for what each DBMS does.

## Use Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.
With repetitions (`-nc`), `-rsr` removes an existing volume only before the first repetition and later repetitions reuse it without loading; `-rsrp` removes it before every repetition. See [Concepts](Concepts.html).

Example:
```bash
bexhoma tpcds \
  -dbms PostgreSQL \
  -sf 1 \
  -nc 2 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_postgresql_storage.log
```
The following status shows we have a volumes of type `shared`.
Every experiment running TPC-DS of SF=1 at MonetDB will take the database from this volume and skip loading.
In this example `-nc` is set to two, that is the complete experiment is repeated twice for statistical confidence.
The first instance of MonetDB mounts the volume and generates the data.
All other instances just use the database without generating and loading data.

```bash
+-----------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| Volumes                                 | configuration   | experiment   | loaded [s]   |   timeLoading [s] | dbms       | storage_class_name   | storage   | status   | size   | used   |
+=========================================+=================+==============+==============+===================+============+======================+===========+==========+========+========+
| bexhoma-storage-monetdb-tpcds-1         | monetdb         | tpcds-1      | True         |               151 | MonetDB    | shared               | 30Gi      | Bound    | 10G    | 2.0G   |
+-----------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-monetdb-tpcds-3         | monetdb         | tpcds-3      | True         |               393 | MonetDB    | shared               | 100Gi     | Bound    | 100G   | 5.4G   |
+-----------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-monetdb-tpcds-100       | monetdb         | tpcds-100    | True         |              4019 | MonetDB    | shared               | 300Gi     | Bound    | 300G   | 156G   |
+-----------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+

+---------------+--------------+--------------+---------------+
| 1707740320    | sut          |   loaded [s] | benchmarker   |
+===============+==============+==============+===============+
| MonetDB-BHT-8 | (1. Running) |       185.41 | (1. Running)  |
+---------------+--------------+--------------+---------------+
```

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_postgresql_storage_summary.md" target="_blank" rel="noopener">docs_tpcds_postgresql_storage.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 1134s 
* Code: 1792709181
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.8.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'random_page_cost'}, '1.1'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_io_concurrency'}, '200'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'io_method'}, 'io_uring'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers_per_gather'}, '2'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers'}, '4'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_worker_processes'}, '6'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'shared_buffers'}, '20GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_cache_size'}, '48GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'work_mem'}, '1GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'maintenance_work_mem'}, '2GB')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:920048
  * datadisk:5794
  * volume_size:49G
  * volume_used:5.7G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792709181
* postgresql-1-2-1-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:920018
  * datadisk:5794
  * volume_size:49G
  * volume_used:5.7G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792709181

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: PostgreSQL-1-2

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1792709181-7bc865bb85-76vzf: 0
* bexhoma-sut-postgresql-1-1792709181-86566ccf8f-f7gz8: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    1 |      101.00 |           7.00 |            1.00 |         43.00 |           42.00 |              8 |           0 |             | None           |             0 | False         |               35.64 | False               |
| PostgreSQL-1-2 |                2 |    1 |      101.00 |           7.00 |            1.00 |         43.00 |           42.00 |              8 |           0 |             | None           |             0 | False         |               35.64 | True                |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        160 |            0.29 |            12744.12 |           2227.50 |          -1 | postgresql-1-1-1-1-1 |
| postgresql-1-2-1-1-1 | PostgreSQL-1    | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        168 |            0.32 |            11676.30 |           2121.43 |          -1 | postgresql-1-2-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        160 |            0.29 |            12744.12 |           2227.50 |          -1 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        168 |            0.32 |            11676.30 |           2121.43 |          -1 |

#### Query Completion per Phase

| phase            |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:-----------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| postgresql-1-2-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   postgresql-1-1-1-1-1 |   postgresql-1-2-1-1-1 |
|:--------------|-----------------------:|-----------------------:|
| TPC-DS Q1     |                  83.00 |                1639.93 |
| TPC-DS Q2     |                 328.66 |                 435.69 |
| TPC-DS Q3     |                  95.66 |                 224.87 |
| TPC-DS Q4     |                5404.33 |                5601.19 |
| TPC-DS Q5     |                 461.25 |                 527.55 |
| TPC-DS Q6     |               48854.02 |               48292.68 |
| TPC-DS Q7     |                 303.64 |                 373.05 |
| TPC-DS Q8     |                  49.02 |                  50.83 |
| TPC-DS Q9     |                1846.80 |                1868.25 |
| TPC-DS Q10    |                 873.83 |                2690.03 |
| TPC-DS Q11    |                3049.11 |                3158.64 |
| TPC-DS Q12    |                  54.72 |                  56.14 |
| TPC-DS Q13    |                 482.72 |                 473.96 |
| TPC-DS Q14a+b |                2144.67 |                2153.59 |
| TPC-DS Q15    |                  93.03 |                 106.86 |
| TPC-DS Q16    |                 175.58 |                 205.71 |
| TPC-DS Q17    |                 244.03 |                 263.61 |
| TPC-DS Q18    |                 310.39 |                 342.01 |
| TPC-DS Q19    |                 121.64 |                 122.74 |
| TPC-DS Q20    |                  78.53 |                  81.95 |
| TPC-DS Q21    |                 233.41 |                 310.20 |
| TPC-DS Q22    |                2560.65 |                2655.79 |
| TPC-DS Q23a+b |                3615.45 |                3541.90 |
| TPC-DS Q24a+b |                 646.92 |                 661.22 |
| TPC-DS Q25    |                 259.27 |                 253.64 |
| TPC-DS Q26    |                 193.84 |                 206.05 |
| TPC-DS Q27    |                  40.43 |                  37.46 |
| TPC-DS Q28    |                1343.76 |                1329.40 |
| TPC-DS Q29    |                 268.86 |                 279.32 |
| TPC-DS Q30    |                7687.49 |                7608.32 |
| TPC-DS Q31    |                1300.76 |                1308.44 |
| TPC-DS Q32    |                 101.96 |                 111.28 |
| TPC-DS Q33    |                 329.18 |                 326.42 |
| TPC-DS Q34    |                  18.42 |                  21.32 |
| TPC-DS Q35    |                 969.84 |                 989.42 |
| TPC-DS Q36    |                 284.61 |                 285.48 |
| TPC-DS Q37    |                 324.12 |                 333.45 |
| TPC-DS Q38    |                 958.22 |                 965.90 |
| TPC-DS Q39a+b |                1933.71 |                1960.22 |
| TPC-DS Q40    |                 102.62 |                 107.28 |
| TPC-DS Q41    |                 744.67 |                 746.10 |
| TPC-DS Q42    |                  92.10 |                  86.67 |
| TPC-DS Q43    |                  20.79 |                  17.96 |
| TPC-DS Q44    |                   2.35 |                   4.36 |
| TPC-DS Q45    |                  73.66 |                  71.55 |
| TPC-DS Q46    |                  24.95 |                  22.97 |
| TPC-DS Q47    |                1152.17 |                1160.27 |
| TPC-DS Q48    |                 476.95 |                 477.76 |
| TPC-DS Q49    |                 426.08 |                 424.85 |
| TPC-DS Q50    |                 383.02 |                 383.00 |
| TPC-DS Q51    |                 692.25 |                 684.41 |
| TPC-DS Q52    |                  80.66 |                  90.40 |
| TPC-DS Q53    |                 103.10 |                 109.34 |
| TPC-DS Q54    |                  62.30 |                  67.54 |
| TPC-DS Q55    |                  80.22 |                  80.42 |
| TPC-DS Q56    |                 313.38 |                 312.30 |
| TPC-DS Q57    |                 622.50 |                 588.30 |
| TPC-DS Q58    |                 296.78 |                 317.13 |
| TPC-DS Q59    |                 410.26 |                 416.67 |
| TPC-DS Q60    |                 303.86 |                 300.83 |
| TPC-DS Q61    |                 105.67 |                 106.04 |
| TPC-DS Q62    |                  92.37 |                 101.88 |
| TPC-DS Q63    |                 103.31 |                 109.41 |
| TPC-DS Q64    |                 589.87 |                 581.91 |
| TPC-DS Q65    |                 503.70 |                 512.04 |
| TPC-DS Q66    |                 166.93 |                 187.43 |
| TPC-DS Q67    |                2084.58 |                2126.38 |
| TPC-DS Q68    |                  30.00 |                  34.92 |
| TPC-DS Q69    |                 114.55 |                 121.95 |
| TPC-DS Q70    |                 341.50 |                 340.63 |
| TPC-DS Q71    |                 263.06 |                 276.72 |
| TPC-DS Q72    |                 792.00 |                 829.22 |
| TPC-DS Q73    |                  20.86 |                  21.20 |
| TPC-DS Q74    |                 845.76 |                 817.94 |
| TPC-DS Q75    |                 604.96 |                 586.65 |
| TPC-DS Q76    |                 198.53 |                 206.74 |
| TPC-DS Q77    |                 281.85 |                 289.19 |
| TPC-DS Q78    |                 946.73 |                1036.25 |
| TPC-DS Q79    |                 143.91 |                 155.42 |
| TPC-DS Q80    |                 351.15 |                 359.40 |
| TPC-DS Q81    |               31507.87 |               31646.11 |
| TPC-DS Q82    |                 348.41 |                 361.89 |
| TPC-DS Q83    |                  67.78 |                  71.24 |
| TPC-DS Q84    |                  18.18 |                  19.75 |
| TPC-DS Q85    |                 275.60 |                 265.13 |
| TPC-DS Q86    |                 159.21 |                 150.52 |
| TPC-DS Q87    |                1011.85 |                1027.39 |
| TPC-DS Q88    |                1935.71 |                1938.40 |
| TPC-DS Q89    |                 129.54 |                 130.49 |
| TPC-DS Q90    |                  94.05 |                  97.63 |
| TPC-DS Q91    |                  86.38 |                  93.09 |
| TPC-DS Q92    |                  49.65 |                  50.62 |
| TPC-DS Q93    |                 238.30 |                 237.87 |
| TPC-DS Q94    |                 124.71 |                 137.63 |
| TPC-DS Q95    |                2627.93 |                2605.66 |
| TPC-DS Q96    |                  93.53 |                  97.88 |
| TPC-DS Q97    |                 336.12 |                 332.55 |
| TPC-DS Q98    |                 131.58 |                 135.74 |
| TPC-DS Q99    |                 161.26 |                 164.67 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

|                      |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:---------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| postgresql-1-1-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST failed: SQL warnings (result mismatch)
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
```

</details>


The loading times for both instances of loading are the same, since both relate to the same process of ingesting into the database.
Note the added section about `volume_size` and `volume_used` in the connections section.









## Profiling Benchmark

We have included a custom data profiling benchmark as in [1].
> We differentiate between metric attributes (INTEGER, DOUBLE, DECIMAL) and nominal attributes (others). We seek to obtain basic statistics about the attributes and we use COUNT, COUNT NULL (missing values), COUNT DISTINCT and the distribution: MIN, MAX, truncated AVG of values (metric) or of frequencies (nominal). We query for these 6 statistics per attribute and this yields 429 profiling queries. 

In [1] the benchmark is used to assess node stability and to compare performance of DBMS and cloud providers.

[1] [Orchestrating DBMS Benchmarking in the Cloud with Kubernetes](https://doi.org/10.1007/978-3-030-94437-7_6)
> Erdelt P.K. (2022)
> Orchestrating DBMS Benchmarking in the Cloud with Kubernetes.
> In: Nambiar R., Poess M. (eds) Performance Evaluation and Benchmarking. TPCTC 2021.
> Lecture Notes in Computer Science, vol 13169. Springer, Cham.
> https://doi.org/10.1007/978-3-030-94437-7_6

Here, we run it at TPC-DS SF=10 in PostgreSQL:


```bash
bexhoma tpcds \
  -dbms PostgreSQL \
  -sf 10 \
  -ne 1,1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  profiling &>$LOG_DIR/docs_tpcds_postgresql_profiling.log
```

### Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_postgresql_profiling_summary.md" target="_blank" rel="noopener">docs_tpcds_postgresql_profiling.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Data Profiling SF=10
* Type: tpcds
* Duration: 1161s 
* Code: 1792737661
* We compute for all columns: Minimum, maximum, average, count, count distinct, count NULL and non NULL entries and coefficient of variation.
* This experiment compares imported TPC-DS data sets in different DBMS.
  * TPC-DS (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.8.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'random_page_cost'}, '1.1'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_io_concurrency'}, '200'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'io_method'}, 'io_uring'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers_per_gather'}, '2'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers'}, '4'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_worker_processes'}, '6'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'shared_buffers'}, '20GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_cache_size'}, '48GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'work_mem'}, '1GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'maintenance_work_mem'}, '2GB')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:920044
  * datadisk:50067
  * volume_size:49G
  * volume_used:49G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792737661
* postgresql-1-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:920045
  * datadisk:50067
  * volume_size:49G
  * volume_used:49G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792737661

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1792737661-69dbbc99c-hstmg: 1 (dbms=1, monitor-application=0)
  * dbms: Error (exit 1) at Fri, 23 Oct 2026 08:59:06 +0200; data on a mounted volume

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpcds (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |   10 |      377.00 |           5.00 |            1.00 |        339.00 |           23.00 |              8 |           0 |             | None           |             0 | False         |               95.49 | False               |

### Benchmarking

#### Per Connection

No rows: these totals count only queries that succeeded in every connection of this experiment, and no query did (Q1 failed in 2 of 2 connections; Q2 failed in 2 of 2 connections; Q3 failed in 2 of 2 connections; Q4 failed in 2 of 2 connections; Q5 failed in 2 of 2 connections; Q6 failed in 2 of 2 connections; Q7 failed in 2 of 2 connections; Q8 failed in 2 of 2 connections; Q9 failed in 2 of 2 connections; Q10 failed in 2 of 2 connections; Q11 failed in 2 of 2 connections; Q12 failed in 2 of 2 connections; Q13 failed in 2 of 2 connections; Q14 failed in 2 of 2 connections; Q15 failed in 2 of 2 connections; Q16 failed in 2 of 2 connections; Q17 failed in 2 of 2 connections; Q18 failed in 2 of 2 connections; Q19 failed in 2 of 2 connections; Q20 failed in 2 of 2 connections; Q21 failed in 2 of 2 connections; Q22 failed in 2 of 2 connections; Q23 failed in 2 of 2 connections; Q24 failed in 2 of 2 connections; Q25 failed in 2 of 2 connections; Q26 failed in 2 of 2 connections; Q27 failed in 2 of 2 connections; Q28 failed in 2 of 2 connections; Q29 failed in 2 of 2 connections; Q30 failed in 2 of 2 connections; Q31 failed in 2 of 2 connections; Q32 failed in 2 of 2 connections; Q33 failed in 2 of 2 connections; Q34 failed in 2 of 2 connections; Q35 failed in 2 of 2 connections; Q36 failed in 2 of 2 connections; Q37 failed in 2 of 2 connections; Q38 failed in 2 of 2 connections; Q39 failed in 2 of 2 connections; Q40 failed in 2 of 2 connections; Q41 failed in 2 of 2 connections; Q42 failed in 2 of 2 connections; Q43 failed in 2 of 2 connections; Q44 failed in 2 of 2 connections; Q45 failed in 2 of 2 connections; Q46 failed in 2 of 2 connections; Q47 failed in 2 of 2 connections; Q48 failed in 2 of 2 connections; Q49 failed in 2 of 2 connections; Q50 failed in 2 of 2 connections; Q51 failed in 2 of 2 connections; Q52 failed in 2 of 2 connections; Q53 failed in 2 of 2 connections; Q54 failed in 2 of 2 connections; Q55 failed in 2 of 2 connections; Q56 failed in 2 of 2 connections; Q57 failed in 2 of 2 connections; Q58 failed in 2 of 2 connections; Q59 failed in 2 of 2 connections; Q60 failed in 2 of 2 connections; Q61 failed in 2 of 2 connections; Q62 failed in 2 of 2 connections; Q63 failed in 2 of 2 connections; Q64 failed in 2 of 2 connections; Q65 failed in 2 of 2 connections; Q66 failed in 2 of 2 connections; Q67 failed in 2 of 2 connections; Q68 failed in 2 of 2 connections; Q69 failed in 2 of 2 connections; Q70 failed in 2 of 2 connections; Q71 failed in 2 of 2 connections; Q72 failed in 2 of 2 connections; Q73 failed in 2 of 2 connections; Q74 failed in 2 of 2 connections; Q75 failed in 2 of 2 connections; Q76 failed in 2 of 2 connections; Q77 failed in 2 of 2 connections; Q78 failed in 2 of 2 connections; Q79 failed in 2 of 2 connections; Q80 failed in 2 of 2 connections; Q81 failed in 2 of 2 connections; Q82 failed in 2 of 2 connections; Q83 failed in 2 of 2 connections; Q84 failed in 2 of 2 connections; Q85 failed in 2 of 2 connections; Q86 failed in 2 of 2 connections; Q87 failed in 2 of 2 connections; Q88 failed in 2 of 2 connections; Q89 failed in 2 of 2 connections; Q90 failed in 2 of 2 connections; Q91 failed in 2 of 2 connections; Q92 failed in 2 of 2 connections; Q93 failed in 2 of 2 connections; Q94 failed in 2 of 2 connections; Q95 failed in 2 of 2 connections; Q96 failed in 2 of 2 connections; Q97 failed in 2 of 2 connections; Q98 failed in 2 of 2 connections; Q99 failed in 2 of 2 connections; Q100 failed in 2 of 2 connections; Q101 failed in 2 of 2 connections; Q102 failed in 2 of 2 connections; Q103 failed in 2 of 2 connections; Q104 failed in 2 of 2 connections; Q105 failed in 2 of 2 connections; Q106 failed in 2 of 2 connections; Q107 failed in 2 of 2 connections; Q108 failed in 2 of 2 connections; Q109 failed in 2 of 2 connections; Q110 failed in 2 of 2 connections; Q111 failed in 2 of 2 connections; Q112 failed in 2 of 2 connections; Q113 failed in 2 of 2 connections; Q114 failed in 2 of 2 connections; Q115 failed in 2 of 2 connections; Q116 failed in 2 of 2 connections; Q117 failed in 2 of 2 connections; Q118 failed in 2 of 2 connections; Q119 failed in 2 of 2 connections; Q120 failed in 2 of 2 connections; Q121 failed in 2 of 2 connections; Q122 failed in 2 of 2 connections; Q123 failed in 2 of 2 connections; Q124 failed in 2 of 2 connections; Q125 failed in 2 of 2 connections; Q126 failed in 2 of 2 connections; Q127 failed in 2 of 2 connections; Q128 failed in 2 of 2 connections; Q129 failed in 2 of 2 connections; Q130 failed in 2 of 2 connections; Q131 failed in 2 of 2 connections; Q132 failed in 2 of 2 connections; Q133 failed in 2 of 2 connections; Q134 failed in 2 of 2 connections; Q135 failed in 2 of 2 connections; Q136 failed in 2 of 2 connections; Q137 failed in 2 of 2 connections; Q138 failed in 2 of 2 connections; Q139 failed in 2 of 2 connections; Q140 failed in 2 of 2 connections; Q141 failed in 2 of 2 connections; Q142 failed in 2 of 2 connections; Q143 failed in 2 of 2 connections; Q144 failed in 2 of 2 connections; Q145 failed in 2 of 2 connections; Q146 failed in 2 of 2 connections; Q147 failed in 2 of 2 connections; Q148 failed in 2 of 2 connections; Q149 failed in 2 of 2 connections; Q150 failed in 2 of 2 connections; Q151 failed in 2 of 2 connections; Q152 failed in 2 of 2 connections; Q153 failed in 2 of 2 connections; Q154 failed in 2 of 2 connections; Q155 failed in 2 of 2 connections; Q156 failed in 2 of 2 connections; Q157 failed in 2 of 2 connections; Q158 failed in 2 of 2 connections; Q159 failed in 2 of 2 connections; Q160 failed in 2 of 2 connections; Q161 failed in 2 of 2 connections; Q162 failed in 2 of 2 connections; Q163 failed in 2 of 2 connections; Q164 failed in 2 of 2 connections; Q165 failed in 2 of 2 connections; Q166 failed in 2 of 2 connections; Q167 failed in 2 of 2 connections; Q168 failed in 2 of 2 connections; Q169 failed in 2 of 2 connections; Q170 failed in 2 of 2 connections; Q171 failed in 2 of 2 connections; Q172 failed in 2 of 2 connections; Q173 failed in 2 of 2 connections; Q174 failed in 2 of 2 connections; Q175 failed in 2 of 2 connections; Q176 failed in 2 of 2 connections; Q177 failed in 2 of 2 connections; Q178 failed in 2 of 2 connections; Q179 failed in 2 of 2 connections; Q180 failed in 2 of 2 connections; Q181 failed in 2 of 2 connections; Q182 failed in 2 of 2 connections; Q183 failed in 2 of 2 connections; Q184 failed in 2 of 2 connections; Q185 failed in 2 of 2 connections; Q186 failed in 2 of 2 connections; Q187 failed in 2 of 2 connections; Q188 failed in 2 of 2 connections; Q189 failed in 2 of 2 connections; Q190 failed in 2 of 2 connections; Q191 failed in 2 of 2 connections; Q192 failed in 2 of 2 connections; Q193 failed in 2 of 2 connections; Q194 failed in 2 of 2 connections; Q195 failed in 2 of 2 connections; Q196 failed in 2 of 2 connections; Q197 failed in 2 of 2 connections; Q198 failed in 2 of 2 connections; Q199 failed in 2 of 2 connections; Q200 failed in 2 of 2 connections; Q201 failed in 2 of 2 connections; Q202 failed in 2 of 2 connections; Q203 failed in 2 of 2 connections; Q204 failed in 2 of 2 connections; Q205 failed in 2 of 2 connections; Q206 failed in 2 of 2 connections; Q207 failed in 2 of 2 connections; Q208 failed in 2 of 2 connections; Q209 failed in 2 of 2 connections; Q210 failed in 2 of 2 connections; Q211 failed in 2 of 2 connections; Q212 failed in 2 of 2 connections; Q213 failed in 2 of 2 connections; Q214 failed in 2 of 2 connections; Q215 failed in 2 of 2 connections; Q216 failed in 2 of 2 connections; Q217 failed in 2 of 2 connections; Q218 failed in 2 of 2 connections; Q219 failed in 2 of 2 connections; Q220 failed in 2 of 2 connections; Q221 failed in 2 of 2 connections; Q222 failed in 2 of 2 connections; Q223 failed in 2 of 2 connections; Q224 failed in 2 of 2 connections; Q225 failed in 2 of 2 connections; Q226 failed in 2 of 2 connections; Q227 failed in 2 of 2 connections; Q228 failed in 2 of 2 connections; Q229 failed in 2 of 2 connections; Q230 failed in 2 of 2 connections; Q231 failed in 2 of 2 connections; Q232 failed in 2 of 2 connections; Q233 failed in 2 of 2 connections; Q234 failed in 2 of 2 connections; Q235 failed in 2 of 2 connections; Q236 failed in 2 of 2 connections; Q237 failed in 2 of 2 connections; Q238 failed in 2 of 2 connections; Q239 failed in 2 of 2 connections; Q240 failed in 2 of 2 connections; Q241 failed in 2 of 2 connections; Q242 failed in 2 of 2 connections; Q243 failed in 2 of 2 connections; Q244 failed in 2 of 2 connections; Q245 failed in 2 of 2 connections; Q246 failed in 2 of 2 connections; Q247 failed in 2 of 2 connections; Q248 failed in 2 of 2 connections; Q249 failed in 2 of 2 connections; Q250 failed in 2 of 2 connections; Q251 failed in 2 of 2 connections; Q252 failed in 2 of 2 connections; Q253 failed in 2 of 2 connections; Q254 failed in 2 of 2 connections; Q255 failed in 2 of 2 connections; Q256 failed in 2 of 2 connections; Q257 failed in 2 of 2 connections; Q258 failed in 2 of 2 connections; Q259 failed in 2 of 2 connections; Q260 failed in 2 of 2 connections; Q261 failed in 2 of 2 connections; Q262 failed in 2 of 2 connections; Q263 failed in 2 of 2 connections; Q264 failed in 2 of 2 connections; Q265 failed in 2 of 2 connections; Q266 failed in 2 of 2 connections; Q267 failed in 2 of 2 connections; Q268 failed in 2 of 2 connections; Q269 failed in 2 of 2 connections; Q270 failed in 2 of 2 connections; Q271 failed in 2 of 2 connections; Q272 failed in 2 of 2 connections; Q273 failed in 2 of 2 connections; Q274 failed in 2 of 2 connections; Q275 failed in 2 of 2 connections; Q276 failed in 2 of 2 connections; Q277 failed in 2 of 2 connections; Q278 failed in 2 of 2 connections; Q279 failed in 2 of 2 connections; Q280 failed in 2 of 2 connections; Q281 failed in 2 of 2 connections; Q282 failed in 2 of 2 connections; Q283 failed in 2 of 2 connections; Q284 failed in 2 of 2 connections; Q285 failed in 2 of 2 connections; Q286 failed in 2 of 2 connections; Q287 failed in 2 of 2 connections; Q288 failed in 2 of 2 connections; Q289 failed in 2 of 2 connections; Q290 failed in 2 of 2 connections; Q291 failed in 2 of 2 connections; Q292 failed in 2 of 2 connections; Q293 failed in 2 of 2 connections; Q294 failed in 2 of 2 connections; Q295 failed in 2 of 2 connections; Q296 failed in 2 of 2 connections; Q297 failed in 2 of 2 connections; Q298 failed in 2 of 2 connections; Q299 failed in 2 of 2 connections; Q300 failed in 2 of 2 connections; Q301 failed in 2 of 2 connections; Q302 failed in 2 of 2 connections; Q303 failed in 2 of 2 connections; Q304 failed in 2 of 2 connections; Q305 failed in 2 of 2 connections; Q306 failed in 2 of 2 connections; Q307 failed in 2 of 2 connections; Q308 failed in 2 of 2 connections; Q309 failed in 2 of 2 connections; Q310 failed in 2 of 2 connections; Q311 failed in 2 of 2 connections; Q312 failed in 2 of 2 connections; Q313 failed in 2 of 2 connections; Q314 failed in 2 of 2 connections; Q315 failed in 2 of 2 connections; Q316 failed in 2 of 2 connections; Q317 failed in 2 of 2 connections; Q318 failed in 2 of 2 connections; Q319 failed in 2 of 2 connections; Q320 failed in 2 of 2 connections; Q321 failed in 2 of 2 connections; Q322 failed in 2 of 2 connections; Q323 failed in 2 of 2 connections; Q324 failed in 2 of 2 connections; Q325 failed in 2 of 2 connections; Q326 failed in 2 of 2 connections; Q327 failed in 2 of 2 connections; Q328 failed in 2 of 2 connections; Q329 failed in 2 of 2 connections; Q330 failed in 2 of 2 connections; Q331 failed in 2 of 2 connections; Q332 failed in 2 of 2 connections; Q333 failed in 2 of 2 connections; Q334 failed in 2 of 2 connections; Q335 failed in 2 of 2 connections; Q336 failed in 2 of 2 connections; Q337 failed in 2 of 2 connections; Q338 failed in 2 of 2 connections; Q339 failed in 2 of 2 connections; Q340 failed in 2 of 2 connections; Q341 failed in 2 of 2 connections; Q342 failed in 2 of 2 connections; Q343 failed in 2 of 2 connections; Q344 failed in 2 of 2 connections; Q345 failed in 2 of 2 connections; Q346 failed in 2 of 2 connections; Q347 failed in 2 of 2 connections; Q348 failed in 2 of 2 connections; Q349 failed in 2 of 2 connections; Q350 failed in 2 of 2 connections; Q351 failed in 2 of 2 connections; Q352 failed in 2 of 2 connections; Q353 failed in 2 of 2 connections; Q354 failed in 2 of 2 connections; Q355 failed in 2 of 2 connections; Q356 failed in 2 of 2 connections; Q357 failed in 2 of 2 connections; Q358 failed in 2 of 2 connections; Q359 failed in 2 of 2 connections; Q360 failed in 2 of 2 connections; Q361 failed in 2 of 2 connections; Q362 failed in 2 of 2 connections; Q363 failed in 2 of 2 connections; Q364 failed in 2 of 2 connections; Q365 failed in 2 of 2 connections; Q366 failed in 2 of 2 connections; Q367 failed in 2 of 2 connections; Q368 failed in 2 of 2 connections; Q369 failed in 2 of 2 connections; Q370 failed in 2 of 2 connections; Q371 failed in 2 of 2 connections; Q372 failed in 2 of 2 connections; Q373 failed in 2 of 2 connections; Q374 failed in 2 of 2 connections; Q375 failed in 2 of 2 connections; Q376 failed in 2 of 2 connections; Q377 failed in 2 of 2 connections; Q378 failed in 2 of 2 connections; Q379 failed in 2 of 2 connections; Q380 failed in 2 of 2 connections; Q381 failed in 2 of 2 connections; Q382 failed in 2 of 2 connections; Q383 failed in 2 of 2 connections; Q384 failed in 2 of 2 connections; Q385 failed in 2 of 2 connections; Q386 failed in 2 of 2 connections; Q387 failed in 2 of 2 connections; Q388 failed in 2 of 2 connections; Q389 failed in 2 of 2 connections; Q390 failed in 2 of 2 connections; Q391 failed in 2 of 2 connections; Q392 failed in 2 of 2 connections; Q393 failed in 2 of 2 connections; Q394 failed in 2 of 2 connections; Q395 failed in 2 of 2 connections; Q396 failed in 2 of 2 connections; Q397 failed in 2 of 2 connections; Q398 failed in 2 of 2 connections; Q399 failed in 2 of 2 connections; Q400 failed in 2 of 2 connections; Q401 failed in 2 of 2 connections; Q402 failed in 2 of 2 connections; Q403 failed in 2 of 2 connections; Q404 failed in 2 of 2 connections; Q405 failed in 2 of 2 connections; Q406 failed in 2 of 2 connections; Q407 failed in 2 of 2 connections; Q408 failed in 2 of 2 connections; Q409 failed in 2 of 2 connections; Q410 failed in 2 of 2 connections; Q411 failed in 2 of 2 connections; Q412 failed in 2 of 2 connections; Q413 failed in 2 of 2 connections; Q414 failed in 2 of 2 connections; Q415 failed in 2 of 2 connections; Q416 failed in 2 of 2 connections; Q417 failed in 2 of 2 connections; Q418 failed in 2 of 2 connections; Q419 failed in 2 of 2 connections; Q420 failed in 2 of 2 connections; Q421 failed in 2 of 2 connections; Q422 failed in 2 of 2 connections; Q423 failed in 2 of 2 connections; Q424 failed in 2 of 2 connections; Q425 failed in 2 of 2 connections; Q426 failed in 2 of 2 connections; Q427 failed in 2 of 2 connections; Q428 failed in 2 of 2 connections; Q429 failed in 2 of 2 connections). See Query Completion per Phase for where, and Per Phase (Complete Phases Only) for the phases that completed every query.

#### Per Phase

No rows: these totals count only queries that succeeded in every connection of this experiment, and no query did (Q1 failed in 2 of 2 connections; Q2 failed in 2 of 2 connections; Q3 failed in 2 of 2 connections; Q4 failed in 2 of 2 connections; Q5 failed in 2 of 2 connections; Q6 failed in 2 of 2 connections; Q7 failed in 2 of 2 connections; Q8 failed in 2 of 2 connections; Q9 failed in 2 of 2 connections; Q10 failed in 2 of 2 connections; Q11 failed in 2 of 2 connections; Q12 failed in 2 of 2 connections; Q13 failed in 2 of 2 connections; Q14 failed in 2 of 2 connections; Q15 failed in 2 of 2 connections; Q16 failed in 2 of 2 connections; Q17 failed in 2 of 2 connections; Q18 failed in 2 of 2 connections; Q19 failed in 2 of 2 connections; Q20 failed in 2 of 2 connections; Q21 failed in 2 of 2 connections; Q22 failed in 2 of 2 connections; Q23 failed in 2 of 2 connections; Q24 failed in 2 of 2 connections; Q25 failed in 2 of 2 connections; Q26 failed in 2 of 2 connections; Q27 failed in 2 of 2 connections; Q28 failed in 2 of 2 connections; Q29 failed in 2 of 2 connections; Q30 failed in 2 of 2 connections; Q31 failed in 2 of 2 connections; Q32 failed in 2 of 2 connections; Q33 failed in 2 of 2 connections; Q34 failed in 2 of 2 connections; Q35 failed in 2 of 2 connections; Q36 failed in 2 of 2 connections; Q37 failed in 2 of 2 connections; Q38 failed in 2 of 2 connections; Q39 failed in 2 of 2 connections; Q40 failed in 2 of 2 connections; Q41 failed in 2 of 2 connections; Q42 failed in 2 of 2 connections; Q43 failed in 2 of 2 connections; Q44 failed in 2 of 2 connections; Q45 failed in 2 of 2 connections; Q46 failed in 2 of 2 connections; Q47 failed in 2 of 2 connections; Q48 failed in 2 of 2 connections; Q49 failed in 2 of 2 connections; Q50 failed in 2 of 2 connections; Q51 failed in 2 of 2 connections; Q52 failed in 2 of 2 connections; Q53 failed in 2 of 2 connections; Q54 failed in 2 of 2 connections; Q55 failed in 2 of 2 connections; Q56 failed in 2 of 2 connections; Q57 failed in 2 of 2 connections; Q58 failed in 2 of 2 connections; Q59 failed in 2 of 2 connections; Q60 failed in 2 of 2 connections; Q61 failed in 2 of 2 connections; Q62 failed in 2 of 2 connections; Q63 failed in 2 of 2 connections; Q64 failed in 2 of 2 connections; Q65 failed in 2 of 2 connections; Q66 failed in 2 of 2 connections; Q67 failed in 2 of 2 connections; Q68 failed in 2 of 2 connections; Q69 failed in 2 of 2 connections; Q70 failed in 2 of 2 connections; Q71 failed in 2 of 2 connections; Q72 failed in 2 of 2 connections; Q73 failed in 2 of 2 connections; Q74 failed in 2 of 2 connections; Q75 failed in 2 of 2 connections; Q76 failed in 2 of 2 connections; Q77 failed in 2 of 2 connections; Q78 failed in 2 of 2 connections; Q79 failed in 2 of 2 connections; Q80 failed in 2 of 2 connections; Q81 failed in 2 of 2 connections; Q82 failed in 2 of 2 connections; Q83 failed in 2 of 2 connections; Q84 failed in 2 of 2 connections; Q85 failed in 2 of 2 connections; Q86 failed in 2 of 2 connections; Q87 failed in 2 of 2 connections; Q88 failed in 2 of 2 connections; Q89 failed in 2 of 2 connections; Q90 failed in 2 of 2 connections; Q91 failed in 2 of 2 connections; Q92 failed in 2 of 2 connections; Q93 failed in 2 of 2 connections; Q94 failed in 2 of 2 connections; Q95 failed in 2 of 2 connections; Q96 failed in 2 of 2 connections; Q97 failed in 2 of 2 connections; Q98 failed in 2 of 2 connections; Q99 failed in 2 of 2 connections; Q100 failed in 2 of 2 connections; Q101 failed in 2 of 2 connections; Q102 failed in 2 of 2 connections; Q103 failed in 2 of 2 connections; Q104 failed in 2 of 2 connections; Q105 failed in 2 of 2 connections; Q106 failed in 2 of 2 connections; Q107 failed in 2 of 2 connections; Q108 failed in 2 of 2 connections; Q109 failed in 2 of 2 connections; Q110 failed in 2 of 2 connections; Q111 failed in 2 of 2 connections; Q112 failed in 2 of 2 connections; Q113 failed in 2 of 2 connections; Q114 failed in 2 of 2 connections; Q115 failed in 2 of 2 connections; Q116 failed in 2 of 2 connections; Q117 failed in 2 of 2 connections; Q118 failed in 2 of 2 connections; Q119 failed in 2 of 2 connections; Q120 failed in 2 of 2 connections; Q121 failed in 2 of 2 connections; Q122 failed in 2 of 2 connections; Q123 failed in 2 of 2 connections; Q124 failed in 2 of 2 connections; Q125 failed in 2 of 2 connections; Q126 failed in 2 of 2 connections; Q127 failed in 2 of 2 connections; Q128 failed in 2 of 2 connections; Q129 failed in 2 of 2 connections; Q130 failed in 2 of 2 connections; Q131 failed in 2 of 2 connections; Q132 failed in 2 of 2 connections; Q133 failed in 2 of 2 connections; Q134 failed in 2 of 2 connections; Q135 failed in 2 of 2 connections; Q136 failed in 2 of 2 connections; Q137 failed in 2 of 2 connections; Q138 failed in 2 of 2 connections; Q139 failed in 2 of 2 connections; Q140 failed in 2 of 2 connections; Q141 failed in 2 of 2 connections; Q142 failed in 2 of 2 connections; Q143 failed in 2 of 2 connections; Q144 failed in 2 of 2 connections; Q145 failed in 2 of 2 connections; Q146 failed in 2 of 2 connections; Q147 failed in 2 of 2 connections; Q148 failed in 2 of 2 connections; Q149 failed in 2 of 2 connections; Q150 failed in 2 of 2 connections; Q151 failed in 2 of 2 connections; Q152 failed in 2 of 2 connections; Q153 failed in 2 of 2 connections; Q154 failed in 2 of 2 connections; Q155 failed in 2 of 2 connections; Q156 failed in 2 of 2 connections; Q157 failed in 2 of 2 connections; Q158 failed in 2 of 2 connections; Q159 failed in 2 of 2 connections; Q160 failed in 2 of 2 connections; Q161 failed in 2 of 2 connections; Q162 failed in 2 of 2 connections; Q163 failed in 2 of 2 connections; Q164 failed in 2 of 2 connections; Q165 failed in 2 of 2 connections; Q166 failed in 2 of 2 connections; Q167 failed in 2 of 2 connections; Q168 failed in 2 of 2 connections; Q169 failed in 2 of 2 connections; Q170 failed in 2 of 2 connections; Q171 failed in 2 of 2 connections; Q172 failed in 2 of 2 connections; Q173 failed in 2 of 2 connections; Q174 failed in 2 of 2 connections; Q175 failed in 2 of 2 connections; Q176 failed in 2 of 2 connections; Q177 failed in 2 of 2 connections; Q178 failed in 2 of 2 connections; Q179 failed in 2 of 2 connections; Q180 failed in 2 of 2 connections; Q181 failed in 2 of 2 connections; Q182 failed in 2 of 2 connections; Q183 failed in 2 of 2 connections; Q184 failed in 2 of 2 connections; Q185 failed in 2 of 2 connections; Q186 failed in 2 of 2 connections; Q187 failed in 2 of 2 connections; Q188 failed in 2 of 2 connections; Q189 failed in 2 of 2 connections; Q190 failed in 2 of 2 connections; Q191 failed in 2 of 2 connections; Q192 failed in 2 of 2 connections; Q193 failed in 2 of 2 connections; Q194 failed in 2 of 2 connections; Q195 failed in 2 of 2 connections; Q196 failed in 2 of 2 connections; Q197 failed in 2 of 2 connections; Q198 failed in 2 of 2 connections; Q199 failed in 2 of 2 connections; Q200 failed in 2 of 2 connections; Q201 failed in 2 of 2 connections; Q202 failed in 2 of 2 connections; Q203 failed in 2 of 2 connections; Q204 failed in 2 of 2 connections; Q205 failed in 2 of 2 connections; Q206 failed in 2 of 2 connections; Q207 failed in 2 of 2 connections; Q208 failed in 2 of 2 connections; Q209 failed in 2 of 2 connections; Q210 failed in 2 of 2 connections; Q211 failed in 2 of 2 connections; Q212 failed in 2 of 2 connections; Q213 failed in 2 of 2 connections; Q214 failed in 2 of 2 connections; Q215 failed in 2 of 2 connections; Q216 failed in 2 of 2 connections; Q217 failed in 2 of 2 connections; Q218 failed in 2 of 2 connections; Q219 failed in 2 of 2 connections; Q220 failed in 2 of 2 connections; Q221 failed in 2 of 2 connections; Q222 failed in 2 of 2 connections; Q223 failed in 2 of 2 connections; Q224 failed in 2 of 2 connections; Q225 failed in 2 of 2 connections; Q226 failed in 2 of 2 connections; Q227 failed in 2 of 2 connections; Q228 failed in 2 of 2 connections; Q229 failed in 2 of 2 connections; Q230 failed in 2 of 2 connections; Q231 failed in 2 of 2 connections; Q232 failed in 2 of 2 connections; Q233 failed in 2 of 2 connections; Q234 failed in 2 of 2 connections; Q235 failed in 2 of 2 connections; Q236 failed in 2 of 2 connections; Q237 failed in 2 of 2 connections; Q238 failed in 2 of 2 connections; Q239 failed in 2 of 2 connections; Q240 failed in 2 of 2 connections; Q241 failed in 2 of 2 connections; Q242 failed in 2 of 2 connections; Q243 failed in 2 of 2 connections; Q244 failed in 2 of 2 connections; Q245 failed in 2 of 2 connections; Q246 failed in 2 of 2 connections; Q247 failed in 2 of 2 connections; Q248 failed in 2 of 2 connections; Q249 failed in 2 of 2 connections; Q250 failed in 2 of 2 connections; Q251 failed in 2 of 2 connections; Q252 failed in 2 of 2 connections; Q253 failed in 2 of 2 connections; Q254 failed in 2 of 2 connections; Q255 failed in 2 of 2 connections; Q256 failed in 2 of 2 connections; Q257 failed in 2 of 2 connections; Q258 failed in 2 of 2 connections; Q259 failed in 2 of 2 connections; Q260 failed in 2 of 2 connections; Q261 failed in 2 of 2 connections; Q262 failed in 2 of 2 connections; Q263 failed in 2 of 2 connections; Q264 failed in 2 of 2 connections; Q265 failed in 2 of 2 connections; Q266 failed in 2 of 2 connections; Q267 failed in 2 of 2 connections; Q268 failed in 2 of 2 connections; Q269 failed in 2 of 2 connections; Q270 failed in 2 of 2 connections; Q271 failed in 2 of 2 connections; Q272 failed in 2 of 2 connections; Q273 failed in 2 of 2 connections; Q274 failed in 2 of 2 connections; Q275 failed in 2 of 2 connections; Q276 failed in 2 of 2 connections; Q277 failed in 2 of 2 connections; Q278 failed in 2 of 2 connections; Q279 failed in 2 of 2 connections; Q280 failed in 2 of 2 connections; Q281 failed in 2 of 2 connections; Q282 failed in 2 of 2 connections; Q283 failed in 2 of 2 connections; Q284 failed in 2 of 2 connections; Q285 failed in 2 of 2 connections; Q286 failed in 2 of 2 connections; Q287 failed in 2 of 2 connections; Q288 failed in 2 of 2 connections; Q289 failed in 2 of 2 connections; Q290 failed in 2 of 2 connections; Q291 failed in 2 of 2 connections; Q292 failed in 2 of 2 connections; Q293 failed in 2 of 2 connections; Q294 failed in 2 of 2 connections; Q295 failed in 2 of 2 connections; Q296 failed in 2 of 2 connections; Q297 failed in 2 of 2 connections; Q298 failed in 2 of 2 connections; Q299 failed in 2 of 2 connections; Q300 failed in 2 of 2 connections; Q301 failed in 2 of 2 connections; Q302 failed in 2 of 2 connections; Q303 failed in 2 of 2 connections; Q304 failed in 2 of 2 connections; Q305 failed in 2 of 2 connections; Q306 failed in 2 of 2 connections; Q307 failed in 2 of 2 connections; Q308 failed in 2 of 2 connections; Q309 failed in 2 of 2 connections; Q310 failed in 2 of 2 connections; Q311 failed in 2 of 2 connections; Q312 failed in 2 of 2 connections; Q313 failed in 2 of 2 connections; Q314 failed in 2 of 2 connections; Q315 failed in 2 of 2 connections; Q316 failed in 2 of 2 connections; Q317 failed in 2 of 2 connections; Q318 failed in 2 of 2 connections; Q319 failed in 2 of 2 connections; Q320 failed in 2 of 2 connections; Q321 failed in 2 of 2 connections; Q322 failed in 2 of 2 connections; Q323 failed in 2 of 2 connections; Q324 failed in 2 of 2 connections; Q325 failed in 2 of 2 connections; Q326 failed in 2 of 2 connections; Q327 failed in 2 of 2 connections; Q328 failed in 2 of 2 connections; Q329 failed in 2 of 2 connections; Q330 failed in 2 of 2 connections; Q331 failed in 2 of 2 connections; Q332 failed in 2 of 2 connections; Q333 failed in 2 of 2 connections; Q334 failed in 2 of 2 connections; Q335 failed in 2 of 2 connections; Q336 failed in 2 of 2 connections; Q337 failed in 2 of 2 connections; Q338 failed in 2 of 2 connections; Q339 failed in 2 of 2 connections; Q340 failed in 2 of 2 connections; Q341 failed in 2 of 2 connections; Q342 failed in 2 of 2 connections; Q343 failed in 2 of 2 connections; Q344 failed in 2 of 2 connections; Q345 failed in 2 of 2 connections; Q346 failed in 2 of 2 connections; Q347 failed in 2 of 2 connections; Q348 failed in 2 of 2 connections; Q349 failed in 2 of 2 connections; Q350 failed in 2 of 2 connections; Q351 failed in 2 of 2 connections; Q352 failed in 2 of 2 connections; Q353 failed in 2 of 2 connections; Q354 failed in 2 of 2 connections; Q355 failed in 2 of 2 connections; Q356 failed in 2 of 2 connections; Q357 failed in 2 of 2 connections; Q358 failed in 2 of 2 connections; Q359 failed in 2 of 2 connections; Q360 failed in 2 of 2 connections; Q361 failed in 2 of 2 connections; Q362 failed in 2 of 2 connections; Q363 failed in 2 of 2 connections; Q364 failed in 2 of 2 connections; Q365 failed in 2 of 2 connections; Q366 failed in 2 of 2 connections; Q367 failed in 2 of 2 connections; Q368 failed in 2 of 2 connections; Q369 failed in 2 of 2 connections; Q370 failed in 2 of 2 connections; Q371 failed in 2 of 2 connections; Q372 failed in 2 of 2 connections; Q373 failed in 2 of 2 connections; Q374 failed in 2 of 2 connections; Q375 failed in 2 of 2 connections; Q376 failed in 2 of 2 connections; Q377 failed in 2 of 2 connections; Q378 failed in 2 of 2 connections; Q379 failed in 2 of 2 connections; Q380 failed in 2 of 2 connections; Q381 failed in 2 of 2 connections; Q382 failed in 2 of 2 connections; Q383 failed in 2 of 2 connections; Q384 failed in 2 of 2 connections; Q385 failed in 2 of 2 connections; Q386 failed in 2 of 2 connections; Q387 failed in 2 of 2 connections; Q388 failed in 2 of 2 connections; Q389 failed in 2 of 2 connections; Q390 failed in 2 of 2 connections; Q391 failed in 2 of 2 connections; Q392 failed in 2 of 2 connections; Q393 failed in 2 of 2 connections; Q394 failed in 2 of 2 connections; Q395 failed in 2 of 2 connections; Q396 failed in 2 of 2 connections; Q397 failed in 2 of 2 connections; Q398 failed in 2 of 2 connections; Q399 failed in 2 of 2 connections; Q400 failed in 2 of 2 connections; Q401 failed in 2 of 2 connections; Q402 failed in 2 of 2 connections; Q403 failed in 2 of 2 connections; Q404 failed in 2 of 2 connections; Q405 failed in 2 of 2 connections; Q406 failed in 2 of 2 connections; Q407 failed in 2 of 2 connections; Q408 failed in 2 of 2 connections; Q409 failed in 2 of 2 connections; Q410 failed in 2 of 2 connections; Q411 failed in 2 of 2 connections; Q412 failed in 2 of 2 connections; Q413 failed in 2 of 2 connections; Q414 failed in 2 of 2 connections; Q415 failed in 2 of 2 connections; Q416 failed in 2 of 2 connections; Q417 failed in 2 of 2 connections; Q418 failed in 2 of 2 connections; Q419 failed in 2 of 2 connections; Q420 failed in 2 of 2 connections; Q421 failed in 2 of 2 connections; Q422 failed in 2 of 2 connections; Q423 failed in 2 of 2 connections; Q424 failed in 2 of 2 connections; Q425 failed in 2 of 2 connections; Q426 failed in 2 of 2 connections; Q427 failed in 2 of 2 connections; Q428 failed in 2 of 2 connections; Q429 failed in 2 of 2 connections). See Query Completion per Phase for where, and Per Phase (Complete Phases Only) for the phases that completed every query.

#### Query Completion per Phase

| phase            |   pods | statistics_tab about call_center.cc_call_center_sk - all   | statistics_tab about call_center.cc_call_center_id - all   | statistics_tab about call_center.cc_rec_start_date - all   | statistics_tab about call_center.cc_rec_end_date - all   | statistics_tab about call_center.cc_closed_date_sk - all   | statistics_tab about call_center.cc_open_date_sk - all   | statistics_tab about call_center.cc_name - all   | statistics_tab about call_center.cc_class - all   | statistics_tab about call_center.cc_employees - all   | statistics_tab about call_center.cc_sq_ft - all   | statistics_tab about call_center.cc_hours - all   | statistics_tab about call_center.cc_manager - all   | statistics_tab about call_center.cc_mkt_id - all   | statistics_tab about call_center.cc_mkt_class - all   | statistics_tab about call_center.cc_mkt_desc - all   | statistics_tab about call_center.cc_market_manager - all   | statistics_tab about call_center.cc_division - all   | statistics_tab about call_center.cc_division_name - all   | statistics_tab about call_center.cc_company - all   | statistics_tab about call_center.cc_company_name - all   | statistics_tab about call_center.cc_street_number - all   | statistics_tab about call_center.cc_street_name - all   | statistics_tab about call_center.cc_street_type - all   | statistics_tab about call_center.cc_suite_number - all   | statistics_tab about call_center.cc_city - all   | statistics_tab about call_center.cc_county - all   | statistics_tab about call_center.cc_state - all   | statistics_tab about call_center.cc_zip - all   | statistics_tab about call_center.cc_country - all   | statistics_tab about call_center.cc_gmt_offset - all   | statistics_tab about call_center.cc_tax_percentage - all   | statistics_tab about catalog_page.cp_catalog_page_sk - all   | statistics_tab about catalog_page.cp_catalog_page_id - all   | statistics_tab about catalog_page.cp_start_date_sk - all   | statistics_tab about catalog_page.cp_end_date_sk - all   | statistics_tab about catalog_page.cp_department - all   | statistics_tab about catalog_page.cp_catalog_number - all   | statistics_tab about catalog_page.cp_catalog_page_number - all   | statistics_tab about catalog_page.cp_description - all   | statistics_tab about catalog_page.cp_type - all   | statistics_tab about catalog_returns.cr_returned_date_sk - all   | statistics_tab about catalog_returns.cr_returned_time_sk - all   | statistics_tab about catalog_returns.cr_item_sk - all   | statistics_tab about catalog_returns.cr_refunded_customer_sk - all   | statistics_tab about catalog_returns.cr_refunded_cdemo_sk - all   | statistics_tab about catalog_returns.cr_refunded_hdemo_sk - all   | statistics_tab about catalog_returns.cr_refunded_addr_sk - all   | statistics_tab about catalog_returns.cr_returning_customer_sk - all   | statistics_tab about catalog_returns.cr_returning_cdemo_sk - all   | statistics_tab about catalog_returns.cr_returning_hdemo_sk - all   | statistics_tab about catalog_returns.cr_returning_addr_sk - all   | statistics_tab about catalog_returns.cr_call_center_sk - all   | statistics_tab about catalog_returns.cr_catalog_page_sk - all   | statistics_tab about catalog_returns.cr_ship_mode_sk - all   | statistics_tab about catalog_returns.cr_warehouse_sk - all   | statistics_tab about catalog_returns.cr_reason_sk - all   | statistics_tab about catalog_returns.cr_order_number - all   | statistics_tab about catalog_returns.cr_return_quantity - all   | statistics_tab about catalog_returns.cr_return_amount - all   | statistics_tab about catalog_returns.cr_return_tax - all   | statistics_tab about catalog_returns.cr_return_amt_inc_tax - all   | statistics_tab about catalog_returns.cr_fee - all   | statistics_tab about catalog_returns.cr_return_ship_cost - all   | statistics_tab about catalog_returns.cr_refunded_cash - all   | statistics_tab about catalog_returns.cr_reversed_charge - all   | statistics_tab about catalog_returns.cr_store_credit - all   | statistics_tab about catalog_returns.cr_net_loss - all   | statistics_tab about catalog_sales.cs_sold_date_sk - all   | statistics_tab about catalog_sales.cs_sold_time_sk - all   | statistics_tab about catalog_sales.cs_ship_date_sk - all   | statistics_tab about catalog_sales.cs_bill_customer_sk - all   | statistics_tab about catalog_sales.cs_bill_cdemo_sk - all   | statistics_tab about catalog_sales.cs_bill_hdemo_sk - all   | statistics_tab about catalog_sales.cs_bill_addr_sk - all   | statistics_tab about catalog_sales.cs_ship_customer_sk - all   | statistics_tab about catalog_sales.cs_ship_cdemo_sk - all   | statistics_tab about catalog_sales.cs_ship_hdemo_sk - all   | statistics_tab about catalog_sales.cs_ship_addr_sk - all   | statistics_tab about catalog_sales.cs_call_center_sk - all   | statistics_tab about catalog_sales.cs_catalog_page_sk - all   | statistics_tab about catalog_sales.cs_ship_mode_sk - all   | statistics_tab about catalog_sales.cs_warehouse_sk - all   | statistics_tab about catalog_sales.cs_item_sk - all   | statistics_tab about catalog_sales.cs_promo_sk - all   | statistics_tab about catalog_sales.cs_order_number - all   | statistics_tab about catalog_sales.cs_quantity - all   | statistics_tab about catalog_sales.cs_wholesale_cost - all   | statistics_tab about catalog_sales.cs_list_price - all   | statistics_tab about catalog_sales.cs_sales_price - all   | statistics_tab about catalog_sales.cs_ext_discount_amt - all   | statistics_tab about catalog_sales.cs_ext_sales_price - all   | statistics_tab about catalog_sales.cs_ext_wholesale_cost - all   | statistics_tab about catalog_sales.cs_ext_list_price - all   | statistics_tab about catalog_sales.cs_ext_tax - all   | statistics_tab about catalog_sales.cs_coupon_amt - all   | statistics_tab about catalog_sales.cs_ext_ship_cost - all   | statistics_tab about catalog_sales.cs_net_paid - all   | statistics_tab about catalog_sales.cs_net_paid_inc_tax - all   | statistics_tab about catalog_sales.cs_net_paid_inc_ship - all   | statistics_tab about catalog_sales.cs_net_paid_inc_ship_tax - all   | statistics_tab about catalog_sales.cs_net_profit - all   | statistics_tab about customer.c_customer_sk - all   | statistics_tab about customer.c_customer_id - all   | statistics_tab about customer.c_current_cdemo_sk - all   | statistics_tab about customer.c_current_hdemo_sk - all   | statistics_tab about customer.c_current_addr_sk - all   | statistics_tab about customer.c_first_shipto_date_sk - all   | statistics_tab about customer.c_first_sales_date_sk - all   | statistics_tab about customer.c_salutation - all   | statistics_tab about customer.c_first_name - all   | statistics_tab about customer.c_last_name - all   | statistics_tab about customer.c_preferred_cust_flag - all   | statistics_tab about customer.c_birth_day - all   | statistics_tab about customer.c_birth_month - all   | statistics_tab about customer.c_birth_year - all   | statistics_tab about customer.c_birth_country - all   | statistics_tab about customer.c_login - all   | statistics_tab about customer.c_email_address - all   | statistics_tab about customer.c_last_review_date - all   | statistics_tab about customer_address.ca_address_sk - all   | statistics_tab about customer_address.ca_address_id - all   | statistics_tab about customer_address.ca_street_number - all   | statistics_tab about customer_address.ca_street_name - all   | statistics_tab about customer_address.ca_street_type - all   | statistics_tab about customer_address.ca_suite_number - all   | statistics_tab about customer_address.ca_city - all   | statistics_tab about customer_address.ca_county - all   | statistics_tab about customer_address.ca_state - all   | statistics_tab about customer_address.ca_zip - all   | statistics_tab about customer_address.ca_country - all   | statistics_tab about customer_address.ca_gmt_offset - all   | statistics_tab about customer_address.ca_location_type - all   | statistics_tab about customer_demographics.cd_demo_sk - all   | statistics_tab about customer_demographics.cd_gender - all   | statistics_tab about customer_demographics.cd_marital_status - all   | statistics_tab about customer_demographics.cd_education_status - all   | statistics_tab about customer_demographics.cd_purchase_estimate - all   | statistics_tab about customer_demographics.cd_credit_rating - all   | statistics_tab about customer_demographics.cd_dep_count - all   | statistics_tab about customer_demographics.cd_dep_employed_count - all   | statistics_tab about customer_demographics.cd_dep_college_count - all   | statistics_tab about date_dim.d_date_sk - all   | statistics_tab about date_dim.d_date_id - all   | statistics_tab about date_dim.d_date - all   | statistics_tab about date_dim.d_month_seq - all   | statistics_tab about date_dim.d_week_seq - all   | statistics_tab about date_dim.d_quarter_seq - all   | statistics_tab about date_dim.d_year - all   | statistics_tab about date_dim.d_dow - all   | statistics_tab about date_dim.d_moy - all   | statistics_tab about date_dim.d_dom - all   | statistics_tab about date_dim.d_qoy - all   | statistics_tab about date_dim.d_fy_year - all   | statistics_tab about date_dim.d_fy_quarter_seq - all   | statistics_tab about date_dim.d_fy_week_seq - all   | statistics_tab about date_dim.d_day_name - all   | statistics_tab about date_dim.d_quarter_name - all   | statistics_tab about date_dim.d_holiday - all   | statistics_tab about date_dim.d_weekend - all   | statistics_tab about date_dim.d_following_holiday - all   | statistics_tab about date_dim.d_first_dom - all   | statistics_tab about date_dim.d_last_dom - all   | statistics_tab about date_dim.d_same_day_ly - all   | statistics_tab about date_dim.d_same_day_lq - all   | statistics_tab about date_dim.d_current_day - all   | statistics_tab about date_dim.d_current_week - all   | statistics_tab about date_dim.d_current_month - all   | statistics_tab about date_dim.d_current_quarter - all   | statistics_tab about date_dim.d_current_year - all   | statistics_tab about dbgen_version.dv_version - all   | statistics_tab about dbgen_version.dv_create_date - all   | statistics_tab about dbgen_version.dv_create_time - all   | statistics_tab about dbgen_version.dv_cmdline_args - all   | statistics_tab about household_demographics.hd_demo_sk - all   | statistics_tab about household_demographics.hd_income_band_sk - all   | statistics_tab about household_demographics.hd_buy_potential - all   | statistics_tab about household_demographics.hd_dep_count - all   | statistics_tab about household_demographics.hd_vehicle_count - all   | statistics_tab about income_band.ib_income_band_sk - all   | statistics_tab about income_band.ib_lower_bound - all   | statistics_tab about income_band.ib_upper_bound - all   | statistics_tab about inventory.inv_date_sk - all   | statistics_tab about inventory.inv_item_sk - all   | statistics_tab about inventory.inv_warehouse_sk - all   | statistics_tab about inventory.inv_quantity_on_hand - all   | statistics_tab about item.i_item_sk - all   | statistics_tab about item.i_item_id - all   | statistics_tab about item.i_rec_start_date - all   | statistics_tab about item.i_rec_end_date - all   | statistics_tab about item.i_item_desc - all   | statistics_tab about item.i_current_price - all   | statistics_tab about item.i_wholesale_cost - all   | statistics_tab about item.i_brand_id - all   | statistics_tab about item.i_brand - all   | statistics_tab about item.i_class_id - all   | statistics_tab about item.i_class - all   | statistics_tab about item.i_category_id - all   | statistics_tab about item.i_category - all   | statistics_tab about item.i_manufact_id - all   | statistics_tab about item.i_manufact - all   | statistics_tab about item.i_size - all   | statistics_tab about item.i_formulation - all   | statistics_tab about item.i_color - all   | statistics_tab about item.i_units - all   | statistics_tab about item.i_container - all   | statistics_tab about item.i_manager_id - all   | statistics_tab about item.i_product_name - all   | statistics_tab about promotion.p_promo_sk - all   | statistics_tab about promotion.p_promo_id - all   | statistics_tab about promotion.p_start_date_sk - all   | statistics_tab about promotion.p_end_date_sk - all   | statistics_tab about promotion.p_item_sk - all   | statistics_tab about promotion.p_cost - all   | statistics_tab about promotion.p_response_target - all   | statistics_tab about promotion.p_promo_name - all   | statistics_tab about promotion.p_channel_dmail - all   | statistics_tab about promotion.p_channel_email - all   | statistics_tab about promotion.p_channel_catalog - all   | statistics_tab about promotion.p_channel_tv - all   | statistics_tab about promotion.p_channel_radio - all   | statistics_tab about promotion.p_channel_press - all   | statistics_tab about promotion.p_channel_event - all   | statistics_tab about promotion.p_channel_demo - all   | statistics_tab about promotion.p_channel_details - all   | statistics_tab about promotion.p_purpose - all   | statistics_tab about promotion.p_discount_active - all   | statistics_tab about reason.r_reason_sk - all   | statistics_tab about reason.r_reason_id - all   | statistics_tab about reason.r_reason_desc - all   | statistics_tab about ship_mode.sm_ship_mode_sk - all   | statistics_tab about ship_mode.sm_ship_mode_id - all   | statistics_tab about ship_mode.sm_type - all   | statistics_tab about ship_mode.sm_code - all   | statistics_tab about ship_mode.sm_carrier - all   | statistics_tab about ship_mode.sm_contract - all   | statistics_tab about store.s_store_sk - all   | statistics_tab about store.s_store_id - all   | statistics_tab about store.s_rec_start_date - all   | statistics_tab about store.s_rec_end_date - all   | statistics_tab about store.s_closed_date_sk - all   | statistics_tab about store.s_store_name - all   | statistics_tab about store.s_number_employees - all   | statistics_tab about store.s_floor_space - all   | statistics_tab about store.s_hours - all   | statistics_tab about store.s_manager - all   | statistics_tab about store.s_market_id - all   | statistics_tab about store.s_geography_class - all   | statistics_tab about store.s_market_desc - all   | statistics_tab about store.s_market_manager - all   | statistics_tab about store.s_division_id - all   | statistics_tab about store.s_division_name - all   | statistics_tab about store.s_company_id - all   | statistics_tab about store.s_company_name - all   | statistics_tab about store.s_street_number - all   | statistics_tab about store.s_street_name - all   | statistics_tab about store.s_street_type - all   | statistics_tab about store.s_suite_number - all   | statistics_tab about store.s_city - all   | statistics_tab about store.s_county - all   | statistics_tab about store.s_state - all   | statistics_tab about store.s_zip - all   | statistics_tab about store.s_country - all   | statistics_tab about store.s_gmt_offset - all   | statistics_tab about store.s_tax_precentage - all   | statistics_tab about store_returns.sr_returned_date_sk - all   | statistics_tab about store_returns.sr_return_time_sk - all   | statistics_tab about store_returns.sr_item_sk - all   | statistics_tab about store_returns.sr_customer_sk - all   | statistics_tab about store_returns.sr_cdemo_sk - all   | statistics_tab about store_returns.sr_hdemo_sk - all   | statistics_tab about store_returns.sr_addr_sk - all   | statistics_tab about store_returns.sr_store_sk - all   | statistics_tab about store_returns.sr_reason_sk - all   | statistics_tab about store_returns.sr_ticket_number - all   | statistics_tab about store_returns.sr_return_quantity - all   | statistics_tab about store_returns.sr_return_amt - all   | statistics_tab about store_returns.sr_return_tax - all   | statistics_tab about store_returns.sr_return_amt_inc_tax - all   | statistics_tab about store_returns.sr_fee - all   | statistics_tab about store_returns.sr_return_ship_cost - all   | statistics_tab about store_returns.sr_refunded_cash - all   | statistics_tab about store_returns.sr_reversed_charge - all   | statistics_tab about store_returns.sr_store_credit - all   | statistics_tab about store_returns.sr_net_loss - all   | statistics_tab about store_sales.ss_sold_date_sk - all   | statistics_tab about store_sales.ss_sold_time_sk - all   | statistics_tab about store_sales.ss_item_sk - all   | statistics_tab about store_sales.ss_customer_sk - all   | statistics_tab about store_sales.ss_cdemo_sk - all   | statistics_tab about store_sales.ss_hdemo_sk - all   | statistics_tab about store_sales.ss_addr_sk - all   | statistics_tab about store_sales.ss_store_sk - all   | statistics_tab about store_sales.ss_promo_sk - all   | statistics_tab about store_sales.ss_ticket_number - all   | statistics_tab about store_sales.ss_quantity - all   | statistics_tab about store_sales.ss_wholesale_cost - all   | statistics_tab about store_sales.ss_list_price - all   | statistics_tab about store_sales.ss_sales_price - all   | statistics_tab about store_sales.ss_ext_discount_amt - all   | statistics_tab about store_sales.ss_ext_sales_price - all   | statistics_tab about store_sales.ss_ext_wholesale_cost - all   | statistics_tab about store_sales.ss_ext_list_price - all   | statistics_tab about store_sales.ss_ext_tax - all   | statistics_tab about store_sales.ss_coupon_amt - all   | statistics_tab about store_sales.ss_net_paid - all   | statistics_tab about store_sales.ss_net_paid_inc_tax - all   | statistics_tab about store_sales.ss_net_profit - all   | statistics_tab about time_dim.t_time_sk - all   | statistics_tab about time_dim.t_time_id - all   | statistics_tab about time_dim.t_time - all   | statistics_tab about time_dim.t_hour - all   | statistics_tab about time_dim.t_minute - all   | statistics_tab about time_dim.t_second - all   | statistics_tab about time_dim.t_am_pm - all   | statistics_tab about time_dim.t_shift - all   | statistics_tab about time_dim.t_sub_shift - all   | statistics_tab about time_dim.t_meal_time - all   | statistics_tab about warehouse.w_warehouse_sk - all   | statistics_tab about warehouse.w_warehouse_id - all   | statistics_tab about warehouse.w_warehouse_name - all   | statistics_tab about warehouse.w_warehouse_sq_ft - all   | statistics_tab about warehouse.w_street_number - all   | statistics_tab about warehouse.w_street_name - all   | statistics_tab about warehouse.w_street_type - all   | statistics_tab about warehouse.w_suite_number - all   | statistics_tab about warehouse.w_city - all   | statistics_tab about warehouse.w_county - all   | statistics_tab about warehouse.w_state - all   | statistics_tab about warehouse.w_zip - all   | statistics_tab about warehouse.w_country - all   | statistics_tab about warehouse.w_gmt_offset - all   | statistics_tab about web_page.wp_web_page_sk - all   | statistics_tab about web_page.wp_web_page_id - all   | statistics_tab about web_page.wp_rec_start_date - all   | statistics_tab about web_page.wp_rec_end_date - all   | statistics_tab about web_page.wp_creation_date_sk - all   | statistics_tab about web_page.wp_access_date_sk - all   | statistics_tab about web_page.wp_autogen_flag - all   | statistics_tab about web_page.wp_customer_sk - all   | statistics_tab about web_page.wp_url - all   | statistics_tab about web_page.wp_type - all   | statistics_tab about web_page.wp_char_count - all   | statistics_tab about web_page.wp_link_count - all   | statistics_tab about web_page.wp_image_count - all   | statistics_tab about web_page.wp_max_ad_count - all   | statistics_tab about web_returns.wr_returned_date_sk - all   | statistics_tab about web_returns.wr_returned_time_sk - all   | statistics_tab about web_returns.wr_item_sk - all   | statistics_tab about web_returns.wr_refunded_customer_sk - all   | statistics_tab about web_returns.wr_refunded_cdemo_sk - all   | statistics_tab about web_returns.wr_refunded_hdemo_sk - all   | statistics_tab about web_returns.wr_refunded_addr_sk - all   | statistics_tab about web_returns.wr_returning_customer_sk - all   | statistics_tab about web_returns.wr_returning_cdemo_sk - all   | statistics_tab about web_returns.wr_returning_hdemo_sk - all   | statistics_tab about web_returns.wr_returning_addr_sk - all   | statistics_tab about web_returns.wr_web_page_sk - all   | statistics_tab about web_returns.wr_reason_sk - all   | statistics_tab about web_returns.wr_order_number - all   | statistics_tab about web_returns.wr_return_quantity - all   | statistics_tab about web_returns.wr_return_amt - all   | statistics_tab about web_returns.wr_return_tax - all   | statistics_tab about web_returns.wr_return_amt_inc_tax - all   | statistics_tab about web_returns.wr_fee - all   | statistics_tab about web_returns.wr_return_ship_cost - all   | statistics_tab about web_returns.wr_refunded_cash - all   | statistics_tab about web_returns.wr_reversed_charge - all   | statistics_tab about web_returns.wr_account_credit - all   | statistics_tab about web_returns.wr_net_loss - all   | statistics_tab about web_sales.ws_sold_date_sk - all   | statistics_tab about web_sales.ws_sold_time_sk - all   | statistics_tab about web_sales.ws_ship_date_sk - all   | statistics_tab about web_sales.ws_item_sk - all   | statistics_tab about web_sales.ws_bill_customer_sk - all   | statistics_tab about web_sales.ws_bill_cdemo_sk - all   | statistics_tab about web_sales.ws_bill_hdemo_sk - all   | statistics_tab about web_sales.ws_bill_addr_sk - all   | statistics_tab about web_sales.ws_ship_customer_sk - all   | statistics_tab about web_sales.ws_ship_cdemo_sk - all   | statistics_tab about web_sales.ws_ship_hdemo_sk - all   | statistics_tab about web_sales.ws_ship_addr_sk - all   | statistics_tab about web_sales.ws_web_page_sk - all   | statistics_tab about web_sales.ws_web_site_sk - all   | statistics_tab about web_sales.ws_ship_mode_sk - all   | statistics_tab about web_sales.ws_warehouse_sk - all   | statistics_tab about web_sales.ws_promo_sk - all   | statistics_tab about web_sales.ws_order_number - all   | statistics_tab about web_sales.ws_quantity - all   | statistics_tab about web_sales.ws_wholesale_cost - all   | statistics_tab about web_sales.ws_list_price - all   | statistics_tab about web_sales.ws_sales_price - all   | statistics_tab about web_sales.ws_ext_discount_amt - all   | statistics_tab about web_sales.ws_ext_sales_price - all   | statistics_tab about web_sales.ws_ext_wholesale_cost - all   | statistics_tab about web_sales.ws_ext_list_price - all   | statistics_tab about web_sales.ws_ext_tax - all   | statistics_tab about web_sales.ws_coupon_amt - all   | statistics_tab about web_sales.ws_ext_ship_cost - all   | statistics_tab about web_sales.ws_net_paid - all   | statistics_tab about web_sales.ws_net_paid_inc_tax - all   | statistics_tab about web_sales.ws_net_paid_inc_ship - all   | statistics_tab about web_sales.ws_net_paid_inc_ship_tax - all   | statistics_tab about web_sales.ws_net_profit - all   | statistics_tab about web_site.web_site_sk - all   | statistics_tab about web_site.web_site_id - all   | statistics_tab about web_site.web_rec_start_date - all   | statistics_tab about web_site.web_rec_end_date - all   | statistics_tab about web_site.web_name - all   | statistics_tab about web_site.web_open_date_sk - all   | statistics_tab about web_site.web_close_date_sk - all   | statistics_tab about web_site.web_class - all   | statistics_tab about web_site.web_manager - all   | statistics_tab about web_site.web_mkt_id - all   | statistics_tab about web_site.web_mkt_class - all   | statistics_tab about web_site.web_mkt_desc - all   | statistics_tab about web_site.web_market_manager - all   | statistics_tab about web_site.web_company_id - all   | statistics_tab about web_site.web_company_name - all   | statistics_tab about web_site.web_street_number - all   | statistics_tab about web_site.web_street_name - all   | statistics_tab about web_site.web_street_type - all   | statistics_tab about web_site.web_suite_number - all   | statistics_tab about web_site.web_city - all   | statistics_tab about web_site.web_county - all   | statistics_tab about web_site.web_state - all   | statistics_tab about web_site.web_zip - all   | statistics_tab about web_site.web_country - all   | statistics_tab about web_site.web_gmt_offset - all   | statistics_tab about web_site.web_tax_percentage - all   | complete   |
|:-----------------|-------:|:-----------------------------------------------------------|:-----------------------------------------------------------|:-----------------------------------------------------------|:---------------------------------------------------------|:-----------------------------------------------------------|:---------------------------------------------------------|:-------------------------------------------------|:--------------------------------------------------|:------------------------------------------------------|:--------------------------------------------------|:--------------------------------------------------|:----------------------------------------------------|:---------------------------------------------------|:------------------------------------------------------|:-----------------------------------------------------|:-----------------------------------------------------------|:-----------------------------------------------------|:----------------------------------------------------------|:----------------------------------------------------|:---------------------------------------------------------|:----------------------------------------------------------|:--------------------------------------------------------|:--------------------------------------------------------|:---------------------------------------------------------|:-------------------------------------------------|:---------------------------------------------------|:--------------------------------------------------|:------------------------------------------------|:----------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------------------------|:-------------------------------------------------------------|:-------------------------------------------------------------|:-----------------------------------------------------------|:---------------------------------------------------------|:--------------------------------------------------------|:------------------------------------------------------------|:-----------------------------------------------------------------|:---------------------------------------------------------|:--------------------------------------------------|:-----------------------------------------------------------------|:-----------------------------------------------------------------|:--------------------------------------------------------|:---------------------------------------------------------------------|:------------------------------------------------------------------|:------------------------------------------------------------------|:-----------------------------------------------------------------|:----------------------------------------------------------------------|:-------------------------------------------------------------------|:-------------------------------------------------------------------|:------------------------------------------------------------------|:---------------------------------------------------------------|:----------------------------------------------------------------|:-------------------------------------------------------------|:-------------------------------------------------------------|:----------------------------------------------------------|:-------------------------------------------------------------|:----------------------------------------------------------------|:--------------------------------------------------------------|:-----------------------------------------------------------|:-------------------------------------------------------------------|:----------------------------------------------------|:-----------------------------------------------------------------|:--------------------------------------------------------------|:----------------------------------------------------------------|:-------------------------------------------------------------|:---------------------------------------------------------|:-----------------------------------------------------------|:-----------------------------------------------------------|:-----------------------------------------------------------|:---------------------------------------------------------------|:------------------------------------------------------------|:------------------------------------------------------------|:-----------------------------------------------------------|:---------------------------------------------------------------|:------------------------------------------------------------|:------------------------------------------------------------|:-----------------------------------------------------------|:-------------------------------------------------------------|:--------------------------------------------------------------|:-----------------------------------------------------------|:-----------------------------------------------------------|:------------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------------|:---------------------------------------------------------|:----------------------------------------------------------|:---------------------------------------------------------------|:--------------------------------------------------------------|:-----------------------------------------------------------------|:-------------------------------------------------------------|:------------------------------------------------------|:---------------------------------------------------------|:------------------------------------------------------------|:-------------------------------------------------------|:---------------------------------------------------------------|:----------------------------------------------------------------|:--------------------------------------------------------------------|:---------------------------------------------------------|:----------------------------------------------------|:----------------------------------------------------|:---------------------------------------------------------|:---------------------------------------------------------|:--------------------------------------------------------|:-------------------------------------------------------------|:------------------------------------------------------------|:---------------------------------------------------|:---------------------------------------------------|:--------------------------------------------------|:------------------------------------------------------------|:--------------------------------------------------|:----------------------------------------------------|:---------------------------------------------------|:------------------------------------------------------|:----------------------------------------------|:------------------------------------------------------|:---------------------------------------------------------|:------------------------------------------------------------|:------------------------------------------------------------|:---------------------------------------------------------------|:-------------------------------------------------------------|:-------------------------------------------------------------|:--------------------------------------------------------------|:------------------------------------------------------|:--------------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------------------|:---------------------------------------------------------|:------------------------------------------------------------|:---------------------------------------------------------------|:--------------------------------------------------------------|:-------------------------------------------------------------|:---------------------------------------------------------------------|:-----------------------------------------------------------------------|:------------------------------------------------------------------------|:--------------------------------------------------------------------|:----------------------------------------------------------------|:-------------------------------------------------------------------------|:------------------------------------------------------------------------|:------------------------------------------------|:------------------------------------------------|:---------------------------------------------|:--------------------------------------------------|:-------------------------------------------------|:----------------------------------------------------|:---------------------------------------------|:--------------------------------------------|:--------------------------------------------|:--------------------------------------------|:--------------------------------------------|:------------------------------------------------|:-------------------------------------------------------|:----------------------------------------------------|:-------------------------------------------------|:-----------------------------------------------------|:------------------------------------------------|:------------------------------------------------|:----------------------------------------------------------|:--------------------------------------------------|:-------------------------------------------------|:----------------------------------------------------|:----------------------------------------------------|:----------------------------------------------------|:-----------------------------------------------------|:------------------------------------------------------|:--------------------------------------------------------|:-----------------------------------------------------|:------------------------------------------------------|:----------------------------------------------------------|:----------------------------------------------------------|:-----------------------------------------------------------|:---------------------------------------------------------------|:----------------------------------------------------------------------|:---------------------------------------------------------------------|:-----------------------------------------------------------------|:---------------------------------------------------------------------|:-----------------------------------------------------------|:--------------------------------------------------------|:--------------------------------------------------------|:---------------------------------------------------|:---------------------------------------------------|:--------------------------------------------------------|:------------------------------------------------------------|:--------------------------------------------|:--------------------------------------------|:---------------------------------------------------|:-------------------------------------------------|:----------------------------------------------|:--------------------------------------------------|:---------------------------------------------------|:---------------------------------------------|:------------------------------------------|:---------------------------------------------|:------------------------------------------|:------------------------------------------------|:---------------------------------------------|:------------------------------------------------|:---------------------------------------------|:-----------------------------------------|:------------------------------------------------|:------------------------------------------|:------------------------------------------|:----------------------------------------------|:-----------------------------------------------|:-------------------------------------------------|:--------------------------------------------------|:--------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------------------|:-------------------------------------------------|:----------------------------------------------|:---------------------------------------------------------|:----------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------|:---------------------------------------------------------|:----------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------|:------------------------------------------------------|:---------------------------------------------------------|:-------------------------------------------------|:---------------------------------------------------------|:------------------------------------------------|:------------------------------------------------|:--------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------------|:-----------------------------------------------|:--------------------------------------------------|:---------------------------------------------------|:----------------------------------------------|:----------------------------------------------|:----------------------------------------------------|:--------------------------------------------------|:----------------------------------------------------|:------------------------------------------------|:------------------------------------------------------|:-------------------------------------------------|:-------------------------------------------|:---------------------------------------------|:-----------------------------------------------|:-----------------------------------------------------|:-------------------------------------------------|:----------------------------------------------------|:-------------------------------------------------|:---------------------------------------------------|:------------------------------------------------|:--------------------------------------------------|:---------------------------------------------------|:-------------------------------------------------|:-------------------------------------------------|:--------------------------------------------------|:------------------------------------------|:--------------------------------------------|:-------------------------------------------|:-----------------------------------------|:---------------------------------------------|:------------------------------------------------|:----------------------------------------------------|:---------------------------------------------------------------|:-------------------------------------------------------------|:------------------------------------------------------|:----------------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------|:------------------------------------------------------|:-------------------------------------------------------|:--------------------------------------------------------|:------------------------------------------------------------|:--------------------------------------------------------------|:---------------------------------------------------------|:---------------------------------------------------------|:-----------------------------------------------------------------|:--------------------------------------------------|:---------------------------------------------------------------|:------------------------------------------------------------|:--------------------------------------------------------------|:-----------------------------------------------------------|:-------------------------------------------------------|:---------------------------------------------------------|:---------------------------------------------------------|:----------------------------------------------------|:--------------------------------------------------------|:-----------------------------------------------------|:-----------------------------------------------------|:----------------------------------------------------|:-----------------------------------------------------|:-----------------------------------------------------|:----------------------------------------------------------|:-----------------------------------------------------|:-----------------------------------------------------------|:-------------------------------------------------------|:--------------------------------------------------------|:-------------------------------------------------------------|:------------------------------------------------------------|:---------------------------------------------------------------|:-----------------------------------------------------------|:----------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------------------|:-------------------------------------------------------------|:-------------------------------------------------------|:------------------------------------------------|:------------------------------------------------|:---------------------------------------------|:---------------------------------------------|:-----------------------------------------------|:-----------------------------------------------|:----------------------------------------------|:----------------------------------------------|:--------------------------------------------------|:--------------------------------------------------|:------------------------------------------------------|:------------------------------------------------------|:--------------------------------------------------------|:---------------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------------------|:-----------------------------------------------------|:------------------------------------------------------|:----------------------------------------------|:------------------------------------------------|:-----------------------------------------------|:---------------------------------------------|:-------------------------------------------------|:----------------------------------------------------|:-----------------------------------------------------|:-----------------------------------------------------|:--------------------------------------------------------|:------------------------------------------------------|:----------------------------------------------------------|:--------------------------------------------------------|:------------------------------------------------------|:-----------------------------------------------------|:---------------------------------------------|:----------------------------------------------|:----------------------------------------------------|:----------------------------------------------------|:-----------------------------------------------------|:------------------------------------------------------|:-------------------------------------------------------------|:-------------------------------------------------------------|:----------------------------------------------------|:-----------------------------------------------------------------|:--------------------------------------------------------------|:--------------------------------------------------------------|:-------------------------------------------------------------|:------------------------------------------------------------------|:---------------------------------------------------------------|:---------------------------------------------------------------|:--------------------------------------------------------------|:--------------------------------------------------------|:------------------------------------------------------|:---------------------------------------------------------|:------------------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------|:---------------------------------------------------------------|:------------------------------------------------|:-------------------------------------------------------------|:----------------------------------------------------------|:------------------------------------------------------------|:-----------------------------------------------------------|:-----------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------|:--------------------------------------------------|:-----------------------------------------------------------|:--------------------------------------------------------|:--------------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------------------------|:--------------------------------------------------------|:--------------------------------------------------------|:-------------------------------------------------------|:------------------------------------------------------|:------------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------|:---------------------------------------------------|:-------------------------------------------------------|:---------------------------------------------------|:---------------------------------------------------------|:-----------------------------------------------------|:------------------------------------------------------|:-----------------------------------------------------------|:----------------------------------------------------------|:-------------------------------------------------------------|:---------------------------------------------------------|:--------------------------------------------------|:-----------------------------------------------------|:--------------------------------------------------------|:---------------------------------------------------|:-----------------------------------------------------------|:------------------------------------------------------------|:----------------------------------------------------------------|:-----------------------------------------------------|:--------------------------------------------------|:--------------------------------------------------|:---------------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------------|:-------------------------------------------------------|:--------------------------------------------------------|:------------------------------------------------|:--------------------------------------------------|:-------------------------------------------------|:----------------------------------------------------|:---------------------------------------------------|:---------------------------------------------------------|:-----------------------------------------------------|:-------------------------------------------------------|:--------------------------------------------------------|:------------------------------------------------------|:------------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------------|:-------------------------------------------------|:------------------------------------------------|:----------------------------------------------|:--------------------------------------------------|:-----------------------------------------------------|:---------------------------------------------------------|:-----------|
| postgresql-1-1-1 |      1 | 0/1                                                        | 0/1                                                        | 0/1                                                        | 0/1                                                      | 0/1                                                        | 0/1                                                      | 0/1                                              | 0/1                                               | 0/1                                                   | 0/1                                               | 0/1                                               | 0/1                                                 | 0/1                                                | 0/1                                                   | 0/1                                                  | 0/1                                                        | 0/1                                                  | 0/1                                                       | 0/1                                                 | 0/1                                                      | 0/1                                                       | 0/1                                                     | 0/1                                                     | 0/1                                                      | 0/1                                              | 0/1                                                | 0/1                                               | 0/1                                             | 0/1                                                 | 0/1                                                    | 0/1                                                        | 0/1                                                          | 0/1                                                          | 0/1                                                        | 0/1                                                      | 0/1                                                     | 0/1                                                         | 0/1                                                              | 0/1                                                      | 0/1                                               | 0/1                                                              | 0/1                                                              | 0/1                                                     | 0/1                                                                  | 0/1                                                               | 0/1                                                               | 0/1                                                              | 0/1                                                                   | 0/1                                                                | 0/1                                                                | 0/1                                                               | 0/1                                                            | 0/1                                                             | 0/1                                                          | 0/1                                                          | 0/1                                                       | 0/1                                                          | 0/1                                                             | 0/1                                                           | 0/1                                                        | 0/1                                                                | 0/1                                                 | 0/1                                                              | 0/1                                                           | 0/1                                                             | 0/1                                                          | 0/1                                                      | 0/1                                                        | 0/1                                                        | 0/1                                                        | 0/1                                                            | 0/1                                                         | 0/1                                                         | 0/1                                                        | 0/1                                                            | 0/1                                                         | 0/1                                                         | 0/1                                                        | 0/1                                                          | 0/1                                                           | 0/1                                                        | 0/1                                                        | 0/1                                                   | 0/1                                                    | 0/1                                                        | 0/1                                                    | 0/1                                                          | 0/1                                                      | 0/1                                                       | 0/1                                                            | 0/1                                                           | 0/1                                                              | 0/1                                                          | 0/1                                                   | 0/1                                                      | 0/1                                                         | 0/1                                                    | 0/1                                                            | 0/1                                                             | 0/1                                                                 | 0/1                                                      | 0/1                                                 | 0/1                                                 | 0/1                                                      | 0/1                                                      | 0/1                                                     | 0/1                                                          | 0/1                                                         | 0/1                                                | 0/1                                                | 0/1                                               | 0/1                                                         | 0/1                                               | 0/1                                                 | 0/1                                                | 0/1                                                   | 0/1                                           | 0/1                                                   | 0/1                                                      | 0/1                                                         | 0/1                                                         | 0/1                                                            | 0/1                                                          | 0/1                                                          | 0/1                                                           | 0/1                                                   | 0/1                                                     | 0/1                                                    | 0/1                                                  | 0/1                                                      | 0/1                                                         | 0/1                                                            | 0/1                                                           | 0/1                                                          | 0/1                                                                  | 0/1                                                                    | 0/1                                                                     | 0/1                                                                 | 0/1                                                             | 0/1                                                                      | 0/1                                                                     | 0/1                                             | 0/1                                             | 0/1                                          | 0/1                                               | 0/1                                              | 0/1                                                 | 0/1                                          | 0/1                                         | 0/1                                         | 0/1                                         | 0/1                                         | 0/1                                             | 0/1                                                    | 0/1                                                 | 0/1                                              | 0/1                                                  | 0/1                                             | 0/1                                             | 0/1                                                       | 0/1                                               | 0/1                                              | 0/1                                                 | 0/1                                                 | 0/1                                                 | 0/1                                                  | 0/1                                                   | 0/1                                                     | 0/1                                                  | 0/1                                                   | 0/1                                                       | 0/1                                                       | 0/1                                                        | 0/1                                                            | 0/1                                                                   | 0/1                                                                  | 0/1                                                              | 0/1                                                                  | 0/1                                                        | 0/1                                                     | 0/1                                                     | 0/1                                                | 0/1                                                | 0/1                                                     | 0/1                                                         | 0/1                                         | 0/1                                         | 0/1                                                | 0/1                                              | 0/1                                           | 0/1                                               | 0/1                                                | 0/1                                          | 0/1                                       | 0/1                                          | 0/1                                       | 0/1                                             | 0/1                                          | 0/1                                             | 0/1                                          | 0/1                                      | 0/1                                             | 0/1                                       | 0/1                                       | 0/1                                           | 0/1                                            | 0/1                                              | 0/1                                               | 0/1                                               | 0/1                                                    | 0/1                                                  | 0/1                                              | 0/1                                           | 0/1                                                      | 0/1                                                 | 0/1                                                    | 0/1                                                    | 0/1                                                      | 0/1                                                 | 0/1                                                    | 0/1                                                    | 0/1                                                    | 0/1                                                   | 0/1                                                      | 0/1                                              | 0/1                                                      | 0/1                                             | 0/1                                             | 0/1                                               | 0/1                                                    | 0/1                                                    | 0/1                                            | 0/1                                            | 0/1                                               | 0/1                                                | 0/1                                           | 0/1                                           | 0/1                                                 | 0/1                                               | 0/1                                                 | 0/1                                             | 0/1                                                   | 0/1                                              | 0/1                                        | 0/1                                          | 0/1                                            | 0/1                                                  | 0/1                                              | 0/1                                                 | 0/1                                              | 0/1                                                | 0/1                                             | 0/1                                               | 0/1                                                | 0/1                                              | 0/1                                              | 0/1                                               | 0/1                                       | 0/1                                         | 0/1                                        | 0/1                                      | 0/1                                          | 0/1                                             | 0/1                                                 | 0/1                                                            | 0/1                                                          | 0/1                                                   | 0/1                                                       | 0/1                                                    | 0/1                                                    | 0/1                                                   | 0/1                                                    | 0/1                                                     | 0/1                                                         | 0/1                                                           | 0/1                                                      | 0/1                                                      | 0/1                                                              | 0/1                                               | 0/1                                                            | 0/1                                                         | 0/1                                                           | 0/1                                                        | 0/1                                                    | 0/1                                                      | 0/1                                                      | 0/1                                                 | 0/1                                                     | 0/1                                                  | 0/1                                                  | 0/1                                                 | 0/1                                                  | 0/1                                                  | 0/1                                                       | 0/1                                                  | 0/1                                                        | 0/1                                                    | 0/1                                                     | 0/1                                                          | 0/1                                                         | 0/1                                                            | 0/1                                                        | 0/1                                                 | 0/1                                                    | 0/1                                                  | 0/1                                                          | 0/1                                                    | 0/1                                             | 0/1                                             | 0/1                                          | 0/1                                          | 0/1                                            | 0/1                                            | 0/1                                           | 0/1                                           | 0/1                                               | 0/1                                               | 0/1                                                   | 0/1                                                   | 0/1                                                     | 0/1                                                      | 0/1                                                    | 0/1                                                  | 0/1                                                  | 0/1                                                   | 0/1                                           | 0/1                                             | 0/1                                            | 0/1                                          | 0/1                                              | 0/1                                                 | 0/1                                                  | 0/1                                                  | 0/1                                                     | 0/1                                                   | 0/1                                                       | 0/1                                                     | 0/1                                                   | 0/1                                                  | 0/1                                          | 0/1                                           | 0/1                                                 | 0/1                                                 | 0/1                                                  | 0/1                                                   | 0/1                                                          | 0/1                                                          | 0/1                                                 | 0/1                                                              | 0/1                                                           | 0/1                                                           | 0/1                                                          | 0/1                                                               | 0/1                                                            | 0/1                                                            | 0/1                                                           | 0/1                                                     | 0/1                                                   | 0/1                                                      | 0/1                                                         | 0/1                                                    | 0/1                                                    | 0/1                                                            | 0/1                                             | 0/1                                                          | 0/1                                                       | 0/1                                                         | 0/1                                                        | 0/1                                                  | 0/1                                                    | 0/1                                                    | 0/1                                                    | 0/1                                               | 0/1                                                        | 0/1                                                     | 0/1                                                     | 0/1                                                    | 0/1                                                        | 0/1                                                     | 0/1                                                     | 0/1                                                    | 0/1                                                   | 0/1                                                   | 0/1                                                    | 0/1                                                    | 0/1                                                | 0/1                                                    | 0/1                                                | 0/1                                                      | 0/1                                                  | 0/1                                                   | 0/1                                                        | 0/1                                                       | 0/1                                                          | 0/1                                                      | 0/1                                               | 0/1                                                  | 0/1                                                     | 0/1                                                | 0/1                                                        | 0/1                                                         | 0/1                                                             | 0/1                                                  | 0/1                                               | 0/1                                               | 0/1                                                      | 0/1                                                    | 0/1                                            | 0/1                                                    | 0/1                                                     | 0/1                                             | 0/1                                               | 0/1                                              | 0/1                                                 | 0/1                                                | 0/1                                                      | 0/1                                                  | 0/1                                                    | 0/1                                                     | 0/1                                                   | 0/1                                                   | 0/1                                                    | 0/1                                            | 0/1                                              | 0/1                                             | 0/1                                           | 0/1                                               | 0/1                                                  | 0/1                                                      | no         |
| postgresql-1-1-2 |      1 | 0/1                                                        | 0/1                                                        | 0/1                                                        | 0/1                                                      | 0/1                                                        | 0/1                                                      | 0/1                                              | 0/1                                               | 0/1                                                   | 0/1                                               | 0/1                                               | 0/1                                                 | 0/1                                                | 0/1                                                   | 0/1                                                  | 0/1                                                        | 0/1                                                  | 0/1                                                       | 0/1                                                 | 0/1                                                      | 0/1                                                       | 0/1                                                     | 0/1                                                     | 0/1                                                      | 0/1                                              | 0/1                                                | 0/1                                               | 0/1                                             | 0/1                                                 | 0/1                                                    | 0/1                                                        | 0/1                                                          | 0/1                                                          | 0/1                                                        | 0/1                                                      | 0/1                                                     | 0/1                                                         | 0/1                                                              | 0/1                                                      | 0/1                                               | 0/1                                                              | 0/1                                                              | 0/1                                                     | 0/1                                                                  | 0/1                                                               | 0/1                                                               | 0/1                                                              | 0/1                                                                   | 0/1                                                                | 0/1                                                                | 0/1                                                               | 0/1                                                            | 0/1                                                             | 0/1                                                          | 0/1                                                          | 0/1                                                       | 0/1                                                          | 0/1                                                             | 0/1                                                           | 0/1                                                        | 0/1                                                                | 0/1                                                 | 0/1                                                              | 0/1                                                           | 0/1                                                             | 0/1                                                          | 0/1                                                      | 0/1                                                        | 0/1                                                        | 0/1                                                        | 0/1                                                            | 0/1                                                         | 0/1                                                         | 0/1                                                        | 0/1                                                            | 0/1                                                         | 0/1                                                         | 0/1                                                        | 0/1                                                          | 0/1                                                           | 0/1                                                        | 0/1                                                        | 0/1                                                   | 0/1                                                    | 0/1                                                        | 0/1                                                    | 0/1                                                          | 0/1                                                      | 0/1                                                       | 0/1                                                            | 0/1                                                           | 0/1                                                              | 0/1                                                          | 0/1                                                   | 0/1                                                      | 0/1                                                         | 0/1                                                    | 0/1                                                            | 0/1                                                             | 0/1                                                                 | 0/1                                                      | 0/1                                                 | 0/1                                                 | 0/1                                                      | 0/1                                                      | 0/1                                                     | 0/1                                                          | 0/1                                                         | 0/1                                                | 0/1                                                | 0/1                                               | 0/1                                                         | 0/1                                               | 0/1                                                 | 0/1                                                | 0/1                                                   | 0/1                                           | 0/1                                                   | 0/1                                                      | 0/1                                                         | 0/1                                                         | 0/1                                                            | 0/1                                                          | 0/1                                                          | 0/1                                                           | 0/1                                                   | 0/1                                                     | 0/1                                                    | 0/1                                                  | 0/1                                                      | 0/1                                                         | 0/1                                                            | 0/1                                                           | 0/1                                                          | 0/1                                                                  | 0/1                                                                    | 0/1                                                                     | 0/1                                                                 | 0/1                                                             | 0/1                                                                      | 0/1                                                                     | 0/1                                             | 0/1                                             | 0/1                                          | 0/1                                               | 0/1                                              | 0/1                                                 | 0/1                                          | 0/1                                         | 0/1                                         | 0/1                                         | 0/1                                         | 0/1                                             | 0/1                                                    | 0/1                                                 | 0/1                                              | 0/1                                                  | 0/1                                             | 0/1                                             | 0/1                                                       | 0/1                                               | 0/1                                              | 0/1                                                 | 0/1                                                 | 0/1                                                 | 0/1                                                  | 0/1                                                   | 0/1                                                     | 0/1                                                  | 0/1                                                   | 0/1                                                       | 0/1                                                       | 0/1                                                        | 0/1                                                            | 0/1                                                                   | 0/1                                                                  | 0/1                                                              | 0/1                                                                  | 0/1                                                        | 0/1                                                     | 0/1                                                     | 0/1                                                | 0/1                                                | 0/1                                                     | 0/1                                                         | 0/1                                         | 0/1                                         | 0/1                                                | 0/1                                              | 0/1                                           | 0/1                                               | 0/1                                                | 0/1                                          | 0/1                                       | 0/1                                          | 0/1                                       | 0/1                                             | 0/1                                          | 0/1                                             | 0/1                                          | 0/1                                      | 0/1                                             | 0/1                                       | 0/1                                       | 0/1                                           | 0/1                                            | 0/1                                              | 0/1                                               | 0/1                                               | 0/1                                                    | 0/1                                                  | 0/1                                              | 0/1                                           | 0/1                                                      | 0/1                                                 | 0/1                                                    | 0/1                                                    | 0/1                                                      | 0/1                                                 | 0/1                                                    | 0/1                                                    | 0/1                                                    | 0/1                                                   | 0/1                                                      | 0/1                                              | 0/1                                                      | 0/1                                             | 0/1                                             | 0/1                                               | 0/1                                                    | 0/1                                                    | 0/1                                            | 0/1                                            | 0/1                                               | 0/1                                                | 0/1                                           | 0/1                                           | 0/1                                                 | 0/1                                               | 0/1                                                 | 0/1                                             | 0/1                                                   | 0/1                                              | 0/1                                        | 0/1                                          | 0/1                                            | 0/1                                                  | 0/1                                              | 0/1                                                 | 0/1                                              | 0/1                                                | 0/1                                             | 0/1                                               | 0/1                                                | 0/1                                              | 0/1                                              | 0/1                                               | 0/1                                       | 0/1                                         | 0/1                                        | 0/1                                      | 0/1                                          | 0/1                                             | 0/1                                                 | 0/1                                                            | 0/1                                                          | 0/1                                                   | 0/1                                                       | 0/1                                                    | 0/1                                                    | 0/1                                                   | 0/1                                                    | 0/1                                                     | 0/1                                                         | 0/1                                                           | 0/1                                                      | 0/1                                                      | 0/1                                                              | 0/1                                               | 0/1                                                            | 0/1                                                         | 0/1                                                           | 0/1                                                        | 0/1                                                    | 0/1                                                      | 0/1                                                      | 0/1                                                 | 0/1                                                     | 0/1                                                  | 0/1                                                  | 0/1                                                 | 0/1                                                  | 0/1                                                  | 0/1                                                       | 0/1                                                  | 0/1                                                        | 0/1                                                    | 0/1                                                     | 0/1                                                          | 0/1                                                         | 0/1                                                            | 0/1                                                        | 0/1                                                 | 0/1                                                    | 0/1                                                  | 0/1                                                          | 0/1                                                    | 0/1                                             | 0/1                                             | 0/1                                          | 0/1                                          | 0/1                                            | 0/1                                            | 0/1                                           | 0/1                                           | 0/1                                               | 0/1                                               | 0/1                                                   | 0/1                                                   | 0/1                                                     | 0/1                                                      | 0/1                                                    | 0/1                                                  | 0/1                                                  | 0/1                                                   | 0/1                                           | 0/1                                             | 0/1                                            | 0/1                                          | 0/1                                              | 0/1                                                 | 0/1                                                  | 0/1                                                  | 0/1                                                     | 0/1                                                   | 0/1                                                       | 0/1                                                     | 0/1                                                   | 0/1                                                  | 0/1                                          | 0/1                                           | 0/1                                                 | 0/1                                                 | 0/1                                                  | 0/1                                                   | 0/1                                                          | 0/1                                                          | 0/1                                                 | 0/1                                                              | 0/1                                                           | 0/1                                                           | 0/1                                                          | 0/1                                                               | 0/1                                                            | 0/1                                                            | 0/1                                                           | 0/1                                                     | 0/1                                                   | 0/1                                                      | 0/1                                                         | 0/1                                                    | 0/1                                                    | 0/1                                                            | 0/1                                             | 0/1                                                          | 0/1                                                       | 0/1                                                         | 0/1                                                        | 0/1                                                  | 0/1                                                    | 0/1                                                    | 0/1                                                    | 0/1                                               | 0/1                                                        | 0/1                                                     | 0/1                                                     | 0/1                                                    | 0/1                                                        | 0/1                                                     | 0/1                                                     | 0/1                                                    | 0/1                                                   | 0/1                                                   | 0/1                                                    | 0/1                                                    | 0/1                                                | 0/1                                                    | 0/1                                                | 0/1                                                      | 0/1                                                  | 0/1                                                   | 0/1                                                        | 0/1                                                       | 0/1                                                          | 0/1                                                      | 0/1                                               | 0/1                                                  | 0/1                                                     | 0/1                                                | 0/1                                                        | 0/1                                                         | 0/1                                                             | 0/1                                                  | 0/1                                               | 0/1                                               | 0/1                                                      | 0/1                                                    | 0/1                                            | 0/1                                                    | 0/1                                                     | 0/1                                             | 0/1                                               | 0/1                                              | 0/1                                                 | 0/1                                                | 0/1                                                      | 0/1                                                  | 0/1                                                    | 0/1                                                     | 0/1                                                   | 0/1                                                   | 0/1                                                    | 0/1                                            | 0/1                                              | 0/1                                             | 0/1                                           | 0/1                                               | 0/1                                                  | 0/1                                                      | no         |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

#### Per Phase (Complete Phases Only)

Only the 0 of 2 phases in which every pod completed every active query; each row covers all 429 active queries, so the rows are comparable with each other. Left out: postgresql-1-1-1, postgresql-1-1-2 - see Query Completion per Phase.

### Latency of Timer Execution [ms]
No rows: these totals count only queries that succeeded in every connection of this experiment, and no query did (Q1 failed in 2 of 2 connections; Q2 failed in 2 of 2 connections; Q3 failed in 2 of 2 connections; Q4 failed in 2 of 2 connections; Q5 failed in 2 of 2 connections; Q6 failed in 2 of 2 connections; Q7 failed in 2 of 2 connections; Q8 failed in 2 of 2 connections; Q9 failed in 2 of 2 connections; Q10 failed in 2 of 2 connections; Q11 failed in 2 of 2 connections; Q12 failed in 2 of 2 connections; Q13 failed in 2 of 2 connections; Q14 failed in 2 of 2 connections; Q15 failed in 2 of 2 connections; Q16 failed in 2 of 2 connections; Q17 failed in 2 of 2 connections; Q18 failed in 2 of 2 connections; Q19 failed in 2 of 2 connections; Q20 failed in 2 of 2 connections; Q21 failed in 2 of 2 connections; Q22 failed in 2 of 2 connections; Q23 failed in 2 of 2 connections; Q24 failed in 2 of 2 connections; Q25 failed in 2 of 2 connections; Q26 failed in 2 of 2 connections; Q27 failed in 2 of 2 connections; Q28 failed in 2 of 2 connections; Q29 failed in 2 of 2 connections; Q30 failed in 2 of 2 connections; Q31 failed in 2 of 2 connections; Q32 failed in 2 of 2 connections; Q33 failed in 2 of 2 connections; Q34 failed in 2 of 2 connections; Q35 failed in 2 of 2 connections; Q36 failed in 2 of 2 connections; Q37 failed in 2 of 2 connections; Q38 failed in 2 of 2 connections; Q39 failed in 2 of 2 connections; Q40 failed in 2 of 2 connections; Q41 failed in 2 of 2 connections; Q42 failed in 2 of 2 connections; Q43 failed in 2 of 2 connections; Q44 failed in 2 of 2 connections; Q45 failed in 2 of 2 connections; Q46 failed in 2 of 2 connections; Q47 failed in 2 of 2 connections; Q48 failed in 2 of 2 connections; Q49 failed in 2 of 2 connections; Q50 failed in 2 of 2 connections; Q51 failed in 2 of 2 connections; Q52 failed in 2 of 2 connections; Q53 failed in 2 of 2 connections; Q54 failed in 2 of 2 connections; Q55 failed in 2 of 2 connections; Q56 failed in 2 of 2 connections; Q57 failed in 2 of 2 connections; Q58 failed in 2 of 2 connections; Q59 failed in 2 of 2 connections; Q60 failed in 2 of 2 connections; Q61 failed in 2 of 2 connections; Q62 failed in 2 of 2 connections; Q63 failed in 2 of 2 connections; Q64 failed in 2 of 2 connections; Q65 failed in 2 of 2 connections; Q66 failed in 2 of 2 connections; Q67 failed in 2 of 2 connections; Q68 failed in 2 of 2 connections; Q69 failed in 2 of 2 connections; Q70 failed in 2 of 2 connections; Q71 failed in 2 of 2 connections; Q72 failed in 2 of 2 connections; Q73 failed in 2 of 2 connections; Q74 failed in 2 of 2 connections; Q75 failed in 2 of 2 connections; Q76 failed in 2 of 2 connections; Q77 failed in 2 of 2 connections; Q78 failed in 2 of 2 connections; Q79 failed in 2 of 2 connections; Q80 failed in 2 of 2 connections; Q81 failed in 2 of 2 connections; Q82 failed in 2 of 2 connections; Q83 failed in 2 of 2 connections; Q84 failed in 2 of 2 connections; Q85 failed in 2 of 2 connections; Q86 failed in 2 of 2 connections; Q87 failed in 2 of 2 connections; Q88 failed in 2 of 2 connections; Q89 failed in 2 of 2 connections; Q90 failed in 2 of 2 connections; Q91 failed in 2 of 2 connections; Q92 failed in 2 of 2 connections; Q93 failed in 2 of 2 connections; Q94 failed in 2 of 2 connections; Q95 failed in 2 of 2 connections; Q96 failed in 2 of 2 connections; Q97 failed in 2 of 2 connections; Q98 failed in 2 of 2 connections; Q99 failed in 2 of 2 connections; Q100 failed in 2 of 2 connections; Q101 failed in 2 of 2 connections; Q102 failed in 2 of 2 connections; Q103 failed in 2 of 2 connections; Q104 failed in 2 of 2 connections; Q105 failed in 2 of 2 connections; Q106 failed in 2 of 2 connections; Q107 failed in 2 of 2 connections; Q108 failed in 2 of 2 connections; Q109 failed in 2 of 2 connections; Q110 failed in 2 of 2 connections; Q111 failed in 2 of 2 connections; Q112 failed in 2 of 2 connections; Q113 failed in 2 of 2 connections; Q114 failed in 2 of 2 connections; Q115 failed in 2 of 2 connections; Q116 failed in 2 of 2 connections; Q117 failed in 2 of 2 connections; Q118 failed in 2 of 2 connections; Q119 failed in 2 of 2 connections; Q120 failed in 2 of 2 connections; Q121 failed in 2 of 2 connections; Q122 failed in 2 of 2 connections; Q123 failed in 2 of 2 connections; Q124 failed in 2 of 2 connections; Q125 failed in 2 of 2 connections; Q126 failed in 2 of 2 connections; Q127 failed in 2 of 2 connections; Q128 failed in 2 of 2 connections; Q129 failed in 2 of 2 connections; Q130 failed in 2 of 2 connections; Q131 failed in 2 of 2 connections; Q132 failed in 2 of 2 connections; Q133 failed in 2 of 2 connections; Q134 failed in 2 of 2 connections; Q135 failed in 2 of 2 connections; Q136 failed in 2 of 2 connections; Q137 failed in 2 of 2 connections; Q138 failed in 2 of 2 connections; Q139 failed in 2 of 2 connections; Q140 failed in 2 of 2 connections; Q141 failed in 2 of 2 connections; Q142 failed in 2 of 2 connections; Q143 failed in 2 of 2 connections; Q144 failed in 2 of 2 connections; Q145 failed in 2 of 2 connections; Q146 failed in 2 of 2 connections; Q147 failed in 2 of 2 connections; Q148 failed in 2 of 2 connections; Q149 failed in 2 of 2 connections; Q150 failed in 2 of 2 connections; Q151 failed in 2 of 2 connections; Q152 failed in 2 of 2 connections; Q153 failed in 2 of 2 connections; Q154 failed in 2 of 2 connections; Q155 failed in 2 of 2 connections; Q156 failed in 2 of 2 connections; Q157 failed in 2 of 2 connections; Q158 failed in 2 of 2 connections; Q159 failed in 2 of 2 connections; Q160 failed in 2 of 2 connections; Q161 failed in 2 of 2 connections; Q162 failed in 2 of 2 connections; Q163 failed in 2 of 2 connections; Q164 failed in 2 of 2 connections; Q165 failed in 2 of 2 connections; Q166 failed in 2 of 2 connections; Q167 failed in 2 of 2 connections; Q168 failed in 2 of 2 connections; Q169 failed in 2 of 2 connections; Q170 failed in 2 of 2 connections; Q171 failed in 2 of 2 connections; Q172 failed in 2 of 2 connections; Q173 failed in 2 of 2 connections; Q174 failed in 2 of 2 connections; Q175 failed in 2 of 2 connections; Q176 failed in 2 of 2 connections; Q177 failed in 2 of 2 connections; Q178 failed in 2 of 2 connections; Q179 failed in 2 of 2 connections; Q180 failed in 2 of 2 connections; Q181 failed in 2 of 2 connections; Q182 failed in 2 of 2 connections; Q183 failed in 2 of 2 connections; Q184 failed in 2 of 2 connections; Q185 failed in 2 of 2 connections; Q186 failed in 2 of 2 connections; Q187 failed in 2 of 2 connections; Q188 failed in 2 of 2 connections; Q189 failed in 2 of 2 connections; Q190 failed in 2 of 2 connections; Q191 failed in 2 of 2 connections; Q192 failed in 2 of 2 connections; Q193 failed in 2 of 2 connections; Q194 failed in 2 of 2 connections; Q195 failed in 2 of 2 connections; Q196 failed in 2 of 2 connections; Q197 failed in 2 of 2 connections; Q198 failed in 2 of 2 connections; Q199 failed in 2 of 2 connections; Q200 failed in 2 of 2 connections; Q201 failed in 2 of 2 connections; Q202 failed in 2 of 2 connections; Q203 failed in 2 of 2 connections; Q204 failed in 2 of 2 connections; Q205 failed in 2 of 2 connections; Q206 failed in 2 of 2 connections; Q207 failed in 2 of 2 connections; Q208 failed in 2 of 2 connections; Q209 failed in 2 of 2 connections; Q210 failed in 2 of 2 connections; Q211 failed in 2 of 2 connections; Q212 failed in 2 of 2 connections; Q213 failed in 2 of 2 connections; Q214 failed in 2 of 2 connections; Q215 failed in 2 of 2 connections; Q216 failed in 2 of 2 connections; Q217 failed in 2 of 2 connections; Q218 failed in 2 of 2 connections; Q219 failed in 2 of 2 connections; Q220 failed in 2 of 2 connections; Q221 failed in 2 of 2 connections; Q222 failed in 2 of 2 connections; Q223 failed in 2 of 2 connections; Q224 failed in 2 of 2 connections; Q225 failed in 2 of 2 connections; Q226 failed in 2 of 2 connections; Q227 failed in 2 of 2 connections; Q228 failed in 2 of 2 connections; Q229 failed in 2 of 2 connections; Q230 failed in 2 of 2 connections; Q231 failed in 2 of 2 connections; Q232 failed in 2 of 2 connections; Q233 failed in 2 of 2 connections; Q234 failed in 2 of 2 connections; Q235 failed in 2 of 2 connections; Q236 failed in 2 of 2 connections; Q237 failed in 2 of 2 connections; Q238 failed in 2 of 2 connections; Q239 failed in 2 of 2 connections; Q240 failed in 2 of 2 connections; Q241 failed in 2 of 2 connections; Q242 failed in 2 of 2 connections; Q243 failed in 2 of 2 connections; Q244 failed in 2 of 2 connections; Q245 failed in 2 of 2 connections; Q246 failed in 2 of 2 connections; Q247 failed in 2 of 2 connections; Q248 failed in 2 of 2 connections; Q249 failed in 2 of 2 connections; Q250 failed in 2 of 2 connections; Q251 failed in 2 of 2 connections; Q252 failed in 2 of 2 connections; Q253 failed in 2 of 2 connections; Q254 failed in 2 of 2 connections; Q255 failed in 2 of 2 connections; Q256 failed in 2 of 2 connections; Q257 failed in 2 of 2 connections; Q258 failed in 2 of 2 connections; Q259 failed in 2 of 2 connections; Q260 failed in 2 of 2 connections; Q261 failed in 2 of 2 connections; Q262 failed in 2 of 2 connections; Q263 failed in 2 of 2 connections; Q264 failed in 2 of 2 connections; Q265 failed in 2 of 2 connections; Q266 failed in 2 of 2 connections; Q267 failed in 2 of 2 connections; Q268 failed in 2 of 2 connections; Q269 failed in 2 of 2 connections; Q270 failed in 2 of 2 connections; Q271 failed in 2 of 2 connections; Q272 failed in 2 of 2 connections; Q273 failed in 2 of 2 connections; Q274 failed in 2 of 2 connections; Q275 failed in 2 of 2 connections; Q276 failed in 2 of 2 connections; Q277 failed in 2 of 2 connections; Q278 failed in 2 of 2 connections; Q279 failed in 2 of 2 connections; Q280 failed in 2 of 2 connections; Q281 failed in 2 of 2 connections; Q282 failed in 2 of 2 connections; Q283 failed in 2 of 2 connections; Q284 failed in 2 of 2 connections; Q285 failed in 2 of 2 connections; Q286 failed in 2 of 2 connections; Q287 failed in 2 of 2 connections; Q288 failed in 2 of 2 connections; Q289 failed in 2 of 2 connections; Q290 failed in 2 of 2 connections; Q291 failed in 2 of 2 connections; Q292 failed in 2 of 2 connections; Q293 failed in 2 of 2 connections; Q294 failed in 2 of 2 connections; Q295 failed in 2 of 2 connections; Q296 failed in 2 of 2 connections; Q297 failed in 2 of 2 connections; Q298 failed in 2 of 2 connections; Q299 failed in 2 of 2 connections; Q300 failed in 2 of 2 connections; Q301 failed in 2 of 2 connections; Q302 failed in 2 of 2 connections; Q303 failed in 2 of 2 connections; Q304 failed in 2 of 2 connections; Q305 failed in 2 of 2 connections; Q306 failed in 2 of 2 connections; Q307 failed in 2 of 2 connections; Q308 failed in 2 of 2 connections; Q309 failed in 2 of 2 connections; Q310 failed in 2 of 2 connections; Q311 failed in 2 of 2 connections; Q312 failed in 2 of 2 connections; Q313 failed in 2 of 2 connections; Q314 failed in 2 of 2 connections; Q315 failed in 2 of 2 connections; Q316 failed in 2 of 2 connections; Q317 failed in 2 of 2 connections; Q318 failed in 2 of 2 connections; Q319 failed in 2 of 2 connections; Q320 failed in 2 of 2 connections; Q321 failed in 2 of 2 connections; Q322 failed in 2 of 2 connections; Q323 failed in 2 of 2 connections; Q324 failed in 2 of 2 connections; Q325 failed in 2 of 2 connections; Q326 failed in 2 of 2 connections; Q327 failed in 2 of 2 connections; Q328 failed in 2 of 2 connections; Q329 failed in 2 of 2 connections; Q330 failed in 2 of 2 connections; Q331 failed in 2 of 2 connections; Q332 failed in 2 of 2 connections; Q333 failed in 2 of 2 connections; Q334 failed in 2 of 2 connections; Q335 failed in 2 of 2 connections; Q336 failed in 2 of 2 connections; Q337 failed in 2 of 2 connections; Q338 failed in 2 of 2 connections; Q339 failed in 2 of 2 connections; Q340 failed in 2 of 2 connections; Q341 failed in 2 of 2 connections; Q342 failed in 2 of 2 connections; Q343 failed in 2 of 2 connections; Q344 failed in 2 of 2 connections; Q345 failed in 2 of 2 connections; Q346 failed in 2 of 2 connections; Q347 failed in 2 of 2 connections; Q348 failed in 2 of 2 connections; Q349 failed in 2 of 2 connections; Q350 failed in 2 of 2 connections; Q351 failed in 2 of 2 connections; Q352 failed in 2 of 2 connections; Q353 failed in 2 of 2 connections; Q354 failed in 2 of 2 connections; Q355 failed in 2 of 2 connections; Q356 failed in 2 of 2 connections; Q357 failed in 2 of 2 connections; Q358 failed in 2 of 2 connections; Q359 failed in 2 of 2 connections; Q360 failed in 2 of 2 connections; Q361 failed in 2 of 2 connections; Q362 failed in 2 of 2 connections; Q363 failed in 2 of 2 connections; Q364 failed in 2 of 2 connections; Q365 failed in 2 of 2 connections; Q366 failed in 2 of 2 connections; Q367 failed in 2 of 2 connections; Q368 failed in 2 of 2 connections; Q369 failed in 2 of 2 connections; Q370 failed in 2 of 2 connections; Q371 failed in 2 of 2 connections; Q372 failed in 2 of 2 connections; Q373 failed in 2 of 2 connections; Q374 failed in 2 of 2 connections; Q375 failed in 2 of 2 connections; Q376 failed in 2 of 2 connections; Q377 failed in 2 of 2 connections; Q378 failed in 2 of 2 connections; Q379 failed in 2 of 2 connections; Q380 failed in 2 of 2 connections; Q381 failed in 2 of 2 connections; Q382 failed in 2 of 2 connections; Q383 failed in 2 of 2 connections; Q384 failed in 2 of 2 connections; Q385 failed in 2 of 2 connections; Q386 failed in 2 of 2 connections; Q387 failed in 2 of 2 connections; Q388 failed in 2 of 2 connections; Q389 failed in 2 of 2 connections; Q390 failed in 2 of 2 connections; Q391 failed in 2 of 2 connections; Q392 failed in 2 of 2 connections; Q393 failed in 2 of 2 connections; Q394 failed in 2 of 2 connections; Q395 failed in 2 of 2 connections; Q396 failed in 2 of 2 connections; Q397 failed in 2 of 2 connections; Q398 failed in 2 of 2 connections; Q399 failed in 2 of 2 connections; Q400 failed in 2 of 2 connections; Q401 failed in 2 of 2 connections; Q402 failed in 2 of 2 connections; Q403 failed in 2 of 2 connections; Q404 failed in 2 of 2 connections; Q405 failed in 2 of 2 connections; Q406 failed in 2 of 2 connections; Q407 failed in 2 of 2 connections; Q408 failed in 2 of 2 connections; Q409 failed in 2 of 2 connections; Q410 failed in 2 of 2 connections; Q411 failed in 2 of 2 connections; Q412 failed in 2 of 2 connections; Q413 failed in 2 of 2 connections; Q414 failed in 2 of 2 connections; Q415 failed in 2 of 2 connections; Q416 failed in 2 of 2 connections; Q417 failed in 2 of 2 connections; Q418 failed in 2 of 2 connections; Q419 failed in 2 of 2 connections; Q420 failed in 2 of 2 connections; Q421 failed in 2 of 2 connections; Q422 failed in 2 of 2 connections; Q423 failed in 2 of 2 connections; Q424 failed in 2 of 2 connections; Q425 failed in 2 of 2 connections; Q426 failed in 2 of 2 connections; Q427 failed in 2 of 2 connections; Q428 failed in 2 of 2 connections; Q429 failed in 2 of 2 connections). See Query Completion per Phase for where, and Per Phase (Complete Phases Only) for the phases that completed every query.

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       577.47 |      2.41 |           9.09 |                 30.34 |
| postgresql-1-1-2-1 |       577.47 |      2.41 |           9.09 |                 30.34 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |         0.14 |      0.00 |           0.00 |                  0.00 |
| postgresql-1-1-2-1 |         0.14 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       202.11 |      1.44 |           0.01 |                  2.82 |
| postgresql-1-1-2-1 |       202.11 |      1.44 |           0.01 |                  2.82 |

### Benchmarking phase: SUT deployment

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |      0.52 |           7.98 |                 37.29 |
| postgresql-1-1-2-1 | n/a          |      0.58 |          21.17 |                 64.00 |

### Benchmarking phase: component benchmarker

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |
| postgresql-1-1-2-1 | n/a          |         0 |           0.00 |                  0.00 |

### Missing Monitoring Metrics
* Memory Usage, Working Set [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU User Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU System Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Network Tx Total [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Network Rx Total [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Utilization [CPUs] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU System Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU User Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Utilization Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* Network Tx Total [MiB] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* Network Rx Total [MiB] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST failed: No SUT container restarts
* TEST passed: SUT data survived container restarts
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component data generator contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Benchmarking phase: SUT deployment contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Benchmarking phase: component benchmarker contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Monitoring metrics missing (data pre-existing; phase shorter than scrape interval; series exists only while non-zero)
* TEST failed: Geo Times [s] contains 0 or NaN
* TEST failed: Power@Size [~Q/h] contains 0 or NaN
* TEST failed: Throughput@Size contains 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
```

</details>













## Example: MonetDB TPC-DS@30

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

This example shows how to run Q1-Q99 derived from TPC-DS in MonetDB at SF=30.
It covers the power and the throughput test.
The refresh stream is not included.

> The query file is derived from the TPC-DS and as such is not comparable to published TPC-DS results, as the query file results do not comply with the TPC-DS specification.

Official TPC-DS benchmark - http://www.tpc.org/tpcds

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**



### Generate and Load Data

At first we generate TPC-DS data at SF=30 (`-sf`) with 8 parallel generators (`-nlp`).
The generated data is stored at the shared disk `data`.
Moreover the data is loaded into an instance of MonetDB using again 8 parallel loaders.
Afterwards the script creates contraints (`-xic`) and indexes (`-xii`) and updates table statistics (`-xis`).
The database is located in another shared disk of storageClass shared (`-rst`) and of size 2000Gi (`-rss`).
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
  -rss 2000Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  run &>$LOG_DIR/docs_tpcds_monetdb_1.log
```


### Status Database and Benchmark

You can watch the status of experiments via `bexhoma status`.

In the following example output we see all components of bexhoma are up and running.
The cluster stores a MonetDB database corresponding to TPC-DS of SF=30.
The disk is of storageClass shared and of size 2000Gi and 156G of that space is used.
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
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_monetdb_1_summary.md" target="_blank" rel="noopener">docs_tpcds_monetdb_1.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=30
* Type: tpcds
* Duration: 9842s 
* Code: 1792720113
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=30) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 14400.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.8.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Database is persisted to disk of type nvme and size 2000Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * SUT requests 4 CPU and 900Gi RAM. RAM limit is 1024Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:922325
  * datadisk:52440
  * volume_size:2.0T
  * volume_used:52G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792720113

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1792720113-56fb44c77f-2mfzt: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |   30 |      688.00 |           4.00 |            1.00 |        517.00 |          147.00 |              8 |           0 |             | None           |             0 | False         |              156.98 | False               |

### Benchmarking

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| monetdb-1-1-1-1-1 | MonetDB-1       | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        626 |            0.61 |           183437.84 |          17079.87 |          -1 | monetdb-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        626 |            0.61 |           183437.84 |          17079.87 |          -1 |

#### Query Completion per Phase

| phase         |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:--------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   monetdb-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |              213.05 |
| TPC-DS Q2     |             1335.04 |
| TPC-DS Q3     |              128.90 |
| TPC-DS Q4     |            14673.24 |
| TPC-DS Q5     |             1362.44 |
| TPC-DS Q6     |              328.85 |
| TPC-DS Q7     |              186.54 |
| TPC-DS Q8     |              229.80 |
| TPC-DS Q9     |              525.15 |
| TPC-DS Q10    |               84.96 |
| TPC-DS Q11    |             6359.08 |
| TPC-DS Q12    |              184.47 |
| TPC-DS Q13    |              294.19 |
| TPC-DS Q14a+b |            34541.82 |
| TPC-DS Q15    |              135.70 |
| TPC-DS Q16    |            43099.63 |
| TPC-DS Q17    |             1805.36 |
| TPC-DS Q18    |              688.40 |
| TPC-DS Q19    |              176.13 |
| TPC-DS Q20    |              123.37 |
| TPC-DS Q21    |              113.15 |
| TPC-DS Q22    |             1140.32 |
| TPC-DS Q23a+b |            49744.89 |
| TPC-DS Q24a+b |            23023.03 |
| TPC-DS Q25    |             2396.98 |
| TPC-DS Q26    |              204.19 |
| TPC-DS Q27    |             1081.00 |
| TPC-DS Q28    |              565.97 |
| TPC-DS Q29    |             1384.46 |
| TPC-DS Q30    |               76.50 |
| TPC-DS Q31    |             1797.82 |
| TPC-DS Q32    |              193.28 |
| TPC-DS Q33    |               96.73 |
| TPC-DS Q34    |              108.57 |
| TPC-DS Q35    |             1352.05 |
| TPC-DS Q36    |             1177.63 |
| TPC-DS Q37    |              374.99 |
| TPC-DS Q38    |             2261.55 |
| TPC-DS Q39a+b |             1495.71 |
| TPC-DS Q40    |              926.98 |
| TPC-DS Q41    |                8.22 |
| TPC-DS Q42    |              110.12 |
| TPC-DS Q43    |              214.88 |
| TPC-DS Q44    |              470.92 |
| TPC-DS Q45    |              135.74 |
| TPC-DS Q46    |              219.05 |
| TPC-DS Q47    |              752.28 |
| TPC-DS Q48    |              256.54 |
| TPC-DS Q49    |             1080.88 |
| TPC-DS Q50    |              529.08 |
| TPC-DS Q51    |             2260.14 |
| TPC-DS Q52    |               89.89 |
| TPC-DS Q53    |               71.90 |
| TPC-DS Q54    |              196.11 |
| TPC-DS Q55    |               88.79 |
| TPC-DS Q56    |              112.72 |
| TPC-DS Q57    |              134.53 |
| TPC-DS Q58    |             3938.10 |
| TPC-DS Q59    |             1082.28 |
| TPC-DS Q60    |              111.34 |
| TPC-DS Q61    |              188.99 |
| TPC-DS Q62    |              244.07 |
| TPC-DS Q63    |               80.84 |
| TPC-DS Q64    |             3871.49 |
| TPC-DS Q65    |              971.58 |
| TPC-DS Q66    |             1942.64 |
| TPC-DS Q67    |             4547.36 |
| TPC-DS Q68    |              364.21 |
| TPC-DS Q69    |               72.16 |
| TPC-DS Q70    |             1767.51 |
| TPC-DS Q71    |              142.95 |
| TPC-DS Q72    |             1098.13 |
| TPC-DS Q73    |               78.47 |
| TPC-DS Q74    |             6588.90 |
| TPC-DS Q75    |             5153.34 |
| TPC-DS Q76    |              298.94 |
| TPC-DS Q77    |              778.39 |
| TPC-DS Q78    |            12022.19 |
| TPC-DS Q79    |              196.48 |
| TPC-DS Q80    |             7161.39 |
| TPC-DS Q81    |               80.46 |
| TPC-DS Q82    |              730.52 |
| TPC-DS Q83    |              360.26 |
| TPC-DS Q84    |               33.68 |
| TPC-DS Q85    |              919.66 |
| TPC-DS Q86    |              374.42 |
| TPC-DS Q87    |             2539.96 |
| TPC-DS Q88    |              496.58 |
| TPC-DS Q89    |              150.26 |
| TPC-DS Q90    |               68.45 |
| TPC-DS Q91    |               27.64 |
| TPC-DS Q92    |              183.12 |
| TPC-DS Q93    |             1888.86 |
| TPC-DS Q94    |            37608.56 |
| TPC-DS Q95    |           294697.32 |
| TPC-DS Q96    |              434.13 |
| TPC-DS Q97    |             4713.24 |
| TPC-DS Q98    |              575.40 |
| TPC-DS Q99    |              290.65 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      2602.42 |      6.17 |          47.99 |                 48.03 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |       201.84 |      0.45 |           0.01 |                  3.36 |

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |     13349.04 |    124.86 |        1014.57 |               1023.96 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        26.27 |      0.61 |           0.36 |                  0.37 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loading.log, expected: series exists only while non-zero)

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
  -rss 2000Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  run &>$LOG_DIR/docs_tpcds_monetdb_2.log
```

### Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_monetdb_2_summary.md" target="_blank" rel="noopener">docs_tpcds_monetdb_2.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=30
* Type: tpcds
* Duration: 3995s 
* Code: 1792730083
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=30) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 14400.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.8.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Database is persisted to disk of type nvme and size 2000Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * SUT requests 4 CPU and 900Gi RAM. RAM limit is 1024Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:926103
  * datadisk:52423
  * volume_size:2.0T
  * volume_used:52G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1792730083
* monetdb-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:922760
  * datadisk:51000
  * volume_size:2.0T
  * volume_used:50G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1792730083
* monetdb-1-2-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:920092
  * datadisk:51000
  * volume_size:2.0T
  * volume_used:50G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1792730083
* monetdb-1-2-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:924425
  * datadisk:51000
  * volume_size:2.0T
  * volume_used:50G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1792730083

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MonetDB-1

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1792730083-fbd98d694-cwknv: 0
* bexhoma-sut-monetdb-1-1792730083-6fc46c7797-86r9r: 0

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
| MonetDB-1-1 |                1 |   30 |      688.00 |           4.00 |            1.00 |        517.00 |          147.00 |              0 |           0 |             | None           |             0 | False         |              156.98 | True                |
| MonetDB-1-2 |                2 |   30 |      688.00 |           4.00 |            1.00 |        517.00 |          147.00 |              0 |           0 |             | None           |             0 | False         |              156.98 | True                |

### Benchmarking

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| monetdb-1-1-1-1-1 | MonetDB-1       | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        863 |            1.04 |           107800.86 |          12389.34 |          -1 | monetdb-1-1-1-1-1 |
| monetdb-1-1-2-1-1 | MonetDB-1       | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |           1 | 30.00 |               99 |                  99 |        818 |            0.83 |           136333.55 |          13070.90 |          -1 | monetdb-1-1-2-1-1 |
| monetdb-1-2-1-1-1 | MonetDB-1       | monetdb-1-2-1 | monetdb-1-2-1-1 |                2 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        924 |            1.23 |            90244.92 |          11571.43 |          -1 | monetdb-1-2-1-1-1 |
| monetdb-1-2-2-1-1 | MonetDB-1       | monetdb-1-2-2 | monetdb-1-2-2-1 |                2 |        2 |               1 |           1 | 30.00 |               99 |                  99 |        829 |            0.99 |           112895.14 |          12897.47 |          -1 | monetdb-1-2-2-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        863 |            1.04 |           107800.86 |          12389.34 |          -1 |
| monetdb-1-1-2 | monetdb-1-1-2 |                1 |        2 |               1 |           1 | 30.00 |               99 |                  99 |        818 |            0.83 |           136333.55 |          13070.90 |          -1 |
| monetdb-1-2-1 | monetdb-1-2-1 |                2 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        924 |            1.23 |            90244.92 |          11571.43 |          -1 |
| monetdb-1-2-2 | monetdb-1-2-2 |                2 |        2 |               1 |           1 | 30.00 |               99 |                  99 |        829 |            0.99 |           112895.14 |          12897.47 |          -1 |

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
| TPC-DS Q1     |             1287.34 |              235.06 |             1341.01 |              367.13 |
| TPC-DS Q2     |             3622.46 |             2289.75 |             3779.29 |             4118.27 |
| TPC-DS Q3     |             7106.32 |             6547.23 |             6883.26 |             5166.57 |
| TPC-DS Q4     |            24195.40 |            16126.95 |            24258.47 |            17180.74 |
| TPC-DS Q5     |            18965.70 |             1812.08 |            21878.90 |             1831.25 |
| TPC-DS Q6     |             3761.56 |              322.43 |             9799.22 |              737.20 |
| TPC-DS Q7     |             5675.96 |             1164.66 |             9806.50 |              798.86 |
| TPC-DS Q8     |             2639.88 |             3003.18 |             3185.97 |             3147.34 |
| TPC-DS Q9     |             1094.01 |              527.25 |             2432.22 |              569.00 |
| TPC-DS Q10    |            21849.03 |              292.76 |            26015.12 |              282.93 |
| TPC-DS Q11    |             8202.96 |             6553.94 |            11277.32 |             6938.86 |
| TPC-DS Q12    |              228.76 |              692.82 |              236.40 |              120.87 |
| TPC-DS Q13    |             1102.80 |             1905.00 |             3835.34 |              470.97 |
| TPC-DS Q14a+b |            36377.00 |            35850.11 |            38191.16 |            38399.09 |
| TPC-DS Q15    |             1298.68 |              117.63 |             1379.04 |              515.91 |
| TPC-DS Q16    |            44898.70 |            43723.49 |            45880.31 |            44062.78 |
| TPC-DS Q17    |             5903.77 |             4774.51 |             4676.49 |             7939.31 |
| TPC-DS Q18    |             1262.91 |             1314.15 |             1272.77 |             1296.60 |
| TPC-DS Q19    |              180.37 |              171.69 |              173.79 |              156.96 |
| TPC-DS Q20    |             1090.74 |              128.25 |              101.69 |             1883.23 |
| TPC-DS Q21    |             2197.12 |              129.82 |             2452.17 |              117.48 |
| TPC-DS Q22    |             1216.59 |             1358.42 |             1252.76 |             1290.43 |
| TPC-DS Q23a+b |            50682.42 |            50333.50 |            55702.25 |            51958.87 |
| TPC-DS Q24a+b |            31040.75 |            27924.68 |            27916.19 |            29299.31 |
| TPC-DS Q25    |             1273.55 |             1755.11 |             1257.76 |             1754.00 |
| TPC-DS Q26    |              164.07 |              150.84 |             1567.72 |              162.14 |
| TPC-DS Q27    |             1047.38 |              960.94 |              934.69 |             1162.23 |
| TPC-DS Q28    |              606.56 |              681.38 |              621.96 |              648.31 |
| TPC-DS Q29    |             2043.50 |             2964.09 |             2200.06 |             2276.28 |
| TPC-DS Q30    |               92.82 |              105.03 |              107.97 |              104.89 |
| TPC-DS Q31    |             3561.46 |             2011.00 |             1891.12 |             2297.20 |
| TPC-DS Q32    |              175.71 |              208.07 |             1611.28 |              149.27 |
| TPC-DS Q33    |              119.48 |              118.19 |              106.28 |              105.25 |
| TPC-DS Q34    |              100.23 |              109.80 |              108.01 |              121.15 |
| TPC-DS Q35    |             1010.41 |              838.16 |             1014.58 |              966.41 |
| TPC-DS Q36    |             1201.48 |             1301.60 |             1178.02 |             1473.39 |
| TPC-DS Q37    |              372.22 |              420.15 |              434.00 |              388.19 |
| TPC-DS Q38    |             2217.35 |             2725.73 |             2316.35 |             2356.33 |
| TPC-DS Q39a+b |             1559.06 |             1578.63 |             1549.81 |             2959.89 |
| TPC-DS Q40    |             1969.27 |             1200.78 |             2008.86 |             1500.14 |
| TPC-DS Q41    |                5.36 |                5.11 |                4.45 |                4.69 |
| TPC-DS Q42    |              109.60 |               86.99 |             1108.99 |              117.74 |
| TPC-DS Q43    |              302.32 |             1520.16 |              839.01 |              312.76 |
| TPC-DS Q44    |              207.41 |              212.63 |              218.43 |              256.08 |
| TPC-DS Q45    |              134.72 |              140.56 |              422.56 |              235.77 |
| TPC-DS Q46    |              217.27 |              227.77 |              220.16 |              208.28 |
| TPC-DS Q47    |             1034.41 |              999.88 |              942.83 |             1072.67 |
| TPC-DS Q48    |              481.04 |              230.30 |              471.42 |              550.35 |
| TPC-DS Q49    |             4252.59 |             1788.40 |             4879.77 |             1775.18 |
| TPC-DS Q50    |              601.58 |              575.60 |              547.20 |              574.35 |
| TPC-DS Q51    |             2972.54 |             2453.11 |             2492.32 |             3444.72 |
| TPC-DS Q52    |              106.92 |               94.25 |              103.05 |              108.70 |
| TPC-DS Q53    |               77.36 |               87.11 |               74.69 |               82.57 |
| TPC-DS Q54    |               89.14 |              100.01 |               98.84 |               96.69 |
| TPC-DS Q55    |               75.53 |               66.26 |               90.35 |             1164.61 |
| TPC-DS Q56    |               93.81 |              108.50 |               88.85 |              103.62 |
| TPC-DS Q57    |              146.95 |              143.35 |              136.55 |              153.66 |
| TPC-DS Q58    |             6224.42 |             5303.05 |             5158.18 |             7359.22 |
| TPC-DS Q59    |             1055.50 |             1107.29 |             1114.95 |             1192.43 |
| TPC-DS Q60    |              168.01 |              158.76 |              141.35 |              180.26 |
| TPC-DS Q61    |              201.97 |              206.88 |              207.59 |              214.27 |
| TPC-DS Q62    |              252.85 |              301.45 |             2097.85 |              352.56 |
| TPC-DS Q63    |               86.18 |               93.83 |               85.67 |               89.57 |
| TPC-DS Q64    |             3958.97 |             4593.14 |             8094.55 |             6440.59 |
| TPC-DS Q65    |             1103.59 |             1079.07 |             1133.27 |             1173.47 |
| TPC-DS Q66    |             2040.09 |             2514.33 |             2251.12 |             2644.37 |
| TPC-DS Q67    |             4823.22 |             4872.60 |             4756.53 |             7593.72 |
| TPC-DS Q68    |              348.40 |              373.84 |              330.34 |              361.50 |
| TPC-DS Q69    |              290.81 |              346.02 |              292.12 |              350.42 |
| TPC-DS Q70    |             1845.81 |             2160.23 |             2035.23 |             2975.71 |
| TPC-DS Q71    |              207.78 |              187.07 |              305.57 |             1107.15 |
| TPC-DS Q72    |             1138.92 |             1144.46 |             1156.88 |             1275.81 |
| TPC-DS Q73    |               70.82 |               83.99 |               76.18 |               83.53 |
| TPC-DS Q74    |             1801.52 |             1741.70 |             2947.44 |             1712.33 |
| TPC-DS Q75    |             5556.96 |            34708.40 |             6557.27 |             6900.06 |
| TPC-DS Q76    |             8106.24 |            17656.01 |             6669.04 |            10371.47 |
| TPC-DS Q77    |             1182.22 |              887.95 |              753.75 |              864.46 |
| TPC-DS Q78    |            12442.51 |            14639.71 |            13692.92 |            13578.45 |
| TPC-DS Q79    |              225.30 |              213.07 |              234.16 |              245.63 |
| TPC-DS Q80    |             7507.60 |             8853.23 |             9149.26 |             8269.46 |
| TPC-DS Q81    |              147.40 |              148.29 |             2136.47 |              147.63 |
| TPC-DS Q82    |              435.24 |              448.05 |              440.15 |              451.21 |
| TPC-DS Q83    |               49.59 |               56.79 |             1903.75 |              258.01 |
| TPC-DS Q84    |              350.16 |              335.76 |              354.03 |              368.74 |
| TPC-DS Q85    |             1257.63 |             1223.39 |            12030.56 |             1507.73 |
| TPC-DS Q86    |              372.85 |              377.05 |              389.84 |              422.18 |
| TPC-DS Q87    |             2588.99 |             2541.34 |             2766.70 |             3795.63 |
| TPC-DS Q88    |              500.50 |              518.47 |             2319.86 |              546.69 |
| TPC-DS Q89    |              149.22 |              143.89 |              138.91 |             1677.70 |
| TPC-DS Q90    |               70.80 |               94.24 |               72.24 |              105.92 |
| TPC-DS Q91    |             1101.26 |               79.74 |               54.04 |               80.82 |
| TPC-DS Q92    |              148.37 |              153.39 |              173.77 |             5241.62 |
| TPC-DS Q93    |             2030.58 |             2011.97 |             2032.08 |             4328.29 |
| TPC-DS Q94    |            36946.47 |            37302.68 |            38332.73 |            39547.86 |
| TPC-DS Q95    |           370600.83 |           354662.99 |           379412.24 |           375111.99 |
| TPC-DS Q96    |             1846.42 |             1394.46 |              424.03 |              409.88 |
| TPC-DS Q97    |             4147.63 |             4149.78 |             3556.72 |             3317.90 |
| TPC-DS Q98    |             2205.84 |              238.11 |             1539.75 |             2215.88 |
| TPC-DS Q99    |             1640.42 |              306.32 |              289.26 |              289.84 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

|                   |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| monetdb-1-1-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| monetdb-1-2-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| monetdb-1-2-2-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |     11121.16 |    175.59 |        1014.75 |               1023.99 |
| monetdb-1-1-2-1 |     13243.25 |    191.90 |        1005.46 |               1023.98 |
| monetdb-1-2-1-1 |     13871.87 |    170.64 |        1016.95 |               1023.97 |
| monetdb-1-2-2-1 |     12766.76 |    186.16 |         991.97 |               1024.00 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        69.37 |      0.69 |           0.61 |                  0.63 |
| monetdb-1-1-2-1 |        68.24 |      0.73 |           0.56 |                  0.57 |
| monetdb-1-2-1-1 |        70.25 |      0.89 |           0.53 |                  0.55 |
| monetdb-1-2-2-1 |        68.71 |      0.97 |           0.57 |                  0.59 |

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
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST failed: SQL warnings (result mismatch)
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
  -rss 2000Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  run &>$LOG_DIR/docs_tpcds_monetdb_3.log
```

### Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_monetdb_3_summary.md" target="_blank" rel="noopener">docs_tpcds_monetdb_3.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=30
* Type: tpcds
* Duration: 3193s 
* Code: 1792734284
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=30) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 14400.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.8.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Database is persisted to disk of type nvme and size 2000Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 1, 3] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * SUT requests 4 CPU and 900Gi RAM. RAM limit is 1024Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:920070
  * datadisk:51000
  * volume_size:2.0T
  * volume_used:50G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1792734284
* monetdb-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:920015
  * datadisk:51000
  * volume_size:2.0T
  * volume_used:50G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1792734284
* monetdb-1-1-3-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:920020
  * datadisk:51000
  * volume_size:2.0T
  * volume_used:50G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1792734284
* monetdb-1-1-3-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:920020
  * datadisk:51000
  * volume_size:2.0T
  * volume_used:50G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1792734284
* monetdb-1-1-3-1-3 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:920020
  * datadisk:51000
  * volume_size:2.0T
  * volume_used:50G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1792734284

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MonetDB-1

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1792734284-5d4d46898d-vgb5m: 0

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
| MonetDB-1-1 |                1 |   30 |      688.00 |           4.00 |            1.00 |        517.00 |          147.00 |              0 |           0 |             | None           |             0 | False         |              156.98 | True                |

### Benchmarking

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| monetdb-1-1-1-1-1 | MonetDB-1       | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        647 |            0.92 |           122585.57 |          16525.50 |          -1 | monetdb-1-1-1-1-1 |
| monetdb-1-1-2-1-1 | MonetDB-1       | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |           1 | 30.00 |               99 |                  99 |        558 |            0.64 |           179040.49 |          19161.29 |          -1 | monetdb-1-1-2-1-1 |
| monetdb-1-1-3-1-1 | MonetDB-1       | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |           1 | 30.00 |               99 |                  99 |       1593 |            0.85 |           131938.85 |           6711.86 |          -1 | monetdb-1-1-3-1-1 |
| monetdb-1-1-3-1-2 | MonetDB-1       | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |           1 | 30.00 |               99 |                  99 |        858 |            1.07 |           104503.48 |          12461.54 |          -1 | monetdb-1-1-3-1-2 |
| monetdb-1-1-3-1-3 | MonetDB-1       | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |           1 | 30.00 |               99 |                  99 |       1622 |            0.85 |           133354.40 |           6591.86 |          -1 | monetdb-1-1-3-1-3 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        647 |            0.92 |           122585.57 |          16525.50 |          -1 |
| monetdb-1-1-2 | monetdb-1-1-2 |                1 |        2 |               1 |           1 | 30.00 |               99 |                  99 |        558 |            0.64 |           179040.49 |          19161.29 |          -1 |
| monetdb-1-1-3 | monetdb-1-1-3 |                1 |        3 |               1 |           3 | 30.00 |              297 |                 297 |       1622 |            0.92 |           122509.64 |          19775.59 |          -1 |

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
| TPC-DS Q1     |             1597.41 |              251.28 |              404.99 |              391.14 |              822.32 |
| TPC-DS Q2     |             3707.42 |             2260.92 |             1879.92 |             2687.72 |             2412.33 |
| TPC-DS Q3     |             6772.81 |              141.92 |              854.65 |              214.21 |              709.42 |
| TPC-DS Q4     |            23754.43 |            14319.85 |            19912.89 |            15703.58 |            16029.96 |
| TPC-DS Q5     |            19987.04 |             1270.47 |             1577.24 |             1636.59 |             1726.09 |
| TPC-DS Q6     |              568.43 |              290.26 |             1034.23 |              452.05 |             1443.57 |
| TPC-DS Q7     |             5345.23 |              172.40 |              193.94 |              201.15 |              179.39 |
| TPC-DS Q8     |             3160.88 |              206.85 |              381.50 |              221.28 |              262.27 |
| TPC-DS Q9     |              519.26 |             1126.27 |              617.15 |             1074.57 |             1312.71 |
| TPC-DS Q10    |            22224.34 |              124.98 |              131.19 |              115.88 |              130.95 |
| TPC-DS Q11    |             6718.46 |             7903.05 |             8195.27 |             7645.84 |             6962.59 |
| TPC-DS Q12    |              253.15 |             3352.91 |             2025.47 |              871.86 |              124.42 |
| TPC-DS Q13    |              357.60 |             1631.91 |             2022.81 |             2103.34 |              314.28 |
| TPC-DS Q14a+b |            31255.23 |            30565.85 |            31390.51 |            33553.53 |            33649.77 |
| TPC-DS Q15    |              174.35 |              861.33 |              129.99 |             2058.16 |              157.28 |
| TPC-DS Q16    |            47109.07 |            40383.85 |            94729.66 |            39797.17 |            64914.01 |
| TPC-DS Q17    |             4887.11 |             1879.82 |             2148.09 |             4823.26 |             5042.48 |
| TPC-DS Q18    |             1401.98 |             1635.64 |             5170.08 |             3730.30 |             8638.36 |
| TPC-DS Q19    |              180.86 |             1446.97 |              220.99 |            14320.56 |            19996.59 |
| TPC-DS Q20    |              150.59 |              160.16 |              896.22 |             2053.83 |              231.76 |
| TPC-DS Q21    |             2491.03 |              103.63 |              106.47 |            25459.22 |              168.84 |
| TPC-DS Q22    |             1265.09 |             1078.98 |             1142.07 |             5974.90 |             1308.31 |
| TPC-DS Q23a+b |            34702.70 |            43920.03 |            45274.45 |            38201.30 |            45535.33 |
| TPC-DS Q24a+b |            39306.70 |            39127.48 |            56509.24 |            63603.04 |            56018.98 |
| TPC-DS Q25    |             2293.80 |             2287.50 |             2609.15 |             8266.52 |             7975.78 |
| TPC-DS Q26    |             1495.54 |              168.27 |             1924.45 |             1524.81 |              178.94 |
| TPC-DS Q27    |              928.45 |              961.71 |             1813.78 |             1579.50 |             1772.69 |
| TPC-DS Q28    |              630.36 |              529.80 |             1633.00 |             1236.28 |             2726.69 |
| TPC-DS Q29    |             2192.55 |             3660.81 |             2379.03 |             2856.47 |             2494.39 |
| TPC-DS Q30    |               96.68 |               71.31 |               96.02 |              325.10 |               70.55 |
| TPC-DS Q31    |             1936.59 |             1697.98 |             1866.34 |             2372.63 |             2384.68 |
| TPC-DS Q32    |              163.42 |              179.10 |              189.76 |              309.37 |              535.14 |
| TPC-DS Q33    |              114.71 |               91.98 |               99.80 |             1202.56 |              120.20 |
| TPC-DS Q34    |              104.68 |              100.89 |              105.98 |              231.79 |              187.13 |
| TPC-DS Q35    |              801.26 |              860.18 |              875.89 |              941.72 |              802.74 |
| TPC-DS Q36    |             1517.66 |             1618.78 |             1675.22 |             1616.22 |             1668.06 |
| TPC-DS Q37    |              416.09 |              433.76 |              348.03 |              439.08 |              385.13 |
| TPC-DS Q38    |             2564.39 |             2138.27 |             2808.87 |             2354.71 |             2330.16 |
| TPC-DS Q39a+b |             1257.66 |             1251.34 |             1439.76 |             1370.24 |             1349.31 |
| TPC-DS Q40    |             1574.61 |              898.16 |             1435.25 |             2468.94 |              936.77 |
| TPC-DS Q41    |                6.48 |                5.70 |                6.23 |                8.78 |                5.44 |
| TPC-DS Q42    |              105.77 |               70.87 |               75.94 |              128.40 |               82.09 |
| TPC-DS Q43    |              304.76 |              289.27 |              441.06 |              476.27 |             1957.95 |
| TPC-DS Q44    |             7993.69 |              500.65 |              477.67 |              704.59 |              492.90 |
| TPC-DS Q45    |             1163.79 |              140.73 |              166.50 |              272.89 |              167.55 |
| TPC-DS Q46    |              202.88 |              195.13 |              249.67 |              197.53 |              250.23 |
| TPC-DS Q47    |              788.13 |              781.04 |              863.12 |             1139.08 |             1279.02 |
| TPC-DS Q48    |              212.26 |              209.12 |              228.71 |              222.95 |              279.57 |
| TPC-DS Q49    |             4522.60 |             1026.49 |             1017.17 |             1252.06 |             2516.64 |
| TPC-DS Q50    |              525.46 |              512.52 |              665.55 |              549.74 |              626.30 |
| TPC-DS Q51    |             2312.30 |             2343.64 |             2649.19 |             2580.46 |             2830.79 |
| TPC-DS Q52    |               97.21 |              100.47 |              111.15 |               96.81 |               80.62 |
| TPC-DS Q53    |               76.47 |               84.27 |               83.36 |               82.08 |               87.38 |
| TPC-DS Q54    |               88.19 |               93.21 |               94.24 |              107.50 |               97.27 |
| TPC-DS Q55    |               89.64 |               84.77 |              100.37 |              105.77 |               59.96 |
| TPC-DS Q56    |               94.12 |               88.20 |              124.33 |              113.96 |              111.50 |
| TPC-DS Q57    |              136.61 |              132.48 |              154.04 |              203.96 |              146.98 |
| TPC-DS Q58    |             6275.82 |             4844.48 |             6122.77 |             4656.50 |             4337.37 |
| TPC-DS Q59    |             1096.81 |             1135.85 |              779.93 |              907.32 |              889.70 |
| TPC-DS Q60    |              119.82 |              120.68 |              123.12 |              120.19 |              106.47 |
| TPC-DS Q61    |              160.01 |              164.13 |              203.18 |              637.47 |              482.92 |
| TPC-DS Q62    |              252.32 |              245.55 |             1363.24 |              362.28 |              280.69 |
| TPC-DS Q63    |               84.50 |               92.80 |               90.98 |              101.44 |               81.69 |
| TPC-DS Q64    |             3941.21 |             3911.14 |             4538.23 |             5817.23 |             4601.79 |
| TPC-DS Q65    |             1578.48 |             1040.79 |             2855.89 |             1306.40 |             1497.94 |
| TPC-DS Q66    |             1917.58 |             1746.09 |             4981.09 |             7586.23 |             5697.03 |
| TPC-DS Q67    |             4593.13 |             4578.33 |             4911.89 |             5041.24 |             5558.25 |
| TPC-DS Q68    |              366.44 |              377.70 |              214.40 |              246.33 |              325.01 |
| TPC-DS Q69    |               98.36 |               72.69 |               61.09 |               83.02 |               66.80 |
| TPC-DS Q70    |             1876.16 |             1933.56 |             1801.66 |             1925.06 |             2148.35 |
| TPC-DS Q71    |              227.91 |              139.25 |              138.50 |              121.90 |              196.15 |
| TPC-DS Q72    |             1174.61 |             1132.73 |             1367.48 |             1139.57 |             1124.10 |
| TPC-DS Q73    |               73.54 |               81.58 |             2086.61 |               80.17 |               71.95 |
| TPC-DS Q74    |             1795.04 |             1703.94 |             3794.04 |             4700.31 |             3884.41 |
| TPC-DS Q75    |             5484.80 |             5588.02 |             6333.89 |             6355.40 |             6449.30 |
| TPC-DS Q76    |             3013.77 |              167.59 |              160.84 |              280.11 |              150.38 |
| TPC-DS Q77    |              738.02 |              769.26 |             1315.09 |             1186.98 |              768.25 |
| TPC-DS Q78    |            12295.69 |            12004.23 |            14595.10 |            15458.00 |            14822.52 |
| TPC-DS Q79    |              209.00 |              194.82 |              190.76 |              204.68 |              467.71 |
| TPC-DS Q80    |             7559.98 |             7498.00 |             9188.28 |             9447.77 |             9630.26 |
| TPC-DS Q81    |              146.74 |              146.76 |              127.63 |              205.42 |              143.58 |
| TPC-DS Q82    |              400.27 |              436.25 |              402.86 |              383.05 |             1422.24 |
| TPC-DS Q83    |              284.68 |               57.69 |               53.51 |               47.74 |              159.11 |
| TPC-DS Q84    |              399.14 |               34.63 |               31.99 |               33.84 |               31.33 |
| TPC-DS Q85    |              929.36 |              874.20 |              910.02 |              804.83 |              899.82 |
| TPC-DS Q86    |              392.11 |              383.98 |              403.86 |              380.20 |              367.24 |
| TPC-DS Q87    |             2620.05 |             2421.52 |             2719.28 |             2552.54 |             2683.82 |
| TPC-DS Q88    |              498.57 |              503.05 |              565.12 |              540.29 |             2451.31 |
| TPC-DS Q89    |              121.09 |              125.95 |              130.28 |              121.62 |              110.20 |
| TPC-DS Q90    |               72.15 |               65.38 |               84.01 |              146.56 |               67.96 |
| TPC-DS Q91    |               44.25 |               33.64 |               45.43 |               31.54 |               40.81 |
| TPC-DS Q92    |              170.27 |              160.88 |              807.21 |              185.87 |              520.18 |
| TPC-DS Q93    |             1941.84 |             1953.46 |             2735.78 |             2683.60 |             3137.62 |
| TPC-DS Q94    |            36065.55 |            37270.07 |           160860.79 |            35764.44 |           192940.43 |
| TPC-DS Q95    |           217497.11 |           206215.32 |          1017826.53 |           378028.73 |          1017694.09 |
| TPC-DS Q96    |               36.40 |               38.36 |              567.50 |            10280.38 |               51.25 |
| TPC-DS Q97    |             3343.61 |             4809.53 |             4884.06 |            15769.23 |             2963.11 |
| TPC-DS Q98    |              160.54 |              146.41 |              441.07 |             6505.34 |              155.57 |
| TPC-DS Q99    |             2186.10 |              230.62 |              379.66 |             5125.89 |              237.60 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

|                   |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| monetdb-1-1-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| monetdb-1-1-3-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| monetdb-1-1-3-1-2 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| monetdb-1-1-3-1-3 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      9257.78 |    121.48 |         986.95 |                986.96 |
| monetdb-1-1-2-1 |      9525.96 |    115.80 |         940.81 |                940.82 |
| monetdb-1-1-3-1 |     27387.42 |    214.25 |        1022.34 |               1024.00 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        28.61 |      0.38 |           0.40 |                  0.40 |
| monetdb-1-1-2-1 |        31.46 |      0.40 |           0.38 |                  0.38 |
| monetdb-1-1-3-1 |        99.95 |      1.40 |           0.41 |                  0.42 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-3-1 (bexhoma-metrics-monetdb-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-3-1 (bexhoma-metrics-monetdb-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MonetDB-1)
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST failed: SQL warnings (result mismatch)
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
```

</details>



