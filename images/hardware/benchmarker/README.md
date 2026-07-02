# Benchmarker for hardware benchmarks (sysbench / fio)

This folder contains the Dockerfile for a benchmarker that connects to a SUT
container via SSH and runs sysbench (CPU and memory) or fio (disk I/O) workloads
remotely.

## Environment variables

### Bexhoma experiment identity

* `BEXHOMA_DBMS`: DBMS label. Echoed to the log.
* `BEXHOMA_CONFIGURATION`: Configuration name. Echoed to the log.
* `BEXHOMA_CONNECTION`: Bexhoma connection name. Used to address the Redis message queue.
* `BEXHOMA_EXPERIMENT`: Bexhoma experiment identifier. Used to address the Redis message queue.
* `BEXHOMA_EXPERIMENT_RUN`: Number of the current repetition of the complete experiment.
* `BEXHOMA_CLIENT`: Client index. Echoed to the log.
* `BEXHOMA_BENCHMARK_RUN`: Benchmark run index. Echoed to the log.
* `BEXHOMA_CHILD`: Index of the current pod (1-based). Overwritten at runtime by the Redis queue entry.

### Scaling and parallelism

* `BEXHOMA_NUM_PODS`: Number of parallel pods.
* `BEXHOMA_RNGSEED`: Random seed. Currently ignored.

### Pod synchronisation

Pods always synchronise before starting: each pod decrements the Redis counter
`bexhoma-benchmarker-podcount-job-<CONNECTION>-<EXPERIMENT>` and waits until all
`BEXHOMA_NUM_PODS` pods are ready.

* `BEXHOMA_TIME_START`: Optional RFC-3339 timestamp. When non-zero, the pod sleeps until this time before starting.
* `BEXHOMA_TIME_NOW`: Informational timestamp of the planned start, echoed to the log.

### SUT connection

* `BEXHOMA_SUT_HOST`: Hostname of the SUT container (default `sut-service`).
* `BEXHOMA_SUT_USER`: SSH user on the SUT (default `bench`).
* `BEXHOMA_SUT_KEY`: Path to the SSH private key inside the benchmarker image (default `/root/.ssh/id_ed25519`).

### Hardware benchmark parameters

* `HARDWARE_TYPE`: Benchmark to run — `sysbench` or `fio`.
* `HARDWARE_THREADS`: Number of threads passed to sysbench (default `4`). Not used by fio.
* `HARDWARE_TEST_DIR`: Directory on the SUT where fio creates its test files (default `/tmp/fio-test`). Not used by sysbench.
* `HARDWARE_SIZE`: Size of fio test files (default `1G`). Not used by sysbench.

## Workloads

### sysbench (`HARDWARE_TYPE=sysbench`)

Runs two tests sequentially on the SUT via SSH:

1. **CPU** — prime-number calculation (`--cpu-max-prime=20000`).
2. **Memory** — sequential memory transfers (1 KB blocks, 10 GB total).

### fio (`HARDWARE_TYPE=fio`)

Runs two tests sequentially on the SUT via SSH:

1. **Sequential write** — 1 MB blocks, 30-second runtime.
2. **Random read/write (QD1)** — 4 KB blocks, `iodepth=1`, `fsync=1`, 30-second runtime.
