## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 631s 
* Code: 1793531683
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [12].
  * Factors for benchmarking are [4]. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.11.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Garnet'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* garnet-1-1-1-1 uses docker image ghcr.io/microsoft/garnet:2.2.5
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:675148
  * datadisk:1527
  * volume_size:49G
  * volume_used:1.5G
  * cpu_list:0-223
  * args:['--port', '6379', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793531683
* garnet-1-2-1-1 uses docker image ghcr.io/microsoft/garnet:2.2.5
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:673792
  * datadisk:2513
  * volume_size:49G
  * volume_used:2.5G
  * cpu_list:0-223
  * args:['--port', '6379', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793531683

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: Garnet-1-2

### Data Parameters of Reused Volumes
* Garnet-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### Init Scripts Not in Folder
* Garnet-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-garnet-1-1793531683-5f49d776b5-qm97d: 0
* bexhoma-sut-garnet-1-1793531683-649bd899dd-fw6rj: 0

### Workflow

#### Actual

* DBMS Garnet-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Garnet-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS Garnet-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Garnet-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection       |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:-----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| garnet-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        15846.86 |                 7888.00 |            125000.00 |                              1382.00 | 1.00 |              456.39 |
| garnet-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        17499.65 |                 7143.00 |            125000.00 |                              1369.00 | 1.00 |              503.99 |
| garnet-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        15447.36 |                 8092.00 |            125000.00 |                              1390.00 | 1.00 |              444.88 |
| garnet-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        15118.53 |                 8268.00 |            125000.00 |                              1381.00 | 1.00 |              435.41 |
| garnet-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        17667.84 |                 7075.00 |            125000.00 |                              1502.00 | 1.00 |              508.83 |
| garnet-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        16960.65 |                 7370.00 |            125000.00 |                              1325.00 | 1.00 |              488.47 |
| garnet-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        18184.46 |                 6874.00 |            125000.00 |                              1363.00 | 1.00 |              523.71 |
| garnet-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        16598.06 |                 7531.00 |            125000.00 |                              1426.00 | 1.00 |              478.02 |

#### Per Run

| DBMS       |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:-----------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Garnet-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              435.41 |                       133323.41 |                 8268.00 |           1000000.00 |                              1392.25 |

### Benchmarking

#### Per Connection

| DBMS             | phase        | job            | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-------------|:---------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| garnet-1-1-1-1-1 | garnet-1-1-1 | garnet-1-1-1-1 | Garnet-1        |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        65472.02 |               152737.00 |            5000715 |                             535.00 |              4999285 |                               440.00 |
| garnet-1-2-1-1-1 | garnet-1-2-1 | garnet-1-2-1-1 | Garnet-1        |                2 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        65491.32 |               152692.00 |            4998870 |                             418.00 |              5001130 |                               401.00 |

#### Per Phase

| DBMS         | phase        |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------|:-------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| garnet-1-1-1 | garnet-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        65472.02 |               152737.00 |            5000715 |                             535.00 |              4999285 |                               440.00 |
| garnet-1-2-1 | garnet-1-2-1 |                2 |       128 |    65536 |               1 |           1 |            0 |                        65491.32 |               152692.00 |            4998870 |                             418.00 |              5001130 |                               401.00 |

#### Reset

| phase        | job            |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:-------------|:---------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| garnet-1-1-1 | garnet-1-1-1-1 |                1 |        1 |               1 |         4.00 |                |
| garnet-1-2-1 | garnet-1-2-1-1 |                2 |        1 |               1 |         6.00 |                |

### Monitoring

### Loading phase: component loader

| DBMS           | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|:-------------|----------:|---------------:|----------------------:|
| garnet-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: component benchmarker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| garnet-1-1-1-1 |       707.94 |      4.84 |           1.03 |                  1.03 |
| garnet-1-2-1-1 |       725.93 |      5.05 |           1.03 |        - waiting 30s -               : done
MariaDB-1                     : has running benchmarks
MariaDB-2                     : has running benchmarks
MariaDB-3                     : has running benchmarks
MariaDB-4                     : has running benchmarks
Loop pass                     : took 3.5s (0 kubectl calls 0.0s, 64 API requests 3.2s)
- waiting 30s -               : done
MariaDB-1                     : has running benchmarks
MariaDB-2                     : has running benchmarks
MariaDB-3                     : has running benchmarks
MariaDB-4                     : has running benchmarks
Loop pass                     : took 2.6s (0 kubectl calls 0.0s, 64 API requests 3.2s)
- waiting 30s -               : done
MariaDB-1                     : has running benchmarks
MariaDB-2                     : has running benchmarks
MariaDB-3                     : has running benchmarks
MariaDB-4                     : has running benchmarks
Loop pass                     : took 3.5s (0 kubectl calls 0.0s, 64 API requests 3.2s)
- waiting 30s -               : done
MariaDB-1                     : has running benchmarks
MariaDB-2                     : has running benchmarks
MariaDB-3                     : has running benchmarks
MariaDB-4                     : has running benchmarks
Loop pass                     : took 3.6s (0 kubectl calls 0.0s, 64 API requests 3.1s)
- waiting 30s -               : done
MariaDB-1                     : has running benchmarks
MariaDB-2                     : has running benchmarks
MariaDB-3                     : has running benchmarks
MariaDB-4                     : has running benchmarks
Loop pass                     : took 2.5s (0 kubectl calls 0.0s, 64 API requests 3.0s)
- waiting 30s -               : done
MariaDB-1                     : has running benchmarks
MariaDB-2                     : has running benchmarks
MariaDB-3                     : has running benchmarks
MariaDB-4                     : has running benchmarks
Loop pass                     : took 3.5s (0 kubectl calls 0.0s, 64 API requests 3.1s)
- waiting 30s -               : done
MariaDB-1                     : has running benchmarks
MariaDB-2                     : has running benchmarks
MariaDB-3                     : has running benchmarks
MariaDB-4                     : has running benchmarks
Loop pass                     : took 2.5s (0 kubectl calls 0.0s, 64 API requests 3.1s)
- waiting 30s -               : done
MariaDB-1                     : has running benchmarks
MariaDB-2                     : has running benchmarks
MariaDB-3                     : has running benchmarks
MariaDB-4                     : has running benchmarks
Loop pass                     : took 3.1s (0 kubectl calls 0.0s, 64 API requests 2.9s)
- waiting 30s -               : done
MariaDB-1                     : has running benchmarks
MariaDB-2                     : has running benchmarks
MariaDB-3                     : has running benchmarks
MariaDB-4                     : has running benchmarks
Loop pass                     : took 2.2s (0 kubectl calls 0.0s, 64 API requests 2.6s)
- waiting 30s -               : done
MariaDB-1                     : has running benchmarks
MariaDB-2                     : has running benchmarks
MariaDB-3                     : has running benchmarks
MariaDB-4                     : has running benchmarks
Loop pass                     : took 2.6s (0 kubectl calls 0.0s, 64 API requests 2.3s)
- waiting 30s -               : done
MariaDB-1                     : has running benchmarks
MariaDB-2                     : has running benchmarks
MariaDB-3                     : has running benchmarks
MariaDB-4                     : has running benchmarks
Loop pass                     : took 1.7s (0 kubectl calls 0.0s, 64 API requests 2.1s)
- waiting 30s -               : done
MariaDB-1                     : has running benchmarks
MariaDB-2                     : has running benchmarks
MariaDB-3                     : has running benchmarks
MariaDB-4                     : has running benchmarks
Loop pass                     : took 2.7s (0 kubectl calls 0.0s, 64 API requests 2.3s)
- waiting 30s -               : done
MariaDB-2                     : has running benchmarks
MariaDB-3                     : has running benchmarks
MariaDB-4                     : has running benchmarks
mariadb-1-1-1-1               : wrote benchmarking_timespans to D:/data/benchmarks/1794779752/mariadb-1-1-1-1.config
mariadb-1-1-1-1               : showing benchmarker times
mariadb-1-1-1-1               : benchmarker timespan job from 1794781118 to 1794782118
mariadb-1-1-1-1               : benchmarker timespan pods from 1794781121 to 1794782098
mariadb-1-1-1-1               : benchmarker timespan (start to end single container [s]) = 977
mariadb-1-1-1-1               : benchmarker times (start/end per pod and container) = [(1794781121, 1794782098)]
mariadb-1-1-1-1               : found and updated times {'benchmarker': [(1794781121, 1794782098)]}
Loop pass                     : took 9.6s (4 kubectl calls 4.5s, 69 API requests 2.7s)
MariaDB-1                     : can be stopped
MariaDB-1                     : had 0 restarts at worker bexhoma-sut-mariadb-1-1794779752-5dbc844949-ch6b2
MariaDB-2                     : has running benchmarks
MariaDB-3                     : has running benchmarks
MariaDB-4                     : has running benchmarks
Loop pass                     : took 5.7s (3 kubectl calls 3.0s, 74 API requests 2.6s)
- waiting 30s -               : done
mariadb-4-1-1-1               : wrote benchmarking_timespans to D:/data/benchmarks/1794779752/mariadb-4-1-1-1.config
mariadb-4-1-1-1               : showing benchmarker times
mariadb-4-1-1-1               : benchmarker timespan job from 1794781165 to 1794782161
mariadb-4-1-1-1               : benchmarker timespan pods from 1794781167 to 1794782145
mariadb-4-1-1-1               : benchmarker timespan (start to end single container [s]) = 978
mariadb-4-1-1-1               : benchmarker times (start/end per pod and container) = [(1794781167, 1794782145)]
mariadb-3-1-1-1               : wrote benchmarking_timespans to D:/data/benchmarks/1794779752/mariadb-3-1-1-1.config
mariadb-3-1-1-1               : showing benchmarker times
mariadb-3-1-1-1               : benchmarker timespan job from 1794781166 to 1794782161
mariadb-3-1-1-1               : benchmarker timespan pods from 1794781170 to 1794782147
mariadb-3-1-1-1               : benchmarker timespan (start to end single container [s]) = 977
mariadb-3-1-1-1               : benchmarker times (start/end per pod and container) = [(1794781170, 1794782147)]
mariadb-4-1-1-1               : found and updated times {'benchmarker': [(1794781167, 1794782145)]}
mariadb-3-1-1-1               : found and updated times {'benchmarker': [(1794781170, 1794782147)]}
mariadb-2-1-1-1               : wrote benchmarking_timespans to D:/data/benchmarks/1794779752/mariadb-2-1-1-1.config
mariadb-2-1-1-1               : showing benchmarker times
mariadb-2-1-1-1               : benchmarker timespan job from 1794781166 to 1794782161
mariadb-2-1-1-1               : benchmarker timespan pods from 1794781169 to 1794782147
mariadb-2-1-1-1               : benchmarker timespan (start to end single container [s]) = 978
mariadb-2-1-1-1               : benchmarker times (start/end per pod and container) = [(1794781169, 1794782147)]
mariadb-2-1-1-1               : found and updated times {'benchmarker': [(1794781169, 1794782147)]}
Experiment                    : ended 3 benchmarker jobs in 2.7s (4 at once; 6 kubectl calls 6.6s, 32 API requests 1.3s)
Loop pass                     : took 6.4s (8 kubectl calls 9.0s, 67 API requests 2.7s)
MariaDB-2                     : can be stopped
MariaDB-2                     : had 0 restarts at worker bexhoma-sut-mariadb-2-1794779752-6ddd65d4bf-t8vng
MariaDB-3                     : can be stopped
MariaDB-3                     : had 0 restarts at worker bexhoma-sut-mariadb-3-1794779752-6f9866b9-b98nk
MariaDB-4                     : can be stopped
MariaDB-4                     : had 0 restarts at worker bexhoma-sut-mariadb-4-1794779752-6cc6b45497-p4kkv
Loop pass                     : took 12.4s (9 kubectl calls 9.1s, 82 API requests 2.5s)
Experiment                    : ends at 2026-11-15 23:36:16.737806 (43649.528659) - 2423.94s total
Experiment                    : downloading partial results
Experiment                    : uploading full results
Experiment                    : uploading workload file
Result workflow complete

## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 2424s 
* Code: 1794779752
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
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 4 and 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [32, 64] threads, split into [4, 8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mariadb', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mariadb-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1060290
  * datadisk:1794
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794779752
* mariadb-2-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1060290
  * datadisk:1770
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794779752
* mariadb-3-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1060290
  * datadisk:1798
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794779752
* mariadb-4-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1060290
  * datadisk:1766
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794779752

### Ingestion
* MariaDB-1: 4 of 4 units ok
* MariaDB-2: 8 of 8 units ok
* MariaDB-3: 4 of 4 units ok
* MariaDB-4: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1794779752-5dbc844949-ch6b2: 0
* bexhoma-sut-mariadb-2-1794779752-6ddd65d4bf-t8vng: 0
* bexhoma-sut-mariadb-3-1794779752-6f9866b9-b98nk: 0
* bexhoma-sut-mariadb-4-1794779752-6cc6b45497-p4kkv: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MariaDB-2 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MariaDB-3 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MariaDB-4 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MariaDB-2 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MariaDB-3 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MariaDB-4 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection        |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| mariadb-1-1-0-1-1 |             1.00 |      8.00 |   256.00 |        4.00 |     0.00 |                          255.94 |               976810.00 |            250000.00 |                              4251.00 | 1.00 |                3.69 |
| mariadb-1-1-0-1-2 |             1.00 |      8.00 |   256.00 |        4.00 |     0.00 |                          255.93 |               976823.00 |            250000.00 |                              4187.00 | 1.00 |                3.69 |
| mariadb-1-1-0-1-3 |             1.00 |      8.00 |   256.00 |        4.00 |     0.00 |                          255.93 |               976819.00 |            250000.00 |                              4151.00 | 1.00 |                3.69 |
| mariadb-1-1-0-1-4 |             1.00 |      8.00 |   256.00 |        4.00 |     0.00 |                          255.93 |               976812.00 |            250000.00 |                              4343.00 | 1.00 |                3.69 |
| mariadb-2-1-0-1-1 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.97 |               976803.00 |            125000.00 |                              4307.00 | 1.00 |                3.69 |
| mariadb-2-1-0-1-2 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.97 |               976805.00 |            125000.00 |                              4271.00 | 1.00 |                3.69 |
| mariadb-2-1-0-1-3 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.97 |               976802.00 |            125000.00 |                              4411.00 | 1.00 |                3.69 |
| mariadb-2-1-0-1-4 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.97 |               976814.00 |            125000.00 |                              4155.00 | 1.00 |                3.69 |
| mariadb-2-1-0-1-5 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.97 |               976809.00 |            125000.00 |                              4379.00 | 1.00 |                3.69 |
| mariadb-2-1-0-1-6 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.97 |               976796.00 |            125000.00 |                              4207.00 | 1.00 |                3.69 |
| mariadb-2-1-0-1-7 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.97 |               976808.00 |            125000.00 |                              4199.00 | 1.00 |                3.69 |
| mariadb-2-1-0-1-8 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.97 |               976812.00 |            125000.00 |                              3963.00 | 1.00 |                3.69 |
| mariadb-3-1-0-1-1 |             1.00 |     16.00 |   256.00 |        4.00 |     0.00 |                          255.92 |               976882.00 |            250000.00 |                              4291.00 | 1.00 |                3.69 |
| mariadb-3-1-0-1-2 |             1.00 |     16.00 |   256.00 |        4.00 |     0.00 |                          255.92 |               976868.00 |            250000.00 |                              4375.00 | 1.00 |                3.69 |
| mariadb-3-1-0-1-3 |             1.00 |     16.00 |   256.00 |        4.00 |     0.00 |                          255.92 |               976870.00 |            250000.00 |                              4303.00 | 1.00 |                3.69 |
| mariadb-3-1-0-1-4 |             1.00 |     16.00 |   256.00 |        4.00 |     0.00 |                          255.92 |               976886.00 |            250000.00 |                              4291.00 | 1.00 |                3.69 |
| mariadb-4-1-0-1-1 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.96 |               976850.00 |            125000.00 |                              4355.00 | 1.00 |                3.69 |
| mariadb-4-1-0-1-2 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.96 |               976852.00 |            125000.00 |                              4607.00 | 1.00 |                3.69 |
| mariadb-4-1-0-1-3 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.96 |               976837.00 |            125000.00 |                              4411.00 | 1.00 |                3.69 |
| mariadb-4-1-0-1-4 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.96 |               976860.00 |            125000.00 |                              4647.00 | 1.00 |                3.69 |
| mariadb-4-1-0-1-5 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.96 |               976852.00 |            125000.00 |                              4531.00 | 1.00 |                3.69 |
| mariadb-4-1-0-1-6 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.96 |               976868.00 |            125000.00 |                              4431.00 | 1.00 |                3.69 |
| mariadb-4-1-0-1-7 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.96 |               976851.00 |            125000.00 |                              4435.00 | 1.00 |                3.69 |
| mariadb-4-1-0-1-8 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.96 |               976861.00 |            125000.00 |                              4575.00 | 1.00 |                3.69 |

#### Per Run

| DBMS        |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:------------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MariaDB-1-1 |             1.00 |     32.00 |  1024.00 |        4.00 |     0.00 | 1.00 |                3.69 |                         1023.73 |               976823.00 |           1000000.00 |                              4233.00 |
| MariaDB-2-1 |             1.00 |     32.00 |  1024.00 |        8.00 |     0.00 | 1.00 |                3.69 |                         1023.74 |               976814.00 |           1000000.00 |                              4236.50 |
| MariaDB-3-1 |             1.00 |     64.00 |  1024.00 |        4.00 |     0.00 | 1.00 |                3.69 |                         1023.67 |               976886.00 |           1000000.00 |                              4315.00 |
| MariaDB-4-1 |             1.00 |     64.00 |  1024.00 |        8.00 |     0.00 | 1.00 |                3.69 |                         1023.69 |               976868.00 |           1000000.00 |                              4499.00 |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1023.51 |               977028.00 |             500843 |                            1115.00 |               499157 |                              2403.00 |
| mariadb-2-1-1-1-1 | mariadb-2-1-1 | mariadb-2-1-1-1 |                1 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1023.23 |               977294.00 |             499799 |                            1124.00 |               500201 |                              2371.00 |
| mariadb-3-1-1-1-1 | mariadb-3-1-1 | mariadb-3-1-1-1 |                1 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1023.23 |               977297.00 |             500343 |                            1143.00 |               499657 |                              2393.00 |
| mariadb-4-1-1-1-1 | mariadb-4-1-1 | mariadb-4-1-1-1 |                1 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1023.31 |               977223.00 |             499318 |                            1150.00 |               500682 |                              2459.00 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1023.51 |               977028.00 |             500843 |                            1115.00 |               499157 |                              2403.00 |
| mariadb-2-1-1 | mariadb-2-1-1 |                1 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1023.23 |               977294.00 |             499799 |                            1124.00 |               500201 |                              2371.00 |
| mariadb-3-1-1 | mariadb-3-1-1 |                1 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1023.23 |               977297.00 |             500343 |                            1143.00 |               499657 |                              2393.00 |
| mariadb-4-1-1 | mariadb-4-1-1 |                1 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1023.31 |               977223.00 |             499318 |                            1150.00 |               500682 |                              2459.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
