# Example: Multi-Tenant

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

In a multi-tenant architecture, it is assumed that each tenant maintains an isolated dataset and interacts exclusively with this dataset.
Several strategies exist to achieve this separation, including the schema-per-tenant, database-per-tenant, and container-per-tenant approaches.
In the following sections, we present an evaluation of these strategies using bexhoma to compare their performance characteristics.

## Background

To make this work, there has to be some preparation.
* In the experiment folders, there are init scripts containing placeholders for the database `{BEXHOMA_DATABASE}` or schema `{BEXHOMA_SCHEMA}`
* The DBMS must have placeholders in the connection parameters - c.f. [DBMS](DBMS.html#postgresql)

Bexhoma contains these preparations for PostgreSQL and MySQL (without the schema-per-tenant option).

## Preparation

You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"

mkdir -p $LOG_DIR
```

We set the number of tenants to 2 in the following:
```
BEXHOMA_NUM_TENANTS=2
```


## TPC-H

An extensive example for an evaluation is in the [repository](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/dev/MT-Benchbase-Merger-collector.ipynb).

### Schema-Per-Tenant

At first we remove old storage
```
kubectl delete pvc bexhoma-storage-postgresql-schema-2-tpch-1
```

Example for power test with 2 tenants, each having a dedicated schema in the same database:
```bash
nohup python tpch.py -tr \
  --dbms PostgreSQL \
  -ii -ic -is -nlp $BEXHOMA_NUM_TENANTS -nlt 1 -nbp $BEXHOMA_NUM_TENANTS -nbt 64 -ne $BEXHOMA_NUM_TENANTS -mtn $BEXHOMA_NUM_TENANTS -mtb schema \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 10Gi \
  run </dev/null &>$LOG_DIR/test_tpch_run_postgresql_tenants_schema.log &
```

test_tpch_run_postgresql_tenants_schema.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 560s 
    Code: 1758636313
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.12.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 2 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 10Gi.
    Loading is tested with [1] threads, split into [2] pods.
    Benchmarking is tested with [64] threads, split into [2] pods.
    Benchmarking is run as [2] times the number of benchmarking pods.
    Number of tenants is 2, one schema per tenant.
    Experiment is run once.

### Connections
PostgreSQL-BHT-2-1-1 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:435678944
    datadisk:5475
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1758636313
        TENANT_BY:schema
        TENANT_NUM:2
PostgreSQL-BHT-2-1-2 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:435678944
    datadisk:5475
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1758636313
        TENANT_BY:schema
        TENANT_NUM:2

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-2-1-1  PostgreSQL-BHT-2-1-2
Pricing Summary Report (TPC-H Q1)                                 2423.38               2431.48
Minimum Cost Supplier Query (TPC-H Q2)                             448.58                470.28
Shipping Priority (TPC-H Q3)                                      1210.57               1198.93
Order Priority Checking Query (TPC-H Q4)                           341.19                346.82
Local Supplier Volume (TPC-H Q5)                                   644.08                644.24
Forecasting Revenue Change (TPC-H Q6)                              459.33                467.47
Forecasting Revenue Change (TPC-H Q7)                              762.71                789.73
National Market Share (TPC-H Q8)                                   452.12                459.72
Product Type Profit Measure (TPC-H Q9)                            1012.60               1056.78
Forecasting Revenue Change (TPC-H Q10)                             555.73                576.09
Important Stock Identification (TPC-H Q11)                         196.54                181.43
Shipping Modes and Order Priority (TPC-H Q12)                      692.25                690.46
Customer Distribution (TPC-H Q13)                                 2023.76               2068.50
Forecasting Revenue Change (TPC-H Q14)                             503.97                804.93
Top Supplier Query (TPC-H Q15)                                     507.53                518.91
Parts/Supplier Relationship (TPC-H Q16)                            563.52                571.81
Small-Quantity-Order Revenue (TPC-H Q17)                          1796.32               1814.44
Large Volume Customer (TPC-H Q18)                                 6685.08               7496.41
Discounted Revenue (TPC-H Q19)                                     404.96                126.39
Potential Part Promotion (TPC-H Q20)                               238.96                266.61
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                745.50                756.90
Global Sales Opportunity Query (TPC-H Q22)                         245.95                224.72

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-2-1-1           1.0          120.0         5.0      209.0     337.0
PostgreSQL-BHT-2-1-2           1.0          120.0         5.0      209.0     337.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-2-1-1           0.68
PostgreSQL-BHT-2-1-2           0.67

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-2-1-1            5281.29
PostgreSQL-BHT-2-1-2            5367.42

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                  time [s]  count   SF  Throughput@Size
DBMS               SF  num_experiment num_client                                       
PostgreSQL-BHT-2-1 1.0 1              1                 26      2  1.0          6092.31

### Workflow
                               orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
PostgreSQL-BHT-2-1-1  PostgreSQL-BHT-2-1  1.0     2               1           1       1758636804     1758636829
PostgreSQL-BHT-2-1-2  PostgreSQL-BHT-2-1  1.0     2               1           1       1758636804     1758636830

#### Actual
DBMS PostgreSQL-BHT-2 - Pods [[2]]

#### Planned
DBMS PostgreSQL-BHT-2 - Pods [[2]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
```


### Database-Per-Tenant

At first we remove old storage
```
kubectl delete pvc bexhoma-storage-postgresql-database-2-tpch-1
```

Example for power test with 2 tenants, each having a dedicated database in the same DBMS:
```bash
nohup python tpch.py -tr \
  --dbms PostgreSQL \
  -ii -ic -is -nlp $BEXHOMA_NUM_TENANTS -nlt 1 -nbp $BEXHOMA_NUM_TENANTS -nbt 64 -ne $BEXHOMA_NUM_TENANTS -mtn $BEXHOMA_NUM_TENANTS -mtb database \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 10Gi \
  run </dev/null &>$LOG_DIR/test_tpch_run_postgresql_tenants_database.log &
```

test_tpch_run_postgresql_tenants_database.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 434s 
    Code: 1758636914
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.12.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 2 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 10Gi.
    Loading is tested with [1] threads, split into [2] pods.
    Benchmarking is tested with [64] threads, split into [2] pods.
    Benchmarking is run as [2] times the number of benchmarking pods.
    Number of tenants is 2, one database per tenant.
    Experiment is run once.

### Connections
PostgreSQL-BHT-1-0-1-1 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:441324476
    datadisk:2757
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1758636914
        TENANT_BY:container
        TENANT_NUM:2
PostgreSQL-BHT-1-1-1-1 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:441324476
    datadisk:2757
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1758636914
        TENANT_BY:container
        TENANT_NUM:2
        TENANT:1
PostgreSQL-BHT-2-1-1 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:441324476
    datadisk:5489
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1758636914
        TENANT_BY:database
        TENANT_NUM:2
PostgreSQL-BHT-2-1-2 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:441324476
    datadisk:5489
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1758636914
        TENANT_BY:database
        TENANT_NUM:2

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-1-0-1-1  PostgreSQL-BHT-1-1-1-1  PostgreSQL-BHT-2-1-1  PostgreSQL-BHT-2-1-2
Pricing Summary Report (TPC-H Q1)                                   2586.79                 2467.52               2426.49               2416.74
Minimum Cost Supplier Query (TPC-H Q2)                               481.17                  468.32                485.95                450.17
Shipping Priority (TPC-H Q3)                                        1194.62                 1151.43               1208.86               1146.06
Order Priority Checking Query (TPC-H Q4)                             355.15                  338.39                344.43                337.36
Local Supplier Volume (TPC-H Q5)                                     626.07                  610.69                613.78                604.29
Forecasting Revenue Change (TPC-H Q6)                                493.41                  477.65                469.06                472.37
Forecasting Revenue Change (TPC-H Q7)                                749.15                  754.55                716.39                729.21
National Market Share (TPC-H Q8)                                     439.73                  420.13                414.57                413.31
Product Type Profit Measure (TPC-H Q9)                              1035.88                 1026.90               1005.06                984.63
Forecasting Revenue Change (TPC-H Q10)                               564.70                  555.80                531.22                528.76
Important Stock Identification (TPC-H Q11)                           170.80                  178.14                158.66                159.07
Shipping Modes and Order Priority (TPC-H Q12)                        705.28                  682.54                749.41                742.00
Customer Distribution (TPC-H Q13)                                   2123.73                 2141.26               2119.66               2111.94
Forecasting Revenue Change (TPC-H Q14)                               520.00                  505.43                506.27                508.73
Top Supplier Query (TPC-H Q15)                                       520.73                  508.88                508.68                508.42
Parts/Supplier Relationship (TPC-H Q16)                              580.97                  593.35                585.88                587.60
Small-Quantity-Order Revenue (TPC-H Q17)                            2010.08                 1878.49               1824.55               1814.78
Large Volume Customer (TPC-H Q18)                                   6425.31                 5723.41               5977.98               5813.65
Discounted Revenue (TPC-H Q19)                                       124.50                  120.32                134.82                143.52
Potential Part Promotion (TPC-H Q20)                                 244.13                  260.46                266.97                250.43
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                  769.12                  749.08                744.46                740.93
Global Sales Opportunity Query (TPC-H Q22)                           230.77                  223.21                221.61                229.85

### Loading [s]
                        timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-1-0-1-1           0.0          116.0         0.0      179.0     299.0
PostgreSQL-BHT-1-1-1-1           0.0          117.0         1.0      180.0     300.0
PostgreSQL-BHT-2-1-1             3.0          107.0         2.0      181.0     295.0
PostgreSQL-BHT-2-1-2             3.0          107.0         2.0      181.0     295.0

### Geometric Mean of Medians of Timer Run [s]
                        Geo Times [s]
DBMS                                 
PostgreSQL-BHT-1-0-1-1           0.65
PostgreSQL-BHT-1-1-1-1           0.64
PostgreSQL-BHT-2-1-1             0.64
PostgreSQL-BHT-2-1-2             0.64

### Power@Size ((3600*SF)/(geo times))
                        Power@Size [~Q/h]
DBMS                                     
PostgreSQL-BHT-1-0-1-1            5503.16
PostgreSQL-BHT-1-1-1-1            5630.97
PostgreSQL-BHT-2-1-1              5621.47
PostgreSQL-BHT-2-1-2              5667.73

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                    time [s]  count   SF  Throughput@Size
DBMS                 SF  num_experiment num_client                                       
PostgreSQL-BHT-1-0-1 1.0 1              1                 24      1  1.0           3300.0
PostgreSQL-BHT-1-1-1 1.0 1              1                 24      1  1.0           3300.0
PostgreSQL-BHT-2-1   1.0 1              1                 25      2  1.0           6336.0

### Workflow
                                   orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
PostgreSQL-BHT-1-0-1-1  PostgreSQL-BHT-1-0-1  1.0     1               1           1       1758637293     1758637317
PostgreSQL-BHT-1-1-1-1  PostgreSQL-BHT-1-1-1  1.0     1               1           1       1758637291     1758637315
PostgreSQL-BHT-2-1-1      PostgreSQL-BHT-2-1  1.0     2               1           1       1758637279     1758637304
PostgreSQL-BHT-2-1-2      PostgreSQL-BHT-2-1  1.0     2               1           1       1758637279     1758637303

#### Actual
DBMS PostgreSQL-BHT-1-0 - Pods [[1]]
DBMS PostgreSQL-BHT-1 - Pods [[1]]
DBMS PostgreSQL-BHT-2 - Pods [[2]]

#### Planned
DBMS PostgreSQL-BHT-2 - Pods [[2]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST failed: Workflow not as planned
```


### Container-Per-Tenant

At first we remove old storage
```
kubectl delete pvc bexhoma-storage-postgresql-0-2-tpch-1
kubectl delete pvc bexhoma-storage-postgresql-1-2-tpch-1
```

Example for power test with 2 tenants, each having a dedicated DBMS:
```bash
nohup python tpch.py \
  -mtn $BEXHOMA_NUM_TENANTS -mtb container \
  -sf 1 \
  --dbms PostgreSQL \
  -ii -ic -is \
  -nlp 1 -nbp 1 \
  -ne 1,1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/test_tpch_run_postgresql_tenants_container.log &
```

test_tpch_run_postgresql_tenants_container.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 548s 
    Code: 1758636914
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.12.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 1] times the number of benchmarking pods.
    Number of tenants is 2, one container per tenant.
    Experiment is run once.

### Connections
PostgreSQL-BHT-1-0-1-1 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:441324476
    datadisk:2757
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1758636914
        TENANT_BY:container
        TENANT_NUM:2
PostgreSQL-BHT-1-0-2-1 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:441324464
    datadisk:2757
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1758636914
        TENANT_BY:container
        TENANT_NUM:2
PostgreSQL-BHT-1-1-1-1 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:441324476
    datadisk:2757
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1758636914
        TENANT_BY:container
        TENANT_NUM:2
        TENANT:1
PostgreSQL-BHT-1-1-2-1 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:441324460
    datadisk:2757
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1758636914
        TENANT_BY:container
        TENANT_NUM:2
        TENANT:1
PostgreSQL-BHT-2-1-1 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:441324476
    datadisk:5489
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1758636914
        TENANT_BY:database
        TENANT_NUM:2
PostgreSQL-BHT-2-1-2 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:441324476
    datadisk:5489
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1758636914
        TENANT_BY:database
        TENANT_NUM:2

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-1-0-1-1  PostgreSQL-BHT-1-0-2-1  PostgreSQL-BHT-1-1-1-1  PostgreSQL-BHT-1-1-2-1  PostgreSQL-BHT-2-1-1  PostgreSQL-BHT-2-1-2
Pricing Summary Report (TPC-H Q1)                                   2586.79                 2577.01                 2467.52                 2456.87               2426.49               2416.74
Minimum Cost Supplier Query (TPC-H Q2)                               481.17                  434.63                  468.32                  446.76                485.95                450.17
Shipping Priority (TPC-H Q3)                                        1194.62                 1080.50                 1151.43                 1068.08               1208.86               1146.06
Order Priority Checking Query (TPC-H Q4)                             355.15                  349.52                  338.39                  334.99                344.43                337.36
Local Supplier Volume (TPC-H Q5)                                     626.07                  615.34                  610.69                  608.61                613.78                604.29
Forecasting Revenue Change (TPC-H Q6)                                493.41                  484.09                  477.65                  473.82                469.06                472.37
Forecasting Revenue Change (TPC-H Q7)                                749.15                  725.18                  754.55                  737.58                716.39                729.21
National Market Share (TPC-H Q8)                                     439.73                  376.39                  420.13                  367.65                414.57                413.31
Product Type Profit Measure (TPC-H Q9)                              1035.88                 1017.80                 1026.90                 1010.53               1005.06                984.63
Forecasting Revenue Change (TPC-H Q10)                               564.70                  556.83                  555.80                  549.80                531.22                528.76
Important Stock Identification (TPC-H Q11)                           170.80                  157.77                  178.14                  165.83                158.66                159.07
Shipping Modes and Order Priority (TPC-H Q12)                        705.28                  706.27                  682.54                  685.33                749.41                742.00
Customer Distribution (TPC-H Q13)                                   2123.73                 2097.59                 2141.26                 2042.19               2119.66               2111.94
Forecasting Revenue Change (TPC-H Q14)                               520.00                  528.34                  505.43                  512.79                506.27                508.73
Top Supplier Query (TPC-H Q15)                                       520.73                  525.56                  508.88                  515.38                508.68                508.42
Parts/Supplier Relationship (TPC-H Q16)                              580.97                  588.59                  593.35                  582.55                585.88                587.60
Small-Quantity-Order Revenue (TPC-H Q17)                            2010.08                 1814.21                 1878.49                 1870.81               1824.55               1814.78
Large Volume Customer (TPC-H Q18)                                   6425.31                 5472.85                 5723.41                 6804.17               5977.98               5813.65
Discounted Revenue (TPC-H Q19)                                       124.50                  123.50                  120.32                  121.26                134.82                143.52
Potential Part Promotion (TPC-H Q20)                                 244.13                  238.87                  260.46                  263.32                266.97                250.43
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                  769.12                  783.07                  749.08                  747.04                744.46                740.93
Global Sales Opportunity Query (TPC-H Q22)                           230.77                  231.21                  223.21                  220.54                221.61                229.85

### Loading [s]
                        timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-1-0-1-1           0.0          116.0         0.0      179.0     299.0
PostgreSQL-BHT-1-0-2-1           0.0          116.0         0.0      179.0     299.0
PostgreSQL-BHT-1-1-1-1           0.0          117.0         1.0      180.0     300.0
PostgreSQL-BHT-1-1-2-1           0.0          117.0         1.0      180.0     300.0
PostgreSQL-BHT-2-1-1             3.0          107.0         2.0      181.0     295.0
PostgreSQL-BHT-2-1-2             3.0          107.0         2.0      181.0     295.0

### Geometric Mean of Medians of Timer Run [s]
                        Geo Times [s]
DBMS                                 
PostgreSQL-BHT-1-0-1-1           0.65
PostgreSQL-BHT-1-0-2-1           0.63
PostgreSQL-BHT-1-1-1-1           0.64
PostgreSQL-BHT-1-1-2-1           0.63
PostgreSQL-BHT-2-1-1             0.64
PostgreSQL-BHT-2-1-2             0.64

### Power@Size ((3600*SF)/(geo times))
                        Power@Size [~Q/h]
DBMS                                     
PostgreSQL-BHT-1-0-1-1            5503.16
PostgreSQL-BHT-1-0-2-1            5707.73
PostgreSQL-BHT-1-1-1-1            5630.97
PostgreSQL-BHT-1-1-2-1            5699.08
PostgreSQL-BHT-2-1-1              5621.47
PostgreSQL-BHT-2-1-2              5667.73

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                    time [s]  count   SF  Throughput@Size
DBMS                 SF  num_experiment num_client                                       
PostgreSQL-BHT-1-0-1 1.0 1              1                 24      1  1.0          3300.00
PostgreSQL-BHT-1-0-2 1.0 1              2                 23      1  1.0          3443.48
PostgreSQL-BHT-1-1-1 1.0 1              1                 24      1  1.0          3300.00
PostgreSQL-BHT-1-1-2 1.0 1              2                 25      1  1.0          3168.00
PostgreSQL-BHT-2-1   1.0 1              1                 25      2  1.0          6336.00

### Workflow
                                   orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
PostgreSQL-BHT-1-0-1-1  PostgreSQL-BHT-1-0-1  1.0     1               1           1       1758637293     1758637317
PostgreSQL-BHT-1-0-2-1  PostgreSQL-BHT-1-0-2  1.0     1               1           2       1758637388     1758637411
PostgreSQL-BHT-1-1-1-1  PostgreSQL-BHT-1-1-1  1.0     1               1           1       1758637291     1758637315
PostgreSQL-BHT-1-1-2-1  PostgreSQL-BHT-1-1-2  1.0     1               1           2       1758637387     1758637412
PostgreSQL-BHT-2-1-1      PostgreSQL-BHT-2-1  1.0     2               1           1       1758637279     1758637304
PostgreSQL-BHT-2-1-2      PostgreSQL-BHT-2-1  1.0     2               1           1       1758637279     1758637303

#### Actual
DBMS PostgreSQL-BHT-1-0 - Pods [[1, 1]]
DBMS PostgreSQL-BHT-1 - Pods [[1, 1]]
DBMS PostgreSQL-BHT-2 - Pods [[2]]

#### Planned
DBMS PostgreSQL-BHT-1-0 - Pods [[1, 1]]
DBMS PostgreSQL-BHT-1-1 - Pods [[1, 1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST failed: Workflow not as planned
```





## TPC-C

An extensive example for an evaluation is in the [repository](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/dev/MT-TPC-H-Merger-collector.ipynb).


### Schema-Per-Tenant

At first we remove old storage
```
kubectl delete pvc bexhoma-storage-postgresql-benchbase-tpcc-1
```

Example for run with 2 tenants for 5 minutes, keying and thinking time activated, 1 warehouse and 10 clients per tenant, each having a dedicated schema in the same database:
```bash
nohup python benchbase.py \
  -mtn $BEXHOMA_NUM_TENANTS -mtb schema \
  -sf 1 -sd 5 -xkey \
  --dbms PostgreSQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/test_benchbase_run_postgresql_tenants_schema.log &
```

test_benchbase_run_postgresql_tenants_schema.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=1
    Type: benchbase
    Duration: 1193s 
    Code: 1758637514
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.12.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [10] threads, split into [1] pods.
    Benchmarking is run as [2, 2] times the number of benchmarking pods.
    Number of tenants is 2, one schema per tenant.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:436330084
    datadisk:636
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1758637514
                TENANT_BY:schema
                TENANT_NUM:2
PostgreSQL-1-1-1024-2 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:436331096
    datadisk:637
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1758637514
                TENANT_BY:schema
                TENANT_NUM:2

### Execution

#### Per Pod
                         experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                     
PostgreSQL-1-1-1024-1-1               1         10    1024       1      1  300.0           0                      0.469999                   0.463332   97.278098                                                      64762.0                                              30838.0
PostgreSQL-1-1-1024-1-2               1         10    1024       1      2  300.0           0                      0.453332                   0.446665   93.778864                                                      74535.0                                              34088.0
PostgreSQL-1-1-1024-2-2               1         10    1024       2      1  300.0           0                      0.436665                   0.439999   92.379195                                                      76630.0                                              30646.0
PostgreSQL-1-1-1024-2-1               1         10    1024       2      2  300.0           0                      0.496665                   0.496665  104.276508                                                      72419.0                                              27951.0

#### Aggregated Parallel
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         20    2048          2  300.0           0                          0.92                       0.91         0.0                                                      74535.0                                              32463.0
PostgreSQL-1-1-1024-2               1         20    2048          2  300.0           0                          0.93                       0.94         0.0                                                      76630.0                                              29298.5

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[2, 2]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[2, 2]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1      157.0        1.0   2.0          22.929936
PostgreSQL-1-1-1024-2      157.0        1.0   2.0          22.929936

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```


### Database-Per-Tenant

At first we remove old storage
```
kubectl delete pvc bexhoma-storage-postgresql-benchbase-tpcc-1
```

Example for run with 2 tenants for 5 minutes, keying and thinking time activated, 1 warehouse and 10 clients per tenant, each having a dedicated database in the same DBMS:
```bash
nohup python benchbase.py \
  -mtn $BEXHOMA_NUM_TENANTS -mtb database \
  -sf 1 -sd 5 -xkey \
  --dbms PostgreSQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/test_benchbase_run_postgresql_tenants_database.log &
```

test_benchbase_run_postgresql_tenants_database.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=1
    Type: benchbase
    Duration: 1130s 
    Code: 1758638715
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.12.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [10] threads, split into [1] pods.
    Benchmarking is run as [2, 2] times the number of benchmarking pods.
    Number of tenants is 2, one database per tenant.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:436345096
    datadisk:651
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1758638715
                TENANT_BY:database
                TENANT_NUM:2
PostgreSQL-1-1-1024-2 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:436346132
    datadisk:652
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1758638715
                TENANT_BY:database
                TENANT_NUM:2

### Execution

#### Per Pod
                         experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                     
PostgreSQL-1-1-1024-1-2               1         10    1024       1      1  300.0           0                      0.426665                   0.423332   88.879965                                                      61449.0                                              29823.0
PostgreSQL-1-1-1024-1-1               1         10    1024       1      2  300.0           0                      0.506665                   0.499998  104.976346                                                      90704.0                                              32813.0
PostgreSQL-1-1-1024-2-1               1         10    1024       2      1  300.0           0                      0.473332                   0.476665  100.077456                                                      84390.0                                              40163.0
PostgreSQL-1-1-1024-2-2               1         10    1024       2      2  300.0           0                      0.503333                   0.500000  104.976657                                                      99732.0                                              43215.0

#### Aggregated Parallel
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         20    2048          2  300.0           0                          0.93                       0.92         0.0                                                      90704.0                                              31318.0
PostgreSQL-1-1-1024-2               1         20    2048          2  300.0           0                          0.98                       0.98         0.0                                                      99732.0                                              41689.0

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[2, 2]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[2, 2]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1      115.0        1.0   2.0          31.304348
PostgreSQL-1-1-1024-2      115.0        1.0   2.0          31.304348

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```


### Container-Per-Tenant

At first we remove old storage
```
kubectl delete pvc bexhoma-storage-postgresql-0-2-benchbase-tpcc-1
kubectl delete pvc bexhoma-storage-postgresql-1-2-benchbase-tpcc-1
```

Example for run with 2 tenants for 5 minutes, keying and thinking time activated, 1 warehouse and 10 clients per tenant, each having a dedicated DBMS:
```bash
nohup python benchbase.py \
  -mtn $BEXHOMA_NUM_TENANTS -mtb container \
  -sf 1 -sd 5 -xkey \
  --dbms PostgreSQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne 1,1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/test_benchbase_run_postgresql_tenants_container.log &
```

test_benchbase_run_postgresql_tenants_container.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=1
    Type: benchbase
    Duration: 1438s 
    Code: 1758639855
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.12.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [10] threads, split into [1] pods.
    Benchmarking is run as [1, 1] times the number of benchmarking pods.
    Number of tenants is 2, one container per tenant.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-0-1 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:436353348
    datadisk:330
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1758639855
                TENANT_BY:container
                TENANT_NUM:2
PostgreSQL-1-1-1024-0-2 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:436354360
    datadisk:330
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1758639855
                TENANT_BY:container
                TENANT_NUM:2
PostgreSQL-1-1-1024-1-1 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:436353348
    datadisk:330
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1758639855
                TENANT_BY:container
                TENANT_NUM:2
                TENANT:1
PostgreSQL-1-1-1024-1-2 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:436354360
    datadisk:330
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1758639855
                TENANT_BY:container
                TENANT_NUM:2
                TENANT:1

### Execution

#### Per Pod
                           experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                       
PostgreSQL-1-1-1024-1-1-1               1         10    1024       1      1  300.0           0                      0.513332                   0.516665  108.475570                                                      90863.0                                              41350.0
PostgreSQL-1-1-1024-0-1-1               1         10    1024       1      1  300.0           0                      0.473332                   0.476665  100.077458                                                      90346.0                                              42377.0
PostgreSQL-1-1-1024-0-2-1               1         10    1024       2      1  300.0           0                      0.483332                   0.486665  102.176970                                                      58744.0                                              26375.0
PostgreSQL-1-1-1024-1-2-1               1         10    1024       2      1  300.0           0                      0.453332                   0.453332   95.178593                                                      60172.0                                              29796.0

#### Aggregated Parallel
     experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
1-1               1         20    2048          2  300.0           0                          0.99                       0.99         0.0                                                      90863.0                                              41863.5
1-2               1         20    2048          2  300.0           0                          0.94                       0.94         0.0                                                      60172.0                                              28085.5

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024-0 - Pods [[1, 1]]
DBMS PostgreSQL-1-1-1024-1 - Pods [[1, 1]]

#### Planned
DBMS PostgreSQL-1-1-1024-0 - Pods [[1, 1]]
DBMS PostgreSQL-1-1-1024-1 - Pods [[1, 1]]

### Loading
                         time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-0-1      260.0        1.0   1.0          13.846154
PostgreSQL-1-1-1024-0-2      260.0        1.0   1.0          13.846154
PostgreSQL-1-1-1024-1-1      260.0        1.0   1.0          13.846154
PostgreSQL-1-1-1024-1-2      260.0        1.0   1.0          13.846154

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```

