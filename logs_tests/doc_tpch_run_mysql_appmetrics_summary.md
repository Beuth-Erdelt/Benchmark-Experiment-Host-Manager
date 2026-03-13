## Show Summary

### Workload
TPC-H Queries SF=3
    Type: tpch
    Duration: 8466s 
    Code: 1773304403
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.9.3.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['MySQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MySQL-BHT-64-1-1 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:189236
    cpu_list:0-63
    args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=300', '--innodb-io-capacity_max=600', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:16Gi
    limits_memory:64Gi
    eval_parameters
        code:1773304403

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 MySQL-BHT-64-1-1
Pricing Summary Report (TPC-H Q1)                            87517.97
Minimum Cost Supplier Query (TPC-H Q2)                        1073.79
Shipping Priority (TPC-H Q3)                                 13601.88
Order Priority Checking Query (TPC-H Q4)                      4942.47
Local Supplier Volume (TPC-H Q5)                             12617.82
Forecasting Revenue Change (TPC-H Q6)                        12625.97
Forecasting Revenue Change (TPC-H Q7)                        18603.43
National Market Share (TPC-H Q8)                             28566.90
Product Type Profit Measure (TPC-H Q9)                       21033.20
Forecasting Revenue Change (TPC-H Q10)                       15816.28
Important Stock Identification (TPC-H Q11)                    1525.58
Shipping Modes and Order Priority (TPC-H Q12)                19426.31
Customer Distribution (TPC-H Q13)                            72005.11
Forecasting Revenue Change (TPC-H Q14)                       15487.35
Top Supplier Query (TPC-H Q15)                              122059.78
Parts/Supplier Relationship (TPC-H Q16)                       2630.19
Small-Quantity-Order Revenue (TPC-H Q17)                      3800.74
Large Volume Customer (TPC-H Q18)                            17741.37
Discounted Revenue (TPC-H Q19)                                1232.37
Potential Part Promotion (TPC-H Q20)                          2340.66
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)          57842.46
Global Sales Opportunity Query (TPC-H Q22)                    1508.25

### Loading [s]
                  timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MySQL-BHT-64-1-1          12.0          651.0         5.0     7370.0    8044.0

### Geometric Mean of Medians of Timer Run [s]
                  Geo Times [s]
DBMS                           
MySQL-BHT-64-1-1          10.67

### Power@Size ((3600*SF)/(geo times))
                  Power@Size [~Q/h]
DBMS                               
MySQL-BHT-64-1-1            1024.33

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                              time [s]  count   SF  Throughput@Size
DBMS           SF  num_experiment num_client                                       
MySQL-BHT-64-1 3.0 1              1                540      1  3.0            440.0

### Workflow
                       orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
MySQL-BHT-64-1-1  MySQL-BHT-64-1  3.0     8               1           1       1773312249     1773312789

#### Actual
DBMS MySQL-BHT-64 - Pods [[1]]

#### Planned
DBMS MySQL-BHT-64 - Pods [[1]]

### Ingestion - SUT
                CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-64-1     7623.06     3.43         31.48                 64.0

### Ingestion - Loader
                CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-64-1       14.93     0.03          0.01                 0.39

### Execution - SUT
                CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-64-1      525.07     1.02         31.52                 64.0

### Execution - Benchmarker
                CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-64-1       18.84     0.25          0.37                 0.38

### Application Metrics

#### Loading phase: SUT deployment
                InnoDB Buffer Pool Hit Ratio  Queries Per Second (QPS)  Connection Usage Ratio  Slow Queries Rate  InnoDB Log Waits Rate
MySQL-BHT-64-1                           1.0                      0.99                    0.01               0.09                      0

#### Execution phase: SUT deployment
                InnoDB Buffer Pool Hit Ratio  Queries Per Second (QPS)  Connection Usage Ratio  Slow Queries Rate  InnoDB Log Waits Rate
MySQL-BHT-64-1                             0                      0.75                     0.0               0.04                      0

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
