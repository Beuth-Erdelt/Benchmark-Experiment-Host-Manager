######################################################################################
# Dockerfile for Bexhoma - TPC-H Refresh Loader IBM Db2
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma TPC-H refresh stream benchmarker
# that applies RF1 (INSERT) and RF2 (DELETE) operations to an IBM Db2 database.
# It reads pre-generated update files from /data/tpch-refresh/SF<SF>/ on the PVC.
#
# Base Image: python:3.12-slim
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2026-11-11
# Version: 1.0
# Description: Applies TPCH_REFRESH_STREAMS pairs of RF1+RF2 starting at
# TPCH_REFRESH_STREAM_OFFSET+1. RF1 with load.py (the same as in
# images/tpch/loader_db2: remote external tables, one transaction per chunk),
# RF2 with rf2.py (one transaction, the delete file as a remote external table).
# ibm_db installs the IBM Data Server Driver for ODBC and CLI (redistributable).
# Synchronises with the query-stream benchmarker via Redis round counter.
# Emits BEXHOMA_DURATION/START/END.
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
# Refresh stream
ENV SF=1
ENV TPCH_REFRESH_STREAMS=1
ENV TPCH_REFRESH_STREAM_OFFSET=0
ENV STORE_RAW_DATA=1

# Target DBMS connection
ENV BEXHOMA_HOST=www.example.com
ENV BEXHOMA_PORT=50000
ENV BEXHOMA_USER=db2inst1
ENV BEXHOMA_PASSWORD=""
ENV BEXHOMA_DATABASE=bexhoma
ENV BEXHOMA_SCHEMA=""

# Loading: column delimiter, lines per transaction of RF1, attempts per chunk on connection errors
ENV DB2_DELIMITER="|"
ENV DB2_LOAD_CHUNK_ROWS=200000
ENV DB2_LOAD_RETRIES=10

# Bexhoma experiment identity
ENV BEXHOMA_CONNECTION=db2
ENV BEXHOMA_EXPERIMENT=12345
ENV BEXHOMA_EXPERIMENT_RUN=1
ENV BEXHOMA_CONFIGURATION=""
ENV BEXHOMA_CLIENT=1
ENV BEXHOMA_BENCHMARK_RUN=2

######################################################################################
# Working directory and scripts
######################################################################################
WORKDIR /tmp
COPY ./loader.sh /tmp/loader.sh
COPY ./load.py /tmp/load.py
COPY ./rf2.py /tmp/rf2.py
RUN chmod +x /tmp/loader.sh

######################################################################################
# Entrypoint
######################################################################################
CMD ["/bin/bash", "-c", "/tmp/loader.sh"]
