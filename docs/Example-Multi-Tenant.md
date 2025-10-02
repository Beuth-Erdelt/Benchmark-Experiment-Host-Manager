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

## PostgreSQL

### TPC-H

An extensive example for an evaluation is in the [repository](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/dev/MT-TPC-H-Merger-collector.ipynb).

#### Schema-Per-Tenant

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
    Duration: 435s 
    Code: 1758721012
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
    Benchmarking is tested with [64] threads, split into [1] pods.
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
    disk:435683892
    datadisk:5475
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1758721012
        TENANT_BY:schema
        TENANT_NUM:2
PostgreSQL-BHT-2-1-2 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:435683892
    datadisk:5475
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1758721012
        TENANT_BY:schema
        TENANT_NUM:2

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-2-1-1  PostgreSQL-BHT-2-1-2
Pricing Summary Report (TPC-H Q1)                                 2530.16               2537.68
Minimum Cost Supplier Query (TPC-H Q2)                             478.22                479.49
Shipping Priority (TPC-H Q3)                                       736.74                738.25
Order Priority Checking Query (TPC-H Q4)                           366.72                372.07
Local Supplier Volume (TPC-H Q5)                                   672.41                662.88
Forecasting Revenue Change (TPC-H Q6)                              480.45                474.21
Forecasting Revenue Change (TPC-H Q7)                              783.58                782.35
National Market Share (TPC-H Q8)                                   451.96                482.31
Product Type Profit Measure (TPC-H Q9)                            1052.85               1087.34
Forecasting Revenue Change (TPC-H Q10)                             616.21                620.68
Important Stock Identification (TPC-H Q11)                         180.13                186.72
Shipping Modes and Order Priority (TPC-H Q12)                      706.02                702.03
Customer Distribution (TPC-H Q13)                                 2232.58               2262.71
Forecasting Revenue Change (TPC-H Q14)                             523.79                517.70
Top Supplier Query (TPC-H Q15)                                     527.76                532.80
Parts/Supplier Relationship (TPC-H Q16)                            585.69                588.36
Small-Quantity-Order Revenue (TPC-H Q17)                          2052.93               1965.86
Large Volume Customer (TPC-H Q18)                                 5848.00               6460.44
Discounted Revenue (TPC-H Q19)                                     141.14                125.94
Potential Part Promotion (TPC-H Q20)                               281.37                263.08
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                763.64                762.30
Global Sales Opportunity Query (TPC-H Q22)                         230.03                229.54

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-2-1-1           1.0          115.0         1.0      181.0     300.0
PostgreSQL-BHT-2-1-2           1.0          115.0         1.0      181.0     300.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-2-1-1           0.66
PostgreSQL-BHT-2-1-2           0.66

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-2-1-1            5488.62
PostgreSQL-BHT-2-1-2            5484.90

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                  time [s]  count   SF  Throughput@Size
DBMS               SF  num_experiment num_client                                       
PostgreSQL-BHT-2-1 1.0 1              1                 25      2  1.0           6336.0

### Workflow
                               orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
PostgreSQL-BHT-2-1-1  PostgreSQL-BHT-2-1  1.0     2               1           1       1758721376     1758721401
PostgreSQL-BHT-2-1-2  PostgreSQL-BHT-2-1  1.0     2               1           1       1758721376     1758721401

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


#### Database-Per-Tenant

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
    Duration: 467s 
    Code: 1758721493
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
    Benchmarking is tested with [64] threads, split into [1] pods.
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
    disk:441329444
    datadisk:2757
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1758721493
        TENANT_BY:container
        TENANT_NUM:2
PostgreSQL-BHT-1-1-1-1 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:441329444
    datadisk:2757
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1758721493
        TENANT_BY:container
        TENANT_NUM:2
        TENANT:1
PostgreSQL-BHT-2-1-1 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:441329444
    datadisk:5489
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1758721493
        TENANT_BY:database
        TENANT_NUM:2
