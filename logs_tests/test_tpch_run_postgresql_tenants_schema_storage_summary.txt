## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 764s 
    Code: 1750318614
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.8.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 2 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 50Gi.
    Loading is tested with [1] threads, split into [2] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [2, 2] times the number of benchmarking pods.
    Number of tenants per schema is 2.
    Experiment is run once.

### Services
PostgreSQL-BHT-2
    kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-bht-2-1750318614 9091:9091

### Connections
PostgreSQL-BHT-2-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:398097044
    datadisk:5476
    volume_size:50G
    volume_used:5.4G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750318614
        TENANT_BY:schema
        TENANT_NUM:2
PostgreSQL-BHT-2-1-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:398097044
    datadisk:5476
    volume_size:50G
    volume_used:5.4G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750318614
        TENANT_BY:schema
        TENANT_NUM:2
PostgreSQL-BHT-2-2-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:398097080
    datadisk:5476
    volume_size:50G
    volume_used:5.4G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750318614
        TENANT_BY:schema
        TENANT_NUM:2
PostgreSQL-BHT-2-2-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:398097080
    datadisk:5476
    volume_size:50G
    volume_used:5.4G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750318614
        TENANT_BY:schema
        TENANT_NUM:2

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-2-1-1  PostgreSQL-BHT-2-1-2  PostgreSQL-BHT-2-2-1  PostgreSQL-BHT-2-2-2
Pricing Summary Report (TPC-H Q1)                                 2796.04               2759.08               2753.07               2776.21
Minimum Cost Supplier Query (TPC-H Q2)                             444.04                445.54                476.55                451.25
Shipping Priority (TPC-H Q3)                                       797.64                772.74                788.67                785.36
Order Priority Checking Query (TPC-H Q4)                          1300.65               1291.55               1278.84               1290.21
Local Supplier Volume (TPC-H Q5)                                   684.36                684.04                671.55                701.00
Forecasting Revenue Change (TPC-H Q6)                              529.35                523.84                524.05                515.52
Forecasting Revenue Change (TPC-H Q7)                              811.81                815.03                794.71                785.46
National Market Share (TPC-H Q8)                                   639.71                649.62                648.40                638.77
Product Type Profit Measure (TPC-H Q9)                            1149.71               1163.29               1130.03               1121.37
Forecasting Revenue Change (TPC-H Q10)                            1303.56               1288.43               1297.67               1286.39
Important Stock Identification (TPC-H Q11)                         261.41                260.40                258.83                261.67
Shipping Modes and Order Priority (TPC-H Q12)                     1045.65               1037.78               1037.28               1022.82
Customer Distribution (TPC-H Q13)                                 1905.68               1939.91               1977.35               2017.59
Forecasting Revenue Change (TPC-H Q14)                             567.15                558.25                563.68                553.52
Top Supplier Query (TPC-H Q15)                                     584.31                581.26                577.17                566.45
Parts/Supplier Relationship (TPC-H Q16)                            584.93                585.85                569.31                578.32
Small-Quantity-Order Revenue (TPC-H Q17)                          2004.64               2146.29               2061.73               2055.97
Large Volume Customer (TPC-H Q18)                                 6883.23               7946.93               6888.95               7457.23
Discounted Revenue (TPC-H Q19)                                     722.55                692.90                716.93                702.38
Potential Part Promotion (TPC-H Q20)                               681.30                702.67                655.73                678.40
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                948.54                923.80                910.26                916.14
Global Sales Opportunity Query (TPC-H Q22)                         255.80                248.28                234.76                227.29

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-2-1-1           0.0          123.0         4.0      181.0     310.0
PostgreSQL-BHT-2-1-2           0.0          123.0         4.0      181.0     310.0
PostgreSQL-BHT-2-2-1           0.0          123.0         4.0      181.0     310.0
PostgreSQL-BHT-2-2-2           0.0          123.0         4.0      181.0     310.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-2-1-1           0.88
PostgreSQL-BHT-2-1-2           0.88
PostgreSQL-BHT-2-2-1           0.87
PostgreSQL-BHT-2-2-2           0.87

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-2-1-1            4089.75
PostgreSQL-BHT-2-1-2            4072.82
PostgreSQL-BHT-2-2-1            4127.53
PostgreSQL-BHT-2-2-2            4127.22

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                  time [s]  count   SF  Throughput@Size
DBMS               SF  num_experiment num_client                                       
PostgreSQL-BHT-2-1 1.0 1              1                 30      2  1.0           5280.0
PostgreSQL-BHT-2-2 1.0 1              2                 33      2  1.0           4800.0

### Workflow

#### Actual
DBMS PostgreSQL-BHT-2 - Pods [[2, 2]]

#### Planned
DBMS PostgreSQL-BHT-2 - Pods [[2, 2]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
