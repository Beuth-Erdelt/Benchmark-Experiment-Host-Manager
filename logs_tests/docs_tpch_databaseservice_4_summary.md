## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 270s 
* Code: 1793622540
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['DatabaseService'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 2.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* databaseservice-1-1-1-1-1 uses docker image postgres:16.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:741664
  * datadisk:39
  * volume_size:49G
  * volume_used:39M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 1.0 CPU, 1.0 GiB RAM requested in 1 pods
    * sut: 1 x, 1.0 CPU, 1.0 GiB RAM
  * eval_parameters
    * code:1793622540

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: DatabaseService-1

### Data Parameters of Reused Volumes
* DatabaseService-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-databaseservice-1-1793622540-558b9f99d5-fljn9: 0

### Workflow

#### Actual

* DBMS DatabaseService-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS DatabaseService-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                     |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:--------------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| DatabaseService-1-1 |                1 |    3 |       41.00 |           2.00 |           24.00 |          7.00 |            3.00 |              0 |           0 |             | None           |             0 | False         |              263.41 | True                |

### Benchmarking

#### Per Connection

| DBMS                      | configuration     | phase                 | job                     |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                       |
|:--------------------------|:------------------|:----------------------|:------------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:--------------------------|
| databaseservice-1-1-1-1-1 | DatabaseService-1 | databaseservice-1-1-1 | databaseservice-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  22 |          4 |            0.00 |          6109156.06 |          59400.00 |          -1 | databaseservice-1-1-1-1-1 |

#### Per Phase

|                       | phase                 |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------------|:----------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| databaseservice-1-1-1 | databaseservice-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  22 |          4 |            0.00 |          6109156.06 |          59400.00 |          -1 |

#### Query Completion per Phase

| phase                 |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:----------------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| databaseservice-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   databaseservice-1-1-1-1-1 |
|:----------------------------------------------------|----------------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                       35.21 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                        3.25 |
| Shipping Priority (TPC-H Q3)                        |                        1.65 |
| Order Priority Checking Query (TPC-H Q4)            |                        1.26 |
| Local Supplier Volume (TPC-H Q5)                    |                        1.94 |
| Forecasting Revenue Change (TPC-H Q6)               |                        1.16 |
| Volume Shipping Query (TPC-H Q7)                    |                        1.78 |
| National Market Share (TPC-H Q8)                    |                        2.31 |
| Product Type Profit Measure (TPC-H Q9)              |                        1.67 |
| Returned Item Reporting Query (TPC-H Q10)           |                        1.82 |
| Important Stock Identification (TPC-H Q11)          |                        1.85 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                        1.17 |
| Customer Distribution (TPC-H Q13)                   |                        1.51 |
| Promotion Effect Query (TPC-H Q14)                  |                        1.29 |
| Top Supplier Query (TPC-H Q15)                      |                        1.09 |
| Parts/Supplier Relationship (TPC-H Q16)             |                        1.06 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                        1.23 |
| Large Volume Customer (TPC-H Q18)                   |                        1.27 |
| Discounted Revenue (TPC-H Q19)                      |                        1.50 |
| Potential Part Promotion (TPC-H Q20)                |                        1.53 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                        1.59 |
| Global Sales Opportunity Query (TPC-H Q22)          |                        1.49 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Benchmarking phase: component benchmarker

| DBMS                    | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|:-------------|----------:|---------------:|----------------------:|
| databaseservice-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Missing Monitoring Metrics
* Memory Usage, Working Set [MiB] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Memory Usage incl. Page Cache [MiB] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Utilization [CPUs] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization Time [s] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttled Time [s] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU User Time [s] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU System Time [s] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Network Rx Total [MiB] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Network Tx Total [MiB] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: DatabaseService-1)
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST skipped: Benchmarking phase: component benchmarker contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Monitoring metrics missing (phase shorter than scrape interval; series exists only while non-zero)
* TEST failed: Geo Times [s] contains 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
