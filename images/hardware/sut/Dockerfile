######################################################################################
# Dockerfile for Bexhoma - SUT Hardware
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma SUT that accepts hardware benchmark
# commands from the benchmarker container via SSH.
#
# Base Image: alpine:3.20
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2025-05-18
# Version: 1.0
# Description: Runs an SSH daemon and exposes sysbench and fio to the benchmarker
#   container. The benchmarker connects via SSH and triggers workloads remotely.
#   Also starts a fixed pool of persistent sockperf server instances (see below),
#   one pair (UDP+TCP) per port, so that several benchmarker pods can each reach
#   a dedicated server inside this same SUT pod. No Redis or Bexhoma experiment
#   coordination takes place in this image.
######################################################################################

######################################################################################
# Build sockperf from source (not packaged for Alpine/musl)
######################################################################################
FROM alpine:3.20 AS sockperf-builder
RUN apk add --no-cache git gcc g++ make automake autoconf libtool linux-headers musl-dev
RUN git clone --depth 1 https://github.com/Mellanox/sockperf.git /src
WORKDIR /src
# musl provides no <execinfo.h>/backtrace(); os_printf_backtrace() is only used
# for diagnostic stack traces on fatal-error paths (common.cpp), not core
# functionality, so it is patched to a no-op instead of vendoring libexecinfo.
# musl's headers are also stricter than glibc's about transitive includes, so
# two files need an explicit #include that glibc pulls in implicitly.
RUN sed -i '/AC_SEARCH_LIBS(\[backtrace\]/d' configure.ac \
    && sed -i '/#include <execinfo.h>/d' src/os_abstract.h \
    && awk '/^void os_printf_backtrace\(void\) \{/{print; print "}"; f=1; next} f && /^\}/{f=0; next} f{next} {print}' src/os_abstract.cpp > /tmp/os_abstract.cpp \
    && mv /tmp/os_abstract.cpp src/os_abstract.cpp \
    && sed -i '1i #include <cstdio>' src/vma-xlio-redirect.cpp \
    && sed -i '1i #include <sys/time.h>' src/ticks.h
RUN ./autogen.sh && ./configure && make -j$(nproc)

FROM alpine:3.20

######################################################################################
# Install SSH server, fio, sysbench, and sockperf's runtime dependency (libstdc++)
######################################################################################
RUN apk add --no-cache openssh fio sysbench libstdc++ \
    && ssh-keygen -A \
    && adduser -D -s /bin/sh bench \
    && echo "bench:bench" | chpasswd \
    && mkdir -p /home/bench/.ssh \
    && chmod 700 /home/bench/.ssh \
    && printf 'PasswordAuthentication no\nUsePAM no\n' >> /etc/ssh/sshd_config

COPY --from=sockperf-builder /src/sockperf /usr/local/bin/sockperf

######################################################################################
# Install benchmarker public key for passwordless SSH access
######################################################################################
COPY bench_key.pub /home/bench/.ssh/authorized_keys
RUN chown -R bench:bench /home/bench \
    && chmod 700 /home/bench \
    && chmod 700 /home/bench/.ssh \
    && chmod 600 /home/bench/.ssh/authorized_keys

######################################################################################
# Base folder for fio/sysbench benchmarks
######################################################################################
# World-writable so fio (run over SSH as "bench") can use it whether or not
# k8s/deploymenttemplate-Hardware.yml's PVC ends up mounted here — with no PVC
# (use_storage()=False, e.g. no -rst flag passed to hardware.py) this directory
# is just part of the container's own ephemeral filesystem; with a PVC it's
# the mount point (also chmod'd by that manifest's initContainer).
RUN mkdir -p /database \
    && chmod 777 /database

######################################################################################
# sockperf server pool
######################################################################################
# One UDP and one TCP sockperf server is started per port in the range
# [SOCKPERF_BASE_PORT, SOCKPERF_BASE_PORT + SOCKPERF_NUM_SERVERS), so that
# several benchmarker pods (BEXHOMA_NUM_PODS > 1) can each connect to their
# own dedicated server (see images/hardware/benchmarker/run_sockperf.sh, which
# picks a port from BEXHOMA_CHILD) instead of contending on a shared socket.
# These are static defaults, not per-experiment values — every other SUT env
# var in this image family is static too (see k8s/deploymenttemplate-Hardware.yml).
ENV SOCKPERF_NUM_SERVERS=16
ENV SOCKPERF_BASE_PORT=20000

######################################################################################
# Copy entrypoint and expose SSH + sockperf ports
######################################################################################
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 22
# 20000-20015/tcp and 20000-20015/udp (SOCKPERF_BASE_PORT..+SOCKPERF_NUM_SERVERS-1)
EXPOSE 20000-20015
EXPOSE 20000-20015/udp
ENTRYPOINT ["/entrypoint.sh"]