PostgreSQL-BHT-2-1-2 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:441329444
    datadisk:5489
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1758721493
        TENANT_BY:database
        TENANT_NUM:2

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-1-0-1-1  PostgreSQL-BHT-1-1-1-1  PostgreSQL-BHT-2-1-1  PostgreSQL-BHT-2-1-2
Pricing Summary Report (TPC-H Q1)                                   2287.47                 2277.68               2364.53               2364.78
Minimum Cost Supplier Query (TPC-H Q2)                               428.61                  444.66                508.20                495.13
Shipping Priority (TPC-H Q3)                                         700.51                  705.20                717.58                732.84
Order Priority Checking Query (TPC-H Q4)                             336.71                  347.10                372.14                371.88
Local Supplier Volume (TPC-H Q5)                                     616.76                  644.01                676.15                676.36
Forecasting Revenue Change (TPC-H Q6)                                470.07                  480.24                470.68                478.04
Forecasting Revenue Change (TPC-H Q7)                                718.12                  740.01                802.55                797.70
National Market Share (TPC-H Q8)                                     400.22                  402.16                418.38                413.35
Product Type Profit Measure (TPC-H Q9)                              1068.62                 1053.78               1053.17               1077.64
Forecasting Revenue Change (TPC-H Q10)                               582.07                  599.02                593.99                593.65
Important Stock Identification (TPC-H Q11)                           149.98                  162.13                177.12                171.10
Shipping Modes and Order Priority (TPC-H Q12)                        682.95                  683.88                695.74                696.34
Customer Distribution (TPC-H Q13)                                   2159.42                 2281.56               2099.96               2176.76
Forecasting Revenue Change (TPC-H Q14)                               505.18                  508.17                793.52                493.97
Top Supplier Query (TPC-H Q15)                                       507.64                  518.43                518.94                502.34
Parts/Supplier Relationship (TPC-H Q16)                              582.07                  577.65                581.77                594.53
Small-Quantity-Order Revenue (TPC-H Q17)                            1873.47                 1981.58               1937.60               1898.55
Large Volume Customer (TPC-H Q18)                                   5633.82                 6100.01               6565.06               6631.91
Discounted Revenue (TPC-H Q19)                                       129.09                  121.42                123.00                764.99
Potential Part Promotion (TPC-H Q20)                                 236.94                  242.46                363.98                266.73
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                  756.55                  761.78                764.43                755.50
Global Sales Opportunity Query (TPC-H Q22)                           224.76                  229.39                223.46                221.47

### Loading [s]
                        timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-1-0-1-1           0.0          101.0         0.0      179.0     285.0
PostgreSQL-BHT-1-1-1-1           0.0          100.0         1.0      179.0     282.0
PostgreSQL-BHT-2-1-1             2.0          116.0         2.0      213.0     335.0
PostgreSQL-BHT-2-1-2             2.0          116.0         2.0      213.0     335.0

### Geometric Mean of Medians of Timer Run [s]
                        Geo Times [s]
DBMS                                 
PostgreSQL-BHT-1-0-1-1           0.61
PostgreSQL-BHT-1-1-1-1           0.63
PostgreSQL-BHT-2-1-1             0.67
PostgreSQL-BHT-2-1-2             0.70

### Power@Size ((3600*SF)/(geo times))
                        Power@Size [~Q/h]
DBMS                                     
PostgreSQL-BHT-1-0-1-1            5864.90
PostgreSQL-BHT-1-1-1-1            5743.01
PostgreSQL-BHT-2-1-1              5408.02
PostgreSQL-BHT-2-1-2              5163.53

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                    time [s]  count   SF  Throughput@Size
DBMS                 SF  num_experiment num_client                                       
PostgreSQL-BHT-1-0-1 1.0 1              1                 22      1  1.0          3600.00
PostgreSQL-BHT-1-1-1 1.0 1              1                 23      1  1.0          3443.48
PostgreSQL-BHT-2-1   1.0 1              1                 25      2  1.0          6336.00

