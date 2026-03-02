## Show Summary

### Workload
TPC-DS Queries SF=1
    Type: tpcds
    Duration: 994s 
    Code: 1772393584
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.21.
    Experiment is limited to DBMS ['MonetDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Database is persisted to disk of type shared and size 10Gi.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
MonetDB-BHT-8-1-1-1 uses docker image monetdb/monetdb:Dec2025
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:147505
    volume_size:10G
    volume_used:5.3G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1772393584
MonetDB-BHT-8-2-1-1 uses docker image monetdb/monetdb:Dec2025
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:147505
    volume_size:10G
    volume_used:5.5G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1772393584

### Errors (failed queries)
No errors

### Warnings (result mismatch)
               MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-2-1-1
TPC-DS Q39a+b                False                 True

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-2-1-1
TPC-DS Q1                    49.50               382.91
TPC-DS Q2                   224.70               624.01
TPC-DS Q3                    37.58               733.46
TPC-DS Q4                  1220.85              3308.45
TPC-DS Q5                   123.94              1311.40
TPC-DS Q6                    66.84               482.78
TPC-DS Q7                    59.21              2005.29
TPC-DS Q8                    46.45               195.00
TPC-DS Q9                    74.71               261.80
TPC-DS Q10                   38.04              4754.01
TPC-DS Q11                  577.90               611.12
TPC-DS Q12                   20.53               125.15
TPC-DS Q13                   63.28               593.12
TPC-DS Q14a+b              2532.78              2382.43
TPC-DS Q15                   31.06                26.74
TPC-DS Q16                   39.87               996.52
TPC-DS Q17                  180.99               245.55
TPC-DS Q18                  135.37               203.23
TPC-DS Q19                   37.35               129.01
TPC-DS Q20                   24.13                21.32
TPC-DS Q21                  100.52              2939.91
TPC-DS Q22                 1060.82              1096.96
TPC-DS Q23a+b              2495.09              2835.67
TPC-DS Q24a+b               226.58               400.17
TPC-DS Q25                   87.97                95.19
TPC-DS Q26                   18.61                20.67
TPC-DS Q27                  104.26               123.99
TPC-DS Q28                   64.81                78.66
TPC-DS Q29                  102.96               105.35
TPC-DS Q30                   21.01               159.98
TPC-DS Q31                  167.34               167.23
TPC-DS Q32                   15.52                16.90
TPC-DS Q33                   20.44               178.57
TPC-DS Q34                   35.55               277.54
TPC-DS Q35                   77.23                92.12
TPC-DS Q36                  114.08               136.06
TPC-DS Q37                  154.83               133.06
TPC-DS Q38                  183.74               202.12
TPC-DS Q39a+b              1425.49              1417.17
TPC-DS Q40                   73.62                51.32
TPC-DS Q41                    6.42                 6.29
TPC-DS Q42                   18.00                17.76
TPC-DS Q43                   42.47                58.28
TPC-DS Q44                   31.30                34.21
TPC-DS Q45                   13.24                38.48
TPC-DS Q46                   42.26               205.96
TPC-DS Q47                  232.75               310.91
TPC-DS Q48                   46.49                46.75
TPC-DS Q49                  111.96               622.13
TPC-DS Q50                  100.55               302.09
TPC-DS Q51                  491.17               489.54
TPC-DS Q52                   22.25                19.07
TPC-DS Q53                   28.20                24.53
TPC-DS Q54                   26.20                26.40
TPC-DS Q55                   16.45                15.46
TPC-DS Q56                   26.43                47.78
TPC-DS Q57                   98.95               135.64
TPC-DS Q58                   55.34                58.92
TPC-DS Q59                  119.42               108.28
TPC-DS Q60                   23.13                26.63
TPC-DS Q61                   32.48               105.07
TPC-DS Q62                   66.97                49.24
TPC-DS Q63                   24.21                26.22
TPC-DS Q64                  413.92               743.14
TPC-DS Q65                   84.99               117.99
TPC-DS Q66                   92.71               156.43
TPC-DS Q67                  396.26               426.44
TPC-DS Q68                   38.49                43.67
TPC-DS Q69                   30.02                68.51
TPC-DS Q70                   88.86               472.64
TPC-DS Q71                   28.69                30.84
TPC-DS Q72                  174.28              1639.27
TPC-DS Q73                   21.64                22.23
TPC-DS Q74                  177.75               196.59
TPC-DS Q75                  482.02               475.17
TPC-DS Q76                   88.82               510.07
TPC-DS Q77                   53.73               178.20
TPC-DS Q78                  736.69               796.39
TPC-DS Q79                   42.33                44.56
TPC-DS Q80                  403.57               402.21
TPC-DS Q81                   28.27               137.01
TPC-DS Q82                  230.27               252.52
TPC-DS Q83                   26.19                20.30
TPC-DS Q84                   12.69                92.47
TPC-DS Q85                   87.70               107.51
TPC-DS Q86                   23.94                24.06
TPC-DS Q87                  234.34               258.76
TPC-DS Q88                   90.91               221.56
TPC-DS Q89                   38.39                35.34
TPC-DS Q90                   16.73                13.36
TPC-DS Q91                   22.74                56.20
TPC-DS Q92                   11.34                12.71
TPC-DS Q93                   92.58               102.11
TPC-DS Q94                   18.93                18.24
TPC-DS Q95                  250.97               242.09
TPC-DS Q96                   16.87                10.81
TPC-DS Q97                  249.06               217.81
TPC-DS Q98                   38.32                37.12
TPC-DS Q99                   59.70                56.18

### Loading [s]
                     timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1-1           1.0           99.0        12.0      323.0     442.0
MonetDB-BHT-8-2-1-1           1.0           99.0        12.0      323.0     442.0

### Geometric Mean of Medians of Timer Run [s]
                     Geo Times [s]
DBMS                              
MonetDB-BHT-8-1-1-1           0.08
MonetDB-BHT-8-2-1-1           0.15

### Power@Size ((3600*SF)/(geo times))
                     Power@Size [~Q/h]
DBMS                                  
MonetDB-BHT-8-1-1-1           49560.53
MonetDB-BHT-8-2-1-1           25877.47

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                 time [s]  count   SF  Throughput@Size
DBMS              SF  num_experiment num_client                                       
MonetDB-BHT-8-1-1 1.0 1              1                 28      1  1.0         12728.57
MonetDB-BHT-8-2-1 1.0 2              1                101      1  1.0          3528.71

### Workflow
                             orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-1-1  1.0     8               1           1       1772394114     1772394142
MonetDB-BHT-8-2-1-1  MonetDB-BHT-8-2-1  1.0     8               2           1       1772394411     1772394512

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1], [1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1], [1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST failed: SQL warnings (result mismatch)
TEST passed: Workflow as planned
