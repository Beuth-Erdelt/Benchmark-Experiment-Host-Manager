# SUT for hardware benchmarks

This folder contains the Dockerfile for a System Under Test (SUT) that accepts
hardware benchmark commands from the benchmarker container via SSH.

The image installs sysbench and fio, creates a passwordless SSH user `bench`,
and starts an SSH daemon as its entrypoint. The benchmarker connects to this
container via SSH and invokes the tools directly; no Bexhoma coordination logic
runs inside this image.

## Included tools

* **sysbench** — CPU and memory benchmarks.
* **fio** — disk I/O benchmarks.
* **OpenSSH server** — listens on port 22; accepts the benchmarker's key.

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
