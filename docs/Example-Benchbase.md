# Benchmark: Benchbase's TPC-C

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

Benchbase's TPC-C [1] implementation [2,5] does not allow scaling data generation and ingestion, but scaling the benchmarking driver.
It needs considerable client resources, so simulating many users requires scale-out of the driver [6].

> TPC-C involves a mix of five concurrent transactions of different types and complexity either executed on-line or queued for deferred execution. The database is comprised of nine types of tables with a wide range of record and population sizes. TPC-C is measured in transactions per minute (tpmC). While the benchmark portrays the activity of a wholesale supplier, TPC-C is not limited to the activity of any particular business segment, but, rather represents any industry that must manage, sell, or distribute a product or service.

In Benchbase's implementation, for each warehouse the number of assigned threads is computed [3].
Each thread receives a fixed warehouse and a fixed number of districts and starts a connection [4].
There still can be deadlocks, because *A supplying warehouse number (OL_SUPPLY_W_ID) is selected as the home warehouse 99% of the time and as a remote warehouse 1% of the time* [1], and a new order sets a lock at the stock table.


<img src="https://raw.githubusercontent.com/wiki/cmu-db/benchbase/img/tpcc.png" alt="drawing" width="600"/>

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. TPC-C Homepage: https://www.tpc.org/tpcc/
1. Benchbase Repository: https://github.com/cmu-db/benchbase/wiki/TPC-C
1. Benchbase threads per warehouse: https://github.com/cmu-db/benchbase/blob/main/src/main/java/com/oltpbenchmark/benchmarks/tpcc/TPCCBenchmark.java
1. Benchbase connect: https://github.com/cmu-db/benchbase/blob/main/src/main/java/com/oltpbenchmark/api/BenchmarkModule.java#L82
1. OLTP-Bench: An Extensible Testbed for Benchmarking Relational Databases: http://www.vldb.org/pvldb/vol7/p277-difallah.pdf
1. A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools: https://doi.org/10.1007/978-3-031-68031-1_9

## Perform Benchmark

You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"
BEXHOMA_MS=1
BEXHOMA_STORAGE_CLASS="shared"

mkdir -p $LOG_DIR
```

The experiment is run with the [benchbase file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/benchbase.py).

Example:
```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 160 \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_scale.log
```

This
* starts a clean instance of PostgreSQL (`-dbms`)
  * data directory inside a Docker container
* starts 1 loader pod (per DBMS) that
  * creates TPC-C schema in the database
  * imports data for 16 (`-sf`) warehouses into the DBMS
  * using all threads of driver machine (benchbase setting)
* runs streams of TPC-C queries (per DBMS)
    * running for 5 (`-xsd`) minutes
    * each stream (pod) having 16 threads to simulate 16 users (`-nbt`)
    * `-nbp`: first stream 1 pod, second stream 2 pods (8 threads each)
    * target is 16x(`-ltf`) 1024 (`-xtb`) ops
* with a maximum of 1 DBMS per time (`-ms`)
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
+---------------------+--------------+--------------+----------------+-----------------------------+
| 1726658756          | sut          |   loaded [s] | use case       | benchmarker                 |
+=====================+==============+==============+================+=============================+
| PostgreSQL-1-1-1024 | (1. Running) |           62 | benchbase_tpcc | (2. Succeeded) (2. Running) |
+---------------------+--------------+--------------+----------------+-----------------------------+
```

The code `1726658756` is the unique identifier of the experiment.
You can find the number also in the output of `benchbase.py`.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1726658756` (removes everything that is related to experiment `1726658756`).

## Evaluate Results

At the end of a benchmark you will see a summary like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_postgresql_scale_summary.md" target="_blank" rel="noopener">docs_benchbase_postgresql_scale.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1062s 
* Code: 1795443622
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.3.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:834209
  * datadisk:4308
  * volume_size:1.8T
  * volume_used:815G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795443622
    * TENANT_VOL:False
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:848377
  * datadisk:20436
  * volume_size:1.8T
  * volume_used:829G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795443622
    * TENANT_VOL:False

### Ingestion
* PostgreSQL-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1795443622-dd5c9f7c7-4kh95: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |   16 |       97.00 |           6.00 |            0.00 |         81.00 |           10.00 |              1 |         1 |             |                |             0 | False         |              593.81 | False               |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 |       160 |    16384 |           0 | 300.00 |       80 |                       16351.87 |                    16153.73 |         0.00 |                                                      17284.00 |                                               5671.00 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       1 |        80 |     8192 |           0 | 300.00 |       14 |                        5124.70 |                     5069.09 |         0.00 |                                                      35127.00 |                                              15599.00 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       2 |        80 |     8192 |           0 | 300.00 |       18 |                        5131.36 |                     5075.84 |         0.00 |                                                      35243.00 |                                              15582.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 |       160 |    16384 |           0 | 300.00 |       80 |                       16351.87 |                    16153.73 |         0.00 |                                                      17284.00 |                                               5671.00 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        2 |               1 |           2 |       160 |    16384 |           0 | 300.00 |       32 |                       10256.06 |                    10144.93 |         0.00 |                                                      35243.00 |                                              15590.50 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
```

