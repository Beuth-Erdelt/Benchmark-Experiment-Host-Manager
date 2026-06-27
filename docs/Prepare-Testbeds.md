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
* Duration: 163s 
* Code: 1782304165
* Start DBMS and do not load data.
* This just starts a SUT.
  * Workload is 'C'.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 10Gi.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782304165 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220502
  * datadisk:39
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782304165

### Tests
```

docs_ycsb_postgresql_start.log
```markdown
## Show Summary

### Workload
YCSB Start DBMS
* Type: ycsb
* Duration: 163s 
* Code: 1782304165
* Start DBMS and do not load data.
* This just starts a SUT.
  * Workload is 'C'.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 10Gi.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782304165 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220502
  * datadisk:39
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782304165

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
* Duration: 339s 
* Code: 1782304350
* YCSB driver runs the experiment.
* This imports YCSB data sets.
  * Workload is 'C'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Target is based on multiples of '16384'.
  * Factors for loading are [1].
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 10Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782304350 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:222854
  * datadisk:2391
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782304350

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| PostgreSQL-1-1-0-1-1 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.95 |                61276.00 |            125000.00 |                              1477.00 | 1.00 |               58.75 |
| PostgreSQL-1-1-0-1-2 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.98 |                61275.00 |            125000.00 |                              1497.00 | 1.00 |               58.75 |
| PostgreSQL-1-1-0-1-3 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.08 |                61272.00 |            125000.00 |                              1497.00 | 1.00 |               58.75 |
| PostgreSQL-1-1-0-1-4 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.18 |                61269.00 |            125000.00 |                              1495.00 | 1.00 |               58.76 |
| PostgreSQL-1-1-0-1-5 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.28 |                61266.00 |            125000.00 |                              1545.00 | 1.00 |               58.76 |
| PostgreSQL-1-1-0-1-6 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.22 |                61268.00 |            125000.00 |                              1497.00 | 1.00 |               58.76 |
| PostgreSQL-1-1-0-1-7 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.62 |                61256.00 |            125000.00 |                              1506.00 | 1.00 |               58.77 |
| PostgreSQL-1-1-0-1-8 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.38 |                61263.00 |            125000.00 |                              1508.00 | 1.00 |               58.76 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 16384.00 |        8.00 |         0.00 | 1.00 |               58.75 |                        16321.70 |                61276.00 |           1000000.00 |                              1502.75 |

### Monitoring

### Loading phase: SUT deployment

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |       241.19 |      3.91 |           1.71 |                  2.70 |

### Loading phase: component loader

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |        82.91 |      1.44 |           0.11 |                  0.11 |

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
* Duration: 339s 
* Code: 1782304350
* YCSB driver runs the experiment.
* This imports YCSB data sets.
  * Workload is 'C'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Target is based on multiples of '16384'.
  * Factors for loading are [1].
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 10Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782304350 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:222854
  * datadisk:2391
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782304350

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| PostgreSQL-1-1-0-1-1 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.95 |                61276.00 |            125000.00 |                              1477.00 | 1.00 |               58.75 |
| PostgreSQL-1-1-0-1-2 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.98 |                61275.00 |            125000.00 |                              1497.00 | 1.00 |               58.75 |
| PostgreSQL-1-1-0-1-3 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.08 |                61272.00 |            125000.00 |                              1497.00 | 1.00 |               58.75 |
| PostgreSQL-1-1-0-1-4 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.18 |                61269.00 |            125000.00 |                              1495.00 | 1.00 |               58.76 |
| PostgreSQL-1-1-0-1-5 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.28 |                61266.00 |            125000.00 |                              1545.00 | 1.00 |               58.76 |
| PostgreSQL-1-1-0-1-6 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.22 |                61268.00 |            125000.00 |                              1497.00 | 1.00 |               58.76 |
| PostgreSQL-1-1-0-1-7 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.62 |                61256.00 |            125000.00 |                              1506.00 | 1.00 |               58.77 |
| PostgreSQL-1-1-0-1-8 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.38 |                61263.00 |            125000.00 |                              1508.00 | 1.00 |               58.76 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 16384.00 |        8.00 |         0.00 | 1.00 |               58.75 |                        16321.70 |                61276.00 |           1000000.00 |                              1502.75 |

### Monitoring

### Loading phase: SUT deployment

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |       241.19 |      3.91 |           1.71 |                  2.70 |

