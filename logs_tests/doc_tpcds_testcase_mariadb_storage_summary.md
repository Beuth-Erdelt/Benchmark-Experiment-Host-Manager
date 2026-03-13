## Show Summary

### Workload
TPC-DS Queries SF=1
    Type: tpcds
    Duration: 12001s 
    Code: 1731412634
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Benchmark is limited to DBMS ['MariaDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
MariaDB-BHT-8-1-1-1 uses docker image mariadb:11.4.2
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:352151620
    datadisk:4680562
    volume_size:30G
    volume_used:4.5G
    requests_cpu:4
    requests_memory:16Gi
MariaDB-BHT-8-2-1-1 uses docker image mariadb:11.4.2
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:352151288
    datadisk:4680587
    volume_size:30G
    volume_used:4.5G
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
            MariaDB-BHT-8-1-1-1  MariaDB-BHT-8-2-1-1
TPC-DS Q72                 True                 True
TPC-DS Q94                 True                 True
TPC-DS Q95                 True                 True
TPC-DS Q72
MariaDB-BHT-8-1-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=6) Query execution was interrupted (max_statement_time exceeded)
MariaDB-BHT-8-2-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=19) Query execution was interrupted (max_statement_time exceeded)
TPC-DS Q94
MariaDB-BHT-8-1-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=6) Query execution was interrupted (max_statement_time exceeded)
MariaDB-BHT-8-2-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=19) Query execution was interrupted (max_statement_time exceeded)
TPC-DS Q95
MariaDB-BHT-8-1-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=6) Query execution was interrupted (max_statement_time exceeded)
MariaDB-BHT-8-2-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=19) Query execution was interrupted (max_statement_time exceeded)

### Warnings (result mismatch)
            MariaDB-BHT-8-1-1-1  MariaDB-BHT-8-2-1-1
TPC-DS Q44                False                 True
TPC-DS Q64                False                 True
TPC-DS Q75                False                 True

