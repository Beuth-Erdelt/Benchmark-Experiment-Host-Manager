# Example: Multi-Tenant

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

In a multi-tenant architecture, it is assumed that each tenant maintains an isolated dataset and interacts exclusively with this dataset.
Several strategies exist to achieve this separation, including the schema-per-tenant, database-per-tenant, and container-per-tenant approaches.
In the following sections, we present an evaluation of these strategies using bexhoma to compare their performance characteristics.

You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"

mkdir -p $LOG_DIR
```



## TPC-H


### Schema-Per-Tenant

Example for power test with 2 tenants, each having a dedicated schema in the same database:
```bash
nohup python tpch.py \
  -mtn 2 -mtb schema \
  -sf 1 \
  --dbms PostgreSQL \
  -ii -ic -is \
  -nlp 2 -nbp 1 \
  -ne 2,2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/test_tpch_run_postgresql_tenants_schema.log &
```

test_tpch_run_postgresql_tenants_schema.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 753s 
    Code: 1750354013
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
    Loading is tested with [1] threads, split into [2] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [2, 2] times the number of benchmarking pods.
    Number of tenants is 2, one schema per tenant.
    Experiment is run once.

### Connections
PostgreSQL-BHT-2-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:404022032
    datadisk:5476
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750354013
        TENANT_BY:schema
        TENANT_NUM:2
PostgreSQL-BHT-2-1-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:404022032
    datadisk:5476
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750354013
        TENANT_BY:schema
        TENANT_NUM:2
PostgreSQL-BHT-2-2-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:404021832
    datadisk:5476
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750354013
        TENANT_BY:schema
        TENANT_NUM:2
PostgreSQL-BHT-2-2-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:404021832
    datadisk:5476
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750354013
        TENANT_BY:schema
        TENANT_NUM:2

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-2-1-1  PostgreSQL-BHT-2-1-2  PostgreSQL-BHT-2-2-1  PostgreSQL-BHT-2-2-2
Pricing Summary Report (TPC-H Q1)                                 2625.72               2618.63               2635.35               2631.00
Minimum Cost Supplier Query (TPC-H Q2)                             444.24                447.05                435.64                455.12
Shipping Priority (TPC-H Q3)                                       807.95                801.33                792.28                790.43
Order Priority Checking Query (TPC-H Q4)                          1316.50               1279.23               1287.48               1280.68
Local Supplier Volume (TPC-H Q5)                                   703.25                706.98                710.06                704.50
Forecasting Revenue Change (TPC-H Q6)                              521.43                516.78                519.85                523.83
Forecasting Revenue Change (TPC-H Q7)                              820.88                829.23                821.94                800.86
National Market Share (TPC-H Q8)                                   644.51                645.86                640.93                654.11
Product Type Profit Measure (TPC-H Q9)                            1148.25               1134.70               1137.91               1148.17
Forecasting Revenue Change (TPC-H Q10)                            1305.82               1295.66               1283.57               1300.50
Important Stock Identification (TPC-H Q11)                         269.86                262.83                267.06                266.05
Shipping Modes and Order Priority (TPC-H Q12)                     1077.33               1060.94               1075.81               1069.22
Customer Distribution (TPC-H Q13)                                 1876.89               1894.83               1953.09               1905.28
Forecasting Revenue Change (TPC-H Q14)                             564.64                567.02                574.17                562.97
Top Supplier Query (TPC-H Q15)                                     565.38                567.10                567.25                567.64
Parts/Supplier Relationship (TPC-H Q16)                            572.21                582.05                577.98                577.82
Small-Quantity-Order Revenue (TPC-H Q17)                          2107.27               2024.30               2081.42               2082.15
Large Volume Customer (TPC-H Q18)                                 7400.72               8028.22               7437.48               7413.39
Discounted Revenue (TPC-H Q19)                                     719.29                717.86                720.79                715.91
Potential Part Promotion (TPC-H Q20)                               691.82                694.70                658.50                667.95
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                967.97                970.01                960.62                942.84
Global Sales Opportunity Query (TPC-H Q22)                         256.03                244.30                228.00                234.21

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-2-1-1           0.0          126.0         3.0      181.0     312.0
PostgreSQL-BHT-2-1-2           0.0          126.0         3.0      181.0     312.0
PostgreSQL-BHT-2-2-1           0.0          126.0         3.0      181.0     312.0
PostgreSQL-BHT-2-2-2           0.0          126.0         3.0      181.0     312.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-2-1-1           0.89
PostgreSQL-BHT-2-1-2           0.88
PostgreSQL-BHT-2-2-1           0.88
PostgreSQL-BHT-2-2-2           0.88

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-2-1-1            4064.70
PostgreSQL-BHT-2-1-2            4074.64
PostgreSQL-BHT-2-2-1            4102.17
PostgreSQL-BHT-2-2-2            4100.40

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                  time [s]  count   SF  Throughput@Size
DBMS               SF  num_experiment num_client                                       
PostgreSQL-BHT-2-1 1.0 1              1                 29      2  1.0          5462.07
PostgreSQL-BHT-2-2 1.0 1              2                 29      2  1.0          5462.07

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
```


