## Show Summary

### Workload
TPC-DS Queries SF=1
    Type: tpcds
    Duration: 31291s 
    Code: 1772394654
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.21.
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MariaDB-BHT-8-1-1 uses docker image mariadb:11.4.7
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:152072
    cpu_list:0-63
    args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    eval_parameters
        code:1772394654
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Dec2025
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:152978
    cpu_list:0-63
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    eval_parameters
        code:1772394654
MySQL-BHT-64-1-1 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:185771
    cpu_list:0-63
    args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=300', '--innodb-io-capacity_max=600', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    eval_parameters
        code:1772394654
PostgreSQL-BHT-8-1-1 uses docker image postgres:18.3
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:153308
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    eval_parameters
        code:1772394654

### Errors (failed queries)
            MariaDB-BHT-8-1-1  MonetDB-BHT-8-1-1  MySQL-BHT-64-1-1  PostgreSQL-BHT-8-1-1
TPC-DS Q72               True              False             False                 False
TPC-DS Q94               True              False             False                 False
TPC-DS Q95               True              False             False                 False
TPC-DS Q72
MariaDB-BHT-8-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=232) Query execution was interrupted (max_statement_time exceeded)
TPC-DS Q94
MariaDB-BHT-8-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=232) Query execution was interrupted (max_statement_time exceeded)
TPC-DS Q95
MariaDB-BHT-8-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=232) Query execution was interrupted (max_statement_time exceeded)

### Warnings (result mismatch)
               MariaDB-BHT-8-1-1  MonetDB-BHT-8-1-1  MySQL-BHT-64-1-1  PostgreSQL-BHT-8-1-1
TPC-DS Q27                 False               True             False                  True
TPC-DS Q36                 False               True             False                  True
TPC-DS Q39a+b              False               True              True                  True
TPC-DS Q47                 False               True             False                 False
TPC-DS Q70                 False               True             False                 False
TPC-DS Q72                 False               True              True                  True
TPC-DS Q78                 False               True             False                  True
TPC-DS Q80                 False               True             False                  True
TPC-DS Q86                 False               True              True                  True
TPC-DS Q94                 False               True              True                  True
TPC-DS Q95                 False               True              True                  True
TPC-DS Q98                 False               True             False                 False