</details>


To see the summary again you can simply call `bexhoma summary -e 1708411664` with the experiment code.

### Detailed Evaluation

Results are transformed into pandas DataFrames and can be inspected in detail.
See for example
* [Jupyter Notebooks](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/evaluator_dbmsbenchmarker/notebooks/)

You can connect to an evaluation server in the cluster by `bexhoma dashboard`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888

You can connect to an evaluation server locally by `bexhoma jupyter`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888

## Adjust Parameters

The script supports
* exact repetitions for statistical confidence
* variations to scan a large parameters space
* combine results for easy evaluation

There are various ways to change parameters.

### Manifests

The YAML manifests for the components can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/k8s

### SQL Scrips

The SQL scripts for pre and post ingestion can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/benchbase

There are per DBMS
* `initschema`-files, that are invoked before loading of data
* `checkschema`-files, that are invoked after loading of data

You can find the output of the files in the result folder.



### Dockerfiles

The Dockerfiles for the components can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/benchbase

### Command line

You maybe want to adjust some of the parameters that are set in the file: `python benchbase.py -h`

```bash
usage: benchbase.py [-h] [-aws] [-db] [-sl] [-ss] [-ar] [-cx CONTEXT]
                    [-e EXPERIMENT] [-m] [-ma] [-mc] [-mm MONITORING_METRICS]
                    [-ms MAX_SUT] [-mse MAX_SUT_EXPERIMENT]
                    [-et EXPERIMENT_TIMEOUT] [-lt LOADING_TIMEOUT]
                    [-nc NUM_CONFIG] [-ne NUM_QUERY_EXECUTORS]
                    [-nw NUM_WORKER] [-nwr NUM_WORKER_REPLICAS]
                    [-nws NUM_WORKER_SHARDS] [-nlp NUM_LOADING_PODS]
                    [-nlt NUM_LOADING_THREADS] [-nbp NUM_BENCHMARKING_PODS]
                    [-nbt NUM_BENCHMARKING_THREADS] [-sf SCALING_FACTOR]
                    [-t TIMEOUT] [-lr LIMIT_RAM] [-lc LIMIT_CPU]
                    [-rr REQUEST_RAM] [-rc REQUEST_CPU]
                    [-rct REQUEST_CPU_TYPE] [-rg REQUEST_GPU]
                    [-rgt REQUEST_GPU_TYPE] [-rst REQUEST_STORAGE_TYPE]
                    [-rss REQUEST_STORAGE_SIZE] [-rsr] [-rsrp]
                    [-rnn [REQUEST_NODE_NAME]] [-rnl [REQUEST_NODE_LOADING]]
                    [-rnb [REQUEST_NODE_BENCHMARKING]]
                    [-rnp [REQUEST_NODE_POOLING]] [-mtn MULTI_TENANT_NUM]
                    [-mtb MULTI_TENANT_BY] [-mtv] [-tr] [-rp] [--set SETS]
                    [-dbms [{PostgreSQL,MySQL,MariaDB,YugabyteDB,CockroachDB,TiDB,DatabaseService,Citus,PGBouncer,CedarDB} ...]]
                    [-xnsr NUM_SUT_REPLICAS] [-xnpd NUM_PD_NODES]
                    [-xnbf NUM_BENCHMARKING_TARGET_FACTORS]
                    [-xnpp NUM_POOLING_PODS] [-xnpi NUM_POOLING_IN]
                    [-xnpo NUM_POOLING_OUT] [-xwl {a,b,c,d,e,f,c2}]
                    [-xsd SCALING_DURATION] [-xli SCALING_LOGGING] [-xkey]
                    [-xconn] [-xbatch EXTRA_BATCHSIZE]
                    [-xbt {tpcc,twitter,chbenchmark,ycsb}] [-xtb TARGET_BASE]
                    [-xwu WARMUP]
                    {run,start,load}

Run Benchbase benchmarks (TPC-C, YCSB, Twitter, CH-Benchmark) against a DBMS
in Kubernetes. Controls loading concurrency, benchmarking throughput targets,
optional connection pooling, and resource allocation.

positional arguments:
  {run,start,load}      experiment phase: start SUT only, load data, or run
                        the full benchmark

options:
  -h, --help            show this help message and exit
  -aws, --aws           pin components to AWS EKS node groups
  -db, --debug          enable debug logging
  -sl, --skip-loading   skip data loading and start benchmarking immediately
  -ss, --skip-shutdown  keep SUT pods running after the experiment finishes
  -ar, --activate-reset
                        activate configured reset scripts (e.g.
                        CHECKPOINT/VACUUM) when set on a benchmarker entry;
                        off by default
  -cx, --context CONTEXT
                        kubectl context to use (default: current context)
  -e, --experiment EXPERIMENT
                        resume an existing experiment by its code
  -m, --monitoring      enable Prometheus monitoring for the SUT
  -ma, --monitoring-app
                        enable application-level metrics collection
  -mc, --monitoring-cluster
                        enable node-level monitoring for the entire cluster
  -mm, --monitoring-metrics MONITORING_METRICS
                        switch single cluster-wide hardware metrics of
                        cluster.config on or off for this experiment,
                        overriding their 'active' flag, e.g.
                        total_gpu_util=on,total_network_rx=off; needs -m or
                        -mc
  -ms, --max-sut MAX_SUT
                        maximum number of DBMS configurations to run in
                        parallel cluster-wide (default: no limit)
  -mse, --max-sut-experiment MAX_SUT_EXPERIMENT
                        maximum number of DBMS configurations in this
                        experiment to run in parallel (default: no limit)
  -et, --experiment-timeout EXPERIMENT_TIMEOUT
                        maximum wall-clock duration of the experiment in
                        minutes; when exceeded, the experiment is stopped and
                        all its components are removed from the cluster
                        (default: no limit)
  -lt, --loading-timeout LOADING_TIMEOUT
                        maximum loading duration per configuration in minutes;
                        captures diagnostics and removes the experiment when
                        exceeded (default: no limit)
  -nc, --num-config NUM_CONFIG
                        number of experiment repetitions per configuration
  -ne, --num-query-executors NUM_QUERY_EXECUTORS
                        comma-separated list of parallel client counts to
                        sweep
  -nw, --num-worker NUM_WORKER
                        number of worker nodes for distributed DBMS
  -nwr, --num-worker-replicas NUM_WORKER_REPLICAS
                        number of replicas per worker node
  -nws, --num-worker-shards NUM_WORKER_SHARDS
                        number of shards per worker node
  -nlp, --num-loading-pods NUM_LOADING_PODS
                        comma-separated list of total loader pod counts
  -nlt, --num-loading-threads NUM_LOADING_THREADS
                        comma-separated list of total loader threads (split
                        across pods)
  -nbp, --num-benchmarking-pods NUM_BENCHMARKING_PODS
                        comma-separated list of benchmarker pod counts
  -nbt, --num-benchmarking-threads NUM_BENCHMARKING_THREADS
                        total benchmarking threads, split evenly across pods
  -sf, --scaling-factor SCALING_FACTOR
                        scaling factor controlling dataset size
  -t, --timeout TIMEOUT
                        per-query timeout in seconds
  -lr, --limit-ram LIMIT_RAM
                        RAM limit for the SUT and worker pods (e.g. 64Gi; 0 =
                        no limit); comma-separated to sweep several settings
                        (e.g. 32Gi,64Gi), one configuration per entry
  -lc, --limit-cpu LIMIT_CPU
                        CPU limit for the SUT and worker pods (e.g. 4; 0 = no
                        limit); comma-separated to sweep, must then match the
                        length of any other swept resource list
  -rr, --request-ram REQUEST_RAM
                        RAM request for the SUT and worker pods (e.g. 16Gi);
                        comma-separated to sweep several settings (e.g.
                        32Gi,64Gi), one configuration per entry
  -rc, --request-cpu REQUEST_CPU
                        CPU request for the SUT and worker pods (e.g. 4);
                        comma-separated to sweep, must then match the length
                        of any other swept resource list
  -rct, --request-cpu-type REQUEST_CPU_TYPE
                        require SUT node to carry label cpu=<value>
  -rg, --request-gpu REQUEST_GPU
                        number of GPUs to request for the SUT pod
  -rgt, --request-gpu-type REQUEST_GPU_TYPE
                        require SUT node to carry label gpu=<value>
  -rst, --request-storage-type REQUEST_STORAGE_TYPE
                        storage class for the SUT persistent volume ('' or
                        unset = ephemeral, 'ramdisk' = in-memory; other values
                        must be declared for the active cluster context, see
                        cluster config 'storage_classes'); comma-separated to
                        sweep the class, one configuration per entry and
                        paired by position with -rc/-lc/-rr/-lr, an empty
                        entry meaning ephemeral
  -rss, --request-storage-size REQUEST_STORAGE_SIZE
                        size of the SUT persistent volume (e.g. 10Gi)
  -rsr, --request-storage-remove
                        delete any existing PVC for the SUT before starting
  -rsrp, --request-storage-remove-per-repetition
                        delete the PVC of the SUT before every repetition
                        (-nc), so each repetition loads into a fresh volume;
                        implies -rsr
  -rnn, --request-node-name [REQUEST_NODE_NAME]
                        pin the SUT pod to this Kubernetes node
  -rnl, --request-node-loading [REQUEST_NODE_LOADING]
                        pin loader pods to this Kubernetes node
  -rnb, --request-node-benchmarking [REQUEST_NODE_BENCHMARKING]
                        pin benchmarker pods to this Kubernetes node
  -rnp, --request-node-pooling [REQUEST_NODE_POOLING]
                        pin pooling pods to this Kubernetes node
  -mtn, --multi-tenant-num MULTI_TENANT_NUM
                        number of tenants for multi-tenant experiments
  -mtb, --multi-tenant-by MULTI_TENANT_BY
                        tenancy granularity: schema, database, or container
  -mtv, --multi-tenant-volume
                        allocate a separate persistent volume per tenant
  -tr, --test-result    validate that results meet basic correctness
                        requirements
  -rp, --report         also write a tiered Markdown summary report
                        (report/index.md + detail files) to the result folder
  --set SETS            override a deployment parameter, e.g.
                        deployment[bexhoma-deployment-postgres].container[dbms].
                        max_worker_processes=128
  -dbms, --dbms [{PostgreSQL,MySQL,MariaDB,YugabyteDB,CockroachDB,TiDB,DatabaseService,Citus,PGBouncer,CedarDB} ...]
                        one or more DBMS engines to test
  -xnsr, --xnum-sut-replicas NUM_SUT_REPLICAS
                        number of SUT replicas per configuration
  -xnpd, --xnum-pd-nodes NUM_PD_NODES
                        number of PD (Placement Driver) nodes, independent of
                        -nw (TiDB only; keep odd)
  -xnbf, --xnum-benchmarking-target-factors NUM_BENCHMARKING_TARGET_FACTORS
                        comma-separated multipliers for the benchmarking ops
                        target (target = -xtb × factor)
  -xnpp, --xnum-pooling-pods NUM_POOLING_PODS
                        comma-separated list of connection-pooler pod counts
  -xnpi, --xnum-pooling-in NUM_POOLING_IN
                        comma-separated list of max inbound connections per
                        pooler pod
  -xnpo, --xnum-pooling-out NUM_POOLING_OUT
                        comma-separated list of max outbound connections per
                        pooler pod (to the DBMS)
  -xwl, --xworkload {a,b,c,d,e,f,c2}
                        YCSB workload letter, only used when -xbt ycsb
  -xsd, --xscaling-duration SCALING_DURATION
                        benchmark duration in minutes
  -xli, --xlogging-interval SCALING_LOGGING
                        status logging interval in milliseconds (0 = disabled)
  -xkey, --extra-keying
                        simulate TPC-C keying and think times between
                        transactions
  -xconn, --extra-new-connection
                        open a new database connection for every transaction
  -xbatch, --extra-batchsize EXTRA_BATCHSIZE
                        number of rows per INSERT batch during loading
  -xbt, --xbenchmark-type {tpcc,twitter,chbenchmark,ycsb}
                        Benchbase benchmark suite to run
  -xtb, --xtarget-base TARGET_BASE
                        base ops-per-second target; multiply by -xnbf factors
                        to get per-pod target (0 = unlimited)
  -xwu, --xwarmup WARMUP
                        warmup in seconds before the measured benchmark
                        duration (not part of the results)
```

