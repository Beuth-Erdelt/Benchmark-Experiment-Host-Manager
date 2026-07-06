# SUT for hardware benchmarks

This folder contains the Dockerfile for a System Under Test (SUT) that accepts
hardware benchmark commands from the benchmarker container via SSH.

The image installs sysbench and fio, creates a passwordless SSH user `bench`,
and starts an SSH daemon as its entrypoint. The benchmarker connects to this
container via SSH and invokes fio/sysbench directly; no Bexhoma coordination
logic runs inside this image. It also starts a fixed pool of persistent
`sockperf server` instances (see below) that the benchmarker's sockperf client
connects to directly, without SSH.

## Included tools

* **sysbench** — CPU and memory benchmarks.
* **fio** — disk I/O benchmarks.
* **sockperf** — network latency/throughput benchmarks; built from source in a
  builder stage (not packaged for Alpine/musl), see the Dockerfile comments.
* **OpenSSH server** — listens on port 22; accepts the benchmarker's key.

## sockperf server pool

`entrypoint.sh` starts one UDP and one TCP `sockperf server` per port in
`[SOCKPERF_BASE_PORT, SOCKPERF_BASE_PORT + SOCKPERF_NUM_SERVERS)` (defaults:
20000, 16 servers), all backgrounded before `sshd` takes over as the
foreground process. This lets several benchmarker pods (`BEXHOMA_NUM_PODS > 1`)
each connect to their own dedicated server — see
`images/hardware/benchmarker/run_sockperf.sh`, which picks a port from
`BEXHOMA_CHILD` — instead of contending on a single socket. The count is a
static ceiling baked into this image and `k8s/deploymenttemplate-Hardware.yml`,
not a per-experiment setting; pods wrap around (share a server) if a sweep
ever asks for more pods than provisioned servers.

## SSH access

The image expects `bench_key.pub` (the benchmarker's public key) to be present
in the build context. It is installed as `/home/bench/.ssh/authorized_keys` for
the `bench` user.

The matching private key `bench_key` must be placed in the benchmarker image
build context (`images/hardware/benchmarker/bench_key`).

## Storage

`/database` is the base directory the benchmarker's fio job targets via
`HARDWARE_TEST_DIR` (see `images/hardware/benchmarker/README.md`). The
Dockerfile bakes it in (`mkdir` + `chmod 777`) so it always exists and is
writable by `bench`, regardless of whether a volume ends up mounted there:

* **No `-rst` flag on `hardware.py`** (the default) — no PVC is requested,
  `/database` is just part of this container's own ephemeral filesystem, lost
  when the pod is removed.
* **`-rst shared`** (or another storage class) — `k8s/deploymenttemplate-Hardware.yml`
  mounts a real PVC at `/database` instead, made world-writable by that
  manifest's own initContainer (not tied to `bench`'s uid, since ownership set
  by an initContainer isn't reliably visible on every storage class's separate
  mount into the main container). Use this when you actually want to measure
  PVC-backed storage rather than the SUT's ephemeral layer.
