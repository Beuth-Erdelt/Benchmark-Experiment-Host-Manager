# Example: Benchmark a Cloud Database

This example shows how to benchmark a database service outside of Kubernetes, that is compatible with PostgreSQL, with YCSB, Benchbase's TPC-C and TPC-H (configuration key `DatabaseService`).

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

The following example treats **a cloud database that is compatible to PostgreSQL**.

This differs from the default behaviour of bexhoma, since we benchmark **a distributed DBMS, that is not managed by bexhoma and does not exist in the Kubernetes cluster in the same namespace**.

Important implications of this:
* Bexhoma does neither start nor stop the DBMS.
* There can only be one DBMS in the cluster at the same time.
* Bexhoma does not know what resides inside of the database.
* Bexhoma still can only monitor the components of the experiment other than the SUT.

In order to be fully functional, bexhoma installs an instance of PostgreSQL, that does nothing (a container with psql would be enough).
Bexhoma writes infos about the status of the experiment to this "SUT" pod to mimick it has access to the DBMS.
Moreover the container is used to install a schema to the database via psql.

All metrics in monitoring are summed across all matching components.

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. [YCSB Repository](https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload)
1. [Benchmarking cloud serving systems with YCSB](https://dl.acm.org/doi/10.1145/1807128.1807152)
1. [Benchbase Repository](https://github.com/cmu-db/benchbase/wiki/TPC-C)
1. [OLTP-Bench: An Extensible Testbed for Benchmarking Relational Databases](http://www.vldb.org/pvldb/vol7/p277-difallah.pdf)
1. [Orchestrating DBMS Benchmarking in the Cloud with Kubernetes](https://doi.org/10.1007/978-3-030-94437-7_6)
1. [A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools](https://doi.org/10.1007/978-3-031-68031-1_9)
1. Test script of this page: [test-docs-databaseservice.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-databaseservice.sh), [test-docs-databaseservice.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-databaseservice.ps1)


## Perform YCSB Benchmark

### Prerequisites: Placeholder of a Cloud Service

In order to have a test environment, we install a placeholder instance PostgreSQL and treat it like an external service.

Create the test placeholder
```bash
# start database service
kubectl create -f k8s/deploymenttemplate-PostgreSQLService.yml
```

This starts a deployment `bexhoma-deployment-postgres` with a service `bexhoma-service`.

We can delete these after the experiment has finished by
```bash
# delete database service
kubectl delete deployment bexhoma-deployment-postgres
kubectl delete svc bexhoma-service
```

All demonstration and test runs in the following are run against this placeholder.

### Run the Benchmark

You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"
BEXHOMA_MS=2
BEXHOMA_STORAGE_CLASS="shared"

mkdir -p $LOG_DIR
```

For performing the experiment we can run the [ycsb file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/ycsb.py).

Example: 
```bash
bexhoma ycsb \
  -dbms DatabaseService \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xop 1 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_databaseservice.log
```

This
* loops over `n` in [8] and `t` in [4]
  * starts a clean instance of a dummy container as a placeholder for the DatabaseService (`-dbms`)
    * data directory inside a Docker container
  * creates YCSB schema in each database
  * starts `n` loader pods per DBMS
    * with a loading container each
      * threads = 64/`n` (`-nlt`)
      * target throughput is `t` * 16384
      * generates YCSB data = 1.000.000 rows (i.e., SF=10, `-sf`)
      * imports it into the DBMS
  * loops over `m` in [1] and `s` in [4]
    * runs `m` parallel streams of YCSB queries per DBMS
      * 10.000.000 operations (`-xop`)
      * workload A = 50% read / 50% write (`--workload`)
      * target throughput is `s` * 16384
      * threads = 64/`m` (`-nbt`)
    * with a maximum of 1 DBMS per time (`-ms`) (plus 1 for the placeholder)
* tests if results match workflow (`-tr`)
* shows a summary

### Status

You can watch the status while benchmark is running via `bexhoma status`

```bash
Dashboard: Running
Cluster Prometheus: Running
Message Queue: Running
Data directory: Running
Result directory: Running
+----------------------------+--------------+--------------+------------+---------------+
| 1730133803                 | sut          |   loaded [s] | use case   | benchmarker   |
+============================+==============+==============+============+===============+
| DatabaseService-64-8-65536 | (1. Running) |           41 | ycsb       | (1. Running)  |
+----------------------------+--------------+--------------+------------+---------------+
```

The code `1730133803` is the unique identifier of the experiment.
You can find the number also in the output of `ycsb.py`.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1730133803` (removes everything that is related to experiment `1730133803`).

### Evaluate Results

At the end of a benchmark you will see a summary like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_databaseservice_summary.md" target="_blank" rel="noopener">docs_ycsb_databaseservice.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 380s 
* Code: 1793617549
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [4].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * Experiment is limited to DBMS ['DatabaseService'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 2.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* databaseservice-1-1-1-1 uses docker image postgres:16.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:741412
  * datadisk:39
  * volume_size:1.8T
  * volume_used:725G
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 1.0 CPU, 1.0 GiB RAM requested in 1 pods
    * sut: 1 x, 1.0 CPU, 1.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793617549

### Init Scripts Not in Folder
* DatabaseService-1: skipped checkschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-databaseservice-1-1793617549-7dfc479b6b-x5pbq: 0

### Workflow

#### Actual

* DBMS DatabaseService-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS DatabaseService-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection                |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:--------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| databaseservice-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         6936.74 |                18020.00 |            125000.00 |                              4695.00 | 1.00 |              199.78 |
| databaseservice-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7003.59 |                17848.00 |            125000.00 |                              4895.00 | 1.00 |              201.70 |
| databaseservice-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         6949.46 |                17987.00 |            125000.00 |                              4935.00 | 1.00 |              200.14 |
| databaseservice-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         6959.14 |                17962.00 |            125000.00 |                              4943.00 | 1.00 |              200.42 |
| databaseservice-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         6951.01 |                17983.00 |            125000.00 |                              4799.00 | 1.00 |              200.19 |
| databaseservice-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         6950.24 |                17985.00 |            125000.00 |                              4951.00 | 1.00 |              200.17 |
| databaseservice-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         6848.94 |                18251.00 |            125000.00 |                              4807.00 | 1.00 |              197.25 |
| databaseservice-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         6753.11 |                18510.00 |            125000.00 |                              4811.00 | 1.00 |              194.49 |

#### Per Run

| DBMS                |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| DatabaseService-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 1.00 |              194.49 |                        55352.21 |                18510.00 |           1000000.00 |                              4854.50 |

### Benchmarking

#### Per Connection

| DBMS                      | phase                 | job                     | configuration     |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------------|:----------------------|:------------------------|:------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| databaseservice-1-1-1-1-1 | databaseservice-1-1-1 | databaseservice-1-1-1-1 | DatabaseService-1 |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                        63922.27 |                15644.00 |             499360 |                             436.00 |               500640 |                              1663.00 |

#### Per Phase

| DBMS                  | phase                 |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------------|:----------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| databaseservice-1-1-1 | databaseservice-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                        63922.27 |                15644.00 |             499360 |                             436.00 |               500640 |                              1663.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>

To see the summary again you can simply call `bexhoma summary -e 1730133803` with the experiment code.

Results are transformed into pandas DataFrames and can be inspected in detail.
See for example
* [Jupyter Notebooks](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/notebooks/)

You can connect to an evaluation server locally by `bexhoma jupyter`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888


## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).

The `-mc` option is mandatory here: The sidecar container approach is not working (since bexhoma does not manage the deployment), so either you have Prometheus / Node exporter already installed in your cluster or a daemonset is needed.
Moreover the SUT itself cannot be monitored, since it is outside of the cluster.
For further explanation see the monitoring section of this documentation.

The following run skips loading (`-sl`), as the data of the run above is still present in the database, and monitors the components (`-m -mc`):

```bash
bexhoma ycsb \
  -dbms DatabaseService \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xop 10 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -sl \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_databaseservice_monitoring.log
```

This skips loading (`-sl`), as data is already present in the database.

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_databaseservice_monitoring_summary.md" target="_blank" rel="noopener">docs_ycsb_databaseservice_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 428s 
* Code: 1793617939
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [4].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['DatabaseService'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Loading is skipped.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 2.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* databaseservice-1-1-1-1 uses docker image postgres:16.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:741415
  * datadisk:39
  * volume_size:1.8T
  * volume_used:725G
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 1.0 CPU, 1.0 GiB RAM requested in 1 pods
    * sut: 1 x, 1.0 CPU, 1.0 GiB RAM
  * eval_parameters
    * code:1793617939

### SUT Container Restarts
* bexhoma-sut-databaseservice-1-1793617939-74b4987f44-gh52g: 0

### Workflow

#### Actual

* DBMS DatabaseService-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS DatabaseService-1 - Experiment 1 Client 1: ycsb (1 pods)

### Benchmarking

#### Per Connection

| DBMS                      | phase                 | job                     | configuration     |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------------|:----------------------|:------------------------|:------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| databaseservice-1-1-1-1-1 | databaseservice-1-1-1 | databaseservice-1-1-1-1 | DatabaseService-1 |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                        65383.41 |               152944.00 |            5004929 |                             425.00 |              4995071 |                               829.00 |

#### Per Phase

| DBMS                  | phase                 |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------------|:----------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| databaseservice-1-1-1 | databaseservice-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                        65383.41 |               152944.00 |            5004929 |                             425.00 |              4995071 |                               829.00 |

### Monitoring

### Benchmarking phase: component benchmarker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| databaseservice-1-1-1-1 |       609.04 |      4.86 |           1.05 |                  1.05 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>


## Persistent Storage

Persistent Storage is not managed by bexhoma, but by the Cloud service.
We can add the request for a PVC to the experiment setup:

```bash
bexhoma ycsb \
  -dbms DatabaseService \
  -sf 5 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xop 10 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_databaseservice_storage.log
```

This will add a PVC to the Dummy DBMS.
Nothing will be stored there, but it maintains status information about previous loading processes.

```bash
+----------------------------------------+-----------------+--------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+
| Volumes                                | configuration   | experiment   | loaded [s]   |   timeLoading [s] | dbms            | storage_class_name   | storage   | status   | size   | used   |
+========================================+=================+==============+==============+===================+=================+======================+===========+==========+========+========+
| bexhoma-storage-databaseservice-ycsb-5 | databaseservice | ycsb-5       | True         |                98 | DatabaseService | shared               | 50Gi      | Bound    | 50G    | 36M    |
+----------------------------------------+-----------------+--------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+
```

The above means there has been a YCSB loading process (managed by bexhoma) of size SF=5, that has been completed.
All following calls of such an experiment will skip loading, since the PVC tells it has been finished.
This thus helps to spare the `-sl` parameter.

However bexhoma cannot verify such information.
If data is delete somehow, this PVC information will be outdated and wrong.

This approach helps bexhoma to persist status information, but it does not persist data inside the Cloud database.

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_databaseservice_storage_summary.md" target="_blank" rel="noopener">docs_ycsb_databaseservice_storage.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=5
* Type: ycsb
* Duration: 586s 
* Code: 1793618720
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 5000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [4].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['DatabaseService'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 2.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* databaseservice-1-1-1-1 uses docker image postgres:16.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:741386
  * datadisk:39
  * volume_size:49G
  * volume_used:39M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 1.0 CPU, 1.0 GiB RAM requested in 1 pods
    * sut: 1 x, 1.0 CPU, 1.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793618720

### Init Scripts Not in Folder
* DatabaseService-1: skipped checkschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-databaseservice-1-1793618720-567bd59768-4cxvw: 0

### Workflow

#### Actual

* DBMS DatabaseService-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS DatabaseService-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection                |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:--------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| databaseservice-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7177.97 |                87072.00 |            625000.00 |                              5175.00 | 5.00 |              206.73 |
| databaseservice-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7117.88 |                87807.00 |            625000.00 |                              5075.00 | 5.00 |              205.00 |
| databaseservice-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7184.49 |                86993.00 |            625000.00 |                              5099.00 | 5.00 |              206.91 |
| databaseservice-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7100.74 |                88019.00 |            625000.00 |                              5139.00 | 5.00 |              204.50 |
| databaseservice-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7134.05 |                87608.00 |            625000.00 |                              5107.00 | 5.00 |              205.46 |
| databaseservice-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7079.83 |                88279.00 |            625000.00 |                              5231.00 | 5.00 |              203.90 |
| databaseservice-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7102.68 |                87995.00 |            625000.00 |                              5135.00 | 5.00 |              204.56 |
| databaseservice-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7092.60 |                88120.00 |            625000.00 |                              5167.00 | 5.00 |              204.27 |

#### Per Run

| DBMS                |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| DatabaseService-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 5.00 |              203.90 |                        56990.23 |                88279.00 |           5000000.00 |                              5141.00 |

### Benchmarking

#### Per Connection

| DBMS                      | phase                 | job                     | configuration     |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------------|:----------------------|:------------------------|:------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| databaseservice-1-1-1-1-1 | databaseservice-1-1-1 | databaseservice-1-1-1-1 | DatabaseService-1 |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                        65377.42 |               152958.00 |            5001895 |                             441.00 |              4998105 |                              1570.00 |

#### Per Phase

| DBMS                  | phase                 |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------------|:----------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| databaseservice-1-1-1 | databaseservice-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                        65377.42 |               152958.00 |            5001895 |                             441.00 |              4998105 |                              1570.00 |

### Monitoring

### Loading phase: component loader

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| databaseservice-1-1-1-1 |       370.16 |      6.16 |           0.29 |                  0.29 |

### Benchmarking phase: component benchmarker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| databaseservice-1-1-1-1 |       526.87 |      4.82 |           1.05 |                  1.06 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-loader.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>


## Technical Details

### Types of DBMS

#### Managed by Bexhoma

We included [CockroachDB](Example-CockroachDB.md) as an example for a distributed DBMS, that is managed by bexhoma.

Advantages
* Bexhoma can monitor all components
* Bexhoma knows about loaded databases, their status and timings

Disadvantages
* This is only implemented for some examples
* This cannot be applied to Cloud services (or any other database outside of the Kubernetes cluster)

#### Not Managed by Bexhoma

We included [YugaByteDB](Example-YugaByteDB.md) as an example for a distributed DBMS, that is not managed by bexhoma, but runs in the same Kubernetes cluster.

Advantages
* Can be applied to all systems running in Kubernetes
* Bexhoma can monitor all components

Disadvantages
* Bexhoma not necessarily knows about loaded databases, their status and timings - they might be affected by outside services
* This cannot be applied to Cloud services (or any other database outside of the Kubernetes cluster)

#### Outside of Kubernetes

Here we present an example for a DBMS, that is not managed by bexhoma and might be running outside of the Kubernetes cluster.

Advantages
* This can be applied to all Cloud services (or any other database outside of the Kubernetes cluster) with a JDBC interface

Disadvantages
* The SUT cannot be monitored by Bexhoma
* Bexhoma not necessarily knows about loaded databases, their status and timings - they might be affected by outside services

### Configuration of Bexhoma

`DatabaseService` is a generic configuration for external database services — cloud-managed databases or any PostgreSQL-compatible endpoint that is not deployed by bexhoma.
In `cluster.config` there is a section:

```python
'DatabaseService': {
    'loadData': 'psql -U postgres --host bexhoma-service.{namespace}.svc.cluster.local --port 9091 < {scriptname}',
    'template': {
        'version': 'v11.4',
        'alias': 'General-B',
        'docker_alias': 'GP-B',
        'JDBC': {
            'driver': "org.postgresql.Driver",
            'auth': ["postgres", ""],
            'url': 'jdbc:postgresql://bexhoma-service.{namespace}.svc.cluster.local:9091/postgres?reWriteBatchedInserts=true',
            'jar': 'postgresql-42.5.0.jar',
            'database': 'postgres',
            'explain': ['EXPLAIN (VERBOSE, FORMAT JSON) {query}'],
        }
    },
    'logfile': '/usr/local/data/logfile',
    'datadir': '/var/lib/postgresql/data/',
    'priceperhourdollar': 0.0,
},
```

where
* `loadData`: command to create the schema, here against the placeholder service `bexhoma-service`
* `JDBC`: used to configure YCSB and DBMSBenchmarker

Please make sure to adjust host, port and credentials to the cloud service you want to benchmark.

### Preparation of YCSB

In the Docker files for YCSB
* https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/ycsb/generator/Dockerfile
* https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/ycsb/benchmarker/Dockerfile

there is a section about including the needed JDBC driver:
```bash
######### Specific version of PostgreSQL JDBC #########
RUN wget https://jdbc.postgresql.org/download/postgresql-42.5.0.jar --no-check-certificate
RUN cp postgresql-42.5.0.jar jars/postgresql-42.5.0.jar
```


### Placeholder SUT

Bexhoma deploys a pod to carry status informations.
Here it is an instance of PostgreSQL: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-DatabaseService.yml


### Schema SQL File

If data should be loaded, bexhoma at first creates a schema according to: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/DatabaseService


### Workflow of YCSB

In `ycsb.py` there is a section about DatabaseService.

Watch for
* `config.monitoring_sut = False`: SUT cannot be monitored since it is outside of K8s

### Load Durability

`-xld` has no effect: there are no durability scripts for DatabaseService.

### Reset Scripts

DatabaseService has no reset scripts; with `-ar` the experiment prints a warning at the start.


## Benchbase's TPC-C

```bash
bexhoma benchbase \
  -dbms DatabaseService \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 16 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_databaseservice.log
```

yields

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_databaseservice_summary.md" target="_blank" rel="noopener">docs_benchbase_databaseservice.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 937s 
* Code: 1793619380
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * Experiment is limited to DBMS ['DatabaseService'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 2.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* databaseservice-1-1-1-1 uses docker image postgres:16.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:741429
  * datadisk:39
  * volume_size:1.8T
  * volume_used:725G
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 1.0 CPU, 1.0 GiB RAM requested in 1 pods
    * sut: 1 x, 1.0 CPU, 1.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793619380
* databaseservice-1-1-2-1 uses docker image postgres:16.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:741441
  * datadisk:39
  * volume_size:1.8T
  * volume_used:725G
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 1.0 CPU, 1.0 GiB RAM requested in 1 pods
    * sut: 1 x, 1.0 CPU, 1.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793619380

### Init Scripts Not in Folder
* DatabaseService-1: skipped checkschema-benchbase.sql, initschema-benchbase.sql

### SUT Container Restarts
* bexhoma-sut-databaseservice-1-1793619380-965bfc4cb-fnhhc: 0

### Workflow

#### Actual

* DBMS DatabaseService-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS DatabaseService-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS DatabaseService-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS DatabaseService-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

|                     |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:--------------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| DatabaseService-1-1 |                1 |   16 |        3.00 |           1.00 |            0.00 |          1.00 |            1.00 |              1 |           1 |             | None           |             0 | False         |            19200.00 | False               |

### Benchmarking

#### Per Connection

| DBMS                      | phase                 | job                     |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:--------------------------|:----------------------|:------------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| databaseservice-1-1-1-1-1 | databaseservice-1-1-1 | databaseservice-1-1-1-1 |                1 |          16 |    16384 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                        7382.44 |                        0.00 |         0.00 |                                                       5255.00 |                                               2164.00 |
| databaseservice-1-1-2-1-1 | databaseservice-1-1-2 | databaseservice-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       1 |          -1 | 300.00 |            0 |                        8189.23 |                        0.00 |         0.00 |                                                       1886.00 |                                                779.00 |
| databaseservice-1-1-2-1-2 | databaseservice-1-1-2 | databaseservice-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       2 |          -1 | 300.00 |            0 |                        8062.64 |                        0.00 |         0.00 |                                                       2162.00 |                                                901.00 |

#### Per Phase

| DBMS                  | phase                 |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:----------------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| databaseservice-1-1-1 | databaseservice-1-1-1 |                1 |          16 |    16384 |               1 |           1 |          -1 | 300.00 |            0 |                        7382.44 |                        0.00 |         0.00 |                                                       5255.00 |                                               2164.00 |
| databaseservice-1-1-2 | databaseservice-1-1-2 |                1 |          16 |    16384 |               1 |           2 |          -1 | 300.00 |            0 |                       16251.87 |                        0.00 |         0.00 |                                                       2162.00 |                                                840.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
```

</details>

### Benchbase Example Explained

The setup is the same as for YCSB (see above).

However the connection string this time is not only read from `cluster.config`, but are also constructed from parameters that are set explicitly in the workflow file `benchbase.py`:

```bash
BENCHBASE_PROFILE = 'postgres',
BEXHOMA_DATABASE = 'postgres',
```

### Only Execution

This time we skip loading (`-sl`), since the database is already present.

```bash
bexhoma benchbase \
  -dbms DatabaseService \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 16 \
  -ms $BEXHOMA_MS \
  -sl \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_databaseservice_execution.log
```

yields

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_databaseservice_execution_summary.md" target="_blank" rel="noopener">docs_benchbase_databaseservice_execution.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 910s 
* Code: 1793620326
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * Experiment is limited to DBMS ['DatabaseService'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Loading is skipped.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 2.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* databaseservice-1-1-1-1 uses docker image postgres:16.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:741449
  * datadisk:39
  * volume_size:1.8T
  * volume_used:725G
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 1.0 CPU, 1.0 GiB RAM requested in 1 pods
    * sut: 1 x, 1.0 CPU, 1.0 GiB RAM
  * eval_parameters
    * code:1793620326
* databaseservice-1-1-2-1 uses docker image postgres:16.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:741453
  * datadisk:39
  * volume_size:1.8T
  * volume_used:725G
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 1.0 CPU, 1.0 GiB RAM requested in 1 pods
    * sut: 1 x, 1.0 CPU, 1.0 GiB RAM
  * eval_parameters
    * code:1793620326

### SUT Container Restarts
* bexhoma-sut-databaseservice-1-1793620326-746b5686dd-r8fjj: 0
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\benchbase.py", line 942, in <module>
    experiment.process()
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\experiments\base.py", line 384, in process
    self.show_summary(write_report=getattr(self.args, 'write_report', False))
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\experiments\mixed.py", line 156, in show_summary
    benchmark.show_summary(self, write_report=write_report)
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\benchmarks\base.py", line 502, in show_summary
    loading_section, df_loading = self._show_loading_sections(experiment, is_multitenant)
                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\benchmarks\base.py", line 279, in _show_loading_sections
    df = self.evaluator.get_summary_loading_per_run()
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\evaluators\benchbase.py", line 559, in get_summary_loading_per_run
    df = self.get_loading_per_run()
         ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\evaluators\base.py", line 815, in get_loading_per_run
    df = self.get_loading_per_connection()
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\evaluators\base.py", line 791, in get_loading_per_connection
    df_tpx = (df['SF'] * 3600.0)/df_load.sort_index()
             ~~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~~
  File "C:\Users\Patrick\anaconda3\envs\bexhoma\Lib\site-packages\pandas\core\ops\common.py", line 76, in new_method
    return method(self, other)
           ^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\anaconda3\envs\bexhoma\Lib\site-packages\pandas\core\arraylike.py", line 210, in __truediv__
    return self._arith_method(other, operator.truediv)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\anaconda3\envs\bexhoma\Lib\site-packages\pandas\core\series.py", line 6154, in _arith_method
    return base.IndexOpsMixin._arith_method(self, other, op)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\anaconda3\envs\bexhoma\Lib\site-packages\pandas\core\base.py", line 1391, in _arith_method
    result = ops.arithmetic_op(lvalues, rvalues, op)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\anaconda3\envs\bexhoma\Lib\site-packages\pandas\core\ops\array_ops.py", line 283, in arithmetic_op
    res_values = _na_arithmetic_op(left, right, op)  # type: ignore[arg-type]
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\anaconda3\envs\bexhoma\Lib\site-packages\pandas\core\ops\array_ops.py", line 218, in _na_arithmetic_op
    result = func(left, right)
             ^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\anaconda3\envs\bexhoma\Lib\site-packages\pandas\core\computation\expressions.py", line 242, in evaluate
    return _evaluate(op, op_str, a, b)  # type: ignore[misc]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\anaconda3\envs\bexhoma\Lib\site-packages\pandas\core\computation\expressions.py", line 73, in _evaluate_standard
    return op(a, b)
           ^^^^^^^^
ZeroDivisionError: float division by zero
```

</details>




## TPC-H

In the following we run TPC-H against the Cloud Database Service.


### Simple Run

At first we run a simple power test against SF=3.
Components are monitored.

```bash
bexhoma tpch \
  -dbms DatabaseService \
  -sf 3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_databaseservice.log
```

yields

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_databaseservice_summary.md" target="_blank" rel="noopener">docs_tpch_databaseservice.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 657s 
* Code: 1793862917
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['DatabaseService'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* databaseservice-1-1-1-1-1 uses docker image postgres:16.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:777077
  * datadisk:39
  * volume_size:1.8T
  * volume_used:759G
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 1.0 CPU, 1.0 GiB RAM requested in 1 pods
    * sut: 1 x, 1.0 CPU, 1.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793862917

### Init Scripts Not in Folder
* DatabaseService-1: skipped checkschema-tpch.sql

### SUT Container Restarts
* bexhoma-sut-databaseservice-1-1793862917-578f4c4598-bbrfl: 0

### Workflow

#### Actual

* DBMS DatabaseService-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS DatabaseService-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                     |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:--------------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| DatabaseService-1-1 |                1 |    3 |      262.00 |           2.00 |           15.00 |        100.00 |          137.00 |              8 |           0 |             | None           |             0 | False         |               41.22 | False               |

### Benchmarking

#### Per Connection

| DBMS                      | configuration     | phase                 | job                     |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                       |
|:--------------------------|:------------------|:----------------------|:------------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:--------------------------|
| databaseservice-1-1-1-1-1 | DatabaseService-1 | databaseservice-1-1-1 | databaseservice-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  22 |         51 |            1.50 |             7446.73 |           4658.82 |          -1 | databaseservice-1-1-1-1-1 |

#### Per Phase

|                       | phase                 |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------------|:----------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| databaseservice-1-1-1 | databaseservice-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  22 |         51 |            1.50 |             7446.73 |           4658.82 |          -1 |

#### Query Completion per Phase

| phase                 |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:----------------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| databaseservice-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   databaseservice-1-1-1-1-1 |
|:----------------------------------------------------|----------------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                     3493.13 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                     1057.29 |
| Shipping Priority (TPC-H Q3)                        |                     1649.79 |
| Order Priority Checking Query (TPC-H Q4)            |                     2236.57 |
| Local Supplier Volume (TPC-H Q5)                    |                     1515.99 |
| Forecasting Revenue Change (TPC-H Q6)               |                      821.37 |
| Volume Shipping Query (TPC-H Q7)                    |                     1453.37 |
| National Market Share (TPC-H Q8)                    |                      998.75 |
| Product Type Profit Measure (TPC-H Q9)              |                     2344.28 |
| Returned Item Reporting Query (TPC-H Q10)           |                     1848.46 |
| Important Stock Identification (TPC-H Q11)          |                      366.59 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                     1634.69 |
| Customer Distribution (TPC-H Q13)                   |                     4296.38 |
| Promotion Effect Query (TPC-H Q14)                  |                      891.22 |
| Top Supplier Query (TPC-H Q15)                      |                      943.40 |
| Parts/Supplier Relationship (TPC-H Q16)             |                      761.56 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                     3941.77 |
| Large Volume Customer (TPC-H Q18)                   |                    11370.54 |
| Discounted Revenue (TPC-H Q19)                      |                     1257.21 |
| Potential Part Promotion (TPC-H Q20)                |                      698.23 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                     1706.32 |
| Global Sales Opportunity Query (TPC-H Q22)          |                      301.80 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: component data generator

| DBMS                    | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|:-------------|----------:|---------------:|----------------------:|
| databaseservice-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| databaseservice-1-1-1-1 |        45.06 |      0.94 |           0.00 |                  0.38 |

### Benchmarking phase: component benchmarker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| databaseservice-1-1-1-1 |        12.92 |      0.54 |           0.26 |                  0.26 |

### Missing Monitoring Metrics
* Memory Usage, Working Set [MiB] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-loader.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (data pre-existing; series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
```

</details>

### Execution Only

Now loading is skipped (`-sl`) as data is already present in the Cloud system.

```bash
bexhoma tpch \
  -dbms DatabaseService \
  -sf 3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -sl \
  -t 1200 \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_databaseservice_execution.log
```

yields

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_databaseservice_execution_summary.md" target="_blank" rel="noopener">docs_tpch_databaseservice_execution.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 301s 
* Code: 1793863632
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['DatabaseService'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Loading is skipped.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* databaseservice-1-1-1-1-1 uses docker image postgres:16.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:777081
  * datadisk:39
  * volume_size:1.8T
  * volume_used:759G
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 1.0 CPU, 1.0 GiB RAM requested in 1 pods
    * sut: 1 x, 1.0 CPU, 1.0 GiB RAM
  * eval_parameters
    * code:1793863632

### SUT Container Restarts
* bexhoma-sut-databaseservice-1-1793863632-8b9c74856-zk7ft: 0

### Workflow

#### Actual

* DBMS DatabaseService-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS DatabaseService-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                     |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:--------------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| DatabaseService-1-1 |                1 |    3 |        0.00 |           0.00 |            0.00 |          0.00 |            0.00 |              0 |           0 |             | None           |             0 | False         |                 nan | False               |

### Benchmarking

#### Per Connection

| DBMS                      | configuration     | phase                 | job                     |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                       |
|:--------------------------|:------------------|:----------------------|:------------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:--------------------------|
| databaseservice-1-1-1-1-1 | DatabaseService-1 | databaseservice-1-1-1 | databaseservice-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  22 |         50 |            1.49 |             7468.29 |           4752.00 |          -1 | databaseservice-1-1-1-1-1 |

#### Per Phase

|                       | phase                 |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------------|:----------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| databaseservice-1-1-1 | databaseservice-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  22 |         50 |            1.49 |             7468.29 |           4752.00 |          -1 |

#### Query Completion per Phase

| phase                 |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:----------------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| databaseservice-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   databaseservice-1-1-1-1-1 |
|:----------------------------------------------------|----------------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                     3472.78 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                     1064.00 |
| Shipping Priority (TPC-H Q3)                        |                     1626.15 |
| Order Priority Checking Query (TPC-H Q4)            |                     2197.31 |
| Local Supplier Volume (TPC-H Q5)                    |                     1529.18 |
| Forecasting Revenue Change (TPC-H Q6)               |                      843.57 |
| Volume Shipping Query (TPC-H Q7)                    |                     1457.15 |
| National Market Share (TPC-H Q8)                    |                     1015.46 |
| Product Type Profit Measure (TPC-H Q9)              |                     2314.50 |
| Returned Item Reporting Query (TPC-H Q10)           |                     1831.77 |
| Important Stock Identification (TPC-H Q11)          |                      360.59 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                     1655.30 |
| Customer Distribution (TPC-H Q13)                   |                     4105.53 |
| Promotion Effect Query (TPC-H Q14)                  |                      885.73 |
| Top Supplier Query (TPC-H Q15)                      |                      941.04 |
| Parts/Supplier Relationship (TPC-H Q16)             |                      864.05 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                     3817.14 |
| Large Volume Customer (TPC-H Q18)                   |                    10865.46 |
| Discounted Revenue (TPC-H Q19)                      |                     1233.65 |
| Potential Part Promotion (TPC-H Q20)                |                      684.33 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                     1692.12 |
| Global Sales Opportunity Query (TPC-H Q22)          |                      299.46 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Benchmarking phase: component benchmarker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| databaseservice-1-1-1-1 |        12.53 |      0.50 |           0.27 |                  0.28 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: No monitoring metrics missing
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
```

</details>


### Persistent Storage

We now use a PVC to store infos about the loading process.
At first, we remove the placeholder and recreate it again.
An existing PVC of the placeholder is removed before loading (`-rsr`).
```bash
# delete database service placeholder
kubectl delete deployment bexhoma-deployment-postgres
kubectl delete svc bexhoma-service

sleep 30

# start database service placeholder
kubectl create -f k8s/deploymenttemplate-PostgreSQLService.yml

sleep 10
```

### Ingestion with Persistent Storage

```bash
bexhoma tpch \
  -dbms DatabaseService \
  -sf 3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_databaseservice_storage.log
```

yields

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_databaseservice_storage_summary.md" target="_blank" rel="noopener">docs_tpch_databaseservice_storage.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 565s 
* Code: 1793822962
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['DatabaseService'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* databaseservice-1-1-1-1-1 uses docker image postgres:16.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:850944
  * datadisk:39
  * volume_size:49G
  * volume_used:39M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 1.0 CPU, 1.0 GiB RAM requested in 1 pods
    * sut: 1 x, 1.0 CPU, 1.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793822962

### Init Scripts Not in Folder
* DatabaseService-1: skipped checkschema-tpch.sql

### SUT Container Restarts
* bexhoma-sut-databaseservice-1-1793822962-799cb5f644-qphft: 0

### Workflow

#### Actual

* DBMS DatabaseService-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS DatabaseService-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                     |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:--------------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| DatabaseService-1-1 |                1 |    3 |      120.00 |           1.00 |           24.00 |         20.00 |           71.00 |              8 |           0 |             | None           |             0 | False         |               90.00 | False               |

### Benchmarking

#### Per Connection

| DBMS                      | configuration     | phase                 | job                     |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                       |
|:--------------------------|:------------------|:----------------------|:------------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:--------------------------|
| databaseservice-1-1-1-1-1 | DatabaseService-1 | databaseservice-1-1-1 | databaseservice-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  22 |         37 |            1.01 |            11112.81 |           6421.62 |          -1 | databaseservice-1-1-1-1-1 |

#### Per Phase

|                       | phase                 |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------------|:----------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| databaseservice-1-1-1 | databaseservice-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  22 |         37 |            1.01 |            11112.81 |           6421.62 |          -1 |

#### Query Completion per Phase

| phase                 |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:----------------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| databaseservice-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   databaseservice-1-1-1-1-1 |
|:----------------------------------------------------|----------------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                     2855.81 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                      870.18 |
| Shipping Priority (TPC-H Q3)                        |                     1203.62 |
| Order Priority Checking Query (TPC-H Q4)            |                     1463.89 |
| Local Supplier Volume (TPC-H Q5)                    |                     1019.33 |
| Forecasting Revenue Change (TPC-H Q6)               |                      476.52 |
| Volume Shipping Query (TPC-H Q7)                    |                     1169.37 |
| National Market Share (TPC-H Q8)                    |                      585.58 |
| Product Type Profit Measure (TPC-H Q9)              |                     1365.09 |
| Returned Item Reporting Query (TPC-H Q10)           |                     1200.16 |
| Important Stock Identification (TPC-H Q11)          |                      280.45 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                     1031.31 |
| Customer Distribution (TPC-H Q13)                   |                     2214.30 |
| Promotion Effect Query (TPC-H Q14)                  |                      630.25 |
| Top Supplier Query (TPC-H Q15)                      |                      574.81 |
| Parts/Supplier Relationship (TPC-H Q16)             |                      745.19 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                     1692.54 |
| Large Volume Customer (TPC-H Q18)                   |                     8138.31 |
| Discounted Revenue (TPC-H Q19)                      |                      899.67 |
| Potential Part Promotion (TPC-H Q20)                |                      452.99 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                     1092.49 |
| Global Sales Opportunity Query (TPC-H Q22)          |                      210.90 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: component data generator

| DBMS                    | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|:-------------|----------:|---------------:|----------------------:|
| databaseservice-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS                    | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|:-------------|----------:|---------------:|----------------------:|
| databaseservice-1-1-1-1 | n/a          |         0 |           0.00 |                  0.13 |

### Benchmarking phase: component benchmarker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| databaseservice-1-1-1-1 |        16.02 |      0.53 |           0.32 |                  0.33 |

### Missing Monitoring Metrics
* Memory Usage, Working Set [MiB] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-loader.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (data pre-existing; job pods ran shorter than scrape interval; series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
```

</details>

### Execution Only with Persistent Storage

Data is now present in the database.
The persistent volume helps to memorize this.
We can rerun the experiment without explicitly skipping ingestion (no `-sl`).

```bash
bexhoma tpch \
  -dbms DatabaseService \
  -sf 3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_databaseservice_storage_execution.log
```

yields

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_databaseservice_storage_execution_summary.md" target="_blank" rel="noopener">docs_tpch_databaseservice_storage_execution.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 303s 
* Code: 1793823612
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['DatabaseService'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* databaseservice-1-1-1-1-1 uses docker image postgres:16.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:850928
  * datadisk:39
  * volume_size:49G
  * volume_used:39M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 1.0 CPU, 1.0 GiB RAM requested in 1 pods
    * sut: 1 x, 1.0 CPU, 1.0 GiB RAM
  * eval_parameters
    * code:1793823612

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: DatabaseService-1

### Data Parameters of Reused Volumes
* DatabaseService-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-databaseservice-1-1793823612-c58bd6668-b9946: 0

### Workflow

#### Actual

* DBMS DatabaseService-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS DatabaseService-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                     |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:--------------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| DatabaseService-1-1 |                1 |    3 |      120.00 |           1.00 |           24.00 |         20.00 |           71.00 |              0 |           0 |             | None           |             0 | False         |               90.00 | True                |

### Benchmarking

#### Per Connection

| DBMS                      | configuration     | phase                 | job                     |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                       |
|:--------------------------|:------------------|:----------------------|:------------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:--------------------------|
| databaseservice-1-1-1-1-1 | DatabaseService-1 | databaseservice-1-1-1 | databaseservice-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  22 |         39 |            0.99 |            11369.80 |           6092.31 |          -1 | databaseservice-1-1-1-1-1 |

#### Per Phase

|                       | phase                 |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------------|:----------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| databaseservice-1-1-1 | databaseservice-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  22 |         39 |            0.99 |            11369.80 |           6092.31 |          -1 |

#### Query Completion per Phase

| phase                 |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:----------------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| databaseservice-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   databaseservice-1-1-1-1-1 |
|:----------------------------------------------------|----------------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                     2883.42 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                      841.24 |
| Shipping Priority (TPC-H Q3)                        |                     1119.86 |
| Order Priority Checking Query (TPC-H Q4)            |                     1277.09 |
| Local Supplier Volume (TPC-H Q5)                    |                      872.84 |
| Forecasting Revenue Change (TPC-H Q6)               |                      484.43 |
| Volume Shipping Query (TPC-H Q7)                    |                     1073.97 |
| National Market Share (TPC-H Q8)                    |                      565.58 |
| Product Type Profit Measure (TPC-H Q9)              |                     1462.15 |
| Returned Item Reporting Query (TPC-H Q10)           |                     1226.52 |
| Important Stock Identification (TPC-H Q11)          |                      274.60 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                      971.60 |
| Customer Distribution (TPC-H Q13)                   |                     2288.64 |
| Promotion Effect Query (TPC-H Q14)                  |                      530.62 |
| Top Supplier Query (TPC-H Q15)                      |                      605.64 |
| Parts/Supplier Relationship (TPC-H Q16)             |                      528.01 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                     1830.66 |
| Large Volume Customer (TPC-H Q18)                   |                     9958.40 |
| Discounted Revenue (TPC-H Q19)                      |                      929.11 |
| Potential Part Promotion (TPC-H Q20)                |                      476.76 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                     1228.42 |
| Global Sales Opportunity Query (TPC-H Q22)          |                      196.47 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Benchmarking phase: component benchmarker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| databaseservice-1-1-1-1 |        16.37 |      0.58 |           0.37 |                  0.37 |

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: DatabaseService-1)
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: No monitoring metrics missing
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
```

</details>

## Refresh Stream

`-xrs N` runs the TPC-H refresh functions RF1 (insert new orders) and RF2 (delete old orders) as an additional job next to the query streams, see [TPC-H](Example-TPC-H.md#refresh-stream).
For a PostgreSQL-compatible database service, the loader image of PostgreSQL is used: RF1 and RF2 run against the service.
Here, 3 query streams run in parallel with a refresh stream of 3 RF1+RF2 pairs.

```bash
bexhoma tpch \
  -dbms DatabaseService \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii \
  -xic \
  -xis \
  -ne 3 \
  -xrs 3 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_databaseservice_refresh.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_databaseservice_refresh_summary.md" target="_blank" rel="noopener">docs_tpch_databaseservice_refresh.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 494s 
* Code: 1794045379
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * A TPC-H refresh stream (RF1+RF2) runs in parallel, with 3 pair(s) applied per round.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.13.
  * Experiment is limited to DBMS ['DatabaseService'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [3] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 2.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* databaseservice-1-1-1-1-1 uses docker image postgres:16.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806783
  * datadisk:39
  * volume_size:1.8T
  * volume_used:788G
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 1.0 CPU, 1.0 GiB RAM requested in 1 pods
    * sut: 1 x, 1.0 CPU, 1.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794045379
* databaseservice-1-1-1-1-2 uses docker image postgres:16.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806783
  * datadisk:39
  * volume_size:1.8T
  * volume_used:788G
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 1.0 CPU, 1.0 GiB RAM requested in 1 pods
    * sut: 1 x, 1.0 CPU, 1.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794045379
* databaseservice-1-1-1-1-3 uses docker image postgres:16.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806783
  * datadisk:39
  * volume_size:1.8T
  * volume_used:788G
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 1.0 CPU, 1.0 GiB RAM requested in 1 pods
    * sut: 1 x, 1.0 CPU, 1.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794045379

### Init Scripts Not in Folder
* DatabaseService-1: skipped checkschema-tpch.sql

### SUT Container Restarts
* bexhoma-sut-databaseservice-1-1794045379-55b9f4cbd8-fwh4q: 0

### Workflow

#### Actual

* DBMS DatabaseService-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

#### Planned

* DBMS DatabaseService-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

### Loading

#### Per Run

|                     |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:--------------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| DatabaseService-1-1 |                1 |    1 |       67.00 |           3.00 |           17.00 |          9.00 |           33.00 |              8 |           0 |             | None           |             0 | False         |               53.73 | False               |

### Benchmarking

#### Per Connection

| DBMS                      | configuration     | phase                 | job                     |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                       |
|:--------------------------|:------------------|:----------------------|:------------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:--------------------------|
| databaseservice-1-1-1-1-1 | DatabaseService-1 | databaseservice-1-1-1 | databaseservice-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         17 |            0.37 |             9829.56 |           4658.82 |          -1 | databaseservice-1-1-1-1-1 |
| databaseservice-1-1-1-1-2 | DatabaseService-1 | databaseservice-1-1-1 | databaseservice-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         16 |            0.39 |             9244.78 |           4950.00 |          -1 | databaseservice-1-1-1-1-2 |
| databaseservice-1-1-1-1-3 | DatabaseService-1 | databaseservice-1-1-1 | databaseservice-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         17 |            0.38 |             9431.78 |           4658.82 |          -1 | databaseservice-1-1-1-1-3 |

#### Per Phase

|                       | phase                 |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------------|:----------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| databaseservice-1-1-1 | databaseservice-1-1-1 |                1 |        1 |               1 |           3 | 1.00 |               66 |                  66 |         17 |            0.38 |             9498.93 |          13976.47 |          -1 |

#### Query Completion per Phase

| phase                 |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:----------------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| databaseservice-1-1-1 |      3 | 3/3                                 | 3/3                                      | 3/3                            | 3/3                                        | 3/3                                | 3/3                                     | 3/3                                | 3/3                                | 3/3                                      | 3/3                                         | 3/3                                          | 3/3                                             | 3/3                                 | 3/3                                  | 3/3                              | 3/3                                       | 3/3                                        | 3/3                                 | 3/3                              | 3/3                                    | 3/3                                                   | 3/3                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### tpch_refresh

| connection                | phase                 | job                     |   experiment_run |   client |   benchmark_run |   pod_count | benchmark_begin     | benchmark_end       |   benchmark_duration |
|:--------------------------|:----------------------|:------------------------|-----------------:|---------:|----------------:|------------:|:--------------------|:--------------------|---------------------:|
| databaseservice-1-1-1-2-1 | databaseservice-1-1-1 | databaseservice-1-1-1-2 |                1 |        1 |               2 |           1 | 2026-11-07 11:03:37 | 2026-11-07 11:03:40 |                    3 |

### Latency of Timer Execution [ms]
| Queries                                             |   databaseservice-1-1-1-1-1 |   databaseservice-1-1-1-1-2 |   databaseservice-1-1-1-1-3 |
|:----------------------------------------------------|----------------------------:|----------------------------:|----------------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                     1852.31 |                     1505.41 |                     1645.94 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                      218.32 |                      237.02 |                      243.57 |
| Shipping Priority (TPC-H Q3)                        |                      348.88 |                      345.59 |                      409.73 |
| Order Priority Checking Query (TPC-H Q4)            |                      524.83 |                      600.17 |                      548.58 |
| Local Supplier Volume (TPC-H Q5)                    |                      299.05 |                      313.92 |                      343.72 |
| Forecasting Revenue Change (TPC-H Q6)               |                      252.09 |                      229.46 |                      243.00 |
| Volume Shipping Query (TPC-H Q7)                    |                      325.53 |                      413.20 |                      336.64 |
| National Market Share (TPC-H Q8)                    |                      277.15 |                      322.62 |                      277.39 |
| Product Type Profit Measure (TPC-H Q9)              |                      503.02 |                      559.57 |                      539.99 |
| Returned Item Reporting Query (TPC-H Q10)           |                      554.79 |                      558.90 |                      637.13 |
| Important Stock Identification (TPC-H Q11)          |                      103.55 |                      122.51 |                      110.33 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                      403.38 |                      462.13 |                      388.44 |
| Customer Distribution (TPC-H Q13)                   |                      679.13 |                      712.21 |                      745.35 |
| Promotion Effect Query (TPC-H Q14)                  |                      216.60 |                      229.27 |                      209.80 |
| Top Supplier Query (TPC-H Q15)                      |                      228.58 |                      227.80 |                      263.02 |
| Parts/Supplier Relationship (TPC-H Q16)             |                      278.33 |                      345.24 |                      211.24 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                      620.33 |                      623.98 |                      662.97 |
| Large Volume Customer (TPC-H Q18)                   |                     3408.52 |                     2995.54 |                     4029.48 |
| Discounted Revenue (TPC-H Q19)                      |                      289.82 |                      300.22 |                      303.27 |
| Potential Part Promotion (TPC-H Q20)                |                      251.90 |                      262.57 |                      259.81 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                      347.46 |                      388.07 |                      302.72 |
| Global Sales Opportunity Query (TPC-H Q22)          |                       85.81 |                      105.50 |                      109.37 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
```

</details>