### Loading phase: component loader

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |        82.91 |      1.44 |           0.11 |                  0.11 |

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
* Duration: 429s 
* Code: 1782304720
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
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 10Gi.
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
  * disk:222854
  * datadisk:2391
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782304720

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (8 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (8 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| PostgreSQL-1-1-0-1-1 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.55 |                61258.00 |            125000.00 |                              1509.00 | 1.00 |               58.77 |
| PostgreSQL-1-1-0-1-2 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.98 |                61275.00 |            125000.00 |                              1516.00 | 1.00 |               58.75 |
| PostgreSQL-1-1-0-1-3 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.35 |                61264.00 |            125000.00 |                              1511.00 | 1.00 |               58.76 |
| PostgreSQL-1-1-0-1-4 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.42 |                61262.00 |            125000.00 |                              1484.00 | 1.00 |               58.76 |
| PostgreSQL-1-1-0-1-5 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.45 |                61261.00 |            125000.00 |                              1515.00 | 1.00 |               58.76 |
| PostgreSQL-1-1-0-1-6 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.15 |                61270.00 |            125000.00 |                              1507.00 | 1.00 |               58.76 |
| PostgreSQL-1-1-0-1-7 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.12 |                61271.00 |            125000.00 |                              1468.00 | 1.00 |               58.76 |
| PostgreSQL-1-1-0-1-8 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.25 |                61267.00 |            125000.00 |                              1574.00 | 1.00 |               58.76 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 16384.00 |        8.00 |         0.00 | 1.00 |               58.75 |                        16322.27 |                61275.00 |           1000000.00 |                              1510.50 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|
| PostgreSQL-1-1-1-1-5 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       5 |         8 |     2048 |           8 |            0 |                         2040.22 |                61268.00 |             125000 |                             632.00 |
| PostgreSQL-1-1-1-1-7 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       7 |         8 |     2048 |           8 |            0 |                         2040.22 |                61268.00 |             125000 |                             726.00 |
| PostgreSQL-1-1-1-1-8 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       8 |         8 |     2048 |           8 |            0 |                         2040.05 |                61273.00 |             125000 |                             699.00 |
| PostgreSQL-1-1-1-1-3 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       3 |         8 |     2048 |           8 |            0 |                         2040.62 |                61256.00 |             125000 |                             693.00 |
| PostgreSQL-1-1-1-1-4 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       4 |         8 |     2048 |           8 |            0 |                         2040.45 |                61261.00 |             125000 |                             757.00 |
| PostgreSQL-1-1-1-1-6 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       6 |         8 |     2048 |           8 |            0 |                         2040.32 |                61265.00 |             125000 |                             677.00 |
| PostgreSQL-1-1-1-1-2 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       2 |         8 |     2048 |           8 |            0 |                         2040.38 |                61263.00 |             125000 |                             646.00 |
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |         8 |     2048 |           8 |            0 |                         2040.55 |                61258.00 |             125000 |                             656.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        64 |    16384 |               1 |           8 |            0 |                        16322.80 |                61273.00 |            1000000 |                             757.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       238.22 |      3.89 |           1.57 |                  2.66 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        67.39 |      1.94 |           0.11 |                  0.11 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       120.71 |      2.22 |           1.85 |                  3.02 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        70.74 |      1.28 |           0.10 |                  0.11 |

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
* Duration: 429s 
* Code: 1782304720
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
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 10Gi.
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
  * disk:222854
  * datadisk:2391
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782304720

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (8 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (8 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| PostgreSQL-1-1-0-1-1 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.55 |                61258.00 |            125000.00 |                              1509.00 | 1.00 |               58.77 |
| PostgreSQL-1-1-0-1-2 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.98 |                61275.00 |            125000.00 |                              1516.00 | 1.00 |               58.75 |
| PostgreSQL-1-1-0-1-3 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.35 |                61264.00 |            125000.00 |                              1511.00 | 1.00 |               58.76 |
| PostgreSQL-1-1-0-1-4 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.42 |                61262.00 |            125000.00 |                              1484.00 | 1.00 |               58.76 |
| PostgreSQL-1-1-0-1-5 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.45 |                61261.00 |            125000.00 |                              1515.00 | 1.00 |               58.76 |
| PostgreSQL-1-1-0-1-6 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.15 |                61270.00 |            125000.00 |                              1507.00 | 1.00 |               58.76 |
| PostgreSQL-1-1-0-1-7 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.12 |                61271.00 |            125000.00 |                              1468.00 | 1.00 |               58.76 |
| PostgreSQL-1-1-0-1-8 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.25 |                61267.00 |            125000.00 |                              1574.00 | 1.00 |               58.76 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 16384.00 |        8.00 |         0.00 | 1.00 |               58.75 |                        16322.27 |                61275.00 |           1000000.00 |                              1510.50 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|
| PostgreSQL-1-1-1-1-5 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       5 |         8 |     2048 |           8 |            0 |                         2040.22 |                61268.00 |             125000 |                             632.00 |
| PostgreSQL-1-1-1-1-7 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       7 |         8 |     2048 |           8 |            0 |                         2040.22 |                61268.00 |             125000 |                             726.00 |
| PostgreSQL-1-1-1-1-8 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       8 |         8 |     2048 |           8 |            0 |                         2040.05 |                61273.00 |             125000 |                             699.00 |
| PostgreSQL-1-1-1-1-3 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       3 |         8 |     2048 |           8 |            0 |                         2040.62 |                61256.00 |             125000 |                             693.00 |
| PostgreSQL-1-1-1-1-4 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       4 |         8 |     2048 |           8 |            0 |                         2040.45 |                61261.00 |             125000 |                             757.00 |
| PostgreSQL-1-1-1-1-6 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       6 |         8 |     2048 |           8 |            0 |                         2040.32 |                61265.00 |             125000 |                             677.00 |
| PostgreSQL-1-1-1-1-2 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       2 |         8 |     2048 |           8 |            0 |                         2040.38 |                61263.00 |             125000 |                             646.00 |
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |         8 |     2048 |           8 |            0 |                         2040.55 |                61258.00 |             125000 |                             656.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        64 |    16384 |               1 |           8 |            0 |                        16322.80 |                61273.00 |            1000000 |                             757.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       238.22 |      3.89 |           1.57 |                  2.66 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        67.39 |      1.94 |           0.11 |                  0.11 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       120.71 |      2.22 |           1.85 |                  3.02 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        70.74 |      1.28 |           0.10 |                  0.11 |

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
* Duration: 197s 
* Code: 1782305186
* Start DBMS and do not load data.
* This just starts a SUT.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 10Gi.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782305186 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220502
  * datadisk:39
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782305186
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
* Duration: 197s 
* Code: 1782305186
* Start DBMS and do not load data.
* This just starts a SUT.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 10Gi.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782305186 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220502
  * datadisk:39
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782305186
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
* Duration: 237s 
* Code: 1782380192
* Benchbase runs a TPC-C experiment.
* This imports a Benchbase data set.
  * Benchbase data is generated and loaded using several threads. Scaling factor is 1. Target is based on multiples of '1024'.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [64] threads, split into [8] pods.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782380192 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220803
  * datadisk:330
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782380192
    * TENANT_VOL:False

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |       65.00 |           1.00 |            0.00 |         25.00 |           39.00 |              1 |           1 |             |                |             0 | False         |               55.38 |

### Monitoring

### Loading phase: SUT deployment

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |        20.70 |      0.60 |           0.50 |                  0.65 |

### Loading phase: component loader

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |         7.00 |      0.00 |           0.22 |                  0.22 |

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
* Duration: 237s 
* Code: 1782380192
* Benchbase runs a TPC-C experiment.
* This imports a Benchbase data set.
  * Benchbase data is generated and loaded using several threads. Scaling factor is 1. Target is based on multiples of '1024'.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [64] threads, split into [8] pods.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782380192 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220803
  * datadisk:330
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782380192
    * TENANT_VOL:False

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |       65.00 |           1.00 |            0.00 |         25.00 |           39.00 |              1 |           1 |             |                |             0 | False         |               55.38 |

### Monitoring

### Loading phase: SUT deployment

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |        20.70 |      0.60 |           0.50 |                  0.65 |

### Loading phase: component loader

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |         7.00 |      0.00 |           0.22 |                  0.22 |

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
* Duration: 611s 
* Code: 1782305705
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 10Gi.
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
  * disk:220793
  * datadisk:330
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782305705
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
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       1 |           0 | 300.00 |            0 |                          52.83 |                       52.35 |         0.00 |                                                     755417.00 |                                             151346.00 |
| PostgreSQL-1-1-1-1-2 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       2 |           0 | 300.00 |            0 |                          53.23 |                       52.70 |         0.00 |                                                     755040.00 |                                             150160.00 |
| PostgreSQL-1-1-1-1-3 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       3 |           0 | 300.00 |            0 |                          50.55 |                       50.09 |         0.00 |                                                     784752.00 |                                             157853.00 |
| PostgreSQL-1-1-1-1-4 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       4 |           0 | 300.00 |            0 |                          52.24 |                       51.75 |         0.00 |                                                     760276.00 |                                             153034.00 |
| PostgreSQL-1-1-1-1-5 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       5 |           0 | 300.00 |            2 |                          51.42 |                       51.00 |         0.00 |                                                     768047.00 |                                             155439.00 |
| PostgreSQL-1-1-1-1-6 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       6 |           0 | 300.00 |            1 |                          51.52 |                       51.08 |         0.00 |                                                     780820.00 |                                             154906.00 |
| PostgreSQL-1-1-1-1-7 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       7 |           0 | 300.00 |            0 |                          51.63 |                       51.27 |         0.00 |                                                     774322.00 |                                             154791.00 |
| PostgreSQL-1-1-1-1-8 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       8 |           0 | 300.00 |            0 |                          52.21 |                       51.68 |         0.00 |                                                     769977.00 |                                             152923.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |          64 |     1024 |               1 |           8 |           0 | 300.00 |            3 |                         415.62 |                      411.92 |         0.00 |                                                     784752.00 |                                             153806.50 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        19.28 |      0.85 |           0.51 |                  0.66 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         7.32 |      0.00 |           0.24 |                  0.24 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       712.35 |      2.66 |           0.90 |                  1.18 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       196.11 |      1.73 |           0.23 |                  0.23 |

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
* Duration: 611s 
* Code: 1782305705
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 10Gi.
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
  * disk:220793
  * datadisk:330
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782305705
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
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       1 |           0 | 300.00 |            0 |                          52.83 |                       52.35 |         0.00 |                                                     755417.00 |                                             151346.00 |
| PostgreSQL-1-1-1-1-2 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       2 |           0 | 300.00 |            0 |                          53.23 |                       52.70 |         0.00 |                                                     755040.00 |                                             150160.00 |
| PostgreSQL-1-1-1-1-3 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       3 |           0 | 300.00 |            0 |                          50.55 |                       50.09 |         0.00 |                                                     784752.00 |                                             157853.00 |
| PostgreSQL-1-1-1-1-4 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       4 |           0 | 300.00 |            0 |                          52.24 |                       51.75 |         0.00 |                                                     760276.00 |                                             153034.00 |
| PostgreSQL-1-1-1-1-5 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       5 |           0 | 300.00 |            2 |                          51.42 |                       51.00 |         0.00 |                                                     768047.00 |                                             155439.00 |
| PostgreSQL-1-1-1-1-6 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       6 |           0 | 300.00 |            1 |                          51.52 |                       51.08 |         0.00 |                                                     780820.00 |                                             154906.00 |
| PostgreSQL-1-1-1-1-7 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       7 |           0 | 300.00 |            0 |                          51.63 |                       51.27 |         0.00 |                                                     774322.00 |                                             154791.00 |
| PostgreSQL-1-1-1-1-8 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       8 |           0 | 300.00 |            0 |                          52.21 |                       51.68 |         0.00 |                                                     769977.00 |                                             152923.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |          64 |     1024 |               1 |           8 |           0 | 300.00 |            3 |                         415.62 |                      411.92 |         0.00 |                                                     784752.00 |                                             153806.50 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        19.28 |      0.85 |           0.51 |                  0.66 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         7.32 |      0.00 |           0.24 |                  0.24 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       712.35 |      2.66 |           0.90 |                  1.18 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       196.11 |      1.73 |           0.23 |                  0.23 |

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
* Duration: 164s 
* Code: 1782378815
* Start DBMS and do not load data.
* This just starts a SUT.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * SUT is fixed to cl-worker38.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782378815 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220512
  * datadisk:39
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782378815

### Tests
```

docs_hammerdb_postgresql_start.log
```markdown
## Show Summary

### Workload
HammerDB Start DBMS
* Type: tpcc
* Duration: 164s 
* Code: 1782378815
* Start DBMS and do not load data.
* This just starts a SUT.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * SUT is fixed to cl-worker38.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782378815 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220512
  * datadisk:39
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782378815

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
* Duration: 264s 
* Code: 1782379011
* HammerDB runs the benchmark.
* This imports TPC-C data sets.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 1.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782379011 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220752
  * datadisk:280
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782379011

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |       56.00 |           0.00 |            0.00 |         21.00 |           35.00 |              1 |           1 |             | None           |             0 | False         |               64.29 |

### Monitoring

### Loading phase: SUT deployment

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |         0.14 |      0.01 |           0.40 |                  0.44 |

### Loading phase: component loader

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |         0.02 |      0.00 |           0.00 |                  0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
```

docs_hammerdb_postgresql_load.log
```markdown
## Show Summary

### Workload
HammerDB Data Loading SF=1 (warehouses for TPC-C)
* Type: tpcc
* Duration: 264s 
* Code: 1782379011
* HammerDB runs the benchmark.
* This imports TPC-C data sets.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 1.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782379011 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220752
  * datadisk:280
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782379011

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |       56.00 |           0.00 |            0.00 |         21.00 |           35.00 |              1 |           1 |             | None           |             0 | False         |               64.29 |

### Monitoring

### Loading phase: SUT deployment

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |         0.14 |      0.01 |           0.40 |                  0.44 |

### Loading phase: component loader

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |         0.02 |      0.00 |           0.00 |                  0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
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
* Duration: 729s 
* Code: 1782379306
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 1. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.10.0.
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
  * disk:220752
  * datadisk:280
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782379306

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |       62.00 |           1.00 |            0.00 |         26.00 |           35.00 |              1 |           1 |             | None           |             0 | False         |               58.06 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |    TPM |   efficiency |   duration |   errors |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|-------:|-------------:|-----------:|---------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |       64 |        1 |               1 |       1 |  43822 | 101042 |         0.00 |          5 |        0 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   efficiency |     NOPM |       TPM |   duration |   errors |
|:-----------------|:-----------------|-----------------:|---------:|---------:|----------------:|------------:|-------------:|---------:|----------:|-----------:|---------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |       64 |        1 |               1 |           1 |         0.00 | 43822.00 | 101042.00 |          5 |        0 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         1.55 |      0.05 |           0.44 |                  0.49 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.02 |      0.00 |           0.00 |                  0.00 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      3336.04 |      8.76 |           1.72 |                  2.49 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        97.18 |      0.29 |           0.23 |                  0.24 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
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
* Duration: 729s 
* Code: 1782379306
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 1. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.10.0.
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
  * disk:220752
  * datadisk:280
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782379306

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |       62.00 |           1.00 |            0.00 |         26.00 |           35.00 |              1 |           1 |             | None           |             0 | False         |               58.06 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |    TPM |   efficiency |   duration |   errors |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|-------:|-------------:|-----------:|---------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |       64 |        1 |               1 |       1 |  43822 | 101042 |         0.00 |          5 |        0 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   efficiency |     NOPM |       TPM |   duration |   errors |
|:-----------------|:-----------------|-----------------:|---------:|---------:|----------------:|------------:|-------------:|---------:|----------:|-----------:|---------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |       64 |        1 |               1 |           1 |         0.00 | 43822.00 | 101042.00 |          5 |        0 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         1.55 |      0.05 |           0.44 |                  0.49 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.02 |      0.00 |           0.00 |                  0.00 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      3336.04 |      8.76 |           1.72 |                  2.49 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        97.18 |      0.29 |           0.23 |                  0.24 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
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
* Duration: 192s 
* Code: 1782307622
* Start DBMS and do not load data.
* This just starts a SUT.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 10Gi.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782307622 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220503
  * datadisk:39
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782307622

### Tests
```

docs_tpch_postgresql_start.log
```markdown
## Show Summary

### Workload
TPC-H Start DBMS
* Type: tpch
* Duration: 192s 
* Code: 1782307622
* Start DBMS and do not load data.
* This just starts a SUT.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 10Gi.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782307622 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220503
  * datadisk:39
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782307622

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
* Duration: 269s 
* Code: 1782307837
* This includes the reading queries of TPC-H.
* This imports TPC-H data sets.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 10Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782307837 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:223221
  * datadisk:2757
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782307837

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      111.00 |           0.00 |            0.00 |         29.00 |           81.00 |              1 |           0 |             |                |             0 | False         |               32.43 |

### Monitoring

### Loading phase: SUT deployment

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |        16.27 |      0.33 |           0.50 |                  1.72 |

### Loading phase: component data generator

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |         0.02 |      0.00 |           0.00 |                  0.00 |

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
* Duration: 269s 
* Code: 1782307837
* This includes the reading queries of TPC-H.
* This imports TPC-H data sets.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 10Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782307837 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:223221
  * datadisk:2757
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782307837

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      111.00 |           0.00 |            0.00 |         29.00 |           81.00 |              1 |           0 |             |                |             0 | False         |               32.43 |

### Monitoring

### Loading phase: SUT deployment

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |        16.27 |      0.33 |           0.50 |                  1.72 |

### Loading phase: component data generator

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |         0.02 |      0.00 |           0.00 |                  0.00 |

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
* Duration: 351s 
* Code: 1782308137
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 10Gi.
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
  * disk:223221
  * datadisk:2757
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782308137

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      110.00 |           0.00 |            0.00 |         29.00 |           80.00 |              1 |           0 |             |                |             0 | False         |               32.73 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         11 |            0.29 |            12590.58 |           7200.00 |           0 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         11 |            0.29 |            12590.58 |           7200.00 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |
|:----------------------------------------------------|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                1162.36 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 202.23 |
| Shipping Priority (TPC-H Q3)                        |                 304.63 |
| Order Priority Checking Query (TPC-H Q4)            |                 131.74 |
| Local Supplier Volume (TPC-H Q5)                    |                 281.63 |
| Forecasting Revenue Change (TPC-H Q6)               |                 190.26 |
| Volume Shipping Query (TPC-H Q7)                    |                 377.36 |
| National Market Share (TPC-H Q8)                    |                 193.01 |
| Product Type Profit Measure (TPC-H Q9)              |                 557.27 |
| Returned Item Reporting Query (TPC-H Q10)           |                 298.93 |
| Important Stock Identification (TPC-H Q11)          |                  90.60 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 279.81 |
| Customer Distribution (TPC-H Q13)                   |                1444.53 |
| Promotion Effect Query (TPC-H Q14)                  |                 309.12 |
| Top Supplier Query (TPC-H Q15)                      |                 203.16 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 226.64 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                 633.14 |
| Large Volume Customer (TPC-H Q18)                   |                2882.49 |
| Discounted Revenue (TPC-H Q19)                      |                  54.50 |
| Potential Part Promotion (TPC-H Q20)                |                 133.07 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 271.66 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  94.89 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        38.52 |      0.67 |           2.05 |                  3.60 |

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
| PostgreSQL-1-1-1-1 |         2.31 |      0.67 |           2.05 |                  3.60 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.02 |      0.00 |           0.00 |                  0.00 |

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

docs_tpch_postgresql_run.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 351s 
* Code: 1782308137
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 10Gi.
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
  * disk:223221
  * datadisk:2757
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782308137

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      110.00 |           0.00 |            0.00 |         29.00 |           80.00 |              1 |           0 |             |                |             0 | False         |               32.73 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         11 |            0.29 |            12590.58 |           7200.00 |           0 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         11 |            0.29 |            12590.58 |           7200.00 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |
|:----------------------------------------------------|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                1162.36 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 202.23 |
| Shipping Priority (TPC-H Q3)                        |                 304.63 |
| Order Priority Checking Query (TPC-H Q4)            |                 131.74 |
| Local Supplier Volume (TPC-H Q5)                    |                 281.63 |
| Forecasting Revenue Change (TPC-H Q6)               |                 190.26 |
| Volume Shipping Query (TPC-H Q7)                    |                 377.36 |
| National Market Share (TPC-H Q8)                    |                 193.01 |
| Product Type Profit Measure (TPC-H Q9)              |                 557.27 |
| Returned Item Reporting Query (TPC-H Q10)           |                 298.93 |
| Important Stock Identification (TPC-H Q11)          |                  90.60 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 279.81 |
| Customer Distribution (TPC-H Q13)                   |                1444.53 |
| Promotion Effect Query (TPC-H Q14)                  |                 309.12 |
| Top Supplier Query (TPC-H Q15)                      |                 203.16 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 226.64 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                 633.14 |
| Large Volume Customer (TPC-H Q18)                   |                2882.49 |
| Discounted Revenue (TPC-H Q19)                      |                  54.50 |
| Potential Part Promotion (TPC-H Q20)                |                 133.07 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 271.66 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  94.89 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        38.52 |      0.67 |           2.05 |                  3.60 |

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
| PostgreSQL-1-1-1-1 |         2.31 |      0.67 |           2.05 |                  3.60 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.02 |      0.00 |           0.00 |                  0.00 |

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
* Duration: 169s 
* Code: 1782308542
* Start DBMS and do not load data.
* This just starts a SUT.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 10Gi.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782308542 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220503
  * datadisk:39
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782308542

### Tests
```

docs_tpcds_postgresql_start.log
```markdown
## Show Summary

### Workload
TPC-DS Start DBMS
* Type: tpcds
* Duration: 169s 
* Code: 1782308542
* Start DBMS and do not load data.
* This just starts a SUT.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 10Gi.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782308542 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220503
  * datadisk:39
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782308542

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
* Duration: 368s 
* Code: 1782308736
* This includes the reading queries of TPC-DS.
* This imports TPC-DS data sets.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 10Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782308736 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:226210
  * datadisk:5747
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782308736

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      197.00 |           1.00 |            0.00 |         63.00 |          132.00 |              1 |           0 |             | None           |             0 | False         |               18.27 |

### Monitoring

### Loading phase: SUT deployment

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |        98.89 |      1.53 |           2.82 |                  5.50 |

### Loading phase: component data generator

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |         7.82 |      0.17 |           0.00 |                  0.67 |

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
* Duration: 368s 
* Code: 1782308736
* This includes the reading queries of TPC-DS.
* This imports TPC-DS data sets.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 10Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782308736 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:226210
  * datadisk:5747
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782308736

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      197.00 |           1.00 |            0.00 |         63.00 |          132.00 |              1 |           0 |             | None           |             0 | False         |               18.27 |

### Monitoring

### Loading phase: SUT deployment

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |        98.89 |      1.53 |           2.82 |                  5.50 |

### Loading phase: component data generator

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |         7.82 |      0.17 |           0.00 |                  0.67 |

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
* Duration: 585s 
* Code: 1782309137
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 10Gi.
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
  * disk:226210
  * datadisk:5747
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782309137

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      194.00 |           0.00 |            0.00 |         62.00 |          130.00 |              1 |           0 |             | None           |             0 | False         |               18.56 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |        177 |            0.36 |            10054.69 |           2013.56 |          -1 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |        177 |            0.36 |            10054.69 |           2013.56 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   PostgreSQL-1-1-1-1-1 |
|:--------------|-----------------------:|
| TPC-DS Q1     |                 127.73 |
| TPC-DS Q2     |                 312.43 |
| TPC-DS Q3     |                 188.47 |
| TPC-DS Q4     |                8922.19 |
| TPC-DS Q5     |                 530.52 |
| TPC-DS Q6     |               51798.15 |
| TPC-DS Q7     |                 375.14 |
| TPC-DS Q8     |                  69.22 |
| TPC-DS Q9     |                2497.53 |
| TPC-DS Q10    |                1187.07 |
| TPC-DS Q11    |                5421.18 |
| TPC-DS Q12    |                  62.56 |
| TPC-DS Q13    |                 577.65 |
| TPC-DS Q14a+b |                2099.85 |
| TPC-DS Q15    |                 108.23 |
| TPC-DS Q16    |                 182.95 |
| TPC-DS Q17    |                 287.66 |
| TPC-DS Q18    |                 375.59 |
| TPC-DS Q19    |                 166.11 |
| TPC-DS Q20    |                 107.04 |
| TPC-DS Q21    |                 232.32 |
| TPC-DS Q22    |                3949.31 |
| TPC-DS Q23a+b |                5435.30 |
| TPC-DS Q24a+b |                 705.70 |
| TPC-DS Q25    |                 357.89 |
| TPC-DS Q26    |                 263.42 |
| TPC-DS Q27    |                  37.13 |
| TPC-DS Q28    |                 861.96 |
| TPC-DS Q29    |                 355.98 |
| TPC-DS Q30    |                8750.39 |
| TPC-DS Q31    |                1535.26 |
| TPC-DS Q32    |                  77.95 |
| TPC-DS Q33    |                 426.68 |
| TPC-DS Q34    |                  35.09 |
| TPC-DS Q35    |                1366.75 |
| TPC-DS Q36    |                  36.16 |
| TPC-DS Q37    |                 553.56 |
| TPC-DS Q38    |                1381.16 |
| TPC-DS Q39a+b |                2587.64 |
| TPC-DS Q40    |                 131.75 |
| TPC-DS Q41    |                 881.31 |
| TPC-DS Q42    |                 100.36 |
| TPC-DS Q43    |                  34.45 |
| TPC-DS Q44    |                   3.53 |
| TPC-DS Q45    |                  88.03 |
| TPC-DS Q46    |                  43.17 |
| TPC-DS Q47    |                1766.50 |
| TPC-DS Q48    |                 622.78 |
| TPC-DS Q49    |                 482.28 |
| TPC-DS Q50    |                 422.69 |
| TPC-DS Q51    |                 814.58 |
| TPC-DS Q52    |                  93.10 |
| TPC-DS Q53    |                 122.83 |
| TPC-DS Q54    |                  96.51 |
| TPC-DS Q55    |                  94.57 |
| TPC-DS Q56    |                 434.94 |
| TPC-DS Q57    |                 824.05 |
| TPC-DS Q58    |                 421.86 |
| TPC-DS Q59    |                 445.07 |
| TPC-DS Q60    |                 384.17 |
| TPC-DS Q61    |                 172.89 |
| TPC-DS Q62    |                 119.71 |
| TPC-DS Q63    |                 120.33 |
| TPC-DS Q64    |                 670.19 |
| TPC-DS Q65    |                 595.19 |
| TPC-DS Q66    |                 217.19 |
| TPC-DS Q67    |                2897.31 |
| TPC-DS Q68    |                  46.50 |
| TPC-DS Q69    |                 269.83 |
| TPC-DS Q70    |                 383.19 |
| TPC-DS Q71    |                 345.73 |
| TPC-DS Q72    |                 822.10 |
| TPC-DS Q73    |                  37.03 |
| TPC-DS Q74    |                 886.82 |
| TPC-DS Q75    |                1037.75 |
| TPC-DS Q76    |                 162.64 |
| TPC-DS Q77    |                 392.28 |
| TPC-DS Q78    |                1753.25 |
| TPC-DS Q79    |                 179.18 |
| TPC-DS Q80    |                 579.86 |
| TPC-DS Q81    |               38959.51 |
| TPC-DS Q82    |                 806.39 |
| TPC-DS Q83    |                 100.88 |
| TPC-DS Q84    |                  97.10 |
| TPC-DS Q85    |                 347.72 |
| TPC-DS Q86    |                 207.42 |
| TPC-DS Q87    |                1427.97 |
| TPC-DS Q88    |                2984.98 |
| TPC-DS Q89    |                  37.75 |
| TPC-DS Q90    |                 133.71 |
| TPC-DS Q91    |                 154.90 |
| TPC-DS Q92    |                  57.54 |
| TPC-DS Q93    |                 225.38 |
| TPC-DS Q94    |                 169.22 |
| TPC-DS Q95    |                3078.26 |
| TPC-DS Q96    |                 101.50 |
| TPC-DS Q97    |                 384.47 |
| TPC-DS Q98    |                 173.97 |
| TPC-DS Q99    |                 176.20 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        78.34 |      0.87 |           2.17 |                  4.58 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         9.66 |      0.30 |           0.00 |                  0.98 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       240.60 |      2.08 |           3.10 |                  5.79 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        13.15 |      0.43 |           0.30 |                  0.30 |

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
* Duration: 585s 
* Code: 1782309137
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 10Gi.
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
  * disk:226210
  * datadisk:5747
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782309137

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      194.00 |           0.00 |            0.00 |         62.00 |          130.00 |              1 |           0 |             | None           |             0 | False         |               18.56 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |        177 |            0.36 |            10054.69 |           2013.56 |          -1 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |        177 |            0.36 |            10054.69 |           2013.56 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   PostgreSQL-1-1-1-1-1 |
|:--------------|-----------------------:|
| TPC-DS Q1     |                 127.73 |
| TPC-DS Q2     |                 312.43 |
| TPC-DS Q3     |                 188.47 |
| TPC-DS Q4     |                8922.19 |
| TPC-DS Q5     |                 530.52 |
| TPC-DS Q6     |               51798.15 |
| TPC-DS Q7     |                 375.14 |
| TPC-DS Q8     |                  69.22 |
| TPC-DS Q9     |                2497.53 |
| TPC-DS Q10    |                1187.07 |
| TPC-DS Q11    |                5421.18 |
| TPC-DS Q12    |                  62.56 |
| TPC-DS Q13    |                 577.65 |
| TPC-DS Q14a+b |                2099.85 |
| TPC-DS Q15    |                 108.23 |
| TPC-DS Q16    |                 182.95 |
| TPC-DS Q17    |                 287.66 |
| TPC-DS Q18    |                 375.59 |
| TPC-DS Q19    |                 166.11 |
| TPC-DS Q20    |                 107.04 |
| TPC-DS Q21    |                 232.32 |
| TPC-DS Q22    |                3949.31 |
| TPC-DS Q23a+b |                5435.30 |
| TPC-DS Q24a+b |                 705.70 |
| TPC-DS Q25    |                 357.89 |
| TPC-DS Q26    |                 263.42 |
| TPC-DS Q27    |                  37.13 |
| TPC-DS Q28    |                 861.96 |
| TPC-DS Q29    |                 355.98 |
| TPC-DS Q30    |                8750.39 |
| TPC-DS Q31    |                1535.26 |
| TPC-DS Q32    |                  77.95 |
| TPC-DS Q33    |                 426.68 |
| TPC-DS Q34    |                  35.09 |
| TPC-DS Q35    |                1366.75 |
| TPC-DS Q36    |                  36.16 |
| TPC-DS Q37    |                 553.56 |
| TPC-DS Q38    |                1381.16 |
| TPC-DS Q39a+b |                2587.64 |
| TPC-DS Q40    |                 131.75 |
| TPC-DS Q41    |                 881.31 |
| TPC-DS Q42    |                 100.36 |
| TPC-DS Q43    |                  34.45 |
| TPC-DS Q44    |                   3.53 |
| TPC-DS Q45    |                  88.03 |
| TPC-DS Q46    |                  43.17 |
| TPC-DS Q47    |                1766.50 |
| TPC-DS Q48    |                 622.78 |
| TPC-DS Q49    |                 482.28 |
| TPC-DS Q50    |                 422.69 |
| TPC-DS Q51    |                 814.58 |
| TPC-DS Q52    |                  93.10 |
| TPC-DS Q53    |                 122.83 |
| TPC-DS Q54    |                  96.51 |
| TPC-DS Q55    |                  94.57 |
| TPC-DS Q56    |                 434.94 |
| TPC-DS Q57    |                 824.05 |
| TPC-DS Q58    |                 421.86 |
| TPC-DS Q59    |                 445.07 |
| TPC-DS Q60    |                 384.17 |
| TPC-DS Q61    |                 172.89 |
| TPC-DS Q62    |                 119.71 |
| TPC-DS Q63    |                 120.33 |
| TPC-DS Q64    |                 670.19 |
| TPC-DS Q65    |                 595.19 |
| TPC-DS Q66    |                 217.19 |
| TPC-DS Q67    |                2897.31 |
| TPC-DS Q68    |                  46.50 |
| TPC-DS Q69    |                 269.83 |
| TPC-DS Q70    |                 383.19 |
| TPC-DS Q71    |                 345.73 |
| TPC-DS Q72    |                 822.10 |
| TPC-DS Q73    |                  37.03 |
| TPC-DS Q74    |                 886.82 |
| TPC-DS Q75    |                1037.75 |
| TPC-DS Q76    |                 162.64 |
| TPC-DS Q77    |                 392.28 |
| TPC-DS Q78    |                1753.25 |
| TPC-DS Q79    |                 179.18 |
| TPC-DS Q80    |                 579.86 |
| TPC-DS Q81    |               38959.51 |
| TPC-DS Q82    |                 806.39 |
| TPC-DS Q83    |                 100.88 |
| TPC-DS Q84    |                  97.10 |
| TPC-DS Q85    |                 347.72 |
| TPC-DS Q86    |                 207.42 |
| TPC-DS Q87    |                1427.97 |
| TPC-DS Q88    |                2984.98 |
| TPC-DS Q89    |                  37.75 |
| TPC-DS Q90    |                 133.71 |
| TPC-DS Q91    |                 154.90 |
| TPC-DS Q92    |                  57.54 |
| TPC-DS Q93    |                 225.38 |
| TPC-DS Q94    |                 169.22 |
| TPC-DS Q95    |                3078.26 |
| TPC-DS Q96    |                 101.50 |
| TPC-DS Q97    |                 384.47 |
| TPC-DS Q98    |                 173.97 |
| TPC-DS Q99    |                 176.20 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        78.34 |      0.87 |           2.17 |                  4.58 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         9.66 |      0.30 |           0.00 |                  0.98 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       240.60 |      2.08 |           3.10 |                  5.79 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        13.15 |      0.43 |           0.30 |                  0.30 |

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
