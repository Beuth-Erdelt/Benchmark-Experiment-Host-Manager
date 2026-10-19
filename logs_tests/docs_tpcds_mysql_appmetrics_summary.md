## Show Summary

### Workload
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 1501s 
* Code: 1792330119
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.11.6.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 2 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [2] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:898804
  * volume_size:1.8T
  * volume_used:878G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1792330119

### SUT Container Restarts
* bexhoma-sut-mysql-1-1792330119-55cdfb74c9-sgm7c: 1 (dbms=1, monitor-application=0)
  * dbms: OOMKilled (exit 137) at Sun, 18 Oct 2026 15:48:32 +0200; data on a mounted volume

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |    3 |      753.00 |           6.00 |            0.00 |        177.00 |          566.00 |              2 |           0 |             | None           |             0 | False         |               14.34 | False               |

### Benchmarking

#### Per Connection

No rows: these totals count only queries that succeeded in every connection of this experiment, and no query did (Q1 failed in 1 of 1 connections; Q2 failed in 1 of 1 connections; Q3 failed in 1 of 1 connections; Q4 failed in 1 of 1 connections; Q5 failed in 1 of 1 connections; Q6 failed in 1 of 1 connections; Q7 failed in 1 of 1 connections; Q8 failed in 1 of 1 connections; Q9 failed in 1 of 1 connections; Q10 failed in 1 of 1 connections; Q11 failed in 1 of 1 connections; Q12 failed in 1 of 1 connections; Q13 failed in 1 of 1 connections; Q14 failed in 1 of 1 connections; Q15 failed in 1 of 1 connections; Q16 failed in 1 of 1 connections; Q17 failed in 1 of 1 connections; Q18 failed in 1 of 1 connections; Q19 failed in 1 of 1 connections; Q20 failed in 1 of 1 connections; Q21 failed in 1 of 1 connections; Q22 failed in 1 of 1 connections; Q23 failed in 1 of 1 connections; Q24 failed in 1 of 1 connections; Q25 failed in 1 of 1 connections; Q26 failed in 1 of 1 connections; Q27 failed in 1 of 1 connections; Q28 failed in 1 of 1 connections; Q29 failed in 1 of 1 connections; Q30 failed in 1 of 1 connections; Q31 failed in 1 of 1 connections; Q32 failed in 1 of 1 connections; Q33 failed in 1 of 1 connections; Q34 failed in 1 of 1 connections; Q35 failed in 1 of 1 connections; Q36 failed in 1 of 1 connections; Q37 failed in 1 of 1 connections; Q38 failed in 1 of 1 connections; Q39 failed in 1 of 1 connections; Q40 failed in 1 of 1 connections; Q41 failed in 1 of 1 connections; Q42 failed in 1 of 1 connections; Q43 failed in 1 of 1 connections; Q44 failed in 1 of 1 connections; Q45 failed in 1 of 1 connections; Q46 failed in 1 of 1 connections; Q47 failed in 1 of 1 connections; Q48 failed in 1 of 1 connections; Q49 failed in 1 of 1 connections; Q50 failed in 1 of 1 connections; Q51 failed in 1 of 1 connections; Q52 failed in 1 of 1 connections; Q53 failed in 1 of 1 connections; Q54 failed in 1 of 1 connections; Q55 failed in 1 of 1 connections; Q56 failed in 1 of 1 connections; Q57 failed in 1 of 1 connections; Q58 failed in 1 of 1 connections; Q59 failed in 1 of 1 connections; Q60 failed in 1 of 1 connections; Q61 failed in 1 of 1 connections; Q62 failed in 1 of 1 connections; Q63 failed in 1 of 1 connections; Q64 failed in 1 of 1 connections; Q65 failed in 1 of 1 connections; Q66 failed in 1 of 1 connections; Q67 failed in 1 of 1 connections; Q68 failed in 1 of 1 connections; Q69 failed in 1 of 1 connections; Q70 failed in 1 of 1 connections; Q71 failed in 1 of 1 connections; Q72 failed in 1 of 1 connections; Q73 failed in 1 of 1 connections; Q74 failed in 1 of 1 connections; Q75 failed in 1 of 1 connections; Q76 failed in 1 of 1 connections; Q77 failed in 1 of 1 connections; Q78 failed in 1 of 1 connections; Q79 failed in 1 of 1 connections; Q80 failed in 1 of 1 connections; Q81 failed in 1 of 1 connections; Q82 failed in 1 of 1 connections; Q83 failed in 1 of 1 connections; Q84 failed in 1 of 1 connections; Q85 failed in 1 of 1 connections; Q86 failed in 1 of 1 connections; Q87 failed in 1 of 1 connections; Q88 failed in 1 of 1 connections; Q89 failed in 1 of 1 connections; Q90 failed in 1 of 1 connections; Q91 failed in 1 of 1 connections; Q92 failed in 1 of 1 connections; Q93 failed in 1 of 1 connections; Q94 failed in 1 of 1 connections; Q95 failed in 1 of 1 connections; Q96 failed in 1 of 1 connections; Q97 failed in 1 of 1 connections; Q98 failed in 1 of 1 connections; Q99 failed in 1 of 1 connections). See Query Completion per Phase for where, and Per Phase (Complete Phases Only) for the phases that completed every query.