### Latency of Timer Execution [ms]
DBMS           MariaDB-BHT-8-1-1-1  MariaDB-BHT-8-2-1-1
TPC-DS Q1                   310.48               185.54
TPC-DS Q2                 15807.47             16423.53
TPC-DS Q3                    68.53                85.74
TPC-DS Q4                 40998.03             40568.70
TPC-DS Q5                 31160.02             30591.55
TPC-DS Q6                  2828.70              2845.70
TPC-DS Q7                 12986.45             12962.24
TPC-DS Q8                  1090.02              1003.78
TPC-DS Q9                 12966.11             13110.65
TPC-DS Q10                 5801.84               211.33
TPC-DS Q11                26469.94             26252.48
TPC-DS Q12                  930.99               917.50
TPC-DS Q13                 3044.79              3419.94
TPC-DS Q14a+b            153160.81            156750.29
TPC-DS Q15                  538.63               524.24
TPC-DS Q16                30965.08             32520.57
TPC-DS Q17                 2523.00              4049.98
TPC-DS Q18                 6952.92              8125.14
TPC-DS Q19                  670.72               775.37
TPC-DS Q20                 1741.43              2017.67
TPC-DS Q21                78953.37             85001.64
TPC-DS Q22                  583.33               542.82
TPC-DS Q23a+b            208067.62            206688.19
TPC-DS Q24a+b               191.86               195.61
TPC-DS Q25                  479.49               337.49
TPC-DS Q26                 2719.52              2690.06
TPC-DS Q27                 4839.41              4823.07
TPC-DS Q28                 9705.08              9662.90
TPC-DS Q29                  131.87               129.78
TPC-DS Q30                  305.06               304.10
TPC-DS Q31                 4121.85              4144.71
TPC-DS Q32                   24.33                23.53
TPC-DS Q33                  443.62               442.93
TPC-DS Q34                11609.30             11490.51
TPC-DS Q35                 3227.21              3191.36
TPC-DS Q36                 5323.12              5274.71
TPC-DS Q37                13483.22             13377.74
TPC-DS Q38                26446.68             26202.24
TPC-DS Q39a+b              4700.43              4634.06
TPC-DS Q40                  724.67               721.64
TPC-DS Q41                 1428.85              1418.86
TPC-DS Q42                  737.05               667.05
TPC-DS Q43                 3408.59              3370.53
TPC-DS Q44                 8680.18              4114.60
TPC-DS Q45                  393.42               390.68
TPC-DS Q46                13785.23             13634.88
TPC-DS Q47                43146.95             43212.60
TPC-DS Q48                 3332.73              3319.76
TPC-DS Q49                 1000.61              1040.34
TPC-DS Q50                  155.24                93.78
TPC-DS Q51                26541.81             26819.16
TPC-DS Q52                  644.78               757.36
TPC-DS Q53                  628.97               620.17
TPC-DS Q54                 2723.57              2891.77
TPC-DS Q55                  625.11               722.57
TPC-DS Q56                  593.53               637.57
TPC-DS Q57                20656.77             20800.62
TPC-DS Q58                22874.78             23225.74
TPC-DS Q59                39042.15             37906.37
TPC-DS Q60                 1817.23              1934.15
TPC-DS Q61                 1087.65              1100.87
TPC-DS Q62                 7009.46              6930.01
TPC-DS Q63                  624.74               614.14
TPC-DS Q64                 2045.59              2072.67
TPC-DS Q65                22435.53             22393.55
TPC-DS Q66                 3819.54              3936.19
TPC-DS Q67                27811.54             28163.04
TPC-DS Q68                12277.18             12131.46
TPC-DS Q69                   79.34                 2.56
TPC-DS Q70                32547.97             32223.83
TPC-DS Q71                 1277.32              1269.88
TPC-DS Q73                11263.01             11120.92
TPC-DS Q74                19148.88             19171.27
TPC-DS Q75                17586.58             17280.21
TPC-DS Q76                 3261.06              1401.92
TPC-DS Q77                23873.30             23583.15
TPC-DS Q78                18745.34             18887.04
TPC-DS Q79                12577.30             12208.73
TPC-DS Q80                 2251.75              2192.87
TPC-DS Q81                 1644.66               659.22
TPC-DS Q82                14234.32             13446.92
TPC-DS Q83                 3509.46              3435.86
TPC-DS Q84                  636.52               151.14
TPC-DS Q85                  515.63               424.60
TPC-DS Q86                 3712.97              3582.47
TPC-DS Q87                27217.73             26016.17
TPC-DS Q88                90031.60             88284.36
TPC-DS Q89                 5120.31              4972.55
TPC-DS Q90                  370.59               369.35
TPC-DS Q91                  158.31                55.37
TPC-DS Q92                   15.53                15.19
TPC-DS Q93                  188.71                95.76
TPC-DS Q96                 9531.48              9476.81
TPC-DS Q97                18766.33             19046.13
TPC-DS Q98                 3400.33              3727.77
TPC-DS Q99                22672.65             16810.82

### Loading [s]
                     timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MariaDB-BHT-8-1-1-1           1.0          751.0         4.0    16525.0   17288.0
MariaDB-BHT-8-2-1-1           1.0          751.0         4.0    16525.0   17288.0

### Geometric Mean of Medians of Timer Run [s]
                     Geo Times [s]
DBMS                              
MariaDB-BHT-8-1-1-1           3.34
MariaDB-BHT-8-2-1-1           2.92

### Power@Size
                     Power@Size [~Q/h]
DBMS                                  
MariaDB-BHT-8-1-1-1            1080.52
MariaDB-BHT-8-2-1-1            1237.17

### Throughput@Size
                                                time [s]  count  SF  Throughput@Size [~GB/h]
DBMS              SF num_experiment num_client                                              
MariaDB-BHT-8-1-1 1  1              1               4966      1   1                    15.95
MariaDB-BHT-8-2-1 1  2              1               4956      1   1                    15.98

### Workflow

#### Actual
DBMS MariaDB-BHT-8 - Pods [[1], [1]]

#### Planned
DBMS MariaDB-BHT-8 - Pods [[1], [1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST failed: SQL errors
TEST failed: SQL warnings (result mismatch)
TEST passed: Workflow as planned
