######################################################################################
# Dockerfile for Bexhoma - Loader TPC-H SQL Server
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma loader for TPC-H data into
# Microsoft SQL Server.
#
# Base Image: ubuntu:22.04
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2026-11-11
# Version: 1.0
# Description: This container loads pre-generated TPC-H .tbl files into SQL Server
# via bcp (mssql-tools18). The child index is read from /tmp/tpch/BEXHOMA_CHILD
# written by the generator pod. nation and region are only loaded by pod 1.
# The tools are installed from packages.microsoft.com (ACCEPT_EULA of msodbcsql18
# and mssql-tools18); redis-tools is installed for the synchronisation counters.
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
# Scaling and parallelism
ENV SF=1
ENV BEXHOMA_NUM_PODS=4
ENV BEXHOMA_CHILD=1
ENV BEXHOMA_RNGSEED=123

# Target DBMS connection
ENV BEXHOMA_HOST="www.example.com"
ENV BEXHOMA_PORT=1433
ENV BEXHOMA_USER=sa
ENV BEXHOMA_PASSWORD=""
ENV BEXHOMA_DATABASE=tpch
ENV BEXHOMA_SCHEMA=""
# Unused/compatibility
ENV BEXHOMA_URL=jdbc:sqlserver://localhost:1433
ENV BEXHOMA_JAR=mssql-jdbc-12.8.1.jre8.jar
ENV BEXHOMA_DRIVER=com.microsoft.sqlserver.jdbc.SQLServerDriver

# Bexhoma experiment identity
ENV BEXHOMA_CONNECTION=sqlserver
ENV BEXHOMA_EXPERIMENT=12345
ENV BEXHOMA_EXPERIMENT_RUN=1
ENV BEXHOMA_CONFIGURATION=""
ENV BEXHOMA_CLIENT=1

# Multi-tenancy
ENV BEXHOMA_TENANT_BY=""
ENV BEXHOMA_TENANT_NUM=""
ENV BEXHOMA_NUM_PODS_TOTAL=""

# Data storage and loading control
ENV STORE_RAW_DATA=0
ENV BEXHOMA_SYNCH_LOAD=0
ENV TPCH_TABLE=""

######################################################################################
# Working directory and data folder
######################################################################################
WORKDIR /tmp
RUN mkdir -p /tmp/tpch

######################################################################################
# Loader script
######################################################################################
COPY ./loader.sh /tmp/loader.sh
RUN chmod +x /tmp/loader.sh

######################################################################################
# Entrypoint
######################################################################################
CMD ["/bin/bash", "-c", "/tmp/loader.sh"]
