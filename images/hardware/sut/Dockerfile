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
    && mkdir -p /home/bench/.ssh \
    && chmod 700 /home/bench/.ssh

######################################################################################
# Install benchmarker public key for passwordless SSH access
######################################################################################
COPY bench_key.pub /home/bench/.ssh/authorized_keys
RUN chown -R bench:bench /home/bench/.ssh \
    && chmod 600 /home/bench/.ssh/authorized_keys

######################################################################################
# Copy entrypoint and expose SSH port
######################################################################################
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 22
ENTRYPOINT ["/entrypoint.sh"]
