######################################################################################
# Dockerfile for Bexhoma - TPC-H Refresh Loader Oracle Database
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma TPC-H refresh stream benchmarker
# that applies RF1 (INSERT) and RF2 (DELETE) operations to an Oracle database.
# It reads pre-generated update files from /data/tpch-refresh/SF<SF>/ on the PVC.
#
# Base Image: oraclelinux:9-slim
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2026-11-11
# Version: 1.0
# Description: Applies TPCH_REFRESH_STREAMS pairs of RF1+RF2 starting at
# TPCH_REFRESH_STREAM_OFFSET+1. Uses SQL*Loader for RF1 and a staging table for
# RF2 (sqlldr and sqlplus of the Oracle Instant Client, from the Oracle Linux yum
# repository). Synchronises with the query-stream benchmarker via Redis round
# counter. Emits BEXHOMA_DURATION/START/END.
######################################################################################
FROM oraclelinux:9-slim

######################################################################################
# Install dependencies
######################################################################################
RUN microdnf -y install oracle-instantclient-release-23ai-el9 \
    && microdnf -y install oracle-instantclient-basic oracle-instantclient-sqlplus oracle-instantclient-tools \
    && microdnf -y install redis findutils \
    && microdnf clean all
# the rpm links only sqlplus to /usr/bin; sqlldr is in the bin folder of the client
ENV PATH="${PATH}:/usr/lib/oracle/23/client64/bin"

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
ENV BEXHOMA_PORT=1521
ENV BEXHOMA_USER=bexhoma
ENV BEXHOMA_PASSWORD=""
# Schema (= user) the tables are in
ENV BEXHOMA_DATABASE=bexhoma
ENV BEXHOMA_SCHEMA=""
# Service name of the pluggable database
ENV ORACLE_SERVICE=FREEPDB1

# Bexhoma experiment identity
ENV BEXHOMA_CONNECTION=oracle
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
# Loader script and SQL*Loader control files
######################################################################################
COPY ./loader.sh /tmp/loader.sh
COPY ./ctl /tmp/ctl
RUN chmod +x /tmp/loader.sh

######################################################################################
# Entrypoint
######################################################################################
CMD ["/bin/bash", "-c", "/tmp/loader.sh"]
