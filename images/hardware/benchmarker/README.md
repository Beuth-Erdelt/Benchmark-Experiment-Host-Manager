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

* `BEXHOMA_HOST`: Hostname of the SUT container. Injected automatically by bexhoma's manifest builder (`configurations/manifest.py`) with the SUT's real Kubernetes service DNS name; not set via the Dockerfile.
* `BEXHOMA_SUT_USER`: SSH user on the SUT (default `bench`).
* `BEXHOMA_SUT_KEY`: Path to the SSH private key inside the benchmarker image (default `/root/.ssh/id_ed25519`).

### Hardware benchmark parameters

* `HARDWARE_TYPE`: Benchmark to run — `sysbench` or `fio`.
* `HARDWARE_THREADS`: Number of threads passed to sysbench (default `4`). Not used by fio.
* `HARDWARE_TEST_DIR`: Directory on the SUT where fio creates its test files (default `/database/fio-test`). Not used by sysbench. `/database` is the PVC-backed volume mounted by `k8s/deploymenttemplate-Hardware.yml`, so fio results reflect the benchmarked storage rather than the SUT container's ephemeral filesystem.
* `HARDWARE_SIZE`: Size of the fio test file (default `1G`). Not used by sysbench.
* `HARDWARE_DURATION`: Runtime of the fio job in seconds (default `30`). Not used by sysbench.

### fio workload parameters (`HARDWARE_TYPE=fio` only)

fio runs as a **single** job per pod, fully described by these variables (mirrors the
options exposed by `scripts/hardware-benchmark.sh`):

* `HARDWARE_FIO_RW`: I/O pattern — `write`, `read`, `randwrite`, `randread`, or `randrw` (default `randrw`).
* `HARDWARE_FIO_BS`: Block size (default `8k`).
* `HARDWARE_FIO_IODEPTH`: Queue depth (default `1`).
* `HARDWARE_FIO_NUMJOBS`: Number of parallel fio jobs (default `1`).
* `HARDWARE_FIO_ENGINE`: fio ioengine — `sync`, `libaio`, `io_uring`, ... (default `sync`; `sync` needs no special kernel/seccomp support, which is not guaranteed for every SUT container).
* `HARDWARE_FIO_FSYNC`: Call `fsync` every N writes; `0` disables it (default `0`).
* `HARDWARE_FIO_RWMIXREAD`: Percentage of reads when `HARDWARE_FIO_RW=randrw` (default `50`). Ignored for all other `HARDWARE_FIO_RW` values.

## Workloads

### sysbench (`HARDWARE_TYPE=sysbench`)

Runs two tests sequentially on the SUT via SSH:

1. **CPU** — prime-number calculation (`--cpu-max-prime=20000`).
2. **Memory** — sequential memory transfers (1 KB blocks, 10 GB total).

### fio (`HARDWARE_TYPE=fio`)

Runs one fio job on the SUT via SSH, configured entirely by the `HARDWARE_FIO_*`
variables above, with `--direct=1 --time_based --group_reporting --output-format=json`.

## Output

Both workloads write their raw result(s) to `/results/$BEXHOMA_EXPERIMENT/`, named
`<tool>.$BEXHOMA_CONNECTION.$BEXHOMA_CLIENT.<uuid>.<ext>` (consistent with the other
Bexhoma benchmarker images):

* **sysbench**: `sysbench.....cpu.txt` and `sysbench.....memory.txt` (raw stdout).
* **fio**: `fio.....json` (raw fio JSON report) and `fio.....csv` (one-row summary:
  IOPS, bandwidth, and 8 completion-latency percentiles — p01/p10/p50/p90/p95/p99/p999/p9999,
  in ms — per read/write direction).

Both scripts also echo a `KEY:VALUE` summary of the same metrics to stdout
(`HARDWARE_FIO_READ_IOPS`, `HARDWARE_FIO_READ_LAT_P99_MS`, `HARDWARE_SYSBENCH_CPU_EVENTS_PER_SEC`,
etc.), so results can be scraped from the pod log without opening the result files.
