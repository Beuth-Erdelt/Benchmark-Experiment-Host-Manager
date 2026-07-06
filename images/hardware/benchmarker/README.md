# Benchmarker for hardware benchmarks (sysbench / fio / sockperf)

This folder contains the Dockerfile for a benchmarker that connects to a SUT
container and runs sysbench (CPU and memory) or fio (disk I/O) workloads over
SSH, or a sockperf (network latency/throughput) workload directly against one
of the SUT's persistent sockperf server instances (no SSH).

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

### Multi-tenancy

* `BEXHOMA_TENANT_BY`: Tenancy mode. Only `container` is meaningful for Hardware (one SUT pod per tenant, all pinned to the same node via `-rnn`); empty means no tenancy. Echoed to the log.
* `BEXHOMA_TENANT_NUM`: Total number of tenants (`-mtn`). Echoed to the log.
* `BEXHOMA_TENANT_ID`: This tenant's 0-based index, injected directly as a benchmarking parameter by `hardware.py` (no shell-side computation, unlike the `schema`/`database` tenancy modes used by other benchmark types). Echoed to the log.

When `BEXHOMA_TENANT_BY=container`, this pod additionally decrements and polls the
experiment-level Redis counter `bexhoma-benchmarker-podcount-exp-<EXPERIMENT>` before
starting its workload, so that every co-located tenant's sysbench/fio run begins at the
same synchronized instant — the basis for co-located noisy-neighbor experiments (`-mtn N
-mtb container` on `hardware.py`, each tenant getting its own `-rc`/`-lc` CPU quota).

### SUT connection

* `BEXHOMA_HOST`: Hostname of the SUT container. Injected automatically by bexhoma's manifest builder (`configurations/manifest.py`) with the SUT's real Kubernetes service DNS name; not set via the Dockerfile. SSH connects on port 9091, not 22 — `bexhoma-service` maps the SUT's real SSH port (22) to service port 9091 (`port-dbms`), the same port every other DBMS's client connects through. sockperf connects directly to `BEXHOMA_HOST` on one of its own dedicated ports instead (see below) — no SSH involved.
* `BEXHOMA_SUT_USER`: SSH user on the SUT (default `bench`). Not used by sockperf.
* `BEXHOMA_SUT_KEY`: Path to the SSH private key inside the benchmarker image (default `/root/.ssh/id_ed25519`). Not used by sockperf.

### Hardware benchmark parameters

* `HARDWARE_TYPE`: Benchmark to run — `sysbench`, `fio`, or `sockperf`.
* `HARDWARE_THREADS`: Number of threads passed to sysbench (default `4`). Not used by fio.
* `HARDWARE_TEST_DIR`: Directory on the SUT where fio creates its test files (default `/database/fio-test`). Not used by sysbench. `/database` is always present on the SUT (baked into `images/hardware/sut/Dockerfile`); whether it's backed by a real PVC or is just the SUT container's own ephemeral filesystem depends on `-rst` at deploy time — see `images/hardware/sut/README.md`.
* `HARDWARE_SIZE`: Size of the fio test file (default `1G`). Not used by sysbench.
* `HARDWARE_DURATION`: Runtime in seconds (default `30`) — fio's `--runtime` (time-based, so actual runtime matches) and, since both sysbench sub-tests pass `--time=$HARDWARE_DURATION`, an upper bound for each of the CPU and memory phases. The memory phase can finish earlier than `HARDWARE_DURATION` if `--memory-total-size` (10G) transfers before the time limit.

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

### sockperf workload parameters (`HARDWARE_TYPE=sockperf` only)

* `HARDWARE_SOCKPERF_MODE`: `ul` (under-load — fixed send rate, full latency percentiles) or `pp` (ping-pong — one message at a time; default `ul`).
* `HARDWARE_SOCKPERF_PROTOCOL`: `udp` or `tcp` (default `udp`). The SUT runs one server of each protocol per port, so either can be selected without a separate port range.
* `HARDWARE_SOCKPERF_MSGSIZE`: Message payload size in bytes (default `64`).
* `HARDWARE_SOCKPERF_MPS`: Messages per second, or the literal `max` for uncapped (default `max`). Passed directly to sockperf's own `--mps` flag.
* `SOCKPERF_BASE_PORT` / `SOCKPERF_NUM_SERVERS`: Must stay numerically in sync with the same-named `ENV` in `images/hardware/sut/Dockerfile` — used to compute which of the SUT's server instances this pod connects to (see below).

## Workloads

### sysbench (`HARDWARE_TYPE=sysbench`)

Runs two tests sequentially on the SUT via SSH:

1. **CPU** — prime-number calculation (`--cpu-max-prime=20000`), capped at `HARDWARE_DURATION` seconds.
2. **Memory** — sequential memory transfers (1 KB blocks, 10 GB total or `HARDWARE_DURATION` seconds, whichever comes first).

### fio (`HARDWARE_TYPE=fio`)

Runs one fio job on the SUT via SSH, configured entirely by the `HARDWARE_FIO_*`
variables above, with `--direct=1 --time_based --group_reporting --output-format=json`.

### sockperf (`HARDWARE_TYPE=sockperf`)

Runs one `sockperf {ul|pp}` client directly against one of the SUT's persistent
server instances (no SSH). The target port is derived from `BEXHOMA_CHILD`:

```
port = SOCKPERF_BASE_PORT + ((BEXHOMA_CHILD - 1) mod SOCKPERF_NUM_SERVERS)
```

so several benchmarker pods (`BEXHOMA_NUM_PODS > 1`) each get their own
dedicated server instead of contending on one socket; if a sweep ever asks for
more pods than provisioned servers, pods wrap around and share a server.

## Output

All three workloads write their raw result(s) to `/results/$BEXHOMA_EXPERIMENT/`, named
`<tool>.$BEXHOMA_CONNECTION.$BEXHOMA_CLIENT.<uuid>.<ext>` (consistent with the other
Bexhoma benchmarker images):

* **sysbench**: `sysbench.....cpu.txt` and `sysbench.....memory.txt` (raw stdout).
* **fio**: `fio.....json` (raw fio JSON report) and `fio.....csv` (one-row summary:
  IOPS, bandwidth, and 8 completion-latency percentiles — p01/p10/p50/p90/p95/p99/p999/p9999,
  in ms — per read/write direction).
* **sockperf**: `sockperf.....fulllog.csv` (sockperf's own per-message `--full-log`) and
  `sockperf.....csv` (one-row summary: avg/p50/p99/p999 latency in ms, message rate, and
  dropped-message rate).

All three scripts also echo a `KEY:VALUE` summary of the same metrics to stdout
(`HARDWARE_FIO_READ_IOPS`, `HARDWARE_FIO_READ_LAT_P99_MS`, `HARDWARE_SYSBENCH_CPU_EVENTS_PER_SEC`,
`HARDWARE_SOCKPERF_LATENCY_P99_MS`, `HARDWARE_SOCKPERF_MSG_RATE_PER_SEC`, etc.), so results can
be scraped from the pod log without opening the result files.
