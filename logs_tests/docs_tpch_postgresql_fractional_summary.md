## Show Summary

### Workload
TPC-H Queries SF=0.1
* Type: tpch
* Duration: 743s 
* Code: 1782123168
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=0.1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.18.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 5Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:219924
  * datadisk:315
  * volume_size:5.0G
  * volume_used:312M
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782123168
* PostgreSQL-1-2-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:219924
  * datadisk:315
  * volume_size:5.0G
  * volume_used:312M
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782123168

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (1 pods)

### Loading

#### Per Run

Traceback (most recent call last):
  File "/home/perdelt/Git-projects/Benchmark-Experiment-Host-Manager/tpch.py", line 420, in <module>
    experiment.process()
    ~~~~~~~~~~~~~~~~~~^^
  File "/home/perdelt/Git-projects/Benchmark-Experiment-Host-Manager/bexhoma/experiments/base.py", line 291, in process
    self.show_summary()
    ~~~~~~~~~~~~~~~~~^^
  File "/home/perdelt/Git-projects/Benchmark-Experiment-Host-Manager/bexhoma/experiments/tpch.py", line 159, in show_summary
    super().show_summary()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/perdelt/Git-projects/Benchmark-Experiment-Host-Manager/bexhoma/experiments/dbmsbenchmarker.py", line 120, in show_summary
    primary.show_summary(self)
    ~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/home/perdelt/Git-projects/Benchmark-Experiment-Host-Manager/bexhoma/benchmarks/base.py", line 155, in show_summary
    df_loading = self._show_loading_sections(experiment, is_multitenant)
  File "/home/perdelt/Git-projects/Benchmark-Experiment-Host-Manager/bexhoma/benchmarks/base.py", line 91, in _show_loading_sections
    df = self.evaluator.get_summary_loading_per_run()
  File "/home/perdelt/Git-projects/Benchmark-Experiment-Host-Manager/bexhoma/evaluators/dbmsbenchmarker.py", line 477, in get_summary_loading_per_run
    df = self.get_loading_per_run()
  File "/home/perdelt/Git-projects/Benchmark-Experiment-Host-Manager/bexhoma/evaluators/base.py", line 545, in get_loading_per_run
    df = self.get_loading_per_connection()
  File "/home/perdelt/Git-projects/Benchmark-Experiment-Host-Manager/bexhoma/evaluators/base.py", line 523, in get_loading_per_connection
    df['SF'] = int(workload_properties['defaultParameters']['SF'])
               ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ValueError: invalid literal for int() with base 10: '0.1'
