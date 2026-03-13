## Show Summary

### Workload
TPC-DS Queries SF=30
    Type: tpcds
    Duration: 2117s 
    Code: 1772477169
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=30) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 14400.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.21.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['MonetDB'].
    Import is handled by 8 processes (pods).
    Database is persisted to disk of type shared and size 1000Gi. Persistent storage is removed at experiment start.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Dec2025
    RAM:2164173176832
    CPU:INTEL(R) XEON(R) PLATINUM 8570
    Cores:224
    host:6.8.0-90-generic
    node:cl-worker36
    disk:1191991
    volume_size:1000G
    volume_used:74G
    cpu_list:0-223
    requests_cpu:4
    requests_memory:1024Gi
    limits_memory:1024Gi
    eval_parameters
        code:1772477169

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1
TPC-DS Q1                 193.27
TPC-DS Q2                1526.60
TPC-DS Q3                 380.82
TPC-DS Q4               14935.93
TPC-DS Q5                1541.80
TPC-DS Q6                 649.31
TPC-DS Q7                 439.74
TPC-DS Q8                 384.51
TPC-DS Q9                 729.72
TPC-DS Q10                188.86
TPC-DS Q11               6298.10
TPC-DS Q12                147.34
TPC-DS Q13                631.75
TPC-DS Q14a+b           30432.64
TPC-DS Q15                232.85
TPC-DS Q16              39752.83
TPC-DS Q17               2337.01
TPC-DS Q18               1060.14
TPC-DS Q19                241.70
TPC-DS Q20                108.09
TPC-DS Q21                231.53
TPC-DS Q22               1063.13
TPC-DS Q23a+b           48877.88
TPC-DS Q24a+b           10765.56
TPC-DS Q25               2444.36
TPC-DS Q26                278.23
TPC-DS Q27               1638.08
TPC-DS Q28               1104.57
TPC-DS Q29               2209.12
TPC-DS Q30                 97.37
TPC-DS Q31               1810.39
TPC-DS Q32                140.76
TPC-DS Q33                135.26
TPC-DS Q34                332.76
TPC-DS Q35                919.98
TPC-DS Q36               1095.37
TPC-DS Q37                561.93
TPC-DS Q38               2449.73
TPC-DS Q39a+b            1039.45
TPC-DS Q40               1121.32
TPC-DS Q41                  4.98
TPC-DS Q42                 87.49
TPC-DS Q43                217.30
TPC-DS Q44               5426.16
TPC-DS Q45                163.15
TPC-DS Q46                196.36
TPC-DS Q47                819.24
TPC-DS Q48                445.06
TPC-DS Q49               1180.53
TPC-DS Q50                731.27
TPC-DS Q51               2320.06
TPC-DS Q52                 77.56
TPC-DS Q53                106.32
TPC-DS Q54                107.43
TPC-DS Q55                 69.33
TPC-DS Q56                215.84
TPC-DS Q57                184.76
TPC-DS Q58                616.98
TPC-DS Q59                885.19
TPC-DS Q60                159.01
TPC-DS Q61                181.21
TPC-DS Q62                499.11
TPC-DS Q63                109.98
TPC-DS Q64               4943.99
TPC-DS Q65               1176.64
TPC-DS Q66               1530.81
TPC-DS Q67               5031.62
TPC-DS Q68                300.06
TPC-DS Q69                396.97
TPC-DS Q70               1459.57
TPC-DS Q71                385.23
TPC-DS Q72               1418.80
TPC-DS Q73                136.81
TPC-DS Q74               1874.97
TPC-DS Q75               5674.84
TPC-DS Q76               6814.96
TPC-DS Q77                785.78
TPC-DS Q78              11417.69
TPC-DS Q79                262.48
TPC-DS Q80               8096.49
TPC-DS Q81                162.02
TPC-DS Q82                512.69
TPC-DS Q83                110.86
TPC-DS Q84                 51.48
TPC-DS Q85                424.81
TPC-DS Q86                327.47
TPC-DS Q87               3162.41
TPC-DS Q88               1022.97
TPC-DS Q89                260.37
TPC-DS Q90                130.10
TPC-DS Q91                 30.01
TPC-DS Q92                146.50
TPC-DS Q93               2205.86
TPC-DS Q94              37402.72
TPC-DS Q95             425489.83
TPC-DS Q96               3739.14
TPC-DS Q97               3242.70
TPC-DS Q98                413.30
TPC-DS Q99               1472.86

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           1.0          257.0        11.0     1070.0    1376.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1           0.76

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1          147316.59

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                time [s]  count    SF  Throughput@Size
DBMS            SF   num_experiment num_client                                        
MonetDB-BHT-8-1 30.0 1              1                747      1  30.0         14313.25

### Workflow
                         orig_name    SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
MonetDB-BHT-8-1-1  MonetDB-BHT-8-1  30.0     8               1           1       1772478466     1772479213

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1]]

### Ingestion - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1     2418.14    12.11         73.33                73.35

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1      262.31     1.54          0.02                 6.08

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1    26665.86   155.19       1001.41               1024.0

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       26.94     0.12          0.37                 0.38

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
