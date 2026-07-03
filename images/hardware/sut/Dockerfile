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
#   No Redis or Bexhoma experiment coordination takes place in this image.
######################################################################################
FROM alpine:3.20

######################################################################################
# Install SSH server, fio, and sysbench
######################################################################################
RUN apk add --no-cache openssh fio sysbench \
    && ssh-keygen -A \
    && adduser -D -s /bin/sh bench \
    && echo "bench:bench" | chpasswd \
    && mkdir -p /home/bench/.ssh \
    && chmod 700 /home/bench/.ssh \
    && printf 'PasswordAuthentication no\nUsePAM no\n' >> /etc/ssh/sshd_config

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
# Copy entrypoint and expose SSH port
######################################################################################
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 22
ENTRYPOINT ["/entrypoint.sh"]