### Database-Per-Tenant

Example for power test with 2 tenants, each having a dedicated database in the same DBMS:
```bash
nohup python tpch.py \
  -mtn 2 -mtb database \
  -sf 1 \
  --dbms PostgreSQL \
  -ii -ic -is \
  -nlp 2 -nbp 1 \
  -ne 2,2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/test_tpch_run_postgresql_tenants_database.log &
```

test_tpch_run_postgresql_tenants_database.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 829s 
    Code: 1750353147
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
    Loading is tested with [1] threads, split into [2] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [2, 2] times the number of benchmarking pods.
    Number of tenants is 2, one database per tenant.
    Experiment is run once.

### Connections
PostgreSQL-BHT-2-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:404505516
    datadisk:5496
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750353147
        TENANT_BY:database
        TENANT_NUM:2
PostgreSQL-BHT-2-1-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:404505516
    datadisk:5496
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750353147
        TENANT_BY:database
        TENANT_NUM:2
PostgreSQL-BHT-2-2-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:404505644
    datadisk:5496
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750353147
        TENANT_BY:database
        TENANT_NUM:2
PostgreSQL-BHT-2-2-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:404505644
    datadisk:5496
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750353147
        TENANT_BY:database
        TENANT_NUM:2

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-2-1-1  PostgreSQL-BHT-2-1-2  PostgreSQL-BHT-2-2-1  PostgreSQL-BHT-2-2-2
Pricing Summary Report (TPC-H Q1)                                 2535.16               2560.78               2534.69               2559.49
Minimum Cost Supplier Query (TPC-H Q2)                             440.04                436.67                434.29                433.25
Shipping Priority (TPC-H Q3)                                       770.69                796.80                754.80                761.52
Order Priority Checking Query (TPC-H Q4)                          1292.76               1333.43               1293.23               1276.90
Local Supplier Volume (TPC-H Q5)                                   672.24                691.72                687.10                672.35
Forecasting Revenue Change (TPC-H Q6)                              507.84                512.99                511.54                511.30
Forecasting Revenue Change (TPC-H Q7)                              789.88                780.94                785.88                774.65
National Market Share (TPC-H Q8)                                   635.07                640.30                626.69                632.52
Product Type Profit Measure (TPC-H Q9)                            1139.05               1121.06               1108.05               1100.29
Forecasting Revenue Change (TPC-H Q10)                            1323.11               1282.26               1322.12               1287.62
Important Stock Identification (TPC-H Q11)                         261.39                257.40                272.07                256.86
Shipping Modes and Order Priority (TPC-H Q12)                     1070.84               1043.70               1081.28               1048.22
Customer Distribution (TPC-H Q13)                                 2066.18               2044.67               2081.73               2003.59
Forecasting Revenue Change (TPC-H Q14)                             567.87                569.49                546.74                557.69
Top Supplier Query (TPC-H Q15)                                     595.62                571.90                564.56                565.63
Parts/Supplier Relationship (TPC-H Q16)                            570.72                595.31                577.52                569.76
Small-Quantity-Order Revenue (TPC-H Q17)                          2159.90               2088.75               2166.86               2025.73
Large Volume Customer (TPC-H Q18)                                 7048.82               7114.40               7464.36               7450.41
Discounted Revenue (TPC-H Q19)                                     714.45                716.57                706.68                709.31
Potential Part Promotion (TPC-H Q20)                               715.30                687.11                670.06                654.16
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                929.48                926.86                880.95                908.14
Global Sales Opportunity Query (TPC-H Q22)                         243.84                247.91                226.64                226.54

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-2-1-1           0.0          127.0         6.0      182.0     322.0
PostgreSQL-BHT-2-1-2           0.0          127.0         6.0      182.0     322.0
PostgreSQL-BHT-2-2-1           0.0          127.0         6.0      182.0     322.0
PostgreSQL-BHT-2-2-2           0.0          127.0         6.0      182.0     322.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-2-1-1           0.88
PostgreSQL-BHT-2-1-2           0.88
PostgreSQL-BHT-2-2-1           0.87
PostgreSQL-BHT-2-2-2           0.86

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-2-1-1            4102.39
PostgreSQL-BHT-2-1-2            4109.86
PostgreSQL-BHT-2-2-1            4142.92
PostgreSQL-BHT-2-2-2            4187.51

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                  time [s]  count   SF  Throughput@Size
DBMS               SF  num_experiment num_client                                       
PostgreSQL-BHT-2-1 1.0 1              1                 28      2  1.0          5657.14
PostgreSQL-BHT-2-2 1.0 1              2                 33      2  1.0          4800.00

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
```


### Container-Per-Tenant

Example for power test with 2 tenants, each having a dedicated DBMS:
```bash
nohup python tpch.py \
  -mtn 2 -mtb database \
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
    Duration: 739s 
    Code: 1750354803
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.8.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1, 1] times the number of benchmarking pods.
    Number of tenants is 2, one container per tenant.
    Experiment is run once.

