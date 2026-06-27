## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 9694s 
* Code: 1780391716
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '1024'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Experiment uses bexhoma version 0.9.9.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 4 and 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker3.
  * Loading is tested with [32, 64] threads, split into [4, 8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MySQL-1-1-1 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:94107
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780391716
* MySQL-2-1-1 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:94075
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780391716
* MySQL-3-1-1 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:94108
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780391716
* MySQL-4-1-1 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:94080
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780391716

### Workflow

#### Actual

* DBMS MySQL-1 - Pods [[1]]
* DBMS MySQL-2 - Pods [[1]]
* DBMS MySQL-3 - Pods [[1]]
* DBMS MySQL-4 - Pods [[1]]

#### Planned

* DBMS MySQL-1 - Pods [[1]]
* DBMS MySQL-2 - Pods [[1]]
* DBMS MySQL-3 - Pods [[1]]
* DBMS MySQL-4 - Pods [[1]]

### Loading

#### Per Connection

| connection    |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1-0-1 |             1.00 |      8.00 |   256.00 |        4.00 |         0.00 |                          254.24 |               983341.00 |            250000.00 |                             16495.00 |
| MySQL-1-1-0-2 |             1.00 |      8.00 |   256.00 |        4.00 |         0.00 |                          254.41 |               982675.00 |            250000.00 |                             16559.00 |
| MySQL-1-1-0-3 |             1.00 |      8.00 |   256.00 |        4.00 |         0.00 |                          254.31 |               983041.00 |            250000.00 |                             16335.00 |
| MySQL-1-1-0-4 |             1.00 |      8.00 |   256.00 |        4.00 |         0.00 |                          254.21 |               983433.00 |            250000.00 |                             16511.00 |
| MySQL-2-1-0-1 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.90 |               977335.00 |            125000.00 |                             16127.00 |
| MySQL-2-1-0-2 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.90 |               977360.00 |            125000.00 |                             16135.00 |
| MySQL-2-1-0-3 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.89 |               977383.00 |            125000.00 |                             16119.00 |
| MySQL-2-1-0-4 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.89 |               977431.00 |            125000.00 |                             16079.00 |
| MySQL-2-1-0-5 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.89 |               977384.00 |            125000.00 |                             16383.00 |
| MySQL-2-1-0-6 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.90 |               977356.00 |            125000.00 |                             16255.00 |
| MySQL-2-1-0-7 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.90 |               977329.00 |            125000.00 |                             16231.00 |
| MySQL-2-1-0-8 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.89 |               977377.00 |            125000.00 |                             15999.00 |
| MySQL-3-1-0-1 |             1.00 |     16.00 |   256.00 |        4.00 |         0.00 |                          254.10 |               983854.00 |            250000.00 |                             16447.00 |
| MySQL-3-1-0-2 |             1.00 |     16.00 |   256.00 |        4.00 |         0.00 |                          254.26 |               983244.00 |            250000.00 |                             16703.00 |
| MySQL-3-1-0-3 |             1.00 |     16.00 |   256.00 |        4.00 |         0.00 |                          254.17 |               983604.00 |            250000.00 |                             16575.00 |
| MySQL-3-1-0-4 |             1.00 |     16.00 |   256.00 |        4.00 |         0.00 |                          254.06 |               984030.00 |            250000.00 |                             16447.00 |
| MySQL-4-1-0-1 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.87 |               977529.00 |            125000.00 |                             16575.00 |
| MySQL-4-1-0-2 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.88 |               977501.00 |            125000.00 |                             16927.00 |
| MySQL-4-1-0-3 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.88 |               977470.00 |            125000.00 |                             16303.00 |
| MySQL-4-1-0-4 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.87 |               977549.00 |            125000.00 |                             16287.00 |
| MySQL-4-1-0-5 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.87 |               977536.00 |            125000.00 |                             16327.00 |
| MySQL-4-1-0-6 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.87 |               977566.00 |            125000.00 |                             16143.00 |
| MySQL-4-1-0-7 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.88 |               977473.00 |            125000.00 |                             16623.00 |
| MySQL-4-1-0-8 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.85 |               977696.00 |            125000.00 |                             16167.00 |

#### Per Run

| DBMS      |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1 |             1.00 |     32.00 |  1024.00 |        4.00 |         0.00 |                         1017.17 |               983433.00 |           1000000.00 |                             16475.00 |
| MySQL-2-1 |             1.00 |     32.00 |  1024.00 |        8.00 |         0.00 |                         1023.15 |               977431.00 |           1000000.00 |                             16166.00 |
| MySQL-3-1 |             1.00 |     64.00 |  1024.00 |        4.00 |         0.00 |                         1016.59 |               984030.00 |           1000000.00 |                             16543.00 |
| MySQL-4-1 |             1.00 |     64.00 |  1024.00 |        8.00 |         0.00 |                         1022.98 |               977696.00 |           1000000.00 |                             16419.00 |

### Execution

#### Per Connection

| DBMS          | configuration   |   experiment_run |   client |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------|:----------------|-----------------:|---------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1-1-1 | MySQL-1         |                1 |        1 |       1 |        64 |     1024 |           1 |            0 |                         1022.03 |               978441.00 |             499891 |                            1225.00 |               500109 |                             14967.00 |
| MySQL-2-1-1-1 | MySQL-2         |                1 |        1 |       1 |        64 |     1024 |           1 |            0 |                         1022.07 |               978404.00 |             498987 |                            1218.00 |               501013 |                             15103.00 |
| MySQL-3-1-1-1 | MySQL-3         |                1 |        1 |       1 |        64 |     1024 |           1 |            0 |                         1022.21 |               978274.00 |             499498 |                            1215.00 |               500502 |                             15111.00 |
| MySQL-4-1-1-1 | MySQL-4         |                1 |        1 |       1 |        64 |     1024 |           1 |            0 |                         1021.89 |               978579.00 |             500273 |                            1174.00 |               499727 |                             15015.00 |

#### Per Phase

| DBMS        |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1-1 |             1.00 |     64.00 |  1024.00 |        1.00 |         0.00 |                         1022.03 |               978441.00 |          499891.00 |                            1225.00 |            500109.00 |                             14967.00 |
| MySQL-2-1-1 |             1.00 |     64.00 |  1024.00 |        1.00 |         0.00 |                         1022.07 |               978404.00 |          498987.00 |                            1218.00 |            501013.00 |                             15103.00 |
| MySQL-3-1-1 |             1.00 |     64.00 |  1024.00 |        1.00 |         0.00 |                         1022.21 |               978274.00 |          499498.00 |                            1215.00 |            500502.00 |                             15111.00 |
| MySQL-4-1-1 |             1.00 |     64.00 |  1024.00 |        1.00 |         0.00 |                         1021.89 |               978579.00 |          500273.00 |                            1174.00 |            499727.00 |                             15015.00 |

### Tests
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
