## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 211s 
* Code: 1793709889
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
  * Status is logged every 10s.
  * TiDB uses 3 SUT replica(s) and 3 PD node(s).
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * Experiment is limited to DBMS ['TiDB'].
  * Import is handled by 8 processes (pods).
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 3 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* tidb-1-1-1-1 uses docker image pingcap/tidb:v8.5.8
  * RAM:540590821376
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-137-generic
  * node:cl-worker23
  * disk:1281932
  * cpu_list:0-95
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * sut 0
    * RAM:540590821376
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-137-generic
    * node:cl-worker23
    * disk:1281932
    * cpu_list:0-95
  * sut 1
    * RAM:540590792704
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker25
    * disk:125736
    * cpu_list:0-95
  * sut 2
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:269038
    * cpu_list:0-127
  * pd 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:809123
    * datadisk:123
    * cpu_list:0-223
  * pd 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:620059
    * datadisk:123
    * cpu_list:0-127
  * pd 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:642331
    * datadisk:123
    * cpu_list:0-127
  * tikv 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:809123
    * datadisk:18157
    * cpu_list:0-223
  * tikv 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:620059
    * datadisk:9139
    * cpu_list:0-127
  * tikv 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:642331
    * datadisk:18163
    * cpu_list:0-127
  * resources_total: 24.75 CPU, 385.5 GiB RAM requested in 9 pods
    * pd: 3 x, 0.75 CPU, 1.5 GiB RAM
    * tikv: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793709889
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-tidb-1-1793709889-7995985d79-4p9qq: 0
* bexhoma-sut-tidb-1-1793709889-7995985d79-hd95j: 0
* bexhoma-sut-tidb-1-1793709889-7995985d79-w69tf: 0
* bx-pd-ti-1-1793709889-0: 0
* bx-pd-ti-1-1793709889-1: 0
* bx-pd-ti-1-1793709889-2: 0
* bx-tikv-ti-1-1793709889-0: 0
* bx-tikv-ti-1-1793709889-1: 0
* bx-tikv-ti-1-1793709889-2: 0
Traceback (most recent call last):
  File "/home/perdelt/Git-projects/Benchmark-Experiment-Host-Manager/ycsb.py", line 1071, in <module>
    run(args)
    ~~~^^^^^^
  File "/home/perdelt/Git-projects/Benchmark-Experiment-Host-Manager/ycsb.py", line 1065, in run
    experiment.process()
    ~~~~~~~~~~~~~~~~~~^^
  File "/home/perdelt/Git-projects/Benchmark-Experiment-Host-Manager/bexhoma/experiments/base.py", line 384, in process
    self.show_summary(write_report=getattr(self.args, 'write_report', False))
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/perdelt/Git-projects/Benchmark-Experiment-Host-Manager/bexhoma/experiments/mixed.py", line 156, in show_summary
    benchmark.show_summary(self, write_report=write_report)
    ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/perdelt/Git-projects/Benchmark-Experiment-Host-Manager/bexhoma/benchmarks/base.py", line 502, in show_summary
    loading_section, df_loading = self._show_loading_sections(experiment, is_multitenant)
                                  ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/perdelt/Git-projects/Benchmark-Experiment-Host-Manager/bexhoma/benchmarks/ycsb.py", line 136, in _show_loading_sections
    df_loading = self.evaluator.get_summary_loading_per_connection()
  File "/home/perdelt/Git-projects/Benchmark-Experiment-Host-Manager/bexhoma/evaluators/ycsb.py", line 1050, in get_summary_loading_per_connection
    df_plot = self.loading_set_datatypes(df)
  File "/home/perdelt/Git-projects/Benchmark-Experiment-Host-Manager/bexhoma/evaluators/ycsb.py", line 455, in loading_set_datatypes
    df_typed = df.astype({
        'code':'str',
    ...<26 lines>...
        '[INSERT].Return=OK':'int',
    })
  File "/home/perdelt/anaconda3/envs/bexhoma/lib/python3.14/site-packages/pandas/core/generic.py", line 6505, in astype
    raise KeyError(
    ...<3 lines>...
    )
KeyError: "Only a column name can be used for the key in a dtype mappings argument. '[CLEANUP].Operations' not found in columns."