### Connections
PostgreSQL-BHT-1-0-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:404059076
    datadisk:2757
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750354803
        TENANT_BY:container
        TENANT_NUM:2
PostgreSQL-BHT-1-0-2-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:404059196
    datadisk:2757
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750354803
        TENANT_BY:container
        TENANT_NUM:2
PostgreSQL-BHT-1-1-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:404059112
    datadisk:2757
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750354803
        TENANT_BY:container
        TENANT_NUM:2
PostgreSQL-BHT-1-1-2-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:404059068
    datadisk:2757
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750354803
        TENANT_BY:container
        TENANT_NUM:2

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-1-0-1-1  PostgreSQL-BHT-1-0-2-1  PostgreSQL-BHT-1-1-1-1  PostgreSQL-BHT-1-1-2-1
Pricing Summary Report (TPC-H Q1)                                   2595.13                 2542.19                 2678.92                 2664.32
Minimum Cost Supplier Query (TPC-H Q2)                               449.51                  426.70                  442.98                  435.19
Shipping Priority (TPC-H Q3)                                         773.37                  757.14                  817.51                  799.96
Order Priority Checking Query (TPC-H Q4)                            1306.04                 1266.85                 1297.85                 1286.83
Local Supplier Volume (TPC-H Q5)                                     676.21                  653.01                  703.75                  711.57
Forecasting Revenue Change (TPC-H Q6)                                507.18                  481.03                  534.69                  523.02
Forecasting Revenue Change (TPC-H Q7)                                813.61                  765.36                  808.30                  794.46
National Market Share (TPC-H Q8)                                     631.15                  629.07                  664.74                  650.47
Product Type Profit Measure (TPC-H Q9)                              1138.59                 1068.43                 1163.92                 1149.40
Forecasting Revenue Change (TPC-H Q10)                              1291.09                 1238.37                 1331.76                 1299.94
Important Stock Identification (TPC-H Q11)                           260.34                  249.95                  276.08                  271.37
Shipping Modes and Order Priority (TPC-H Q12)                       1036.15                 1020.72                 1085.29                 1037.68
Customer Distribution (TPC-H Q13)                                   2161.33                 1956.95                 2075.84                 2033.01
Forecasting Revenue Change (TPC-H Q14)                               555.04                  538.51                  574.16                  569.65
Top Supplier Query (TPC-H Q15)                                       568.20                  552.38                  589.85                  581.81
Parts/Supplier Relationship (TPC-H Q16)                              565.85                  566.06                  577.70                  583.47
Small-Quantity-Order Revenue (TPC-H Q17)                            2107.43                 1904.31                 2114.23                 1944.85
Large Volume Customer (TPC-H Q18)                                   8129.29                 7517.60                 7108.87                 7896.40
Discounted Revenue (TPC-H Q19)                                       706.68                  695.28                  735.10                  715.18
Potential Part Promotion (TPC-H Q20)                                 692.70                  626.02                  668.52                  643.88
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                  939.96                  889.95                  965.36                  911.12
Global Sales Opportunity Query (TPC-H Q22)                           250.09                  218.01                  255.10                  237.73

### Loading [s]
                        timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-1-0-1-1           0.0          128.0         2.0       92.0     232.0
PostgreSQL-BHT-1-0-2-1           0.0          128.0         2.0       92.0     232.0
PostgreSQL-BHT-1-1-1-1           0.0          132.0         2.0       92.0     228.0
PostgreSQL-BHT-1-1-2-1           0.0          132.0         2.0       92.0     228.0

