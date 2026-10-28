######################################################################################
# Dockerfile for Bexhoma - Loader SSB MariaDB
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma loader for SSB data into MariaDB.
#
# Base Image: debian:stable-20251103-slim
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2026-10-28
# Version: 1.0
# Description: This container loads pre-generated SSB .tbl files into MariaDB via
# LOAD DATA LOCAL INFILE and checks the row count of every file (ROW_COUNT()). The
# child index is read from /tmp/ssb/BEXHOMA_CHILD written by the generator in the
# same pod. Each pod loads the files of its own folder; the folder of child 1 also
# holds the dimensions. With SSB_SCHEMA_VARIANT=flat it loads lineorder_flat.
# Client and base image as in images/tpch/loader_mariadb. loader.sh is the same file
# as in loader_mysql.
######################################################################################
FROM debian:stable-20251103-slim

######################################################################################
# Install dependencies: redis-cli, MariaDB client
######################################################################################
RUN apt-get update && apt-get install -y --no-install-recommends mariadb-client redis-tools \
    && rm -rf /var/lib/apt/lists/*

######################################################################################
# Environment variables — runtime configuration
######################################################################################
# Scaling and parallelism
ENV SF=1
ENV BEXHOMA_NUM_PODS=4
ENV BEXHOMA_CHILD=1

# Target DBMS connection
ENV BEXHOMA_HOST="www.example.com"
ENV BEXHOMA_PORT=3306
ENV BEXHOMA_USER=bexhoma
ENV BEXHOMA_PASSWORD=password
ENV BEXHOMA_VOLUME=ssb
ENV MYSQL_CLIENT_OPTIONS=""

# Bexhoma experiment identity
ENV BEXHOMA_CONNECTION=mariadb
ENV BEXHOMA_EXPERIMENT=12345
ENV BEXHOMA_EXPERIMENT_RUN=1
ENV BEXHOMA_CONFIGURATION=""
ENV BEXHOMA_CLIENT=1

# Data storage and loading control
ENV STORE_RAW_DATA=0
ENV BEXHOMA_SYNCH_LOAD=0
ENV SSB_SCHEMA_VARIANT=normal
ENV SSB_TABLE=""

######################################################################################
# Working directory and data folder
######################################################################################
WORKDIR /tmp
RUN mkdir -p /tmp/ssb

######################################################################################
# Loader script
######################################################################################
COPY ./loader.sh /tmp/loader.sh
RUN chmod +x /tmp/loader.sh

######################################################################################
# Entrypoint
######################################################################################
CMD ["/bin/bash", "-c", "/tmp/loader.sh"]
