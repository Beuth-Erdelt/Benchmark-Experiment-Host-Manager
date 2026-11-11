######################################################################################
# Dockerfile for Bexhoma - Loader TPC-H Oracle Database
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma loader for TPC-H data into
# Oracle Database (Free).
#
# Base Image: oraclelinux:9-slim
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2026-11-11
# Version: 1.0
# Description: This container loads pre-generated TPC-H .tbl files into Oracle
# Database via SQL*Loader (sqlldr of the Oracle Instant Client tools). The child
# index is read from /tmp/tpch/BEXHOMA_CHILD written by the generator pod.
# nation and region are only loaded by pod 1.
# The Instant Client (basic, sqlplus, tools) comes from the Oracle Linux yum
# repository (Oracle Free Use Terms); redis is installed for the
# synchronisation counters (redis-cli).
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
# Scaling and parallelism
ENV SF=1
ENV BEXHOMA_NUM_PODS=4
ENV BEXHOMA_CHILD=1
ENV BEXHOMA_RNGSEED=123

# Target DBMS connection
ENV BEXHOMA_HOST="www.example.com"
ENV BEXHOMA_PORT=1521
ENV BEXHOMA_USER=bexhoma
ENV BEXHOMA_PASSWORD=""
# Schema (= user) the tables are in
ENV BEXHOMA_DATABASE=bexhoma
ENV BEXHOMA_SCHEMA=""
# Service name of the pluggable database
ENV ORACLE_SERVICE=FREEPDB1
# Unused/compatibility
ENV BEXHOMA_URL=jdbc:oracle:thin:@//localhost:1521/FREEPDB1
ENV BEXHOMA_JAR=ojdbc11-23.26.0.0.0.jar
ENV BEXHOMA_DRIVER=oracle.jdbc.OracleDriver

# Bexhoma experiment identity
ENV BEXHOMA_CONNECTION=oracle
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
# Loader script and SQL*Loader control files
######################################################################################
COPY ./loader.sh /tmp/loader.sh
COPY ./ctl /tmp/ctl
RUN chmod +x /tmp/loader.sh

######################################################################################
# Entrypoint
######################################################################################
CMD ["/bin/bash", "-c", "/tmp/loader.sh"]
