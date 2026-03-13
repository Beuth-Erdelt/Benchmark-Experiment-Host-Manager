## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 2529s 
    Code: 1772130153
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.20.
    Experiment is limited to DBMS ['MariaDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [1] threads, split into [8] pods.
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
    disk:148150
    cpu_list:0-63
    args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1772130153

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 MariaDB-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                             24920.40
Minimum Cost Supplier Query (TPC-H Q2)                         1294.58
Shipping Priority (TPC-H Q3)                                   4932.40
Order Priority Checking Query (TPC-H Q4)                       1006.43
Local Supplier Volume (TPC-H Q5)                               3226.57
Forecasting Revenue Change (TPC-H Q6)                          2859.92
Forecasting Revenue Change (TPC-H Q7)                          3515.33
National Market Share (TPC-H Q8)                               6234.82
Product Type Profit Measure (TPC-H Q9)                         5121.78
Forecasting Revenue Change (TPC-H Q10)                         2657.32
Important Stock Identification (TPC-H Q11)                      331.07
Shipping Modes and Order Priority (TPC-H Q12)                 10808.50
Customer Distribution (TPC-H Q13)                             10050.94
Forecasting Revenue Change (TPC-H Q14)                        28840.44
Top Supplier Query (TPC-H Q15)                                 6515.60
Parts/Supplier Relationship (TPC-H Q16)                         661.35
Small-Quantity-Order Revenue (TPC-H Q17)                        153.69
Large Volume Customer (TPC-H Q18)                              9971.97
Discounted Revenue (TPC-H Q19)                                  262.46
Potential Part Promotion (TPC-H Q20)                            489.79
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)          190084.01
Global Sales Opportunity Query (TPC-H Q22)                      379.93

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MariaDB-BHT-8-1-1          23.0          272.0         2.0     1854.0    2154.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MariaDB-BHT-8-1-1           3.08

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MariaDB-BHT-8-1-1            1206.16

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                               time [s]  count   SF  Throughput@Size
DBMS            SF  num_experiment num_client                                       
MariaDB-BHT-8-1 1.0 1              1                321      1  1.0           246.73

### Workflow
                         orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
MariaDB-BHT-8-1-1  MariaDB-BHT-8-1  1.0     8               1           1       1772132292     1772132613

#### Actual
DBMS MariaDB-BHT-8 - Pods [[1]]

#### Planned
DBMS MariaDB-BHT-8 - Pods [[1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
