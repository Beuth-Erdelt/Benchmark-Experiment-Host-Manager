## Show Summary

### Workload
TPC-DS Queries SF=10
    Type: tpcds
    Duration: 23147s 
    Code: 1750159279
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
    Database is persisted to disk of type shared and size 100Gi.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
PostgreSQL-BHT-8-1-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:392867964
    datadisk:55265
    volume_size:100G
    volume_used:54G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750159279
PostgreSQL-BHT-8-1-2-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393427956
    datadisk:55265
    volume_size:100G
    volume_used:54G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750159279
PostgreSQL-BHT-8-1-2-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393427956
    datadisk:55265
    volume_size:100G
    volume_used:54G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750159279
PostgreSQL-BHT-8-2-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393519928
    datadisk:55265
    volume_size:100G
    volume_used:54G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750159279
PostgreSQL-BHT-8-2-2-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393442192
    datadisk:55265
    volume_size:100G
    volume_used:54G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750159279
PostgreSQL-BHT-8-2-2-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393442192
    datadisk:55265
    volume_size:100G
    volume_used:54G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750159279

### Errors (failed queries)
            PostgreSQL-BHT-8-1-1-1  PostgreSQL-BHT-8-1-2-1  PostgreSQL-BHT-8-1-2-2  PostgreSQL-BHT-8-2-1-1  PostgreSQL-BHT-8-2-2-1  PostgreSQL-BHT-8-2-2-2
TPC-DS Q6                     True                    True                    True                    True                    True                    True
TPC-DS Q30                    True                    True                    True                    True                    True                    True
TPC-DS Q81                    True                    True                    True                    True                    True                    True
TPC-DS Q6
PostgreSQL-BHT-8-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
PostgreSQL-BHT-8-2-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
PostgreSQL-BHT-8-1-2-2: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
PostgreSQL-BHT-8-2-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
PostgreSQL-BHT-8-1-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
PostgreSQL-BHT-8-2-2-2: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
TPC-DS Q30
PostgreSQL-BHT-8-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
PostgreSQL-BHT-8-2-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
PostgreSQL-BHT-8-1-2-2: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
PostgreSQL-BHT-8-2-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
PostgreSQL-BHT-8-1-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
PostgreSQL-BHT-8-2-2-2: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
TPC-DS Q81
PostgreSQL-BHT-8-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
PostgreSQL-BHT-8-2-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
PostgreSQL-BHT-8-1-2-2: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
PostgreSQL-BHT-8-2-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
PostgreSQL-BHT-8-1-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
PostgreSQL-BHT-8-2-2-2: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request

### Warnings (result mismatch)
               PostgreSQL-BHT-8-1-1-1  PostgreSQL-BHT-8-1-2-1  PostgreSQL-BHT-8-1-2-2  PostgreSQL-BHT-8-2-1-1  PostgreSQL-BHT-8-2-2-1  PostgreSQL-BHT-8-2-2-2
TPC-DS Q39a+b                   False                    True                    True                    True                    True                    True

