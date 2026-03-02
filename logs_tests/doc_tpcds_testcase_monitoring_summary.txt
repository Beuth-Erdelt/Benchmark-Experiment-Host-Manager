## Show Summary

### Workload
TPC-DS Queries SF=3
    Type: tpcds
    Duration: 969s 
    Code: 1772470683
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.21.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['MonetDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Dec2025
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:159764
    cpu_list:0-63
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    eval_parameters
        code:1772470683

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1
TPC-DS Q1                  54.82
TPC-DS Q2                 640.48
TPC-DS Q3                  40.08
TPC-DS Q4                4019.00
TPC-DS Q5                 292.97
TPC-DS Q6                 253.23
TPC-DS Q7                  83.79
TPC-DS Q8                  96.75
TPC-DS Q9                 140.66
TPC-DS Q10                 84.49
TPC-DS Q11               1914.95
TPC-DS Q12                 34.65
TPC-DS Q13                147.68
TPC-DS Q14a+b            7730.64
TPC-DS Q15                 54.92
TPC-DS Q16                323.98
TPC-DS Q17                479.92
TPC-DS Q18                248.64
TPC-DS Q19                 81.21
TPC-DS Q20                 45.67
TPC-DS Q21                 94.35
TPC-DS Q22               2645.45
TPC-DS Q23a+b            7029.47
TPC-DS Q24a+b             828.27
TPC-DS Q25                376.51
TPC-DS Q26                 78.63
TPC-DS Q27                336.99
TPC-DS Q28                190.21
TPC-DS Q29                245.80
TPC-DS Q30                 41.77
TPC-DS Q31                562.71
TPC-DS Q32                 40.60
TPC-DS Q33                 46.71
TPC-DS Q34                 61.28
TPC-DS Q35                191.14
TPC-DS Q36                231.86
TPC-DS Q37                 94.15
TPC-DS Q38                593.42
TPC-DS Q39a+b            4384.57
TPC-DS Q40                218.58
TPC-DS Q41                  6.91
TPC-DS Q42                 45.94
TPC-DS Q43                102.80
TPC-DS Q44                 76.26
TPC-DS Q45                 25.51
TPC-DS Q46                 90.67
TPC-DS Q47                550.42
TPC-DS Q48                 96.64
TPC-DS Q49                332.49
TPC-DS Q50                252.10
TPC-DS Q51               1440.98
TPC-DS Q52                 34.32
TPC-DS Q53                 50.18
TPC-DS Q54                 50.74
TPC-DS Q55                 26.93
TPC-DS Q56                 62.76
TPC-DS Q57                182.03
TPC-DS Q58                184.02
TPC-DS Q59                318.27
TPC-DS Q60                 48.86
TPC-DS Q61                 76.92
TPC-DS Q62                 47.70
TPC-DS Q63                 49.13
TPC-DS Q64               1407.74
TPC-DS Q65                371.57
TPC-DS Q66                301.20
TPC-DS Q67               1361.97
TPC-DS Q68                 88.02
TPC-DS Q69                 36.55
TPC-DS Q70                232.11
TPC-DS Q71                 65.57
TPC-DS Q72                259.36
TPC-DS Q73                 42.85
TPC-DS Q74                510.08
TPC-DS Q75               1618.80
TPC-DS Q76                154.38
TPC-DS Q77                175.46
TPC-DS Q78               3096.44
TPC-DS Q79                 91.68
TPC-DS Q80               2298.91
TPC-DS Q81                 46.15
TPC-DS Q82                396.67
TPC-DS Q83                 22.94
TPC-DS Q84                123.75
TPC-DS Q85                 54.78
TPC-DS Q86                 61.82
TPC-DS Q87                734.82
TPC-DS Q88                176.56
TPC-DS Q89                 63.74
TPC-DS Q90                 15.53
TPC-DS Q91                 25.07
TPC-DS Q92                 20.35
TPC-DS Q93                463.40
TPC-DS Q94                 73.16
TPC-DS Q95               1132.99
TPC-DS Q96                 24.18
TPC-DS Q97                870.83
TPC-DS Q98                 82.00
TPC-DS Q99                 97.43

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           1.0          256.0        10.0      622.0     897.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1           0.18

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           64987.44

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                               time [s]  count   SF  Throughput@Size
DBMS            SF  num_experiment num_client                                       
MonetDB-BHT-8-1 3.0 1              1                 68      1  3.0         15723.53

### Workflow
                         orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
MonetDB-BHT-8-1-1  MonetDB-BHT-8-1  3.0     8               1           1       1772471533     1772471601

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1]]

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       32.56     0.21          0.01                 2.21

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1      116.88     2.07          6.66                15.16

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       15.07      0.3          0.33                 0.34

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
