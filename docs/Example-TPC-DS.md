# Benchmark: TPC-DS

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

TPC-DS does allow scaling data generation and ingestion, and scaling the benchmarking driver.
Scale-out can simulate distributed clients for the loading test and the throughput test [2].

This example shows how to benchmark 99 reading queries Q1-Q99 derived from TPC-DS in PostgreSQL.

> The query file is derived from the TPC-DS and as such is not comparable to published TPC-DS results, as the query file results do not comply with the TPC-DS Specification.

The queries are adapted, because
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

The experiment is run with the [tpcds file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpcds.py).

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
    * `-nlt 8` is ignored: the TPC-DS loaders use one connection per pod, and bexhoma says so in the log
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
* Duration: 632s 
* Code: 1795120919
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.0.
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'random_page_cost', 'target': 'container'}, '1.1'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_io_concurrency', 'target': 'container'}, '200'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'io_method', 'target': 'container'}, 'io_uring'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers_per_gather', 'target': 'container'}, '2'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers', 'target': 'container'}, '4'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_worker_processes', 'target': 'container'}, '6'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'shared_buffers', 'target': 'container'}, '20GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_cache_size', 'target': 'container'}, '48GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'work_mem', 'target': 'container'}, '1GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'maintenance_work_mem', 'target': 'container'}, '2GB')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:834185
  * datadisk:5787
  * volume_size:1.8T
  * volume_used:815G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795120919

### Ingestion
* PostgreSQL-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1795120919-75ccbbbf57-7prvw: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    1 |       94.00 |           2.00 |            1.00 |         49.00 |           33.00 |              8 |         0 |             | None           |             0 | False         |               38.30 | False               |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               99 |                  99 |        159 |            0.32 |            11635.11 |           2241.51 |          -1 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        159 |            0.32 |            11635.11 |           2241.51 |          -1 |

#### Query Completion per Phase

| phase            |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:-----------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   postgresql-1-1-1-1-1 |
|:--------------|-----------------------:|
| TPC-DS Q1     |                  91.23 |
| TPC-DS Q2     |                 336.94 |
| TPC-DS Q3     |                 112.12 |
| TPC-DS Q4     |                5547.88 |
| TPC-DS Q5     |                 472.97 |
| TPC-DS Q6     |               50039.42 |
| TPC-DS Q7     |                 322.67 |
| TPC-DS Q8     |                  47.33 |
| TPC-DS Q9     |                1872.25 |
| TPC-DS Q10    |                 897.26 |
| TPC-DS Q11    |                3178.72 |
| TPC-DS Q12    |                 118.03 |
| TPC-DS Q13    |                 511.79 |
| TPC-DS Q14a+b |                2182.75 |
| TPC-DS Q15    |                 107.50 |
| TPC-DS Q16    |                 196.30 |
| TPC-DS Q17    |                 259.25 |
| TPC-DS Q18    |                 343.39 |
| TPC-DS Q19    |                 134.81 |
| TPC-DS Q20    |                  85.90 |
| TPC-DS Q21    |                 241.64 |
| TPC-DS Q22    |                2771.96 |
| TPC-DS Q23a+b |                3138.78 |
| TPC-DS Q24a+b |                 730.03 |
| TPC-DS Q25    |                 264.48 |
| TPC-DS Q26    |                 211.67 |
| TPC-DS Q27    |                 315.78 |
| TPC-DS Q28    |                1578.19 |
| TPC-DS Q29    |                 290.79 |
| TPC-DS Q30    |                7329.64 |
| TPC-DS Q31    |                1305.48 |
| TPC-DS Q32    |                 100.67 |
| TPC-DS Q33    |                 302.07 |
| TPC-DS Q34    |                  17.44 |
| TPC-DS Q35    |                 971.32 |
| TPC-DS Q36    |                 287.17 |
| TPC-DS Q37    |                 442.84 |
| TPC-DS Q38    |                 822.42 |
| TPC-DS Q39a+b |                2033.47 |
| TPC-DS Q40    |                 106.69 |
| TPC-DS Q41    |                 714.32 |
| TPC-DS Q42    |                  91.64 |
| TPC-DS Q43    |                  18.13 |
| TPC-DS Q44    |                   1.80 |
| TPC-DS Q45    |                  75.68 |
| TPC-DS Q46    |                  22.82 |
| TPC-DS Q47    |                1276.22 |
| TPC-DS Q48    |                 483.06 |
| TPC-DS Q49    |                 418.94 |
| TPC-DS Q50    |                 395.90 |
| TPC-DS Q51    |                 688.59 |
| TPC-DS Q52    |                  88.69 |
| TPC-DS Q53    |                 118.74 |
| TPC-DS Q54    |                  58.30 |
| TPC-DS Q55    |                  87.13 |
| TPC-DS Q56    |                 258.77 |
| TPC-DS Q57    |                 771.62 |
| TPC-DS Q58    |                 352.62 |
| TPC-DS Q59    |                 410.65 |
| TPC-DS Q60    |                 321.11 |
| TPC-DS Q61    |                 104.74 |
| TPC-DS Q62    |                  83.96 |
| TPC-DS Q63    |                 114.69 |
| TPC-DS Q64    |                 605.55 |
| TPC-DS Q65    |                 499.37 |
| TPC-DS Q66    |                 172.52 |
| TPC-DS Q67    |                2756.78 |
| TPC-DS Q68    |                  29.33 |
| TPC-DS Q69    |                 293.22 |
| TPC-DS Q70    |                 343.35 |
| TPC-DS Q71    |                 248.79 |
| TPC-DS Q72    |                 797.08 |
| TPC-DS Q73    |                  22.14 |
| TPC-DS Q74    |                 911.63 |
| TPC-DS Q75    |                 567.03 |
| TPC-DS Q76    |                 140.67 |
| TPC-DS Q77    |                 274.18 |
| TPC-DS Q78    |                1461.99 |
| TPC-DS Q79    |                 107.12 |
| TPC-DS Q80    |                 364.80 |
| TPC-DS Q81    |               32621.45 |
| TPC-DS Q82    |                 352.45 |
| TPC-DS Q83    |                  70.99 |
| TPC-DS Q84    |                  67.44 |
| TPC-DS Q85    |                 259.63 |
| TPC-DS Q86    |                 186.59 |
| TPC-DS Q87    |                 830.68 |
| TPC-DS Q88    |                1970.19 |
| TPC-DS Q89    |                 128.79 |
| TPC-DS Q90    |                 103.60 |
| TPC-DS Q91    |                 120.18 |
| TPC-DS Q92    |                  57.02 |
| TPC-DS Q93    |                 262.90 |
| TPC-DS Q94    |                 138.06 |
| TPC-DS Q95    |                2634.73 |
| TPC-DS Q96    |                  98.43 |
| TPC-DS Q97    |                 348.82 |
| TPC-DS Q98    |                 426.54 |
| TPC-DS Q99    |                 160.31 |

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

This gives a survey about the errors and warnings (result set mismatch) and the latencies of execution per query.
Moreover the loading times (schema creation, ingestion and indexing), the geometric mean of query execution times and the TPC-DS metrics power and throughput are reported.
The results are not official TPC-DS results.
The data maintenance functions are not included.

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
usage: tpcds.py [-h] [-aws] [-db] [-sl] [-ss] [-ks {auto,yes,no}]
                [-xld {durable,relaxed,unsafe}] [-ar] [-cx CONTEXT]
                [-e EXPERIMENT] [-m] [-ma] [-mc] [-mm MONITORING_METRICS]
                [-ms MAX_SUT] [-mse MAX_SUT_EXPERIMENT]
                [-et EXPERIMENT_TIMEOUT] [-lt LOADING_TIMEOUT]
                [-nc NUM_CONFIG] [-ne NUM_QUERY_EXECUTORS] [-nw NUM_WORKER]
                [-nwr NUM_WORKER_REPLICAS] [-nws NUM_WORKER_SHARDS]
                [-xddl DDL_PARAMETERS] [-nlp NUM_LOADING_PODS]
                [-nlt NUM_LOADING_THREADS] [-nbp NUM_BENCHMARKING_PODS]
                [-nbt NUM_BENCHMARKING_THREADS] [-sf SCALING_FACTOR]
                [-t TIMEOUT] [-lr LIMIT_RAM] [-lc LIMIT_CPU] [-rr REQUEST_RAM]
                [-rc REQUEST_CPU] [-rct REQUEST_CPU_TYPE] [-rg REQUEST_GPU]
                [-rgt REQUEST_GPU_TYPE] [-rst REQUEST_STORAGE_TYPE]
                [-rss REQUEST_STORAGE_SIZE] [-rsr] [-rsrp]
                [-rnn [REQUEST_NODE_NAME]] [-rnl [REQUEST_NODE_LOADING]]
                [-rnb [REQUEST_NODE_BENCHMARKING]]
                [-rnp [REQUEST_NODE_POOLING]] [-rnw [REQUEST_NODE_WORKER]]
                [-mtn MULTI_TENANT_NUM] [-mtb MULTI_TENANT_BY] [-mtv] [-rp]
                [--set SETS]
                [-dbms [{PostgreSQL,MySQL,MariaDB,MariaDBCS,MonetDB,ClickHouse,ClickHouseCluster,DB2} ...]]
                [-xlit LIMIT_IMPORT_TABLE] [-xdt] [-xqr NUM_RUN]
                [-xnls NUM_LOADING_SPLIT] [-xii] [-xic] [-xis] [-xcol] [-xrcp]
                [-xrd] [-xshq] [-xaq ACTIVE_QUERIES] [-xve] [-xse]
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
  -ss, --skip-shutdown  keep SUT pods running after the experiment finishes;
                        same as --keep-sut yes
  -ks {auto,yes,no}, --keep-sut {auto,yes,no}
                        keep the SUT of each configuration's last repetition
                        running at the end: auto (default) keeps it in modes
                        load and start and stops it otherwise; yes keeps it,
                        no stops it. A kept SUT that another configuration
                        waits for (-ms/-mse) is stopped
  -xld {durable,relaxed,unsafe}, --load-durability {durable,relaxed,unsafe}
                        durability of the DBMS during the load only
                        (afterwards the configured state of template and --set
                        is restored): durable makes the load crash-safe (e.g.
                        PostgreSQL synchronous_commit/fsync on, MySQL
                        innodb_flush_log_at_trx_commit=1); relaxed (default)
                        commits without flushing and skips checks (e.g.
                        PostgreSQL synchronous_commit=off, MySQL
                        innodb_flush_log_at_trx_commit); unsafe uses the
                        strongest lever of the DBMS (e.g. MySQL redo log off,
                        PostgreSQL fsync=off), a crash during the load can
                        lose data. Runs the scripts durability-<level>.* and
                        restoredurability-<level>.* the DBMS folder has
  -ar, --activate-reset
                        activate configured reset scripts (e.g.
                        CHECKPOINT/VACUUM) when set on a benchmarker entry;
                        off by default
  -cx CONTEXT, --context CONTEXT
                        kubectl context to use (default: current context)
  -e EXPERIMENT, --experiment EXPERIMENT
                        resume an existing experiment by its code
  -m, --monitoring      enable Prometheus monitoring for the SUT
  -ma, --monitoring-app
                        enable application-level metrics collection
  -mc, --monitoring-cluster
                        enable node-level monitoring for the entire cluster
  -mm MONITORING_METRICS, --monitoring-metrics MONITORING_METRICS
                        switch single cluster-wide hardware metrics of
                        cluster.config on or off for this experiment,
                        overriding their 'active' flag, e.g.
                        total_gpu_util=on,total_network_rx=off; needs -m or
                        -mc
  -ms MAX_SUT, --max-sut MAX_SUT
                        maximum number of DBMS configurations to run in
                        parallel cluster-wide (default: no limit)
  -mse MAX_SUT_EXPERIMENT, --max-sut-experiment MAX_SUT_EXPERIMENT
                        maximum number of DBMS configurations in this
                        experiment to run in parallel (default: no limit)
  -et EXPERIMENT_TIMEOUT, --experiment-timeout EXPERIMENT_TIMEOUT
                        maximum wall-clock duration of the experiment in
                        minutes; when exceeded, the experiment is stopped and
                        all its components are removed from the cluster
                        (default: no limit)
  -lt LOADING_TIMEOUT, --loading-timeout LOADING_TIMEOUT
                        maximum loading duration per configuration in minutes;
                        captures diagnostics and removes the experiment when
                        exceeded (default: no limit)
  -nc NUM_CONFIG, --num-config NUM_CONFIG
                        number of experiment repetitions per configuration
  -ne NUM_QUERY_EXECUTORS, --num-query-executors NUM_QUERY_EXECUTORS
                        comma-separated list of parallel client counts to
                        sweep
  -nw NUM_WORKER, --num-worker NUM_WORKER
                        number of worker nodes for distributed DBMS
  -nwr NUM_WORKER_REPLICAS, --num-worker-replicas NUM_WORKER_REPLICAS
                        number of replicas per worker node
  -nws NUM_WORKER_SHARDS, --num-worker-shards NUM_WORKER_SHARDS
                        number of shards per worker node
  -xddl DDL_PARAMETERS, --ddl-parameter DDL_PARAMETERS
                        DDL parameter KEY=VALUE filled into the schema scripts
                        of every DBMS whose folder declares KEY in ddl-
                        parameters.config (repeatable); a comma list KEY=V1,V2
                        sweeps it, one configuration per value (several swept
                        keys: one per combination)
  -nlp NUM_LOADING_PODS, --num-loading-pods NUM_LOADING_PODS
                        comma-separated list of total loader pod counts
  -nlt NUM_LOADING_THREADS, --num-loading-threads NUM_LOADING_THREADS
                        comma-separated list of total loader threads (split
                        across pods)
  -nbp NUM_BENCHMARKING_PODS, --num-benchmarking-pods NUM_BENCHMARKING_PODS
                        comma-separated list of benchmarker pod counts
  -nbt NUM_BENCHMARKING_THREADS, --num-benchmarking-threads NUM_BENCHMARKING_THREADS
                        total benchmarking threads, split evenly across pods
  -sf SCALING_FACTOR, --scaling-factor SCALING_FACTOR
                        scaling factor controlling dataset size
  -t TIMEOUT, --timeout TIMEOUT
                        per-query timeout in seconds
  -lr LIMIT_RAM, --limit-ram LIMIT_RAM
                        RAM limit for the SUT and worker pods (e.g. 64Gi; 0 =
                        no limit); comma-separated to sweep several settings
                        (e.g. 32Gi,64Gi), one configuration per entry
  -lc LIMIT_CPU, --limit-cpu LIMIT_CPU
                        CPU limit for the SUT and worker pods (e.g. 4; 0 = no
                        limit); comma-separated to sweep, must then match the
                        length of any other swept resource list
  -rr REQUEST_RAM, --request-ram REQUEST_RAM
                        RAM request for the SUT and worker pods (e.g. 16Gi);
                        comma-separated to sweep several settings (e.g.
                        32Gi,64Gi), one configuration per entry
  -rc REQUEST_CPU, --request-cpu REQUEST_CPU
                        CPU request for the SUT and worker pods (e.g. 4);
                        comma-separated to sweep, must then match the length
                        of any other swept resource list
  -rct REQUEST_CPU_TYPE, --request-cpu-type REQUEST_CPU_TYPE
                        require SUT node to carry label cpu=<value>
  -rg REQUEST_GPU, --request-gpu REQUEST_GPU
                        number of GPUs to request for the SUT pod
  -rgt REQUEST_GPU_TYPE, --request-gpu-type REQUEST_GPU_TYPE
                        require SUT node to carry label gpu=<value>
  -rst REQUEST_STORAGE_TYPE, --request-storage-type REQUEST_STORAGE_TYPE
                        storage class for the SUT persistent volume ('' or
                        unset = ephemeral, 'ramdisk' = in-memory; other values
                        must be declared for the active cluster context, see
                        cluster config 'storage_classes'); comma-separated to
                        sweep the class, one configuration per entry and
                        paired by position with -rc/-lc/-rr/-lr, an empty
                        entry meaning ephemeral
  -rss REQUEST_STORAGE_SIZE, --request-storage-size REQUEST_STORAGE_SIZE
                        size of the SUT persistent volume (e.g. 10Gi)
  -rsr, --request-storage-remove
                        delete any existing PVC for the SUT before starting
  -rsrp, --request-storage-remove-per-repetition
                        delete the PVC of the SUT before every repetition
                        (-nc), so each repetition loads into a fresh volume;
                        implies -rsr
  -rnn [REQUEST_NODE_NAME], --request-node-name [REQUEST_NODE_NAME]
                        pin the SUT pod to this Kubernetes node
  -rnl [REQUEST_NODE_LOADING], --request-node-loading [REQUEST_NODE_LOADING]
                        pin loader pods to this Kubernetes node
  -rnb [REQUEST_NODE_BENCHMARKING], --request-node-benchmarking [REQUEST_NODE_BENCHMARKING]
                        pin benchmarker pods to this Kubernetes node
  -rnp [REQUEST_NODE_POOLING], --request-node-pooling [REQUEST_NODE_POOLING]
                        pin pooling pods to this Kubernetes node
  -rnw [REQUEST_NODE_WORKER], --request-node-worker [REQUEST_NODE_WORKER]
                        pin the worker pods (all StatefulSets of the SUT) to
                        these Kubernetes nodes, joined by '+' and spread
                        evenly (e.g. cl-worker37+cl-worker38+cl-worker39);
                        'sut' stands for the -rnn node; comma-separated to
                        sweep, one configuration per entry and paired by
                        position with -rc/-lc/-rr/-lr/-rst
  -mtn MULTI_TENANT_NUM, --multi-tenant-num MULTI_TENANT_NUM
                        number of tenants for multi-tenant experiments
  -mtb MULTI_TENANT_BY, --multi-tenant-by MULTI_TENANT_BY
                        tenancy granularity: schema, database, or container
  -mtv, --multi-tenant-volume
                        allocate a separate persistent volume per tenant
  -rp, --report         also write a tiered Markdown summary report
                        (report/index.md + detail files) to the result folder
  --set SETS            override a deployment parameter, e.g.
                        deployment[bexhoma-deployment-
                        postgres].container[dbms].max_worker_processes=128;
                        the name in deployment[...] is metadata.name of the
                        Deployment in the DBMS template (PostgreSQL -c
                        key=value, MySQL/MariaDB --key=value, chosen by the
                        template) or an environment variable via
                        ...container[dbms].env.NAME=VALUE; an emptyDir volume
                        of the SUT via
                        deployment[NAME].volume[VOLUME].sizeLimit=64Gi or
                        .medium=Memory (empty: node disk)
  -dbms [{PostgreSQL,MySQL,MariaDB,MariaDBCS,MonetDB,ClickHouse,ClickHouseCluster,DB2} ...], --dbms [{PostgreSQL,MySQL,MariaDB,MariaDBCS,MonetDB,ClickHouse,ClickHouseCluster,DB2} ...]
                        one or more DBMS engines to test
  -xlit LIMIT_IMPORT_TABLE, --xlimit-import-table LIMIT_IMPORT_TABLE
                        import only this table (useful for partial re-loads)
  -xdt, --xdata-transfer
                        also measure data transfer volume per query
  -xqr NUM_RUN, --xnum-query-runs NUM_RUN
                        number of times to repeat each query
  -xnls NUM_LOADING_SPLIT, --xnum-loading-split NUM_LOADING_SPLIT
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
  -xrd, --xrecreate-data
                        generate the raw data again although it exists on the
                        shared data volume, e.g. to measure the data generator
                        (-mc); the new files replace the old ones atomically,
                        so a loader of a parallel configuration keeps reading
                        complete files
  -xshq, --xshuffle-queries
                        shuffle query execution order independently per stream
  -xaq ACTIVE_QUERIES, --xactive-queries ACTIVE_QUERIES
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

