######################################################################################
# Dockerfile for Bexhoma - Loader TPC-H refresh stream ClickHouse
######################################################################################
#
# This Dockerfile builds an image for the main container of the TPC-H refresh benchmarker
# job (benchmark_run=2) against ClickHouse and ClickHouseCluster.
#
# Base Image: clickhouse/clickhouse-server:26.8.34.13 (same version as the SUT templates)
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Version: 1.0
# Description: Applies the TPC-H refresh functions RF1 (INSERT ... FORMAT CSV) and
# RF2 (lightweight DELETE by order key) from the update files that the generator
# initContainer left on the PVC. Only the client is used; the server of the base image does
# not start. redis-cli is installed via apt to synchronise with the query stream.
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
# Scaling and refresh sets
ENV SF=1 \
    TPCH_REFRESH_STREAMS=1 \
    TPCH_REFRESH_STREAM_OFFSET=0 \
    STORE_RAW_DATA=1

# Target DBMS connection (BEXHOMA_PORT is the HTTP port of the service, CLICKHOUSE_PORT the native one)
ENV BEXHOMA_HOST=www.example.com \
    BEXHOMA_PORT=9091 \
    CLICKHOUSE_PORT=9000 \
    BEXHOMA_DATABASE=default \
    BEXHOMA_CLICKHOUSE_CLUSTER=""

# Bexhoma experiment identity
ENV BEXHOMA_CONNECTION=clickhouse \
    BEXHOMA_EXPERIMENT=12345 \
    BEXHOMA_EXPERIMENT_RUN=1 \
    BEXHOMA_CONFIGURATION="" \
    BEXHOMA_CLIENT=1 \
    BEXHOMA_BENCHMARK_RUN=2

######################################################################################
# Working directory and loader script
######################################################################################
WORKDIR /tmp
COPY ./loader.sh /tmp/loader.sh
RUN chmod +x /tmp/loader.sh

######################################################################################
# Entrypoint (replaces the server entrypoint of the base image)
######################################################################################
ENTRYPOINT []
CMD ["/bin/bash", "-c", "/tmp/loader.sh"]
