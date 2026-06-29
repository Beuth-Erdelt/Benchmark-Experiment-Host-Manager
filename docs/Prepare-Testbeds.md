# Example: Prepare Testbeds

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

## Overview

A **testbed** is a running, data-loaded DBMS deployment inside the Kubernetes cluster, ready for benchmarking.
Preparing a testbed involves the following steps:

1. Start the SUT (System Under Test — the DBMS container).
2. Start monitoring.
3. Run the loading phase (generate and import data).
4. Run the benchmarking phase.
5. Collect and evaluate measurements.
6. Remove all ephemeral components from the cluster.

Normally you want all phases to run in one go.
Bexhoma exposes three operating modes that let you stop the process at different points, which is useful for debugging, extending the implementation, or inspecting the DBMS state after loading.

> **Note:** All examples below keep the DBMS running after the experiment finishes.
> The summary output includes a "Services" section with the `kubectl port-forward` command to connect to the running instance.

---

## Operating Modes

Every benchmark script (`ycsb.py`, `benchbase.py`, `hammerdb.py`, `tpch.py`, `tpcds.py`) accepts the same three positional mode arguments:

| Mode | What happens |
|---|---|
| `start` | Start the SUT only. No data is loaded. Useful to inspect the fresh DBMS or run custom SQL by hand. |
| `load` | Start the SUT and run the data loading phase. Stops before benchmarking. Useful to pre-populate a volume and check import metrics. |
| `run` | Full experiment: start SUT, load data (or reuse an existing volume), run the benchmark, collect results. |

Data volumes are identified by DBMS, benchmark, and scale factor.
If a volume already exists and is marked as loaded, the `load` step is skipped automatically in `run` mode — the data is reused.

---

## Environment Variables

The examples below assume three node-selector variables and a log directory.
Adjust the node names to match your cluster, or drop `-rnn`/`-rnl`/`-rnb` entirely to let Kubernetes schedule freely.

```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"
BEXHOMA_MS=1        # number of parallel experiment management processes

mkdir -p $LOG_DIR
```

---

## Reading the Summary Output

After each mode completes, Bexhoma prints a summary.
The sections have consistent meaning across all benchmark types:

| Section | Present in | Description |
|---|---|---|
| **Workload** | all modes | Experiment metadata: type, code, duration, parameter choices, bexhoma version |
| **Services** | all modes | `kubectl port-forward` command to reach the running SUT from your local machine |
| **Connections** | all modes | Hardware details of the node hosting the SUT (RAM, CPU, disk, resource requests) |
| **Loading** | `load`, `run` | Import throughput metrics (rows/second, time, pod count) |
| **Execution** | `run` | Benchmark results: throughput, latency, error count |
| **Workflow** | `run` | Planned vs. actual pod configuration — useful for verifying scale-out |
| **Ingestion - SUT** | `load`, `run` | CPU and RAM consumed by the DBMS during the loading phase |
| **Ingestion - Loader** | `load`, `run` | CPU and RAM consumed by the loader pods during the loading phase |
| **Execution - SUT** | `run` | CPU and RAM consumed by the DBMS during benchmarking |
| **Execution - Benchmarker** | `run` | CPU and RAM consumed by the driver pods during benchmarking |
| **Tests** | all modes | Automated sanity checks — e.g., no zero throughput, no NaN metrics, workflow matches plan |

A `TEST failed` line does not necessarily abort the experiment; it flags a condition worth investigating (e.g., a query error in TPC-DS Q90, or a monitoring gap).

---

## Inspecting Cluster State

You can watch or clean up all pods belonging to a specific benchmark using its use-case label:

```bash
# Watch components
kubectl get all -l app=bexhoma,usecase=<label>

# Remove all components
kubectl delete all -l app=bexhoma,usecase=<label>
```

| Benchmark | Label |
|---|---|
| YCSB | `ycsb` |
| Benchbase TPC-C | `benchbase_tpcc` |
| HammerDB TPC-C | `hammerdb_tpcc` |
| TPC-H | `tpc-h` |
| TPC-DS | `tpc-ds` |

---

## YCSB

YCSB is a key-value workload generator.
Configurations are numbered sequentially per DBMS — the first configuration is `PostgreSQL-1`, the second `PostgreSQL-2`, and so on.

### Start DBMS

Starts PostgreSQL without loading any data.
After this completes you can connect to the instance and run queries manually.

```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -xwl c \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT \
  start &>$LOG_DIR/docs_ycsb_postgresql_start.log
```

docs_ycsb_postgresql_start.log
```markdown
## Show Summary

### Workload
YCSB Start DBMS
* Type: ycsb
* Duration: 225s 
* Code: 1782727531
* Start DBMS and do not load data.
* This just starts a SUT.
  * Workload is 'C'.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * SUT is fixed to cl-worker38.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782727531 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263522
  * datadisk:39
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782727531

### Tests
```

docs_ycsb_postgresql_start.log
```markdown
## Show Summary

### Workload
YCSB Start DBMS
* Type: ycsb
* Duration: 225s 
* Code: 1782727531
* Start DBMS and do not load data.
* This just starts a SUT.
  * Workload is 'C'.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * SUT is fixed to cl-worker38.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782727531 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263522
  * datadisk:39
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782727531

### Tests
```

The summary confirms the SUT is running and shows the port-forward command.

### Start DBMS and Load Data

Starts PostgreSQL and imports YCSB data using 8 parallel loader pods with 64 threads each.

```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -xwl c \
  -nlp 8 \
  -nlt 64 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load &>$LOG_DIR/docs_ycsb_postgresql_load.log
```

docs_ycsb_postgresql_load.log
```markdown
## Show Summary

### Workload
YCSB Data Loading SF=1
* Type: ycsb
* Duration: 347s 
* Code: 1782727797
* YCSB driver runs the experiment.
* This imports YCSB data sets.
  * Workload is 'C'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Target is based on multiples of '16384'.
  * Factors for loading are [1].
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [64] threads, split into [8] pods.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782727797 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:265873
  * datadisk:2391
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782727797

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| PostgreSQL-1-1-0-1-1 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.98 |                61275.00 |            125000.00 |                              2099.00 | 1.00 |               58.75 |
| PostgreSQL-1-1-0-1-2 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.45 |                61291.00 |            125000.00 |                              2215.00 | 1.00 |               58.74 |
| PostgreSQL-1-1-0-1-3 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.02 |                61304.00 |            125000.00 |                              2179.00 | 1.00 |               58.72 |
| PostgreSQL-1-1-0-1-4 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.45 |                61261.00 |            125000.00 |                              2071.00 | 1.00 |               58.76 |
| PostgreSQL-1-1-0-1-5 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.48 |                61260.00 |            125000.00 |                              2177.00 | 1.00 |               58.77 |
| PostgreSQL-1-1-0-1-6 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.45 |                61261.00 |            125000.00 |                              2155.00 | 1.00 |               58.76 |
| PostgreSQL-1-1-0-1-7 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.85 |                61279.00 |            125000.00 |                              2211.00 | 1.00 |               58.75 |
| PostgreSQL-1-1-0-1-8 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.42 |                61262.00 |            125000.00 |                              2205.00 | 1.00 |               58.76 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 16384.00 |        8.00 |         0.00 | 1.00 |               58.72 |                        16320.10 |                61304.00 |           1000000.00 |                              2164.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |       252.96 |      3.96 |           1.58 |                  2.76 |

### Loading phase: component loader

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |        91.71 |      1.57 |           0.11 |                  0.11 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
```