#### Per Phase

No rows: these totals count only queries that succeeded in every connection of this experiment, and no query did (Q1 failed in 1 of 1 connections; Q2 failed in 1 of 1 connections; Q3 failed in 1 of 1 connections; Q4 failed in 1 of 1 connections; Q5 failed in 1 of 1 connections; Q6 failed in 1 of 1 connections; Q7 failed in 1 of 1 connections; Q8 failed in 1 of 1 connections; Q9 failed in 1 of 1 connections; Q10 failed in 1 of 1 connections; Q11 failed in 1 of 1 connections; Q12 failed in 1 of 1 connections; Q13 failed in 1 of 1 connections; Q14 failed in 1 of 1 connections; Q15 failed in 1 of 1 connections; Q16 failed in 1 of 1 connections; Q17 failed in 1 of 1 connections; Q18 failed in 1 of 1 connections; Q19 failed in 1 of 1 connections; Q20 failed in 1 of 1 connections; Q21 failed in 1 of 1 connections; Q22 failed in 1 of 1 connections; Q23 failed in 1 of 1 connections; Q24 failed in 1 of 1 connections; Q25 failed in 1 of 1 connections; Q26 failed in 1 of 1 connections; Q27 failed in 1 of 1 connections; Q28 failed in 1 of 1 connections; Q29 failed in 1 of 1 connections; Q30 failed in 1 of 1 connections; Q31 failed in 1 of 1 connections; Q32 failed in 1 of 1 connections; Q33 failed in 1 of 1 connections; Q34 failed in 1 of 1 connections; Q35 failed in 1 of 1 connections; Q36 failed in 1 of 1 connections; Q37 failed in 1 of 1 connections; Q38 failed in 1 of 1 connections; Q39 failed in 1 of 1 connections; Q40 failed in 1 of 1 connections; Q41 failed in 1 of 1 connections; Q42 failed in 1 of 1 connections; Q43 failed in 1 of 1 connections; Q44 failed in 1 of 1 connections; Q45 failed in 1 of 1 connections; Q46 failed in 1 of 1 connections; Q47 failed in 1 of 1 connections; Q48 failed in 1 of 1 connections; Q49 failed in 1 of 1 connections; Q50 failed in 1 of 1 connections; Q51 failed in 1 of 1 connections; Q52 failed in 1 of 1 connections; Q53 failed in 1 of 1 connections; Q54 failed in 1 of 1 connections; Q55 failed in 1 of 1 connections; Q56 failed in 1 of 1 connections; Q57 failed in 1 of 1 connections; Q58 failed in 1 of 1 connections; Q59 failed in 1 of 1 connections; Q60 failed in 1 of 1 connections; Q61 failed in 1 of 1 connections; Q62 failed in 1 of 1 connections; Q63 failed in 1 of 1 connections; Q64 failed in 1 of 1 connections; Q65 failed in 1 of 1 connections; Q66 failed in 1 of 1 connections; Q67 failed in 1 of 1 connections; Q68 failed in 1 of 1 connections; Q69 failed in 1 of 1 connections; Q70 failed in 1 of 1 connections; Q71 failed in 1 of 1 connections; Q72 failed in 1 of 1 connections; Q73 failed in 1 of 1 connections; Q74 failed in 1 of 1 connections; Q75 failed in 1 of 1 connections; Q76 failed in 1 of 1 connections; Q77 failed in 1 of 1 connections; Q78 failed in 1 of 1 connections; Q79 failed in 1 of 1 connections; Q80 failed in 1 of 1 connections; Q81 failed in 1 of 1 connections; Q82 failed in 1 of 1 connections; Q83 failed in 1 of 1 connections; Q84 failed in 1 of 1 connections; Q85 failed in 1 of 1 connections; Q86 failed in 1 of 1 connections; Q87 failed in 1 of 1 connections; Q88 failed in 1 of 1 connections; Q89 failed in 1 of 1 connections; Q90 failed in 1 of 1 connections; Q91 failed in 1 of 1 connections; Q92 failed in 1 of 1 connections; Q93 failed in 1 of 1 connections; Q94 failed in 1 of 1 connections; Q95 failed in 1 of 1 connections; Q96 failed in 1 of 1 connections; Q97 failed in 1 of 1 connections; Q98 failed in 1 of 1 connections; Q99 failed in 1 of 1 connections). See Query Completion per Phase for where, and Per Phase (Complete Phases Only) for the phases that completed every query.

