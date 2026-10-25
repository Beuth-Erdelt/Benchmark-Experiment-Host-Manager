## Show Summary

### Workload
HammerDB Workload SF=4 (warehouses for TPC-C)
* Type: tpcc
* Duration: 951s 
* Code: 1792645244
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 4. Benchmarking runs for 2 minutes. Ramp-up period is 2 minutes before measurements begin. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.7.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Loading is tested with [4] threads, split into [1] pods.
  * Benchmarking is tested with [4] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* mariadb-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:908103
  * datadisk:617
  * volume_size:1.8T
  * volume_used:887G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792645244
* mariadb-1-1-2-1 uses docker image mariadb:12.3.3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:908366
  * datadisk:886
  * volume_size:1.8T
  * volume_used:888G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792645244

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1792645244-756864ccdd-gdxrz: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: hammerdb (2 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: hammerdb (2 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |    4 |       40.00 |           4.00 |            0.00 |         33.00 |            3.00 |              1 |           4 |             | None           |             0 | False         |              360.00 | False               |

### Benchmarking

#### Per Connection

| DBMS              | phase         | job             |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |    TPM |   efficiency |   duration |   errors |
|:------------------|:--------------|:----------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|-------:|-------------:|-----------:|---------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        4 |        1 |               1 |       1 |  62515 | 144688 |         0.00 |          2 |        0 |
| mariadb-1-1-2-1-1 | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        4 |        2 |               1 |       1 | 109294 | 253690 |         0.00 |          2 |        0 |
| mariadb-1-1-2-1-2 | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        4 |        2 |               1 |       2 | 109225 | 253513 |         0.00 |          2 |        0 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   efficiency |      NOPM |       TPM |   duration |   errors |
|:--------------|:--------------|-----------------:|---------:|---------:|----------------:|------------:|-------------:|----------:|----------:|-----------:|---------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        4 |        1 |               1 |           1 |         0.00 |  62515.00 | 144688.00 |          2 |        0 |
| mariadb-1-1-2 | mariadb-1-1-2 |                1 |        8 |        2 |               1 |           2 |         0.00 | 109259.50 | 253601.50 |          2 |        0 |

#### Reset

| phase         | job             |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:--------------|:----------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |         5.00 |                |
| mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |        19.00 |                |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Reset scripts ran without errors
