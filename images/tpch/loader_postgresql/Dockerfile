######################################################################################
# Dockerfile for Bexhoma - Loader TPC-H PostgreSQL
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma loader for TPC-H data into PostgreSQL.
#
# Base Image: alpine:3.15
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2025-05-18
# Version: 1.0
# Description: This container loads pre-generated TPC-H .tbl files into PostgreSQL
# via psql \COPY. The child index is read from /tmp/tpch/BEXHOMA_CHILD written by
# the generator pod. nation and region are only loaded by pod 1 in non-tenant mode.
# Multi-tenancy (schema and database isolation) is supported. redis and postgresql-client
# are installed via apk.
######################################################################################
FROM alpine:3.15

######################################################################################
# Install dependencies
######################################################################################
RUN apk update && apk add --no-cache bash nano make cmake gcc libc-dev redis postgresql-client

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
ENV BEXHOMA_PORT=5432
ENV BEXHOMA_USER=postgres
ENV BEXHOMA_PASSWORD=postgres
ENV BEXHOMA_DATABASE=tpch
ENV BEXHOMA_SCHEMA=""
# Unused/compatibility
ENV BEXHOMA_URL=jdbc:mysql://localhost:3306/ycsb
ENV BEXHOMA_JAR=mysql-connector-j-8.0.31.jar
ENV BEXHOMA_DRIVER=com.mysql.cj.jdbc.Driver

# Bexhoma experiment identity
ENV BEXHOMA_CONNECTION=mysql
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
