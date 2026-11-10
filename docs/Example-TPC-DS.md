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
  --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=2 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=4 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=6 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=20GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=1GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB \
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
  --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=2 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=4 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=6 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=20GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=1GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB \
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
  --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=2 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=4 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=6 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=20GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=1GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB \
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
* Duration: 899s 
* Code: 1794064480
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.13.
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'random_page_cost', 'target': 'container'}, '1.1'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_io_concurrency', 'target': 'container'}, '200'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'io_method', 'target': 'container'}, 'io_uring'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers_per_gather', 'target': 'container'}, '2'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers', 'target': 'container'}, '4'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_worker_processes', 'target': 'container'}, '6'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'shared_buffers', 'target': 'container'}, '20GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_cache_size', 'target': 'container'}, '48GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'work_mem', 'target': 'container'}, '1GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'maintenance_work_mem', 'target': 'container'}, '2GB')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:812221
  * datadisk:5790
  * volume_size:1.8T
  * volume_used:794G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794064480
* postgresql-1-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:812183
  * datadisk:5790
  * volume_size:1.8T
  * volume_used:794G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794064480
* postgresql-1-1-2-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:812183
  * datadisk:5790
  * volume_size:1.8T
  * volume_used:794G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794064480

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1794064480-6df7956555-69722: 0

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
| PostgreSQL-1-1 |                1 |    1 |      100.00 |           5.00 |            1.00 |         46.00 |           40.00 |              8 |           0 |             | None           |             0 | False         |               36.00 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        188 |            0.34 |            10751.29 |           1895.74 |          -1 | postgresql-1-1-1-1-1 |
| postgresql-1-1-2-1-1 | PostgreSQL-1    | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               99 |                  99 |        204 |            0.43 |             8555.40 |           1747.06 |          -1 | postgresql-1-1-2-1-1 |
| postgresql-1-1-2-1-2 | PostgreSQL-1    | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               99 |                  99 |        205 |            0.43 |             8607.32 |           1738.54 |          -1 | postgresql-1-1-2-1-2 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        188 |            0.34 |            10751.29 |           1895.74 |          -1 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        2 |               1 |           2 | 1.00 |              198 |                 198 |        205 |            0.43 |             8581.32 |           3477.07 |          -1 |

#### Query Completion per Phase

| phase            |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:-----------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| postgresql-1-1-2 |      2 | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   postgresql-1-1-1-1-1 |   postgresql-1-1-2-1-1 |   postgresql-1-1-2-1-2 |
|:--------------|-----------------------:|-----------------------:|-----------------------:|
| TPC-DS Q1     |                  82.32 |                 100.86 |                  93.04 |
| TPC-DS Q2     |                 363.62 |                 377.40 |                 368.31 |
| TPC-DS Q3     |                 105.32 |                 110.99 |                 114.33 |
| TPC-DS Q4     |                6934.86 |                7402.28 |                7982.37 |
| TPC-DS Q5     |                 520.44 |                 714.83 |                 537.94 |
| TPC-DS Q6     |               55431.05 |               55371.56 |               54797.45 |
| TPC-DS Q7     |                 336.93 |                 362.37 |                 374.01 |
| TPC-DS Q8     |                  47.17 |                  57.10 |                  61.48 |
| TPC-DS Q9     |                1820.02 |                2387.12 |                2591.46 |
| TPC-DS Q10    |                 867.08 |                1101.34 |                1669.82 |
| TPC-DS Q11    |                3296.02 |                4918.31 |                4695.32 |
| TPC-DS Q12    |                  52.37 |                  71.20 |                  84.11 |
| TPC-DS Q13    |                 484.95 |                 599.46 |                 570.61 |
| TPC-DS Q14a+b |                2977.82 |                3599.79 |                3074.25 |
| TPC-DS Q15    |                 101.57 |                 116.46 |                 120.96 |
| TPC-DS Q16    |                 186.72 |                 372.82 |                 253.87 |
| TPC-DS Q17    |                 246.18 |                 310.52 |                 339.97 |
| TPC-DS Q18    |                 336.35 |                 391.15 |                 405.41 |
| TPC-DS Q19    |                 129.63 |                 182.98 |                 183.61 |
| TPC-DS Q20    |                  79.25 |                 116.07 |                 104.27 |
| TPC-DS Q21    |                 234.00 |                 298.20 |                 285.30 |
| TPC-DS Q22    |                3244.62 |                3934.08 |                4505.75 |
| TPC-DS Q23a+b |                3971.72 |                6386.12 |                5138.12 |
| TPC-DS Q24a+b |                 318.66 |                 395.24 |                 404.40 |
| TPC-DS Q25    |                 277.20 |                 337.59 |                 335.19 |
| TPC-DS Q26    |                 205.08 |                 279.06 |                 326.87 |
| TPC-DS Q27    |                 312.02 |                 702.41 |                 675.12 |
| TPC-DS Q28    |                1400.08 |                2512.42 |                2542.97 |
| TPC-DS Q29    |                 262.89 |                 399.85 |                 383.99 |
| TPC-DS Q30    |                8105.04 |               11794.29 |               11765.55 |
| TPC-DS Q31    |                1394.24 |                2194.75 |                1997.66 |
| TPC-DS Q32    |                  88.57 |                 100.10 |                  92.71 |
| TPC-DS Q33    |                 303.81 |                 385.50 |                 381.00 |
| TPC-DS Q34    |                  16.65 |                  28.10 |                  27.46 |
| TPC-DS Q35    |                 954.72 |                1273.29 |                1308.76 |
| TPC-DS Q36    |                 265.66 |                 496.26 |                 503.04 |
| TPC-DS Q37    |                 269.75 |                 503.22 |                 382.98 |
| TPC-DS Q38    |                 815.93 |                1517.43 |                1454.84 |
| TPC-DS Q39a+b |                2531.97 |                3239.77 |                3219.05 |
| TPC-DS Q40    |                 108.22 |                 134.75 |                 128.31 |
| TPC-DS Q41    |                 775.41 |                1082.21 |                1157.52 |
| TPC-DS Q42    |                  91.19 |                 115.80 |                 103.07 |
| TPC-DS Q43    |                  18.98 |                  20.16 |                  29.15 |
| TPC-DS Q44    |                 376.34 |                 477.42 |                 464.81 |
| TPC-DS Q45    |                  63.90 |                  89.77 |                  83.96 |
| TPC-DS Q46    |                  23.52 |                  28.09 |                  30.47 |
| TPC-DS Q47    |                1268.57 |                1615.84 |                1687.19 |
| TPC-DS Q48    |                 637.07 |                 730.54 |                1311.89 |
| TPC-DS Q49    |                 432.88 |                1048.89 |                 794.53 |
| TPC-DS Q50    |                 409.32 |                 490.85 |                 461.26 |
| TPC-DS Q51    |                 690.31 |                1108.03 |                1332.17 |
| TPC-DS Q52    |                  87.15 |                 107.07 |                 102.78 |
| TPC-DS Q53    |                 105.27 |                 143.67 |                 150.94 |
| TPC-DS Q54    |                  60.83 |                  82.53 |                  80.84 |
| TPC-DS Q55    |                  82.14 |                 102.59 |                 103.13 |
| TPC-DS Q56    |                 299.94 |                 398.66 |                 403.07 |
| TPC-DS Q57    |                 740.47 |                1228.74 |                1462.36 |
| TPC-DS Q58    |                 610.90 |                 790.69 |                 420.45 |
| TPC-DS Q59    |                 554.89 |                 521.18 |                 588.86 |
| TPC-DS Q60    |                 410.09 |                 440.91 |                 436.69 |
| TPC-DS Q61    |                 127.62 |                 153.55 |                 135.21 |
| TPC-DS Q62    |                  99.06 |                 104.74 |                 113.63 |
| TPC-DS Q63    |                 112.29 |                 130.56 |                 136.77 |
| TPC-DS Q64    |                 643.08 |                 819.87 |                1007.34 |
| TPC-DS Q65    |                 509.05 |                 730.90 |                 956.13 |
| TPC-DS Q66    |                 171.22 |                 215.22 |                 214.60 |
| TPC-DS Q67    |                3007.08 |                4300.23 |                4317.02 |
| TPC-DS Q68    |                  29.44 |                  34.52 |                  39.34 |
| TPC-DS Q69    |                 299.58 |                 410.94 |                 389.48 |
| TPC-DS Q70    |                 339.59 |                 497.33 |                 585.65 |
| TPC-DS Q71    |                 265.37 |                 314.17 |                 588.17 |
| TPC-DS Q72    |                 825.52 |                1486.53 |                1369.41 |
| TPC-DS Q73    |                  23.64 |                  51.21 |                  29.17 |
| TPC-DS Q74    |                1563.00 |                1384.75 |                1101.72 |
| TPC-DS Q75    |                 571.65 |                 794.44 |                 866.89 |
| TPC-DS Q76    |                 206.46 |                 293.63 |                 250.90 |
| TPC-DS Q77    |                 277.08 |                 357.67 |                 574.63 |
| TPC-DS Q78    |                1106.27 |                1612.14 |                1567.41 |
| TPC-DS Q79    |                 120.05 |                 209.10 |                 149.59 |
| TPC-DS Q80    |                 531.08 |                 570.98 |                 527.96 |
| TPC-DS Q81    |               47514.05 |               41824.51 |               42209.39 |
| TPC-DS Q82    |                 419.02 |                 368.86 |                 361.36 |
| TPC-DS Q83    |                  74.44 |                  63.72 |                  63.63 |
| TPC-DS Q84    |                  83.20 |                  64.40 |                  68.06 |
| TPC-DS Q85    |                 348.48 |                 484.10 |                 427.28 |
| TPC-DS Q86    |                 193.39 |                 296.21 |                 153.79 |
| TPC-DS Q87    |                1064.61 |                 815.09 |                 844.53 |
| TPC-DS Q88    |                2920.21 |                1956.96 |                1950.43 |
| TPC-DS Q89    |                  25.10 |                  22.44 |                  21.93 |
| TPC-DS Q90    |                 122.59 |                  97.37 |                  86.81 |
| TPC-DS Q91    |                 140.38 |                 116.44 |                 111.43 |
| TPC-DS Q92    |                  58.86 |                  50.86 |                  41.75 |
| TPC-DS Q93    |                 272.43 |                 227.43 |                 197.81 |
| TPC-DS Q94    |                 166.02 |                 127.64 |                 330.92 |
| TPC-DS Q95    |                4487.29 |                3705.83 |                3418.82 |
| TPC-DS Q96    |                 105.62 |                  96.10 |                  94.67 |
| TPC-DS Q97    |                 442.97 |                 408.00 |                 334.45 |
| TPC-DS Q98    |                 169.81 |                 306.52 |                 310.21 |
| TPC-DS Q99    |                 195.71 |                 363.38 |                 280.74 |

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
  --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=2 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=4 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=6 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=20GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=1GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB \
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
* Duration: 1077s 
* Code: 1793872554
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
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
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:878780
  * datadisk:5790
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
    * code:1793872554
* postgresql-1-2-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:893631
  * datadisk:5790
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
    * code:1793872554

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: PostgreSQL-1-2

### Data Parameters of Reused Volumes
* PostgreSQL-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793872554-858cd4cb9b-4mm7t: 0
* bexhoma-sut-postgresql-1-1793872554-544fd7d6d9-qxb5g: 0

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
| PostgreSQL-1-1 |                1 |    1 |      104.00 |           2.00 |            0.00 |         56.00 |           37.00 |              8 |           0 |             | None           |             0 | False         |               34.62 | False               |
| PostgreSQL-1-2 |                2 |    1 |      104.00 |           2.00 |            0.00 |         56.00 |           37.00 |              8 |           0 |             | None           |             0 | False         |               34.62 | True                |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        204 |            0.36 |            10277.17 |           1747.06 |          -1 | postgresql-1-1-1-1-1 |
| postgresql-1-2-1-1-1 | PostgreSQL-1    | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        201 |            0.40 |             9279.48 |           1773.13 |          -1 | postgresql-1-2-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        204 |            0.36 |            10277.17 |           1747.06 |          -1 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        201 |            0.40 |             9279.48 |           1773.13 |          -1 |

#### Query Completion per Phase

