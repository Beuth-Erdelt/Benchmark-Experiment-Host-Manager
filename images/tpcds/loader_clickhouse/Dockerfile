######################################################################################
# Dockerfile for Bexhoma - Loader TPC-DS ClickHouse
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma loader for TPC-DS data into ClickHouse.
#
# Base Image: clickhouse/clickhouse-server:26.8.34.13 (same version as the SUT templates)
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2026-10-23
# Version: 1.0
# Description: This container loads pre-generated TPC-DS .dat files into ClickHouse using
# clickhouse-client INSERT ... FORMAT CSV over the native protocol. Only the client is
# used; the server of the base image does not start. redis-cli is installed via apt.
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
    BEXHOMA_CHILD=1 \
    BEXHOMA_RNGSEED=123

# Target DBMS connection
ENV BEXHOMA_URL=jdbc:clickhouse://localhost:8123/default \
    BEXHOMA_HOST=www.example.com \
    BEXHOMA_PORT=9091 \
    CLICKHOUSE_PORT=9000 \
    BEXHOMA_JAR=clickhouse-jdbc-0.11.0-all-dependencies.jar \
    BEXHOMA_DRIVER=com.clickhouse.jdbc.Driver \
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
    TPCDS_TABLE=""

######################################################################################
# Working directory and data folder
######################################################################################
WORKDIR /tmp
RUN mkdir -p /tmp/tpcds

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
