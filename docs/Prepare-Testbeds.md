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
The configuration name encodes concurrency and target throughput: `PostgreSQL-<threads>-<pods>-<target>`.

### Start DBMS

Starts PostgreSQL without loading any data.
After this completes you can connect to the instance and run queries manually.

```bash
bexhoma ycsb -ms 1 -tr \
  --dbms PostgreSQL \
  --workload c \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT \
  start &>$LOG_DIR/test_ycsb_start_postgresql.log
```

The summary confirms the SUT is running and shows the port-forward command.

### Start DBMS and Load Data

Starts PostgreSQL and imports YCSB data using 8 parallel loader pods with 64 threads each.
The data volume is created and marked as loaded; subsequent `run` invocations with the same parameters will skip this step.

```bash
bexhoma ycsb -ms 1 -tr \
  --dbms PostgreSQL \
  --workload c \
  -m -mc \
  -nlp 8 -nlt 64 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load &>$LOG_DIR/test_ycsb_load_postgresql.log
```

Key parameters:
- `-nlp 8`: 8 parallel loader pods
- `-nlt 64`: 64 threads per loader pod

The summary's **Loading** table shows aggregate throughput across all loader pods.
The **Ingestion** tables show how much CPU and RAM the SUT and loader consumed.

### Start DBMS and Load Data and Run Workload

Full experiment: loads data and then runs YCSB workload C with 8 benchmarker pods.

```bash
bexhoma ycsb -ms 1 -tr \
  --dbms PostgreSQL \
  --workload c \
  -m -mc \
  -nlp 8 -nlt 64 -nbp 8 -nbt 64 -ss \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_ycsb_run_postgresql.log
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
The configuration name encodes concurrency and target: `PostgreSQL-<pods>-<pods>-<target>`.

### Start DBMS

```bash
bexhoma benchbase -ms 1 -tr \
  --dbms PostgreSQL \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT \
  start &>$LOG_DIR/test_benchbase_start_postgresql.log
```

### Start DBMS and Load Data

Imports TPC-C data (scale factor 1) using 8 parallel loader pods.

```bash
bexhoma benchbase -ms 1 -tr \
  --dbms PostgreSQL \
  -m -mc \
  -nlp 8 -nlt 64 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load &>$LOG_DIR/test_benchbase_load_postgresql.log
```

The **Loading** table reports `Throughput [SF/h]` — scale factors loaded per hour.

### Start DBMS and Load Data and Run Workload

Loads data with 1 pod (Benchbase loads serially by design) and runs the workload with 8 benchmarker pods for 5 minutes.

```bash
bexhoma benchbase -ms 1 -tr \
  --dbms PostgreSQL \
  -m -mc \
  -nlp 1 -nlt 64 -nbp 8 -nbt 64 -ss \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_benchbase_run_postgresql.log
```

The **Execution** table reports:
- `Throughput (requests/second)` and `Goodput (requests/second)` — total and successful transaction rate
- `Latency Distribution.95th Percentile Latency (microseconds)` — tail latency
- `efficiency` — how close actual throughput came to the target

---

## HammerDB (TPC-C)

HammerDB runs TPC-C using virtual users (vusers).
The configuration name encodes virtual users and clients: `PostgreSQL-BHT-<vusers>-<clients>`.

### Start DBMS

```bash
bexhoma hammerdb -ms 1 -tr \
  --dbms PostgreSQL \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT \
  start &>$LOG_DIR/test_hammerdb_start_postgresql.log
```

### Start DBMS and Load Data

Imports TPC-C data (1 warehouse = scale factor 1) using a single loader pod.
HammerDB's loader is inherently single-threaded, so `-nlp 1 -nlt 1` is typical.

```bash
bexhoma hammerdb -ms 1 -tr \
  --dbms PostgreSQL \
  -m -mc \
  -nlp 1 -nlt 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load &>$LOG_DIR/test_hammerdb_load_postgresql.log
```

The **Loading** table reports `Imported warehouses [1/h]`.

### Start DBMS and Load Data and Run Workload

Loads data and runs TPC-C for 5 minutes with 64 virtual users.

```bash
bexhoma hammerdb -ms 1 -tr \
  --dbms PostgreSQL \
  -m -mc \
  -nlp 1 -nlt 1 -nbp 1 -nbt 64 -ss \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_hammerdb_run_postgresql.log
```

The **Execution** table reports `NOPM` (New Orders Per Minute) and `TPM` (Transactions Per Minute), which are the standard HammerDB TPC-C metrics.

---

## TPC-H

TPC-H is the standard analytical benchmark with 22 queries.
Data is generated by a loader pod using `dbgen`, then loaded into the SUT.
After loading, the DBMSBenchmarker tool runs the 22 queries and records per-query latency.

### Start DBMS

```bash
bexhoma tpch -ms 1 -tr \
  --dbms PostgreSQL \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT \
  start &>$LOG_DIR/test_tpch_start_postgresql.log
```

### Start DBMS and Load Data

Generates and loads TPC-H data at scale factor 1.
The flags `-ii -ic -is` trigger index creation, constraint application, and statistics gathering after the raw data is ingested.

```bash
bexhoma tpch -ms 1 -tr \
  --dbms PostgreSQL \
  -m -mc \
  -ii -ic -is -nlp 1 -nlt 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load &>$LOG_DIR/test_tpch_load_postgresql.log
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
bexhoma tpch -ms 1 -tr \
  --dbms PostgreSQL \
  -m -mc \
  -ii -ic -is -nlp 1 -nlt 1 -nbp 1 -nbt 64 -ss  \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpch_run_postgresql.log
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
bexhoma tpcds -ms 1 -tr \
  --dbms PostgreSQL \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT \
  start &>$LOG_DIR/test_tpcds_start_postgresql.log
```

### Start DBMS and Load Data

```bash
bexhoma tpcds -ms 1 -tr \
  --dbms PostgreSQL \
  -m -mc \
  -ii -ic -is -nlp 1 -nlt 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load &>$LOG_DIR/test_tpcds_load_postgresql.log
```

### Start DBMS and Load Data and Run Workload

Loads TPC-DS data and runs all 99 queries.
Some queries may fail on certain DBMS (e.g., Q90 raises a division-by-zero on PostgreSQL at SF=1); these are flagged in the **Errors** section and in **Tests**.

```bash
bexhoma tpcds -ms 1 -tr \
  --dbms PostgreSQL \
  -m -mc \
  -ii -ic -is -nlp 1 -nlt 1 -nbp 1 -nbt 64 -ss  \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpcds_run_postgresql.log
```

The **Execution** section reports per-query latency for all 99 TPC-DS queries and the same Power@Size / Throughput@Size metrics as TPC-H.
