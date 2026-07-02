######################################################################################
# Dockerfile for Bexhoma - Benchmarker Hardware
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma benchmarker running sysbench and fio
# workloads againt a SUT container.
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

RUN apk add --no-cache openssh-client bash

COPY bench_key /root/.ssh/id_ed25519
RUN chmod 700 /root/.ssh 2>/dev/null || mkdir -p /root/.ssh && chmod 700 /root/.ssh
RUN chmod 600 /root/.ssh/id_ed25519

COPY run_sysbench.sh /usr/local/bin/run_sysbench.sh
COPY run_fio.sh /usr/local/bin/run_fio.sh
RUN chmod +x /usr/local/bin/run_sysbench.sh /usr/local/bin/run_fio.sh

ENTRYPOINT ["/bin/sh"]