### Latency of Timer Execution [ms]
DBMS           MariaDB-BHT-8-1-1  MonetDB-BHT-8-1-1  MySQL-BHT-64-1-1  PostgreSQL-BHT-8-1-1
TPC-DS Q1                  19.76              43.65             67.46                197.15
TPC-DS Q2               14140.33             236.29          20108.54                815.22
TPC-DS Q3                  20.89              21.34             30.50                419.61
TPC-DS Q4               37552.77            1253.31          98118.81              19157.75
TPC-DS Q5               29540.39              92.23          44132.86               1316.41
TPC-DS Q6                2786.13              81.87         290774.81             189867.64
TPC-DS Q7               12303.66              50.86           2800.35                947.14
TPC-DS Q8                 977.34              36.37           1447.85                133.95
TPC-DS Q9               12844.29              64.61          18125.77               5727.58
TPC-DS Q10                 53.96              40.18            108.03               2773.32
TPC-DS Q11              24915.76             633.36          62737.54              10763.44
TPC-DS Q12                943.83              19.30           1358.52                172.31
TPC-DS Q13               2996.02              60.48           5625.00               1696.22
TPC-DS Q14a+b          157105.76            2699.49         200799.53               5621.97
TPC-DS Q15                540.12              23.67            773.41                307.80
TPC-DS Q16              30985.66              37.83            774.15                794.89
TPC-DS Q17               2664.40             170.03           2259.13                834.85
TPC-DS Q18               6926.27             119.91           3528.43               1094.26
TPC-DS Q19                699.44              39.56           1278.44                423.02
TPC-DS Q20               1749.96              24.21           2634.24                274.60
TPC-DS Q21              81527.89              68.70         121245.22                580.72
TPC-DS Q22              63331.94             954.08          21749.78               9610.29
TPC-DS Q23a+b          177968.55            2108.19         135621.99              10336.46
TPC-DS Q24a+b              85.63             241.98          13174.34               1498.98
TPC-DS Q25                413.71             110.98            500.94                809.04
TPC-DS Q26               2747.78              24.93          20576.55                651.30
TPC-DS Q27               4918.54             110.84           2245.38                 52.81
TPC-DS Q28               9162.29              65.94          12464.32               2170.39
TPC-DS Q29                139.67             115.09            156.43                876.17
TPC-DS Q30                306.00              19.23           1677.09              25844.21
TPC-DS Q31               4154.50             139.47          46898.21               4723.47
TPC-DS Q32                 23.01              19.90           1244.96                465.35
TPC-DS Q33                639.78              41.39            988.77               1028.01
TPC-DS Q34              12555.18              32.54           3934.22                 57.88
TPC-DS Q35               3422.86              99.84          55691.59               3049.83
TPC-DS Q36               5303.17              74.04           5331.02                 52.12
TPC-DS Q37              13660.58              75.63             23.02                622.25
TPC-DS Q38              26255.06             224.60          36669.45               3506.22
TPC-DS Q39a+b            4468.68            1406.76           8305.57               6076.00
TPC-DS Q40                730.42              82.99            800.66                300.02
TPC-DS Q41               1670.18               6.18           5752.41               3085.73
TPC-DS Q42                712.86              17.59             94.11                221.45
TPC-DS Q43               3646.89              43.83              2.63                 58.44
TPC-DS Q44               3931.69              71.32           6252.69               1044.48
TPC-DS Q45                448.07              14.29            506.85                204.35
TPC-DS Q46              13719.34              46.25           4722.07                 74.56
TPC-DS Q47              41975.18             250.29          31439.91               4945.08
TPC-DS Q48               3462.58              44.96           3902.23               1662.88
TPC-DS Q49               1085.73             103.83           1425.59               1943.49
TPC-DS Q50                 75.83             104.53             94.59               1081.41
TPC-DS Q51              26365.03             460.96          27092.64               2967.68
TPC-DS Q52                778.10              19.24             92.44                222.64
TPC-DS Q53                621.93              30.63           1138.12                284.70
TPC-DS Q54               2810.32              27.90          12095.66                188.88
TPC-DS Q55                663.82              14.51             82.47                222.00
TPC-DS Q56                425.64              25.49            796.38                948.48
TPC-DS Q57              23357.91             100.43          15799.83               2371.71
TPC-DS Q58              23625.99              58.23          30401.73                998.59
TPC-DS Q59              36659.86             116.27          28287.98               1061.82
TPC-DS Q60               2130.28              26.26           1910.84               1046.16
TPC-DS Q61               1162.10              32.07              2.83                334.52
TPC-DS Q62               6219.99              24.65          13114.05                275.08
TPC-DS Q63                632.56              26.87           1150.49                275.91
TPC-DS Q64               2041.22             422.37           1539.80               1672.97
TPC-DS Q65              22703.82              94.52          34144.15               1382.92
TPC-DS Q66               4124.36             112.33           7519.16                545.08
TPC-DS Q67              25477.77             387.91          36687.37               8115.41
TPC-DS Q68              12098.80              38.13           1342.40                 75.17
TPC-DS Q69               1272.12              35.90           2006.18                642.70
TPC-DS Q70              34422.53              91.42          57246.05               1115.69
TPC-DS Q71               1290.46              28.69           1892.92                858.96
TPC-DS Q73              11241.59              22.41           4198.38                 57.41
TPC-DS Q74              18666.35             174.60          22130.36               2697.92
TPC-DS Q75              17555.67             504.15           7412.58               1526.69
TPC-DS Q76               1491.84              45.27           1776.11                573.00
TPC-DS Q77              23713.51              62.54          44195.62                785.68
TPC-DS Q78              18561.29             812.26          48086.68               4526.56
TPC-DS Q79              12497.26              40.39          19029.58                399.40
TPC-DS Q80               2200.01             426.81          39078.42               1129.51
TPC-DS Q81                656.01              26.67           6536.44             110172.33
TPC-DS Q82              14113.01             158.60            158.42               1011.58
TPC-DS Q83               3379.23              18.24           3774.61                250.69
TPC-DS Q84                149.60              50.49            233.51                237.35
TPC-DS Q85                427.27              77.85            402.13                813.09
TPC-DS Q86               3495.45              23.34           5219.97                540.28
TPC-DS Q87              26107.27             246.04          36814.05               3534.40
TPC-DS Q88              29820.73              64.35           6633.89               6067.04
TPC-DS Q89               4897.17              35.49            400.12                291.50
TPC-DS Q90                342.83              15.15           1390.33                336.70
TPC-DS Q91                 38.97              22.13             42.12                251.26
TPC-DS Q92                 12.73              10.35             80.27                139.32
TPC-DS Q93                 86.63              90.34            130.74                479.55
TPC-DS Q96               2140.96              12.83            438.01                235.37
TPC-DS Q97              19032.57             232.24          26891.29                964.99
TPC-DS Q98               3368.06              40.04           4830.05                448.03
TPC-DS Q99              18260.28              58.33          54863.04                390.97

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MariaDB-BHT-8-1-1              1.0          575.0         5.0    10765.0   11352.0
MonetDB-BHT-8-1-1              0.0           95.0        11.0      328.0     441.0
MySQL-BHT-64-1-1               0.0          365.0        10.0    10675.0   11070.0
PostgreSQL-BHT-8-1-1           1.0          135.0         3.0      363.0     508.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
MariaDB-BHT-8-1-1              2.95
MonetDB-BHT-8-1-1              0.08
MySQL-BHT-64-1-1               3.12
PostgreSQL-BHT-8-1-1           0.89

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
MariaDB-BHT-8-1-1               1223.80
MonetDB-BHT-8-1-1              50913.85
MySQL-BHT-64-1-1                1156.30
PostgreSQL-BHT-8-1-1            4075.26

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                  time [s]  count   SF  Throughput@Size
DBMS               SF  num_experiment num_client                                       
MariaDB-BHT-8-1    1.0 1              1               4895      1  1.0            70.60
MonetDB-BHT-8-1    1.0 1              1                 35      1  1.0          9874.29
MySQL-BHT-64-1     1.0 1              1               1997      1  1.0           173.06
PostgreSQL-BHT-8-1 1.0 1              1                521      1  1.0           663.34

### Workflow
                               orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
MariaDB-BHT-8-1-1        MariaDB-BHT-8-1  1.0     8               1           1       1772407740     1772412635
MonetDB-BHT-8-1-1        MonetDB-BHT-8-1  1.0     8               1           1       1772396466     1772396501
MySQL-BHT-64-1-1          MySQL-BHT-64-1  1.0     8               1           1       1772423861     1772425858
PostgreSQL-BHT-8-1-1  PostgreSQL-BHT-8-1  1.0     8               1           1       1772395281     1772395802

#### Actual
DBMS MariaDB-BHT-8 - Pods [[1]]
DBMS MonetDB-BHT-8 - Pods [[1]]
DBMS MySQL-BHT-64 - Pods [[1]]
DBMS PostgreSQL-BHT-8 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1]]
DBMS MonetDB-BHT-8 - Pods [[1]]
DBMS MariaDB-BHT-8 - Pods [[1]]
DBMS MySQL-BHT-64 - Pods [[1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST failed: SQL errors
TEST failed: SQL warnings (result mismatch)
TEST passed: Workflow as planned
