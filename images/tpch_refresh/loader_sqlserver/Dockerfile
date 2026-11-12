######################################################################################
# Dockerfile for Bexhoma - TPC-H Refresh Loader SQL Server
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma TPC-H refresh stream benchmarker
# that applies RF1 (INSERT) and RF2 (DELETE) operations to a SQL Server database.
# It reads pre-generated update files from /data/tpch-refresh/SF<SF>/ on the PVC.
#
# Base Image: ubuntu:22.04
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2026-11-11
# Version: 1.0
# Description: Applies TPCH_REFRESH_STREAMS pairs of RF1+RF2 starting at
# TPCH_REFRESH_STREAM_OFFSET+1. Uses bcp for RF1 and a staging table for RF2
# (mssql-tools18 from packages.microsoft.com). Synchronises with the query-stream
# benchmarker via Redis round counter. Emits BEXHOMA_DURATION/START/END.
######################################################################################
FROM ubuntu:22.04

######################################################################################
# Install dependencies
######################################################################################
# packages-microsoft-prod.deb installs the signing key and the source list together
# (the prod.list alone names no keyring: apt then fails with NO_PUBKEY EB3E94ADBE1229CF)
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates redis-tools \
    && curl -fsSL -o /tmp/packages-microsoft-prod.deb https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb \
    && dpkg -i /tmp/packages-microsoft-prod.deb \
    && rm /tmp/packages-microsoft-prod.deb \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql18 mssql-tools18 unixodbc \
    && rm -rf /var/lib/apt/lists/*
ENV PATH="${PATH}:/opt/mssql-tools18/bin"

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
ENV BEXHOMA_PORT=1433
ENV BEXHOMA_USER=sa
ENV BEXHOMA_PASSWORD=""
ENV BEXHOMA_DATABASE=tpch
ENV BEXHOMA_SCHEMA=""

# Bexhoma experiment identity
ENV BEXHOMA_CONNECTION=sqlserver
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
