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
