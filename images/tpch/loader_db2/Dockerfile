######################################################################################
# Dockerfile for Bexhoma - Loader TPC-H IBM Db2
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma loader for TPC-H data into
# IBM Db2 (Community Edition).
#
# Base Image: python:3.12-slim
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2026-11-11
# Version: 1.0
# Description: This container loads pre-generated TPC-H .tbl files into Db2 as
# remote external tables (INSERT ... SELECT * FROM EXTERNAL ... REMOTESOURCE 'YES',
# load.py). The child index is read from /tmp/tpch/BEXHOMA_CHILD written by the
# generator pod. nation and region are only loaded by pod 1.
# ibm_db installs the IBM Data Server Driver for ODBC and CLI (clidriver, a
# redistributable driver of IBM, see clidriver/license in the image); redis-tools
# is installed for the synchronisation counters (redis-cli).
######################################################################################
FROM python:3.12-slim

######################################################################################
# Install dependencies
######################################################################################
RUN apt-get update \
    && apt-get install -y --no-install-recommends redis-tools libxml2 \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir ibm_db==3.2.6

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
ENV BEXHOMA_PORT=50000
ENV BEXHOMA_USER=db2inst1
ENV BEXHOMA_PASSWORD=""
# Database the tables are in
ENV BEXHOMA_DATABASE=bexhoma
# Schema of the tables; empty = default schema of BEXHOMA_USER
ENV BEXHOMA_SCHEMA=""
# Unused/compatibility
ENV BEXHOMA_URL=jdbc:db2://localhost:50000/bexhoma
ENV BEXHOMA_JAR=jcc-12.1.5.0.jar
ENV BEXHOMA_DRIVER=com.ibm.db2.jcc.DB2Driver

# Loading: column delimiter, lines per transaction, attempts per chunk on connection errors
ENV DB2_DELIMITER="|"
ENV DB2_LOAD_CHUNK_ROWS=200000
ENV DB2_LOAD_RETRIES=10

# Bexhoma experiment identity
ENV BEXHOMA_CONNECTION=db2
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
# Loader scripts
######################################################################################
COPY ./loader.sh /tmp/loader.sh
COPY ./load.py /tmp/load.py
RUN chmod +x /tmp/loader.sh

######################################################################################
# Entrypoint
######################################################################################
CMD ["/bin/bash", "-c", "/tmp/loader.sh"]