### Geometric Mean of Medians of Timer Run [s]
                        Geo Times [s]
DBMS                                 
PostgreSQL-BHT-1-0-1-1           0.88
PostgreSQL-BHT-1-0-2-1           0.84
PostgreSQL-BHT-1-1-1-1           0.90
PostgreSQL-BHT-1-1-2-1           0.88

### Power@Size ((3600*SF)/(geo times))
                        Power@Size [~Q/h]
DBMS                                     
PostgreSQL-BHT-1-0-1-1            4083.33
PostgreSQL-BHT-1-0-2-1            4289.59
PostgreSQL-BHT-1-1-1-1            4021.88
PostgreSQL-BHT-1-1-2-1            4096.90

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                    time [s]  count   SF  Throughput@Size
DBMS                 SF  num_experiment num_client                                       
PostgreSQL-BHT-1-0-1 1.0 1              1                 30      1  1.0          2640.00
PostgreSQL-BHT-1-0-2 1.0 1              2                 28      1  1.0          2828.57
PostgreSQL-BHT-1-1-1 1.0 1              1                 29      1  1.0          2731.03
PostgreSQL-BHT-1-1-2 1.0 1              2                 29      1  1.0          2731.03

### Workflow

#### Actual
DBMS PostgreSQL-BHT-1-0 - Pods [[1, 1]]
DBMS PostgreSQL-BHT-1 - Pods [[1, 1]]

