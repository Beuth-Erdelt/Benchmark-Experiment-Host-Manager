######################################################################################
# Dockerfile for Bexhoma - Benchmarker HammerDB
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma benchmarker running TPC-C workloads
# against an already-loaded DBMS using HammerDB.
#
# Base Image: tpcorg/hammerdb:v5.0
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
FROM tpcorg/hammerdb:v5.0

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

# HammerDB workload parameters
ENV HAMMERDB_TYPE=postgresql
ENV HAMMERDB_RAMPUP=2
ENV HAMMERDB_DURATION=5
ENV HAMMERDB_ITERATIONS=10000000
ENV HAMMERDB_VUSERS="1 2 4 8"
ENV HAMMERDB_NUM_VU=4
ENV HAMMERDB_MYSQL_ENGINE=innodb
ENV HAMMERDB_TIMEPROFILE=true
ENV HAMMERDB_ALLWAREHOUSES=false
ENV HAMMERDB_KEYANDTHINK=false

######################################################################################
# Install Redis client
######################################################################################
RUN apt update && apt install -y redis-tools && rm -rf /var/lib/apt/lists/*

######################################################################################
# Create temp TPC-C directory and copy entrypoint script
######################################################################################
RUN mkdir -p /tmp/tpcc

COPY ./benchmarker.sh ./benchmarker.sh
RUN ["chmod", "+x", "./benchmarker.sh"]

CMD ["/bin/bash", "-c", "./benchmarker.sh"]