[Monitoring](Monitoring.md) can be activated for DBMS only (`-m`) or for all components (`-mc`).

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
  -ms $BEXHOMA_MS \
  -t 1200 \
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
* Duration: 2273s 
* Code: 1794605374
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'random_page_cost', 'target': 'container'}, '1.1'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_io_concurrency', 'target': 'container'}, '200'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'io_method', 'target': 'container'}, 'io_uring'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers_per_gather', 'target': 'container'}, '2'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers', 'target': 'container'}, '4'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_worker_processes', 'target': 'container'}, '6'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'shared_buffers', 'target': 'container'}, '20GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_cache_size', 'target': 'container'}, '48GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'work_mem', 'target': 'container'}, '1GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'maintenance_work_mem', 'target': 'container'}, '2GB')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1137071
  * datadisk:14228
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794605374

### Ingestion
* PostgreSQL-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1794605374-78d7b6b57-jz2sm: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    3 |      247.00 |           5.00 |            1.00 |        148.00 |           84.00 |              8 |         0 |             | None           |             0 | False         |               43.72 | False               |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 | 3.00 |               99 |                  99 |       1667 |            0.88 |            12545.38 |            641.39 |          -1 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |       1667 |            0.88 |            12545.38 |            641.39 |          -1 |

#### Query Completion per Phase

| phase            |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:-----------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   postgresql-1-1-1-1-1 |
|:--------------|-----------------------:|
| TPC-DS Q1     |              936170.51 |
| TPC-DS Q2     |                1061.48 |
| TPC-DS Q3     |                 301.22 |
| TPC-DS Q4     |               18743.13 |
| TPC-DS Q5     |                2323.08 |
| TPC-DS Q6     |              221867.65 |
| TPC-DS Q7     |                 545.06 |
| TPC-DS Q8     |                 230.20 |
| TPC-DS Q9     |                3279.12 |
| TPC-DS Q10    |                1347.62 |
| TPC-DS Q11    |               10467.86 |
| TPC-DS Q12    |                 135.42 |
| TPC-DS Q13    |                1158.92 |
| TPC-DS Q14a+b |                8225.18 |
| TPC-DS Q15    |                 289.32 |
| TPC-DS Q16    |                 418.23 |
| TPC-DS Q17    |                 698.19 |
| TPC-DS Q18    |                 654.25 |
| TPC-DS Q19    |                 418.30 |
| TPC-DS Q20    |                 239.34 |
| TPC-DS Q21    |                 500.79 |
| TPC-DS Q22    |                7118.65 |
| TPC-DS Q23a+b |               12403.76 |
| TPC-DS Q24a+b |                 881.93 |
| TPC-DS Q25    |                 619.21 |
| TPC-DS Q26    |                 425.50 |
| TPC-DS Q27    |                 565.15 |
| TPC-DS Q28    |                2417.56 |
| TPC-DS Q29    |                 723.66 |
| TPC-DS Q30    |               66779.62 |
| TPC-DS Q31    |                3673.54 |
| TPC-DS Q32    |                 261.27 |
| TPC-DS Q33    |                 645.59 |
| TPC-DS Q34    |                  34.61 |
| TPC-DS Q35    |                1419.71 |
| TPC-DS Q36    |                 779.50 |
| TPC-DS Q37    |                 722.33 |
| TPC-DS Q38    |                2968.27 |
| TPC-DS Q39a+b |                5468.51 |
| TPC-DS Q40    |                 213.46 |
| TPC-DS Q41    |                2448.66 |
| TPC-DS Q42    |                 255.75 |
| TPC-DS Q43    |                  52.73 |
| TPC-DS Q44    |                 539.96 |
| TPC-DS Q45    |                 187.27 |
| TPC-DS Q46    |                  61.60 |
| TPC-DS Q47    |                3524.26 |
| TPC-DS Q48    |                1055.79 |
| TPC-DS Q49    |                1030.33 |
| TPC-DS Q50    |                1186.77 |
| TPC-DS Q51    |                2111.13 |
| TPC-DS Q52    |                 246.86 |
| TPC-DS Q53    |                 310.72 |
| TPC-DS Q54    |                  60.39 |
| TPC-DS Q55    |                 244.99 |
| TPC-DS Q56    |                 682.00 |
| TPC-DS Q57    |                1774.71 |
| TPC-DS Q58    |                 694.38 |
| TPC-DS Q59    |                1194.02 |
| TPC-DS Q60    |                 813.97 |
| TPC-DS Q61    |                 105.80 |
| TPC-DS Q62    |                 203.01 |
| TPC-DS Q63    |                 319.78 |
| TPC-DS Q64    |                1235.87 |
| TPC-DS Q65    |                1618.99 |
| TPC-DS Q66    |                 513.26 |
| TPC-DS Q67    |                8296.80 |
| TPC-DS Q68    |                  67.65 |
| TPC-DS Q69    |                 674.00 |
| TPC-DS Q70    |                 922.74 |
| TPC-DS Q71    |                 687.98 |
| TPC-DS Q72    |                2165.12 |
| TPC-DS Q73    |                  36.40 |
| TPC-DS Q74    |                1445.37 |
| TPC-DS Q75    |                2682.48 |
| TPC-DS Q76    |                 532.60 |
| TPC-DS Q77    |                 588.38 |
| TPC-DS Q78    |                4231.88 |
| TPC-DS Q79    |                 454.27 |
| TPC-DS Q80    |                 729.39 |
| TPC-DS Q81    |              271701.16 |
| TPC-DS Q82    |                 999.40 |
| TPC-DS Q83    |                 120.29 |
| TPC-DS Q84    |                  86.73 |
| TPC-DS Q85    |                 394.29 |
| TPC-DS Q86    |                 238.96 |
| TPC-DS Q87    |                2247.03 |
| TPC-DS Q88    |                3068.03 |
| TPC-DS Q89    |                 310.81 |
| TPC-DS Q90    |                 273.70 |
| TPC-DS Q91    |                 141.78 |
| TPC-DS Q92    |                 109.47 |
| TPC-DS Q93    |                 854.24 |
| TPC-DS Q94    |                 294.06 |
| TPC-DS Q95    |                6503.67 |
| TPC-DS Q96    |                 255.09 |
| TPC-DS Q97    |                 935.70 |
| TPC-DS Q98    |                 395.87 |
| TPC-DS Q99    |                 479.99 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       288.01 |      2.23 |           6.37 |                 13.05 |

### Loading phase: component data generator

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        46.44 |      0.37 |           0.01 |                  2.21 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      1781.64 |      1.87 |           6.59 |                 13.69 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        25.58 |      0.07 |           0.29 |                  0.30 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)

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

This gives a survey about CPU (in CPU seconds) and RAM usage (in Gb) during loading and execution of the benchmark.
Metrics are fetched every 30 seconds, so a short phase has few samples.


## Resources of the Clients

To get an impression of the resources the clients need, `-mc` also monitors the components outside the SUT.
This run uses MonetDB at SF 30, so that every phase lasts long enough for the monitoring.
`-xrd` generates the raw data again although it exists on the shared data volume, so that the summary also contains the data generator; `-ms 1` keeps other SUTs off the cluster during the measurement: `-ms` counts the SUTs of the whole cluster, so the experiment waits until no SUT of another experiment runs.
`-ne 1,2` runs one and then two parallel query streams.

```bash
bexhoma tpcds \
  -dbms MonetDB \
  -sf 30 \
  -nc 1 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xrd \
  -m \
  -mc \
  -ms 1 \
  -t 14400 \
  -lr 1024Gi \
  -rr 900Gi \
  -rsr \
  -rss 3000Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_monetdb_clients.log
```

The tables *Loading phase: component data generator*, *Loading phase: component loader* and *Benchmarking phase: component benchmarker* show the clients: `CPU [CPUs]` is the CPU time in seconds, `Max CPU` the peak number of cores and `Max RAM [Gb]` the peak working set of all pods of the component.
The data generator and the loader run in 8 pods (`-nlp 8`); the benchmarker runs one pod per stream.

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_monetdb_clients_summary.md" target="_blank" rel="noopener">docs_tpcds_monetdb_clients.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=30
* Type: tpcds
* Duration: 8165s 
* Code: 1795772856
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=30) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 14400.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
  * System metrics are monitored by a cluster-wide installation for all components.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 3000Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 1.
  * SUT requests 4 CPU and 900Gi RAM. RAM limit is 1024Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:745326
  * datadisk:75600
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
    * code:1795772856
* monetdb-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:745326
  * datadisk:76836
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
    * code:1795772856
* monetdb-1-1-2-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:745326
  * datadisk:76836
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
    * code:1795772856

### Ingestion
* MonetDB-1: 81 of 81 units ok

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1795772856-6bff4547b5-q8lx8: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpcds (2 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpcds (2 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |   30 |     1576.00 |           2.00 |          563.00 |        491.00 |          517.00 |              8 |         0 |             | None           |             0 | False         |               68.53 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 30.00 |               99 |                  99 |        355 |            0.54 |           201608.06 |          30118.31 |          -1 |
| monetdb-1-1-2-1-1 | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |       1 | 30.00 |               99 |                  99 |        398 |            0.66 |           162522.23 |          26864.32 |          -1 |
| monetdb-1-1-2-1-2 | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |       2 | 30.00 |               99 |                  99 |        421 |            0.57 |           190218.65 |          25396.67 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        355 |            0.54 |           201608.06 |          30118.31 |          -1 |
| monetdb-1-1-2 | monetdb-1-1-2 |                1 |        2 |               1 |           2 | 30.00 |              198 |                 198 |        421 |            0.61 |           175825.93 |          50793.35 |          -1 |

#### Query Completion per Phase

| phase         |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:--------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| monetdb-1-1-2 |      2 | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   monetdb-1-1-1-1-1 |   monetdb-1-1-2-1-1 |   monetdb-1-1-2-1-2 |
|:--------------|--------------------:|--------------------:|--------------------:|
| TPC-DS Q1     |              124.01 |              107.95 |              215.88 |
| TPC-DS Q2     |             1461.25 |             1833.90 |             2191.54 |
| TPC-DS Q3     |              105.05 |              108.21 |              101.83 |
| TPC-DS Q4     |            15832.98 |            14752.68 |            15590.25 |
| TPC-DS Q5     |             1425.42 |             1428.07 |             1324.32 |
| TPC-DS Q6     |              446.08 |              773.99 |              747.21 |
| TPC-DS Q7     |              183.42 |              158.86 |              400.40 |
| TPC-DS Q8     |              315.65 |              374.19 |              308.49 |
| TPC-DS Q9     |              500.85 |              825.08 |              671.29 |
| TPC-DS Q10    |              189.13 |              239.59 |              151.34 |
| TPC-DS Q11    |             7210.77 |             6756.72 |             7593.00 |
| TPC-DS Q12    |              149.21 |              113.54 |              171.63 |
| TPC-DS Q13    |              341.36 |              291.30 |              289.71 |
| TPC-DS Q14a+b |            29978.61 |            29917.20 |            31467.36 |
| TPC-DS Q15    |              146.26 |              142.36 |              129.83 |
| TPC-DS Q16    |            44476.90 |            41171.92 |            67929.13 |
| TPC-DS Q17    |             2455.90 |             3681.04 |             2221.02 |
| TPC-DS Q18    |              949.72 |             3810.74 |              955.35 |
| TPC-DS Q19    |              186.11 |            10548.01 |              143.71 |
| TPC-DS Q20    |              129.91 |            11701.91 |              112.51 |
| TPC-DS Q21    |              113.12 |              108.94 |              107.41 |
| TPC-DS Q22    |             1057.05 |             1102.88 |             1021.34 |
| TPC-DS Q23a+b |            53570.09 |            49899.90 |            52353.71 |
| TPC-DS Q24a+b |            14380.13 |            11788.36 |            14540.61 |
| TPC-DS Q25    |             2430.52 |             3347.83 |             3566.38 |
| TPC-DS Q26    |              189.21 |              550.16 |              173.85 |
| TPC-DS Q27    |             1259.54 |             1465.74 |             1935.99 |
| TPC-DS Q28    |              533.24 |             2179.99 |              581.36 |
| TPC-DS Q29    |             2841.34 |             2873.41 |             2963.92 |
| TPC-DS Q30    |               89.98 |              289.88 |               74.86 |
| TPC-DS Q31    |             1590.91 |             2387.99 |             1579.72 |
| TPC-DS Q32    |              164.70 |              184.11 |              179.12 |
| TPC-DS Q33    |              122.69 |              112.00 |              339.04 |
| TPC-DS Q34    |              107.90 |              103.69 |              102.54 |
| TPC-DS Q35    |              727.45 |             1173.29 |              691.12 |
| TPC-DS Q36    |             1996.99 |             2608.11 |             1402.87 |
| TPC-DS Q37    |              454.47 |              422.23 |              546.98 |
| TPC-DS Q38    |             2858.25 |             2639.59 |             2463.81 |
| TPC-DS Q39a+b |             1616.40 |             1188.82 |             1233.98 |
| TPC-DS Q40    |              928.35 |             1293.94 |             1536.99 |
| TPC-DS Q41    |                6.51 |                7.58 |                6.70 |
| TPC-DS Q42    |              106.34 |              114.25 |              135.88 |
| TPC-DS Q43    |              217.36 |              196.00 |              217.52 |
| TPC-DS Q44    |              195.73 |              215.58 |              257.21 |
| TPC-DS Q45    |              127.34 |              123.04 |              131.44 |
| TPC-DS Q46    |              200.72 |              218.18 |              305.26 |
| TPC-DS Q47    |             1591.54 |              830.05 |              982.05 |
| TPC-DS Q48    |              206.33 |              217.15 |              229.16 |
| TPC-DS Q49    |             1044.65 |             1308.48 |             1061.89 |
| TPC-DS Q50    |              615.83 |              554.15 |              573.06 |
| TPC-DS Q51    |             3065.12 |             2815.27 |             3023.40 |
| TPC-DS Q52    |              101.74 |              111.04 |               87.73 |
| TPC-DS Q53    |               90.70 |               92.63 |              165.43 |
| TPC-DS Q54    |               92.85 |               98.92 |              127.24 |
| TPC-DS Q55    |               57.71 |               97.53 |              102.40 |
| TPC-DS Q56    |              140.19 |              157.82 |              122.62 |
| TPC-DS Q57    |              128.84 |              138.80 |              148.83 |
| TPC-DS Q58    |              520.81 |              590.79 |              545.99 |
| TPC-DS Q59    |              998.54 |              693.89 |              754.48 |
| TPC-DS Q60    |              152.37 |              154.67 |              155.66 |
| TPC-DS Q61    |              158.61 |              163.79 |              190.92 |
| TPC-DS Q62    |              259.96 |              270.47 |              309.83 |
| TPC-DS Q63    |              134.65 |              102.48 |               91.90 |
| TPC-DS Q64    |             4539.93 |             2281.65 |             2297.30 |
| TPC-DS Q65    |             1967.58 |             1119.92 |             1207.44 |
| TPC-DS Q66    |              298.08 |              316.89 |              302.19 |
| TPC-DS Q67    |             6026.07 |             6455.00 |             5836.87 |
| TPC-DS Q68    |              212.91 |              221.91 |              224.25 |
| TPC-DS Q69    |              293.96 |              280.99 |              237.49 |
| TPC-DS Q70    |             1531.69 |             1506.37 |             1544.38 |
| TPC-DS Q71    |              294.57 |              206.42 |              184.65 |
| TPC-DS Q72    |             1901.57 |             1081.13 |             1041.38 |
| TPC-DS Q73    |              142.09 |               99.96 |               97.83 |
| TPC-DS Q74    |             1954.28 |             2267.34 |             2370.78 |
| TPC-DS Q75    |             5576.75 |             5351.57 |             5727.89 |
| TPC-DS Q76    |              179.31 |              156.33 |              256.94 |
| TPC-DS Q77    |              734.24 |              753.59 |              686.34 |
| TPC-DS Q78    |            12681.29 |            13356.51 |            13714.74 |
| TPC-DS Q79    |              251.49 |              242.70 |              265.07 |
| TPC-DS Q80    |             7508.01 |             8587.38 |             8665.00 |
| TPC-DS Q81    |              140.01 |              185.09 |              368.25 |
| TPC-DS Q82    |              447.63 |              477.40 |              479.44 |
| TPC-DS Q83    |               65.65 |               44.67 |               36.07 |
| TPC-DS Q84    |               28.97 |               36.19 |               34.19 |
| TPC-DS Q85    |              289.24 |              288.82 |              324.14 |
| TPC-DS Q86    |              307.28 |              299.31 |              293.39 |
| TPC-DS Q87    |             3438.74 |             2637.17 |             2790.67 |
| TPC-DS Q88    |              442.41 |              440.57 |              511.85 |
| TPC-DS Q89    |              138.38 |              169.23 |              167.18 |
| TPC-DS Q90    |               68.83 |               81.24 |               68.01 |
| TPC-DS Q91    |               26.24 |               40.41 |               35.52 |
| TPC-DS Q92    |              104.22 |              162.38 |              156.96 |
| TPC-DS Q93    |             2402.93 |             2285.92 |             1994.42 |
| TPC-DS Q94    |            40927.30 |            36720.13 |            75565.53 |
| TPC-DS Q95    |            42709.70 |            42464.51 |            43327.96 |
| TPC-DS Q96    |               33.78 |             2558.81 |               52.84 |
| TPC-DS Q97    |             3015.74 |            22826.25 |             3209.45 |
| TPC-DS Q98    |              140.90 |              153.54 |              149.49 |
| TPC-DS Q99    |              235.13 |              254.55 |              241.52 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      3087.61 |      6.96 |          73.59 |                 73.60 |
| monetdb-1-1-2-1 |      3087.61 |      6.96 |          73.59 |                 73.60 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      4146.41 |      8.00 |           0.02 |                  5.98 |
| monetdb-1-1-2-1 |      4146.41 |      8.00 |           0.02 |                  5.98 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |       468.39 |      1.33 |           0.00 |                  0.00 |
| monetdb-1-1-2-1 |       468.39 |      1.33 |           0.00 |                  0.00 |

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      5728.01 |     73.47 |         419.30 |                419.31 |
| monetdb-1-1-2-1 |     12902.17 |    132.85 |         451.81 |                451.83 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        15.73 |      0.02 |           0.29 |                  0.30 |
| monetdb-1-1-2-1 |        32.53 |      0.95 |           0.30 |                  0.31 |

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
* CPU Throttling Rate [s/s] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)

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


## Perform Benchmark - Throughput Test

The experiment is run with the [tpcds file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpcds.py).

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
* Duration: 853s 
* Code: 1794607790
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
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
  * disk:1129609
  * datadisk:5791
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794607790
* postgresql-1-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1132177
  * datadisk:5791
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794607790
* postgresql-1-1-2-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1132177
  * datadisk:5791
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794607790

### Ingestion
* PostgreSQL-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1794607790-67c88fbc64-rggwr: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpcds (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpcds (2 pods)

### Loading

#### Per Run

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    1 |       97.00 |           5.00 |            1.00 |         45.00 |           38.00 |              8 |         0 |             | None           |             0 | False         |               37.11 | False               |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               99 |                  99 |        163 |            0.32 |            11452.18 |           2186.50 |          -1 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       1 | 1.00 |               99 |                  99 |        176 |            0.37 |            10038.95 |           2025.00 |          -1 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       2 | 1.00 |               99 |                  99 |        174 |            0.37 |             9940.59 |           2048.28 |          -1 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        163 |            0.32 |            11452.18 |           2186.50 |          -1 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        2 |               1 |           2 | 1.00 |              198 |                 198 |        176 |            0.37 |             9989.65 |           4050.00 |          -1 |

#### Query Completion per Phase

| phase            |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:-----------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| postgresql-1-1-2 |      2 | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   postgresql-1-1-1-1-1 |   postgresql-1-1-2-1-1 |   postgresql-1-1-2-1-2 |
|:--------------|-----------------------:|-----------------------:|-----------------------:|
| TPC-DS Q1     |                  86.73 |                  92.20 |                  86.07 |
| TPC-DS Q2     |                 325.48 |                 325.35 |                 331.25 |
| TPC-DS Q3     |                 103.25 |                  97.90 |                 105.68 |
| TPC-DS Q4     |                5518.15 |                5430.23 |                5798.33 |
| TPC-DS Q5     |                 466.75 |                 458.55 |                 466.32 |
| TPC-DS Q6     |               50066.76 |               50388.75 |               50923.73 |
| TPC-DS Q7     |                 334.23 |                 300.75 |                 317.49 |
| TPC-DS Q8     |                  48.78 |                  50.41 |                  54.42 |
| TPC-DS Q9     |                1909.52 |                1861.43 |                1929.26 |
| TPC-DS Q10    |                 878.82 |                 859.55 |                 980.01 |
| TPC-DS Q11    |                3157.06 |                3806.66 |                3306.80 |
| TPC-DS Q12    |                  57.05 |                  52.26 |                 105.46 |
| TPC-DS Q13    |                 588.27 |                 831.47 |                 663.74 |
| TPC-DS Q14a+b |                2202.97 |                3236.87 |                2559.16 |
| TPC-DS Q15    |                 103.02 |                  94.88 |                 101.00 |
| TPC-DS Q16    |                 193.05 |                 411.85 |                 186.67 |
| TPC-DS Q17    |                 275.88 |                 413.32 |                 332.59 |
| TPC-DS Q18    |                 358.60 |                 336.72 |                 651.19 |
| TPC-DS Q19    |                 125.55 |                 124.25 |                 130.93 |
| TPC-DS Q20    |                  89.40 |                  86.21 |                  84.14 |
| TPC-DS Q21    |                 231.34 |                 258.02 |                 229.53 |
| TPC-DS Q22    |                2726.59 |                3100.28 |                2891.59 |
| TPC-DS Q23a+b |                3214.04 |                3226.20 |                3521.00 |
| TPC-DS Q24a+b |                 496.92 |                 514.20 |                 570.01 |
| TPC-DS Q25    |                 273.36 |                 257.38 |                 255.53 |
| TPC-DS Q26    |                 203.07 |                 201.94 |                 201.51 |
| TPC-DS Q27    |                 323.43 |                 328.86 |                 300.24 |
| TPC-DS Q28    |                1467.50 |                1439.51 |                1390.76 |
| TPC-DS Q29    |                 384.03 |                 272.19 |                 277.38 |
| TPC-DS Q30    |                7694.58 |                7830.05 |                7839.44 |
| TPC-DS Q31    |                1325.95 |                1479.87 |                1302.90 |
| TPC-DS Q32    |                  89.65 |                 115.08 |                 163.63 |
| TPC-DS Q33    |                 337.20 |                 446.17 |                 497.63 |
| TPC-DS Q34    |                  19.49 |                  22.35 |                  23.50 |
| TPC-DS Q35    |                1141.18 |                 977.92 |                1074.66 |
| TPC-DS Q36    |                 265.88 |                 261.78 |                 263.11 |
| TPC-DS Q37    |                 278.22 |                 278.89 |                 276.42 |
| TPC-DS Q38    |                 766.52 |                1259.45 |                 757.34 |
| TPC-DS Q39a+b |                2168.88 |                2333.45 |                2787.23 |
| TPC-DS Q40    |                 110.46 |                  96.77 |                 105.18 |
| TPC-DS Q41    |                 747.36 |                 743.08 |                 760.44 |
| TPC-DS Q42    |                  93.43 |                  86.95 |                  92.74 |
| TPC-DS Q43    |                  21.36 |                  19.06 |                  23.49 |
| TPC-DS Q44    |                 341.50 |                 335.49 |                 346.15 |
| TPC-DS Q45    |                  66.65 |                  71.75 |                  68.27 |
| TPC-DS Q46    |                  28.00 |                  30.13 |                  26.33 |
| TPC-DS Q47    |                1327.01 |                1308.96 |                1378.19 |
| TPC-DS Q48    |                 479.70 |                 468.61 |                 466.65 |
| TPC-DS Q49    |                 431.79 |                 587.71 |                 588.54 |
| TPC-DS Q50    |                 316.58 |                 311.39 |                 311.27 |
| TPC-DS Q51    |                 708.74 |                 886.01 |                 887.24 |
| TPC-DS Q52    |                  99.73 |                  92.52 |                  92.04 |
| TPC-DS Q53    |                 117.18 |                 308.71 |                 304.65 |
| TPC-DS Q54    |                  66.42 |                 130.35 |                 143.86 |
| TPC-DS Q55    |                  91.69 |                 213.50 |                 201.34 |
| TPC-DS Q56    |                 280.98 |                 315.77 |                 364.43 |
| TPC-DS Q57    |                 715.85 |                 701.07 |                 760.58 |
| TPC-DS Q58    |                 300.69 |                 372.29 |                 343.86 |
| TPC-DS Q59    |                 412.41 |                 414.11 |                 415.78 |
| TPC-DS Q60    |                 531.20 |                 328.04 |                 328.08 |
| TPC-DS Q61    |                 121.13 |                 102.04 |                 104.01 |
| TPC-DS Q62    |                  97.05 |                  85.01 |                  85.25 |
| TPC-DS Q63    |                 129.55 |                 113.48 |                 118.43 |
| TPC-DS Q64    |                 573.36 |                 685.27 |                 617.04 |
| TPC-DS Q65    |                 511.13 |                 677.83 |                 525.41 |
| TPC-DS Q66    |                 152.76 |                 160.55 |                 158.87 |
| TPC-DS Q67    |                2588.28 |                2554.63 |                2635.12 |
| TPC-DS Q68    |                  30.41 |                  28.30 |                  30.17 |
| TPC-DS Q69    |                 110.63 |                 179.49 |                 117.01 |
| TPC-DS Q70    |                 359.06 |                 413.07 |                 348.01 |
| TPC-DS Q71    |                 273.48 |                 525.34 |                 261.69 |
| TPC-DS Q72    |                 809.30 |                1269.89 |                1414.68 |
| TPC-DS Q73    |                  21.19 |                  22.04 |                  40.53 |
| TPC-DS Q74    |                 853.27 |                 856.56 |                 905.95 |
| TPC-DS Q75    |                 602.29 |                 602.88 |                 594.56 |
| TPC-DS Q76    |                 234.21 |                 214.13 |                 233.17 |
| TPC-DS Q77    |                 288.13 |                 301.71 |                 284.50 |
| TPC-DS Q78    |                1004.58 |                1381.29 |                1520.96 |
| TPC-DS Q79    |                 119.73 |                 121.00 |                 149.88 |
| TPC-DS Q80    |                 365.19 |                 362.01 |                 359.29 |
| TPC-DS Q81    |               32791.17 |               34760.03 |               35644.25 |
| TPC-DS Q82    |                 331.59 |                 514.98 |                 588.42 |
| TPC-DS Q83    |                  69.83 |                 136.83 |                 142.99 |
| TPC-DS Q84    |                  18.39 |                  41.32 |                  41.72 |
| TPC-DS Q85    |                 272.39 |                 496.94 |                 984.18 |
| TPC-DS Q86    |                 156.29 |                 264.34 |                 221.01 |
| TPC-DS Q87    |                 818.73 |                 993.35 |                1032.26 |
| TPC-DS Q88    |                2001.02 |                2535.06 |                2530.23 |
| TPC-DS Q89    |                 133.27 |                 145.42 |                 135.60 |
| TPC-DS Q90    |                  93.76 |                 107.98 |                 106.33 |
| TPC-DS Q91    |                 113.29 |                 121.74 |                 123.48 |
| TPC-DS Q92    |                  56.90 |                  57.67 |                  59.17 |
| TPC-DS Q93    |                 203.38 |                 258.02 |                 286.30 |
| TPC-DS Q94    |                 138.19 |                 143.43 |                 146.29 |
| TPC-DS Q95    |                2645.61 |                2556.65 |                2554.16 |
| TPC-DS Q96    |                  95.21 |                 102.47 |                 102.64 |
| TPC-DS Q97    |                 328.53 |                 353.61 |                 429.57 |
| TPC-DS Q98    |                 140.07 |                 256.00 |                 424.37 |
| TPC-DS Q99    |                 161.89 |                 403.37 |                 167.73 |

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
With repetitions (`-nc`), `-rsr` removes an existing volume only before the first repetition and later repetitions reuse it without loading; `-rsrp` removes it before every repetition. See [Concepts](Concepts.md).

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
The following status shows a volume of type `shared`.
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
* Duration: 1076s 
* Code: 1794608769
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'random_page_cost', 'target': 'container'}, '1.1'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_io_concurrency', 'target': 'container'}, '200'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'io_method', 'target': 'container'}, 'io_uring'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers_per_gather', 'target': 'container'}, '2'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers', 'target': 'container'}, '4'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_worker_processes', 'target': 'container'}, '6'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'shared_buffers', 'target': 'container'}, '20GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_cache_size', 'target': 'container'}, '48GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'work_mem', 'target': 'container'}, '1GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'maintenance_work_mem', 'target': 'container'}, '2GB')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1123941
  * datadisk:5787
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
    * code:1794608769