docs_ycsb_postgresql_load.log
```markdown
## Show Summary

### Workload
YCSB Data Loading SF=1
* Type: ycsb
* Duration: 347s 
* Code: 1782727797
* YCSB driver runs the experiment.
* This imports YCSB data sets.
  * Workload is 'C'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Target is based on multiples of '16384'.
  * Factors for loading are [1].
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [64] threads, split into [8] pods.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782727797 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:265873
  * datadisk:2391
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782727797

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| PostgreSQL-1-1-0-1-1 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.98 |                61275.00 |            125000.00 |                              2099.00 | 1.00 |               58.75 |
| PostgreSQL-1-1-0-1-2 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.45 |                61291.00 |            125000.00 |                              2215.00 | 1.00 |               58.74 |
| PostgreSQL-1-1-0-1-3 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.02 |                61304.00 |            125000.00 |                              2179.00 | 1.00 |               58.72 |
| PostgreSQL-1-1-0-1-4 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.45 |                61261.00 |            125000.00 |                              2071.00 | 1.00 |               58.76 |
| PostgreSQL-1-1-0-1-5 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.48 |                61260.00 |            125000.00 |                              2177.00 | 1.00 |               58.77 |
| PostgreSQL-1-1-0-1-6 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.45 |                61261.00 |            125000.00 |                              2155.00 | 1.00 |               58.76 |
| PostgreSQL-1-1-0-1-7 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.85 |                61279.00 |            125000.00 |                              2211.00 | 1.00 |               58.75 |
| PostgreSQL-1-1-0-1-8 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.42 |                61262.00 |            125000.00 |                              2205.00 | 1.00 |               58.76 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 16384.00 |        8.00 |         0.00 | 1.00 |               58.72 |                        16320.10 |                61304.00 |           1000000.00 |                              2164.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |       252.96 |      3.96 |           1.58 |                  2.76 |

### Loading phase: component loader

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |        91.71 |      1.57 |           0.11 |                  0.11 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
```

Key parameters:
- `-nlp 8`: 8 parallel loader pods
- `-nlt 64`: 64 threads per loader pod

The summary's **Loading** table shows aggregate throughput across all loader pods.
The **Ingestion** tables show how much CPU and RAM the SUT and loader consumed.

### Start DBMS and Load Data and Run Workload

Full experiment: loads data and then runs YCSB workload C with 8 benchmarker pods.

```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -xwl c \
  -nlp 8 \
  -nlt 64 \
  -nbp 8 \
  -nbt 64 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -ss \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_postgresql_run.log
```

