## Show Summary

### Workload
TPC-DS Queries SF=10
    Type: tpcds
    Duration: 7431s 
    Code: 1750151567
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=10) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.8.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:449714548
    datadisk:55281
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750151567

### Errors (failed queries)
            PostgreSQL-BHT-8-1-1
TPC-DS Q6                   True
TPC-DS Q30                  True
TPC-DS Q81                  True
TPC-DS Q6
PostgreSQL-BHT-8-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
TPC-DS Q30
PostgreSQL-BHT-8-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
TPC-DS Q81
PostgreSQL-BHT-8-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           PostgreSQL-BHT-8-1-1
TPC-DS Q1                   2634.37
TPC-DS Q2                   5235.23
TPC-DS Q3                   2870.39
TPC-DS Q4                 107415.41
TPC-DS Q5                   9899.03
TPC-DS Q7                   4716.17
TPC-DS Q8                   3664.65
TPC-DS Q9                  16777.37
TPC-DS Q10                  6345.62
TPC-DS Q11                 97696.55
TPC-DS Q12                  1134.51
TPC-DS Q13                  7455.15
TPC-DS Q14a+b              52583.06
TPC-DS Q15                  2239.03
TPC-DS Q16                  4575.63
TPC-DS Q17                  6970.03
TPC-DS Q18                  7033.56
TPC-DS Q19                  5036.13
TPC-DS Q20                  1963.22
TPC-DS Q21                  5690.08
TPC-DS Q22                111627.69
TPC-DS Q23a+b             118299.71
TPC-DS Q24a+b              11846.23
TPC-DS Q25                  7389.72
TPC-DS Q26                  3483.94
TPC-DS Q27                  5951.02
TPC-DS Q28                 13347.63
TPC-DS Q29                  7198.26
TPC-DS Q31                 16926.45
TPC-DS Q32                  1298.98
TPC-DS Q33                 10911.03
TPC-DS Q34                   774.52
TPC-DS Q35                  7675.22
TPC-DS Q36                  8382.58
TPC-DS Q37                  6053.16
TPC-DS Q38                 20623.60
TPC-DS Q39a+b              77756.41
TPC-DS Q40                  3311.95
TPC-DS Q41                 90664.06
TPC-DS Q42                  2884.14
TPC-DS Q43                  4509.95
TPC-DS Q44                  7515.71
TPC-DS Q45                  1348.52
TPC-DS Q46                  1392.16
TPC-DS Q47                 26127.03
TPC-DS Q48                  7030.54
TPC-DS Q49                 11863.25
TPC-DS Q50                  8076.05
TPC-DS Q51                 27973.61
TPC-DS Q52                  2840.38
TPC-DS Q53                  3151.07
TPC-DS Q54                  2620.48
TPC-DS Q55                  2704.18
TPC-DS Q56                  9956.28
TPC-DS Q57                 19399.61
TPC-DS Q58                  8875.07
TPC-DS Q59                  9449.10
TPC-DS Q60                 10445.78
TPC-DS Q61                  4459.86
TPC-DS Q62                  1866.80
TPC-DS Q63                  3101.14
TPC-DS Q64                 15865.04
TPC-DS Q65                 18222.22
TPC-DS Q66                 10258.60
TPC-DS Q67                 70472.91
TPC-DS Q68                  1451.97
TPC-DS Q69                  5116.28
TPC-DS Q70                 10512.15
TPC-DS Q71                  8546.26
TPC-DS Q72                 37283.95
TPC-DS Q73                   758.84
TPC-DS Q74                 25089.08
TPC-DS Q75                 22688.67
TPC-DS Q76                  6019.57
TPC-DS Q77                  8275.49
TPC-DS Q78                 45298.51
TPC-DS Q79                  5242.64
TPC-DS Q80                 11696.92
TPC-DS Q82                  6321.02
TPC-DS Q83                  1178.78
TPC-DS Q84                   510.23
TPC-DS Q85                  2914.20
TPC-DS Q86                  3898.90
TPC-DS Q87                 20672.32
TPC-DS Q88                 14858.10
TPC-DS Q89                  3587.25
TPC-DS Q90                  3761.34
TPC-DS Q91                   677.39
TPC-DS Q92                   721.17
TPC-DS Q93                  3704.76
TPC-DS Q94                  3875.99
TPC-DS Q95                 70045.35
TPC-DS Q96                  2127.91
TPC-DS Q97                  7919.80
TPC-DS Q98                  3728.64
TPC-DS Q99                  3033.00

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           1.0         1222.0         1.0      798.0    2030.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           7.01

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            5159.09

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                   time [s]  count    SF  Throughput@Size
DBMS               SF   num_experiment num_client                                        
PostgreSQL-BHT-8-1 10.0 1              1               5130      1  10.0           673.68

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1]]

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1     3561.37     3.33         27.82                54.66

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       57.09     0.07          5.31                11.39

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1     7478.18     3.51         29.49                56.24

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       31.65     0.04           0.3                  0.3

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST failed: SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
