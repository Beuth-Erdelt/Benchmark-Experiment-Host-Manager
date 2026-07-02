######################################################################################
# Dockerfile for Bexhoma - Hardware Benchmarks
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma SUT running hardware workloads.
#
# Base Image: alpine:3.20
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2025-05-18
# Version: 1.0
# Description: Runs the HammerDB timed TPC-C driver against a target DBMS.
#   Configuration is supplied via environment variables.
#   A Redis message queue is consulted for pod-assignment details.
#   redis-tools is installed for queue interaction.
######################################################################################
FROM alpine:3.20

######################################################################################
# Environment variables — runtime configuration
######################################################################################
# Scaling and parallelism
ENV SF=1
ENV BEXHOMA_NUM_PODS=4
ENV BEXHOMA_CHILD=1
ENV BEXHOMA_RNGSEED=123

# Target DBMS connection
ENV BEXHOMA_DBMS_TYPE=postgresql
ENV BEXHOMA_HOST=www.example.com
ENV BEXHOMA_PORT=5432
ENV BEXHOMA_USER=postgres
ENV BEXHOMA_PASSWORD=postgres
ENV BEXHOMA_DATABASE=tpcc

# Bexhoma experiment identity
ENV BEXHOMA_DBMS=postgresql
ENV BEXHOMA_CONFIGURATION=postgresql
ENV BEXHOMA_CONNECTION=postgresql
ENV BEXHOMA_EXPERIMENT=12345
ENV BEXHOMA_EXPERIMENT_RUN=1
ENV BEXHOMA_CLIENT=1

# Pod synchronisation
ENV BEXHOMA_TIME_START=0
ENV BEXHOMA_TIME_NOW=0

RUN apk add --no-cache openssh fio sysbench \
    && ssh-keygen -A \
    && adduser -D -s /bin/sh bench \
    && mkdir -p /home/bench/.ssh \
    && chmod 700 /home/bench/.ssh

COPY bench_key.pub /home/bench/.ssh/authorized_keys
RUN chown -R bench:bench /home/bench/.ssh \
    && chmod 600 /home/bench/.ssh/authorized_keys

COPY sshd_entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 22
ENTRYPOINT ["/entrypoint.sh"]