## Monitoring

[Monitoring](Monitoring.md) can be activated for DBMS only (`-m`) or for all components (`-mc`).

Example:

```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 160 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_monitoring.log
```

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_postgresql_monitoring_summary.md" target="_blank" rel="noopener">docs_benchbase_postgresql_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 977s 
* Code: 1795444701
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.3.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:828836
  * datadisk:4307
  * volume_size:1.8T
  * volume_used:810G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795444701
    * TENANT_VOL:False
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:849392
  * datadisk:20319
  * volume_size:1.8T
  * volume_used:830G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795444701
    * TENANT_VOL:False

### Ingestion
* PostgreSQL-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1795444701-58f8c5d6db-52l8x: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |   16 |       85.00 |           4.00 |            0.00 |         71.00 |           10.00 |              1 |         1 |             |                |             0 | False         |              677.65 | False               |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 |       160 |    16384 |           0 | 300.00 |       67 |                       16343.16 |                    16149.58 |         0.00 |                                                      15818.00 |                                               5288.00 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       1 |        80 |     8192 |           0 | 300.00 |       17 |                        5744.28 |                     5680.62 |         0.00 |                                                      32479.00 |                                              13513.00 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       2 |        80 |     8192 |           0 | 300.00 |       23 |                        5742.98 |                     5680.13 |         0.00 |                                                      32514.00 |                                              13536.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 |       160 |    16384 |           0 | 300.00 |       67 |                       16343.16 |                    16149.58 |         0.00 |                                                      15818.00 |                                               5288.00 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        2 |               1 |           2 |       160 |    16384 |           0 | 300.00 |       40 |                       11487.26 |                    11360.76 |         0.00 |                                                      32514.00 |                                              13524.50 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       165.10 |      2.94 |           2.06 |                  3.68 |
| postgresql-1-1-2-1 |       165.10 |      2.94 |           2.06 |                  3.68 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       613.67 |     15.20 |           0.24 |                  0.24 |
| postgresql-1-1-2-1 |       613.67 |     15.20 |           0.24 |                  0.24 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      5398.22 |     18.73 |           8.15 |                 13.60 |
| postgresql-1-1-2-1 |      4466.22 |     21.24 |          12.04 |                 16.00 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      2818.61 |     11.14 |           1.11 |                  1.11 |
| postgresql-1-1-2-1 |      2734.23 |     12.69 |           0.87 |                  0.88 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
```

</details>

This gives a survey about CPU (in CPU seconds) and RAM usage (in Gb) during loading and execution of the benchmark.

In this example, metrics are very instable. Metrics are fetched every 30 seconds.
This is too coarse for such a quick example.


## Use Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.
With repetitions (`-nc`), `-rsr` removes an existing volume only before the first repetition and later repetitions reuse it without loading; `-rsrp` removes it before every repetition. See [Concepts](Concepts.md).

Example:
```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nc 2 \
  -nbp 1 \
  -nbt 160 \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_storage.log
