## Show Summary

### Workload
TPC-DS Queries SF=30
    Type: tpcds
    Duration: 1771s 
    Code: 1772481803
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
    Database is persisted to disk of type shared and size 1000Gi.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 1, 3] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Dec2025
    RAM:2164173176832
    CPU:INTEL(R) XEON(R) PLATINUM 8570
    Cores:224
    host:6.8.0-90-generic
    node:cl-worker36
    disk:1191989
    volume_size:1000G
    volume_used:74G
    cpu_list:0-223
    requests_cpu:4
    requests_memory:1024Gi
    limits_memory:1024Gi
    eval_parameters
        code:1772481803
MonetDB-BHT-8-2-1 uses docker image monetdb/monetdb:Dec2025
    RAM:2164173176832
    CPU:INTEL(R) XEON(R) PLATINUM 8570
    Cores:224
    host:6.8.0-90-generic
    node:cl-worker36
    disk:1191974
    volume_size:1000G
    volume_used:74G
    cpu_list:0-223
    requests_cpu:4
    requests_memory:1024Gi
    limits_memory:1024Gi
    eval_parameters
        code:1772481803
MonetDB-BHT-8-3-1 uses docker image monetdb/monetdb:Dec2025
    RAM:2164173176832
    CPU:INTEL(R) XEON(R) PLATINUM 8570
    Cores:224
    host:6.8.0-90-generic
    node:cl-worker36
    disk:1191977
    volume_size:1000G
    volume_used:74G
    cpu_list:0-223
    requests_cpu:4
    requests_memory:1024Gi
    limits_memory:1024Gi
    eval_parameters
        code:1772481803
MonetDB-BHT-8-3-2 uses docker image monetdb/monetdb:Dec2025
    RAM:2164173176832
    CPU:INTEL(R) XEON(R) PLATINUM 8570
    Cores:224
    host:6.8.0-90-generic
    node:cl-worker36
    disk:1191977
    volume_size:1000G
    volume_used:74G
    cpu_list:0-223
    requests_cpu:4
    requests_memory:1024Gi
    limits_memory:1024Gi
    eval_parameters
        code:1772481803
MonetDB-BHT-8-3-3 uses docker image monetdb/monetdb:Dec2025
    RAM:2164173176832
    CPU:INTEL(R) XEON(R) PLATINUM 8570
    Cores:224
    host:6.8.0-90-generic
    node:cl-worker36
    disk:1191977
    volume_size:1000G
    volume_used:74G
    cpu_list:0-223
    requests_cpu:4
    requests_memory:1024Gi
    limits_memory:1024Gi
    eval_parameters
        code:1772481803

### Errors (failed queries)
            MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-3-1  MonetDB-BHT-8-3-2  MonetDB-BHT-8-3-3
TPC-DS Q90               True               True               True               True               True
TPC-DS Q90
MonetDB-BHT-8-3-2: numRun 1: : java.sql.SQLException: division by zero.
MonetDB-BHT-8-3-3: numRun 1: : java.sql.SQLException: division by zero.
MonetDB-BHT-8-1-1: numRun 1: : java.sql.SQLException: division by zero.
MonetDB-BHT-8-2-1: numRun 1: : java.sql.SQLException: division by zero.
MonetDB-BHT-8-3-1: numRun 1: : java.sql.SQLException: division by zero.

### Warnings (result mismatch)
               MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-3-1  MonetDB-BHT-8-3-2  MonetDB-BHT-8-3-3
