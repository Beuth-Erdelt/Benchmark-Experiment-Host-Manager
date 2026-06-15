######################################################################################
# Dockerfile for Bexhoma - TPC-H Refresh Loader MySQL
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma TPC-H refresh stream benchmarker
# that applies RF1 (INSERT) and RF2 (DELETE) operations to a MySQL database.
# It reads pre-generated update files from /data/tpch-refresh/SF<SF>/ on the PVC.
#
# Base Image: debian:stable-20240110-slim
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2025-06-15
# Version: 1.0
# Description: Applies TPCH_REFRESH_STREAMS pairs of RF1+RF2 starting at
# TPCH_REFRESH_STREAM_OFFSET+1. Uses mysql LOAD DATA LOCAL INFILE for RF1 and
# a temporary table for RF2. Synchronises with the query-stream benchmarker via
# Redis round counter. Emits BEXHOMA_DURATION/START/END.
######################################################################################
FROM debian:stable-20240110-slim

######################################################################################
# Install build dependencies and build Redis CLI
######################################################################################
RUN apt-get clean \
    && apt-get -y update \
    && apt-get clean all

RUN apt-get install -y --no-install-recommends build-essential wget \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q http://download.redis.io/redis-stable.tar.gz \
    && tar xvzf redis-stable.tar.gz \
    && cd redis-stable \
    && make redis-cli \
    && cp src/redis-cli /usr/local/bin/ \
    && chmod 755 /usr/local/bin/redis-cli \
    && cd / \
    && rm -rf redis-stable redis-stable.tar.gz

######################################################################################
# Set locale
######################################################################################
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends locales ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG=en_US.utf8

######################################################################################
# Install MySQL client
######################################################################################
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

######################################################################################
# Environment variables — runtime configuration
######################################################################################
# Scaling
ENV SF=1
ENV TPCH_REFRESH_STREAMS=1
ENV TPCH_REFRESH_STREAM_OFFSET=0

# Data storage
ENV STORE_RAW_DATA=1

# Target DBMS connection
ENV BEXHOMA_HOST=www.example.com
ENV BEXHOMA_PORT=3306
ENV BEXHOMA_USER=root
ENV BEXHOMA_PASSWORD=root
# MySQL uses BEXHOMA_VOLUME as the database name (set at runtime)
ENV BEXHOMA_VOLUME=tpch
ENV BEXHOMA_DATABASE=tpch

# Bexhoma experiment identity
ENV BEXHOMA_CONNECTION=mysql
ENV BEXHOMA_EXPERIMENT=12345
ENV BEXHOMA_EXPERIMENT_RUN=1
ENV BEXHOMA_CONFIGURATION=""
ENV BEXHOMA_CLIENT=1
ENV BEXHOMA_BENCHMARK_RUN=2

######################################################################################
# Working directory
######################################################################################
WORKDIR /tmp

######################################################################################
# Loader script
######################################################################################
COPY ./loader.sh /tmp/loader.sh
RUN chmod +x /tmp/loader.sh

######################################################################################
# Entrypoint
######################################################################################
CMD ["/bin/bash", "-c", "/tmp/loader.sh"]
