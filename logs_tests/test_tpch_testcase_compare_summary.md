## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 1300s 
* Code: 1782313700
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 10Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MariaDB-1-1-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:256385
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782313700
* MonetDB-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP1
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:261209
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782313700
* MySQL-1-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:285361
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782313700
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:264644
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782313700

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1    |                1 |    1 |       64.00 |           0.00 |           17.00 |         41.00 |            3.00 |              8 |           0 |             | None           |             0 | False         |               56.25 |
| MonetDB-1-1    |                1 |    1 |      165.00 |           2.00 |           16.00 |         19.00 |          124.00 |              8 |           0 |             | None           |             0 | False         |               21.82 |
| MySQL-1-1      |                1 |    1 |      197.00 |           1.00 |           19.00 |         19.00 |          153.00 |              8 |           0 |             | None           |             0 | False         |               18.27 |
| PostgreSQL-1-1 |                1 |    1 |      203.00 |           2.00 |           24.00 |          7.00 |          166.00 |              8 |           0 |             |                |             0 | False         |               17.73 |

### Execution

#### Per Connection


#### Per Phase



### Latency of Timer Execution [ms]
bexhoma : Traceback (most recent call last):
In Zeile:1 Zeichen:1
+ bexhoma tpch `
+ ~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (Traceback (most recent call last)::String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\tpch.py", line 420, in <module>
    experiment.process()
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\experiments\base.py", line 291, in process
    self.show_summary()
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\experiments\tpch.py", line 159, in show_summary
    super().show_summary()
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\experiments\dbmsbenchmarker.py", line 120, in 
show_summary
    primary.show_summary(self)
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\benchmarks\base.py", line 170, in show_summary
    extra_context = self._show_extra_sections(experiment, df_aggregated_reduced)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\benchmarks\base.py", line 276, in 
_show_extra_sections
    df_latencies = self.evaluator.get_query_latencies(query_titles=True)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\evaluators\dbmsbenchmarker.py", line 387, in 
get_query_latencies
    df = self.evaluation.get_aggregated_query_statistics(type='latency', name='execution', query_aggregate='Mean').T
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'T'