| phase            |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:-----------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| postgresql-1-2-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   postgresql-1-1-1-1-1 |   postgresql-1-2-1-1-1 |
|:--------------|-----------------------:|-----------------------:|
| TPC-DS Q1     |                  78.57 |                3406.38 |
| TPC-DS Q2     |                 343.67 |                1429.11 |
| TPC-DS Q3     |                 105.03 |                 678.32 |
| TPC-DS Q4     |                6250.10 |                7425.21 |
| TPC-DS Q5     |                 773.17 |                 670.86 |
| TPC-DS Q6     |               59432.00 |               62316.77 |
| TPC-DS Q7     |                 372.86 |                1061.78 |
| TPC-DS Q8     |                 101.85 |                  50.84 |
| TPC-DS Q9     |                2326.82 |                2210.19 |
| TPC-DS Q10    |                 906.38 |                6629.32 |
| TPC-DS Q11    |                4203.30 |                3632.85 |
| TPC-DS Q12    |                  56.20 |                  59.03 |
| TPC-DS Q13    |                 481.33 |                 514.34 |
| TPC-DS Q14a+b |                2268.85 |                2921.00 |
| TPC-DS Q15    |                 106.57 |                 106.00 |
| TPC-DS Q16    |                 204.20 |                 354.32 |
| TPC-DS Q17    |                 261.86 |                 302.60 |
| TPC-DS Q18    |                 327.07 |                 401.41 |
| TPC-DS Q19    |                 122.87 |                 136.34 |
| TPC-DS Q20    |                  81.05 |                  88.48 |
| TPC-DS Q21    |                 422.52 |                 686.87 |
| TPC-DS Q22    |                3896.81 |                3545.15 |
| TPC-DS Q23a+b |                4487.89 |                4258.04 |
| TPC-DS Q24a+b |                 468.85 |                 722.40 |
| TPC-DS Q25    |                 254.98 |                 271.84 |
| TPC-DS Q26    |                 241.10 |                 268.56 |
| TPC-DS Q27    |                 304.38 |                 343.93 |
| TPC-DS Q28    |                1491.02 |                2144.30 |
| TPC-DS Q29    |                 443.79 |                 313.62 |
| TPC-DS Q30    |                8306.46 |                8611.32 |
| TPC-DS Q31    |                1750.15 |                1613.82 |
| TPC-DS Q32    |                  99.04 |                 227.90 |
| TPC-DS Q33    |                 308.89 |                 335.38 |
| TPC-DS Q34    |                  18.83 |                  21.91 |
| TPC-DS Q35    |                1104.94 |                1025.50 |
| TPC-DS Q36    |                 267.51 |                 301.63 |
| TPC-DS Q37    |                 281.89 |                 274.07 |
| TPC-DS Q38    |                1358.88 |                 878.28 |
| TPC-DS Q39a+b |                2579.46 |                2661.56 |
| TPC-DS Q40    |                 104.47 |                 140.08 |
| TPC-DS Q41    |                 754.34 |                 808.10 |
| TPC-DS Q42    |                  93.63 |                  89.50 |
| TPC-DS Q43    |                  22.50 |                  22.36 |
| TPC-DS Q44    |                   2.77 |                   8.75 |
| TPC-DS Q45    |                  70.72 |                  75.08 |
| TPC-DS Q46    |                  34.52 |                  28.60 |
| TPC-DS Q47    |                2462.33 |                1331.88 |
| TPC-DS Q48    |                 462.23 |                 542.14 |
| TPC-DS Q49    |                 448.91 |                 661.17 |
| TPC-DS Q50    |                 320.75 |                 505.55 |
| TPC-DS Q51    |                 848.84 |                 794.29 |
| TPC-DS Q52    |                 105.73 |                  98.14 |
| TPC-DS Q53    |                 129.56 |                 135.33 |
| TPC-DS Q54    |                  67.44 |                  76.86 |
| TPC-DS Q55    |                  86.98 |                 100.41 |
| TPC-DS Q56    |                 273.24 |                 350.45 |
| TPC-DS Q57    |                 705.35 |                 779.87 |
| TPC-DS Q58    |                 320.41 |                 345.58 |
| TPC-DS Q59    |                 431.32 |                 463.86 |
| TPC-DS Q60    |                 313.83 |                 343.68 |
| TPC-DS Q61    |                 211.69 |                 137.23 |
| TPC-DS Q62    |                 157.56 |                 149.29 |
| TPC-DS Q63    |                 225.37 |                 166.36 |
| TPC-DS Q64    |                1247.39 |                 817.97 |
| TPC-DS Q65    |                 508.87 |                 552.27 |
| TPC-DS Q66    |                 154.69 |                 208.91 |
| TPC-DS Q67    |                2512.72 |                2991.78 |
| TPC-DS Q68    |                  38.77 |                  32.70 |
| TPC-DS Q69    |                 117.93 |                 131.43 |
| TPC-DS Q70    |                 362.42 |                 355.01 |
| TPC-DS Q71    |                 707.54 |                 263.71 |
| TPC-DS Q72    |                1304.07 |                 833.87 |
| TPC-DS Q73    |                  22.93 |                  22.17 |
| TPC-DS Q74    |                1141.86 |                1165.25 |
| TPC-DS Q75    |                 957.68 |                 633.99 |
| TPC-DS Q76    |                 223.04 |                 249.57 |
| TPC-DS Q77    |                 291.18 |                 275.68 |
| TPC-DS Q78    |                 909.38 |                1028.32 |
| TPC-DS Q79    |                 129.75 |                 153.13 |
| TPC-DS Q80    |                 420.74 |                 451.05 |
| TPC-DS Q81    |               41625.53 |               35871.32 |
| TPC-DS Q82    |                 424.15 |                 344.28 |
| TPC-DS Q83    |                  99.29 |                  69.86 |
| TPC-DS Q84    |                  77.34 |                  68.96 |
| TPC-DS Q85    |                 287.57 |                 256.54 |
| TPC-DS Q86    |                 162.28 |                 260.11 |
| TPC-DS Q87    |                1119.58 |                1077.82 |
| TPC-DS Q88    |                2194.86 |                2215.90 |
| TPC-DS Q89    |                 141.82 |                 103.70 |
| TPC-DS Q90    |                 101.84 |                  95.05 |
| TPC-DS Q91    |                 148.51 |                 118.98 |
| TPC-DS Q92    |                  95.70 |                  62.10 |
| TPC-DS Q93    |                 366.70 |                 248.83 |
| TPC-DS Q94    |                 150.15 |                 143.31 |
| TPC-DS Q95    |                2931.78 |                2713.11 |
| TPC-DS Q96    |                  90.43 |                  94.16 |
| TPC-DS Q97    |                 351.45 |                 348.42 |
| TPC-DS Q98    |                 165.27 |                 141.13 |
| TPC-DS Q99    |                 370.88 |                 230.47 |

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
  -rss 100Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=2 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=4 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=6 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=20GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=1GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB \
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
* Duration: 2549s 
* Code: 1793879951
* We compute for all columns: Minimum, maximum, average, count, count distinct, count NULL and non NULL entries and coefficient of variation.
* This experiment compares imported TPC-DS data sets in different DBMS.
  * TPC-DS (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 100Gi.
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
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:956397
  * datadisk:60749
  * volume_size:98G
  * volume_used:60G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793879951
* postgresql-1-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:956382
  * datadisk:60749
  * volume_size:98G
  * volume_used:60G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793879951

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793879951-f575c9c9d-thln5: 0

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
| PostgreSQL-1-1 |                1 |   10 |      757.00 |           2.00 |            1.00 |        447.00 |          296.00 |              8 |           0 |             | None           |             0 | False         |               47.56 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |              429 |                 429 |        738 |            0.06 |           653052.84 |          20926.83 |          -1 | postgresql-1-1-1-1-1 |
| postgresql-1-1-2-1-1 | PostgreSQL-1    | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |           1 | 10.00 |              429 |                 429 |        725 |            0.06 |           676585.80 |          21302.07 |          -1 | postgresql-1-1-2-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |              429 |                 429 |        738 |            0.06 |           653052.84 |          20926.83 |          -1 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        2 |               1 |           1 | 10.00 |              429 |                 429 |        725 |            0.06 |           676585.80 |          21302.07 |          -1 |

#### Query Completion per Phase

| phase            |   pods | statistics_tab about call_center.cc_call_center_sk - all   | statistics_tab about call_center.cc_call_center_id - all   | statistics_tab about call_center.cc_rec_start_date - all   | statistics_tab about call_center.cc_rec_end_date - all   | statistics_tab about call_center.cc_closed_date_sk - all   | statistics_tab about call_center.cc_open_date_sk - all   | statistics_tab about call_center.cc_name - all   | statistics_tab about call_center.cc_class - all   | statistics_tab about call_center.cc_employees - all   | statistics_tab about call_center.cc_sq_ft - all   | statistics_tab about call_center.cc_hours - all   | statistics_tab about call_center.cc_manager - all   | statistics_tab about call_center.cc_mkt_id - all   | statistics_tab about call_center.cc_mkt_class - all   | statistics_tab about call_center.cc_mkt_desc - all   | statistics_tab about call_center.cc_market_manager - all   | statistics_tab about call_center.cc_division - all   | statistics_tab about call_center.cc_division_name - all   | statistics_tab about call_center.cc_company - all   | statistics_tab about call_center.cc_company_name - all   | statistics_tab about call_center.cc_street_number - all   | statistics_tab about call_center.cc_street_name - all   | statistics_tab about call_center.cc_street_type - all   | statistics_tab about call_center.cc_suite_number - all   | statistics_tab about call_center.cc_city - all   | statistics_tab about call_center.cc_county - all   | statistics_tab about call_center.cc_state - all   | statistics_tab about call_center.cc_zip - all   | statistics_tab about call_center.cc_country - all   | statistics_tab about call_center.cc_gmt_offset - all   | statistics_tab about call_center.cc_tax_percentage - all   | statistics_tab about catalog_page.cp_catalog_page_sk - all   | statistics_tab about catalog_page.cp_catalog_page_id - all   | statistics_tab about catalog_page.cp_start_date_sk - all   | statistics_tab about catalog_page.cp_end_date_sk - all   | statistics_tab about catalog_page.cp_department - all   | statistics_tab about catalog_page.cp_catalog_number - all   | statistics_tab about catalog_page.cp_catalog_page_number - all   | statistics_tab about catalog_page.cp_description - all   | statistics_tab about catalog_page.cp_type - all   | statistics_tab about catalog_returns.cr_returned_date_sk - all   | statistics_tab about catalog_returns.cr_returned_time_sk - all   | statistics_tab about catalog_returns.cr_item_sk - all   | statistics_tab about catalog_returns.cr_refunded_customer_sk - all   | statistics_tab about catalog_returns.cr_refunded_cdemo_sk - all   | statistics_tab about catalog_returns.cr_refunded_hdemo_sk - all   | statistics_tab about catalog_returns.cr_refunded_addr_sk - all   | statistics_tab about catalog_returns.cr_returning_customer_sk - all   | statistics_tab about catalog_returns.cr_returning_cdemo_sk - all   | statistics_tab about catalog_returns.cr_returning_hdemo_sk - all   | statistics_tab about catalog_returns.cr_returning_addr_sk - all   | statistics_tab about catalog_returns.cr_call_center_sk - all   | statistics_tab about catalog_returns.cr_catalog_page_sk - all   | statistics_tab about catalog_returns.cr_ship_mode_sk - all   | statistics_tab about catalog_returns.cr_warehouse_sk - all   | statistics_tab about catalog_returns.cr_reason_sk - all   | statistics_tab about catalog_returns.cr_order_number - all   | statistics_tab about catalog_returns.cr_return_quantity - all   | statistics_tab about catalog_returns.cr_return_amount - all   | statistics_tab about catalog_returns.cr_return_tax - all   | statistics_tab about catalog_returns.cr_return_amt_inc_tax - all   | statistics_tab about catalog_returns.cr_fee - all   | statistics_tab about catalog_returns.cr_return_ship_cost - all   | statistics_tab about catalog_returns.cr_refunded_cash - all   | statistics_tab about catalog_returns.cr_reversed_charge - all   | statistics_tab about catalog_returns.cr_store_credit - all   | statistics_tab about catalog_returns.cr_net_loss - all   | statistics_tab about catalog_sales.cs_sold_date_sk - all   | statistics_tab about catalog_sales.cs_sold_time_sk - all   | statistics_tab about catalog_sales.cs_ship_date_sk - all   | statistics_tab about catalog_sales.cs_bill_customer_sk - all   | statistics_tab about catalog_sales.cs_bill_cdemo_sk - all   | statistics_tab about catalog_sales.cs_bill_hdemo_sk - all   | statistics_tab about catalog_sales.cs_bill_addr_sk - all   | statistics_tab about catalog_sales.cs_ship_customer_sk - all   | statistics_tab about catalog_sales.cs_ship_cdemo_sk - all   | statistics_tab about catalog_sales.cs_ship_hdemo_sk - all   | statistics_tab about catalog_sales.cs_ship_addr_sk - all   | statistics_tab about catalog_sales.cs_call_center_sk - all   | statistics_tab about catalog_sales.cs_catalog_page_sk - all   | statistics_tab about catalog_sales.cs_ship_mode_sk - all   | statistics_tab about catalog_sales.cs_warehouse_sk - all   | statistics_tab about catalog_sales.cs_item_sk - all   | statistics_tab about catalog_sales.cs_promo_sk - all   | statistics_tab about catalog_sales.cs_order_number - all   | statistics_tab about catalog_sales.cs_quantity - all   | statistics_tab about catalog_sales.cs_wholesale_cost - all   | statistics_tab about catalog_sales.cs_list_price - all   | statistics_tab about catalog_sales.cs_sales_price - all   | statistics_tab about catalog_sales.cs_ext_discount_amt - all   | statistics_tab about catalog_sales.cs_ext_sales_price - all   | statistics_tab about catalog_sales.cs_ext_wholesale_cost - all   | statistics_tab about catalog_sales.cs_ext_list_price - all   | statistics_tab about catalog_sales.cs_ext_tax - all   | statistics_tab about catalog_sales.cs_coupon_amt - all   | statistics_tab about catalog_sales.cs_ext_ship_cost - all   | statistics_tab about catalog_sales.cs_net_paid - all   | statistics_tab about catalog_sales.cs_net_paid_inc_tax - all   | statistics_tab about catalog_sales.cs_net_paid_inc_ship - all   | statistics_tab about catalog_sales.cs_net_paid_inc_ship_tax - all   | statistics_tab about catalog_sales.cs_net_profit - all   | statistics_tab about customer.c_customer_sk - all   | statistics_tab about customer.c_customer_id - all   | statistics_tab about customer.c_current_cdemo_sk - all   | statistics_tab about customer.c_current_hdemo_sk - all   | statistics_tab about customer.c_current_addr_sk - all   | statistics_tab about customer.c_first_shipto_date_sk - all   | statistics_tab about customer.c_first_sales_date_sk - all   | statistics_tab about customer.c_salutation - all   | statistics_tab about customer.c_first_name - all   | statistics_tab about customer.c_last_name - all   | statistics_tab about customer.c_preferred_cust_flag - all   | statistics_tab about customer.c_birth_day - all   | statistics_tab about customer.c_birth_month - all   | statistics_tab about customer.c_birth_year - all   | statistics_tab about customer.c_birth_country - all   | statistics_tab about customer.c_login - all   | statistics_tab about customer.c_email_address - all   | statistics_tab about customer.c_last_review_date - all   | statistics_tab about customer_address.ca_address_sk - all   | statistics_tab about customer_address.ca_address_id - all   | statistics_tab about customer_address.ca_street_number - all   | statistics_tab about customer_address.ca_street_name - all   | statistics_tab about customer_address.ca_street_type - all   | statistics_tab about customer_address.ca_suite_number - all   | statistics_tab about customer_address.ca_city - all   | statistics_tab about customer_address.ca_county - all   | statistics_tab about customer_address.ca_state - all   | statistics_tab about customer_address.ca_zip - all   | statistics_tab about customer_address.ca_country - all   | statistics_tab about customer_address.ca_gmt_offset - all   | statistics_tab about customer_address.ca_location_type - all   | statistics_tab about customer_demographics.cd_demo_sk - all   | statistics_tab about customer_demographics.cd_gender - all   | statistics_tab about customer_demographics.cd_marital_status - all   | statistics_tab about customer_demographics.cd_education_status - all   | statistics_tab about customer_demographics.cd_purchase_estimate - all   | statistics_tab about customer_demographics.cd_credit_rating - all   | statistics_tab about customer_demographics.cd_dep_count - all   | statistics_tab about customer_demographics.cd_dep_employed_count - all   | statistics_tab about customer_demographics.cd_dep_college_count - all   | statistics_tab about date_dim.d_date_sk - all   | statistics_tab about date_dim.d_date_id - all   | statistics_tab about date_dim.d_date - all   | statistics_tab about date_dim.d_month_seq - all   | statistics_tab about date_dim.d_week_seq - all   | statistics_tab about date_dim.d_quarter_seq - all   | statistics_tab about date_dim.d_year - all   | statistics_tab about date_dim.d_dow - all   | statistics_tab about date_dim.d_moy - all   | statistics_tab about date_dim.d_dom - all   | statistics_tab about date_dim.d_qoy - all   | statistics_tab about date_dim.d_fy_year - all   | statistics_tab about date_dim.d_fy_quarter_seq - all   | statistics_tab about date_dim.d_fy_week_seq - all   | statistics_tab about date_dim.d_day_name - all   | statistics_tab about date_dim.d_quarter_name - all   | statistics_tab about date_dim.d_holiday - all   | statistics_tab about date_dim.d_weekend - all   | statistics_tab about date_dim.d_following_holiday - all   | statistics_tab about date_dim.d_first_dom - all   | statistics_tab about date_dim.d_last_dom - all   | statistics_tab about date_dim.d_same_day_ly - all   | statistics_tab about date_dim.d_same_day_lq - all   | statistics_tab about date_dim.d_current_day - all   | statistics_tab about date_dim.d_current_week - all   | statistics_tab about date_dim.d_current_month - all   | statistics_tab about date_dim.d_current_quarter - all   | statistics_tab about date_dim.d_current_year - all   | statistics_tab about dbgen_version.dv_version - all   | statistics_tab about dbgen_version.dv_create_date - all   | statistics_tab about dbgen_version.dv_create_time - all   | statistics_tab about dbgen_version.dv_cmdline_args - all   | statistics_tab about household_demographics.hd_demo_sk - all   | statistics_tab about household_demographics.hd_income_band_sk - all   | statistics_tab about household_demographics.hd_buy_potential - all   | statistics_tab about household_demographics.hd_dep_count - all   | statistics_tab about household_demographics.hd_vehicle_count - all   | statistics_tab about income_band.ib_income_band_sk - all   | statistics_tab about income_band.ib_lower_bound - all   | statistics_tab about income_band.ib_upper_bound - all   | statistics_tab about inventory.inv_date_sk - all   | statistics_tab about inventory.inv_item_sk - all   | statistics_tab about inventory.inv_warehouse_sk - all   | statistics_tab about inventory.inv_quantity_on_hand - all   | statistics_tab about item.i_item_sk - all   | statistics_tab about item.i_item_id - all   | statistics_tab about item.i_rec_start_date - all   | statistics_tab about item.i_rec_end_date - all   | statistics_tab about item.i_item_desc - all   | statistics_tab about item.i_current_price - all   | statistics_tab about item.i_wholesale_cost - all   | statistics_tab about item.i_brand_id - all   | statistics_tab about item.i_brand - all   | statistics_tab about item.i_class_id - all   | statistics_tab about item.i_class - all   | statistics_tab about item.i_category_id - all   | statistics_tab about item.i_category - all   | statistics_tab about item.i_manufact_id - all   | statistics_tab about item.i_manufact - all   | statistics_tab about item.i_size - all   | statistics_tab about item.i_formulation - all   | statistics_tab about item.i_color - all   | statistics_tab about item.i_units - all   | statistics_tab about item.i_container - all   | statistics_tab about item.i_manager_id - all   | statistics_tab about item.i_product_name - all   | statistics_tab about promotion.p_promo_sk - all   | statistics_tab about promotion.p_promo_id - all   | statistics_tab about promotion.p_start_date_sk - all   | statistics_tab about promotion.p_end_date_sk - all   | statistics_tab about promotion.p_item_sk - all   | statistics_tab about promotion.p_cost - all   | statistics_tab about promotion.p_response_target - all   | statistics_tab about promotion.p_promo_name - all   | statistics_tab about promotion.p_channel_dmail - all   | statistics_tab about promotion.p_channel_email - all   | statistics_tab about promotion.p_channel_catalog - all   | statistics_tab about promotion.p_channel_tv - all   | statistics_tab about promotion.p_channel_radio - all   | statistics_tab about promotion.p_channel_press - all   | statistics_tab about promotion.p_channel_event - all   | statistics_tab about promotion.p_channel_demo - all   | statistics_tab about promotion.p_channel_details - all   | statistics_tab about promotion.p_purpose - all   | statistics_tab about promotion.p_discount_active - all   | statistics_tab about reason.r_reason_sk - all   | statistics_tab about reason.r_reason_id - all   | statistics_tab about reason.r_reason_desc - all   | statistics_tab about ship_mode.sm_ship_mode_sk - all   | statistics_tab about ship_mode.sm_ship_mode_id - all   | statistics_tab about ship_mode.sm_type - all   | statistics_tab about ship_mode.sm_code - all   | statistics_tab about ship_mode.sm_carrier - all   | statistics_tab about ship_mode.sm_contract - all   | statistics_tab about store.s_store_sk - all   | statistics_tab about store.s_store_id - all   | statistics_tab about store.s_rec_start_date - all   | statistics_tab about store.s_rec_end_date - all   | statistics_tab about store.s_closed_date_sk - all   | statistics_tab about store.s_store_name - all   | statistics_tab about store.s_number_employees - all   | statistics_tab about store.s_floor_space - all   | statistics_tab about store.s_hours - all   | statistics_tab about store.s_manager - all   | statistics_tab about store.s_market_id - all   | statistics_tab about store.s_geography_class - all   | statistics_tab about store.s_market_desc - all   | statistics_tab about store.s_market_manager - all   | statistics_tab about store.s_division_id - all   | statistics_tab about store.s_division_name - all   | statistics_tab about store.s_company_id - all   | statistics_tab about store.s_company_name - all   | statistics_tab about store.s_street_number - all   | statistics_tab about store.s_street_name - all   | statistics_tab about store.s_street_type - all   | statistics_tab about store.s_suite_number - all   | statistics_tab about store.s_city - all   | statistics_tab about store.s_county - all   | statistics_tab about store.s_state - all   | statistics_tab about store.s_zip - all   | statistics_tab about store.s_country - all   | statistics_tab about store.s_gmt_offset - all   | statistics_tab about store.s_tax_precentage - all   | statistics_tab about store_returns.sr_returned_date_sk - all   | statistics_tab about store_returns.sr_return_time_sk - all   | statistics_tab about store_returns.sr_item_sk - all   | statistics_tab about store_returns.sr_customer_sk - all   | statistics_tab about store_returns.sr_cdemo_sk - all   | statistics_tab about store_returns.sr_hdemo_sk - all   | statistics_tab about store_returns.sr_addr_sk - all   | statistics_tab about store_returns.sr_store_sk - all   | statistics_tab about store_returns.sr_reason_sk - all   | statistics_tab about store_returns.sr_ticket_number - all   | statistics_tab about store_returns.sr_return_quantity - all   | statistics_tab about store_returns.sr_return_amt - all   | statistics_tab about store_returns.sr_return_tax - all   | statistics_tab about store_returns.sr_return_amt_inc_tax - all   | statistics_tab about store_returns.sr_fee - all   | statistics_tab about store_returns.sr_return_ship_cost - all   | statistics_tab about store_returns.sr_refunded_cash - all   | statistics_tab about store_returns.sr_reversed_charge - all   | statistics_tab about store_returns.sr_store_credit - all   | statistics_tab about store_returns.sr_net_loss - all   | statistics_tab about store_sales.ss_sold_date_sk - all   | statistics_tab about store_sales.ss_sold_time_sk - all   | statistics_tab about store_sales.ss_item_sk - all   | statistics_tab about store_sales.ss_customer_sk - all   | statistics_tab about store_sales.ss_cdemo_sk - all   | statistics_tab about store_sales.ss_hdemo_sk - all   | statistics_tab about store_sales.ss_addr_sk - all   | statistics_tab about store_sales.ss_store_sk - all   | statistics_tab about store_sales.ss_promo_sk - all   | statistics_tab about store_sales.ss_ticket_number - all   | statistics_tab about store_sales.ss_quantity - all   | statistics_tab about store_sales.ss_wholesale_cost - all   | statistics_tab about store_sales.ss_list_price - all   | statistics_tab about store_sales.ss_sales_price - all   | statistics_tab about store_sales.ss_ext_discount_amt - all   | statistics_tab about store_sales.ss_ext_sales_price - all   | statistics_tab about store_sales.ss_ext_wholesale_cost - all   | statistics_tab about store_sales.ss_ext_list_price - all   | statistics_tab about store_sales.ss_ext_tax - all   | statistics_tab about store_sales.ss_coupon_amt - all   | statistics_tab about store_sales.ss_net_paid - all   | statistics_tab about store_sales.ss_net_paid_inc_tax - all   | statistics_tab about store_sales.ss_net_profit - all   | statistics_tab about time_dim.t_time_sk - all   | statistics_tab about time_dim.t_time_id - all   | statistics_tab about time_dim.t_time - all   | statistics_tab about time_dim.t_hour - all   | statistics_tab about time_dim.t_minute - all   | statistics_tab about time_dim.t_second - all   | statistics_tab about time_dim.t_am_pm - all   | statistics_tab about time_dim.t_shift - all   | statistics_tab about time_dim.t_sub_shift - all   | statistics_tab about time_dim.t_meal_time - all   | statistics_tab about warehouse.w_warehouse_sk - all   | statistics_tab about warehouse.w_warehouse_id - all   | statistics_tab about warehouse.w_warehouse_name - all   | statistics_tab about warehouse.w_warehouse_sq_ft - all   | statistics_tab about warehouse.w_street_number - all   | statistics_tab about warehouse.w_street_name - all   | statistics_tab about warehouse.w_street_type - all   | statistics_tab about warehouse.w_suite_number - all   | statistics_tab about warehouse.w_city - all   | statistics_tab about warehouse.w_county - all   | statistics_tab about warehouse.w_state - all   | statistics_tab about warehouse.w_zip - all   | statistics_tab about warehouse.w_country - all   | statistics_tab about warehouse.w_gmt_offset - all   | statistics_tab about web_page.wp_web_page_sk - all   | statistics_tab about web_page.wp_web_page_id - all   | statistics_tab about web_page.wp_rec_start_date - all   | statistics_tab about web_page.wp_rec_end_date - all   | statistics_tab about web_page.wp_creation_date_sk - all   | statistics_tab about web_page.wp_access_date_sk - all   | statistics_tab about web_page.wp_autogen_flag - all   | statistics_tab about web_page.wp_customer_sk - all   | statistics_tab about web_page.wp_url - all   | statistics_tab about web_page.wp_type - all   | statistics_tab about web_page.wp_char_count - all   | statistics_tab about web_page.wp_link_count - all   | statistics_tab about web_page.wp_image_count - all   | statistics_tab about web_page.wp_max_ad_count - all   | statistics_tab about web_returns.wr_returned_date_sk - all   | statistics_tab about web_returns.wr_returned_time_sk - all   | statistics_tab about web_returns.wr_item_sk - all   | statistics_tab about web_returns.wr_refunded_customer_sk - all   | statistics_tab about web_returns.wr_refunded_cdemo_sk - all   | statistics_tab about web_returns.wr_refunded_hdemo_sk - all   | statistics_tab about web_returns.wr_refunded_addr_sk - all   | statistics_tab about web_returns.wr_returning_customer_sk - all   | statistics_tab about web_returns.wr_returning_cdemo_sk - all   | statistics_tab about web_returns.wr_returning_hdemo_sk - all   | statistics_tab about web_returns.wr_returning_addr_sk - all   | statistics_tab about web_returns.wr_web_page_sk - all   | statistics_tab about web_returns.wr_reason_sk - all   | statistics_tab about web_returns.wr_order_number - all   | statistics_tab about web_returns.wr_return_quantity - all   | statistics_tab about web_returns.wr_return_amt - all   | statistics_tab about web_returns.wr_return_tax - all   | statistics_tab about web_returns.wr_return_amt_inc_tax - all   | statistics_tab about web_returns.wr_fee - all   | statistics_tab about web_returns.wr_return_ship_cost - all   | statistics_tab about web_returns.wr_refunded_cash - all   | statistics_tab about web_returns.wr_reversed_charge - all   | statistics_tab about web_returns.wr_account_credit - all   | statistics_tab about web_returns.wr_net_loss - all   | statistics_tab about web_sales.ws_sold_date_sk - all   | statistics_tab about web_sales.ws_sold_time_sk - all   | statistics_tab about web_sales.ws_ship_date_sk - all   | statistics_tab about web_sales.ws_item_sk - all   | statistics_tab about web_sales.ws_bill_customer_sk - all   | statistics_tab about web_sales.ws_bill_cdemo_sk - all   | statistics_tab about web_sales.ws_bill_hdemo_sk - all   | statistics_tab about web_sales.ws_bill_addr_sk - all   | statistics_tab about web_sales.ws_ship_customer_sk - all   | statistics_tab about web_sales.ws_ship_cdemo_sk - all   | statistics_tab about web_sales.ws_ship_hdemo_sk - all   | statistics_tab about web_sales.ws_ship_addr_sk - all   | statistics_tab about web_sales.ws_web_page_sk - all   | statistics_tab about web_sales.ws_web_site_sk - all   | statistics_tab about web_sales.ws_ship_mode_sk - all   | statistics_tab about web_sales.ws_warehouse_sk - all   | statistics_tab about web_sales.ws_promo_sk - all   | statistics_tab about web_sales.ws_order_number - all   | statistics_tab about web_sales.ws_quantity - all   | statistics_tab about web_sales.ws_wholesale_cost - all   | statistics_tab about web_sales.ws_list_price - all   | statistics_tab about web_sales.ws_sales_price - all   | statistics_tab about web_sales.ws_ext_discount_amt - all   | statistics_tab about web_sales.ws_ext_sales_price - all   | statistics_tab about web_sales.ws_ext_wholesale_cost - all   | statistics_tab about web_sales.ws_ext_list_price - all   | statistics_tab about web_sales.ws_ext_tax - all   | statistics_tab about web_sales.ws_coupon_amt - all   | statistics_tab about web_sales.ws_ext_ship_cost - all   | statistics_tab about web_sales.ws_net_paid - all   | statistics_tab about web_sales.ws_net_paid_inc_tax - all   | statistics_tab about web_sales.ws_net_paid_inc_ship - all   | statistics_tab about web_sales.ws_net_paid_inc_ship_tax - all   | statistics_tab about web_sales.ws_net_profit - all   | statistics_tab about web_site.web_site_sk - all   | statistics_tab about web_site.web_site_id - all   | statistics_tab about web_site.web_rec_start_date - all   | statistics_tab about web_site.web_rec_end_date - all   | statistics_tab about web_site.web_name - all   | statistics_tab about web_site.web_open_date_sk - all   | statistics_tab about web_site.web_close_date_sk - all   | statistics_tab about web_site.web_class - all   | statistics_tab about web_site.web_manager - all   | statistics_tab about web_site.web_mkt_id - all   | statistics_tab about web_site.web_mkt_class - all   | statistics_tab about web_site.web_mkt_desc - all   | statistics_tab about web_site.web_market_manager - all   | statistics_tab about web_site.web_company_id - all   | statistics_tab about web_site.web_company_name - all   | statistics_tab about web_site.web_street_number - all   | statistics_tab about web_site.web_street_name - all   | statistics_tab about web_site.web_street_type - all   | statistics_tab about web_site.web_suite_number - all   | statistics_tab about web_site.web_city - all   | statistics_tab about web_site.web_county - all   | statistics_tab about web_site.web_state - all   | statistics_tab about web_site.web_zip - all   | statistics_tab about web_site.web_country - all   | statistics_tab about web_site.web_gmt_offset - all   | statistics_tab about web_site.web_tax_percentage - all   | complete   |
|:-----------------|-------:|:-----------------------------------------------------------|:-----------------------------------------------------------|:-----------------------------------------------------------|:---------------------------------------------------------|:-----------------------------------------------------------|:---------------------------------------------------------|:-------------------------------------------------|:--------------------------------------------------|:------------------------------------------------------|:--------------------------------------------------|:--------------------------------------------------|:----------------------------------------------------|:---------------------------------------------------|:------------------------------------------------------|:-----------------------------------------------------|:-----------------------------------------------------------|:-----------------------------------------------------|:----------------------------------------------------------|:----------------------------------------------------|:---------------------------------------------------------|:----------------------------------------------------------|:--------------------------------------------------------|:--------------------------------------------------------|:---------------------------------------------------------|:-------------------------------------------------|:---------------------------------------------------|:--------------------------------------------------|:------------------------------------------------|:----------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------------------------|:-------------------------------------------------------------|:-------------------------------------------------------------|:-----------------------------------------------------------|:---------------------------------------------------------|:--------------------------------------------------------|:------------------------------------------------------------|:-----------------------------------------------------------------|:---------------------------------------------------------|:--------------------------------------------------|:-----------------------------------------------------------------|:-----------------------------------------------------------------|:--------------------------------------------------------|:---------------------------------------------------------------------|:------------------------------------------------------------------|:------------------------------------------------------------------|:-----------------------------------------------------------------|:----------------------------------------------------------------------|:-------------------------------------------------------------------|:-------------------------------------------------------------------|:------------------------------------------------------------------|:---------------------------------------------------------------|:----------------------------------------------------------------|:-------------------------------------------------------------|:-------------------------------------------------------------|:----------------------------------------------------------|:-------------------------------------------------------------|:----------------------------------------------------------------|:--------------------------------------------------------------|:-----------------------------------------------------------|:-------------------------------------------------------------------|:----------------------------------------------------|:-----------------------------------------------------------------|:--------------------------------------------------------------|:----------------------------------------------------------------|:-------------------------------------------------------------|:---------------------------------------------------------|:-----------------------------------------------------------|:-----------------------------------------------------------|:-----------------------------------------------------------|:---------------------------------------------------------------|:------------------------------------------------------------|:------------------------------------------------------------|:-----------------------------------------------------------|:---------------------------------------------------------------|:------------------------------------------------------------|:------------------------------------------------------------|:-----------------------------------------------------------|:-------------------------------------------------------------|:--------------------------------------------------------------|:-----------------------------------------------------------|:-----------------------------------------------------------|:------------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------------|:---------------------------------------------------------|:----------------------------------------------------------|:---------------------------------------------------------------|:--------------------------------------------------------------|:-----------------------------------------------------------------|:-------------------------------------------------------------|:------------------------------------------------------|:---------------------------------------------------------|:------------------------------------------------------------|:-------------------------------------------------------|:---------------------------------------------------------------|:----------------------------------------------------------------|:--------------------------------------------------------------------|:---------------------------------------------------------|:----------------------------------------------------|:----------------------------------------------------|:---------------------------------------------------------|:---------------------------------------------------------|:--------------------------------------------------------|:-------------------------------------------------------------|:------------------------------------------------------------|:---------------------------------------------------|:---------------------------------------------------|:--------------------------------------------------|:------------------------------------------------------------|:--------------------------------------------------|:----------------------------------------------------|:---------------------------------------------------|:------------------------------------------------------|:----------------------------------------------|:------------------------------------------------------|:---------------------------------------------------------|:------------------------------------------------------------|:------------------------------------------------------------|:---------------------------------------------------------------|:-------------------------------------------------------------|:-------------------------------------------------------------|:--------------------------------------------------------------|:------------------------------------------------------|:--------------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------------------|:---------------------------------------------------------|:------------------------------------------------------------|:---------------------------------------------------------------|:--------------------------------------------------------------|:-------------------------------------------------------------|:---------------------------------------------------------------------|:-----------------------------------------------------------------------|:------------------------------------------------------------------------|:--------------------------------------------------------------------|:----------------------------------------------------------------|:-------------------------------------------------------------------------|:------------------------------------------------------------------------|:------------------------------------------------|:------------------------------------------------|:---------------------------------------------|:--------------------------------------------------|:-------------------------------------------------|:----------------------------------------------------|:---------------------------------------------|:--------------------------------------------|:--------------------------------------------|:--------------------------------------------|:--------------------------------------------|:------------------------------------------------|:-------------------------------------------------------|:----------------------------------------------------|:-------------------------------------------------|:-----------------------------------------------------|:------------------------------------------------|:------------------------------------------------|:----------------------------------------------------------|:--------------------------------------------------|:-------------------------------------------------|:----------------------------------------------------|:----------------------------------------------------|:----------------------------------------------------|:-----------------------------------------------------|:------------------------------------------------------|:--------------------------------------------------------|:-----------------------------------------------------|:------------------------------------------------------|:----------------------------------------------------------|:----------------------------------------------------------|:-----------------------------------------------------------|:---------------------------------------------------------------|:----------------------------------------------------------------------|:---------------------------------------------------------------------|:-----------------------------------------------------------------|:---------------------------------------------------------------------|:-----------------------------------------------------------|:--------------------------------------------------------|:--------------------------------------------------------|:---------------------------------------------------|:---------------------------------------------------|:--------------------------------------------------------|:------------------------------------------------------------|:--------------------------------------------|:--------------------------------------------|:---------------------------------------------------|:-------------------------------------------------|:----------------------------------------------|:--------------------------------------------------|:---------------------------------------------------|:---------------------------------------------|:------------------------------------------|:---------------------------------------------|:------------------------------------------|:------------------------------------------------|:---------------------------------------------|:------------------------------------------------|:---------------------------------------------|:-----------------------------------------|:------------------------------------------------|:------------------------------------------|:------------------------------------------|:----------------------------------------------|:-----------------------------------------------|:-------------------------------------------------|:--------------------------------------------------|:--------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------------------|:-------------------------------------------------|:----------------------------------------------|:---------------------------------------------------------|:----------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------|:---------------------------------------------------------|:----------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------|:------------------------------------------------------|:---------------------------------------------------------|:-------------------------------------------------|:---------------------------------------------------------|:------------------------------------------------|:------------------------------------------------|:--------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------------|:-----------------------------------------------|:--------------------------------------------------|:---------------------------------------------------|:----------------------------------------------|:----------------------------------------------|:----------------------------------------------------|:--------------------------------------------------|:----------------------------------------------------|:------------------------------------------------|:------------------------------------------------------|:-------------------------------------------------|:-------------------------------------------|:---------------------------------------------|:-----------------------------------------------|:-----------------------------------------------------|:-------------------------------------------------|:----------------------------------------------------|:-------------------------------------------------|:---------------------------------------------------|:------------------------------------------------|:--------------------------------------------------|:---------------------------------------------------|:-------------------------------------------------|:-------------------------------------------------|:--------------------------------------------------|:------------------------------------------|:--------------------------------------------|:-------------------------------------------|:-----------------------------------------|:---------------------------------------------|:------------------------------------------------|:----------------------------------------------------|:---------------------------------------------------------------|:-------------------------------------------------------------|:------------------------------------------------------|:----------------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------|:------------------------------------------------------|:-------------------------------------------------------|:--------------------------------------------------------|:------------------------------------------------------------|:--------------------------------------------------------------|:---------------------------------------------------------|:---------------------------------------------------------|:-----------------------------------------------------------------|:--------------------------------------------------|:---------------------------------------------------------------|:------------------------------------------------------------|:--------------------------------------------------------------|:-----------------------------------------------------------|:-------------------------------------------------------|:---------------------------------------------------------|:---------------------------------------------------------|:----------------------------------------------------|:--------------------------------------------------------|:-----------------------------------------------------|:-----------------------------------------------------|:----------------------------------------------------|:-----------------------------------------------------|:-----------------------------------------------------|:----------------------------------------------------------|:-----------------------------------------------------|:-----------------------------------------------------------|:-------------------------------------------------------|:--------------------------------------------------------|:-------------------------------------------------------------|:------------------------------------------------------------|:---------------------------------------------------------------|:-----------------------------------------------------------|:----------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------------------|:-------------------------------------------------------------|:-------------------------------------------------------|:------------------------------------------------|:------------------------------------------------|:---------------------------------------------|:---------------------------------------------|:-----------------------------------------------|:-----------------------------------------------|:----------------------------------------------|:----------------------------------------------|:--------------------------------------------------|:--------------------------------------------------|:------------------------------------------------------|:------------------------------------------------------|:--------------------------------------------------------|:---------------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------------------|:-----------------------------------------------------|:------------------------------------------------------|:----------------------------------------------|:------------------------------------------------|:-----------------------------------------------|:---------------------------------------------|:-------------------------------------------------|:----------------------------------------------------|:-----------------------------------------------------|:-----------------------------------------------------|:--------------------------------------------------------|:------------------------------------------------------|:----------------------------------------------------------|:--------------------------------------------------------|:------------------------------------------------------|:-----------------------------------------------------|:---------------------------------------------|:----------------------------------------------|:----------------------------------------------------|:----------------------------------------------------|:-----------------------------------------------------|:------------------------------------------------------|:-------------------------------------------------------------|:-------------------------------------------------------------|:----------------------------------------------------|:-----------------------------------------------------------------|:--------------------------------------------------------------|:--------------------------------------------------------------|:-------------------------------------------------------------|:------------------------------------------------------------------|:---------------------------------------------------------------|:---------------------------------------------------------------|:--------------------------------------------------------------|:--------------------------------------------------------|:------------------------------------------------------|:---------------------------------------------------------|:------------------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------|:---------------------------------------------------------------|:------------------------------------------------|:-------------------------------------------------------------|:----------------------------------------------------------|:------------------------------------------------------------|:-----------------------------------------------------------|:-----------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------|:--------------------------------------------------|:-----------------------------------------------------------|:--------------------------------------------------------|:--------------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------------------------|:--------------------------------------------------------|:--------------------------------------------------------|:-------------------------------------------------------|:------------------------------------------------------|:------------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------|:---------------------------------------------------|:-------------------------------------------------------|:---------------------------------------------------|:---------------------------------------------------------|:-----------------------------------------------------|:------------------------------------------------------|:-----------------------------------------------------------|:----------------------------------------------------------|:-------------------------------------------------------------|:---------------------------------------------------------|:--------------------------------------------------|:-----------------------------------------------------|:--------------------------------------------------------|:---------------------------------------------------|:-----------------------------------------------------------|:------------------------------------------------------------|:----------------------------------------------------------------|:-----------------------------------------------------|:--------------------------------------------------|:--------------------------------------------------|:---------------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------------|:-------------------------------------------------------|:--------------------------------------------------------|:------------------------------------------------|:--------------------------------------------------|:-------------------------------------------------|:----------------------------------------------------|:---------------------------------------------------|:---------------------------------------------------------|:-----------------------------------------------------|:-------------------------------------------------------|:--------------------------------------------------------|:------------------------------------------------------|:------------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------------|:-------------------------------------------------|:------------------------------------------------|:----------------------------------------------|:--------------------------------------------------|:-----------------------------------------------------|:---------------------------------------------------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1                                                        | 1/1                                                        | 1/1                                                        | 1/1                                                      | 1/1                                                        | 1/1                                                      | 1/1                                              | 1/1                                               | 1/1                                                   | 1/1                                               | 1/1                                               | 1/1                                                 | 1/1                                                | 1/1                                                   | 1/1                                                  | 1/1                                                        | 1/1                                                  | 1/1                                                       | 1/1                                                 | 1/1                                                      | 1/1                                                       | 1/1                                                     | 1/1                                                     | 1/1                                                      | 1/1                                              | 1/1                                                | 1/1                                               | 1/1                                             | 1/1                                                 | 1/1                                                    | 1/1                                                        | 1/1                                                          | 1/1                                                          | 1/1                                                        | 1/1                                                      | 1/1                                                     | 1/1                                                         | 1/1                                                              | 1/1                                                      | 1/1                                               | 1/1                                                              | 1/1                                                              | 1/1                                                     | 1/1                                                                  | 1/1                                                               | 1/1                                                               | 1/1                                                              | 1/1                                                                   | 1/1                                                                | 1/1                                                                | 1/1                                                               | 1/1                                                            | 1/1                                                             | 1/1                                                          | 1/1                                                          | 1/1                                                       | 1/1                                                          | 1/1                                                             | 1/1                                                           | 1/1                                                        | 1/1                                                                | 1/1                                                 | 1/1                                                              | 1/1                                                           | 1/1                                                             | 1/1                                                          | 1/1                                                      | 1/1                                                        | 1/1                                                        | 1/1                                                        | 1/1                                                            | 1/1                                                         | 1/1                                                         | 1/1                                                        | 1/1                                                            | 1/1                                                         | 1/1                                                         | 1/1                                                        | 1/1                                                          | 1/1                                                           | 1/1                                                        | 1/1                                                        | 1/1                                                   | 1/1                                                    | 1/1                                                        | 1/1                                                    | 1/1                                                          | 1/1                                                      | 1/1                                                       | 1/1                                                            | 1/1                                                           | 1/1                                                              | 1/1                                                          | 1/1                                                   | 1/1                                                      | 1/1                                                         | 1/1                                                    | 1/1                                                            | 1/1                                                             | 1/1                                                                 | 1/1                                                      | 1/1                                                 | 1/1                                                 | 1/1                                                      | 1/1                                                      | 1/1                                                     | 1/1                                                          | 1/1                                                         | 1/1                                                | 1/1                                                | 1/1                                               | 1/1                                                         | 1/1                                               | 1/1                                                 | 1/1                                                | 1/1                                                   | 1/1                                           | 1/1                                                   | 1/1                                                      | 1/1                                                         | 1/1                                                         | 1/1                                                            | 1/1                                                          | 1/1                                                          | 1/1                                                           | 1/1                                                   | 1/1                                                     | 1/1                                                    | 1/1                                                  | 1/1                                                      | 1/1                                                         | 1/1                                                            | 1/1                                                           | 1/1                                                          | 1/1                                                                  | 1/1                                                                    | 1/1                                                                     | 1/1                                                                 | 1/1                                                             | 1/1                                                                      | 1/1                                                                     | 1/1                                             | 1/1                                             | 1/1                                          | 1/1                                               | 1/1                                              | 1/1                                                 | 1/1                                          | 1/1                                         | 1/1                                         | 1/1                                         | 1/1                                         | 1/1                                             | 1/1                                                    | 1/1                                                 | 1/1                                              | 1/1                                                  | 1/1                                             | 1/1                                             | 1/1                                                       | 1/1                                               | 1/1                                              | 1/1                                                 | 1/1                                                 | 1/1                                                 | 1/1                                                  | 1/1                                                   | 1/1                                                     | 1/1                                                  | 1/1                                                   | 1/1                                                       | 1/1                                                       | 1/1                                                        | 1/1                                                            | 1/1                                                                   | 1/1                                                                  | 1/1                                                              | 1/1                                                                  | 1/1                                                        | 1/1                                                     | 1/1                                                     | 1/1                                                | 1/1                                                | 1/1                                                     | 1/1                                                         | 1/1                                         | 1/1                                         | 1/1                                                | 1/1                                              | 1/1                                           | 1/1                                               | 1/1                                                | 1/1                                          | 1/1                                       | 1/1                                          | 1/1                                       | 1/1                                             | 1/1                                          | 1/1                                             | 1/1                                          | 1/1                                      | 1/1                                             | 1/1                                       | 1/1                                       | 1/1                                           | 1/1                                            | 1/1                                              | 1/1                                               | 1/1                                               | 1/1                                                    | 1/1                                                  | 1/1                                              | 1/1                                           | 1/1                                                      | 1/1                                                 | 1/1                                                    | 1/1                                                    | 1/1                                                      | 1/1                                                 | 1/1                                                    | 1/1                                                    | 1/1                                                    | 1/1                                                   | 1/1                                                      | 1/1                                              | 1/1                                                      | 1/1                                             | 1/1                                             | 1/1                                               | 1/1                                                    | 1/1                                                    | 1/1                                            | 1/1                                            | 1/1                                               | 1/1                                                | 1/1                                           | 1/1                                           | 1/1                                                 | 1/1                                               | 1/1                                                 | 1/1                                             | 1/1                                                   | 1/1                                              | 1/1                                        | 1/1                                          | 1/1                                            | 1/1                                                  | 1/1                                              | 1/1                                                 | 1/1                                              | 1/1                                                | 1/1                                             | 1/1                                               | 1/1                                                | 1/1                                              | 1/1                                              | 1/1                                               | 1/1                                       | 1/1                                         | 1/1                                        | 1/1                                      | 1/1                                          | 1/1                                             | 1/1                                                 | 1/1                                                            | 1/1                                                          | 1/1                                                   | 1/1                                                       | 1/1                                                    | 1/1                                                    | 1/1                                                   | 1/1                                                    | 1/1                                                     | 1/1                                                         | 1/1                                                           | 1/1                                                      | 1/1                                                      | 1/1                                                              | 1/1                                               | 1/1                                                            | 1/1                                                         | 1/1                                                           | 1/1                                                        | 1/1                                                    | 1/1                                                      | 1/1                                                      | 1/1                                                 | 1/1                                                     | 1/1                                                  | 1/1                                                  | 1/1                                                 | 1/1                                                  | 1/1                                                  | 1/1                                                       | 1/1                                                  | 1/1                                                        | 1/1                                                    | 1/1                                                     | 1/1                                                          | 1/1                                                         | 1/1                                                            | 1/1                                                        | 1/1                                                 | 1/1                                                    | 1/1                                                  | 1/1                                                          | 1/1                                                    | 1/1                                             | 1/1                                             | 1/1                                          | 1/1                                          | 1/1                                            | 1/1                                            | 1/1                                           | 1/1                                           | 1/1                                               | 1/1                                               | 1/1                                                   | 1/1                                                   | 1/1                                                     | 1/1                                                      | 1/1                                                    | 1/1                                                  | 1/1                                                  | 1/1                                                   | 1/1                                           | 1/1                                             | 1/1                                            | 1/1                                          | 1/1                                              | 1/1                                                 | 1/1                                                  | 1/1                                                  | 1/1                                                     | 1/1                                                   | 1/1                                                       | 1/1                                                     | 1/1                                                   | 1/1                                                  | 1/1                                          | 1/1                                           | 1/1                                                 | 1/1                                                 | 1/1                                                  | 1/1                                                   | 1/1                                                          | 1/1                                                          | 1/1                                                 | 1/1                                                              | 1/1                                                           | 1/1                                                           | 1/1                                                          | 1/1                                                               | 1/1                                                            | 1/1                                                            | 1/1                                                           | 1/1                                                     | 1/1                                                   | 1/1                                                      | 1/1                                                         | 1/1                                                    | 1/1                                                    | 1/1                                                            | 1/1                                             | 1/1                                                          | 1/1                                                       | 1/1                                                         | 1/1                                                        | 1/1                                                  | 1/1                                                    | 1/1                                                    | 1/1                                                    | 1/1                                               | 1/1                                                        | 1/1                                                     | 1/1                                                     | 1/1                                                    | 1/1                                                        | 1/1                                                     | 1/1                                                     | 1/1                                                    | 1/1                                                   | 1/1                                                   | 1/1                                                    | 1/1                                                    | 1/1                                                | 1/1                                                    | 1/1                                                | 1/1                                                      | 1/1                                                  | 1/1                                                   | 1/1                                                        | 1/1                                                       | 1/1                                                          | 1/1                                                      | 1/1                                               | 1/1                                                  | 1/1                                                     | 1/1                                                | 1/1                                                        | 1/1                                                         | 1/1                                                             | 1/1                                                  | 1/1                                               | 1/1                                               | 1/1                                                      | 1/1                                                    | 1/1                                            | 1/1                                                    | 1/1                                                     | 1/1                                             | 1/1                                               | 1/1                                              | 1/1                                                 | 1/1                                                | 1/1                                                      | 1/1                                                  | 1/1                                                    | 1/1                                                     | 1/1                                                   | 1/1                                                   | 1/1                                                    | 1/1                                            | 1/1                                              | 1/1                                             | 1/1                                           | 1/1                                               | 1/1                                                  | 1/1                                                      | yes        |
| postgresql-1-1-2 |      1 | 1/1                                                        | 1/1                                                        | 1/1                                                        | 1/1                                                      | 1/1                                                        | 1/1                                                      | 1/1                                              | 1/1                                               | 1/1                                                   | 1/1                                               | 1/1                                               | 1/1                                                 | 1/1                                                | 1/1                                                   | 1/1                                                  | 1/1                                                        | 1/1                                                  | 1/1                                                       | 1/1                                                 | 1/1                                                      | 1/1                                                       | 1/1                                                     | 1/1                                                     | 1/1                                                      | 1/1                                              | 1/1                                                | 1/1                                               | 1/1                                             | 1/1                                                 | 1/1                                                    | 1/1                                                        | 1/1                                                          | 1/1                                                          | 1/1                                                        | 1/1                                                      | 1/1                                                     | 1/1                                                         | 1/1                                                              | 1/1                                                      | 1/1                                               | 1/1                                                              | 1/1                                                              | 1/1                                                     | 1/1                                                                  | 1/1                                                               | 1/1                                                               | 1/1                                                              | 1/1                                                                   | 1/1                                                                | 1/1                                                                | 1/1                                                               | 1/1                                                            | 1/1                                                             | 1/1                                                          | 1/1                                                          | 1/1                                                       | 1/1                                                          | 1/1                                                             | 1/1                                                           | 1/1                                                        | 1/1                                                                | 1/1                                                 | 1/1                                                              | 1/1                                                           | 1/1                                                             | 1/1                                                          | 1/1                                                      | 1/1                                                        | 1/1                                                        | 1/1                                                        | 1/1                                                            | 1/1                                                         | 1/1                                                         | 1/1                                                        | 1/1                                                            | 1/1                                                         | 1/1                                                         | 1/1                                                        | 1/1                                                          | 1/1                                                           | 1/1                                                        | 1/1                                                        | 1/1                                                   | 1/1                                                    | 1/1                                                        | 1/1                                                    | 1/1                                                          | 1/1                                                      | 1/1                                                       | 1/1                                                            | 1/1                                                           | 1/1                                                              | 1/1                                                          | 1/1                                                   | 1/1                                                      | 1/1                                                         | 1/1                                                    | 1/1                                                            | 1/1                                                             | 1/1                                                                 | 1/1                                                      | 1/1                                                 | 1/1                                                 | 1/1                                                      | 1/1                                                      | 1/1                                                     | 1/1                                                          | 1/1                                                         | 1/1                                                | 1/1                                                | 1/1                                               | 1/1                                                         | 1/1                                               | 1/1                                                 | 1/1                                                | 1/1                                                   | 1/1                                           | 1/1                                                   | 1/1                                                      | 1/1                                                         | 1/1                                                         | 1/1                                                            | 1/1                                                          | 1/1                                                          | 1/1                                                           | 1/1                                                   | 1/1                                                     | 1/1                                                    | 1/1                                                  | 1/1                                                      | 1/1                                                         | 1/1                                                            | 1/1                                                           | 1/1                                                          | 1/1                                                                  | 1/1                                                                    | 1/1                                                                     | 1/1                                                                 | 1/1                                                             | 1/1                                                                      | 1/1                                                                     | 1/1                                             | 1/1                                             | 1/1                                          | 1/1                                               | 1/1                                              | 1/1                                                 | 1/1                                          | 1/1                                         | 1/1                                         | 1/1                                         | 1/1                                         | 1/1                                             | 1/1                                                    | 1/1                                                 | 1/1                                              | 1/1                                                  | 1/1                                             | 1/1                                             | 1/1                                                       | 1/1                                               | 1/1                                              | 1/1                                                 | 1/1                                                 | 1/1                                                 | 1/1                                                  | 1/1                                                   | 1/1                                                     | 1/1                                                  | 1/1                                                   | 1/1                                                       | 1/1                                                       | 1/1                                                        | 1/1                                                            | 1/1                                                                   | 1/1                                                                  | 1/1                                                              | 1/1                                                                  | 1/1                                                        | 1/1                                                     | 1/1                                                     | 1/1                                                | 1/1                                                | 1/1                                                     | 1/1                                                         | 1/1                                         | 1/1                                         | 1/1                                                | 1/1                                              | 1/1                                           | 1/1                                               | 1/1                                                | 1/1                                          | 1/1                                       | 1/1                                          | 1/1                                       | 1/1                                             | 1/1                                          | 1/1                                             | 1/1                                          | 1/1                                      | 1/1                                             | 1/1                                       | 1/1                                       | 1/1                                           | 1/1                                            | 1/1                                              | 1/1                                               | 1/1                                               | 1/1                                                    | 1/1                                                  | 1/1                                              | 1/1                                           | 1/1                                                      | 1/1                                                 | 1/1                                                    | 1/1                                                    | 1/1                                                      | 1/1                                                 | 1/1                                                    | 1/1                                                    | 1/1                                                    | 1/1                                                   | 1/1                                                      | 1/1                                              | 1/1                                                      | 1/1                                             | 1/1                                             | 1/1                                               | 1/1                                                    | 1/1                                                    | 1/1                                            | 1/1                                            | 1/1                                               | 1/1                                                | 1/1                                           | 1/1                                           | 1/1                                                 | 1/1                                               | 1/1                                                 | 1/1                                             | 1/1                                                   | 1/1                                              | 1/1                                        | 1/1                                          | 1/1                                            | 1/1                                                  | 1/1                                              | 1/1                                                 | 1/1                                              | 1/1                                                | 1/1                                             | 1/1                                               | 1/1                                                | 1/1                                              | 1/1                                              | 1/1                                               | 1/1                                       | 1/1                                         | 1/1                                        | 1/1                                      | 1/1                                          | 1/1                                             | 1/1                                                 | 1/1                                                            | 1/1                                                          | 1/1                                                   | 1/1                                                       | 1/1                                                    | 1/1                                                    | 1/1                                                   | 1/1                                                    | 1/1                                                     | 1/1                                                         | 1/1                                                           | 1/1                                                      | 1/1                                                      | 1/1                                                              | 1/1                                               | 1/1                                                            | 1/1                                                         | 1/1                                                           | 1/1                                                        | 1/1                                                    | 1/1                                                      | 1/1                                                      | 1/1                                                 | 1/1                                                     | 1/1                                                  | 1/1                                                  | 1/1                                                 | 1/1                                                  | 1/1                                                  | 1/1                                                       | 1/1                                                  | 1/1                                                        | 1/1                                                    | 1/1                                                     | 1/1                                                          | 1/1                                                         | 1/1                                                            | 1/1                                                        | 1/1                                                 | 1/1                                                    | 1/1                                                  | 1/1                                                          | 1/1                                                    | 1/1                                             | 1/1                                             | 1/1                                          | 1/1                                          | 1/1                                            | 1/1                                            | 1/1                                           | 1/1                                           | 1/1                                               | 1/1                                               | 1/1                                                   | 1/1                                                   | 1/1                                                     | 1/1                                                      | 1/1                                                    | 1/1                                                  | 1/1                                                  | 1/1                                                   | 1/1                                           | 1/1                                             | 1/1                                            | 1/1                                          | 1/1                                              | 1/1                                                 | 1/1                                                  | 1/1                                                  | 1/1                                                     | 1/1                                                   | 1/1                                                       | 1/1                                                     | 1/1                                                   | 1/1                                                  | 1/1                                          | 1/1                                           | 1/1                                                 | 1/1                                                 | 1/1                                                  | 1/1                                                   | 1/1                                                          | 1/1                                                          | 1/1                                                 | 1/1                                                              | 1/1                                                           | 1/1                                                           | 1/1                                                          | 1/1                                                               | 1/1                                                            | 1/1                                                            | 1/1                                                           | 1/1                                                     | 1/1                                                   | 1/1                                                      | 1/1                                                         | 1/1                                                    | 1/1                                                    | 1/1                                                            | 1/1                                             | 1/1                                                          | 1/1                                                       | 1/1                                                         | 1/1                                                        | 1/1                                                  | 1/1                                                    | 1/1                                                    | 1/1                                                    | 1/1                                               | 1/1                                                        | 1/1                                                     | 1/1                                                     | 1/1                                                    | 1/1                                                        | 1/1                                                     | 1/1                                                     | 1/1                                                    | 1/1                                                   | 1/1                                                   | 1/1                                                    | 1/1                                                    | 1/1                                                | 1/1                                                    | 1/1                                                | 1/1                                                      | 1/1                                                  | 1/1                                                   | 1/1                                                        | 1/1                                                       | 1/1                                                          | 1/1                                                      | 1/1                                               | 1/1                                                  | 1/1                                                     | 1/1                                                | 1/1                                                        | 1/1                                                         | 1/1                                                             | 1/1                                                  | 1/1                                               | 1/1                                               | 1/1                                                      | 1/1                                                    | 1/1                                            | 1/1                                                    | 1/1                                                     | 1/1                                             | 1/1                                               | 1/1                                              | 1/1                                                 | 1/1                                                | 1/1                                                      | 1/1                                                  | 1/1                                                    | 1/1                                                     | 1/1                                                   | 1/1                                                   | 1/1                                                    | 1/1                                            | 1/1                                              | 1/1                                             | 1/1                                           | 1/1                                               | 1/1                                                  | 1/1                                                      | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                                                |   postgresql-1-1-1-1-1 |   postgresql-1-1-2-1-1 |
|:-----------------------------------------------------------------------|-----------------------:|-----------------------:|
| statistics_tab about call_center.cc_call_center_sk - all               |                 215.63 |                 244.64 |
| statistics_tab about call_center.cc_call_center_id - all               |                   2.96 |                   1.80 |
| statistics_tab about call_center.cc_rec_start_date - all               |                   1.93 |                   1.68 |
| statistics_tab about call_center.cc_rec_end_date - all                 |                   2.00 |                   1.28 |
| statistics_tab about call_center.cc_closed_date_sk - all               |                   1.27 |                   1.10 |
| statistics_tab about call_center.cc_open_date_sk - all                 |                   1.71 |                   1.20 |
| statistics_tab about call_center.cc_name - all                         |                   1.44 |                   1.50 |
| statistics_tab about call_center.cc_class - all                        |                   4.01 |                   1.33 |
| statistics_tab about call_center.cc_employees - all                    |                   1.14 |                   1.26 |
| statistics_tab about call_center.cc_sq_ft - all                        |                   1.05 |                   1.18 |
| statistics_tab about call_center.cc_hours - all                        |                   1.61 |                   1.49 |
| statistics_tab about call_center.cc_manager - all                      |                   1.34 |                   1.29 |
| statistics_tab about call_center.cc_mkt_id - all                       |                   1.80 |                   1.31 |
| statistics_tab about call_center.cc_mkt_class - all                    |                   1.52 |                   1.41 |
| statistics_tab about call_center.cc_mkt_desc - all                     |                   1.81 |                   1.37 |
| statistics_tab about call_center.cc_market_manager - all               |                   1.57 |                   1.32 |
| statistics_tab about call_center.cc_division - all                     |                   1.33 |                   1.09 |
| statistics_tab about call_center.cc_division_name - all                |                   1.44 |                   1.20 |
| statistics_tab about call_center.cc_company - all                      |                   1.35 |                   1.31 |
| statistics_tab about call_center.cc_company_name - all                 |                   1.80 |                   2.34 |
| statistics_tab about call_center.cc_street_number - all                |                   1.27 |                   1.73 |
| statistics_tab about call_center.cc_street_name - all                  |                   1.25 |                   1.76 |
| statistics_tab about call_center.cc_street_type - all                  |                   1.34 |                   1.84 |
| statistics_tab about call_center.cc_suite_number - all                 |                   1.04 |                   1.74 |
| statistics_tab about call_center.cc_city - all                         |                   1.10 |                   1.71 |
| statistics_tab about call_center.cc_county - all                       |                   1.26 |                   1.71 |
| statistics_tab about call_center.cc_state - all                        |                   1.11 |                   1.52 |
| statistics_tab about call_center.cc_zip - all                          |                   1.01 |                   1.63 |
| statistics_tab about call_center.cc_country - all                      |                   1.25 |                   1.28 |
| statistics_tab about call_center.cc_gmt_offset - all                   |                   1.35 |                   1.45 |
| statistics_tab about call_center.cc_tax_percentage - all               |                   1.24 |                   1.25 |
| statistics_tab about catalog_page.cp_catalog_page_sk - all             |                   5.57 |                   5.38 |
| statistics_tab about catalog_page.cp_catalog_page_id - all             |                  13.59 |                  13.57 |
| statistics_tab about catalog_page.cp_start_date_sk - all               |                   3.22 |                   2.86 |
| statistics_tab about catalog_page.cp_end_date_sk - all                 |                   3.61 |                   2.79 |
| statistics_tab about catalog_page.cp_department - all                  |                   5.34 |                   3.88 |
| statistics_tab about catalog_page.cp_catalog_number - all              |                   7.10 |                   2.90 |
| statistics_tab about catalog_page.cp_catalog_page_number - all         |                  10.67 |                   2.94 |
| statistics_tab about catalog_page.cp_description - all                 |                  34.53 |                  13.05 |
| statistics_tab about catalog_page.cp_type - all                        |                  10.84 |                   4.00 |
| statistics_tab about catalog_returns.cr_returned_date_sk - all         |                1158.58 |                 655.24 |
| statistics_tab about catalog_returns.cr_returned_time_sk - all         |                 310.91 |                 306.82 |
| statistics_tab about catalog_returns.cr_item_sk - all                  |                 935.02 |                 764.96 |
| statistics_tab about catalog_returns.cr_refunded_customer_sk - all     |                 713.36 |                 321.15 |
| statistics_tab about catalog_returns.cr_refunded_cdemo_sk - all        |                 333.13 |                 683.52 |
| statistics_tab about catalog_returns.cr_refunded_hdemo_sk - all        |                 270.09 |                 587.56 |
| statistics_tab about catalog_returns.cr_refunded_addr_sk - all         |                 306.98 |                 299.39 |
| statistics_tab about catalog_returns.cr_returning_customer_sk - all    |                 804.56 |                 756.60 |
| statistics_tab about catalog_returns.cr_returning_cdemo_sk - all       |                 323.88 |                 325.20 |
| statistics_tab about catalog_returns.cr_returning_hdemo_sk - all       |                 266.86 |                 274.62 |
| statistics_tab about catalog_returns.cr_returning_addr_sk - all        |                 303.92 |                 307.28 |
| statistics_tab about catalog_returns.cr_call_center_sk - all           |                 253.39 |                 256.05 |
| statistics_tab about catalog_returns.cr_catalog_page_sk - all          |                 259.67 |                 254.46 |
| statistics_tab about catalog_returns.cr_ship_mode_sk - all             |                 619.08 |                 584.11 |
| statistics_tab about catalog_returns.cr_warehouse_sk - all             |                 918.35 |                 857.98 |
| statistics_tab about catalog_returns.cr_reason_sk - all                |                 655.20 |                 267.54 |
| statistics_tab about catalog_returns.cr_order_number - all             |                 446.29 |                 298.93 |
| statistics_tab about catalog_returns.cr_return_quantity - all          |                 289.60 |                 267.52 |
| statistics_tab about catalog_returns.cr_return_amount - all            |                 540.53 |                 476.51 |
| statistics_tab about catalog_returns.cr_return_tax - all               |                 453.38 |                 431.97 |
| statistics_tab about catalog_returns.cr_return_amt_inc_tax - all       |                 505.43 |                 505.93 |
| statistics_tab about catalog_returns.cr_fee - all                      |                 550.46 |                 459.13 |
| statistics_tab about catalog_returns.cr_return_ship_cost - all         |                 953.73 |                 484.97 |
| statistics_tab about catalog_returns.cr_refunded_cash - all            |                1069.69 |                 490.84 |
| statistics_tab about catalog_returns.cr_reversed_charge - all          |                 548.91 |                 472.83 |
| statistics_tab about catalog_returns.cr_store_credit - all             |                 499.51 |                 527.62 |
| statistics_tab about catalog_returns.cr_net_loss - all                 |                 546.10 |                 686.81 |
| statistics_tab about catalog_sales.cs_sold_date_sk - all               |                3860.60 |                3466.72 |
| statistics_tab about catalog_sales.cs_sold_time_sk - all               |                2477.23 |                2279.53 |
| statistics_tab about catalog_sales.cs_ship_date_sk - all               |                2883.49 |                3361.46 |
| statistics_tab about catalog_sales.cs_bill_customer_sk - all           |                5908.23 |                4423.11 |
| statistics_tab about catalog_sales.cs_bill_cdemo_sk - all              |                2603.63 |                2506.30 |
| statistics_tab about catalog_sales.cs_bill_hdemo_sk - all              |                2470.17 |                2942.57 |
| statistics_tab about catalog_sales.cs_bill_addr_sk - all               |                2581.96 |                3016.11 |
| statistics_tab about catalog_sales.cs_ship_customer_sk - all           |                5508.88 |                4591.09 |
| statistics_tab about catalog_sales.cs_ship_cdemo_sk - all              |                3137.67 |                2464.24 |
| statistics_tab about catalog_sales.cs_ship_hdemo_sk - all              |                2285.49 |                2212.09 |
| statistics_tab about catalog_sales.cs_ship_addr_sk - all               |                5208.33 |                5098.33 |
| statistics_tab about catalog_sales.cs_call_center_sk - all             |                4928.56 |                4748.82 |
| statistics_tab about catalog_sales.cs_catalog_page_sk - all            |                2509.75 |                2795.73 |
| statistics_tab about catalog_sales.cs_ship_mode_sk - all               |                2520.28 |                3125.28 |
| statistics_tab about catalog_sales.cs_warehouse_sk - all               |                6623.98 |                6688.65 |
| statistics_tab about catalog_sales.cs_item_sk - all                    |               12634.79 |               13142.99 |
| statistics_tab about catalog_sales.cs_promo_sk - all                   |               11389.05 |               10240.78 |
| statistics_tab about catalog_sales.cs_order_number - all               |                4739.82 |                5028.99 |
| statistics_tab about catalog_sales.cs_quantity - all                   |                2596.45 |                3943.51 |
| statistics_tab about catalog_sales.cs_wholesale_cost - all             |                4351.81 |                6627.52 |
| statistics_tab about catalog_sales.cs_list_price - all                 |                5135.21 |                4778.87 |
| statistics_tab about catalog_sales.cs_sales_price - all                |                4467.74 |                5549.97 |
| statistics_tab about catalog_sales.cs_ext_discount_amt - all           |                5175.18 |                7024.13 |
| statistics_tab about catalog_sales.cs_ext_sales_price - all            |                5356.06 |                6907.70 |
| statistics_tab about catalog_sales.cs_ext_wholesale_cost - all         |                5090.93 |                8121.71 |
| statistics_tab about catalog_sales.cs_ext_list_price - all             |                5782.12 |                7409.16 |
| statistics_tab about catalog_sales.cs_ext_tax - all                    |                4696.86 |                6218.69 |
| statistics_tab about catalog_sales.cs_coupon_amt - all                 |                4306.68 |                5272.95 |
| statistics_tab about catalog_sales.cs_ext_ship_cost - all              |                4978.56 |                4921.72 |
| statistics_tab about catalog_sales.cs_net_paid - all                   |                5006.91 |                5717.21 |
| statistics_tab about catalog_sales.cs_net_paid_inc_tax - all           |                5438.08 |                5873.89 |
| statistics_tab about catalog_sales.cs_net_paid_inc_ship - all          |                5765.70 |                5817.55 |
| statistics_tab about catalog_sales.cs_net_paid_inc_ship_tax - all      |               13918.53 |                6492.09 |
| statistics_tab about catalog_sales.cs_net_profit - all                 |               18342.61 |                5863.28 |
| statistics_tab about customer.c_customer_sk - all                      |                 350.57 |                 131.90 |
| statistics_tab about customer.c_customer_id - all                      |                1127.55 |                 724.96 |
| statistics_tab about customer.c_current_cdemo_sk - all                 |                 275.79 |                 287.05 |
| statistics_tab about customer.c_current_hdemo_sk - all                 |                 115.64 |                 112.24 |
| statistics_tab about customer.c_current_addr_sk - all                  |                 267.44 |                 259.04 |
| statistics_tab about customer.c_first_shipto_date_sk - all             |                 104.12 |                 104.64 |
| statistics_tab about customer.c_first_sales_date_sk - all              |                 104.97 |                 105.25 |
| statistics_tab about customer.c_salutation - all                       |                 137.41 |                 132.56 |
| statistics_tab about customer.c_first_name - all                       |                 204.03 |                 186.25 |
| statistics_tab about customer.c_last_name - all                        |                 408.27 |                 210.91 |
| statistics_tab about customer.c_preferred_cust_flag - all              |                 131.06 |                 123.81 |
| statistics_tab about customer.c_birth_day - all                        |                 105.50 |                  96.80 |
| statistics_tab about customer.c_birth_month - all                      |                 106.70 |                 121.95 |
| statistics_tab about customer.c_birth_year - all                       |                 108.19 |                 110.54 |
| statistics_tab about customer.c_birth_country - all                    |                 270.59 |                 318.20 |
| statistics_tab about customer.c_login - all                            |                 107.01 |                 104.24 |
| statistics_tab about customer.c_email_address - all                    |                 743.62 |                1003.83 |
| statistics_tab about customer.c_last_review_date - all                 |                 187.96 |                 422.95 |
| statistics_tab about customer_address.ca_address_sk - all              |                  97.10 |                 145.90 |
| statistics_tab about customer_address.ca_address_id - all              |                 301.45 |                 430.64 |
| statistics_tab about customer_address.ca_street_number - all           |                  86.43 |                 107.59 |
| statistics_tab about customer_address.ca_street_name - all             |                  89.93 |                  94.80 |
| statistics_tab about customer_address.ca_street_type - all             |                  83.70 |                  92.93 |
| statistics_tab about customer_address.ca_suite_number - all            |                  84.91 |                  91.31 |
| statistics_tab about customer_address.ca_city - all                    |                  81.87 |                  81.23 |
| statistics_tab about customer_address.ca_county - all                  |                 133.87 |                 133.94 |
| statistics_tab about customer_address.ca_state - all                   |                  76.61 |                  77.33 |
| statistics_tab about customer_address.ca_zip - all                     |                 242.32 |                  87.65 |
| statistics_tab about customer_address.ca_country - all                 |                 144.06 |                  82.64 |
| statistics_tab about customer_address.ca_gmt_offset - all              |                  63.53 |                  66.34 |
| statistics_tab about customer_address.ca_location_type - all           |                  87.23 |                  81.68 |
| statistics_tab about customer_demographics.cd_demo_sk - all            |                 438.99 |                 498.74 |
| statistics_tab about customer_demographics.cd_gender - all             |                 325.93 |                 353.85 |
| statistics_tab about customer_demographics.cd_marital_status - all     |                 345.94 |                 340.55 |
| statistics_tab about customer_demographics.cd_education_status - all   |                 760.32 |                 425.25 |
| statistics_tab about customer_demographics.cd_purchase_estimate - all  |                 554.16 |                 312.34 |
| statistics_tab about customer_demographics.cd_credit_rating - all      |                 412.25 |                 407.16 |
| statistics_tab about customer_demographics.cd_dep_count - all          |                 318.93 |                 318.40 |
| statistics_tab about customer_demographics.cd_dep_employed_count - all |                 301.07 |                 339.93 |
| statistics_tab about customer_demographics.cd_dep_college_count - all  |                 317.98 |                 324.37 |
| statistics_tab about date_dim.d_date_sk - all                          |                  19.72 |                  27.02 |
| statistics_tab about date_dim.d_date_id - all                          |                 199.36 |                  75.64 |
| statistics_tab about date_dim.d_date - all                             |                  50.49 |                  51.26 |
| statistics_tab about date_dim.d_month_seq - all                        |                  13.17 |                  10.15 |
| statistics_tab about date_dim.d_week_seq - all                         |                  13.08 |                  10.89 |
| statistics_tab about date_dim.d_quarter_seq - all                      |                  13.29 |                  12.95 |
| statistics_tab about date_dim.d_year - all                             |                  15.90 |                  14.21 |
| statistics_tab about date_dim.d_dow - all                              |                  13.16 |                  11.05 |
| statistics_tab about date_dim.d_moy - all                              |                  13.75 |                  11.09 |
| statistics_tab about date_dim.d_dom - all                              |                  42.09 |                  11.73 |
| statistics_tab about date_dim.d_qoy - all                              |                  14.58 |                  10.96 |
| statistics_tab about date_dim.d_fy_year - all                          |                  16.95 |                  11.09 |
| statistics_tab about date_dim.d_fy_quarter_seq - all                   |                  13.87 |                  11.51 |
| statistics_tab about date_dim.d_fy_week_seq - all                      |                  14.29 |                  11.04 |
| statistics_tab about date_dim.d_day_name - all                         |                  23.18 |                  19.04 |
| statistics_tab about date_dim.d_quarter_name - all                     |                  22.36 |                  18.08 |
| statistics_tab about date_dim.d_holiday - all                          |                  22.80 |                  18.52 |
| statistics_tab about date_dim.d_weekend - all                          |                  22.11 |                  18.10 |
| statistics_tab about date_dim.d_following_holiday - all                |                  70.57 |                  19.68 |
| statistics_tab about date_dim.d_first_dom - all                        |                  24.43 |                  12.45 |
| statistics_tab about date_dim.d_last_dom - all                         |                  16.52 |                  16.00 |
| statistics_tab about date_dim.d_same_day_ly - all                      |                  15.16 |                  12.67 |
| statistics_tab about date_dim.d_same_day_lq - all                      |                  16.96 |                  13.73 |
| statistics_tab about date_dim.d_current_day - all                      |                  25.08 |                  20.61 |
| statistics_tab about date_dim.d_current_week - all                     |                  24.89 |                  20.12 |
| statistics_tab about date_dim.d_current_month - all                    |                  29.89 |                  21.73 |
| statistics_tab about date_dim.d_current_quarter - all                  |                  28.50 |                  21.50 |
| statistics_tab about date_dim.d_current_year - all                     |                  26.03 |                  21.77 |
| statistics_tab about dbgen_version.dv_version - all                    |                   2.15 |                   1.43 |
| statistics_tab about dbgen_version.dv_create_date - all                |                   2.29 |                   1.35 |
| statistics_tab about dbgen_version.dv_create_time - all                |                   1.87 |                   1.65 |
| statistics_tab about dbgen_version.dv_cmdline_args - all               |                   1.73 |                   1.17 |
| statistics_tab about household_demographics.hd_demo_sk - all           |                   3.06 |                   2.67 |
| statistics_tab about household_demographics.hd_income_band_sk - all    |                   2.66 |                   2.14 |
| statistics_tab about household_demographics.hd_buy_potential - all     |                   6.19 |                   3.15 |
| statistics_tab about household_demographics.hd_dep_count - all         |                   2.82 |                   1.90 |
| statistics_tab about household_demographics.hd_vehicle_count - all     |                   2.71 |                   2.52 |
| statistics_tab about income_band.ib_income_band_sk - all               |                   2.01 |                   1.07 |
| statistics_tab about income_band.ib_lower_bound - all                  |                   1.71 |                   0.97 |
| statistics_tab about income_band.ib_upper_bound - all                  |                   0.90 |                   1.09 |
| statistics_tab about inventory.inv_date_sk - all                       |               24839.93 |               24626.20 |
| statistics_tab about inventory.inv_item_sk - all                       |               64165.96 |               66008.77 |
| statistics_tab about inventory.inv_warehouse_sk - all                  |               24023.17 |               22230.32 |
| statistics_tab about inventory.inv_quantity_on_hand - all              |               24886.72 |               25582.49 |
| statistics_tab about item.i_item_sk - all                              |                  43.16 |                  41.76 |
| statistics_tab about item.i_item_id - all                              |                  88.56 |                  85.02 |
| statistics_tab about item.i_rec_start_date - all                       |                  34.50 |                  31.54 |
| statistics_tab about item.i_rec_end_date - all                         |                  29.80 |                  29.57 |
| statistics_tab about item.i_item_desc - all                            |                 124.52 |                 122.87 |
| statistics_tab about item.i_current_price - all                        |                  34.73 |                  38.29 |
| statistics_tab about item.i_wholesale_cost - all                       |                  32.88 |                  44.27 |
| statistics_tab about item.i_brand_id - all                             |                  22.50 |                  24.72 |
| statistics_tab about item.i_brand - all                                |                  81.41 |                  81.45 |
| statistics_tab about item.i_class_id - all                             |                  20.56 |                  21.33 |
| statistics_tab about item.i_class - all                                |                  56.33 |                  54.49 |
| statistics_tab about item.i_category_id - all                          |                  21.29 |                  28.83 |
| statistics_tab about item.i_category - all                             |                  50.12 |                  57.20 |
| statistics_tab about item.i_manufact_id - all                          |                  25.30 |                  24.20 |
| statistics_tab about item.i_manufact - all                             |                  78.85 |                  64.43 |
| statistics_tab about item.i_size - all                                 |                  51.45 |                  45.64 |
| statistics_tab about item.i_formulation - all                          |                  94.31 |                 103.42 |
| statistics_tab about item.i_color - all                                |                  48.16 |                  58.66 |
| statistics_tab about item.i_units - all                                |                  46.02 |                  47.33 |
| statistics_tab about item.i_container - all                            |                  40.80 |                  38.51 |
| statistics_tab about item.i_manager_id - all                           |                  24.32 |                  24.13 |
| statistics_tab about item.i_product_name - all                         |                 239.54 |                 190.16 |
| statistics_tab about promotion.p_promo_sk - all                        |                   2.98 |                   1.56 |
| statistics_tab about promotion.p_promo_id - all                        |                   1.81 |                   1.70 |
| statistics_tab about promotion.p_start_date_sk - all                   |                   1.13 |                   1.78 |
| statistics_tab about promotion.p_end_date_sk - all                     |                   1.22 |                   1.12 |
| statistics_tab about promotion.p_item_sk - all                         |                   1.15 |                   1.50 |
| statistics_tab about promotion.p_cost - all                            |                   1.07 |                   1.06 |
| statistics_tab about promotion.p_response_target - all                 |                   1.21 |                   1.32 |
| statistics_tab about promotion.p_promo_name - all                      |                   1.60 |                   1.20 |
| statistics_tab about promotion.p_channel_dmail - all                   |                   1.38 |                   1.25 |
| statistics_tab about promotion.p_channel_email - all                   |                   1.32 |                   1.11 |
| statistics_tab about promotion.p_channel_catalog - all                 |                   1.28 |                   1.33 |
| statistics_tab about promotion.p_channel_tv - all                      |                   1.46 |                   1.31 |
| statistics_tab about promotion.p_channel_radio - all                   |                   1.39 |                   1.43 |
| statistics_tab about promotion.p_channel_press - all                   |                   1.17 |                   1.58 |
| statistics_tab about promotion.p_channel_event - all                   |                   1.37 |                   1.53 |
| statistics_tab about promotion.p_channel_demo - all                    |                   1.40 |                   1.99 |
| statistics_tab about promotion.p_channel_details - all                 |                   1.51 |                   1.73 |
| statistics_tab about promotion.p_purpose - all                         |                   1.63 |                   1.89 |
| statistics_tab about promotion.p_discount_active - all                 |                   1.30 |                   1.71 |
| statistics_tab about reason.r_reason_sk - all                          |                   1.04 |                   1.17 |
| statistics_tab about reason.r_reason_id - all                          |                   1.15 |                   1.07 |
| statistics_tab about reason.r_reason_desc - all                        |                   1.15 |                   1.32 |
| statistics_tab about ship_mode.sm_ship_mode_sk - all                   |                   1.07 |                   1.12 |
| statistics_tab about ship_mode.sm_ship_mode_id - all                   |                   1.02 |                   1.26 |
| statistics_tab about ship_mode.sm_type - all                           |                   1.37 |                   1.15 |
| statistics_tab about ship_mode.sm_code - all                           |                   1.15 |                   1.17 |
| statistics_tab about ship_mode.sm_carrier - all                        |                   1.14 |                   1.28 |
| statistics_tab about ship_mode.sm_contract - all                       |                   1.17 |                   1.11 |
| statistics_tab about store.s_store_sk - all                            |                   1.45 |                   1.29 |
| statistics_tab about store.s_store_id - all                            |                   1.40 |                   1.34 |
| statistics_tab about store.s_rec_start_date - all                      |                   1.43 |                   1.30 |
| statistics_tab about store.s_rec_end_date - all                        |                   1.40 |                   1.47 |
| statistics_tab about store.s_closed_date_sk - all                      |                   1.09 |                   1.30 |
| statistics_tab about store.s_store_name - all                          |                   1.37 |                   1.55 |
| statistics_tab about store.s_number_employees - all                    |                   1.16 |                   1.24 |
| statistics_tab about store.s_floor_space - all                         |                   1.31 |                   1.37 |
| statistics_tab about store.s_hours - all                               |                   1.59 |                   1.64 |
| statistics_tab about store.s_manager - all                             |                   1.59 |                   1.30 |
| statistics_tab about store.s_market_id - all                           |                   1.39 |                   1.10 |
| statistics_tab about store.s_geography_class - all                     |                   1.24 |                   1.63 |
| statistics_tab about store.s_market_desc - all                         |                   1.48 |                   3.29 |
| statistics_tab about store.s_market_manager - all                      |                   1.84 |                   1.84 |
| statistics_tab about store.s_division_id - all                         |                   1.52 |                   1.21 |
| statistics_tab about store.s_division_name - all                       |                   1.80 |                   1.43 |
| statistics_tab about store.s_company_id - all                          |                   1.20 |                   1.53 |
| statistics_tab about store.s_company_name - all                        |                   1.57 |                   1.62 |
| statistics_tab about store.s_street_number - all                       |                   1.45 |                   1.55 |
| statistics_tab about store.s_street_name - all                         |                   1.98 |                   1.98 |
| statistics_tab about store.s_street_type - all                         |                   1.36 |                   1.70 |
| statistics_tab about store.s_suite_number - all                        |                   1.47 |                   1.84 |
| statistics_tab about store.s_city - all                                |                   1.28 |                   1.60 |
| statistics_tab about store.s_county - all                              |                   1.32 |                   1.40 |
| statistics_tab about store.s_state - all                               |                   1.68 |                   1.36 |
| statistics_tab about store.s_zip - all                                 |                   1.46 |                   1.36 |
| statistics_tab about store.s_country - all                             |                   1.53 |                   1.40 |
| statistics_tab about store.s_gmt_offset - all                          |                   1.40 |                   1.44 |
| statistics_tab about store.s_tax_precentage - all                      |                   1.30 |                   1.42 |
| statistics_tab about store_returns.sr_returned_date_sk - all           |                1670.98 |                2165.98 |
| statistics_tab about store_returns.sr_return_time_sk - all             |                 511.20 |                 518.48 |
| statistics_tab about store_returns.sr_item_sk - all                    |                1649.13 |                1635.94 |
| statistics_tab about store_returns.sr_customer_sk - all                |                1436.53 |                1425.26 |
| statistics_tab about store_returns.sr_cdemo_sk - all                   |                 596.72 |                 974.89 |
| statistics_tab about store_returns.sr_hdemo_sk - all                   |                 493.70 |                 594.61 |
| statistics_tab about store_returns.sr_addr_sk - all                    |                 543.21 |                 563.95 |
| statistics_tab about store_returns.sr_store_sk - all                   |                1300.91 |                1318.22 |
| statistics_tab about store_returns.sr_reason_sk - all                  |                 526.94 |                 501.66 |
| statistics_tab about store_returns.sr_ticket_number - all              |                1610.96 |                 574.74 |
| statistics_tab about store_returns.sr_return_quantity - all            |                 534.06 |                 530.43 |
| statistics_tab about store_returns.sr_return_amt - all                 |                1021.92 |                 921.59 |
| statistics_tab about store_returns.sr_return_tax - all                 |                1177.41 |                 802.37 |
| statistics_tab about store_returns.sr_return_amt_inc_tax - all         |                 997.45 |                 894.27 |
| statistics_tab about store_returns.sr_fee - all                        |                 845.66 |                 972.36 |
| statistics_tab about store_returns.sr_return_ship_cost - all           |                 899.48 |                1167.64 |
| statistics_tab about store_returns.sr_refunded_cash - all              |                 894.88 |                 913.66 |
| statistics_tab about store_returns.sr_reversed_charge - all            |                1218.70 |                 867.87 |
| statistics_tab about store_returns.sr_store_credit - all               |                1053.20 |                 852.54 |
| statistics_tab about store_returns.sr_net_loss - all                   |                 973.05 |                1675.27 |
| statistics_tab about store_sales.ss_sold_date_sk - all                 |                9241.52 |                8692.41 |
| statistics_tab about store_sales.ss_sold_time_sk - all                 |                4532.70 |                4730.38 |
| statistics_tab about store_sales.ss_item_sk - all                      |               26011.61 |               23891.17 |
| statistics_tab about store_sales.ss_customer_sk - all                  |                9464.70 |                9069.75 |
| statistics_tab about store_sales.ss_cdemo_sk - all                     |                5305.79 |                5453.00 |
| statistics_tab about store_sales.ss_hdemo_sk - all                     |                4915.39 |                4689.24 |
| statistics_tab about store_sales.ss_addr_sk - all                      |                4716.71 |                4585.45 |
| statistics_tab about store_sales.ss_store_sk - all                     |                9137.35 |                8991.26 |
| statistics_tab about store_sales.ss_promo_sk - all                     |               19775.07 |               21411.19 |
| statistics_tab about store_sales.ss_ticket_number - all                |                4579.67 |                4690.49 |
| statistics_tab about store_sales.ss_quantity - all                     |                5337.99 |                4547.93 |
| statistics_tab about store_sales.ss_wholesale_cost - all               |                8066.42 |                8144.77 |
| statistics_tab about store_sales.ss_list_price - all                   |                8225.60 |               22050.77 |
| statistics_tab about store_sales.ss_sales_price - all                  |                8623.49 |               21231.69 |
| statistics_tab about store_sales.ss_ext_discount_amt - all             |                7619.73 |                7761.28 |
| statistics_tab about store_sales.ss_ext_sales_price - all              |                9704.89 |               11542.36 |
| statistics_tab about store_sales.ss_ext_wholesale_cost - all           |               10079.14 |                9012.57 |
| statistics_tab about store_sales.ss_ext_list_price - all               |               10281.77 |                9719.61 |
| statistics_tab about store_sales.ss_ext_tax - all                      |                8319.48 |                9009.24 |
| statistics_tab about store_sales.ss_coupon_amt - all                   |                7943.56 |                7853.40 |
| statistics_tab about store_sales.ss_net_paid - all                     |               10401.26 |               10780.48 |
| statistics_tab about store_sales.ss_net_paid_inc_tax - all             |                9615.86 |               10285.42 |
| statistics_tab about store_sales.ss_net_profit - all                   |               10530.23 |               11356.27 |
| statistics_tab about time_dim.t_time_sk - all                          |                  19.57 |                  22.27 |
| statistics_tab about time_dim.t_time_id - all                          |                  88.89 |                  90.59 |
| statistics_tab about time_dim.t_time - all                             |                  18.10 |                  17.70 |
| statistics_tab about time_dim.t_hour - all                             |                  13.46 |                  13.86 |
| statistics_tab about time_dim.t_minute - all                           |                  13.46 |                  14.97 |
| statistics_tab about time_dim.t_second - all                           |                  14.14 |                  15.67 |
| statistics_tab about time_dim.t_am_pm - all                            |                  41.12 |                  33.59 |
| statistics_tab about time_dim.t_shift - all                            |                  38.43 |                  32.44 |
| statistics_tab about time_dim.t_sub_shift - all                        |                  40.77 |                  32.05 |
| statistics_tab about time_dim.t_meal_time - all                        |                  36.89 |                  29.86 |
| statistics_tab about warehouse.w_warehouse_sk - all                    |                   1.33 |                   0.84 |
| statistics_tab about warehouse.w_warehouse_id - all                    |                   1.38 |                   1.27 |
| statistics_tab about warehouse.w_warehouse_name - all                  |                   1.50 |                   1.01 |
| statistics_tab about warehouse.w_warehouse_sq_ft - all                 |                   1.40 |                   1.22 |
| statistics_tab about warehouse.w_street_number - all                   |                   1.61 |                   1.20 |
| statistics_tab about warehouse.w_street_name - all                     |                   1.40 |                   1.28 |
| statistics_tab about warehouse.w_street_type - all                     |                   1.35 |                   2.55 |
| statistics_tab about warehouse.w_suite_number - all                    |                   1.33 |                   1.26 |
| statistics_tab about warehouse.w_city - all                            |                   1.07 |                   1.33 |
| statistics_tab about warehouse.w_county - all                          |                   1.97 |                   1.45 |
| statistics_tab about warehouse.w_state - all                           |                   1.72 |                   1.78 |
| statistics_tab about warehouse.w_zip - all                             |                   1.36 |                   1.45 |
| statistics_tab about warehouse.w_country - all                         |                   1.62 |                   1.59 |
| statistics_tab about warehouse.w_gmt_offset - all                      |                   1.35 |                   1.67 |
| statistics_tab about web_page.wp_web_page_sk - all                     |                   1.59 |                   2.62 |
| statistics_tab about web_page.wp_web_page_id - all                     |                   1.99 |                   3.80 |
| statistics_tab about web_page.wp_rec_start_date - all                  |                   1.65 |                   1.21 |
| statistics_tab about web_page.wp_rec_end_date - all                    |                   1.52 |                   1.04 |
| statistics_tab about web_page.wp_creation_date_sk - all                |                   1.86 |                   0.94 |
| statistics_tab about web_page.wp_access_date_sk - all                  |                   1.38 |                   1.16 |
| statistics_tab about web_page.wp_autogen_flag - all                    |                   1.30 |                   1.04 |
| statistics_tab about web_page.wp_customer_sk - all                     |                   1.15 |                   0.75 |
| statistics_tab about web_page.wp_url - all                             |                   1.57 |                   0.93 |
| statistics_tab about web_page.wp_type - all                            |                   1.37 |                   1.18 |
| statistics_tab about web_page.wp_char_count - all                      |                   1.10 |                   0.93 |
| statistics_tab about web_page.wp_link_count - all                      |                   1.25 |                   1.33 |
| statistics_tab about web_page.wp_image_count - all                     |                   1.28 |                   0.93 |
| statistics_tab about web_page.wp_max_ad_count - all                    |                   1.33 |                   0.84 |
| statistics_tab about web_returns.wr_returned_date_sk - all             |                 374.65 |                 452.17 |
| statistics_tab about web_returns.wr_returned_time_sk - all             |                 167.85 |                 276.74 |
| statistics_tab about web_returns.wr_item_sk - all                      |                 403.33 |                 383.13 |
| statistics_tab about web_returns.wr_refunded_customer_sk - all         |                 175.64 |                 173.01 |
| statistics_tab about web_returns.wr_refunded_cdemo_sk - all            |                 175.16 |                 171.88 |
| statistics_tab about web_returns.wr_refunded_hdemo_sk - all            |                 146.22 |                 143.99 |
| statistics_tab about web_returns.wr_refunded_addr_sk - all             |                 163.51 |                 164.64 |
| statistics_tab about web_returns.wr_returning_customer_sk - all        |                 384.90 |                 397.10 |
| statistics_tab about web_returns.wr_returning_cdemo_sk - all           |                 171.55 |                 176.95 |
| statistics_tab about web_returns.wr_returning_hdemo_sk - all           |                 149.64 |                 150.83 |
| statistics_tab about web_returns.wr_returning_addr_sk - all            |                 172.58 |                 172.85 |
| statistics_tab about web_returns.wr_web_page_sk - all                  |                 138.52 |                 140.44 |
| statistics_tab about web_returns.wr_reason_sk - all                    |                 138.18 |                 140.68 |
| statistics_tab about web_returns.wr_order_number - all                 |                 149.95 |                 150.21 |
| statistics_tab about web_returns.wr_return_quantity - all              |                 134.62 |                 136.16 |
| statistics_tab about web_returns.wr_return_amt - all                   |                 253.12 |                 273.31 |
| statistics_tab about web_returns.wr_return_tax - all                   |                 333.16 |                 258.20 |
| statistics_tab about web_returns.wr_return_amt_inc_tax - all           |                 376.99 |                 308.98 |
| statistics_tab about web_returns.wr_fee - all                          |                 405.63 |                 286.69 |
| statistics_tab about web_returns.wr_return_ship_cost - all             |                 290.12 |                 393.01 |
| statistics_tab about web_returns.wr_refunded_cash - all                |                 279.40 |                 295.45 |
| statistics_tab about web_returns.wr_reversed_charge - all              |                 254.73 |                 254.24 |
| statistics_tab about web_returns.wr_account_credit - all               |                 243.65 |                 274.55 |
| statistics_tab about web_returns.wr_net_loss - all                     |                 249.89 |                 319.88 |
| statistics_tab about web_sales.ws_sold_date_sk - all                   |                2018.49 |                2524.17 |
| statistics_tab about web_sales.ws_sold_time_sk - all                   |                1248.21 |                2129.02 |
| statistics_tab about web_sales.ws_ship_date_sk - all                   |                3949.34 |                5123.46 |
| statistics_tab about web_sales.ws_item_sk - all                        |                4217.15 |                5719.51 |
| statistics_tab about web_sales.ws_bill_customer_sk - all               |                2339.32 |                2149.11 |
| statistics_tab about web_sales.ws_bill_cdemo_sk - all                  |                1486.75 |                2058.43 |
| statistics_tab about web_sales.ws_bill_hdemo_sk - all                  |                1237.83 |                1139.24 |
| statistics_tab about web_sales.ws_bill_addr_sk - all                   |                1685.39 |                1267.06 |
| statistics_tab about web_sales.ws_ship_customer_sk - all               |                2041.82 |                2158.28 |
| statistics_tab about web_sales.ws_ship_cdemo_sk - all                  |                1212.71 |                2013.76 |
| statistics_tab about web_sales.ws_ship_hdemo_sk - all                  |                1120.55 |                1276.56 |
| statistics_tab about web_sales.ws_ship_addr_sk - all                   |                2811.56 |                2461.97 |
| statistics_tab about web_sales.ws_web_page_sk - all                    |                1396.04 |                1676.58 |
| statistics_tab about web_sales.ws_web_site_sk - all                    |                4423.60 |                4315.88 |
| statistics_tab about web_sales.ws_ship_mode_sk - all                   |                1425.14 |                2006.63 |
| statistics_tab about web_sales.ws_warehouse_sk - all                   |                3494.36 |                3425.17 |
| statistics_tab about web_sales.ws_promo_sk - all                       |                4444.84 |                5439.51 |
| statistics_tab about web_sales.ws_order_number - all                   |                1252.27 |                1901.57 |
| statistics_tab about web_sales.ws_quantity - all                       |                1277.32 |                1304.64 |
| statistics_tab about web_sales.ws_wholesale_cost - all                 |                2034.85 |                2654.84 |
| statistics_tab about web_sales.ws_list_price - all                     |                2750.69 |                2147.98 |
| statistics_tab about web_sales.ws_sales_price - all                    |                2041.98 |                2108.27 |
| statistics_tab about web_sales.ws_ext_discount_amt - all               |                2388.79 |                2835.20 |
| statistics_tab about web_sales.ws_ext_sales_price - all                |                2807.00 |                2978.37 |
| statistics_tab about web_sales.ws_ext_wholesale_cost - all             |                2397.76 |                2360.09 |
| statistics_tab about web_sales.ws_ext_list_price - all                 |                3053.16 |                2725.99 |
| statistics_tab about web_sales.ws_ext_tax - all                        |                2279.51 |                2176.77 |
| statistics_tab about web_sales.ws_coupon_amt - all                     |                1936.92 |                1927.16 |
| statistics_tab about web_sales.ws_ext_ship_cost - all                  |                3222.84 |                2306.91 |
| statistics_tab about web_sales.ws_net_paid - all                       |                2517.15 |                2467.75 |
| statistics_tab about web_sales.ws_net_paid_inc_tax - all               |                2968.36 |                2488.99 |
| statistics_tab about web_sales.ws_net_paid_inc_ship - all              |                2866.62 |                2672.21 |
| statistics_tab about web_sales.ws_net_paid_inc_ship_tax - all          |                2678.12 |                3302.61 |
| statistics_tab about web_sales.ws_net_profit - all                     |                2452.17 |                2519.30 |
| statistics_tab about web_site.web_site_sk - all                        |                   1.36 |                   1.63 |
| statistics_tab about web_site.web_site_id - all                        |                   1.24 |                   1.24 |
| statistics_tab about web_site.web_rec_start_date - all                 |                   1.04 |                   1.12 |
| statistics_tab about web_site.web_rec_end_date - all                   |                   1.13 |                   1.15 |
| statistics_tab about web_site.web_name - all                           |                   1.05 |                   0.86 |
| statistics_tab about web_site.web_open_date_sk - all                   |                   0.91 |                   1.01 |
| statistics_tab about web_site.web_close_date_sk - all                  |                   0.77 |                   0.96 |
| statistics_tab about web_site.web_class - all                          |                   0.88 |                   1.04 |
| statistics_tab about web_site.web_manager - all                        |                   0.97 |                   1.05 |
| statistics_tab about web_site.web_mkt_id - all                         |                   0.78 |                   0.88 |
| statistics_tab about web_site.web_mkt_class - all                      |                   1.11 |                   0.89 |
| statistics_tab about web_site.web_mkt_desc - all                       |                   1.00 |                   1.40 |
| statistics_tab about web_site.web_market_manager - all                 |                   0.84 |                   1.01 |
| statistics_tab about web_site.web_company_id - all                     |                   1.15 |                   0.97 |
| statistics_tab about web_site.web_company_name - all                   |                   0.91 |                   0.90 |
| statistics_tab about web_site.web_street_number - all                  |                   1.04 |                   0.94 |
| statistics_tab about web_site.web_street_name - all                    |                   0.93 |                   1.50 |
| statistics_tab about web_site.web_street_type - all                    |                   0.94 |                   1.21 |
| statistics_tab about web_site.web_suite_number - all                   |                   1.06 |                   1.36 |
| statistics_tab about web_site.web_city - all                           |                   0.88 |                   0.93 |
| statistics_tab about web_site.web_county - all                         |                   0.97 |                   1.46 |
| statistics_tab about web_site.web_state - all                          |                   0.90 |                   1.30 |
| statistics_tab about web_site.web_zip - all                            |                   1.07 |                   0.94 |
| statistics_tab about web_site.web_country - all                        |                   1.05 |                   1.44 |
| statistics_tab about web_site.web_gmt_offset - all                     |                   0.91 |                   1.07 |
| statistics_tab about web_site.web_tax_percentage - all                 |                   0.85 |                   1.08 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      1346.27 |      2.96 |          23.49 |                 51.49 |
| postgresql-1-1-2-1 |      1346.27 |      2.96 |          23.49 |                 51.49 |

### Loading phase: component data generator

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |
| postgresql-1-1-2-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       205.30 |      1.20 |           0.01 |                  2.82 |
| postgresql-1-1-2-1 |       205.30 |      1.20 |           0.01 |                  2.82 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      1000.24 |      1.94 |          24.03 |                 51.86 |
| postgresql-1-1-2-1 |      1045.49 |      2.11 |          24.54 |                 51.26 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        26.54 |      0.67 |           0.31 |                  0.32 |
| postgresql-1-1-2-1 |        26.12 |      0.12 |           0.28 |                  0.29 |

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
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)

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













## MonetDB at SF 30

An example of MonetDB at SF=30, power and throughput test, is on [Example: Benchmark MonetDB](Example-MonetDB.md#tpc-ds-at-sf-30).
