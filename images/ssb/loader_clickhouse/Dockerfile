######################################################################################
# Dockerfile for Bexhoma - Loader SSB ClickHouse
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma loader for SSB data into ClickHouse.
#
# Base Image: clickhouse/clickhouse-server:26.8.34.13 (same version as the SUT templates)
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2026-10-25
# Version: 1.0
# Description: This container loads pre-generated SSB .tbl files into ClickHouse using
# clickhouse-client INSERT ... FORMAT CSV over the native protocol. Only the client is
# used; the server of the base image does not start. Each pod loads the files of its
# own folder; the folder of child 1 also holds the dimensions. With
# SSB_SCHEMA_VARIANT=flat it loads lineorder_flat. redis-cli is installed via apt.
######################################################################################
FROM clickhouse/clickhouse-server:26.8.34.13

######################################################################################
# Update system and install dependencies
######################################################################################
RUN apt-get update \
    && apt-get install -y --no-install-recommends redis-tools \
    && rm -rf /var/lib/apt/lists/*

######################################################################################
# Environment variables — runtime configuration
######################################################################################
# Scaling and parallelism
ENV SF=1 \
    BEXHOMA_NUM_PODS=4 \
    BEXHOMA_CHILD=1

# Target DBMS connection
ENV BEXHOMA_HOST=www.example.com \
    BEXHOMA_PORT=9091 \
    CLICKHOUSE_PORT=9000 \
    BEXHOMA_USER=default \
    BEXHOMA_PASSWORD= \
    BEXHOMA_DATABASE=default

# Bexhoma experiment identity
ENV BEXHOMA_CONNECTION=clickhouse \
    BEXHOMA_EXPERIMENT=12345 \
    BEXHOMA_EXPERIMENT_RUN=1 \
    BEXHOMA_CONFIGURATION="" \
    BEXHOMA_CLIENT=1

# Data storage and loading control
ENV STORE_RAW_DATA=0 \
    BEXHOMA_SYNCH_LOAD=0 \
    SSB_SCHEMA_VARIANT=normal \
    SSB_TABLE=""

######################################################################################
# Working directory and data folder
######################################################################################
WORKDIR /tmp
RUN mkdir -p /tmp/ssb

######################################################################################
# Loader script
######################################################################################
COPY ./loader.sh /tmp/loader.sh
RUN chmod +x /tmp/loader.sh

######################################################################################
# Entrypoint (replaces the server entrypoint of the base image)
######################################################################################
ENTRYPOINT []
CMD ["/bin/bash", "-c", "/tmp/loader.sh"]