TPC-DS Q39a+b               True               True               True              False               True

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-3-1  MonetDB-BHT-8-3-2  MonetDB-BHT-8-3-3
TPC-DS Q1                2803.58              69.71              73.52              53.87              57.44
TPC-DS Q2                8636.28             217.20             483.02             227.28             380.94
TPC-DS Q3               19256.43             359.37             102.71             567.71             532.36
TPC-DS Q4               47404.68            4054.92            6772.10            7032.01            7949.06
TPC-DS Q5               63149.32            2945.17            1588.82            1526.41            1487.74
TPC-DS Q6                1134.22             567.84             871.56             768.15             246.80
TPC-DS Q7               33931.77             127.99             159.69             212.03             159.79
TPC-DS Q8                 302.24              12.71              16.17              13.35              13.43
TPC-DS Q9                6324.16             686.99            1364.37            1530.11            1122.17
TPC-DS Q10             114502.85              47.49              33.14              40.01             121.52
TPC-DS Q11               2380.92            1644.09            2159.83            2667.66            2052.77
TPC-DS Q12                275.96             106.42             239.59             227.31             238.17
TPC-DS Q13                388.99             258.05             435.11             288.15             212.08
TPC-DS Q14a+b              75.95              27.79              25.32              25.43              28.13
TPC-DS Q15                117.27             129.62             138.21             133.06             120.35
TPC-DS Q16              49963.68           37998.73          112920.96           37736.07           65578.99
TPC-DS Q17              12802.24            2308.06            4348.07            2677.53            4326.35
TPC-DS Q18               4766.91             525.50             935.86            2412.95           16190.55
TPC-DS Q19                306.45             173.01             434.99            7789.65           25793.19
TPC-DS Q20                 97.40             125.16             139.32           14255.65             432.73
TPC-DS Q21               7677.42             115.28             274.69            3808.50             136.01
TPC-DS Q22               2931.76             277.51             270.36            1040.16             452.07
TPC-DS Q23a+b             885.41             847.03             621.95           41871.17            1384.82
TPC-DS Q24a+b            3350.83            3174.31            3831.31            4005.44            4162.98
TPC-DS Q25                817.57             826.34             851.26            1044.04             801.04
TPC-DS Q26                150.48             139.26             158.75             357.60             464.47
TPC-DS Q27               6555.77             810.79             782.19             977.48            1066.21
TPC-DS Q28               1734.06            1044.71             686.95            1240.80            1339.89
TPC-DS Q29                747.44             756.86            1132.73            1366.01            1192.19
TPC-DS Q30                191.30              25.81              33.17              82.61              11.07
TPC-DS Q31               2563.32            1246.91            5385.29            1812.21            1066.69
TPC-DS Q32                153.86             154.81             137.56             167.41             158.73
TPC-DS Q33                 98.75              81.36              68.85             115.08              78.96
TPC-DS Q34               1818.60             328.39             236.52             472.46             133.31
TPC-DS Q35                 32.59              29.95              30.48              38.18              24.89
TPC-DS Q36                841.94             565.84             574.60             766.96             565.11
TPC-DS Q37                482.81             342.44             592.50             492.02             534.97
TPC-DS Q38                  6.32               6.28               5.41               4.89               6.82
TPC-DS Q39a+b              10.05               8.25               7.14              11.79              11.59
TPC-DS Q40               2360.66             541.37             785.37             533.41             761.12
TPC-DS Q41                  5.80               5.89              37.51               6.48              11.55
TPC-DS Q42                 65.77              64.91              70.27              74.08             153.14
TPC-DS Q43                280.81             225.06             267.67             296.65             401.79
TPC-DS Q44              32553.06            5740.13             478.14            5390.60            4231.37
TPC-DS Q45                145.31             142.65             146.96             145.81             176.72
TPC-DS Q46                864.18             204.38             210.67             219.54             175.63
TPC-DS Q47                184.57             137.03             165.87             147.89             197.19
TPC-DS Q48                183.77             161.29             174.82             207.64             276.78
TPC-DS Q49               8313.61            1093.56             903.92            1055.62            1131.00
TPC-DS Q50                864.38             717.24             733.83             604.91             813.81
TPC-DS Q51                 91.12              95.57             109.52             137.41             234.60
TPC-DS Q52                 64.85              63.04             196.57             572.37             100.53
TPC-DS Q53                273.91              90.94             306.55              86.12              98.07
TPC-DS Q54                 98.67              98.26             302.96             124.66             125.56
TPC-DS Q55                 70.61              48.51             184.94              87.97              72.03
TPC-DS Q56               2037.01            2227.03            2069.12            2244.94            2396.48
TPC-DS Q57                226.64             144.32             145.91             164.27             374.95
TPC-DS Q58               1799.45             439.38             440.71             614.94             747.81
TPC-DS Q59                991.79             768.36             964.88             895.87             728.67
TPC-DS Q60               3212.06            3104.75            4233.68            3529.38            3355.82
TPC-DS Q61                472.16             178.71             182.90             423.99             251.76
TPC-DS Q62                361.57             248.52            1303.95             242.52             253.02
TPC-DS Q63                125.88             103.57            2509.54             146.43              91.01
TPC-DS Q64              10774.75            2188.13            2379.56            3400.74            3473.68
TPC-DS Q65                201.24             202.42             188.75             201.48             163.07
TPC-DS Q66               1821.07            1386.27            1579.40            2479.53            4026.82
TPC-DS Q67                 19.43              17.27              16.10            1680.60              76.35
TPC-DS Q68                286.35             252.43             242.65             179.01             221.11
TPC-DS Q69                 39.58              34.79              32.38              49.93              30.61
TPC-DS Q70                540.12              12.50               6.93              14.34               8.28
TPC-DS Q71                168.06             135.65              94.49             107.96             132.17
TPC-DS Q72               1688.20             631.94             532.54             897.29             680.48
TPC-DS Q73                108.79              97.90             105.01             158.49             236.45
TPC-DS Q74                689.27             476.11             381.40             940.41             803.10
TPC-DS Q75               6573.59            3550.55            5712.90            3882.19            4518.24
TPC-DS Q76              20834.45            5040.30             269.67            5219.21            5008.92
TPC-DS Q77                740.88             710.68             545.66             788.12             656.38
TPC-DS Q78               7206.13            2682.08            5491.52            5602.49            5649.14
TPC-DS Q79                139.08             148.61             154.51             160.40             237.46
TPC-DS Q80               6120.70            5939.55            7249.11            8925.97            9619.09
TPC-DS Q81                182.25              28.04              17.52              21.52              17.28
TPC-DS Q82                453.41             429.05             730.50             361.56             378.46
TPC-DS Q83                 27.07              20.55              49.51              23.09              18.27
TPC-DS Q84                 53.71              33.24              27.15              77.00              26.38
TPC-DS Q85                420.64             371.79             373.49             597.47             738.88
TPC-DS Q86                185.09             202.03             178.51             441.08             253.73
TPC-DS Q87                  6.67               6.64               4.94              11.68               8.14
TPC-DS Q88                756.03             654.05             734.00             979.32            1116.13
TPC-DS Q89                189.44             149.20             151.75             179.42             223.14
TPC-DS Q91                171.14              31.49             478.53              86.20              79.90
TPC-DS Q92                125.06             137.27             121.95             134.68             212.19
TPC-DS Q93               1869.49            1905.25            4202.07            3808.53            3754.87
TPC-DS Q94              35218.64           33696.25          129556.76           35459.53          163957.84
TPC-DS Q95              38308.70           37077.34           61195.83           49604.13           56100.01
TPC-DS Q96                 41.19              34.42              27.86           13180.38              58.11
TPC-DS Q97                 69.07              47.53              51.63           21225.57              69.97
TPC-DS Q98                134.70              99.39             120.01           28621.51              96.24
TPC-DS Q99                277.76             295.99             266.47           15876.60             255.60

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           1.0          257.0        11.0     1070.0    1376.0
MonetDB-BHT-8-2-1           1.0          257.0        11.0     1070.0    1376.0
MonetDB-BHT-8-3-1           1.0          257.0        11.0     1070.0    1376.0
MonetDB-BHT-8-3-2           1.0          257.0        11.0     1070.0    1376.0
MonetDB-BHT-8-3-3           1.0          257.0        11.0     1070.0    1376.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1           0.64
MonetDB-BHT-8-2-1           0.26
MonetDB-BHT-8-3-1           0.33
MonetDB-BHT-8-3-2           0.53
MonetDB-BHT-8-3-3           0.37

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1          168770.19
MonetDB-BHT-8-2-1          411294.30
MonetDB-BHT-8-3-1          332405.14
MonetDB-BHT-8-3-2          204235.70
MonetDB-BHT-8-3-3          290573.47

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                time [s]  count    SF  Throughput@Size
DBMS            SF   num_experiment num_client                                        
MonetDB-BHT-8-1 30.0 1              1                605      1  30.0         17494.21
MonetDB-BHT-8-2 30.0 1              2                189      1  30.0         56000.00
MonetDB-BHT-8-3 30.0 1              3                436      3  30.0         72825.69

### Workflow
                         orig_name    SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
MonetDB-BHT-8-1-1  MonetDB-BHT-8-1  30.0     8               1           1       1772481970     1772482575
MonetDB-BHT-8-2-1  MonetDB-BHT-8-2  30.0     8               1           2       1772482728     1772482917
MonetDB-BHT-8-3-1  MonetDB-BHT-8-3  30.0     8               1           3       1772483055     1772483456
MonetDB-BHT-8-3-2  MonetDB-BHT-8-3  30.0     8               1           3       1772483055     1772483429
MonetDB-BHT-8-3-3  MonetDB-BHT-8-3  30.0     8               1           3       1772483055     1772483491

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1, 1, 3]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1, 1, 3]]

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1     9057.51    72.35        177.71               177.80
MonetDB-BHT-8-2     2853.24    22.14         47.24                47.32
MonetDB-BHT-8-3    15960.43    72.12        263.95               264.03

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       11.90     0.16          0.30                  0.3
MonetDB-BHT-8-2       11.90     0.01          0.30                  0.3
MonetDB-BHT-8-3       31.49     0.57          0.29                  0.3

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST failed: SQL errors
TEST failed: SQL warnings (result mismatch)
TEST passed: Workflow as planned
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