```

The following status shows two volumes of type `shared`.
Every PostgreSQL experiment running Benchbase's TPC-C of SF=16 (warehouses) will take the databases from these volumes and skip loading.
In this example `-nc` is set to two, that is the complete experiment is repeated twice for statistical confidence.
The first instance of PostgreSQL mounts the volume and generates the data.
All other instances just use the database without generating and loading data.

```bash
+----------------------------------------------+-----------------+-------------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+
| Volumes                                      | configuration   | experiment        | loaded [s]   |   timeLoading [s] | dbms            | storage_class_name   | storage   | status   | size   | used   |
+==============================================+=================+===================+==============+===================+=================+======================+===========+==========+========+========+
| bexhoma-storage-postgresql-benchbase-tpcc-16 | postgresql      | benchbase-tpcc-16 | True         |               184 | PostgreSQL      | shared               | 50Gi      | Bound    | 50G    | 4.8G   |
+----------------------------------------------+-----------------+-------------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+
```

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_postgresql_storage_summary.md" target="_blank" rel="noopener">docs_benchbase_postgresql_storage.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1193s 
* Code: 1795445710
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.3.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:817229
  * datadisk:4307
  * volume_size:49G
  * volume_used:4.3G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795445710
    * TENANT_VOL:False
* postgresql-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:817232
  * datadisk:18045
  * volume_size:49G
  * volume_used:18G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795445710
    * TENANT_VOL:False

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: PostgreSQL-1-2

### Data Parameters of Reused Volumes
* PostgreSQL-1: loading values of the volume: script=Schema, indexing=Checks

### Ingestion
* PostgreSQL-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1795445710-5874d8d654-swvfj: 0
* bexhoma-sut-postgresql-1-1795445710-cbc9b57d8-78fgd: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (1 pods)

### Loading

#### Per Run

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |   16 |       86.00 |           3.00 |            0.00 |         74.00 |            9.00 |              1 |         1 |             |                |             0 | False         |              669.77 | False               |
| PostgreSQL-1-2 |                2 |   16 |       86.00 |           3.00 |            0.00 |         74.00 |            9.00 |              1 |         1 |             |                |             0 | False         |              669.77 | True                |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 |       160 |    16384 |           0 | 300.00 |       57 |                       12831.42 |                    12693.77 |         0.00 |                                                      33480.00 |                                              12453.00 |
| postgresql-1-2-1-1-1 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |        1 |               1 |       1 |       160 |    16384 |           0 | 300.00 |       21 |                        8071.58 |                     7998.27 |         0.00 |                                                      37095.00 |                                              19806.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 |       160 |    16384 |           0 | 300.00 |       57 |                       12831.42 |                    12693.77 |         0.00 |                                                      33480.00 |                                              12453.00 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |        1 |               1 |           1 |       160 |    16384 |           0 | 300.00 |       21 |                        8071.58 |                     7998.27 |         0.00 |                                                      37095.00 |                                              19806.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
```