#### Planned
DBMS PostgreSQL-BHT-1-0 - Pods [[1, 1]]
DBMS PostgreSQL-BHT-1-1 - Pods [[1, 1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST failed: Workflow not as planned
```





## TPC-C


### Schema-Per-Tenant

Example for run with 2 tenants for 5 minutes, keying and thinking time activated, 1 warehouse and 10 clients per tenant, each having a dedicated schema in the same database:
```bash
nohup python benchbase.py \
  -mtn 2 -mtb schema \
  -sf 1 -sd 5 -xkey \
  --dbms PostgreSQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne 2,2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/test_benchbase_run_postgresql_tenants_schema.log &
```

test_benchbase_run_postgresql_tenants_schema.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=1
    Type: benchbase
    Duration: 1231s 
    Code: 1750583987
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.8.
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
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:425587596
    datadisk:638
    requests_cpu:2
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1750583987
                TENANT_BY:schema
                TENANT_NUM:2
PostgreSQL-1-1-1024-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:425588908
    datadisk:639
    requests_cpu:2
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1750583987
                TENANT_BY:schema
                TENANT_NUM:2

### Execution

#### Per Pod
                         experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                     
PostgreSQL-1-1-1024-1-1               1         10    1024       1      1  300.0           0                      0.456665                   0.456665   95.878387                                                      41540.0                                              14833.0
PostgreSQL-1-1-1024-1-2               1         10    1024       1      2  300.0           0                      0.556665                   0.556665  116.873653                                                      40618.0                                              14016.0
PostgreSQL-1-1-1024-2-2               1         10    1024       2      1  300.0           0                      0.463332                   0.466665   97.977915                                                      40437.0                                              15124.0
PostgreSQL-1-1-1024-2-1               1         10    1024       2      2  300.0           0                      0.466667                   0.470000   98.678057                                                      40630.0                                              14431.0

#### Aggregated Parallel
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         20    2048          2  300.0           0                          1.01                       1.01         0.0                                                      41540.0                                              14424.5
PostgreSQL-1-1-1024-2               1         20    2048          2  300.0           0                          0.93                       0.94         0.0                                                      40630.0                                              14777.5

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[2, 2]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[2, 2]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1       67.0        1.0   2.0          53.731343
PostgreSQL-1-1-1024-2       67.0        1.0   2.0          53.731343

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```


### Database-Per-Tenant

Example for run with 2 tenants for 5 minutes, keying and thinking time activated, 1 warehouse and 10 clients per tenant, each having a dedicated database in the same DBMS:
```bash
nohup python benchbase.py \
  -mtn 2 -mtb database \
  -sf 1 -sd 5 -xkey \
  --dbms PostgreSQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne 2,2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/test_benchbase_run_postgresql_tenants_database.log &
```

test_benchbase_run_postgresql_tenants_database.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=1
    Type: benchbase
    Duration: 1184s 
    Code: 1750585653
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.8.
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
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:425271916
    datadisk:659
    requests_cpu:2
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1750585653
                TENANT_BY:database
                TENANT_NUM:2
PostgreSQL-1-1-1024-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:425274436
    datadisk:660
    requests_cpu:2
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1750585653
                TENANT_BY:database
                TENANT_NUM:2

### Execution

#### Per Pod
                         experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                     
PostgreSQL-1-1-1024-1-2               1         10    1024       1      1  300.0           0                      0.469999                   0.469999   98.677772                                                      40222.0                                              15630.0
PostgreSQL-1-1-1024-1-1               1         10    1024       1      2  300.0           0                      0.513332                   0.509998  107.075890                                                      39544.0                                              14466.0
PostgreSQL-1-1-1024-2-2               1         10    1024       2      1  300.0           0                      0.480000                   0.480000  100.777602                                                      43551.0                                              15861.0
PostgreSQL-1-1-1024-2-1               1         10    1024       2      2  300.0           0                      0.479998                   0.483332  101.477124                                                      39247.0                                              14404.0

#### Aggregated Parallel
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         20    2048          2  300.0           0                          0.98                       0.98         0.0                                                      40222.0                                              15048.0
PostgreSQL-1-1-1024-2               1         20    2048          2  300.0           0                          0.96                       0.96         0.0                                                      43551.0                                              15132.5

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[2, 2]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[2, 2]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1       66.0        1.0   2.0          54.545455
PostgreSQL-1-1-1024-2       66.0        1.0   2.0          54.545455

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```


### Container-Per-Tenant

Example for run with 2 tenants for 5 minutes, keying and thinking time activated, 1 warehouse and 10 clients per tenant, each having a dedicated DBMS:
```bash
nohup python benchbase.py \
  -mtn 2 -mtb database \
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
    Duration: 1336s 
    Code: 1750586851
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.8.
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
PostgreSQL-1-1-1024-0-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:425278028
    datadisk:331
    requests_cpu:2
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1750586851
                TENANT_BY:container
                TENANT_NUM:2
PostgreSQL-1-1-1024-0-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:425280436
    datadisk:331
    requests_cpu:2
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1750586851
                TENANT_BY:container
                TENANT_NUM:2
PostgreSQL-1-1-1024-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:425278148
    datadisk:331
    requests_cpu:2
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1750586851
                TENANT_BY:container
                TENANT_NUM:2
                TENANT:1
PostgreSQL-1-1-1024-1-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:425280556
    datadisk:331
    requests_cpu:2
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1750586851
                TENANT_BY:container
                TENANT_NUM:2
                TENANT:1

### Execution

#### Per Pod
                           experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                       
PostgreSQL-1-1-1024-0-1-1               1         10    1024       1      1  300.0           0                      0.436665                   0.439999   92.379186                                                      36606.0                                              14803.0
PostgreSQL-1-1-1024-1-1-1               1         10    1024       1      1  300.0           0                      0.493332                   0.499998  104.976340                                                      37411.0                                              13621.0
PostgreSQL-1-1-1024-0-2-1               1         10    1024       2      1  300.0           0                      0.509998                   0.509998  107.075869                                                      37464.0                                              14789.0
PostgreSQL-1-1-1024-1-2-1               1         10    1024       2      1  300.0           0                      0.453332                   0.453332   95.178548                                                      39626.0                                              15109.0

#### Aggregated Parallel
                         experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-0-1               1         10    1024          1  300.0           0                          0.44                       0.44       92.38                                                      36606.0                                              14803.0
PostgreSQL-1-1-1024-0-2               1         10    1024          1  300.0           0                          0.51                       0.51      107.08                                                      37464.0                                              14789.0
PostgreSQL-1-1-1024-1-1               1         10    1024          1  300.0           0                          0.49                       0.50      104.98                                                      37411.0                                              13621.0
PostgreSQL-1-1-1024-1-2               1         10    1024          1  300.0           0                          0.45                       0.45       95.18                                                      39626.0                                              15109.0

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024-0 - Pods [[1, 1]]
DBMS PostgreSQL-1-1-1024-1 - Pods [[1, 1]]

#### Planned
DBMS PostgreSQL-1-1-1024-0 - Pods [[1, 1]]
DBMS PostgreSQL-1-1-1024-1 - Pods [[1, 1]]

### Loading
                         time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-0-1       69.0        1.0   1.0          52.173913
PostgreSQL-1-1-1024-0-2       69.0        1.0   1.0          52.173913
PostgreSQL-1-1-1024-1-1       65.0        1.0   1.0          55.384615
PostgreSQL-1-1-1024-1-2       65.0        1.0   1.0          55.384615

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```

