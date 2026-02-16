## Show Summary

### Workload
Benchbase Start DBMS
    Type: benchbase
    Duration: 187s 
    Code: 1749628596
    Intro: Start DBMS and do not load data.
    This just starts a SUT.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    SUT is fixed to cl-worker11.
    Experiment is run once.

### Services
PostgreSQL-1-1-1024
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-1-1-1024-1749628596 9091:9091

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:387168592
    datadisk:39
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1749628596

### Tests
