######################################################################################
# Dockerfile for Bexhoma - Generator TPC-H
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma component "generator".
#
# Base Image: debian:stable-20251103-slim
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2025-05-18
# Version: 1.0
# Description: This container runs a driver for a benchmark. Data is generated and loaded.
# The configuration is given by environment variables.
# A redis queue is consulted for further details.
# Redis client is installed.
# TPC-H generator is copied from external folder.
######################################################################################
FROM debian:stable-20251103-slim

############################
# Install build dependencies
############################
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        build-essential \
        wget \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

############################
# Build Redis CLI
############################
RUN wget -q http://download.redis.io/redis-stable.tar.gz \
    && tar xvzf redis-stable.tar.gz \
    && cd redis-stable \
    && make redis-cli \
    && cp src/redis-cli /usr/local/bin/ \
    && chmod 755 /usr/local/bin/redis-cli

############################
# Copy TPC files and scripts
############################
COPY ./tpc_eula.txt ./tpc_eula.txt
COPY ./dists.dss /tmp/dists.dss
COPY ./dbgen /tmp/dbgen
RUN chmod +x /tmp/dbgen

COPY ./generator.sh /tmp/generator.sh
RUN chmod +x /tmp/generator.sh

############################
# Environment variables
############################
ENV SF=1 \
    BEXHOMA_NUM_PODS=4 \
    BEXHOMA_CHILD=1 \
    BEXHOMA_RNGSEED=123 \
    BEXHOMA_URL=jdbc:mysql://localhost:3306/ycsb \
    BEXHOMA_HOST=www.example.com \
    BEXHOMA_PORT=3306 \
    BEXHOMA_JAR=mysql-connector-j-8.0.31.jar \
    BEXHOMA_DRIVER=com.mysql.cj.jdbc.Driver \
    BEXHOMA_CONNECTION=mysql \
    BEXHOMA_EXPERIMENT=12345 \
    BEXHOMA_EXPERIMENT_RUN=1 \
    BEXHOMA_USER=root \
    BEXHOMA_PASSWORD=root \
    BEXHOMA_DATABASE=demo \
    STORE_RAW_DATA=0 \
    STORE_RAW_DATA_RECREATE=0 \
    TRANSFORM_RAW_DATA=1 \
    BEXHOMA_SYNCH_GENERATE=0

############################
# Working directory
############################
WORKDIR /tmp
RUN mkdir -p /tmp/tpch

############################
# Entrypoint
############################
CMD ["/bin/bash", "-c", "/tmp/generator.sh"]
