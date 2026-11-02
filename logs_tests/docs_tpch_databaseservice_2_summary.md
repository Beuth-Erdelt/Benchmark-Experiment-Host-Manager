## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 270s 
* Code: 1793621753
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
  * Loading is skipped.
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
  * disk:741617
  * datadisk:39
  * volume_size:1.8T
  * volume_used:725G
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 1.0 CPU, 1.0 GiB RAM requested in 1 pods
    * sut: 1 x, 1.0 CPU, 1.0 GiB RAM
  * eval_parameters
    * code:1793621753

### SUT Container Restarts
* bexhoma-sut-databaseservice-1-1793621753-5d5bd95576-9xx2t: 0
bexhoma : Traceback (most recent call last):
In C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\scripts\test-docs-databaseservice.ps1:230 Zeichen:1
+ bexhoma tpch `
+ ~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (Traceback (most recent call last)::String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\tpch.py", line 611, in <module>
    run(args)
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\tpch.py", line 602, in run
    experiment.process()
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\experiments\base.py", line 384, in process
    self.show_summary(write_report=getattr(self.args, 'write_report', False))
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\experiments\tpch.py", line 224, in show_summary
    super().show_summary(write_report=write_report)
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\experiments\dbmsbenchmarker.py", line 154, in show_summary
    primary.show_summary(self, write_report=write_report)
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\benchmarks\base.py", line 502, in show_summary
    loading_section, df_loading = self._show_loading_sections(experiment, is_multitenant)
                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\benchmarks\base.py", line 279, in _show_loading_sections
    df = self.evaluator.get_summary_loading_per_run()
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\evaluators\dbmsbenchmarker.py", line 708, in get_summary_loading_per_run
    df = self.get_loading_per_run()
         ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\evaluators\base.py", line 815, in get_loading_per_run
    df = self.get_loading_per_connection()
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\evaluators\base.py", line 791, in get_loading_per_connection
    df_tpx = (df['SF'] * 3600.0)/df_load.sort_index()
             ~~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~~
  File "C:\Users\Patrick\anaconda3\envs\bexhoma\Lib\site-packages\pandas\core\ops\common.py", line 76, in new_method
    return method(self, other)
           ^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\anaconda3\envs\bexhoma\Lib\site-packages\pandas\core\arraylike.py", line 210, in __truediv__
    return self._arith_method(other, operator.truediv)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\anaconda3\envs\bexhoma\Lib\site-packages\pandas\core\series.py", line 6154, in _arith_method
    return base.IndexOpsMixin._arith_method(self, other, op)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\anaconda3\envs\bexhoma\Lib\site-packages\pandas\core\base.py", line 1391, in _arith_method
    result = ops.arithmetic_op(lvalues, rvalues, op)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\anaconda3\envs\bexhoma\Lib\site-packages\pandas\core\ops\array_ops.py", line 283, in arithmetic_op
    res_values = _na_arithmetic_op(left, right, op)  # type: ignore[arg-type]
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\anaconda3\envs\bexhoma\Lib\site-packages\pandas\core\ops\array_ops.py", line 218, in _na_arithmetic_op
    result = func(left, right)
             ^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\anaconda3\envs\bexhoma\Lib\site-packages\pandas\core\computation\expressions.py", line 242, in evaluate
    return _evaluate(op, op_str, a, b)  # type: ignore[misc]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\anaconda3\envs\bexhoma\Lib\site-packages\pandas\core\computation\expressions.py", line 73, in _evaluate_standard
    return op(a, b)
           ^^^^^^^^
ZeroDivisionError: float division by zero