* postgresql-1-2-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1129408
  * datadisk:5787
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
    * code:1794608769

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: PostgreSQL-1-2

### Data Parameters of Reused Volumes
* PostgreSQL-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### Ingestion
* PostgreSQL-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1794608769-5d57dd5db-qrfdc: 0
* bexhoma-sut-postgresql-1-1794608769-f6f56fff6-snlzr: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpcds (1 pods)

### Loading

#### Per Run

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    1 |       97.00 |           5.00 |            0.00 |         42.00 |           38.00 |              8 |         0 |             | None           |             0 | False         |               37.11 | False               |
| PostgreSQL-1-2 |                2 |    1 |       97.00 |           5.00 |            0.00 |         42.00 |           38.00 |              8 |         0 |             | None           |             0 | False         |               37.11 | True                |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               99 |                  99 |        168 |            0.31 |            11740.21 |           2121.43 |          -1 |
| postgresql-1-2-1-1-1 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |        1 |               1 |       1 | 1.00 |               99 |                  99 |        163 |            0.32 |            11739.08 |           2186.50 |          -1 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        168 |            0.31 |            11740.21 |           2121.43 |          -1 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        163 |            0.32 |            11739.08 |           2186.50 |          -1 |

#### Query Completion per Phase

| phase            |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:-----------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| postgresql-1-2-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   postgresql-1-1-1-1-1 |   postgresql-1-2-1-1-1 |
|:--------------|-----------------------:|-----------------------:|
| TPC-DS Q1     |                 253.34 |                 173.00 |
| TPC-DS Q2     |                 340.78 |                 418.77 |
| TPC-DS Q3     |                 102.24 |                 222.96 |
| TPC-DS Q4     |                5436.24 |                5564.68 |
| TPC-DS Q5     |                 451.50 |                 490.61 |
| TPC-DS Q6     |               50569.19 |               49048.67 |
| TPC-DS Q7     |                 304.80 |                 365.77 |
| TPC-DS Q8     |                  46.36 |                  70.60 |
| TPC-DS Q9     |                1904.54 |                1948.43 |
| TPC-DS Q10    |                 879.24 |                2344.49 |
| TPC-DS Q11    |                3303.65 |                4154.22 |
| TPC-DS Q12    |                  54.87 |                  52.33 |
| TPC-DS Q13    |                 488.00 |                 504.59 |
| TPC-DS Q14a+b |                2219.71 |                2276.03 |
| TPC-DS Q15    |                  97.31 |                 100.94 |
| TPC-DS Q16    |                 199.70 |                 203.42 |
| TPC-DS Q17    |                 274.51 |                 268.03 |
| TPC-DS Q18    |                 346.46 |                 335.66 |
| TPC-DS Q19    |                 126.51 |                 124.95 |
| TPC-DS Q20    |                  96.86 |                  84.46 |
| TPC-DS Q21    |                 239.16 |                 316.90 |
| TPC-DS Q22    |                2680.32 |                2888.61 |
| TPC-DS Q23a+b |                3259.05 |                3160.03 |
| TPC-DS Q24a+b |                 568.04 |                 564.32 |
| TPC-DS Q25    |                 256.41 |                 250.42 |
| TPC-DS Q26    |                 205.15 |                 192.61 |
| TPC-DS Q27    |                 326.84 |                 322.98 |
| TPC-DS Q28    |                1358.29 |                1329.16 |
| TPC-DS Q29    |                 274.49 |                 265.34 |
| TPC-DS Q30    |                7542.38 |                7648.03 |
| TPC-DS Q31    |                1350.10 |                1298.30 |
| TPC-DS Q32    |                 142.44 |                 158.25 |
| TPC-DS Q33    |                 319.48 |                 327.79 |
| TPC-DS Q34    |                  22.28 |                  21.68 |
| TPC-DS Q35    |                 965.95 |                 957.78 |
| TPC-DS Q36    |                 264.10 |                 264.45 |
| TPC-DS Q37    |                 328.87 |                 329.63 |
| TPC-DS Q38    |                 780.27 |                 789.30 |
| TPC-DS Q39a+b |                2087.37 |                2110.59 |
| TPC-DS Q40    |                 100.60 |                  99.11 |
| TPC-DS Q41    |                 336.16 |                 344.43 |
| TPC-DS Q42    |                  87.27 |                  84.73 |
| TPC-DS Q43    |                  20.74 |                  19.08 |
| TPC-DS Q44    |                   2.87 |                   4.92 |
| TPC-DS Q45    |                  80.13 |                  75.30 |
| TPC-DS Q46    |                  27.97 |                  28.59 |
| TPC-DS Q47    |                1224.19 |                1466.62 |
| TPC-DS Q48    |                 476.19 |                 475.64 |
| TPC-DS Q49    |                 454.94 |                 421.14 |
| TPC-DS Q50    |                 568.69 |                 365.78 |
| TPC-DS Q51    |                 708.75 |                 695.38 |
| TPC-DS Q52    |                  88.97 |                  89.85 |
| TPC-DS Q53    |                 110.45 |                 107.55 |
| TPC-DS Q54    |                  70.60 |                  64.78 |
| TPC-DS Q55    |                  86.31 |                  80.32 |
| TPC-DS Q56    |                 334.24 |                 301.61 |
| TPC-DS Q57    |                 697.07 |                 646.43 |
| TPC-DS Q58    |                 315.35 |                 332.89 |
| TPC-DS Q59    |                 418.49 |                 410.36 |
| TPC-DS Q60    |                 306.93 |                 295.25 |
| TPC-DS Q61    |                 107.81 |                 103.39 |
| TPC-DS Q62    |                  93.03 |                  93.32 |
| TPC-DS Q63    |                 113.14 |                 105.20 |
| TPC-DS Q64    |                 594.74 |                 587.50 |
| TPC-DS Q65    |                 510.95 |                 503.08 |
| TPC-DS Q66    |                 164.48 |                 172.07 |
| TPC-DS Q67    |                2622.65 |                2521.80 |
| TPC-DS Q68    |                  31.98 |                  29.08 |
| TPC-DS Q69    |                 306.46 |                 277.81 |
| TPC-DS Q70    |                 358.49 |                 427.81 |
| TPC-DS Q71    |                 268.81 |                 259.15 |
| TPC-DS Q72    |                1017.04 |                 749.64 |
| TPC-DS Q73    |                  21.87 |                  21.48 |
| TPC-DS Q74    |                 838.27 |                 772.91 |
| TPC-DS Q75    |                 625.89 |                 548.76 |
| TPC-DS Q76    |                 141.54 |                 125.52 |
| TPC-DS Q77    |                 291.96 |                 269.04 |
| TPC-DS Q78    |                1075.08 |                 933.02 |
| TPC-DS Q79    |                 166.19 |                 164.19 |
| TPC-DS Q80    |                 383.00 |                 349.12 |
| TPC-DS Q81    |               33398.43 |               32803.41 |
| TPC-DS Q82    |                 566.23 |                 351.76 |
| TPC-DS Q83    |                  73.45 |                  63.92 |
| TPC-DS Q84    |                  21.13 |                  17.67 |
| TPC-DS Q85    |                 260.28 |                 263.00 |
| TPC-DS Q86    |                 155.95 |                 169.91 |
| TPC-DS Q87    |                 832.71 |                 786.34 |
| TPC-DS Q88    |                2036.86 |                2055.24 |
| TPC-DS Q89    |                 131.43 |                 126.28 |
| TPC-DS Q90    |                 111.93 |                  93.28 |
| TPC-DS Q91    |                  90.73 |                  85.02 |
| TPC-DS Q92    |                  53.88 |                  47.00 |
| TPC-DS Q93    |                 272.54 |                 197.59 |
| TPC-DS Q94    |                 134.41 |                 126.92 |
| TPC-DS Q95    |                2518.15 |                2507.61 |
| TPC-DS Q96    |                 101.37 |                  95.76 |
| TPC-DS Q97    |                 340.42 |                 325.32 |
| TPC-DS Q98    |                 144.33 |                 250.61 |
| TPC-DS Q99    |                 164.64 |                 162.04 |

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


The loading times for both instances of loading are the same, since both relate to the same process of ingesting into the database.
Note the added section about `volume_size` and `volume_used` in the connections section.









## Profiling Benchmark

Bexhoma includes a data profiling benchmark as in [1].
> We differentiate between metric attributes (INTEGER, DOUBLE, DECIMAL) and nominal attributes (others). We seek to obtain basic statistics about the attributes and we use COUNT, COUNT NULL (missing values), COUNT DISTINCT and the distribution: MIN, MAX, truncated AVG of values (metric) or of frequencies (nominal). We query for these 6 statistics per attribute and this yields 429 profiling queries. 

In [1] the benchmark is used to assess node stability and to compare performance of DBMS and cloud providers.

[1] [Orchestrating DBMS Benchmarking in the Cloud with Kubernetes](https://doi.org/10.1007/978-3-030-94437-7_6)
> Erdelt P.K. (2022)
> Orchestrating DBMS Benchmarking in the Cloud with Kubernetes.
> In: Nambiar R., Poess M. (eds) Performance Evaluation and Benchmarking. TPCTC 2021.
> Lecture Notes in Computer Science, vol 13169. Springer, Cham.
> https://doi.org/10.1007/978-3-030-94437-7_6

This runs it at TPC-DS SF=10 in PostgreSQL:


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
  -ms $BEXHOMA_MS \
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
* Duration: 2673s 
* Code: 1794655324
* We compute for all columns: Minimum, maximum, average, count, count distinct, count NULL and non NULL entries and coefficient of variation.
* This experiment compares imported TPC-DS data sets in different DBMS.
  * TPC-DS (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'random_page_cost', 'target': 'container'}, '1.1'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_io_concurrency', 'target': 'container'}, '200'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'io_method', 'target': 'container'}, 'io_uring'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers_per_gather', 'target': 'container'}, '2'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers', 'target': 'container'}, '4'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_worker_processes', 'target': 'container'}, '6'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'shared_buffers', 'target': 'container'}, '20GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_cache_size', 'target': 'container'}, '48GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'work_mem', 'target': 'container'}, '1GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'maintenance_work_mem', 'target': 'container'}, '2GB')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1246646
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
  * eval_parameters
    * code:1794655324