### Workflow
                                   orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
PostgreSQL-BHT-1-0-1-1  PostgreSQL-BHT-1-0-1  1.0     1               1           1       1758721873     1758721895
PostgreSQL-BHT-1-1-1-1  PostgreSQL-BHT-1-1-1  1.0     1               1           1       1758721872     1758721895
PostgreSQL-BHT-2-1-1      PostgreSQL-BHT-2-1  1.0     2               1           1       1758721889     1758721914
PostgreSQL-BHT-2-1-2      PostgreSQL-BHT-2-1  1.0     2               1           1       1758721889     1758721913

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


#### Container-Per-Tenant

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
    Duration: 454s 
    Code: 1758721493
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
    Benchmarking is run as [1] times the number of benchmarking pods.
    Number of tenants is 2, one container per tenant.
    Experiment is run once.

### Connections
PostgreSQL-BHT-1-0-1-1 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:441329444
    datadisk:2757
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1758721493
        TENANT_BY:container
        TENANT_NUM:2
PostgreSQL-BHT-1-1-1-1 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:441329444
    datadisk:2757
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1758721493
        TENANT_BY:container
        TENANT_NUM:2
        TENANT:1
PostgreSQL-BHT-2-1-1 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:441329444
    datadisk:5489
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1758721493
        TENANT_BY:database
        TENANT_NUM:2
PostgreSQL-BHT-2-1-2 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:441329444
    datadisk:5489
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1758721493
        TENANT_BY:database
        TENANT_NUM:2

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-1-0-1-1  PostgreSQL-BHT-1-1-1-1  PostgreSQL-BHT-2-1-1  PostgreSQL-BHT-2-1-2
Pricing Summary Report (TPC-H Q1)                                   2287.47                 2277.68               2364.53               2364.78
Minimum Cost Supplier Query (TPC-H Q2)                               428.61                  444.66                508.20                495.13
Shipping Priority (TPC-H Q3)                                         700.51                  705.20                717.58                732.84
Order Priority Checking Query (TPC-H Q4)                             336.71                  347.10                372.14                371.88
Local Supplier Volume (TPC-H Q5)                                     616.76                  644.01                676.15                676.36
Forecasting Revenue Change (TPC-H Q6)                                470.07                  480.24                470.68                478.04
Forecasting Revenue Change (TPC-H Q7)                                718.12                  740.01                802.55                797.70
National Market Share (TPC-H Q8)                                     400.22                  402.16                418.38                413.35
Product Type Profit Measure (TPC-H Q9)                              1068.62                 1053.78               1053.17               1077.64
Forecasting Revenue Change (TPC-H Q10)                               582.07                  599.02                593.99                593.65
Important Stock Identification (TPC-H Q11)                           149.98                  162.13                177.12                171.10
Shipping Modes and Order Priority (TPC-H Q12)                        682.95                  683.88                695.74                696.34
Customer Distribution (TPC-H Q13)                                   2159.42                 2281.56               2099.96               2176.76
Forecasting Revenue Change (TPC-H Q14)                               505.18                  508.17                793.52                493.97
Top Supplier Query (TPC-H Q15)                                       507.64                  518.43                518.94                502.34
Parts/Supplier Relationship (TPC-H Q16)                              582.07                  577.65                581.77                594.53
Small-Quantity-Order Revenue (TPC-H Q17)                            1873.47                 1981.58               1937.60               1898.55
Large Volume Customer (TPC-H Q18)                                   5633.82                 6100.01               6565.06               6631.91
Discounted Revenue (TPC-H Q19)                                       129.09                  121.42                123.00                764.99
Potential Part Promotion (TPC-H Q20)                                 236.94                  242.46                363.98                266.73
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                  756.55                  761.78                764.43                755.50
Global Sales Opportunity Query (TPC-H Q22)                           224.76                  229.39                223.46                221.47