#### Query Completion per Phase

| phase       |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mysql-1-1-1 |      1 | 0/1         | 0/1         | 0/1         | 0/1         | 0/1         | 0/1         | 0/1         | 0/1         | 0/1         | 0/1          | 0/1          | 0/1          | 0/1          | 0/1             | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1             | 0/1             | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1             | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | no         |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

#### Per Phase (Complete Phases Only)

Only the 0 of 1 phases in which every pod completed every active query; each row covers all 99 active queries, so the rows are comparable with each other. Left out: mysql-1-1-1 — see Query Completion per Phase.

### Latency of Timer Execution [ms]
No rows: these totals count only queries that succeeded in every connection of this experiment, and no query did (Q1 failed in 1 of 1 connections; Q2 failed in 1 of 1 connections; Q3 failed in 1 of 1 connections; Q4 failed in 1 of 1 connections; Q5 failed in 1 of 1 connections; Q6 failed in 1 of 1 connections; Q7 failed in 1 of 1 connections; Q8 failed in 1 of 1 connections; Q9 failed in 1 of 1 connections; Q10 failed in 1 of 1 connections; Q11 failed in 1 of 1 connections; Q12 failed in 1 of 1 connections; Q13 failed in 1 of 1 connections; Q14 failed in 1 of 1 connections; Q15 failed in 1 of 1 connections; Q16 failed in 1 of 1 connections; Q17 failed in 1 of 1 connections; Q18 failed in 1 of 1 connections; Q19 failed in 1 of 1 connections; Q20 failed in 1 of 1 connections; Q21 failed in 1 of 1 connections; Q22 failed in 1 of 1 connections; Q23 failed in 1 of 1 connections; Q24 failed in 1 of 1 connections; Q25 failed in 1 of 1 connections; Q26 failed in 1 of 1 connections; Q27 failed in 1 of 1 connections; Q28 failed in 1 of 1 connections; Q29 failed in 1 of 1 connections; Q30 failed in 1 of 1 connections; Q31 failed in 1 of 1 connections; Q32 failed in 1 of 1 connections; Q33 failed in 1 of 1 connections; Q34 failed in 1 of 1 connections; Q35 failed in 1 of 1 connections; Q36 failed in 1 of 1 connections; Q37 failed in 1 of 1 connections; Q38 failed in 1 of 1 connections; Q39 failed in 1 of 1 connections; Q40 failed in 1 of 1 connections; Q41 failed in 1 of 1 connections; Q42 failed in 1 of 1 connections; Q43 failed in 1 of 1 connections; Q44 failed in 1 of 1 connections; Q45 failed in 1 of 1 connections; Q46 failed in 1 of 1 connections; Q47 failed in 1 of 1 connections; Q48 failed in 1 of 1 connections; Q49 failed in 1 of 1 connections; Q50 failed in 1 of 1 connections; Q51 failed in 1 of 1 connections; Q52 failed in 1 of 1 connections; Q53 failed in 1 of 1 connections; Q54 failed in 1 of 1 connections; Q55 failed in 1 of 1 connections; Q56 failed in 1 of 1 connections; Q57 failed in 1 of 1 connections; Q58 failed in 1 of 1 connections; Q59 failed in 1 of 1 connections; Q60 failed in 1 of 1 connections; Q61 failed in 1 of 1 connections; Q62 failed in 1 of 1 connections; Q63 failed in 1 of 1 connections; Q64 failed in 1 of 1 connections; Q65 failed in 1 of 1 connections; Q66 failed in 1 of 1 connections; Q67 failed in 1 of 1 connections; Q68 failed in 1 of 1 connections; Q69 failed in 1 of 1 connections; Q70 failed in 1 of 1 connections; Q71 failed in 1 of 1 connections; Q72 failed in 1 of 1 connections; Q73 failed in 1 of 1 connections; Q74 failed in 1 of 1 connections; Q75 failed in 1 of 1 connections; Q76 failed in 1 of 1 connections; Q77 failed in 1 of 1 connections; Q78 failed in 1 of 1 connections; Q79 failed in 1 of 1 connections; Q80 failed in 1 of 1 connections; Q81 failed in 1 of 1 connections; Q82 failed in 1 of 1 connections; Q83 failed in 1 of 1 connections; Q84 failed in 1 of 1 connections; Q85 failed in 1 of 1 connections; Q86 failed in 1 of 1 connections; Q87 failed in 1 of 1 connections; Q88 failed in 1 of 1 connections; Q89 failed in 1 of 1 connections; Q90 failed in 1 of 1 connections; Q91 failed in 1 of 1 connections; Q92 failed in 1 of 1 connections; Q93 failed in 1 of 1 connections; Q94 failed in 1 of 1 connections; Q95 failed in 1 of 1 connections; Q96 failed in 1 of 1 connections; Q97 failed in 1 of 1 connections; Q98 failed in 1 of 1 connections; Q99 failed in 1 of 1 connections). See Query Completion per Phase for where, and Per Phase (Complete Phases Only) for the phases that completed every query.

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       970.77 |      2.95 |          63.98 |                 64.00 |

