######################################################################################
# Dockerfile for Bexhoma - Benchmarker Hardware
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma benchmarker running sysbench and fio
# hardware workloads against a SUT container via SSH.
#
# Base Image: alpine:3.20
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2025-05-18
# Version: 1.0
# Description: Connects to a SUT container via SSH and runs sysbench (CPU/memory)
#   or a single, ENV-configurable fio (disk I/O) workload. Configuration is supplied
#   via environment variables. A Redis message queue is consulted for pod-assignment
#   details. redis-cli and openssh-client are installed for queue interaction and SSH
#   access; jq parses fio's JSON result into KEY:VALUE metrics and a CSV summary.
######################################################################################
FROM alpine:3.20

######################################################################################
# Environment variables — runtime configuration
######################################################################################
# Bexhoma experiment identity
ENV BEXHOMA_CONNECTION=hardware
ENV BEXHOMA_EXPERIMENT=12345
ENV BEXHOMA_EXPERIMENT_RUN=1
ENV BEXHOMA_CONFIGURATION=hardware
ENV BEXHOMA_CLIENT=1
ENV BEXHOMA_BENCHMARK_RUN=1
ENV BEXHOMA_DBMS=hardware

# Scaling and parallelism
ENV BEXHOMA_NUM_PODS=1
ENV BEXHOMA_CHILD=1
ENV BEXHOMA_RNGSEED=123

# Pod synchronisation
ENV BEXHOMA_TIME_START=0
ENV BEXHOMA_TIME_NOW=0

# SUT connection
# BEXHOMA_HOST is injected at runtime by bexhoma's manifest builder
# (configurations/manifest.py) with the SUT's real k8s service DNS name.
ENV BEXHOMA_SUT_USER=bench
ENV BEXHOMA_SUT_KEY=/root/.ssh/id_ed25519

# Hardware benchmark parameters
ENV HARDWARE_TYPE=sysbench
ENV HARDWARE_THREADS=4
ENV HARDWARE_TEST_DIR=/database/fio-test
ENV HARDWARE_SIZE=1G
ENV HARDWARE_DURATION=30

# fio workload parameters (HARDWARE_TYPE=fio only)
ENV HARDWARE_FIO_RW=randrw
ENV HARDWARE_FIO_BS=8k
ENV HARDWARE_FIO_IODEPTH=1
ENV HARDWARE_FIO_NUMJOBS=1
ENV HARDWARE_FIO_ENGINE=sync
ENV HARDWARE_FIO_FSYNC=0
ENV HARDWARE_FIO_RWMIXREAD=50

######################################################################################
# Install SSH client, redis-cli and jq (for fio JSON result parsing)
######################################################################################
RUN apk add --no-cache openssh-client bash redis jq

######################################################################################
# Install SSH private key for SUT access
######################################################################################
RUN mkdir -p /root/.ssh && chmod 700 /root/.ssh
COPY bench_key /root/.ssh/id_ed25519
RUN chmod 600 /root/.ssh/id_ed25519

######################################################################################
# Copy benchmark scripts and entrypoint
######################################################################################
COPY run_sysbench.sh /usr/local/bin/run_sysbench.sh
COPY run_fio.sh /usr/local/bin/run_fio.sh
RUN chmod +x /usr/local/bin/run_sysbench.sh /usr/local/bin/run_fio.sh

COPY benchmarker.sh /benchmarker.sh
RUN chmod +x /benchmarker.sh

CMD ["/bin/bash", "-c", "/benchmarker.sh"]