### Loading [s]
                        timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-1-0-1-1           0.0          101.0         0.0      179.0     285.0
PostgreSQL-BHT-1-1-1-1           0.0          100.0         1.0      179.0     282.0
PostgreSQL-BHT-2-1-1             2.0          116.0         2.0      213.0     335.0
PostgreSQL-BHT-2-1-2             2.0          116.0         2.0      213.0     335.0

### Geometric Mean of Medians of Timer Run [s]
                        Geo Times [s]
DBMS                                 
PostgreSQL-BHT-1-0-1-1           0.61
PostgreSQL-BHT-1-1-1-1           0.63
PostgreSQL-BHT-2-1-1             0.67
PostgreSQL-BHT-2-1-2             0.70

### Power@Size ((3600*SF)/(geo times))
                        Power@Size [~Q/h]
DBMS                                     
PostgreSQL-BHT-1-0-1-1            5864.90
PostgreSQL-BHT-1-1-1-1            5743.01
PostgreSQL-BHT-2-1-1              5408.02
PostgreSQL-BHT-2-1-2              5163.53

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                    time [s]  count   SF  Throughput@Size
DBMS                 SF  num_experiment num_client                                       
PostgreSQL-BHT-1-0-1 1.0 1              1                 22      1  1.0          3600.00
PostgreSQL-BHT-1-1-1 1.0 1              1                 23      1  1.0          3443.48
PostgreSQL-BHT-2-1   1.0 1              1                 25      2  1.0          6336.00

### Workflow
                                   orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
PostgreSQL-BHT-1-0-1-1  PostgreSQL-BHT-1-0-1  1.0     1               1           1       1758721873     1758721895
PostgreSQL-BHT-1-1-1-1  PostgreSQL-BHT-1-1-1  1.0     1               1           1       1758721872     1758721895
PostgreSQL-BHT-2-1-1      PostgreSQL-BHT-2-1  1.0     2               1           1       1758721889     1758721914
PostgreSQL-BHT-2-1-2      PostgreSQL-BHT-2-1  1.0     2               1           1       1758721889     1758721913

#### Actual
DBMS PostgreSQL-BHT-1-0 - Pods [[1]]
DBMS PostgreSQL-BHT-1 - Pods [[1]]
DBMS PostgreSQL-BHT-2 - Pods [[2]]

#### Planned
DBMS PostgreSQL-BHT-1-0 - Pods [[1]]
DBMS PostgreSQL-BHT-1-1 - Pods [[1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST failed: Workflow not as planned
```





### TPC-C

An extensive example for an evaluation is in the [repository](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/dev/MT-Benchbase-Merger-collector.ipynb).


#### Schema-Per-Tenant

At first we remove old storage
```
kubectl delete pvc bexhoma-storage-postgresql-benchbase-tpcc-1
```

Example for run with 2 tenants for 5 minutes, keying and thinking time activated, 1 warehouse and 10 clients per tenant, each having a dedicated schema in the same database.
The execution phase is run twice.
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


#### Database-Per-Tenant

At first we remove old storage
```
kubectl delete pvc bexhoma-storage-postgresql-benchbase-tpcc-1
```

Example for run with 2 tenants for 5 minutes, keying and thinking time activated, 1 warehouse and 10 clients per tenant, each having a dedicated database in the same DBMS.
The execution phase is run twice.
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


#### Container-Per-Tenant

At first we remove old storage
```
kubectl delete pvc bexhoma-storage-postgresql-0-2-benchbase-tpcc-1
kubectl delete pvc bexhoma-storage-postgresql-1-2-benchbase-tpcc-1
```

Example for run with 2 tenants for 5 minutes, keying and thinking time activated, 1 warehouse and 10 clients per tenant, each having a dedicated DBMS.
The execution phase is run twice.
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