* postgresql-1-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1390744
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
  * eval_parameters
    * code:1794655324

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: PostgreSQL-1

### Data Parameters of Reused Volumes
* PostgreSQL-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1794655324-59448459f9-hwd4q: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpcds (1 pods)

### Loading

#### Per Run

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |   10 |      757.00 |           2.00 |            1.00 |        447.00 |          296.00 |              0 |         0 |             | None           |             0 | False         |               47.56 | True                |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 | 10.00 |              429 |                 429 |       1515 |            0.11 |           349999.48 |          10194.06 |          -1 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       1 | 10.00 |              429 |                 429 |        695 |            0.05 |           707002.24 |          22221.58 |          -1 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |              429 |                 429 |       1515 |            0.11 |           349999.48 |          10194.06 |          -1 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        2 |               1 |           1 | 10.00 |              429 |                 429 |        695 |            0.05 |           707002.24 |          22221.58 |          -1 |

#### Query Completion per Phase

| phase            |   pods | statistics_tab about call_center.cc_call_center_sk - all   | statistics_tab about call_center.cc_call_center_id - all   | statistics_tab about call_center.cc_rec_start_date - all   | statistics_tab about call_center.cc_rec_end_date - all   | statistics_tab about call_center.cc_closed_date_sk - all   | statistics_tab about call_center.cc_open_date_sk - all   | statistics_tab about call_center.cc_name - all   | statistics_tab about call_center.cc_class - all   | statistics_tab about call_center.cc_employees - all   | statistics_tab about call_center.cc_sq_ft - all   | statistics_tab about call_center.cc_hours - all   | statistics_tab about call_center.cc_manager - all   | statistics_tab about call_center.cc_mkt_id - all   | statistics_tab about call_center.cc_mkt_class - all   | statistics_tab about call_center.cc_mkt_desc - all   | statistics_tab about call_center.cc_market_manager - all   | statistics_tab about call_center.cc_division - all   | statistics_tab about call_center.cc_division_name - all   | statistics_tab about call_center.cc_company - all   | statistics_tab about call_center.cc_company_name - all   | statistics_tab about call_center.cc_street_number - all   | statistics_tab about call_center.cc_street_name - all   | statistics_tab about call_center.cc_street_type - all   | statistics_tab about call_center.cc_suite_number - all   | statistics_tab about call_center.cc_city - all   | statistics_tab about call_center.cc_county - all   | statistics_tab about call_center.cc_state - all   | statistics_tab about call_center.cc_zip - all   | statistics_tab about call_center.cc_country - all   | statistics_tab about call_center.cc_gmt_offset - all   | statistics_tab about call_center.cc_tax_percentage - all   | statistics_tab about catalog_page.cp_catalog_page_sk - all   | statistics_tab about catalog_page.cp_catalog_page_id - all   | statistics_tab about catalog_page.cp_start_date_sk - all   | statistics_tab about catalog_page.cp_end_date_sk - all   | statistics_tab about catalog_page.cp_department - all   | statistics_tab about catalog_page.cp_catalog_number - all   | statistics_tab about catalog_page.cp_catalog_page_number - all   | statistics_tab about catalog_page.cp_description - all   | statistics_tab about catalog_page.cp_type - all   | statistics_tab about catalog_returns.cr_returned_date_sk - all   | statistics_tab about catalog_returns.cr_returned_time_sk - all   | statistics_tab about catalog_returns.cr_item_sk - all   | statistics_tab about catalog_returns.cr_refunded_customer_sk - all   | statistics_tab about catalog_returns.cr_refunded_cdemo_sk - all   | statistics_tab about catalog_returns.cr_refunded_hdemo_sk - all   | statistics_tab about catalog_returns.cr_refunded_addr_sk - all   | statistics_tab about catalog_returns.cr_returning_customer_sk - all   | statistics_tab about catalog_returns.cr_returning_cdemo_sk - all   | statistics_tab about catalog_returns.cr_returning_hdemo_sk - all   | statistics_tab about catalog_returns.cr_returning_addr_sk - all   | statistics_tab about catalog_returns.cr_call_center_sk - all   | statistics_tab about catalog_returns.cr_catalog_page_sk - all   | statistics_tab about catalog_returns.cr_ship_mode_sk - all   | statistics_tab about catalog_returns.cr_warehouse_sk - all   | statistics_tab about catalog_returns.cr_reason_sk - all   | statistics_tab about catalog_returns.cr_order_number - all   | statistics_tab about catalog_returns.cr_return_quantity - all   | statistics_tab about catalog_returns.cr_return_amount - all   | statistics_tab about catalog_returns.cr_return_tax - all   | statistics_tab about catalog_returns.cr_return_amt_inc_tax - all   | statistics_tab about catalog_returns.cr_fee - all   | statistics_tab about catalog_returns.cr_return_ship_cost - all   | statistics_tab about catalog_returns.cr_refunded_cash - all   | statistics_tab about catalog_returns.cr_reversed_charge - all   | statistics_tab about catalog_returns.cr_store_credit - all   | statistics_tab about catalog_returns.cr_net_loss - all   | statistics_tab about catalog_sales.cs_sold_date_sk - all   | statistics_tab about catalog_sales.cs_sold_time_sk - all   | statistics_tab about catalog_sales.cs_ship_date_sk - all   | statistics_tab about catalog_sales.cs_bill_customer_sk - all   | statistics_tab about catalog_sales.cs_bill_cdemo_sk - all   | statistics_tab about catalog_sales.cs_bill_hdemo_sk - all   | statistics_tab about catalog_sales.cs_bill_addr_sk - all   | statistics_tab about catalog_sales.cs_ship_customer_sk - all   | statistics_tab about catalog_sales.cs_ship_cdemo_sk - all   | statistics_tab about catalog_sales.cs_ship_hdemo_sk - all   | statistics_tab about catalog_sales.cs_ship_addr_sk - all   | statistics_tab about catalog_sales.cs_call_center_sk - all   | statistics_tab about catalog_sales.cs_catalog_page_sk - all   | statistics_tab about catalog_sales.cs_ship_mode_sk - all   | statistics_tab about catalog_sales.cs_warehouse_sk - all   | statistics_tab about catalog_sales.cs_item_sk - all   | statistics_tab about catalog_sales.cs_promo_sk - all   | statistics_tab about catalog_sales.cs_order_number - all   | statistics_tab about catalog_sales.cs_quantity - all   | statistics_tab about catalog_sales.cs_wholesale_cost - all   | statistics_tab about catalog_sales.cs_list_price - all   | statistics_tab about catalog_sales.cs_sales_price - all   | statistics_tab about catalog_sales.cs_ext_discount_amt - all   | statistics_tab about catalog_sales.cs_ext_sales_price - all   | statistics_tab about catalog_sales.cs_ext_wholesale_cost - all   | statistics_tab about catalog_sales.cs_ext_list_price - all   | statistics_tab about catalog_sales.cs_ext_tax - all   | statistics_tab about catalog_sales.cs_coupon_amt - all   | statistics_tab about catalog_sales.cs_ext_ship_cost - all   | statistics_tab about catalog_sales.cs_net_paid - all   | statistics_tab about catalog_sales.cs_net_paid_inc_tax - all   | statistics_tab about catalog_sales.cs_net_paid_inc_ship - all   | statistics_tab about catalog_sales.cs_net_paid_inc_ship_tax - all   | statistics_tab about catalog_sales.cs_net_profit - all   | statistics_tab about customer.c_customer_sk - all   | statistics_tab about customer.c_customer_id - all   | statistics_tab about customer.c_current_cdemo_sk - all   | statistics_tab about customer.c_current_hdemo_sk - all   | statistics_tab about customer.c_current_addr_sk - all   | statistics_tab about customer.c_first_shipto_date_sk - all   | statistics_tab about customer.c_first_sales_date_sk - all   | statistics_tab about customer.c_salutation - all   | statistics_tab about customer.c_first_name - all   | statistics_tab about customer.c_last_name - all   | statistics_tab about customer.c_preferred_cust_flag - all   | statistics_tab about customer.c_birth_day - all   | statistics_tab about customer.c_birth_month - all   | statistics_tab about customer.c_birth_year - all   | statistics_tab about customer.c_birth_country - all   | statistics_tab about customer.c_login - all   | statistics_tab about customer.c_email_address - all   | statistics_tab about customer.c_last_review_date - all   | statistics_tab about customer_address.ca_address_sk - all   | statistics_tab about customer_address.ca_address_id - all   | statistics_tab about customer_address.ca_street_number - all   | statistics_tab about customer_address.ca_street_name - all   | statistics_tab about customer_address.ca_street_type - all   | statistics_tab about customer_address.ca_suite_number - all   | statistics_tab about customer_address.ca_city - all   | statistics_tab about customer_address.ca_county - all   | statistics_tab about customer_address.ca_state - all   | statistics_tab about customer_address.ca_zip - all   | statistics_tab about customer_address.ca_country - all   | statistics_tab about customer_address.ca_gmt_offset - all   | statistics_tab about customer_address.ca_location_type - all   | statistics_tab about customer_demographics.cd_demo_sk - all   | statistics_tab about customer_demographics.cd_gender - all   | statistics_tab about customer_demographics.cd_marital_status - all   | statistics_tab about customer_demographics.cd_education_status - all   | statistics_tab about customer_demographics.cd_purchase_estimate - all   | statistics_tab about customer_demographics.cd_credit_rating - all   | statistics_tab about customer_demographics.cd_dep_count - all   | statistics_tab about customer_demographics.cd_dep_employed_count - all   | statistics_tab about customer_demographics.cd_dep_college_count - all   | statistics_tab about date_dim.d_date_sk - all   | statistics_tab about date_dim.d_date_id - all   | statistics_tab about date_dim.d_date - all   | statistics_tab about date_dim.d_month_seq - all   | statistics_tab about date_dim.d_week_seq - all   | statistics_tab about date_dim.d_quarter_seq - all   | statistics_tab about date_dim.d_year - all   | statistics_tab about date_dim.d_dow - all   | statistics_tab about date_dim.d_moy - all   | statistics_tab about date_dim.d_dom - all   | statistics_tab about date_dim.d_qoy - all   | statistics_tab about date_dim.d_fy_year - all   | statistics_tab about date_dim.d_fy_quarter_seq - all   | statistics_tab about date_dim.d_fy_week_seq - all   | statistics_tab about date_dim.d_day_name - all   | statistics_tab about date_dim.d_quarter_name - all   | statistics_tab about date_dim.d_holiday - all   | statistics_tab about date_dim.d_weekend - all   | statistics_tab about date_dim.d_following_holiday - all   | statistics_tab about date_dim.d_first_dom - all   | statistics_tab about date_dim.d_last_dom - all   | statistics_tab about date_dim.d_same_day_ly - all   | statistics_tab about date_dim.d_same_day_lq - all   | statistics_tab about date_dim.d_current_day - all   | statistics_tab about date_dim.d_current_week - all   | statistics_tab about date_dim.d_current_month - all   | statistics_tab about date_dim.d_current_quarter - all   | statistics_tab about date_dim.d_current_year - all   | statistics_tab about dbgen_version.dv_version - all   | statistics_tab about dbgen_version.dv_create_date - all   | statistics_tab about dbgen_version.dv_create_time - all   | statistics_tab about dbgen_version.dv_cmdline_args - all   | statistics_tab about household_demographics.hd_demo_sk - all   | statistics_tab about household_demographics.hd_income_band_sk - all   | statistics_tab about household_demographics.hd_buy_potential - all   | statistics_tab about household_demographics.hd_dep_count - all   | statistics_tab about household_demographics.hd_vehicle_count - all   | statistics_tab about income_band.ib_income_band_sk - all   | statistics_tab about income_band.ib_lower_bound - all   | statistics_tab about income_band.ib_upper_bound - all   | statistics_tab about inventory.inv_date_sk - all   | statistics_tab about inventory.inv_item_sk - all   | statistics_tab about inventory.inv_warehouse_sk - all   | statistics_tab about inventory.inv_quantity_on_hand - all   | statistics_tab about item.i_item_sk - all   | statistics_tab about item.i_item_id - all   | statistics_tab about item.i_rec_start_date - all   | statistics_tab about item.i_rec_end_date - all   | statistics_tab about item.i_item_desc - all   | statistics_tab about item.i_current_price - all   | statistics_tab about item.i_wholesale_cost - all   | statistics_tab about item.i_brand_id - all   | statistics_tab about item.i_brand - all   | statistics_tab about item.i_class_id - all   | statistics_tab about item.i_class - all   | statistics_tab about item.i_category_id - all   | statistics_tab about item.i_category - all   | statistics_tab about item.i_manufact_id - all   | statistics_tab about item.i_manufact - all   | statistics_tab about item.i_size - all   | statistics_tab about item.i_formulation - all   | statistics_tab about item.i_color - all   | statistics_tab about item.i_units - all   | statistics_tab about item.i_container - all   | statistics_tab about item.i_manager_id - all   | statistics_tab about item.i_product_name - all   | statistics_tab about promotion.p_promo_sk - all   | statistics_tab about promotion.p_promo_id - all   | statistics_tab about promotion.p_start_date_sk - all   | statistics_tab about promotion.p_end_date_sk - all   | statistics_tab about promotion.p_item_sk - all   | statistics_tab about promotion.p_cost - all   | statistics_tab about promotion.p_response_target - all   | statistics_tab about promotion.p_promo_name - all   | statistics_tab about promotion.p_channel_dmail - all   | statistics_tab about promotion.p_channel_email - all   | statistics_tab about promotion.p_channel_catalog - all   | statistics_tab about promotion.p_channel_tv - all   | statistics_tab about promotion.p_channel_radio - all   | statistics_tab about promotion.p_channel_press - all   | statistics_tab about promotion.p_channel_event - all   | statistics_tab about promotion.p_channel_demo - all   | statistics_tab about promotion.p_channel_details - all   | statistics_tab about promotion.p_purpose - all   | statistics_tab about promotion.p_discount_active - all   | statistics_tab about reason.r_reason_sk - all   | statistics_tab about reason.r_reason_id - all   | statistics_tab about reason.r_reason_desc - all   | statistics_tab about ship_mode.sm_ship_mode_sk - all   | statistics_tab about ship_mode.sm_ship_mode_id - all   | statistics_tab about ship_mode.sm_type - all   | statistics_tab about ship_mode.sm_code - all   | statistics_tab about ship_mode.sm_carrier - all   | statistics_tab about ship_mode.sm_contract - all   | statistics_tab about store.s_store_sk - all   | statistics_tab about store.s_store_id - all   | statistics_tab about store.s_rec_start_date - all   | statistics_tab about store.s_rec_end_date - all   | statistics_tab about store.s_closed_date_sk - all   | statistics_tab about store.s_store_name - all   | statistics_tab about store.s_number_employees - all   | statistics_tab about store.s_floor_space - all   | statistics_tab about store.s_hours - all   | statistics_tab about store.s_manager - all   | statistics_tab about store.s_market_id - all   | statistics_tab about store.s_geography_class - all   | statistics_tab about store.s_market_desc - all   | statistics_tab about store.s_market_manager - all   | statistics_tab about store.s_division_id - all   | statistics_tab about store.s_division_name - all   | statistics_tab about store.s_company_id - all   | statistics_tab about store.s_company_name - all   | statistics_tab about store.s_street_number - all   | statistics_tab about store.s_street_name - all   | statistics_tab about store.s_street_type - all   | statistics_tab about store.s_suite_number - all   | statistics_tab about store.s_city - all   | statistics_tab about store.s_county - all   | statistics_tab about store.s_state - all   | statistics_tab about store.s_zip - all   | statistics_tab about store.s_country - all   | statistics_tab about store.s_gmt_offset - all   | statistics_tab about store.s_tax_precentage - all   | statistics_tab about store_returns.sr_returned_date_sk - all   | statistics_tab about store_returns.sr_return_time_sk - all   | statistics_tab about store_returns.sr_item_sk - all   | statistics_tab about store_returns.sr_customer_sk - all   | statistics_tab about store_returns.sr_cdemo_sk - all   | statistics_tab about store_returns.sr_hdemo_sk - all   | statistics_tab about store_returns.sr_addr_sk - all   | statistics_tab about store_returns.sr_store_sk - all   | statistics_tab about store_returns.sr_reason_sk - all   | statistics_tab about store_returns.sr_ticket_number - all   | statistics_tab about store_returns.sr_return_quantity - all   | statistics_tab about store_returns.sr_return_amt - all   | statistics_tab about store_returns.sr_return_tax - all   | statistics_tab about store_returns.sr_return_amt_inc_tax - all   | statistics_tab about store_returns.sr_fee - all   | statistics_tab about store_returns.sr_return_ship_cost - all   | statistics_tab about store_returns.sr_refunded_cash - all   | statistics_tab about store_returns.sr_reversed_charge - all   | statistics_tab about store_returns.sr_store_credit - all   | statistics_tab about store_returns.sr_net_loss - all   | statistics_tab about store_sales.ss_sold_date_sk - all   | statistics_tab about store_sales.ss_sold_time_sk - all   | statistics_tab about store_sales.ss_item_sk - all   | statistics_tab about store_sales.ss_customer_sk - all   | statistics_tab about store_sales.ss_cdemo_sk - all   | statistics_tab about store_sales.ss_hdemo_sk - all   | statistics_tab about store_sales.ss_addr_sk - all   | statistics_tab about store_sales.ss_store_sk - all   | statistics_tab about store_sales.ss_promo_sk - all   | statistics_tab about store_sales.ss_ticket_number - all   | statistics_tab about store_sales.ss_quantity - all   | statistics_tab about store_sales.ss_wholesale_cost - all   | statistics_tab about store_sales.ss_list_price - all   | statistics_tab about store_sales.ss_sales_price - all   | statistics_tab about store_sales.ss_ext_discount_amt - all   | statistics_tab about store_sales.ss_ext_sales_price - all   | statistics_tab about store_sales.ss_ext_wholesale_cost - all   | statistics_tab about store_sales.ss_ext_list_price - all   | statistics_tab about store_sales.ss_ext_tax - all   | statistics_tab about store_sales.ss_coupon_amt - all   | statistics_tab about store_sales.ss_net_paid - all   | statistics_tab about store_sales.ss_net_paid_inc_tax - all   | statistics_tab about store_sales.ss_net_profit - all   | statistics_tab about time_dim.t_time_sk - all   | statistics_tab about time_dim.t_time_id - all   | statistics_tab about time_dim.t_time - all   | statistics_tab about time_dim.t_hour - all   | statistics_tab about time_dim.t_minute - all   | statistics_tab about time_dim.t_second - all   | statistics_tab about time_dim.t_am_pm - all   | statistics_tab about time_dim.t_shift - all   | statistics_tab about time_dim.t_sub_shift - all   | statistics_tab about time_dim.t_meal_time - all   | statistics_tab about warehouse.w_warehouse_sk - all   | statistics_tab about warehouse.w_warehouse_id - all   | statistics_tab about warehouse.w_warehouse_name - all   | statistics_tab about warehouse.w_warehouse_sq_ft - all   | statistics_tab about warehouse.w_street_number - all   | statistics_tab about warehouse.w_street_name - all   | statistics_tab about warehouse.w_street_type - all   | statistics_tab about warehouse.w_suite_number - all   | statistics_tab about warehouse.w_city - all   | statistics_tab about warehouse.w_county - all   | statistics_tab about warehouse.w_state - all   | statistics_tab about warehouse.w_zip - all   | statistics_tab about warehouse.w_country - all   | statistics_tab about warehouse.w_gmt_offset - all   | statistics_tab about web_page.wp_web_page_sk - all   | statistics_tab about web_page.wp_web_page_id - all   | statistics_tab about web_page.wp_rec_start_date - all   | statistics_tab about web_page.wp_rec_end_date - all   | statistics_tab about web_page.wp_creation_date_sk - all   | statistics_tab about web_page.wp_access_date_sk - all   | statistics_tab about web_page.wp_autogen_flag - all   | statistics_tab about web_page.wp_customer_sk - all   | statistics_tab about web_page.wp_url - all   | statistics_tab about web_page.wp_type - all   | statistics_tab about web_page.wp_char_count - all   | statistics_tab about web_page.wp_link_count - all   | statistics_tab about web_page.wp_image_count - all   | statistics_tab about web_page.wp_max_ad_count - all   | statistics_tab about web_returns.wr_returned_date_sk - all   | statistics_tab about web_returns.wr_returned_time_sk - all   | statistics_tab about web_returns.wr_item_sk - all   | statistics_tab about web_returns.wr_refunded_customer_sk - all   | statistics_tab about web_returns.wr_refunded_cdemo_sk - all   | statistics_tab about web_returns.wr_refunded_hdemo_sk - all   | statistics_tab about web_returns.wr_refunded_addr_sk - all   | statistics_tab about web_returns.wr_returning_customer_sk - all   | statistics_tab about web_returns.wr_returning_cdemo_sk - all   | statistics_tab about web_returns.wr_returning_hdemo_sk - all   | statistics_tab about web_returns.wr_returning_addr_sk - all   | statistics_tab about web_returns.wr_web_page_sk - all   | statistics_tab about web_returns.wr_reason_sk - all   | statistics_tab about web_returns.wr_order_number - all   | statistics_tab about web_returns.wr_return_quantity - all   | statistics_tab about web_returns.wr_return_amt - all   | statistics_tab about web_returns.wr_return_tax - all   | statistics_tab about web_returns.wr_return_amt_inc_tax - all   | statistics_tab about web_returns.wr_fee - all   | statistics_tab about web_returns.wr_return_ship_cost - all   | statistics_tab about web_returns.wr_refunded_cash - all   | statistics_tab about web_returns.wr_reversed_charge - all   | statistics_tab about web_returns.wr_account_credit - all   | statistics_tab about web_returns.wr_net_loss - all   | statistics_tab about web_sales.ws_sold_date_sk - all   | statistics_tab about web_sales.ws_sold_time_sk - all   | statistics_tab about web_sales.ws_ship_date_sk - all   | statistics_tab about web_sales.ws_item_sk - all   | statistics_tab about web_sales.ws_bill_customer_sk - all   | statistics_tab about web_sales.ws_bill_cdemo_sk - all   | statistics_tab about web_sales.ws_bill_hdemo_sk - all   | statistics_tab about web_sales.ws_bill_addr_sk - all   | statistics_tab about web_sales.ws_ship_customer_sk - all   | statistics_tab about web_sales.ws_ship_cdemo_sk - all   | statistics_tab about web_sales.ws_ship_hdemo_sk - all   | statistics_tab about web_sales.ws_ship_addr_sk - all   | statistics_tab about web_sales.ws_web_page_sk - all   | statistics_tab about web_sales.ws_web_site_sk - all   | statistics_tab about web_sales.ws_ship_mode_sk - all   | statistics_tab about web_sales.ws_warehouse_sk - all   | statistics_tab about web_sales.ws_promo_sk - all   | statistics_tab about web_sales.ws_order_number - all   | statistics_tab about web_sales.ws_quantity - all   | statistics_tab about web_sales.ws_wholesale_cost - all   | statistics_tab about web_sales.ws_list_price - all   | statistics_tab about web_sales.ws_sales_price - all   | statistics_tab about web_sales.ws_ext_discount_amt - all   | statistics_tab about web_sales.ws_ext_sales_price - all   | statistics_tab about web_sales.ws_ext_wholesale_cost - all   | statistics_tab about web_sales.ws_ext_list_price - all   | statistics_tab about web_sales.ws_ext_tax - all   | statistics_tab about web_sales.ws_coupon_amt - all   | statistics_tab about web_sales.ws_ext_ship_cost - all   | statistics_tab about web_sales.ws_net_paid - all   | statistics_tab about web_sales.ws_net_paid_inc_tax - all   | statistics_tab about web_sales.ws_net_paid_inc_ship - all   | statistics_tab about web_sales.ws_net_paid_inc_ship_tax - all   | statistics_tab about web_sales.ws_net_profit - all   | statistics_tab about web_site.web_site_sk - all   | statistics_tab about web_site.web_site_id - all   | statistics_tab about web_site.web_rec_start_date - all   | statistics_tab about web_site.web_rec_end_date - all   | statistics_tab about web_site.web_name - all   | statistics_tab about web_site.web_open_date_sk - all   | statistics_tab about web_site.web_close_date_sk - all   | statistics_tab about web_site.web_class - all   | statistics_tab about web_site.web_manager - all   | statistics_tab about web_site.web_mkt_id - all   | statistics_tab about web_site.web_mkt_class - all   | statistics_tab about web_site.web_mkt_desc - all   | statistics_tab about web_site.web_market_manager - all   | statistics_tab about web_site.web_company_id - all   | statistics_tab about web_site.web_company_name - all   | statistics_tab about web_site.web_street_number - all   | statistics_tab about web_site.web_street_name - all   | statistics_tab about web_site.web_street_type - all   | statistics_tab about web_site.web_suite_number - all   | statistics_tab about web_site.web_city - all   | statistics_tab about web_site.web_county - all   | statistics_tab about web_site.web_state - all   | statistics_tab about web_site.web_zip - all   | statistics_tab about web_site.web_country - all   | statistics_tab about web_site.web_gmt_offset - all   | statistics_tab about web_site.web_tax_percentage - all   | complete   |
|:-----------------|-------:|:-----------------------------------------------------------|:-----------------------------------------------------------|:-----------------------------------------------------------|:---------------------------------------------------------|:-----------------------------------------------------------|:---------------------------------------------------------|:-------------------------------------------------|:--------------------------------------------------|:------------------------------------------------------|:--------------------------------------------------|:--------------------------------------------------|:----------------------------------------------------|:---------------------------------------------------|:------------------------------------------------------|:-----------------------------------------------------|:-----------------------------------------------------------|:-----------------------------------------------------|:----------------------------------------------------------|:----------------------------------------------------|:---------------------------------------------------------|:----------------------------------------------------------|:--------------------------------------------------------|:--------------------------------------------------------|:---------------------------------------------------------|:-------------------------------------------------|:---------------------------------------------------|:--------------------------------------------------|:------------------------------------------------|:----------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------------------------|:-------------------------------------------------------------|:-------------------------------------------------------------|:-----------------------------------------------------------|:---------------------------------------------------------|:--------------------------------------------------------|:------------------------------------------------------------|:-----------------------------------------------------------------|:---------------------------------------------------------|:--------------------------------------------------|:-----------------------------------------------------------------|:-----------------------------------------------------------------|:--------------------------------------------------------|:---------------------------------------------------------------------|:------------------------------------------------------------------|:------------------------------------------------------------------|:-----------------------------------------------------------------|:----------------------------------------------------------------------|:-------------------------------------------------------------------|:-------------------------------------------------------------------|:------------------------------------------------------------------|:---------------------------------------------------------------|:----------------------------------------------------------------|:-------------------------------------------------------------|:-------------------------------------------------------------|:----------------------------------------------------------|:-------------------------------------------------------------|:----------------------------------------------------------------|:--------------------------------------------------------------|:-----------------------------------------------------------|:-------------------------------------------------------------------|:----------------------------------------------------|:-----------------------------------------------------------------|:--------------------------------------------------------------|:----------------------------------------------------------------|:-------------------------------------------------------------|:---------------------------------------------------------|:-----------------------------------------------------------|:-----------------------------------------------------------|:-----------------------------------------------------------|:---------------------------------------------------------------|:------------------------------------------------------------|:------------------------------------------------------------|:-----------------------------------------------------------|:---------------------------------------------------------------|:------------------------------------------------------------|:------------------------------------------------------------|:-----------------------------------------------------------|:-------------------------------------------------------------|:--------------------------------------------------------------|:-----------------------------------------------------------|:-----------------------------------------------------------|:------------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------------|:---------------------------------------------------------|:----------------------------------------------------------|:---------------------------------------------------------------|:--------------------------------------------------------------|:-----------------------------------------------------------------|:-------------------------------------------------------------|:------------------------------------------------------|:---------------------------------------------------------|:------------------------------------------------------------|:-------------------------------------------------------|:---------------------------------------------------------------|:----------------------------------------------------------------|:--------------------------------------------------------------------|:---------------------------------------------------------|:----------------------------------------------------|:----------------------------------------------------|:---------------------------------------------------------|:---------------------------------------------------------|:--------------------------------------------------------|:-------------------------------------------------------------|:------------------------------------------------------------|:---------------------------------------------------|:---------------------------------------------------|:--------------------------------------------------|:------------------------------------------------------------|:--------------------------------------------------|:----------------------------------------------------|:---------------------------------------------------|:------------------------------------------------------|:----------------------------------------------|:------------------------------------------------------|:---------------------------------------------------------|:------------------------------------------------------------|:------------------------------------------------------------|:---------------------------------------------------------------|:-------------------------------------------------------------|:-------------------------------------------------------------|:--------------------------------------------------------------|:------------------------------------------------------|:--------------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------------------|:---------------------------------------------------------|:------------------------------------------------------------|:---------------------------------------------------------------|:--------------------------------------------------------------|:-------------------------------------------------------------|:---------------------------------------------------------------------|:-----------------------------------------------------------------------|:------------------------------------------------------------------------|:--------------------------------------------------------------------|:----------------------------------------------------------------|:-------------------------------------------------------------------------|:------------------------------------------------------------------------|:------------------------------------------------|:------------------------------------------------|:---------------------------------------------|:--------------------------------------------------|:-------------------------------------------------|:----------------------------------------------------|:---------------------------------------------|:--------------------------------------------|:--------------------------------------------|:--------------------------------------------|:--------------------------------------------|:------------------------------------------------|:-------------------------------------------------------|:----------------------------------------------------|:-------------------------------------------------|:-----------------------------------------------------|:------------------------------------------------|:------------------------------------------------|:----------------------------------------------------------|:--------------------------------------------------|:-------------------------------------------------|:----------------------------------------------------|:----------------------------------------------------|:----------------------------------------------------|:-----------------------------------------------------|:------------------------------------------------------|:--------------------------------------------------------|:-----------------------------------------------------|:------------------------------------------------------|:----------------------------------------------------------|:----------------------------------------------------------|:-----------------------------------------------------------|:---------------------------------------------------------------|:----------------------------------------------------------------------|:---------------------------------------------------------------------|:-----------------------------------------------------------------|:---------------------------------------------------------------------|:-----------------------------------------------------------|:--------------------------------------------------------|:--------------------------------------------------------|:---------------------------------------------------|:---------------------------------------------------|:--------------------------------------------------------|:------------------------------------------------------------|:--------------------------------------------|:--------------------------------------------|:---------------------------------------------------|:-------------------------------------------------|:----------------------------------------------|:--------------------------------------------------|:---------------------------------------------------|:---------------------------------------------|:------------------------------------------|:---------------------------------------------|:------------------------------------------|:------------------------------------------------|:---------------------------------------------|:------------------------------------------------|:---------------------------------------------|:-----------------------------------------|:------------------------------------------------|:------------------------------------------|:------------------------------------------|:----------------------------------------------|:-----------------------------------------------|:-------------------------------------------------|:--------------------------------------------------|:--------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------------------|:-------------------------------------------------|:----------------------------------------------|:---------------------------------------------------------|:----------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------|:---------------------------------------------------------|:----------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------|:------------------------------------------------------|:---------------------------------------------------------|:-------------------------------------------------|:---------------------------------------------------------|:------------------------------------------------|:------------------------------------------------|:--------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------------|:-----------------------------------------------|:--------------------------------------------------|:---------------------------------------------------|:----------------------------------------------|:----------------------------------------------|:----------------------------------------------------|:--------------------------------------------------|:----------------------------------------------------|:------------------------------------------------|:------------------------------------------------------|:-------------------------------------------------|:-------------------------------------------|:---------------------------------------------|:-----------------------------------------------|:-----------------------------------------------------|:-------------------------------------------------|:----------------------------------------------------|:-------------------------------------------------|:---------------------------------------------------|:------------------------------------------------|:--------------------------------------------------|:---------------------------------------------------|:-------------------------------------------------|:-------------------------------------------------|:--------------------------------------------------|:------------------------------------------|:--------------------------------------------|:-------------------------------------------|:-----------------------------------------|:---------------------------------------------|:------------------------------------------------|:----------------------------------------------------|:---------------------------------------------------------------|:-------------------------------------------------------------|:------------------------------------------------------|:----------------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------|:------------------------------------------------------|:-------------------------------------------------------|:--------------------------------------------------------|:------------------------------------------------------------|:--------------------------------------------------------------|:---------------------------------------------------------|:---------------------------------------------------------|:-----------------------------------------------------------------|:--------------------------------------------------|:---------------------------------------------------------------|:------------------------------------------------------------|:--------------------------------------------------------------|:-----------------------------------------------------------|:-------------------------------------------------------|:---------------------------------------------------------|:---------------------------------------------------------|:----------------------------------------------------|:--------------------------------------------------------|:-----------------------------------------------------|:-----------------------------------------------------|:----------------------------------------------------|:-----------------------------------------------------|:-----------------------------------------------------|:----------------------------------------------------------|:-----------------------------------------------------|:-----------------------------------------------------------|:-------------------------------------------------------|:--------------------------------------------------------|:-------------------------------------------------------------|:------------------------------------------------------------|:---------------------------------------------------------------|:-----------------------------------------------------------|:----------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------------------|:-------------------------------------------------------------|:-------------------------------------------------------|:------------------------------------------------|:------------------------------------------------|:---------------------------------------------|:---------------------------------------------|:-----------------------------------------------|:-----------------------------------------------|:----------------------------------------------|:----------------------------------------------|:--------------------------------------------------|:--------------------------------------------------|:------------------------------------------------------|:------------------------------------------------------|:--------------------------------------------------------|:---------------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------------------|:-----------------------------------------------------|:------------------------------------------------------|:----------------------------------------------|:------------------------------------------------|:-----------------------------------------------|:---------------------------------------------|:-------------------------------------------------|:----------------------------------------------------|:-----------------------------------------------------|:-----------------------------------------------------|:--------------------------------------------------------|:------------------------------------------------------|:----------------------------------------------------------|:--------------------------------------------------------|:------------------------------------------------------|:-----------------------------------------------------|:---------------------------------------------|:----------------------------------------------|:----------------------------------------------------|:----------------------------------------------------|:-----------------------------------------------------|:------------------------------------------------------|:-------------------------------------------------------------|:-------------------------------------------------------------|:----------------------------------------------------|:-----------------------------------------------------------------|:--------------------------------------------------------------|:--------------------------------------------------------------|:-------------------------------------------------------------|:------------------------------------------------------------------|:---------------------------------------------------------------|:---------------------------------------------------------------|:--------------------------------------------------------------|:--------------------------------------------------------|:------------------------------------------------------|:---------------------------------------------------------|:------------------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------|:---------------------------------------------------------------|:------------------------------------------------|:-------------------------------------------------------------|:----------------------------------------------------------|:------------------------------------------------------------|:-----------------------------------------------------------|:-----------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------|:--------------------------------------------------|:-----------------------------------------------------------|:--------------------------------------------------------|:--------------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------------------------|:--------------------------------------------------------|:--------------------------------------------------------|:-------------------------------------------------------|:------------------------------------------------------|:------------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------|:---------------------------------------------------|:-------------------------------------------------------|:---------------------------------------------------|:---------------------------------------------------------|:-----------------------------------------------------|:------------------------------------------------------|:-----------------------------------------------------------|:----------------------------------------------------------|:-------------------------------------------------------------|:---------------------------------------------------------|:--------------------------------------------------|:-----------------------------------------------------|:--------------------------------------------------------|:---------------------------------------------------|:-----------------------------------------------------------|:------------------------------------------------------------|:----------------------------------------------------------------|:-----------------------------------------------------|:--------------------------------------------------|:--------------------------------------------------|:---------------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------------|:-------------------------------------------------------|:--------------------------------------------------------|:------------------------------------------------|:--------------------------------------------------|:-------------------------------------------------|:----------------------------------------------------|:---------------------------------------------------|:---------------------------------------------------------|:-----------------------------------------------------|:-------------------------------------------------------|:--------------------------------------------------------|:------------------------------------------------------|:------------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------------|:-------------------------------------------------|:------------------------------------------------|:----------------------------------------------|:--------------------------------------------------|:-----------------------------------------------------|:---------------------------------------------------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1                                                        | 1/1                                                        | 1/1                                                        | 1/1                                                      | 1/1                                                        | 1/1                                                      | 1/1                                              | 1/1                                               | 1/1                                                   | 1/1                                               | 1/1                                               | 1/1                                                 | 1/1                                                | 1/1                                                   | 1/1                                                  | 1/1                                                        | 1/1                                                  | 1/1                                                       | 1/1                                                 | 1/1                                                      | 1/1                                                       | 1/1                                                     | 1/1                                                     | 1/1                                                      | 1/1                                              | 1/1                                                | 1/1                                               | 1/1                                             | 1/1                                                 | 1/1                                                    | 1/1                                                        | 1/1                                                          | 1/1                                                          | 1/1                                                        | 1/1                                                      | 1/1                                                     | 1/1                                                         | 1/1                                                              | 1/1                                                      | 1/1                                               | 1/1                                                              | 1/1                                                              | 1/1                                                     | 1/1                                                                  | 1/1                                                               | 1/1                                                               | 1/1                                                              | 1/1                                                                   | 1/1                                                                | 1/1                                                                | 1/1                                                               | 1/1                                                            | 1/1                                                             | 1/1                                                          | 1/1                                                          | 1/1                                                       | 1/1                                                          | 1/1                                                             | 1/1                                                           | 1/1                                                        | 1/1                                                                | 1/1                                                 | 1/1                                                              | 1/1                                                           | 1/1                                                             | 1/1                                                          | 1/1                                                      | 1/1                                                        | 1/1                                                        | 1/1                                                        | 1/1                                                            | 1/1                                                         | 1/1                                                         | 1/1                                                        | 1/1                                                            | 1/1                                                         | 1/1                                                         | 1/1                                                        | 1/1                                                          | 1/1                                                           | 1/1                                                        | 1/1                                                        | 1/1                                                   | 1/1                                                    | 1/1                                                        | 1/1                                                    | 1/1                                                          | 1/1                                                      | 1/1                                                       | 1/1                                                            | 1/1                                                           | 1/1                                                              | 1/1                                                          | 1/1                                                   | 1/1                                                      | 1/1                                                         | 1/1                                                    | 1/1                                                            | 1/1                                                             | 1/1                                                                 | 1/1                                                      | 1/1                                                 | 1/1                                                 | 1/1                                                      | 1/1                                                      | 1/1                                                     | 1/1                                                          | 1/1                                                         | 1/1                                                | 1/1                                                | 1/1                                               | 1/1                                                         | 1/1                                               | 1/1                                                 | 1/1                                                | 1/1                                                   | 1/1                                           | 1/1                                                   | 1/1                                                      | 1/1                                                         | 1/1                                                         | 1/1                                                            | 1/1                                                          | 1/1                                                          | 1/1                                                           | 1/1                                                   | 1/1                                                     | 1/1                                                    | 1/1                                                  | 1/1                                                      | 1/1                                                         | 1/1                                                            | 1/1                                                           | 1/1                                                          | 1/1                                                                  | 1/1                                                                    | 1/1                                                                     | 1/1                                                                 | 1/1                                                             | 1/1                                                                      | 1/1                                                                     | 1/1                                             | 1/1                                             | 1/1                                          | 1/1                                               | 1/1                                              | 1/1                                                 | 1/1                                          | 1/1                                         | 1/1                                         | 1/1                                         | 1/1                                         | 1/1                                             | 1/1                                                    | 1/1                                                 | 1/1                                              | 1/1                                                  | 1/1                                             | 1/1                                             | 1/1                                                       | 1/1                                               | 1/1                                              | 1/1                                                 | 1/1                                                 | 1/1                                                 | 1/1                                                  | 1/1                                                   | 1/1                                                     | 1/1                                                  | 1/1                                                   | 1/1                                                       | 1/1                                                       | 1/1                                                        | 1/1                                                            | 1/1                                                                   | 1/1                                                                  | 1/1                                                              | 1/1                                                                  | 1/1                                                        | 1/1                                                     | 1/1                                                     | 1/1                                                | 1/1                                                | 1/1                                                     | 1/1                                                         | 1/1                                         | 1/1                                         | 1/1                                                | 1/1                                              | 1/1                                           | 1/1                                               | 1/1                                                | 1/1                                          | 1/1                                       | 1/1                                          | 1/1                                       | 1/1                                             | 1/1                                          | 1/1                                             | 1/1                                          | 1/1                                      | 1/1                                             | 1/1                                       | 1/1                                       | 1/1                                           | 1/1                                            | 1/1                                              | 1/1                                               | 1/1                                               | 1/1                                                    | 1/1                                                  | 1/1                                              | 1/1                                           | 1/1                                                      | 1/1                                                 | 1/1                                                    | 1/1                                                    | 1/1                                                      | 1/1                                                 | 1/1                                                    | 1/1                                                    | 1/1                                                    | 1/1                                                   | 1/1                                                      | 1/1                                              | 1/1                                                      | 1/1                                             | 1/1                                             | 1/1                                               | 1/1                                                    | 1/1                                                    | 1/1                                            | 1/1                                            | 1/1                                               | 1/1                                                | 1/1                                           | 1/1                                           | 1/1                                                 | 1/1                                               | 1/1                                                 | 1/1                                             | 1/1                                                   | 1/1                                              | 1/1                                        | 1/1                                          | 1/1                                            | 1/1                                                  | 1/1                                              | 1/1                                                 | 1/1                                              | 1/1                                                | 1/1                                             | 1/1                                               | 1/1                                                | 1/1                                              | 1/1                                              | 1/1                                               | 1/1                                       | 1/1                                         | 1/1                                        | 1/1                                      | 1/1                                          | 1/1                                             | 1/1                                                 | 1/1                                                            | 1/1                                                          | 1/1                                                   | 1/1                                                       | 1/1                                                    | 1/1                                                    | 1/1                                                   | 1/1                                                    | 1/1                                                     | 1/1                                                         | 1/1                                                           | 1/1                                                      | 1/1                                                      | 1/1                                                              | 1/1                                               | 1/1                                                            | 1/1                                                         | 1/1                                                           | 1/1                                                        | 1/1                                                    | 1/1                                                      | 1/1                                                      | 1/1                                                 | 1/1                                                     | 1/1                                                  | 1/1                                                  | 1/1                                                 | 1/1                                                  | 1/1                                                  | 1/1                                                       | 1/1                                                  | 1/1                                                        | 1/1                                                    | 1/1                                                     | 1/1                                                          | 1/1                                                         | 1/1                                                            | 1/1                                                        | 1/1                                                 | 1/1                                                    | 1/1                                                  | 1/1                                                          | 1/1                                                    | 1/1                                             | 1/1                                             | 1/1                                          | 1/1                                          | 1/1                                            | 1/1                                            | 1/1                                           | 1/1                                           | 1/1                                               | 1/1                                               | 1/1                                                   | 1/1                                                   | 1/1                                                     | 1/1                                                      | 1/1                                                    | 1/1                                                  | 1/1                                                  | 1/1                                                   | 1/1                                           | 1/1                                             | 1/1                                            | 1/1                                          | 1/1                                              | 1/1                                                 | 1/1                                                  | 1/1                                                  | 1/1                                                     | 1/1                                                   | 1/1                                                       | 1/1                                                     | 1/1                                                   | 1/1                                                  | 1/1                                          | 1/1                                           | 1/1                                                 | 1/1                                                 | 1/1                                                  | 1/1                                                   | 1/1                                                          | 1/1                                                          | 1/1                                                 | 1/1                                                              | 1/1                                                           | 1/1                                                           | 1/1                                                          | 1/1                                                               | 1/1                                                            | 1/1                                                            | 1/1                                                           | 1/1                                                     | 1/1                                                   | 1/1                                                      | 1/1                                                         | 1/1                                                    | 1/1                                                    | 1/1                                                            | 1/1                                             | 1/1                                                          | 1/1                                                       | 1/1                                                         | 1/1                                                        | 1/1                                                  | 1/1                                                    | 1/1                                                    | 1/1                                                    | 1/1                                               | 1/1                                                        | 1/1                                                     | 1/1                                                     | 1/1                                                    | 1/1                                                        | 1/1                                                     | 1/1                                                     | 1/1                                                    | 1/1                                                   | 1/1                                                   | 1/1                                                    | 1/1                                                    | 1/1                                                | 1/1                                                    | 1/1                                                | 1/1                                                      | 1/1                                                  | 1/1                                                   | 1/1                                                        | 1/1                                                       | 1/1                                                          | 1/1                                                      | 1/1                                               | 1/1                                                  | 1/1                                                     | 1/1                                                | 1/1                                                        | 1/1                                                         | 1/1                                                             | 1/1                                                  | 1/1                                               | 1/1                                               | 1/1                                                      | 1/1                                                    | 1/1                                            | 1/1                                                    | 1/1                                                     | 1/1                                             | 1/1                                               | 1/1                                              | 1/1                                                 | 1/1                                                | 1/1                                                      | 1/1                                                  | 1/1                                                    | 1/1                                                     | 1/1                                                   | 1/1                                                   | 1/1                                                    | 1/1                                            | 1/1                                              | 1/1                                             | 1/1                                           | 1/1                                               | 1/1                                                  | 1/1                                                      | yes        |
| postgresql-1-1-2 |      1 | 1/1                                                        | 1/1                                                        | 1/1                                                        | 1/1                                                      | 1/1                                                        | 1/1                                                      | 1/1                                              | 1/1                                               | 1/1                                                   | 1/1                                               | 1/1                                               | 1/1                                                 | 1/1                                                | 1/1                                                   | 1/1                                                  | 1/1                                                        | 1/1                                                  | 1/1                                                       | 1/1                                                 | 1/1                                                      | 1/1                                                       | 1/1                                                     | 1/1                                                     | 1/1                                                      | 1/1                                              | 1/1                                                | 1/1                                               | 1/1                                             | 1/1                                                 | 1/1                                                    | 1/1                                                        | 1/1                                                          | 1/1                                                          | 1/1                                                        | 1/1                                                      | 1/1                                                     | 1/1                                                         | 1/1                                                              | 1/1                                                      | 1/1                                               | 1/1                                                              | 1/1                                                              | 1/1                                                     | 1/1                                                                  | 1/1                                                               | 1/1                                                               | 1/1                                                              | 1/1                                                                   | 1/1                                                                | 1/1                                                                | 1/1                                                               | 1/1                                                            | 1/1                                                             | 1/1                                                          | 1/1                                                          | 1/1                                                       | 1/1                                                          | 1/1                                                             | 1/1                                                           | 1/1                                                        | 1/1                                                                | 1/1                                                 | 1/1                                                              | 1/1                                                           | 1/1                                                             | 1/1                                                          | 1/1                                                      | 1/1                                                        | 1/1                                                        | 1/1                                                        | 1/1                                                            | 1/1                                                         | 1/1                                                         | 1/1                                                        | 1/1                                                            | 1/1                                                         | 1/1                                                         | 1/1                                                        | 1/1                                                          | 1/1                                                           | 1/1                                                        | 1/1                                                        | 1/1                                                   | 1/1                                                    | 1/1                                                        | 1/1                                                    | 1/1                                                          | 1/1                                                      | 1/1                                                       | 1/1                                                            | 1/1                                                           | 1/1                                                              | 1/1                                                          | 1/1                                                   | 1/1                                                      | 1/1                                                         | 1/1                                                    | 1/1                                                            | 1/1                                                             | 1/1                                                                 | 1/1                                                      | 1/1                                                 | 1/1                                                 | 1/1                                                      | 1/1                                                      | 1/1                                                     | 1/1                                                          | 1/1                                                         | 1/1                                                | 1/1                                                | 1/1                                               | 1/1                                                         | 1/1                                               | 1/1                                                 | 1/1                                                | 1/1                                                   | 1/1                                           | 1/1                                                   | 1/1                                                      | 1/1                                                         | 1/1                                                         | 1/1                                                            | 1/1                                                          | 1/1                                                          | 1/1                                                           | 1/1                                                   | 1/1                                                     | 1/1                                                    | 1/1                                                  | 1/1                                                      | 1/1                                                         | 1/1                                                            | 1/1                                                           | 1/1                                                          | 1/1                                                                  | 1/1                                                                    | 1/1                                                                     | 1/1                                                                 | 1/1                                                             | 1/1                                                                      | 1/1                                                                     | 1/1                                             | 1/1                                             | 1/1                                          | 1/1                                               | 1/1                                              | 1/1                                                 | 1/1                                          | 1/1                                         | 1/1                                         | 1/1                                         | 1/1                                         | 1/1                                             | 1/1                                                    | 1/1                                                 | 1/1                                              | 1/1                                                  | 1/1                                             | 1/1                                             | 1/1                                                       | 1/1                                               | 1/1                                              | 1/1                                                 | 1/1                                                 | 1/1                                                 | 1/1                                                  | 1/1                                                   | 1/1                                                     | 1/1                                                  | 1/1                                                   | 1/1                                                       | 1/1                                                       | 1/1                                                        | 1/1                                                            | 1/1                                                                   | 1/1                                                                  | 1/1                                                              | 1/1                                                                  | 1/1                                                        | 1/1                                                     | 1/1                                                     | 1/1                                                | 1/1                                                | 1/1                                                     | 1/1                                                         | 1/1                                         | 1/1                                         | 1/1                                                | 1/1                                              | 1/1                                           | 1/1                                               | 1/1                                                | 1/1                                          | 1/1                                       | 1/1                                          | 1/1                                       | 1/1                                             | 1/1                                          | 1/1                                             | 1/1                                          | 1/1                                      | 1/1                                             | 1/1                                       | 1/1                                       | 1/1                                           | 1/1                                            | 1/1                                              | 1/1                                               | 1/1                                               | 1/1                                                    | 1/1                                                  | 1/1                                              | 1/1                                           | 1/1                                                      | 1/1                                                 | 1/1                                                    | 1/1                                                    | 1/1                                                      | 1/1                                                 | 1/1                                                    | 1/1                                                    | 1/1                                                    | 1/1                                                   | 1/1                                                      | 1/1                                              | 1/1                                                      | 1/1                                             | 1/1                                             | 1/1                                               | 1/1                                                    | 1/1                                                    | 1/1                                            | 1/1                                            | 1/1                                               | 1/1                                                | 1/1                                           | 1/1                                           | 1/1                                                 | 1/1                                               | 1/1                                                 | 1/1                                             | 1/1                                                   | 1/1                                              | 1/1                                        | 1/1                                          | 1/1                                            | 1/1                                                  | 1/1                                              | 1/1                                                 | 1/1                                              | 1/1                                                | 1/1                                             | 1/1                                               | 1/1                                                | 1/1                                              | 1/1                                              | 1/1                                               | 1/1                                       | 1/1                                         | 1/1                                        | 1/1                                      | 1/1                                          | 1/1                                             | 1/1                                                 | 1/1                                                            | 1/1                                                          | 1/1                                                   | 1/1                                                       | 1/1                                                    | 1/1                                                    | 1/1                                                   | 1/1                                                    | 1/1                                                     | 1/1                                                         | 1/1                                                           | 1/1                                                      | 1/1                                                      | 1/1                                                              | 1/1                                               | 1/1                                                            | 1/1                                                         | 1/1                                                           | 1/1                                                        | 1/1                                                    | 1/1                                                      | 1/1                                                      | 1/1                                                 | 1/1                                                     | 1/1                                                  | 1/1                                                  | 1/1                                                 | 1/1                                                  | 1/1                                                  | 1/1                                                       | 1/1                                                  | 1/1                                                        | 1/1                                                    | 1/1                                                     | 1/1                                                          | 1/1                                                         | 1/1                                                            | 1/1                                                        | 1/1                                                 | 1/1                                                    | 1/1                                                  | 1/1                                                          | 1/1                                                    | 1/1                                             | 1/1                                             | 1/1                                          | 1/1                                          | 1/1                                            | 1/1                                            | 1/1                                           | 1/1                                           | 1/1                                               | 1/1                                               | 1/1                                                   | 1/1                                                   | 1/1                                                     | 1/1                                                      | 1/1                                                    | 1/1                                                  | 1/1                                                  | 1/1                                                   | 1/1                                           | 1/1                                             | 1/1                                            | 1/1                                          | 1/1                                              | 1/1                                                 | 1/1                                                  | 1/1                                                  | 1/1                                                     | 1/1                                                   | 1/1                                                       | 1/1                                                     | 1/1                                                   | 1/1                                                  | 1/1                                          | 1/1                                           | 1/1                                                 | 1/1                                                 | 1/1                                                  | 1/1                                                   | 1/1                                                          | 1/1                                                          | 1/1                                                 | 1/1                                                              | 1/1                                                           | 1/1                                                           | 1/1                                                          | 1/1                                                               | 1/1                                                            | 1/1                                                            | 1/1                                                           | 1/1                                                     | 1/1                                                   | 1/1                                                      | 1/1                                                         | 1/1                                                    | 1/1                                                    | 1/1                                                            | 1/1                                             | 1/1                                                          | 1/1                                                       | 1/1                                                         | 1/1                                                        | 1/1                                                  | 1/1                                                    | 1/1                                                    | 1/1                                                    | 1/1                                               | 1/1                                                        | 1/1                                                     | 1/1                                                     | 1/1                                                    | 1/1                                                        | 1/1                                                     | 1/1                                                     | 1/1                                                    | 1/1                                                   | 1/1                                                   | 1/1                                                    | 1/1                                                    | 1/1                                                | 1/1                                                    | 1/1                                                | 1/1                                                      | 1/1                                                  | 1/1                                                   | 1/1                                                        | 1/1                                                       | 1/1                                                          | 1/1                                                      | 1/1                                               | 1/1                                                  | 1/1                                                     | 1/1                                                | 1/1                                                        | 1/1                                                         | 1/1                                                             | 1/1                                                  | 1/1                                               | 1/1                                               | 1/1                                                      | 1/1                                                    | 1/1                                            | 1/1                                                    | 1/1                                                     | 1/1                                             | 1/1                                               | 1/1                                              | 1/1                                                 | 1/1                                                | 1/1                                                      | 1/1                                                  | 1/1                                                    | 1/1                                                     | 1/1                                                   | 1/1                                                   | 1/1                                                    | 1/1                                            | 1/1                                              | 1/1                                             | 1/1                                           | 1/1                                               | 1/1                                                  | 1/1                                                      | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                                                |   postgresql-1-1-1-1-1 |   postgresql-1-1-2-1-1 |
|:-----------------------------------------------------------------------|-----------------------:|-----------------------:|
| statistics_tab about call_center.cc_call_center_sk - all               |                 199.01 |                  35.38 |
| statistics_tab about call_center.cc_call_center_id - all               |                   4.06 |                   2.33 |
| statistics_tab about call_center.cc_rec_start_date - all               |                   1.56 |                   1.93 |
| statistics_tab about call_center.cc_rec_end_date - all                 |                   1.21 |                   1.19 |
| statistics_tab about call_center.cc_closed_date_sk - all               |                   1.02 |                   1.91 |
| statistics_tab about call_center.cc_open_date_sk - all                 |                   0.87 |                   6.49 |
| statistics_tab about call_center.cc_name - all                         |                   1.37 |                   2.16 |
| statistics_tab about call_center.cc_class - all                        |                   1.33 |                   2.05 |
| statistics_tab about call_center.cc_employees - all                    |                   1.69 |                   1.79 |
| statistics_tab about call_center.cc_sq_ft - all                        |                   1.05 |                   1.92 |
| statistics_tab about call_center.cc_hours - all                        |                   1.21 |                   2.30 |
| statistics_tab about call_center.cc_manager - all                      |                   1.25 |                   2.04 |
| statistics_tab about call_center.cc_mkt_id - all                       |                   0.95 |                   1.84 |
| statistics_tab about call_center.cc_mkt_class - all                    |                   1.40 |                   2.12 |
| statistics_tab about call_center.cc_mkt_desc - all                     |                   2.46 |                   1.99 |
| statistics_tab about call_center.cc_market_manager - all               |                   1.06 |                   2.03 |
| statistics_tab about call_center.cc_division - all                     |                   0.73 |                   1.46 |
| statistics_tab about call_center.cc_division_name - all                |                   0.89 |                   1.78 |
| statistics_tab about call_center.cc_company - all                      |                   0.78 |                   1.49 |
| statistics_tab about call_center.cc_company_name - all                 |                   1.13 |                   2.11 |
| statistics_tab about call_center.cc_street_number - all                |                   1.26 |                   1.85 |
| statistics_tab about call_center.cc_street_name - all                  |                   1.15 |                   2.10 |
| statistics_tab about call_center.cc_street_type - all                  |                   1.01 |                   2.23 |
| statistics_tab about call_center.cc_suite_number - all                 |                   1.28 |                   1.90 |
| statistics_tab about call_center.cc_city - all                         |                   1.10 |                   1.99 |
| statistics_tab about call_center.cc_county - all                       |                   1.05 |                   1.85 |
| statistics_tab about call_center.cc_state - all                        |                   0.81 |                   1.90 |
| statistics_tab about call_center.cc_zip - all                          |                   0.89 |                   2.21 |
| statistics_tab about call_center.cc_country - all                      |                   0.94 |                   2.12 |
| statistics_tab about call_center.cc_gmt_offset - all                   |                   2.15 |                   2.01 |
| statistics_tab about call_center.cc_tax_percentage - all               |                   1.25 |                   1.65 |
| statistics_tab about catalog_page.cp_catalog_page_sk - all             |                  17.34 |                   7.38 |
| statistics_tab about catalog_page.cp_catalog_page_id - all             |                  14.60 |                  13.37 |
| statistics_tab about catalog_page.cp_start_date_sk - all               |                   3.28 |                   3.68 |
| statistics_tab about catalog_page.cp_end_date_sk - all                 |                   3.39 |                   4.34 |
| statistics_tab about catalog_page.cp_department - all                  |                   4.47 |                   4.10 |
| statistics_tab about catalog_page.cp_catalog_number - all              |                   3.44 |                   3.26 |
| statistics_tab about catalog_page.cp_catalog_page_number - all         |                   3.24 |                   3.42 |
| statistics_tab about catalog_page.cp_description - all                 |                  17.31 |                  13.62 |
| statistics_tab about catalog_page.cp_type - all                        |                   4.46 |                   6.33 |
| statistics_tab about catalog_returns.cr_returned_date_sk - all         |                8589.82 |                 772.54 |
| statistics_tab about catalog_returns.cr_returned_time_sk - all         |                 319.31 |                 309.91 |
| statistics_tab about catalog_returns.cr_item_sk - all                  |                 864.25 |                 832.51 |
| statistics_tab about catalog_returns.cr_refunded_customer_sk - all     |                 321.73 |                 318.67 |
| statistics_tab about catalog_returns.cr_refunded_cdemo_sk - all        |                 317.38 |                 514.92 |
| statistics_tab about catalog_returns.cr_refunded_hdemo_sk - all        |                 268.18 |                 689.83 |
| statistics_tab about catalog_returns.cr_refunded_addr_sk - all         |                 314.80 |                 457.87 |
| statistics_tab about catalog_returns.cr_returning_customer_sk - all    |                 880.36 |                 824.91 |
| statistics_tab about catalog_returns.cr_returning_cdemo_sk - all       |                 330.97 |                 329.51 |
| statistics_tab about catalog_returns.cr_returning_hdemo_sk - all       |                 275.41 |                 273.49 |
| statistics_tab about catalog_returns.cr_returning_addr_sk - all        |                 316.72 |                 316.47 |
| statistics_tab about catalog_returns.cr_call_center_sk - all           |                 269.80 |                 265.74 |
| statistics_tab about catalog_returns.cr_catalog_page_sk - all          |                 268.23 |                 273.84 |
| statistics_tab about catalog_returns.cr_ship_mode_sk - all             |                 274.63 |                 671.18 |
| statistics_tab about catalog_returns.cr_warehouse_sk - all             |                 460.20 |                 886.23 |
| statistics_tab about catalog_returns.cr_reason_sk - all                |                 283.71 |                 278.18 |
| statistics_tab about catalog_returns.cr_order_number - all             |                 413.40 |                 307.08 |
| statistics_tab about catalog_returns.cr_return_quantity - all          |                 282.98 |                 275.30 |
| statistics_tab about catalog_returns.cr_return_amount - all            |                 494.55 |                 493.10 |
| statistics_tab about catalog_returns.cr_return_tax - all               |                 461.92 |                 519.20 |
| statistics_tab about catalog_returns.cr_return_amt_inc_tax - all       |                 511.29 |                 651.29 |
| statistics_tab about catalog_returns.cr_fee - all                      |                 529.10 |                 461.71 |
| statistics_tab about catalog_returns.cr_return_ship_cost - all         |                 494.38 |                 489.23 |
| statistics_tab about catalog_returns.cr_refunded_cash - all            |                 492.02 |                 486.49 |
| statistics_tab about catalog_returns.cr_reversed_charge - all          |                 478.08 |                 480.70 |
| statistics_tab about catalog_returns.cr_store_credit - all             |                 707.04 |                 486.33 |
| statistics_tab about catalog_returns.cr_net_loss - all                 |                 501.18 |                 505.04 |
| statistics_tab about catalog_sales.cs_sold_date_sk - all               |               34517.16 |                3698.38 |
| statistics_tab about catalog_sales.cs_sold_time_sk - all               |                2261.68 |                2560.04 |
| statistics_tab about catalog_sales.cs_ship_date_sk - all               |                2339.32 |                2796.76 |
| statistics_tab about catalog_sales.cs_bill_customer_sk - all           |                4293.35 |                5329.68 |
| statistics_tab about catalog_sales.cs_bill_cdemo_sk - all              |                2411.14 |                2774.25 |
| statistics_tab about catalog_sales.cs_bill_hdemo_sk - all              |                2292.78 |                2317.82 |
| statistics_tab about catalog_sales.cs_bill_addr_sk - all               |                2422.76 |                2897.54 |
| statistics_tab about catalog_sales.cs_ship_customer_sk - all           |                4113.78 |                5236.81 |
| statistics_tab about catalog_sales.cs_ship_cdemo_sk - all              |                2532.91 |                2703.04 |
| statistics_tab about catalog_sales.cs_ship_hdemo_sk - all              |                2286.58 |                2695.21 |
| statistics_tab about catalog_sales.cs_ship_addr_sk - all               |                4039.22 |                5257.70 |
| statistics_tab about catalog_sales.cs_call_center_sk - all             |                3567.96 |                4574.31 |
| statistics_tab about catalog_sales.cs_catalog_page_sk - all            |                2531.73 |                3161.73 |
| statistics_tab about catalog_sales.cs_ship_mode_sk - all               |                2275.22 |                2232.54 |
| statistics_tab about catalog_sales.cs_warehouse_sk - all               |                4827.69 |                7568.03 |
| statistics_tab about catalog_sales.cs_item_sk - all                    |                9497.30 |               11618.24 |
| statistics_tab about catalog_sales.cs_promo_sk - all                   |                9370.15 |               11263.83 |
| statistics_tab about catalog_sales.cs_order_number - all               |                4598.82 |                4473.72 |
| statistics_tab about catalog_sales.cs_quantity - all                   |                2595.83 |                2681.49 |
| statistics_tab about catalog_sales.cs_wholesale_cost - all             |                4068.30 |                4248.49 |
| statistics_tab about catalog_sales.cs_list_price - all                 |                4472.87 |                4498.41 |
| statistics_tab about catalog_sales.cs_sales_price - all                |                4282.90 |                4249.50 |
| statistics_tab about catalog_sales.cs_ext_discount_amt - all           |                4739.88 |                4842.00 |
| statistics_tab about catalog_sales.cs_ext_sales_price - all            |                4933.64 |                4740.66 |
| statistics_tab about catalog_sales.cs_ext_wholesale_cost - all         |                4734.98 |                4515.42 |
| statistics_tab about catalog_sales.cs_ext_list_price - all             |                5620.36 |                5416.56 |
| statistics_tab about catalog_sales.cs_ext_tax - all                    |                4444.91 |                4203.50 |
| statistics_tab about catalog_sales.cs_coupon_amt - all                 |                3739.83 |                3949.59 |
| statistics_tab about catalog_sales.cs_ext_ship_cost - all              |                5074.78 |                4661.09 |
| statistics_tab about catalog_sales.cs_net_paid - all                   |                7150.22 |                5010.39 |
| statistics_tab about catalog_sales.cs_net_paid_inc_tax - all           |                7931.31 |                4700.53 |
| statistics_tab about catalog_sales.cs_net_paid_inc_ship - all          |                8959.87 |                5247.83 |
| statistics_tab about catalog_sales.cs_net_paid_inc_ship_tax - all      |                8578.43 |                5111.95 |
| statistics_tab about catalog_sales.cs_net_profit - all                 |                8139.04 |                4996.89 |
| statistics_tab about customer.c_customer_sk - all                      |                 701.33 |                 125.17 |
| statistics_tab about customer.c_customer_id - all                      |                1270.82 |                 680.96 |
| statistics_tab about customer.c_current_cdemo_sk - all                 |                 611.49 |                 259.66 |
| statistics_tab about customer.c_current_hdemo_sk - all                 |                 245.61 |                 109.35 |
| statistics_tab about customer.c_current_addr_sk - all                  |                 653.97 |                 239.58 |
| statistics_tab about customer.c_first_shipto_date_sk - all             |                 218.46 |                 104.43 |
| statistics_tab about customer.c_first_sales_date_sk - all              |                 222.63 |                 109.22 |
| statistics_tab about customer.c_salutation - all                       |                 252.76 |                 126.85 |
| statistics_tab about customer.c_first_name - all                       |                 347.16 |                 181.05 |
| statistics_tab about customer.c_last_name - all                        |                 386.90 |                 197.20 |
| statistics_tab about customer.c_preferred_cust_flag - all              |                 238.14 |                 114.37 |
| statistics_tab about customer.c_birth_day - all                        |                 213.10 |                  91.35 |
| statistics_tab about customer.c_birth_month - all                      |                 207.00 |                  91.90 |
| statistics_tab about customer.c_birth_year - all                       |                 216.63 |                  96.11 |
| statistics_tab about customer.c_birth_country - all                    |                 512.45 |                 207.01 |
| statistics_tab about customer.c_login - all                            |                 221.98 |                  89.25 |
| statistics_tab about customer.c_email_address - all                    |                1560.79 |                 711.44 |
| statistics_tab about customer.c_last_review_date - all                 |                 392.03 |                 178.70 |
| statistics_tab about customer_address.ca_address_sk - all              |                 391.03 |                  58.16 |
| statistics_tab about customer_address.ca_address_id - all              |                 611.84 |                 281.38 |
| statistics_tab about customer_address.ca_street_number - all           |                 115.58 |                  76.27 |
| statistics_tab about customer_address.ca_street_name - all             |                 134.68 |                  76.68 |
| statistics_tab about customer_address.ca_street_type - all             |                 155.40 |                  67.40 |
| statistics_tab about customer_address.ca_suite_number - all            |                 130.44 |                  66.24 |
| statistics_tab about customer_address.ca_city - all                    |                 113.50 |                  66.08 |
| statistics_tab about customer_address.ca_county - all                  |                 168.97 |                  92.01 |
| statistics_tab about customer_address.ca_state - all                   |                 163.98 |                  58.91 |
| statistics_tab about customer_address.ca_zip - all                     |                 179.96 |                  75.87 |
| statistics_tab about customer_address.ca_country - all                 |                 126.99 |                  54.23 |
| statistics_tab about customer_address.ca_gmt_offset - all              |                 124.80 |                  56.08 |
| statistics_tab about customer_address.ca_location_type - all           |                 148.42 |                  67.60 |
| statistics_tab about customer_demographics.cd_demo_sk - all            |                2205.55 |                 425.26 |
| statistics_tab about customer_demographics.cd_gender - all             |                 459.67 |                 305.68 |
| statistics_tab about customer_demographics.cd_marital_status - all     |                 474.66 |                 356.63 |
| statistics_tab about customer_demographics.cd_education_status - all   |                 715.79 |                 654.77 |
| statistics_tab about customer_demographics.cd_purchase_estimate - all  |                 397.51 |                 315.42 |
| statistics_tab about customer_demographics.cd_credit_rating - all      |                 531.89 |                 354.92 |
| statistics_tab about customer_demographics.cd_dep_count - all          |                 388.05 |                 303.39 |
| statistics_tab about customer_demographics.cd_dep_employed_count - all |                 607.73 |                 309.89 |
| statistics_tab about customer_demographics.cd_dep_college_count - all  |                 644.79 |                 318.45 |
| statistics_tab about date_dim.d_date_sk - all                          |                 108.30 |                  18.17 |
| statistics_tab about date_dim.d_date_id - all                          |                 130.74 |                  74.10 |
| statistics_tab about date_dim.d_date - all                             |                 118.10 |                  40.74 |
| statistics_tab about date_dim.d_month_seq - all                        |                  34.91 |                  10.54 |
| statistics_tab about date_dim.d_week_seq - all                         |                  29.25 |                  10.89 |
| statistics_tab about date_dim.d_quarter_seq - all                      |                  30.29 |                  15.34 |
| statistics_tab about date_dim.d_year - all                             |                  25.04 |                  13.97 |
| statistics_tab about date_dim.d_dow - all                              |                  28.56 |                  11.27 |
| statistics_tab about date_dim.d_moy - all                              |                  29.15 |                  11.43 |
| statistics_tab about date_dim.d_dom - all                              |                  30.57 |                  12.12 |
| statistics_tab about date_dim.d_qoy - all                              |                  20.69 |                  11.40 |
| statistics_tab about date_dim.d_fy_year - all                          |                  30.80 |                  11.35 |
| statistics_tab about date_dim.d_fy_quarter_seq - all                   |                  32.44 |                  11.73 |
| statistics_tab about date_dim.d_fy_week_seq - all                      |                  29.95 |                  11.50 |
| statistics_tab about date_dim.d_day_name - all                         |                  51.14 |                  19.50 |
| statistics_tab about date_dim.d_quarter_name - all                     |                  49.26 |                  18.30 |
| statistics_tab about date_dim.d_holiday - all                          |                  50.29 |                  18.27 |
| statistics_tab about date_dim.d_weekend - all                          |                  51.53 |                  18.57 |
| statistics_tab about date_dim.d_following_holiday - all                |                  59.42 |                  19.08 |
| statistics_tab about date_dim.d_first_dom - all                        |                  37.38 |                  12.53 |
| statistics_tab about date_dim.d_last_dom - all                         |                  40.85 |                  13.77 |
| statistics_tab about date_dim.d_same_day_ly - all                      |                  36.78 |                  12.43 |
| statistics_tab about date_dim.d_same_day_lq - all                      |                  20.81 |                  12.76 |
| statistics_tab about date_dim.d_current_day - all                      |                  52.63 |                  19.72 |
| statistics_tab about date_dim.d_current_week - all                     |                  53.83 |                  19.97 |
| statistics_tab about date_dim.d_current_month - all                    |                  54.50 |                  21.03 |
| statistics_tab about date_dim.d_current_quarter - all                  |                  55.06 |                  22.29 |
| statistics_tab about date_dim.d_current_year - all                     |                  56.08 |                  21.52 |
| statistics_tab about dbgen_version.dv_version - all                    |                   3.05 |                   1.55 |
| statistics_tab about dbgen_version.dv_create_date - all                |                   1.73 |                   1.78 |
| statistics_tab about dbgen_version.dv_create_time - all                |                   1.96 |                   1.96 |
| statistics_tab about dbgen_version.dv_cmdline_args - all               |                   2.97 |                   1.63 |
| statistics_tab about household_demographics.hd_demo_sk - all           |                  17.00 |                   2.90 |
| statistics_tab about household_demographics.hd_income_band_sk - all    |                   4.00 |                   2.51 |
| statistics_tab about household_demographics.hd_buy_potential - all     |                   4.12 |                   3.15 |
| statistics_tab about household_demographics.hd_dep_count - all         |                   3.49 |                   2.61 |
| statistics_tab about household_demographics.hd_vehicle_count - all     |                   2.66 |                   2.35 |
| statistics_tab about income_band.ib_income_band_sk - all               |                   3.00 |                   1.51 |
| statistics_tab about income_band.ib_lower_bound - all                  |                   1.68 |                   1.49 |
| statistics_tab about income_band.ib_upper_bound - all                  |                   1.47 |                   1.33 |
| statistics_tab about inventory.inv_date_sk - all                       |              141856.36 |               20824.79 |
| statistics_tab about inventory.inv_item_sk - all                       |              212578.64 |               51021.21 |
| statistics_tab about inventory.inv_warehouse_sk - all                  |               42986.22 |               20101.54 |
| statistics_tab about inventory.inv_quantity_on_hand - all              |               76974.08 |               23956.80 |
| statistics_tab about item.i_item_sk - all                              |                 855.38 |                  91.36 |
| statistics_tab about item.i_item_id - all                              |                 466.59 |                  88.12 |
| statistics_tab about item.i_rec_start_date - all                       |                 152.94 |                  32.07 |
| statistics_tab about item.i_rec_end_date - all                         |                 184.08 |                  37.98 |
| statistics_tab about item.i_item_desc - all                            |                 643.62 |                 127.20 |
| statistics_tab about item.i_current_price - all                        |                 149.66 |                  38.58 |
| statistics_tab about item.i_wholesale_cost - all                       |                 158.34 |                  34.71 |
| statistics_tab about item.i_brand_id - all                             |                 163.34 |                  23.39 |
| statistics_tab about item.i_brand - all                                |                 498.76 |                  83.90 |
| statistics_tab about item.i_class_id - all                             |                 205.69 |                  20.65 |
| statistics_tab about item.i_class - all                                |                 509.61 |                  64.45 |
| statistics_tab about item.i_category_id - all                          |                 306.16 |                  21.99 |
| statistics_tab about item.i_category - all                             |                 716.05 |                  47.68 |
| statistics_tab about item.i_manufact_id - all                          |                 286.10 |                  24.91 |
| statistics_tab about item.i_manufact - all                             |                 481.44 |                  64.98 |
| statistics_tab about item.i_size - all                                 |                 421.19 |                  46.43 |
| statistics_tab about item.i_formulation - all                          |                 920.10 |                  85.88 |
| statistics_tab about item.i_color - all                                |                 462.13 |                  48.60 |
| statistics_tab about item.i_units - all                                |                 402.89 |                  43.45 |
| statistics_tab about item.i_container - all                            |                 362.28 |                  47.88 |
| statistics_tab about item.i_manager_id - all                           |                 231.31 |                  24.59 |
| statistics_tab about item.i_product_name - all                         |                1183.16 |                 226.52 |
| statistics_tab about promotion.p_promo_sk - all                        |                   9.07 |                   1.28 |
| statistics_tab about promotion.p_promo_id - all                        |                  10.02 |                   1.62 |
| statistics_tab about promotion.p_start_date_sk - all                   |                   6.12 |                   0.97 |
| statistics_tab about promotion.p_end_date_sk - all                     |                   8.02 |                   1.15 |
| statistics_tab about promotion.p_item_sk - all                         |                   6.19 |                   1.06 |
| statistics_tab about promotion.p_cost - all                            |                   6.13 |                   0.99 |
| statistics_tab about promotion.p_response_target - all                 |                   6.92 |                   1.04 |
| statistics_tab about promotion.p_promo_name - all                      |                   9.01 |                   1.25 |
| statistics_tab about promotion.p_channel_dmail - all                   |                   7.93 |                   1.14 |
| statistics_tab about promotion.p_channel_email - all                   |                   8.47 |                   1.13 |
| statistics_tab about promotion.p_channel_catalog - all                 |                   4.66 |                   1.12 |
| statistics_tab about promotion.p_channel_tv - all                      |                   6.62 |                   1.09 |
| statistics_tab about promotion.p_channel_radio - all                   |                   6.74 |                   1.01 |
| statistics_tab about promotion.p_channel_press - all                   |                   6.93 |                   1.14 |
| statistics_tab about promotion.p_channel_event - all                   |                   8.27 |                   1.14 |
| statistics_tab about promotion.p_channel_demo - all                    |                   7.11 |                   1.16 |
| statistics_tab about promotion.p_channel_details - all                 |                   7.51 |                   1.48 |
| statistics_tab about promotion.p_purpose - all                         |                   6.35 |                   1.08 |
| statistics_tab about promotion.p_discount_active - all                 |                   8.79 |                   1.16 |
| statistics_tab about reason.r_reason_sk - all                          |                   8.65 |                   1.08 |
| statistics_tab about reason.r_reason_id - all                          |                   5.63 |                   1.01 |
| statistics_tab about reason.r_reason_desc - all                        |                   3.33 |                   1.00 |
| statistics_tab about ship_mode.sm_ship_mode_sk - all                   |                   6.90 |                   1.00 |
| statistics_tab about ship_mode.sm_ship_mode_id - all                   |                   5.39 |                   0.98 |
| statistics_tab about ship_mode.sm_type - all                           |                   6.75 |                   0.85 |
| statistics_tab about ship_mode.sm_code - all                           |                   4.29 |                   0.86 |
| statistics_tab about ship_mode.sm_carrier - all                        |                   3.90 |                   1.04 |
| statistics_tab about ship_mode.sm_contract - all                       |                   5.71 |                   0.77 |
| statistics_tab about store.s_store_sk - all                            |                  12.76 |                   1.03 |
| statistics_tab about store.s_store_id - all                            |                   8.77 |                   0.94 |
| statistics_tab about store.s_rec_start_date - all                      |                   4.66 |                   0.95 |
| statistics_tab about store.s_rec_end_date - all                        |                   4.41 |                   1.02 |
| statistics_tab about store.s_closed_date_sk - all                      |                   3.88 |                   0.83 |
| statistics_tab about store.s_store_name - all                          |                   5.17 |                   0.90 |
| statistics_tab about store.s_number_employees - all                    |                   3.94 |                   0.79 |
| statistics_tab about store.s_floor_space - all                         |                   5.09 |                   1.16 |
| statistics_tab about store.s_hours - all                               |                   5.58 |                   1.45 |
| statistics_tab about store.s_manager - all                             |                   3.89 |                   4.59 |
| statistics_tab about store.s_market_id - all                           |                   2.76 |                   0.77 |
| statistics_tab about store.s_geography_class - all                     |                   3.85 |                   0.91 |
| statistics_tab about store.s_market_desc - all                         |                   5.62 |                   1.05 |
| statistics_tab about store.s_market_manager - all                      |                   3.56 |                   1.18 |
| statistics_tab about store.s_division_id - all                         |                   3.92 |                   0.81 |
| statistics_tab about store.s_division_name - all                       |                   5.51 |                   0.89 |
| statistics_tab about store.s_company_id - all                          |                   2.94 |                   1.57 |
| statistics_tab about store.s_company_name - all                        |                   4.98 |                   1.65 |
| statistics_tab about store.s_street_number - all                       |                   5.56 |                   1.22 |
| statistics_tab about store.s_street_name - all                         |                   6.07 |                   1.18 |
| statistics_tab about store.s_street_type - all                         |                   4.61 |                   1.06 |
| statistics_tab about store.s_suite_number - all                        |                   8.07 |                   1.06 |
| statistics_tab about store.s_city - all                                |                   6.70 |                   1.26 |
| statistics_tab about store.s_county - all                              |                   5.59 |                   1.19 |
| statistics_tab about store.s_state - all                               |                   7.13 |                   1.12 |
| statistics_tab about store.s_zip - all                                 |                   7.27 |                   1.35 |
| statistics_tab about store.s_country - all                             |                   9.07 |                   1.22 |
| statistics_tab about store.s_gmt_offset - all                          |                   6.06 |                   0.88 |
| statistics_tab about store.s_tax_precentage - all                      |                   5.50 |                   0.93 |
| statistics_tab about store_returns.sr_returned_date_sk - all           |               27864.13 |                1673.51 |
| statistics_tab about store_returns.sr_return_time_sk - all             |                1117.04 |                 521.37 |
| statistics_tab about store_returns.sr_item_sk - all                    |                6158.16 |                1643.25 |
| statistics_tab about store_returns.sr_customer_sk - all                |                8684.12 |                1430.76 |
| statistics_tab about store_returns.sr_cdemo_sk - all                   |                1339.80 |                 618.10 |
| statistics_tab about store_returns.sr_hdemo_sk - all                   |                1446.88 |                 500.52 |
| statistics_tab about store_returns.sr_addr_sk - all                    |                1611.12 |                 569.08 |
| statistics_tab about store_returns.sr_store_sk - all                   |                7639.19 |                1342.03 |
| statistics_tab about store_returns.sr_reason_sk - all                  |                2253.55 |                 520.38 |
| statistics_tab about store_returns.sr_ticket_number - all              |                2131.93 |                 835.36 |
| statistics_tab about store_returns.sr_return_quantity - all            |                1336.42 |                 530.50 |
| statistics_tab about store_returns.sr_return_amt - all                 |                2430.95 |                 895.33 |
| statistics_tab about store_returns.sr_return_tax - all                 |                4271.63 |                 819.42 |
| statistics_tab about store_returns.sr_return_amt_inc_tax - all         |                2718.01 |                 909.62 |
| statistics_tab about store_returns.sr_fee - all                        |                1758.57 |                 844.77 |
| statistics_tab about store_returns.sr_return_ship_cost - all           |                2366.19 |                 874.60 |
| statistics_tab about store_returns.sr_refunded_cash - all              |                2468.32 |                 899.49 |
| statistics_tab about store_returns.sr_reversed_charge - all            |                2635.12 |                 874.62 |
| statistics_tab about store_returns.sr_store_credit - all               |                1377.46 |                 862.37 |
| statistics_tab about store_returns.sr_net_loss - all                   |                3255.08 |                 932.02 |
| statistics_tab about store_sales.ss_sold_date_sk - all                 |              166167.84 |                9997.83 |
| statistics_tab about store_sales.ss_sold_time_sk - all                 |                6758.40 |                4507.82 |
| statistics_tab about store_sales.ss_item_sk - all                      |               33838.60 |               25425.89 |
| statistics_tab about store_sales.ss_customer_sk - all                  |               11252.80 |                9739.52 |
| statistics_tab about store_sales.ss_cdemo_sk - all                     |                7726.42 |                4977.74 |
| statistics_tab about store_sales.ss_hdemo_sk - all                     |                6911.76 |                4623.84 |
| statistics_tab about store_sales.ss_addr_sk - all                      |                9773.21 |                4697.65 |
| statistics_tab about store_sales.ss_store_sk - all                     |               10673.56 |                9700.67 |
| statistics_tab about store_sales.ss_promo_sk - all                     |               31099.34 |               25571.49 |
| statistics_tab about store_sales.ss_ticket_number - all                |                8015.52 |                5022.48 |
| statistics_tab about store_sales.ss_quantity - all                     |                7087.68 |                4934.41 |
| statistics_tab about store_sales.ss_wholesale_cost - all               |               17020.11 |                8571.26 |
| statistics_tab about store_sales.ss_list_price - all                   |               13904.04 |                8923.67 |
| statistics_tab about store_sales.ss_sales_price - all                  |               16477.16 |                8714.23 |
| statistics_tab about store_sales.ss_ext_discount_amt - all             |               10409.62 |                7189.12 |
| statistics_tab about store_sales.ss_ext_sales_price - all              |               14565.56 |                9200.22 |
| statistics_tab about store_sales.ss_ext_wholesale_cost - all           |               17574.92 |                9285.17 |
| statistics_tab about store_sales.ss_ext_list_price - all               |               15041.96 |               10398.59 |
| statistics_tab about store_sales.ss_ext_tax - all                      |               13441.21 |                9428.71 |
| statistics_tab about store_sales.ss_coupon_amt - all                   |               15221.49 |                8099.54 |
| statistics_tab about store_sales.ss_net_paid - all                     |               18934.29 |                9800.65 |
| statistics_tab about store_sales.ss_net_paid_inc_tax - all             |               17709.97 |               10388.51 |
| statistics_tab about store_sales.ss_net_profit - all                   |               18452.85 |               10227.38 |
| statistics_tab about time_dim.t_time_sk - all                          |                  83.29 |                  22.75 |
| statistics_tab about time_dim.t_time_id - all                          |                 114.63 |                  99.69 |
| statistics_tab about time_dim.t_time - all                             |                  89.86 |                  13.80 |
| statistics_tab about time_dim.t_hour - all                             |                  21.55 |                  12.72 |
| statistics_tab about time_dim.t_minute - all                           |                  21.55 |                  13.51 |
| statistics_tab about time_dim.t_second - all                           |                  22.70 |                  14.10 |
| statistics_tab about time_dim.t_am_pm - all                            |                  47.60 |                  32.42 |
| statistics_tab about time_dim.t_shift - all                            |                  50.95 |                  33.62 |
| statistics_tab about time_dim.t_sub_shift - all                        |                  53.42 |                  33.03 |
| statistics_tab about time_dim.t_meal_time - all                        |                  47.51 |                  28.94 |
| statistics_tab about warehouse.w_warehouse_sk - all                    |                   8.01 |                   1.07 |
| statistics_tab about warehouse.w_warehouse_id - all                    |                   7.02 |                   1.01 |
| statistics_tab about warehouse.w_warehouse_name - all                  |                   4.08 |                   1.11 |
| statistics_tab about warehouse.w_warehouse_sq_ft - all                 |                   4.92 |                   1.09 |
| statistics_tab about warehouse.w_street_number - all                   |                   5.89 |                   1.45 |
| statistics_tab about warehouse.w_street_name - all                     |                   4.85 |                   1.18 |
| statistics_tab about warehouse.w_street_type - all                     |                   6.12 |                   1.14 |
| statistics_tab about warehouse.w_suite_number - all                    |                   6.29 |                   1.18 |
| statistics_tab about warehouse.w_city - all                            |                   5.71 |                   1.13 |
| statistics_tab about warehouse.w_county - all                          |                   7.69 |                   1.24 |
| statistics_tab about warehouse.w_state - all                           |                   3.28 |                   1.28 |
| statistics_tab about warehouse.w_zip - all                             |                   5.70 |                   1.32 |
| statistics_tab about warehouse.w_country - all                         |                   5.52 |                   1.41 |
| statistics_tab about warehouse.w_gmt_offset - all                      |                   2.66 |                   1.32 |
| statistics_tab about web_page.wp_web_page_sk - all                     |                   7.01 |                   1.68 |
| statistics_tab about web_page.wp_web_page_id - all                     |                   5.36 |                   1.54 |
| statistics_tab about web_page.wp_rec_start_date - all                  |                   5.86 |                   1.16 |
| statistics_tab about web_page.wp_rec_end_date - all                    |                   6.02 |                   1.37 |
| statistics_tab about web_page.wp_creation_date_sk - all                |                   2.67 |                   1.31 |
| statistics_tab about web_page.wp_access_date_sk - all                  |                   3.56 |                   1.36 |
| statistics_tab about web_page.wp_autogen_flag - all                    |                   3.88 |                   1.48 |
| statistics_tab about web_page.wp_customer_sk - all                     |                   3.87 |                   1.56 |
| statistics_tab about web_page.wp_url - all                             |                   4.74 |                   1.46 |
| statistics_tab about web_page.wp_type - all                            |                   7.95 |                   1.44 |
| statistics_tab about web_page.wp_char_count - all                      |                   4.11 |                   1.60 |
| statistics_tab about web_page.wp_link_count - all                      |                   6.86 |                   1.47 |
| statistics_tab about web_page.wp_image_count - all                     |                   4.45 |                   1.41 |
| statistics_tab about web_page.wp_max_ad_count - all                    |                   5.92 |                   1.22 |
| statistics_tab about web_returns.wr_returned_date_sk - all             |                5160.52 |                 413.82 |
| statistics_tab about web_returns.wr_returned_time_sk - all             |                 197.95 |                 173.10 |
| statistics_tab about web_returns.wr_item_sk - all                      |                 478.12 |                 396.56 |
| statistics_tab about web_returns.wr_refunded_customer_sk - all         |                 219.44 |                 180.63 |
| statistics_tab about web_returns.wr_refunded_cdemo_sk - all            |                 534.76 |                 184.15 |
| statistics_tab about web_returns.wr_refunded_hdemo_sk - all            |                 274.24 |                 161.24 |
| statistics_tab about web_returns.wr_refunded_addr_sk - all             |                 199.29 |                 181.05 |
| statistics_tab about web_returns.wr_returning_customer_sk - all        |                 408.30 |                 412.50 |
| statistics_tab about web_returns.wr_returning_cdemo_sk - all           |                 350.89 |                 187.42 |
| statistics_tab about web_returns.wr_returning_hdemo_sk - all           |                 361.11 |                 156.33 |
| statistics_tab about web_returns.wr_returning_addr_sk - all            |                 240.13 |                 177.08 |
| statistics_tab about web_returns.wr_web_page_sk - all                  |                 264.30 |                 138.97 |
| statistics_tab about web_returns.wr_reason_sk - all                    |                 415.09 |                 150.37 |
| statistics_tab about web_returns.wr_order_number - all                 |                 226.37 |                 165.84 |
| statistics_tab about web_returns.wr_return_quantity - all              |                 458.69 |                 157.04 |
| statistics_tab about web_returns.wr_return_amt - all                   |                 533.22 |                 290.37 |
| statistics_tab about web_returns.wr_return_tax - all                   |                 456.93 |                 255.59 |
| statistics_tab about web_returns.wr_return_amt_inc_tax - all           |                 393.86 |                 270.89 |
| statistics_tab about web_returns.wr_fee - all                          |                 292.97 |                 258.37 |
| statistics_tab about web_returns.wr_return_ship_cost - all             |                 289.68 |                 279.10 |
| statistics_tab about web_returns.wr_refunded_cash - all                |                 300.98 |                 277.01 |
| statistics_tab about web_returns.wr_reversed_charge - all              |                 308.70 |                 270.01 |
| statistics_tab about web_returns.wr_account_credit - all               |                 298.51 |                 402.58 |
| statistics_tab about web_returns.wr_net_loss - all                     |                 336.89 |                 286.16 |
| statistics_tab about web_sales.ws_sold_date_sk - all                   |               56588.18 |                2528.97 |
| statistics_tab about web_sales.ws_sold_time_sk - all                   |                1484.56 |                1377.61 |
| statistics_tab about web_sales.ws_ship_date_sk - all                   |                5386.14 |                4917.64 |
| statistics_tab about web_sales.ws_item_sk - all                        |                6294.13 |                5748.01 |
| statistics_tab about web_sales.ws_bill_customer_sk - all               |                2488.54 |                2198.43 |
| statistics_tab about web_sales.ws_bill_cdemo_sk - all                  |                1423.74 |                1448.19 |
| statistics_tab about web_sales.ws_bill_hdemo_sk - all                  |                2450.30 |                1329.87 |
| statistics_tab about web_sales.ws_bill_addr_sk - all                   |                1743.96 |                1361.96 |
| statistics_tab about web_sales.ws_ship_customer_sk - all               |                3032.39 |                2436.47 |
| statistics_tab about web_sales.ws_ship_cdemo_sk - all                  |                2545.14 |                1436.31 |
| statistics_tab about web_sales.ws_ship_hdemo_sk - all                  |                3234.38 |                1302.71 |
| statistics_tab about web_sales.ws_ship_addr_sk - all                   |                3072.42 |                2356.08 |
| statistics_tab about web_sales.ws_web_page_sk - all                    |                1346.39 |                1446.40 |
| statistics_tab about web_sales.ws_web_site_sk - all                    |                4171.60 |                4812.42 |
| statistics_tab about web_sales.ws_ship_mode_sk - all                   |                1236.52 |                1341.16 |
| statistics_tab about web_sales.ws_warehouse_sk - all                   |                3790.84 |                3887.78 |
| statistics_tab about web_sales.ws_promo_sk - all                       |                6369.92 |                5449.67 |
| statistics_tab about web_sales.ws_order_number - all                   |                1556.20 |                1677.64 |
| statistics_tab about web_sales.ws_quantity - all                       |                1688.31 |                1505.83 |
| statistics_tab about web_sales.ws_wholesale_cost - all                 |                2691.27 |                2352.66 |
| statistics_tab about web_sales.ws_list_price - all                     |                3412.56 |                2556.04 |
| statistics_tab about web_sales.ws_sales_price - all                    |                3143.40 |                2553.94 |
| statistics_tab about web_sales.ws_ext_discount_amt - all               |                4754.04 |                2983.26 |
| statistics_tab about web_sales.ws_ext_sales_price - all                |                4191.30 |                3012.00 |
| statistics_tab about web_sales.ws_ext_wholesale_cost - all             |                3809.11 |                2670.19 |
| statistics_tab about web_sales.ws_ext_list_price - all                 |                4624.62 |                3850.31 |
| statistics_tab about web_sales.ws_ext_tax - all                        |                2856.29 |                2525.11 |
| statistics_tab about web_sales.ws_coupon_amt - all                     |                3339.56 |                2310.69 |
| statistics_tab about web_sales.ws_ext_ship_cost - all                  |                3425.14 |                3019.24 |
| statistics_tab about web_sales.ws_net_paid - all                       |                2670.72 |                2970.49 |
| statistics_tab about web_sales.ws_net_paid_inc_tax - all               |                3721.94 |                2993.94 |
| statistics_tab about web_sales.ws_net_paid_inc_ship - all              |                2647.86 |                2973.09 |
| statistics_tab about web_sales.ws_net_paid_inc_ship_tax - all          |                4025.61 |                3208.29 |
| statistics_tab about web_sales.ws_net_profit - all                     |                3456.15 |                2854.34 |
| statistics_tab about web_site.web_site_sk - all                        |                   5.94 |                   1.15 |
| statistics_tab about web_site.web_site_id - all                        |                   1.50 |                   1.17 |
| statistics_tab about web_site.web_rec_start_date - all                 |                   1.52 |                   1.01 |
| statistics_tab about web_site.web_rec_end_date - all                   |                   1.03 |                   1.16 |
| statistics_tab about web_site.web_name - all                           |                   1.05 |                   0.94 |
| statistics_tab about web_site.web_open_date_sk - all                   |                   0.65 |                   0.96 |
| statistics_tab about web_site.web_close_date_sk - all                  |                   0.89 |                   0.93 |
| statistics_tab about web_site.web_class - all                          |                   0.97 |                   1.07 |
| statistics_tab about web_site.web_manager - all                        |                   1.08 |                   0.82 |
| statistics_tab about web_site.web_mkt_id - all                         |                   0.97 |                   0.82 |
| statistics_tab about web_site.web_mkt_class - all                      |                   1.06 |                   0.72 |
| statistics_tab about web_site.web_mkt_desc - all                       |                   1.04 |                   0.86 |
| statistics_tab about web_site.web_market_manager - all                 |                   1.28 |                   0.79 |
| statistics_tab about web_site.web_company_id - all                     |                   0.83 |                   1.01 |
| statistics_tab about web_site.web_company_name - all                   |                   1.28 |                   0.90 |
| statistics_tab about web_site.web_street_number - all                  |                   0.88 |                   1.15 |
| statistics_tab about web_site.web_street_name - all                    |                   1.34 |                   1.09 |
| statistics_tab about web_site.web_street_type - all                    |                   0.94 |                   1.06 |
| statistics_tab about web_site.web_suite_number - all                   |                   1.03 |                   1.37 |
| statistics_tab about web_site.web_city - all                           |                   1.01 |                   1.38 |
| statistics_tab about web_site.web_county - all                         |                   0.89 |                   0.91 |
| statistics_tab about web_site.web_state - all                          |                   0.91 |                   0.92 |
| statistics_tab about web_site.web_zip - all                            |                   1.05 |                   0.86 |
| statistics_tab about web_site.web_country - all                        |                   1.20 |                   0.88 |
| statistics_tab about web_site.web_gmt_offset - all                     |                   1.07 |                   0.83 |
| statistics_tab about web_site.web_tax_percentage - all                 |                   0.80 |                   1.11 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      1622.27 |      2.78 |          20.92 |                 41.17 |
| postgresql-1-1-2-1 |       931.98 |      1.93 |          22.69 |                 43.92 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        26.36 |      0.47 |           0.28 |                  0.29 |
| postgresql-1-1-2-1 |        25.67 |      0.08 |           0.28 |                  0.29 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: PostgreSQL-1)
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













## MonetDB at SF 30

An example of MonetDB at SF=30, power and throughput test, is on [Example: Benchmark MonetDB](Example-MonetDB.md#tpc-ds-at-sf-30).
