## Show Summary

### Workload
Benchbase Workload SF=16 (warehouses for TPC-C)
*    Type: benchbase
*    Duration: 1030s 
*    Code: 1728326500
*    This includes no queries. Benchbase runs the benchmark
*    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor (e.g., number of warehouses) is 16. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
*    RAM:541008605184
*    CPU:AMD Opteron(tm) Processor 6378
*    Cores:64
*    host:5.15.0-116-generic
*    node:cl-worker11
*    disk:253380184
*    datadisk:4409116
*    requests_cpu:4
*    requests_memory:16Gi

PostgreSQL-1-1-1024-2 uses docker image postgres:16.1
*    RAM:541008605184
*    CPU:AMD Opteron(tm) Processor 6378
*    Cores:64
*    host:5.15.0-116-generic
*    node:cl-worker11
*    disk:256636664
*    datadisk:7665440
*    requests_cpu:4
*    requests_memory:16Gi

### Execution

|    x                  | experiment_run | terminals | target | pod_count |  time | Throughput (requests/second) | Latency Distribution.95th Percentile Latency (microseconds) | Latency Distribution.Average Latency (microseconds) |
|-----------------------|---------------:|:----------|--------|-----------|-------|------------------------------|-------------------------------------------------------------|-----------------------------------------------------|
| PostgreSQL-1-1-1024-1 |              1 |        16 |  16384 |        1  | 300.0 |                     2619.73  |                                                     13335.0 |                                              6102.0 |
| PostgreSQL-1-1-1024-2 |              1 |        16 |  16384 |        2  | 300.0 |                     2397.49  |                                                     15397.0 |                                              6666.5 |

Warehouses: 16

### Workflow

#### Actual
* DBMS PostgreSQL-1-1-1024 - Pods [[2, 1]]

#### Planned
* DBMS PostgreSQL-1-1-1024 - Pods [[1, 2]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-1-1-1024-1      132.0        1.0   1.0                 436.363636
PostgreSQL-1-1-1024-2      132.0        1.0   2.0                 436.363636

### Ingestion - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1      900.72     9.45          4.01                 5.63
PostgreSQL-1-1-1024-2      900.72     9.45          4.01                 5.63

### Ingestion - Loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1      981.97    10.75          1.33                 1.33
PostgreSQL-1-1-1024-2      981.97    10.75          1.33                 1.33

### Execution - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1     2125.39     7.73          4.83                 7.10
PostgreSQL-1-1-1024-2     2174.26     7.16          5.43                 8.25

### Execution - Benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1     1323.62     4.88          1.44                 1.44
PostgreSQL-1-1-1024-2     1323.62     2.42          4.17                 4.17

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
* TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned

|   animal_1 |   animal_2 |
|-----------:|-----------:|
|          1 |          3 |
|          2 |          4 |