### Latency of Timer Execution [ms]
DBMS           PostgreSQL-BHT-8-1-1-1  PostgreSQL-BHT-8-1-2-1  PostgreSQL-BHT-8-1-2-2  PostgreSQL-BHT-8-2-1-1  PostgreSQL-BHT-8-2-2-1  PostgreSQL-BHT-8-2-2-2
TPC-DS Q1                     2456.38                 2469.70                 2436.25                14339.18                 2467.55                 2439.87
TPC-DS Q2                     5049.66                 5050.39                 5071.91                47856.75                 4967.57                 5007.34
TPC-DS Q3                     5393.67                 5399.32                 5500.10                60991.73                 5258.80                 5273.36
TPC-DS Q4                   106379.64               110400.24               109882.11               110941.69               110777.12               109492.45
TPC-DS Q5                     9715.65                 9824.82                 9795.04                15269.64                 9589.39                 9513.19
TPC-DS Q7                     4640.38                 4696.11                 4786.86                 7306.53                 4504.70                 4604.13
TPC-DS Q8                     3611.10                 3657.04                 3696.83                 3349.92                 3375.57                 3302.09
TPC-DS Q9                    16367.75                16607.21                16748.00                14669.80                15178.13                15319.21
TPC-DS Q10                    6205.78                 6306.41                 6421.02                 7149.30                 5924.31                 6126.72
TPC-DS Q11                   97335.50                99865.83               100436.26                99400.70                99768.93               101417.22
TPC-DS Q12                    1110.12                 1101.04                 1101.79                 1130.43                 1157.47                 1128.53
TPC-DS Q13                    7256.05                 7325.09                 7378.14                 7113.73                 7081.42                 7123.82
TPC-DS Q14a+b                53240.69                53277.69                53366.11                52731.43                52748.78                53242.74
TPC-DS Q15                    2161.79                 2220.80                 2180.87                 2119.54                 2064.19                 2169.26
TPC-DS Q16                    4440.83                 4448.57                 4475.16                 4777.87                 4305.09                 4395.52
TPC-DS Q17                    6894.15                 6918.78                 7181.62                 6891.69                 6655.20                 6827.13
TPC-DS Q18                    6977.89                 6970.12                 7077.19                 6961.44                 6865.14                 7023.47
TPC-DS Q19                    5155.43                 5121.34                 5161.84                 5065.43                 4996.37                 5216.50
TPC-DS Q20                    2009.70                 2048.48                 2014.79                 1916.81                 1903.29                 2007.40
TPC-DS Q21                    5734.20                 5777.55                 5763.22                40861.17                 5331.35                 5369.08
TPC-DS Q22                  107204.17               109667.97               108483.16               108665.23               108349.97               107861.67
TPC-DS Q23a+b                95240.69                94400.39                95100.04                95703.67                95149.35                95939.38
TPC-DS Q24a+b                11775.63                11725.45                11954.48                11438.44                11600.07                11661.13
TPC-DS Q25                    7256.25                 7203.60                 7380.91                 6870.98                 6930.24                 7000.26
TPC-DS Q26                    3409.14                 3417.37                 3478.92                 3284.86                 3371.43                 3405.56
TPC-DS Q27                    5777.23                 5911.11                 5865.82                 5654.66                 5634.64                 5779.77
TPC-DS Q28                   13170.80                13438.49                13399.34                12087.29                12268.11                12367.06
TPC-DS Q29                    7345.62                 7538.70                 7512.28                 6978.86                 7145.90                 7264.45
TPC-DS Q31                   16504.69                16534.17                16697.78                16084.99                16175.12                16674.65
TPC-DS Q32                    1208.37                 1231.37                 1304.67                 2455.93                 1020.34                 1048.53
TPC-DS Q33                   10815.68                10834.49                10814.61                10465.83                10496.43                10556.20
TPC-DS Q34                     767.72                  757.06                  755.25                  764.31                  766.85                  770.81
TPC-DS Q35                    7483.19                 7584.95                 7587.86                 7182.30                 7189.49                 7231.51
TPC-DS Q36                    1037.77                 1026.07                 1037.82                 1058.05                 1036.04                 1073.50
TPC-DS Q37                    6043.04                 6138.99                 6046.42                 5631.09                 5618.38                 5602.03
TPC-DS Q38                   20842.87                21005.73                20864.65                20046.23                21037.33                20612.58
TPC-DS Q39a+b                80141.48                78485.64                78597.98                78022.09                81625.12                80653.51
TPC-DS Q40                    3314.36                 3344.05                 3322.04                 3270.46                 3258.80                 3260.52
TPC-DS Q41                   96822.93                97363.95                80764.43                86282.49                75644.11                88283.96
TPC-DS Q42                    2853.15                 2868.44                 2879.45                 2596.81                 3098.62                 2582.16
TPC-DS Q43                    1856.21                 1826.80                 1845.28                 1835.52                 1876.18                 1901.62
TPC-DS Q44                       5.76                    7.57                    3.22                  135.84                    3.04                    3.32
TPC-DS Q45                    1334.80                 1320.33                 1300.07                 1353.10                 1380.78                 1381.54
TPC-DS Q46                    1346.64                 1343.02                 1339.49                 1349.18                 1373.64                 1395.91
TPC-DS Q47                   26977.24                26850.85                26890.46                25957.14                26443.93                25859.79
TPC-DS Q48                    7066.83                 7176.76                 7095.16                 6928.51                 6933.19                 7154.10
TPC-DS Q49                   11877.35                11996.67                12082.59                11656.19                11760.97                11722.23
TPC-DS Q50                    7855.17                 7871.39                 8243.97                 7852.53                 8222.55                 8030.90
TPC-DS Q51                   27814.01                28036.39                28289.29                27519.49                28684.01                27762.99
TPC-DS Q52                    2804.80                 2808.18                 2964.82                 2552.18                 2461.57                 2541.00
TPC-DS Q53                    3014.82                 3018.68                 2984.75                 2737.54                 2761.46                 2786.93
TPC-DS Q54                    2594.91                 2558.95                 2576.80                 2579.04                 2415.01                 2666.66
TPC-DS Q55                    2722.38                 2698.30                 2803.59                 2452.53                 2888.84                 2491.71
TPC-DS Q56                    9471.35                 9509.33                 9388.58                 9112.23                 9331.43                 9201.84
TPC-DS Q57                   19320.36                19817.78                19559.55                19176.14                19201.53                19122.27
TPC-DS Q58                    8701.34                 8742.50                 8752.68                 8259.98                 8443.12                 8632.24
TPC-DS Q59                    9460.51                 9527.66                 9557.54                 9232.88                 9474.46                 9504.37
TPC-DS Q60                   10473.95                10443.02                10452.93                10082.56                10348.60                10453.34
TPC-DS Q61                    4442.54                 4415.83                 4435.60                 4414.17                 4493.08                 4420.42
TPC-DS Q62                    1851.86                 1847.60                 1848.98                 1907.85                 1833.27                 1854.14
TPC-DS Q63                    3057.52                 3054.67                 3063.21                 2773.24                 2818.54                 2853.31
TPC-DS Q64                   15830.90                15808.64                15732.90                15484.14                15876.20                15640.85
TPC-DS Q65                   17628.63                17681.58                17655.14                16836.23                17331.19                17319.27
TPC-DS Q66                   10266.40                10859.64                10548.78                10405.56                10247.50                10393.38
TPC-DS Q67                   71277.38                71809.51                74044.88                72062.22                72215.31                72698.74
TPC-DS Q68                    1385.09                 1406.16                 1404.31                 1408.55                 1417.26                 1411.15
TPC-DS Q69                    3402.27                 3428.72                 3425.68                 3267.36                 3308.06                 3230.33
TPC-DS Q70                   10651.70                10609.08                10428.95                10533.59                10703.87                10700.89
TPC-DS Q71                    8567.70                 8514.67                 8537.76                 8266.18                 8710.74                 7993.84
TPC-DS Q72                   35531.09                35987.09                35561.93                36431.34                37070.27                36684.58
TPC-DS Q73                     761.73                  751.66                  743.09                  748.35                  776.28                  760.06
TPC-DS Q74                   28943.27                28408.24                28299.63                27872.92                28379.49                28293.25
TPC-DS Q75                   18924.05                18833.04                18701.12                18610.03                19559.28                18909.53
TPC-DS Q76                    5931.42                 6019.41                 6025.68                 5740.77                 5901.49                 5851.60
TPC-DS Q77                    8306.97                 8329.66                 8219.44                 8097.63                 8107.26                 8049.26
TPC-DS Q78                   46510.95                45380.78                45360.30                45047.98                45952.28                45614.67
TPC-DS Q79                    3822.18                 3892.09                 3824.00                 3579.99                 3577.15                 3643.18
TPC-DS Q80                   11727.05                11762.70                11612.15                11381.43                11719.36                11620.27
TPC-DS Q82                    6647.42                 6250.54                 6357.69                 5776.29                 5829.15                 5716.16
TPC-DS Q83                    1237.01                 1237.66                 1225.60                 1262.31                 1249.56                 1304.83
TPC-DS Q84                     512.32                  519.07                  514.22                  519.19                  533.34                  540.97
TPC-DS Q85                    2808.51                 2787.22                 2791.51                 2848.91                 2836.45                 2838.74
TPC-DS Q86                    3848.43                 3896.61                 3873.40                 3858.34                 3975.24                 3902.26
TPC-DS Q87                   20646.65                20908.22                21090.74                20384.72                20558.47                20614.03
TPC-DS Q88                   14823.44                14959.21                14815.70                13398.07                13687.19                13632.84
TPC-DS Q89                    3420.34                 3462.11                 3494.72                 3153.51                 3247.32                 3198.66
TPC-DS Q90                    3799.15                 3743.38                 3828.34                 3784.38                 3927.32                 3837.19
TPC-DS Q91                     686.73                  690.33                  697.87                  729.45                  727.77                  688.24
TPC-DS Q92                     722.18                  713.35                  723.12                 1173.13                  688.30                  686.60
TPC-DS Q93                    3593.74                 3660.69                 3646.92                 3310.12                 3363.69                 3425.67
TPC-DS Q94                    3914.82                 3873.85                 3887.48                 3927.99                 3905.84                 3889.10
TPC-DS Q95                   70692.91                71640.36                70953.25                71752.03                70697.33                69742.99
TPC-DS Q96                    2152.99                 2151.27                 2128.89                 1896.57                 1909.24                 1925.46
TPC-DS Q97                    8033.35                 7949.67                 7901.25                 7452.92                 7356.08                 7488.79
TPC-DS Q98                    3839.45                 3919.02                 3840.59                 3657.33                 3905.85                 3739.45
TPC-DS Q99                    2989.43                 2960.68                 3020.03                 2856.30                 2826.11                 2928.22

