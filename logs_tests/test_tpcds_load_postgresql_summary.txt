## Show Summary

### Workload
TPC-DS Data Loading SF=1
    Type: tpcds
    Duration: 268s 
    Code: 1749632890
    This includes the reading queries of TPC-DS.
    This imports TPC-DS data sets.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Experiment is run once.

### Services
PostgreSQL-BHT-1
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-bht-1-1749632890 9091:9091

### Connections
PostgreSQL-BHT-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:386611056
    datadisk:40
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749632890

### Loading [s]
                    timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-1-1           0.0            0.0         1.0        1.0       3.0

### Tests