docs_ycsb_postgresql_run.log
```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 455s 
* Code: 1782728190
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'C'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:265873
  * datadisk:2391
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782728190

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (8 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (8 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| PostgreSQL-1-1-0-1-1 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.05 |                61273.00 |            125000.00 |                              2327.00 | 1.00 |               58.75 |
| PostgreSQL-1-1-0-1-2 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.45 |                61261.00 |            125000.00 |                              2431.00 | 1.00 |               58.76 |
| PostgreSQL-1-1-0-1-3 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.95 |                61276.00 |            125000.00 |                              2359.00 | 1.00 |               58.75 |
| PostgreSQL-1-1-0-1-4 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.72 |                61283.00 |            125000.00 |                              2069.00 | 1.00 |               58.74 |
| PostgreSQL-1-1-0-1-5 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.32 |                61265.00 |            125000.00 |                              2187.00 | 1.00 |               58.76 |
| PostgreSQL-1-1-0-1-6 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.68 |                61254.00 |            125000.00 |                              1957.00 | 1.00 |               58.77 |
| PostgreSQL-1-1-0-1-7 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.98 |                61275.00 |            125000.00 |                              2237.00 | 1.00 |               58.75 |
| PostgreSQL-1-1-0-1-8 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.92 |                61277.00 |            125000.00 |                              2291.00 | 1.00 |               58.75 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 16384.00 |        8.00 |         0.00 | 1.00 |               58.74 |                        16321.07 |                61283.00 |           1000000.00 |                              2232.25 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|
| PostgreSQL-1-1-1-1-3 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       3 |         8 |     2048 |           8 |            0 |                         2040.08 |                61272.00 |             125000 |                             770.00 |
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |         8 |     2048 |           8 |            0 |                         2040.18 |                61269.00 |             125000 |                             902.00 |
| PostgreSQL-1-1-1-1-2 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       2 |         8 |     2048 |           8 |            0 |                         2040.12 |                61271.00 |             125000 |                             964.00 |
| PostgreSQL-1-1-1-1-7 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       7 |         8 |     2048 |           8 |            0 |                         2040.18 |                61269.00 |             125000 |                             766.00 |
| PostgreSQL-1-1-1-1-6 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       6 |         8 |     2048 |           8 |            0 |                         2040.45 |                61261.00 |             125000 |                             873.00 |
| PostgreSQL-1-1-1-1-8 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       8 |         8 |     2048 |           8 |            0 |                         2040.12 |                61271.00 |             125000 |                             877.00 |
| PostgreSQL-1-1-1-1-4 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       4 |         8 |     2048 |           8 |            0 |                         2040.12 |                61271.00 |             125000 |                             907.00 |
| PostgreSQL-1-1-1-1-5 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       5 |         8 |     2048 |           8 |            0 |                         2039.82 |                61280.00 |             125000 |                             813.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        64 |    16384 |               1 |           8 |            0 |                        16321.07 |                61280.00 |            1000000 |                             964.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       234.93 |      3.78 |           1.57 |                  2.64 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        83.19 |      1.57 |           0.11 |                  0.11 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       137.53 |      2.32 |           1.85 |                  3.02 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        76.45 |      1.32 |           0.10 |                  0.11 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

docs_ycsb_postgresql_run.log
```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 455s 
* Code: 1782728190
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'C'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:265873
  * datadisk:2391
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782728190

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (8 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (8 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| PostgreSQL-1-1-0-1-1 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.05 |                61273.00 |            125000.00 |                              2327.00 | 1.00 |               58.75 |
| PostgreSQL-1-1-0-1-2 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.45 |                61261.00 |            125000.00 |                              2431.00 | 1.00 |               58.76 |
| PostgreSQL-1-1-0-1-3 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.95 |                61276.00 |            125000.00 |                              2359.00 | 1.00 |               58.75 |
| PostgreSQL-1-1-0-1-4 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.72 |                61283.00 |            125000.00 |                              2069.00 | 1.00 |               58.74 |
| PostgreSQL-1-1-0-1-5 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.32 |                61265.00 |            125000.00 |                              2187.00 | 1.00 |               58.76 |
| PostgreSQL-1-1-0-1-6 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.68 |                61254.00 |            125000.00 |                              1957.00 | 1.00 |               58.77 |
| PostgreSQL-1-1-0-1-7 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.98 |                61275.00 |            125000.00 |                              2237.00 | 1.00 |               58.75 |
| PostgreSQL-1-1-0-1-8 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.92 |                61277.00 |            125000.00 |                              2291.00 | 1.00 |               58.75 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 16384.00 |        8.00 |         0.00 | 1.00 |               58.74 |                        16321.07 |                61283.00 |           1000000.00 |                              2232.25 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|
| PostgreSQL-1-1-1-1-3 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       3 |         8 |     2048 |           8 |            0 |                         2040.08 |                61272.00 |             125000 |                             770.00 |
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |         8 |     2048 |           8 |            0 |                         2040.18 |                61269.00 |             125000 |                             902.00 |
| PostgreSQL-1-1-1-1-2 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       2 |         8 |     2048 |           8 |            0 |                         2040.12 |                61271.00 |             125000 |                             964.00 |
| PostgreSQL-1-1-1-1-7 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       7 |         8 |     2048 |           8 |            0 |                         2040.18 |                61269.00 |             125000 |                             766.00 |
| PostgreSQL-1-1-1-1-6 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       6 |         8 |     2048 |           8 |            0 |                         2040.45 |                61261.00 |             125000 |                             873.00 |
| PostgreSQL-1-1-1-1-8 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       8 |         8 |     2048 |           8 |            0 |                         2040.12 |                61271.00 |             125000 |                             877.00 |
| PostgreSQL-1-1-1-1-4 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       4 |         8 |     2048 |           8 |            0 |                         2040.12 |                61271.00 |             125000 |                             907.00 |
| PostgreSQL-1-1-1-1-5 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       5 |         8 |     2048 |           8 |            0 |                         2039.82 |                61280.00 |             125000 |                             813.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        64 |    16384 |               1 |           8 |            0 |                        16321.07 |                61280.00 |            1000000 |                             964.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       234.93 |      3.78 |           1.57 |                  2.64 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        83.19 |      1.57 |           0.11 |                  0.11 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       137.53 |      2.32 |           1.85 |                  3.02 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        76.45 |      1.32 |           0.10 |                  0.11 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

Key parameters:
- `-nbp 8`: 8 parallel benchmarker pods
- `-nbt 64`: 64 threads per benchmarker pod
- `-ss`: use a single shared storage volume

The **Execution** table aggregates throughput across all benchmarker pods.
The **Workflow** section confirms the actual pod count matched the plan.

---

## Benchbase (TPC-C)

Benchbase runs TPC-C transactions.
Configurations are numbered sequentially per DBMS — `PostgreSQL-1`, `PostgreSQL-2`, etc.

### Start DBMS

```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT \
  start &>$LOG_DIR/docs_benchbase_postgresql_start.log
```

docs_benchbase_postgresql_start.log
```markdown
## Show Summary

### Workload
Benchbase Start DBMS
* Type: benchbase
* Duration: 196s 
* Code: 1782728701
* Start DBMS and do not load data.
* This just starts a SUT.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * SUT is fixed to cl-worker38.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782728701 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263522
  * datadisk:39
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782728701
    * TENANT_VOL:False

### Tests
* TEST failed: Throughput (requests/second) contains 0 or NaN
```

docs_benchbase_postgresql_start.log
```markdown
## Show Summary

### Workload
Benchbase Start DBMS
* Type: benchbase
* Duration: 196s 
* Code: 1782728701
* Start DBMS and do not load data.
* This just starts a SUT.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * SUT is fixed to cl-worker38.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782728701 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263522
  * datadisk:39
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782728701
    * TENANT_VOL:False

### Tests
* TEST failed: Throughput (requests/second) contains 0 or NaN
```

### Start DBMS and Load Data

Imports TPC-C data (scale factor 1) using 8 parallel loader pods.

```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -nlp 8 \
  -nlt 64 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load &>$LOG_DIR/docs_benchbase_postgresql_load.log
```

docs_benchbase_postgresql_load.log
```markdown
## Show Summary

### Workload
Benchbase Data tpcc Loading SF=1
* Type: benchbase
* Duration: 305s 
* Code: 1782728921
* Benchbase runs a TPC-C experiment.
* This imports a Benchbase data set.
  * Benchbase data is generated and loaded using several threads. Scaling factor is 1. Target is based on multiples of '1024'.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [64] threads, split into [8] pods.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782728921 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263813
  * datadisk:330
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782728921
    * TENANT_VOL:False

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |       92.00 |           0.00 |            0.00 |         27.00 |           65.00 |              1 |           1 |             |                |             0 | False         |               39.13 |

### Monitoring

### Loading phase: SUT deployment

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |        12.56 |      0.62 |           0.49 |                  0.62 |

### Loading phase: component loader

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |         0.02 |      0.00 |           0.00 |                  0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST failed: Throughput (requests/second) contains 0 or NaN
```

docs_benchbase_postgresql_load.log
```markdown
## Show Summary

### Workload
Benchbase Data tpcc Loading SF=1
* Type: benchbase
* Duration: 305s 
* Code: 1782728921
* Benchbase runs a TPC-C experiment.
* This imports a Benchbase data set.
  * Benchbase data is generated and loaded using several threads. Scaling factor is 1. Target is based on multiples of '1024'.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [64] threads, split into [8] pods.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782728921 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263813
  * datadisk:330
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782728921
    * TENANT_VOL:False

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |       92.00 |           0.00 |            0.00 |         27.00 |           65.00 |              1 |           1 |             |                |             0 | False         |               39.13 |

### Monitoring

### Loading phase: SUT deployment

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |        12.56 |      0.62 |           0.49 |                  0.62 |

### Loading phase: component loader

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |         0.02 |      0.00 |           0.00 |                  0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST failed: Throughput (requests/second) contains 0 or NaN
```

The **Loading** table reports `Throughput [SF/h]` — scale factors loaded per hour.

### Start DBMS and Load Data and Run Workload

Loads data with 1 pod (Benchbase loads serially by design) and runs the workload with 8 benchmarker pods for 5 minutes.

```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -nlp 1 \
  -nlt 64 \
  -nbp 8 \
  -nbt 64 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -ss \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_run.log
```

docs_benchbase_postgresql_run.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=1
* Type: benchbase
* Duration: 623s 
* Code: 1782729260
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [64] threads, split into [1] pods.
  * Benchmarking is tested with [64] threads, split into [8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263813
  * datadisk:330
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782729260
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (8 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (8 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |       60.00 |           0.00 |            0.00 |         24.00 |           36.00 |              1 |           1 |             |                |             0 | False         |               60.00 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       1 |           0 | 300.00 |            0 |                          49.77 |                       49.33 |         0.00 |                                                     795782.00 |                                             160593.00 |
| PostgreSQL-1-1-1-1-2 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       2 |           0 | 300.00 |            0 |                          51.12 |                       50.67 |         0.00 |                                                     776572.00 |                                             156332.00 |
| PostgreSQL-1-1-1-1-3 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       3 |           0 | 300.00 |            0 |                          51.86 |                       51.39 |         0.00 |                                                     759531.00 |                                             154189.00 |
| PostgreSQL-1-1-1-1-4 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       4 |           0 | 300.00 |            0 |                          52.19 |                       51.72 |         0.00 |                                                     761943.00 |                                             153159.00 |
| PostgreSQL-1-1-1-1-5 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       5 |           0 | 300.00 |            1 |                          53.56 |                       53.14 |         0.00 |                                                     735668.00 |                                             149154.00 |
| PostgreSQL-1-1-1-1-6 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       6 |           0 | 300.00 |            0 |                          51.61 |                       51.21 |         0.00 |                                                     771811.00 |                                             154611.00 |
| PostgreSQL-1-1-1-1-7 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       7 |           0 | 300.00 |            0 |                          52.33 |                       51.84 |         0.00 |                                                     766001.00 |                                             152760.00 |
| PostgreSQL-1-1-1-1-8 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       8 |           0 | 300.00 |            0 |                          50.34 |                       49.86 |         0.00 |                                                     784940.00 |                                             158604.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |          64 |     1024 |               1 |           8 |           0 | 300.00 |            1 |                         412.75 |                      409.15 |         0.00 |                                                     795782.00 |                                             154925.25 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        19.78 |      0.55 |           0.51 |                  0.66 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.02 |      0.00 |           0.00 |                  0.00 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       712.12 |      2.61 |           0.90 |                  1.18 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       197.29 |      1.41 |           0.24 |                  0.24 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```

docs_benchbase_postgresql_run.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=1
* Type: benchbase
* Duration: 623s 
* Code: 1782729260
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [64] threads, split into [1] pods.
  * Benchmarking is tested with [64] threads, split into [8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263813
  * datadisk:330
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782729260
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (8 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (8 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |       60.00 |           0.00 |            0.00 |         24.00 |           36.00 |              1 |           1 |             |                |             0 | False         |               60.00 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       1 |           0 | 300.00 |            0 |                          49.77 |                       49.33 |         0.00 |                                                     795782.00 |                                             160593.00 |
| PostgreSQL-1-1-1-1-2 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       2 |           0 | 300.00 |            0 |                          51.12 |                       50.67 |         0.00 |                                                     776572.00 |                                             156332.00 |
| PostgreSQL-1-1-1-1-3 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       3 |           0 | 300.00 |            0 |                          51.86 |                       51.39 |         0.00 |                                                     759531.00 |                                             154189.00 |
| PostgreSQL-1-1-1-1-4 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       4 |           0 | 300.00 |            0 |                          52.19 |                       51.72 |         0.00 |                                                     761943.00 |                                             153159.00 |
| PostgreSQL-1-1-1-1-5 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       5 |           0 | 300.00 |            1 |                          53.56 |                       53.14 |         0.00 |                                                     735668.00 |                                             149154.00 |
| PostgreSQL-1-1-1-1-6 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       6 |           0 | 300.00 |            0 |                          51.61 |                       51.21 |         0.00 |                                                     771811.00 |                                             154611.00 |
| PostgreSQL-1-1-1-1-7 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       7 |           0 | 300.00 |            0 |                          52.33 |                       51.84 |         0.00 |                                                     766001.00 |                                             152760.00 |
| PostgreSQL-1-1-1-1-8 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       8 |           0 | 300.00 |            0 |                          50.34 |                       49.86 |         0.00 |                                                     784940.00 |                                             158604.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |          64 |     1024 |               1 |           8 |           0 | 300.00 |            1 |                         412.75 |                      409.15 |         0.00 |                                                     795782.00 |                                             154925.25 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        19.78 |      0.55 |           0.51 |                  0.66 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.02 |      0.00 |           0.00 |                  0.00 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       712.12 |      2.61 |           0.90 |                  1.18 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       197.29 |      1.41 |           0.24 |                  0.24 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```

The **Execution** table reports:
- `Throughput (requests/second)` and `Goodput (requests/second)` — total and successful transaction rate
- `Latency Distribution.95th Percentile Latency (microseconds)` — tail latency
- `efficiency` — how close actual throughput came to the target

---

## HammerDB (TPC-C)

HammerDB runs TPC-C using virtual users (vusers).
Configurations are numbered sequentially per DBMS — `PostgreSQL-1`, `PostgreSQL-2`, etc.

### Start DBMS

```bash
bexhoma hammerdb \
  -dbms PostgreSQL \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT \
  start &>$LOG_DIR/docs_hammerdb_postgresql_start.log
```

docs_hammerdb_postgresql_start.log
```markdown
## Show Summary

### Workload
HammerDB Start DBMS
* Type: tpcc
* Duration: 195s 
* Code: 1782729924
* Start DBMS and do not load data.
* This just starts a SUT.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * SUT is fixed to cl-worker38.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782729924 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263522
  * datadisk:39
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782729924

### Tests
```

docs_hammerdb_postgresql_start.log
```markdown
## Show Summary

### Workload
HammerDB Start DBMS
* Type: tpcc
* Duration: 195s 
* Code: 1782729924
* Start DBMS and do not load data.
* This just starts a SUT.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * SUT is fixed to cl-worker38.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782729924 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263522
  * datadisk:39
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782729924

### Tests
```

### Start DBMS and Load Data

Imports TPC-C data (1 warehouse = scale factor 1) using a single loader pod.
HammerDB's loader is inherently single-threaded, so `-nlp 1 -nlt 1` is typical.

```bash
bexhoma hammerdb \
  -dbms PostgreSQL \
  -nlp 1 \
  -nlt 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load &>$LOG_DIR/docs_hammerdb_postgresql_load.log
```

docs_hammerdb_postgresql_load.log
```markdown
## Show Summary

### Workload
HammerDB Data Loading SF=1 (warehouses for TPC-C)
* Type: tpcc
* Duration: 268s 
* Code: 1782730137
* HammerDB runs the benchmark.
* This imports TPC-C data sets.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 1.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782730137 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263763
  * datadisk:280
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782730137

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |       55.00 |           0.00 |            0.00 |         21.00 |           34.00 |              1 |           1 |             | None           |             0 | False         |               65.45 |

### Monitoring

### Loading phase: SUT deployment

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |         1.72 |      0.09 |           0.44 |                  0.50 |

### Loading phase: component loader

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST failed: Loading phase: component loader contains 0 or NaN in CPU [CPUs]
```

docs_hammerdb_postgresql_load.log
```markdown
## Show Summary

### Workload
HammerDB Data Loading SF=1 (warehouses for TPC-C)
* Type: tpcc
* Duration: 268s 
* Code: 1782730137
* HammerDB runs the benchmark.
* This imports TPC-C data sets.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 1.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782730137 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263763
  * datadisk:280
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782730137

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |       55.00 |           0.00 |            0.00 |         21.00 |           34.00 |              1 |           1 |             | None           |             0 | False         |               65.45 |

### Monitoring

### Loading phase: SUT deployment

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |         1.72 |      0.09 |           0.44 |                  0.50 |

### Loading phase: component loader

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST failed: Loading phase: component loader contains 0 or NaN in CPU [CPUs]
```

The **Loading** table reports `Imported warehouses [1/h]`.

### Start DBMS and Load Data and Run Workload

Loads data and runs TPC-C for 5 minutes with 64 virtual users.

```bash
bexhoma hammerdb \
  -dbms PostgreSQL \
  -nlp 1 \
  -nlt 1 \
  -nbp 1 \
  -nbt 64 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -ss \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hammerdb_postgresql_run.log
```

docs_hammerdb_postgresql_run.log
```markdown
## Show Summary

### Workload
HammerDB Workload SF=1 (warehouses for TPC-C)
* Type: tpcc
* Duration: 699s 
* Code: 1782730435
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 1. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263809
  * datadisk:280
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782730435

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |       58.00 |           1.00 |            0.00 |         21.00 |           36.00 |              1 |           1 |             | None           |             0 | False         |               62.07 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |   TPM |   efficiency |   duration |   errors |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|------:|-------------:|-----------:|---------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |       64 |        1 |               1 |       1 |  43113 | 99111 |         0.00 |          5 |        0 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   efficiency |     NOPM |      TPM |   duration |   errors |
|:-----------------|:-----------------|-----------------:|---------:|---------:|----------------:|------------:|-------------:|---------:|---------:|-----------:|---------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |       64 |        1 |               1 |           1 |         0.00 | 43113.00 | 99111.00 |          5 |        0 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         1.39 |      0.09 |           0.44 |                  0.48 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      3243.54 |      8.26 |           1.70 |                  2.45 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        93.19 |      0.30 |           0.23 |                  0.24 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST failed: Loading phase: component loader contains 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
```

docs_hammerdb_postgresql_run.log
```markdown
## Show Summary

### Workload
HammerDB Workload SF=1 (warehouses for TPC-C)
* Type: tpcc
* Duration: 699s 
* Code: 1782730435
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 1. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263809
  * datadisk:280
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782730435

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |       58.00 |           1.00 |            0.00 |         21.00 |           36.00 |              1 |           1 |             | None           |             0 | False         |               62.07 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |   TPM |   efficiency |   duration |   errors |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|------:|-------------:|-----------:|---------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |       64 |        1 |               1 |       1 |  43113 | 99111 |         0.00 |          5 |        0 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   efficiency |     NOPM |      TPM |   duration |   errors |
|:-----------------|:-----------------|-----------------:|---------:|---------:|----------------:|------------:|-------------:|---------:|---------:|-----------:|---------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |       64 |        1 |               1 |           1 |         0.00 | 43113.00 | 99111.00 |          5 |        0 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         1.39 |      0.09 |           0.44 |                  0.48 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      3243.54 |      8.26 |           1.70 |                  2.45 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        93.19 |      0.30 |           0.23 |                  0.24 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST failed: Loading phase: component loader contains 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
```

The **Execution** table reports `NOPM` (New Orders Per Minute) and `TPM` (Transactions Per Minute), which are the standard HammerDB TPC-C metrics.

---

## TPC-H

TPC-H is the standard analytical benchmark with 22 queries.
Data is generated by a loader pod using `dbgen`, then loaded into the SUT.
After loading, the DBMSBenchmarker tool runs the 22 queries and records per-query latency.

### Start DBMS

```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT \
  start &>$LOG_DIR/docs_tpch_postgresql_start.log
```

docs_tpch_postgresql_start.log
```markdown
## Show Summary

### Workload
TPC-H Start DBMS
* Type: tpch
* Duration: 163s 
* Code: 1782731190
* Start DBMS and do not load data.
* This just starts a SUT.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * SUT is fixed to cl-worker38.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782731190 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263522
  * datadisk:39
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782731190

### Tests
```

docs_tpch_postgresql_start.log
```markdown
## Show Summary

### Workload
TPC-H Start DBMS
* Type: tpch
* Duration: 163s 
* Code: 1782731190
* Start DBMS and do not load data.
* This just starts a SUT.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * SUT is fixed to cl-worker38.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782731190 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263522
  * datadisk:39
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782731190

### Tests
```

### Start DBMS and Load Data

Generates and loads TPC-H data at scale factor 1.
The flags `-xii -xic -xis` trigger index creation, constraint application, and statistics gathering after the raw data is ingested.

```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -nlp 1 \
  -nlt 1 \
  -xii -xic -xis \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load &>$LOG_DIR/docs_tpch_postgresql_load.log
```

docs_tpch_postgresql_load.log
```markdown
## Show Summary

### Workload
TPC-H Data Loading SF=1
* Type: tpch
* Duration: 306s 
* Code: 1782731396
* This includes the reading queries of TPC-H.
* This imports TPC-H data sets.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782731396 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:266240
  * datadisk:2757
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782731396

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      118.00 |           0.00 |            0.00 |         32.00 |           84.00 |              1 |           0 |             |                |             0 | False         |               30.51 |

### Monitoring

### Loading phase: SUT deployment

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |        33.75 |      0.64 |           1.79 |                  3.32 |

### Loading phase: component data generator

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |         5.14 |      0.00 |           0.00 |                  0.73 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
```

docs_tpch_postgresql_load.log
```markdown
## Show Summary

### Workload
TPC-H Data Loading SF=1
* Type: tpch
* Duration: 306s 
* Code: 1782731396
* This includes the reading queries of TPC-H.
* This imports TPC-H data sets.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782731396 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:266240
  * datadisk:2757
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782731396

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      118.00 |           0.00 |            0.00 |         32.00 |           84.00 |              1 |           0 |             |                |             0 | False         |               30.51 |

### Monitoring

### Loading phase: SUT deployment

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |        33.75 |      0.64 |           1.79 |                  3.32 |

### Loading phase: component data generator

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |         5.14 |      0.00 |           0.00 |                  0.73 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
```

The **Loading** table breaks down time into phases:

| Column | Meaning |
|---|---|
| `timeGenerate` | Time to generate raw data files with `dbgen` |
| `timeIngesting` | Time to import data into the DBMS |
| `timeSchema` | Time to apply schema (DDL) |
| `timeIndex` | Time to create indexes and constraints |
| `timeLoad` | Total loading time |

### Start DBMS and Load Data and Run Workload

Loads TPC-H data and runs all 22 queries once.

```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -nlp 1 \
  -nlt 1 \
  -nbp 1 \
  -nbt 64 \
  -xii -xic -xis \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -ss \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_postgresql_run.log
```

docs_tpch_postgresql_run.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 368s 
* Code: 1782731741
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782731741 9091:9091

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:266241
  * datadisk:2757
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782731741

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      112.00 |           0.00 |            0.00 |         26.00 |           84.00 |              1 |           0 |             |                |             0 | False         |               32.14 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         10 |            0.27 |            13334.38 |           7920.00 |           0 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         10 |            0.27 |            13334.38 |           7920.00 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |
|:----------------------------------------------------|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                1198.68 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 264.33 |
| Shipping Priority (TPC-H Q3)                        |                 318.79 |
| Order Priority Checking Query (TPC-H Q4)            |                 139.65 |
| Local Supplier Volume (TPC-H Q5)                    |                 274.57 |
| Forecasting Revenue Change (TPC-H Q6)               |                 179.45 |
| Volume Shipping Query (TPC-H Q7)                    |                 321.95 |
| National Market Share (TPC-H Q8)                    |                 174.69 |
| Product Type Profit Measure (TPC-H Q9)              |                 521.98 |
| Returned Item Reporting Query (TPC-H Q10)           |                 244.57 |
| Important Stock Identification (TPC-H Q11)          |                  73.80 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 295.34 |
| Customer Distribution (TPC-H Q13)                   |                 752.64 |
| Promotion Effect Query (TPC-H Q14)                  |                 194.42 |
| Top Supplier Query (TPC-H Q15)                      |                 212.76 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 237.22 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                 627.53 |
| Large Volume Customer (TPC-H Q18)                   |                2956.73 |
| Discounted Revenue (TPC-H Q19)                      |                  54.76 |
| Potential Part Promotion (TPC-H Q20)                |                 124.62 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 312.57 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  97.04 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        18.43 |      0.64 |           0.50 |                  1.72 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.02 |      0.00 |           0.00 |                  0.00 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.83 |           1.70 |                  3.25 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST failed: Execution phase: SUT deployment contains 0 or NaN in CPU [CPUs]
* TEST failed: Execution phase: component benchmarker contains 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```

docs_tpch_postgresql_run.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 368s 
* Code: 1782731741
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782731741 9091:9091

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:266241
  * datadisk:2757
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782731741

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      112.00 |           0.00 |            0.00 |         26.00 |           84.00 |              1 |           0 |             |                |             0 | False         |               32.14 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         10 |            0.27 |            13334.38 |           7920.00 |           0 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         10 |            0.27 |            13334.38 |           7920.00 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |
|:----------------------------------------------------|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                1198.68 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 264.33 |
| Shipping Priority (TPC-H Q3)                        |                 318.79 |
| Order Priority Checking Query (TPC-H Q4)            |                 139.65 |
| Local Supplier Volume (TPC-H Q5)                    |                 274.57 |
| Forecasting Revenue Change (TPC-H Q6)               |                 179.45 |
| Volume Shipping Query (TPC-H Q7)                    |                 321.95 |
| National Market Share (TPC-H Q8)                    |                 174.69 |
| Product Type Profit Measure (TPC-H Q9)              |                 521.98 |
| Returned Item Reporting Query (TPC-H Q10)           |                 244.57 |
| Important Stock Identification (TPC-H Q11)          |                  73.80 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 295.34 |
| Customer Distribution (TPC-H Q13)                   |                 752.64 |
| Promotion Effect Query (TPC-H Q14)                  |                 194.42 |
| Top Supplier Query (TPC-H Q15)                      |                 212.76 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 237.22 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                 627.53 |
| Large Volume Customer (TPC-H Q18)                   |                2956.73 |
| Discounted Revenue (TPC-H Q19)                      |                  54.76 |
| Potential Part Promotion (TPC-H Q20)                |                 124.62 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 312.57 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  97.04 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        18.43 |      0.64 |           0.50 |                  1.72 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.02 |      0.00 |           0.00 |                  0.00 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.83 |           1.70 |                  3.25 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST failed: Execution phase: SUT deployment contains 0 or NaN in CPU [CPUs]
* TEST failed: Execution phase: component benchmarker contains 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```

The **Execution** section reports per-query latency in the **Latency of Timer Execution** table and the TPC-H standard metrics:

| Metric | Meaning |
|---|---|
| `Geo Times [s]` | Geometric mean of per-query median runtimes |
| `Power@Size` | TPC-H Power metric: `(3600 × SF) / geo_times` — higher is better |
| `Throughput@Size` | TPC-H Throughput metric across all streams and queries |

---

## TPC-DS

TPC-DS is the decision-support benchmark with 99 queries.
Its structure mirrors TPC-H: `dbgen2` generates data, a loader imports it, DBMSBenchmarker runs the queries.

### Start DBMS

```bash
bexhoma tpcds \
  -dbms PostgreSQL \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT \
  start &>$LOG_DIR/docs_tpcds_postgresql_start.log
```

docs_tpcds_postgresql_start.log
```markdown
## Show Summary

### Workload
TPC-DS Start DBMS
* Type: tpcds
* Duration: 197s 
* Code: 1782732165
* Start DBMS and do not load data.
* This just starts a SUT.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * SUT is fixed to cl-worker38.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782732165 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263523
  * datadisk:39
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782732165

### Tests
```

docs_tpcds_postgresql_start.log
```markdown
## Show Summary

### Workload
TPC-DS Start DBMS
* Type: tpcds
* Duration: 197s 
* Code: 1782732165
* Start DBMS and do not load data.
* This just starts a SUT.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * SUT is fixed to cl-worker38.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782732165 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263523
  * datadisk:39
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782732165

### Tests
```

### Start DBMS and Load Data

```bash
bexhoma tpcds \
  -dbms PostgreSQL \
  -nlp 1 \
  -nlt 1 \
  -xii -xic -xis \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load &>$LOG_DIR/docs_tpcds_postgresql_load.log
```

docs_tpcds_postgresql_load.log
```markdown
## Show Summary

### Workload
TPC-DS Data Loading SF=1
* Type: tpcds
* Duration: 375s 
* Code: 1782732401
* This includes the reading queries of TPC-DS.
* This imports TPC-DS data sets.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782732401 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:269230
  * datadisk:5747
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782732401

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      205.00 |           0.00 |            0.00 |         70.00 |          133.00 |              1 |           0 |             | None           |             0 | False         |               17.56 |

### Monitoring

### Loading phase: SUT deployment

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |       110.34 |      1.88 |           2.80 |                  5.48 |

### Loading phase: component data generator

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |        11.57 |      0.21 |           0.00 |                  1.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
```

docs_tpcds_postgresql_load.log
```markdown
## Show Summary

### Workload
TPC-DS Data Loading SF=1
* Type: tpcds
* Duration: 375s 
* Code: 1782732401
* This includes the reading queries of TPC-DS.
* This imports TPC-DS data sets.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782732401 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:269230
  * datadisk:5747
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782732401

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      205.00 |           0.00 |            0.00 |         70.00 |          133.00 |              1 |           0 |             | None           |             0 | False         |               17.56 |

### Monitoring

### Loading phase: SUT deployment

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |       110.34 |      1.88 |           2.80 |                  5.48 |

### Loading phase: component data generator

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |        11.57 |      0.21 |           0.00 |                  1.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
```

### Start DBMS and Load Data and Run Workload

Loads TPC-DS data and runs all 99 queries.
Some queries may fail on certain DBMS (e.g., Q90 raises a division-by-zero on PostgreSQL at SF=1); these are flagged in the **Errors** section and in **Tests**.

```bash
bexhoma tpcds \
  -dbms PostgreSQL \
  -nlp 1 \
  -nlt 1 \
  -nbp 1 \
  -nbt 64 \
  -xii -xic -xis \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -ss \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_postgresql_run.log
```

docs_tpcds_postgresql_run.log
```markdown
## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 549s 
* Code: 1782732822
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:269230
  * datadisk:5747
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782732822

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      196.00 |           1.00 |            0.00 |         61.00 |          132.00 |              1 |           0 |             | None           |             0 | False         |               18.37 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |        180 |            0.36 |            10101.22 |           1980.00 |          -1 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |        180 |            0.36 |            10101.22 |           1980.00 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   PostgreSQL-1-1-1-1-1 |
|:--------------|-----------------------:|
| TPC-DS Q1     |                 156.58 |
| TPC-DS Q2     |                 314.42 |
| TPC-DS Q3     |                 191.80 |
| TPC-DS Q4     |                8868.43 |
| TPC-DS Q5     |                 496.68 |
| TPC-DS Q6     |               52884.13 |
| TPC-DS Q7     |                 386.10 |
| TPC-DS Q8     |                  69.72 |
| TPC-DS Q9     |                2538.50 |
| TPC-DS Q10    |                1204.19 |
| TPC-DS Q11    |                5301.77 |
| TPC-DS Q12    |                  71.63 |
| TPC-DS Q13    |                 637.11 |
| TPC-DS Q14a+b |                2083.80 |
| TPC-DS Q15    |                 119.24 |
| TPC-DS Q16    |                 210.36 |
| TPC-DS Q17    |                 320.69 |
| TPC-DS Q18    |                 441.67 |
| TPC-DS Q19    |                 164.51 |
| TPC-DS Q20    |                 111.88 |
| TPC-DS Q21    |                 228.09 |
| TPC-DS Q22    |                3486.12 |
| TPC-DS Q23a+b |                5475.90 |
| TPC-DS Q24a+b |                  69.09 |
| TPC-DS Q25    |                 332.17 |
| TPC-DS Q26    |                 265.65 |
| TPC-DS Q27    |                  35.78 |
| TPC-DS Q28    |                 860.33 |
| TPC-DS Q29    |                 357.66 |
| TPC-DS Q30    |                8799.76 |
| TPC-DS Q31    |                1574.81 |
| TPC-DS Q32    |                  98.17 |
| TPC-DS Q33    |                 416.25 |
| TPC-DS Q34    |                  36.18 |
| TPC-DS Q35    |                1697.73 |
| TPC-DS Q36    |                  36.69 |
| TPC-DS Q37    |                 314.84 |
| TPC-DS Q38    |                1843.75 |
| TPC-DS Q39a+b |                3000.19 |
| TPC-DS Q40    |                 138.17 |
| TPC-DS Q41    |                 816.26 |
| TPC-DS Q42    |                  96.10 |
| TPC-DS Q43    |                  35.90 |
| TPC-DS Q44    |                   3.27 |
| TPC-DS Q45    |                  96.50 |
| TPC-DS Q46    |                  43.53 |
| TPC-DS Q47    |                1638.26 |
| TPC-DS Q48    |                 657.10 |
| TPC-DS Q49    |                 488.88 |
| TPC-DS Q50    |                 496.86 |
| TPC-DS Q51    |                 828.76 |
| TPC-DS Q52    |                  95.67 |
| TPC-DS Q53    |                 127.38 |
| TPC-DS Q54    |                  95.76 |
| TPC-DS Q55    |                  93.88 |
| TPC-DS Q56    |                 382.90 |
| TPC-DS Q57    |                 849.61 |
| TPC-DS Q58    |                 422.68 |
| TPC-DS Q59    |                 444.00 |
| TPC-DS Q60    |                 449.66 |
| TPC-DS Q61    |                 113.07 |
| TPC-DS Q62    |                 116.52 |
| TPC-DS Q63    |                 118.67 |
| TPC-DS Q64    |                 694.34 |
| TPC-DS Q65    |                 582.49 |
| TPC-DS Q66    |                 222.89 |
| TPC-DS Q67    |                2969.22 |
| TPC-DS Q68    |                  49.39 |
| TPC-DS Q69    |                 286.52 |
| TPC-DS Q70    |                 388.63 |
| TPC-DS Q71    |                 309.09 |
| TPC-DS Q72    |                 989.17 |
| TPC-DS Q73    |                  36.33 |
| TPC-DS Q74    |                1338.85 |
| TPC-DS Q75    |                 986.15 |
| TPC-DS Q76    |                 166.71 |
| TPC-DS Q77    |                 402.34 |
| TPC-DS Q78    |                1646.83 |
| TPC-DS Q79    |                 182.27 |
| TPC-DS Q80    |                 569.04 |
| TPC-DS Q81    |               39619.65 |
| TPC-DS Q82    |                 597.08 |
| TPC-DS Q83    |                 101.16 |
| TPC-DS Q84    |                  94.59 |
| TPC-DS Q85    |                 363.29 |
| TPC-DS Q86    |                 191.79 |
| TPC-DS Q87    |                1471.58 |
| TPC-DS Q88    |                3002.34 |
| TPC-DS Q89    |                 129.67 |
| TPC-DS Q90    |                 126.16 |
| TPC-DS Q91    |                  98.50 |
| TPC-DS Q92    |                  55.46 |
| TPC-DS Q93    |                 216.40 |
| TPC-DS Q94    |                 172.84 |
| TPC-DS Q95    |                3064.01 |
| TPC-DS Q96    |                  92.19 |
| TPC-DS Q97    |                 387.90 |
| TPC-DS Q98    |                 195.47 |
| TPC-DS Q99    |                 168.06 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       105.72 |      1.53 |           2.81 |                  5.50 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         6.64 |      0.22 |           0.00 |                  0.61 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       252.87 |      2.22 |           3.00 |                  5.68 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        13.64 |      0.02 |           0.28 |                  0.28 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```

docs_tpcds_postgresql_run.log
```markdown
## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 549s 
* Code: 1782732822
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:269230
  * datadisk:5747
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782732822

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      196.00 |           1.00 |            0.00 |         61.00 |          132.00 |              1 |           0 |             | None           |             0 | False         |               18.37 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |        180 |            0.36 |            10101.22 |           1980.00 |          -1 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |        180 |            0.36 |            10101.22 |           1980.00 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   PostgreSQL-1-1-1-1-1 |
|:--------------|-----------------------:|
| TPC-DS Q1     |                 156.58 |
| TPC-DS Q2     |                 314.42 |
| TPC-DS Q3     |                 191.80 |
| TPC-DS Q4     |                8868.43 |
| TPC-DS Q5     |                 496.68 |
| TPC-DS Q6     |               52884.13 |
| TPC-DS Q7     |                 386.10 |
| TPC-DS Q8     |                  69.72 |
| TPC-DS Q9     |                2538.50 |
| TPC-DS Q10    |                1204.19 |
| TPC-DS Q11    |                5301.77 |
| TPC-DS Q12    |                  71.63 |
| TPC-DS Q13    |                 637.11 |
| TPC-DS Q14a+b |                2083.80 |
| TPC-DS Q15    |                 119.24 |
| TPC-DS Q16    |                 210.36 |
| TPC-DS Q17    |                 320.69 |
| TPC-DS Q18    |                 441.67 |
| TPC-DS Q19    |                 164.51 |
| TPC-DS Q20    |                 111.88 |
| TPC-DS Q21    |                 228.09 |
| TPC-DS Q22    |                3486.12 |
| TPC-DS Q23a+b |                5475.90 |
| TPC-DS Q24a+b |                  69.09 |
| TPC-DS Q25    |                 332.17 |
| TPC-DS Q26    |                 265.65 |
| TPC-DS Q27    |                  35.78 |
| TPC-DS Q28    |                 860.33 |
| TPC-DS Q29    |                 357.66 |
| TPC-DS Q30    |                8799.76 |
| TPC-DS Q31    |                1574.81 |
| TPC-DS Q32    |                  98.17 |
| TPC-DS Q33    |                 416.25 |
| TPC-DS Q34    |                  36.18 |
| TPC-DS Q35    |                1697.73 |
| TPC-DS Q36    |                  36.69 |
| TPC-DS Q37    |                 314.84 |
| TPC-DS Q38    |                1843.75 |
| TPC-DS Q39a+b |                3000.19 |
| TPC-DS Q40    |                 138.17 |
| TPC-DS Q41    |                 816.26 |
| TPC-DS Q42    |                  96.10 |
| TPC-DS Q43    |                  35.90 |
| TPC-DS Q44    |                   3.27 |
| TPC-DS Q45    |                  96.50 |
| TPC-DS Q46    |                  43.53 |
| TPC-DS Q47    |                1638.26 |
| TPC-DS Q48    |                 657.10 |
| TPC-DS Q49    |                 488.88 |
| TPC-DS Q50    |                 496.86 |
| TPC-DS Q51    |                 828.76 |
| TPC-DS Q52    |                  95.67 |
| TPC-DS Q53    |                 127.38 |
| TPC-DS Q54    |                  95.76 |
| TPC-DS Q55    |                  93.88 |
| TPC-DS Q56    |                 382.90 |
| TPC-DS Q57    |                 849.61 |
| TPC-DS Q58    |                 422.68 |
| TPC-DS Q59    |                 444.00 |
| TPC-DS Q60    |                 449.66 |
| TPC-DS Q61    |                 113.07 |
| TPC-DS Q62    |                 116.52 |
| TPC-DS Q63    |                 118.67 |
| TPC-DS Q64    |                 694.34 |
| TPC-DS Q65    |                 582.49 |
| TPC-DS Q66    |                 222.89 |
| TPC-DS Q67    |                2969.22 |
| TPC-DS Q68    |                  49.39 |
| TPC-DS Q69    |                 286.52 |
| TPC-DS Q70    |                 388.63 |
| TPC-DS Q71    |                 309.09 |
| TPC-DS Q72    |                 989.17 |
| TPC-DS Q73    |                  36.33 |
| TPC-DS Q74    |                1338.85 |
| TPC-DS Q75    |                 986.15 |
| TPC-DS Q76    |                 166.71 |
| TPC-DS Q77    |                 402.34 |
| TPC-DS Q78    |                1646.83 |
| TPC-DS Q79    |                 182.27 |
| TPC-DS Q80    |                 569.04 |
| TPC-DS Q81    |               39619.65 |
| TPC-DS Q82    |                 597.08 |
| TPC-DS Q83    |                 101.16 |
| TPC-DS Q84    |                  94.59 |
| TPC-DS Q85    |                 363.29 |
| TPC-DS Q86    |                 191.79 |
| TPC-DS Q87    |                1471.58 |
| TPC-DS Q88    |                3002.34 |
| TPC-DS Q89    |                 129.67 |
| TPC-DS Q90    |                 126.16 |
| TPC-DS Q91    |                  98.50 |
| TPC-DS Q92    |                  55.46 |
| TPC-DS Q93    |                 216.40 |
| TPC-DS Q94    |                 172.84 |
| TPC-DS Q95    |                3064.01 |
| TPC-DS Q96    |                  92.19 |
| TPC-DS Q97    |                 387.90 |
| TPC-DS Q98    |                 195.47 |
| TPC-DS Q99    |                 168.06 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       105.72 |      1.53 |           2.81 |                  5.50 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         6.64 |      0.22 |           0.00 |                  0.61 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       252.87 |      2.22 |           3.00 |                  5.68 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        13.64 |      0.02 |           0.28 |                  0.28 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```

The **Execution** section reports per-query latency for all 99 TPC-DS queries and the same Power@Size / Throughput@Size metrics as TPC-H.
