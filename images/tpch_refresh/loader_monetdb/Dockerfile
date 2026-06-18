######################################################################################
# Dockerfile for Bexhoma - TPC-H Refresh Loader MonetDB
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma TPC-H refresh stream benchmarker
# that applies RF1 (INSERT) and RF2 (DELETE) operations to a MonetDB database.
# It reads pre-generated update files from /data/tpch-refresh/SF<SF>/ on the PVC.
#
# Base Image: monetdb/monetdb:Dec2025
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2025-06-16
# Version: 1.0
# Description: Applies TPCH_REFRESH_STREAMS pairs of RF1+RF2 starting at
# TPCH_REFRESH_STREAM_OFFSET+1. Uses mclient COPY N RECORDS INTO ... FROM STDIN
# for RF1 and a stdin-piped session for RF2 so the temporary table persists.
# Synchronises with the query-stream benchmarker via Redis round counter.
# Emits BEXHOMA_DURATION/START/END.
######################################################################################
FROM monetdb/monetdb:Dec2025

######################################################################################
# Update system and install dependencies
######################################################################################
RUN yum -y update \
    && yum install -y \
        redis \
        gcc \
        wget \
    && yum clean all \
    && rm -rf /var/cache/yum

######################################################################################
# Environment variables — runtime configuration
######################################################################################
# Scaling
ENV SF=1 \
    TPCH_REFRESH_STREAMS=1 \
    TPCH_REFRESH_STREAM_OFFSET=0

# Data storage
ENV STORE_RAW_DATA=1

# Target DBMS connection
ENV BEXHOMA_HOST=www.example.com \
    BEXHOMA_PORT=3306 \
    BEXHOMA_USER=monetdb \
    BEXHOMA_PASSWORD=monetdb \
    BEXHOMA_DATABASE=tpch

# Bexhoma experiment identity
ENV BEXHOMA_CONNECTION=monetdb \
    BEXHOMA_EXPERIMENT=12345 \
    BEXHOMA_EXPERIMENT_RUN=1 \
    BEXHOMA_CONFIGURATION="" \
    BEXHOMA_CLIENT=1 \
    BEXHOMA_BENCHMARK_RUN=2

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
