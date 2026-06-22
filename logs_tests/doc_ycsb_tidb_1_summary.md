## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 457s 
* Code: 1782072943
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Experiment uses bexhoma version 0.9.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['TiDB'].
  * Import is handled by 8 processes (pods).
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* TiDB-1-1-1-1 uses docker image pingcap/tidb:v7.1.6
  * RAM:540590841856
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-117-generic
  * node:cl-worker25
  * disk:184602
  * cpu_list:0-95
  * requests_cpu:4
  * requests_memory:16Gi
  * sut 0
    * RAM:540590841856
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-117-generic
    * node:cl-worker25
    * disk:184602
    * cpu_list:0-95
  * sut 1
    * RAM:540579295232
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-124-generic
    * node:cl-worker22
    * disk:399606
    * cpu_list:0-127
  * sut 2
    * RAM:540590825472
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-117-generic
    * node:cl-worker23
    * disk:1419279
    * cpu_list:0-95
  * pd 0
    * RAM:540597927936
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-124-generic
    * node:cl-worker39
    * disk:277866
    * cpu_list:0-255
  * pd 1
    * RAM:540590841856
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-117-generic
    * node:cl-worker25
    * disk:184602
    * cpu_list:0-95
  * pd 2
    * RAM:540590825472
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-117-generic
    * node:cl-worker23
    * disk:1419279
    * cpu_list:0-95
  * tikv 0
    * RAM:1077382602752
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-1052-nvidia
    * node:cl-worker28
    * disk:393225
    * cpu_list:0-255
  * tikv 1
    * RAM:540597927936
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-124-generic
    * node:cl-worker39
    * disk:277866
    * cpu_list:0-255
  * tikv 2
    * RAM:1077381271552
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1354293
    * cpu_list:0-255
  * eval_parameters
    * code:1782072943
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Workflow

#### Actual

* DBMS TiDB-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS TiDB-1 - Experiment 1 Client 1: ycsb (1 pods)
    experiment.process()
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\experiments\base.py", line 291, in process
    self.show_summary()
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\experiments\mixed.py", line 126, in show_summary
    benchmark.show_summary(self)
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\benchmarks\base.py", line 155, in show_summary
    df_loading = self._show_loading_sections(experiment, is_multitenant)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\benchmarks\ycsb.py", line 136, in _show_loading_sections
    df_loading = self.evaluator.get_summary_loading_per_connection()
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\evaluators\ycsb.py", line 1038, in get_summary_loading_per_connection
    df_plot = self.loading_set_datatypes(df)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\evaluators\ycsb.py", line 452, in loading_set_datatypes
    df_typed = df.astype({
               ^^^^^^^^^^^
  File "C:\Users\Patrick\anaconda3\envs\bexhoma\Lib\site-packages\pandas\core\generic.py", line 6627, in astype
    raise KeyError(
KeyError: "Only a column name can be used for the key in a dtype mappings argument. '[CLEANUP].Operations' not found in columns."