### Loading [s]
                        timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1-1           1.0         1151.0         2.0      771.0    1931.0
PostgreSQL-BHT-8-1-2-1           1.0         1151.0         2.0      771.0    1931.0
PostgreSQL-BHT-8-1-2-2           1.0         1151.0         2.0      771.0    1931.0
PostgreSQL-BHT-8-2-1-1           1.0         1151.0         2.0      771.0    1931.0
PostgreSQL-BHT-8-2-2-1           1.0         1151.0         2.0      771.0    1931.0
PostgreSQL-BHT-8-2-2-2           1.0         1151.0         2.0      771.0    1931.0

### Geometric Mean of Medians of Timer Run [s]
                        Geo Times [s]
DBMS                                 
PostgreSQL-BHT-8-1-1-1           6.24
PostgreSQL-BHT-8-1-2-1           6.28
PostgreSQL-BHT-8-1-2-2           6.23
PostgreSQL-BHT-8-2-1-1           7.02
PostgreSQL-BHT-8-2-2-1           6.08
PostgreSQL-BHT-8-2-2-2           6.09

### Power@Size ((3600*SF)/(geo times))
                        Power@Size [~Q/h]
DBMS                                     
PostgreSQL-BHT-8-1-1-1            5794.75
PostgreSQL-BHT-8-1-2-1            5756.52
PostgreSQL-BHT-8-1-2-2            5804.72
PostgreSQL-BHT-8-2-1-1            5146.08
PostgreSQL-BHT-8-2-2-1            5950.47
PostgreSQL-BHT-8-2-2-2            5937.28

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                     time [s]  count    SF  Throughput@Size
DBMS                 SF   num_experiment num_client                                        
PostgreSQL-BHT-8-1-1 10.0 1              1               5091      1  10.0           678.85
PostgreSQL-BHT-8-1-2 10.0 1              2               5099      2  10.0          1355.56
PostgreSQL-BHT-8-2-1 10.0 2              1               5226      1  10.0           661.31
PostgreSQL-BHT-8-2-2 10.0 2              2               5078      2  10.0          1361.17

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1, 2], [1, 2]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1, 2], [1, 2]]

### Ingestion - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1      3413.3     3.32         25.83                52.93
PostgreSQL-BHT-8-1-2      3413.3     3.32         25.83                52.93

### Ingestion - Loader
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1        57.4     0.04          5.28                11.39
PostgreSQL-BHT-8-1-2        57.4     0.04          5.28                11.39

### Execution - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1     7397.68     4.04         30.20                57.62
PostgreSQL-BHT-8-1-2    14691.20     9.55         35.28                62.70
PostgreSQL-BHT-8-2-1    25579.81     4.06         30.85                62.50
PostgreSQL-BHT-8-2-2    14415.45     6.74         27.47                43.45

### Execution - Benchmarker
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1       31.37     0.02          0.29                 0.30
PostgreSQL-BHT-8-1-2       38.04     0.04          0.80                 0.81
PostgreSQL-BHT-8-2-1       32.66     0.04          0.30                 0.32
PostgreSQL-BHT-8-2-2       38.16     0.55          0.80                 0.84

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST failed: SQL errors
TEST failed: SQL warnings (result mismatch)
TEST passed: Workflow as planned
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