### Loading phase: component data generator

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |         6.79 |      0.13 |           0.01 |                  2.43 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |         0.00 |      1.03 |          63.98 |                 64.00 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Missing Monitoring Metrics
* CPU Utilization [CPUs] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log)
* Memory Usage, Working Set [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log)
* Memory Usage incl. Page Cache [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU User Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log)
* CPU System Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Connection Usage Ratio [0..1] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log)
* Average Redo Log Bytes per fsync [B] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log)
* InnoDB Buffer Pool Wait Free [count] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log)
* InnoDB Max Dirty Pages [%] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log)
* InnoDB Max Dirty Pages Low Watermark [%] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log)
* InnoDB Buffer Pool Bytes Data [B] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log)
* InnoDB Redo Log Flushed to Disk [B] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log)
* Ratio of Dirty Pages in Buffer Pool [%] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log)
* Threads Running for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log)
* Open Files Usage Ratio [0..1] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log)
* Memory Usage, Working Set [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                             1.18 |                            0.00 |                            0.02 |                              0.00 |

#### Benchmarking phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                             0.40 |                            0.00 |                            0.00 |                              0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST failed: No SUT container restarts
* TEST passed: SUT data survived container restarts
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Benchmarking phase: SUT deployment contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Benchmarking phase: component benchmarker contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST failed: Monitoring metrics missing
* TEST failed: Geo Times [s] contains 0 or NaN
* TEST failed: Power@Size [~Q/h] contains 0 or NaN
* TEST failed: Throughput@Size contains 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
