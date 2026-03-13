## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 6624s 
    Code: 1772132709
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.20.
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
    disk:148921
    cpu_list:0-63
    args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    eval_parameters
        code:1772132709
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Dec2025
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:149774
    cpu_list:0-63
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    eval_parameters
        code:1772132709
MySQL-BHT-64-1-1 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:182586
    cpu_list:0-63
    args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=300', '--innodb-io-capacity_max=600', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    eval_parameters
        code:1772132709
PostgreSQL-BHT-8-1-1 uses docker image postgres:18.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:148816
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    eval_parameters
        code:1772132709

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 MariaDB-BHT-8-1-1  MonetDB-BHT-8-1-1  MySQL-BHT-64-1-1  PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                             25658.29            1058.80          29064.46               2028.92
Minimum Cost Supplier Query (TPC-H Q2)                         1302.54              25.96            359.86                447.13
Shipping Priority (TPC-H Q3)                                   5396.46             108.68           4235.12                710.16
Order Priority Checking Query (TPC-H Q4)                       1035.89             149.28           1580.40                342.78
Local Supplier Volume (TPC-H Q5)                               3382.99              68.04           4048.76                617.70
Forecasting Revenue Change (TPC-H Q6)                          3281.91              27.15           4173.34                454.52
Forecasting Revenue Change (TPC-H Q7)                          3460.43              96.02           5881.82                710.81
National Market Share (TPC-H Q8)                               6278.81             441.64           9139.40                414.38
Product Type Profit Measure (TPC-H Q9)                         5395.12             103.07           7001.70               1028.47
Forecasting Revenue Change (TPC-H Q10)                         2882.37             136.91           4033.74               1118.22
Important Stock Identification (TPC-H Q11)                      399.08              18.01            491.93                159.83
Shipping Modes and Order Priority (TPC-H Q12)                 11344.40              54.59           7061.09                632.14
Customer Distribution (TPC-H Q13)                              9830.44             527.38          12839.86               1957.52
Forecasting Revenue Change (TPC-H Q14)                        28827.78              36.94           5107.15                493.01
Top Supplier Query (TPC-H Q15)                                 6878.66              36.69          38836.63                494.84
Parts/Supplier Relationship (TPC-H Q16)                         651.74              83.97            922.78                556.05
Small-Quantity-Order Revenue (TPC-H Q17)                        157.92              63.63           1282.78               1794.64
Large Volume Customer (TPC-H Q18)                             10197.63             220.03           5920.24               5329.01
Discounted Revenue (TPC-H Q19)                                  280.65              86.71            438.88                116.51
Potential Part Promotion (TPC-H Q20)                            504.22              38.89            759.12                291.64
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)          193516.10            2535.43          18481.79                737.86
Global Sales Opportunity Query (TPC-H Q22)                      388.16              56.86            521.29                216.40

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MariaDB-BHT-8-1-1             23.0          250.0         2.0     1779.0    2056.0
MonetDB-BHT-8-1-1             22.0           20.0         8.0      153.0     208.0
MySQL-BHT-64-1-1              18.0          256.0         4.0     2541.0    2823.0
PostgreSQL-BHT-8-1-1          24.0           26.0         1.0      167.0     220.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
MariaDB-BHT-8-1-1              3.19
MonetDB-BHT-8-1-1              0.12
MySQL-BHT-64-1-1               3.43
PostgreSQL-BHT-8-1-1           0.65

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
MariaDB-BHT-8-1-1               1157.78
MonetDB-BHT-8-1-1              34899.99
MySQL-BHT-64-1-1                1074.39
PostgreSQL-BHT-8-1-1            5786.21

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                  time [s]  count   SF  Throughput@Size
DBMS               SF  num_experiment num_client                                       
MariaDB-BHT-8-1    1.0 1              1                326      1  1.0           242.94
MonetDB-BHT-8-1    1.0 1              1                 10      1  1.0          7920.00
MySQL-BHT-64-1     1.0 1              1                167      1  1.0           474.25
PostgreSQL-BHT-8-1 1.0 1              1                 25      1  1.0          3168.00

### Workflow
                               orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
MariaDB-BHT-8-1-1        MariaDB-BHT-8-1  1.0     8               1           1       1772135733     1772136059
MonetDB-BHT-8-1-1        MonetDB-BHT-8-1  1.0     8               1           1       1772133527     1772133537
MySQL-BHT-64-1-1          MySQL-BHT-64-1  1.0     8               1           1       1772139099     1772139266
PostgreSQL-BHT-8-1-1  PostgreSQL-BHT-8-1  1.0     8               1           1       1772133097     1772133122

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
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
