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
#   a dedicated server inside this same SUT pod, and a single netserver instance
#   (netserver forks a child per incoming test session natively, so one instance
#   already handles many concurrent netperf clients — see run_netperf.sh for how
#   each concurrent client instance is given its own fixed data port out of a
#   shared pool). No Redis or Bexhoma experiment coordination takes place in this
#   image.
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

######################################################################################
# Build netperf from source (not packaged for Alpine/musl either). Builds cleanly on
# Alpine 3.20/musl with no source patches needed (only doc/makeinfo generation fails,
# so only src/ is built) — verified locally against upstream HewlettPackard/netperf.
######################################################################################
FROM alpine:3.20 AS netperf-builder
RUN apk add --no-cache git gcc g++ make automake autoconf libtool linux-headers musl-dev
RUN git clone --depth 1 https://github.com/HewlettPackard/netperf.git /src
WORKDIR /src
RUN ./autogen.sh && ./configure --enable-histogram
RUN make -C src -j$(nproc)

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
    && printf 'PasswordAuthentication no\n' >> /etc/ssh/sshd_config

COPY --from=sockperf-builder /src/sockperf /usr/local/bin/sockperf
COPY --from=netperf-builder /src/src/netserver /usr/local/bin/netserver

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
# netserver + fixed data-port pool
######################################################################################
# A single netserver instance listens on NETPERF_CONTROL_PORT and forks a child per
# incoming test session (see netserver.c's spawn_child()), so it natively serves many
# concurrent netperf clients without needing a server pool like sockperf's above. Each
# client instance still requests its own data-connection port explicitly (netperf's
# test-specific "-P local,remote" option; verified against upstream netserver that the
# remote value is honored) out of [NETPERF_DATA_BASE_PORT, NETPERF_DATA_BASE_PORT +
# NETPERF_DATA_NUM_PORTS) — required because the k8s Service in
# k8s/deploymenttemplate-Hardware.yml only forwards explicitly declared ports, so an
# OS-assigned ephemeral data port would be unreachable through it. See
# images/hardware/benchmarker/run_netperf.sh for how each pod's concurrent client
# instances are assigned a disjoint slice of this pool via BEXHOMA_CHILD.
ENV NETPERF_CONTROL_PORT=12865
ENV NETPERF_DATA_BASE_PORT=30000
ENV NETPERF_DATA_NUM_PORTS=64

######################################################################################
# Copy entrypoint and expose SSH + sockperf + netperf ports
######################################################################################
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 22
# 20000-20015/tcp and 20000-20015/udp (SOCKPERF_BASE_PORT..+SOCKPERF_NUM_SERVERS-1)
EXPOSE 20000-20015
EXPOSE 20000-20015/udp
# netperf control port, plus the fixed data-port pool (NETPERF_DATA_BASE_PORT..
# +NETPERF_DATA_NUM_PORTS-1) in both protocols (TCP_RR needs TCP, UDP_RR needs UDP)
EXPOSE 12865
EXPOSE 30000-30063
EXPOSE 30000-30063/udp
ENTRYPOINT ["/entrypoint.sh"]