</details>

The loading times for both instances of loading are the same, since both relate to the same process of ingesting into the database.
Note the added section about `volume_size` and `volume_used` in the connections section.
The benchmark writes data, so the volume grows from run to run.

## Reset Scripts

For repeated benchmarking rounds against the same TPC-C database, bloat and stale planner statistics can drift the result away from the first round.
Bexhoma can run a pre-benchmark reset script (for PostgreSQL `VACUUM ANALYZE`, `CHECKPOINT` and a reset of the statistics counters) before each round to start every round from a comparable state.
The feature is off by default; pass `-ar` to activate it.
Every DBMS has a reset for `tpcc`, PostgreSQL and PGBouncer also for `twitter`, `ycsb` and `chbenchmark`; see [Reset scripts](DBMS.md#reset-scripts--ar) for what each DBMS does.
It also works with multi-tenancy (`-mtb`): with `schema` the script runs once and covers all tenants, with `database` once per tenant, with `container` in each tenant's own container.

Example (`-nc 2` repeats the experiment twice, so the reset script runs before each repeat):
```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 4 \
  -xsd 2 \
  -xtb 1024 \
  -xnbf 1 \
  -nc 2 \
  -nbp 1 \
  -nbt 40 \
  -ar \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_reset.log
```

The reset script's own stdout/stderr is saved next to the other per-DBMS SQL script logs in the result folder, one pair of files per repeat, e.g. `bexhoma-reset_1_1_1-postgresql-1-reset-benchbase.sql.log` / `.error`.

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_postgresql_reset_summary.md" target="_blank" rel="noopener">docs_benchbase_postgresql_reset.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=4
* Type: benchbase
* Duration: 907s 
* Code: 1795446912
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 4. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking runs for 2 minutes. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.3.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [40] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:819317
  * datadisk:1133
  * volume_size:1.8T
  * volume_used:801G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795446912
    * TENANT_VOL:False
* postgresql-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:823249
  * datadisk:1132
  * volume_size:1.8T
  * volume_used:804G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795446912
    * TENANT_VOL:False

### Ingestion
* PostgreSQL-1: 2 of 2 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1795446912-cc975bc97-rlpp5: 0
* bexhoma-sut-postgresql-1-1795446912-5779d5f66d-n7rzn: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (1 pods)

### Loading

#### Per Run

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    4 |       42.00 |           3.00 |            0.00 |         31.00 |            8.00 |              1 |         1 |             |                |             0 | False         |              342.86 | False               |
| PostgreSQL-1-2 |                2 |    4 |       40.00 |           5.00 |            0.00 |         30.00 |            5.00 |              1 |         1 |             |                |             0 | False         |              360.00 | False               |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 |        40 |     1024 |           0 | 120.00 |        0 |                        1023.98 |                     1016.65 |         0.00 |                                                      11697.00 |                                               4528.00 |
| postgresql-1-2-1-1-1 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |        1 |               1 |       1 |        40 |     1024 |           0 | 120.00 |        1 |                        1024.01 |                     1016.38 |         0.00 |                                                      12481.00 |                                               4981.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 |        40 |     1024 |           0 | 120.00 |        0 |                        1023.98 |                     1016.65 |         0.00 |                                                      11697.00 |                                               4528.00 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |        1 |               1 |           1 |        40 |     1024 |           0 | 120.00 |        1 |                        1024.01 |                     1016.38 |         0.00 |                                                      12481.00 |                                               4981.00 |

#### Reset

| phase            | job                |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:-----------------|:-------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |         1.00 |                |
| postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |        1 |               1 |         1.00 |                |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
* TEST passed: Reset scripts ran without errors
```

</details>

The `#### Reset` section appears once per experiment repeat (`-nc 2`), right after `#### Per Phase`.
The duration of `CHECKPOINT` and `VACUUM ANALYZE` grows with the table size; compare it with the benchmarking duration.

## Unlimited Target and Warmup

By default the benchmarker throttles to a throughput target of `-xtb` × `-xnbf` requests per second, split over the benchmarking pods.
With `-xtb 0` there is no target: each pod sends transactions as fast as its terminals (`-nbt`) allow (Benchbase's `<rate>unlimited</rate>`).
A factor of 0 in `-xnbf` does the same for a single entry of the sweep, e.g. `-xnbf 0,1,2` compares an unlimited run with two throttled ones.

`-xwu` sets a warmup in seconds before the measured duration (`-xsd`).
Benchbase runs the workload during the warmup, but does not count these transactions in throughput and latency.
Each benchmarker pod therefore runs for about warmup + `-xsd`.
Note that hardware metrics of the benchmarking phase (`-m`, `-mc`) cover the complete pod runtime, including the warmup, and so does a status log (`-xli`).

Example:
```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 4 \
  -xsd 2 \
  -xwu 60 \
  -xtb 0 \
  -xnbf 1 \
  -nbp 1,2 \
  -nbt 40 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_unlimited.log
```

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_postgresql_unlimited_summary.md" target="_blank" rel="noopener">docs_benchbase_postgresql_unlimited.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=4
* Type: benchbase
* Duration: 687s 
* Code: 1795447828
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 4. Target is unlimited. Factors for benchmarking are [1]. Benchmarking runs for 2 minutes. Each benchmarker has a warmup of 60 seconds before that, which is not part of the results.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.3.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [40] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:845283
  * datadisk:1132
  * volume_size:1.8T
  * volume_used:826G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795447828
    * TENANT_VOL:False
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:851123
  * datadisk:3437
  * volume_size:1.8T
  * volume_used:832G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795447828
    * TENANT_VOL:False

### Ingestion
* PostgreSQL-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1795447828-6cbb6f9856-zpsfj: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    4 |       39.00 |           4.00 |            0.00 |         30.00 |            5.00 |              1 |         1 |             |                |             0 | False         |              369.23 | False               |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 |        40 |        0 |           0 | 120.00 |       17 |                        3913.32 |                     5615.64 |         0.00 |                                                      31030.00 |                                              10187.00 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       1 |        20 |        0 |           0 | 120.00 |        6 |                        2034.13 |                     3093.77 |         0.00 |                                                      28230.00 |                                               9818.00 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       2 |        20 |        0 |           0 | 120.00 |        9 |                        1885.30 |                     2879.94 |         0.00 |                                                      32275.00 |                                              10593.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 |        40 |        0 |           0 | 120.00 |       17 |                        3913.32 |                     5615.64 |         0.00 |                                                      31030.00 |                                              10187.00 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        2 |               1 |           2 |        40 |        0 |           0 | 120.00 |       15 |                        3919.43 |                     5973.70 |         0.00 |                                                      32275.00 |                                              10205.50 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
```

</details>

The workload description says `Target is unlimited.` and mentions the warmup.
In `#### Per Connection` the column `target` is 0 for both pod counts, and `time` is the measured duration (`-xsd`) without the warmup.

## Keying and Thinking Time

`-xkey` activates waiting times before and after the execution of transactions, closer to the TPC-C specification.
Make sure that the number of driver threads (`-nbt`) is 10 times the number of warehouses (`-sf`).
Since `-nbt` can exceed the DBMS's connection limit at the largest pod count in the `-nbp` sweep, raise
`max_connections` accordingly with `--set`.

```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 160 \
  -xsd 30 \
  -xtb 1024 \
  -xnbf 1 \
  -nc 1 \
  -ne 1 \
  -nbp 1,2,5,10 \
  -nbt 1600 \
  -xkey \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rsr \
  -rss 100Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_connections=2000 \
  run &>$LOG_DIR/docs_benchbase_postgresql_keytime.log
```

## Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_postgresql_keytime_summary.md" target="_blank" rel="noopener">docs_benchbase_postgresql_keytime.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=160
* Type: benchbase
* Duration: 10083s 
* Code: 1795511763
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 160. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 30 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.3.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 100Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [1600] threads, split into [1, 2, 5, 10] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_connections', 'target': 'container'}, '2000')].
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:977084
  * datadisk:45450
  * volume_size:98G
  * volume_used:45G
  * cpu_list:0-223
  * args:['-c', 'max_connections=2000', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795511763
    * TENANT_VOL:False
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:977687
  * datadisk:45752
  * volume_size:98G
  * volume_used:45G
  * cpu_list:0-223
  * args:['-c', 'max_connections=2000', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795511763
    * TENANT_VOL:False
* postgresql-1-1-3-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1084622
  * datadisk:45973
  * volume_size:98G
  * volume_used:45G
  * cpu_list:0-223
  * args:['-c', 'max_connections=2000', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795511763
    * TENANT_VOL:False
* postgresql-1-1-4-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1084621
  * datadisk:46175
  * volume_size:98G
  * volume_used:46G
  * cpu_list:0-223
  * args:['-c', 'max_connections=2000', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795511763
    * TENANT_VOL:False

### Ingestion
* PostgreSQL-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1795511763-7f849d84b9-7g24j: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: benchbase (5 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: benchbase (10 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: benchbase (5 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: benchbase (10 pods)

### Loading

#### Per Run

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |  160 |     2021.00 |           3.00 |            0.00 |       1965.00 |           53.00 |              1 |         1 |             |                |             0 | False         |              285.01 | False               |

### Benchmarking

#### Per Connection

| connection            | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |    time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|--------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-1-1  | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 |      1600 |     1024 |           0 | 1800.00 |        0 |                          76.63 |                       76.29 |       100.11 |                                                      22793.00 |                                               9594.00 |
| postgresql-1-1-2-1-1  | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       1 |       800 |      512 |           0 | 1800.00 |        0 |                          38.23 |                       38.07 |        49.95 |                                                      22742.00 |                                               9562.00 |
| postgresql-1-1-2-1-2  | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       2 |       800 |      512 |           0 | 1800.00 |        0 |                          38.32 |                       38.14 |        50.04 |                                                      22887.00 |                                               9606.00 |
| postgresql-1-1-3-1-1  | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |        3 |               1 |       1 |       320 |      204 |           0 | 1800.00 |        0 |                          15.31 |                       15.23 |        19.98 |                                                      21580.00 |                                               8977.00 |
| postgresql-1-1-3-1-2  | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |        3 |               1 |       2 |       320 |      204 |           0 | 1800.00 |        0 |                          15.32 |                       15.27 |        20.03 |                                                      21590.00 |                                               8994.00 |
| postgresql-1-1-3-1-3  | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |        3 |               1 |       3 |       320 |      204 |           0 | 1800.00 |        0 |                          15.31 |                       15.24 |        20.00 |                                                      22092.00 |                                               9135.00 |
| postgresql-1-1-3-1-4  | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |        3 |               1 |       4 |       320 |      204 |           0 | 1800.00 |        0 |                          15.35 |                       15.28 |        20.05 |                                                      21841.00 |                                               9120.00 |
| postgresql-1-1-3-1-5  | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |        3 |               1 |       5 |       320 |      204 |           0 | 1800.00 |        0 |                          15.28 |                       15.22 |        19.97 |                                                      21770.00 |                                               9068.00 |
| postgresql-1-1-4-1-1  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |        4 |               1 |       1 |       160 |      102 |           0 | 1800.00 |        0 |                           7.62 |                        7.58 |         9.95 |                                                      21084.00 |                                               8676.00 |
| postgresql-1-1-4-1-2  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |        4 |               1 |       2 |       160 |      102 |           0 | 1800.00 |        0 |                           7.57 |                        7.53 |         9.88 |                                                      21580.00 |                                               8793.00 |
| postgresql-1-1-4-1-3  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |        4 |               1 |       3 |       160 |      102 |           0 | 1800.00 |        0 |                           7.63 |                        7.59 |         9.97 |                                                      21346.00 |                                               8637.00 |
| postgresql-1-1-4-1-4  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |        4 |               1 |       4 |       160 |      102 |           0 | 1800.00 |        0 |                           7.57 |                        7.54 |         9.89 |                                                      21281.00 |                                               8759.00 |
| postgresql-1-1-4-1-5  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |        4 |               1 |       5 |       160 |      102 |           0 | 1800.00 |        0 |                           7.60 |                        7.56 |         9.92 |                                                      21226.00 |                                               8732.00 |
| postgresql-1-1-4-1-6  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |        4 |               1 |       6 |       160 |      102 |           0 | 1800.00 |        0 |                           7.58 |                        7.55 |         9.90 |                                                      21613.00 |                                               8758.00 |
| postgresql-1-1-4-1-7  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |        4 |               1 |       7 |       160 |      102 |           0 | 1800.00 |        0 |                           7.58 |                        7.54 |         9.90 |                                                      21118.00 |                                               8586.00 |
| postgresql-1-1-4-1-8  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |        4 |               1 |       8 |       160 |      102 |           0 | 1800.00 |        0 |                           7.69 |                        7.66 |        10.05 |                                                      21153.00 |                                               8722.00 |
| postgresql-1-1-4-1-9  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |        4 |               1 |       9 |       160 |      102 |           0 | 1800.00 |        0 |                           7.71 |                        7.67 |        10.07 |                                                      21709.00 |                                               8648.00 |
| postgresql-1-1-4-1-10 | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |        4 |               1 |      10 |       160 |      102 |           0 | 1800.00 |        0 |                           7.67 |                        7.63 |        10.01 |                                                      21639.00 |                                               8845.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |    time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|--------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 |      1600 |     1024 |           0 | 1800.00 |        0 |                          76.63 |                       76.29 |       100.11 |                                                      22793.00 |                                               9594.00 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        2 |               1 |           2 |      1600 |     1024 |           0 | 1800.00 |        0 |                          76.55 |                       76.20 |        99.99 |                                                      22887.00 |                                               9584.00 |
| postgresql-1-1-3 | postgresql-1-1-3 |                1 |        3 |               1 |           5 |      1600 |     1020 |           0 | 1800.00 |        0 |                          76.58 |                       76.23 |       100.03 |                                                      22092.00 |                                               9058.80 |
| postgresql-1-1-4 | postgresql-1-1-4 |                1 |        4 |               1 |          10 |      1600 |     1020 |           0 | 1800.00 |        0 |                          76.21 |                       75.85 |        99.53 |                                                      21709.00 |                                               8715.60 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      1656.56 |      5.95 |          17.00 |                 32.98 |
| postgresql-1-1-2-1 |      1656.56 |      5.95 |          17.00 |                 32.98 |
| postgresql-1-1-3-1 |      1656.56 |      5.95 |          17.00 |                 32.98 |
| postgresql-1-1-4-1 |      1656.56 |      5.95 |          17.00 |                 32.98 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |    215422.72 |    121.36 |           0.40 |                  0.40 |
| postgresql-1-1-2-1 |    215422.72 |    121.36 |           0.40 |                  0.40 |
| postgresql-1-1-3-1 |    215422.72 |    121.36 |           0.40 |                  0.40 |
| postgresql-1-1-4-1 |    215422.72 |    121.36 |           0.40 |                  0.40 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       320.25 |      0.48 |          26.65 |                 42.92 |
| postgresql-1-1-2-1 |       299.97 |      0.39 |          26.89 |                 43.37 |
| postgresql-1-1-3-1 |       317.06 |      0.37 |          27.59 |                 44.27 |
| postgresql-1-1-4-1 |       328.61 |      0.49 |          28.16 |                 45.03 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       555.07 |      1.02 |           4.17 |                  4.17 |
| postgresql-1-1-2-1 |       801.03 |      2.83 |           2.90 |                  2.90 |
| postgresql-1-1-3-1 |       899.01 |      5.83 |           1.41 |                  1.41 |
| postgresql-1-1-4-1 |      1394.30 |     13.93 |           0.80 |                  0.80 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-3-1 (bexhoma-metrics-postgresql-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-3-1 (bexhoma-metrics-postgresql-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-3-1 (bexhoma-metrics-postgresql-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-3-1 (bexhoma-metrics-postgresql-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-4-1 (bexhoma-metrics-postgresql-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-4-1 (bexhoma-metrics-postgresql-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-4-1 (bexhoma-metrics-postgresql-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-4-1 (bexhoma-metrics-postgresql-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: efficiency contains no 0 or NaN
* TEST passed: Workflow as planned
```

</details>

Efficiency is computed via `0.45 * 60. * 100. * Goodput (requests/second) / 12.86 / sf`, when number of client threads is 10 times the number of warehouses:
* 45% is the average portion of new orders in the set of transactions
* 60 transforms to per-minute
* 100 makes it a percentage value
* Goodput (requests/second) is the number of successful transactions per second
* sf is the number of warehouses
* 12.86 is the theoretical limit in the TPC-C speficications

Note that these are statistical values.

