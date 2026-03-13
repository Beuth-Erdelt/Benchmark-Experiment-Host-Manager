## Show Summary

### Workload
TPC-DS Queries SF=3
    Type: tpcds
    Duration: 3665s 
    Code: 1773317668
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.9.3.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-BHT-8-1-1 uses docker image postgres:18.3
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:162099
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
    requests_cpu:4
    requests_memory:16Gi
    limits_memory:64Gi
    eval_parameters
        code:1773317668

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           PostgreSQL-BHT-8-1-1
TPC-DS Q1                    543.67
TPC-DS Q2                   1775.12
TPC-DS Q3                   1221.83
TPC-DS Q4                  48726.02
TPC-DS Q5                   2702.04
TPC-DS Q6                 861084.52
TPC-DS Q7                   1802.25
TPC-DS Q8                    299.34
TPC-DS Q9                   8036.28
TPC-DS Q10                  3364.74
TPC-DS Q11                 26675.52
TPC-DS Q12                   416.09
TPC-DS Q13                  4182.11
TPC-DS Q14a+b              20428.85
TPC-DS Q15                   861.47
TPC-DS Q16                  1303.68
TPC-DS Q17                  2090.07
TPC-DS Q18                  1913.19
TPC-DS Q19                  1161.91
TPC-DS Q20                   727.13
TPC-DS Q21                  1072.11
TPC-DS Q22                 23566.97
TPC-DS Q23a+b              35829.93
TPC-DS Q24a+b               4207.69
TPC-DS Q25                  2035.00
TPC-DS Q26                  1444.41
TPC-DS Q27                   119.17
TPC-DS Q28                  6168.26
TPC-DS Q29                  2300.21
TPC-DS Q30                230997.35
TPC-DS Q31                 12220.52
TPC-DS Q32                   936.59
TPC-DS Q33                  2224.00
TPC-DS Q34                   103.02
TPC-DS Q35                  4024.75
TPC-DS Q36                   120.07
TPC-DS Q37                  1385.97
TPC-DS Q38                  8334.95
TPC-DS Q39a+b              13844.37
TPC-DS Q40                   709.12
TPC-DS Q41                 12033.69
TPC-DS Q42                   508.65
TPC-DS Q43                  1192.79
TPC-DS Q44                     3.27
TPC-DS Q45                   502.07
TPC-DS Q46                   161.96
TPC-DS Q47                  8073.33
TPC-DS Q48                  3860.27
TPC-DS Q49                  3803.15
TPC-DS Q50                  3808.00
TPC-DS Q51                  7628.07
TPC-DS Q52                   530.38
TPC-DS Q53                   668.76
TPC-DS Q54                   193.40
TPC-DS Q55                   544.26
TPC-DS Q56                  2107.80
TPC-DS Q57                  6600.10
TPC-DS Q58                  2303.70
TPC-DS Q59                  2731.03
TPC-DS Q60                  2840.64
TPC-DS Q61                   287.41
TPC-DS Q62                   604.81
TPC-DS Q63                   649.99
TPC-DS Q64                  2804.59
TPC-DS Q65                  3905.91
TPC-DS Q66                  1769.09
TPC-DS Q67                 26586.62
TPC-DS Q68                   165.18
TPC-DS Q69                  1148.17
TPC-DS Q70                  2926.49
TPC-DS Q71                  2167.60
TPC-DS Q72                  7045.29
TPC-DS Q73                   102.03
TPC-DS Q74                  6961.53
TPC-DS Q75                  9966.00
TPC-DS Q76                   916.98
TPC-DS Q77                  1363.57
TPC-DS Q78                  6909.87
TPC-DS Q79                  1238.70
TPC-DS Q80                  2177.61
TPC-DS Q81                991893.63
TPC-DS Q82                  1402.05
TPC-DS Q83                   462.31
TPC-DS Q84                   258.50
TPC-DS Q85                   954.96
TPC-DS Q86                  1448.22
TPC-DS Q87                  8470.22
TPC-DS Q88                  7785.53
TPC-DS Q89                   785.28
TPC-DS Q90                  1077.84
TPC-DS Q91                   463.54
TPC-DS Q92                   255.88
TPC-DS Q93                  1315.91
TPC-DS Q94                  1052.19
TPC-DS Q95                 25516.06
TPC-DS Q96                   519.37
TPC-DS Q97                  2405.19
TPC-DS Q98                  1258.27
TPC-DS Q99                   906.64

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           1.0          377.0         2.0      769.0    1159.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           2.03

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            5346.28

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                  time [s]  count   SF  Throughput@Size
DBMS               SF  num_experiment num_client                                       
PostgreSQL-BHT-8-1 3.0 1              1               2547      1  3.0           419.79

### Workflow
                               orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
PostgreSQL-BHT-8-1-1  PostgreSQL-BHT-8-1  3.0     8               1           1       1773318683     1773321230

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1]]

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1      834.49     2.57         11.95                18.81

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1        27.2     0.16          0.01                 2.65

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1     3090.76     2.69         12.25                18.95

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1        22.1     0.03          0.33                 0.34

### Application Metrics

#### Loading phase: SUT deployment
                    Number of Idle Sessions  Number of Idle-in-transaction Sessions  Number of Idle-in-transaction Aborted Sessions  Number of Active Sessions  Number of Active Application Sessions
PostgreSQL-BHT-8-1                        1                                       0                                               0                          9                                      8

#### Execution phase: SUT deployment
                    Number of Idle Sessions  Number of Idle-in-transaction Sessions  Number of Idle-in-transaction Aborted Sessions  Number of Active Sessions  Number of Active Application Sessions
PostgreSQL-BHT-8-1                        1                                       0                                               0                          6                                      6

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
