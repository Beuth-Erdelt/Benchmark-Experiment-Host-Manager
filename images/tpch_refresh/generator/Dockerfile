######################################################################################
# Dockerfile for Bexhoma - Generator TPC-H Refresh Streams
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma generator for TPC-H refresh data.
# It generates update files (orders.tbl.uK, lineitem.tbl.uK, delete.K for K=1..N)
# using the pre-compiled dbgen binary and stores them on the persistent data volume.
#
# Base Image: debian:stable-20251103-slim
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2025-06-15
# Version: 1.0
# Description: Runs dbgen -U N to generate N TPC-H refresh sets into
# /data/tpch-refresh/SF<SF>/. Skips generation if the last required set already
# exists. redis-cli is built from source.
######################################################################################
FROM debian:stable-20251103-slim

######################################################################################
# Install build dependencies
######################################################################################
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        build-essential \
        wget \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

######################################################################################
# Build Redis CLI from source
######################################################################################
RUN wget -q http://download.redis.io/redis-stable.tar.gz \
    && tar xvzf redis-stable.tar.gz \
    && cd redis-stable \
    && make redis-cli \
    && cp src/redis-cli /usr/local/bin/ \
    && chmod 755 /usr/local/bin/redis-cli \
    && cd / \
    && rm -rf redis-stable redis-stable.tar.gz

######################################################################################
# Copy TPC-H generator files
# dbgen and dists.dss must be copied from images/tpch/generator/ before building.
######################################################################################
COPY ./tpc_eula.txt ./tpc_eula.txt
COPY ./dists.dss /tmp/dists.dss
COPY ./dbgen /tmp/dbgen
RUN chmod +x /tmp/dbgen

COPY ./generator.sh /tmp/generator.sh
RUN chmod +x /tmp/generator.sh

######################################################################################
# Environment variables — runtime configuration
######################################################################################
# Scaling
ENV SF=1
ENV TPCH_REFRESH_STREAMS=1
ENV TPCH_REFRESH_STREAM_OFFSET=0

# Data storage
ENV STORE_RAW_DATA=1

# Target DBMS connection (declared for compatibility; not used during generation)
ENV BEXHOMA_HOST=www.example.com
ENV BEXHOMA_PORT=5432
ENV BEXHOMA_USER=postgres
ENV BEXHOMA_PASSWORD=postgres
ENV BEXHOMA_DATABASE=tpch
ENV BEXHOMA_SCHEMA=public

# Bexhoma experiment identity
ENV BEXHOMA_CONNECTION=postgresql
ENV BEXHOMA_EXPERIMENT=12345
ENV BEXHOMA_EXPERIMENT_RUN=1
ENV BEXHOMA_CONFIGURATION=""
ENV BEXHOMA_CLIENT=1
ENV BEXHOMA_BENCHMARK_RUN=2

######################################################################################
# Working directory and data folder
######################################################################################
WORKDIR /tmp
RUN mkdir -p /tmp/tpch-refresh

######################################################################################
# Entrypoint
######################################################################################
CMD ["/bin/bash", "-c", "/tmp/generator.sh"]
