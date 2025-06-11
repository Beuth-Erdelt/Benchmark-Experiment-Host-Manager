## Show Summary

### Workload
HammerDB Start DBMS
    Type: tpcc
    Duration: 186s 
    Code: 1749629932
    Start DBMS and do not load data.
    This just starts a SUT.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    SUT is fixed to cl-worker11.
    Experiment is run once.

### Services
PostgreSQL-BHT-1-1
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-bht-1-1-1749629932 9091:9091

### Connections
PostgreSQL-BHT-1-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:386794388
    datadisk:39
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749629932

### Tests
