######################################################################################
# Dockerfile for Bexhoma - Benchmarker Hardware
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma benchmarker running sysbench, fio, or
# sockperf hardware workloads against a SUT container.
#
# Base Image: alpine:3.20
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2025-05-18
# Version: 1.0
# Description: Connects to a SUT container via SSH and runs sysbench (CPU/memory),
#   a single ENV-configurable fio (disk I/O) workload, or a sockperf (network
#   latency/throughput) workload directly over the SUT's sockperf port. Configuration
#   is supplied via environment variables. A Redis message queue is consulted for
#   pod-assignment details. redis-cli and openssh-client are installed for queue
#   interaction and SSH access; jq parses fio's JSON result into KEY:VALUE metrics
#   and a CSV summary.
######################################################################################

######################################################################################
# Build sockperf from source (not packaged for Alpine/musl) — same build as
# images/hardware/sut/Dockerfile, kept in sync with it.
######################################################################################
FROM alpine:3.20 AS sockperf-builder
RUN apk add --no-cache git gcc g++ make automake autoconf libtool linux-headers musl-dev
RUN git clone --depth 1 https://github.com/Mellanox/sockperf.git /src
WORKDIR /src
RUN sed -i '/AC_SEARCH_LIBS(\[backtrace\]/d' configure.ac \
    && sed -i '/#include <execinfo.h>/d' src/os_abstract.h \
    && awk '/^void os_printf_backtrace\(void\) \{/{print; print "}"; f=1; next} f && /^\}/{f=0; next} f{next} {print}' src/os_abstract.cpp > /tmp/os_abstract.cpp \
    && mv /tmp/os_abstract.cpp src/os_abstract.cpp \
    && sed -i '1i #include <cstdio>' src/vma-xlio-redirect.cpp \
    && sed -i '1i #include <sys/time.h>' src/ticks.h
RUN ./autogen.sh && ./configure && make -j$(nproc)

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

# Multi-tenancy (container tenancy only — see -mtb/-mtn in hardware.py)
ENV BEXHOMA_TENANT_BY=""
ENV BEXHOMA_TENANT_NUM=""

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

# sockperf workload parameters (HARDWARE_TYPE=sockperf only)
ENV HARDWARE_SOCKPERF_MODE=ul
ENV HARDWARE_SOCKPERF_PROTOCOL=udp
ENV HARDWARE_SOCKPERF_MSGSIZE=64
ENV HARDWARE_SOCKPERF_MPS=max
# Must stay numerically in sync with SOCKPERF_BASE_PORT/SOCKPERF_NUM_SERVERS in
# images/hardware/sut/Dockerfile — same kind of manually-synced constant as
# SSH_PORT=9091 already is between run_fio.sh/run_sysbench.sh and the SUT's
# k8s Service (see k8s/deploymenttemplate-Hardware.yml).
ENV SOCKPERF_BASE_PORT=20000
ENV SOCKPERF_NUM_SERVERS=16

######################################################################################
# Install SSH client, redis-cli, jq (for fio JSON result parsing), and
# libstdc++ (sockperf's only runtime dependency)
######################################################################################
RUN apk add --no-cache openssh-client bash redis jq libstdc++

######################################################################################
# Install sockperf binary (built in the sockperf-builder stage above)
######################################################################################
COPY --from=sockperf-builder /src/sockperf /usr/local/bin/sockperf

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
COPY run_sockperf.sh /usr/local/bin/run_sockperf.sh
RUN chmod +x /usr/local/bin/run_sysbench.sh /usr/local/bin/run_fio.sh /usr/local/bin/run_sockperf.sh

COPY benchmarker.sh /benchmarker.sh
RUN chmod +x /benchmarker.sh

CMD ["/bin/bash", "-c", "/benchmarker.sh"]
