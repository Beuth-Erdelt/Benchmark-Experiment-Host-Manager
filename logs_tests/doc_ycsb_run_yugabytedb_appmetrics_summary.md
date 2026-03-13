## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 365s 
    Code: 1772846156
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.9.1.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['YugabyteDB'].
    Import is handled by 8 processes (pods).
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
YugabyteDB-64-8-65536-1 uses docker image postgres:15.0
    RAM:2164173209600
    CPU:INTEL(R) XEON(R) PLATINUM 8570
    Cores:224
    host:6.8.0-90-generic
    node:cl-worker36
    disk:699849
    cpu_list:0-223
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1772846156

### Loading
python : Traceback (most recent call last):
In Zeile:1 Zeichen:1
+ python ycsb.py -ms 1 -tr `
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (Traceback (most recent call last)::String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\ycsb.py", line 1123, in <module>
    experiment.process()
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\experiments.py", line 252, in process
    self.show_summary()
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\experiments.py", line 3809, in show_summary
    df_plot = self.evaluator.loading_set_datatypes(df)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\evaluators.py", line 1052, in 
loading_set_datatypes
    df_typed = df.astype({
               ^^^^^^^^^^^
  File "C:\Users\Patrick\anaconda3\envs\bexhoma\Lib\site-packages\pandas\core\generic.py", line 6627, in astype
    raise KeyError(
KeyError: "Only a column name can be used for the key in a dtype mappings argument. '[CLEANUP].Operations' not found in columns."
