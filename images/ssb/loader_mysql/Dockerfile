######################################################################################
# Dockerfile for Bexhoma - Loader SSB MySQL
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma loader for SSB data into MySQL.
#
# Base Image: debian:stable-20240110-slim
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2026-10-28
# Version: 1.0
# Description: This container loads pre-generated SSB .tbl files into MySQL via
# LOAD DATA LOCAL INFILE and checks the row count of every file (ROW_COUNT()). The
# child index is read from /tmp/ssb/BEXHOMA_CHILD written by the generator in the
# same pod. Each pod loads the files of its own folder; the folder of child 1 also
# holds the dimensions. With SSB_SCHEMA_VARIANT=flat it loads lineorder_flat.
# Client and base image as in images/tpch/loader_mysql (the job template sets
# MYSQL_CLIENT_OPTIONS=--skip-ssl). loader.sh is the same file as in loader_mariadb.
######################################################################################
FROM debian:stable-20240110-slim

######################################################################################
# Install dependencies: redis-cli, MySQL client
######################################################################################
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update --allow-releaseinfo-change \
    && apt-get install -y --no-install-recommends wget gnupg lsb-release ca-certificates redis-tools \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://dev.mysql.com/get/mysql-apt-config_0.8.36-1_all.deb \
    && dpkg -i mysql-apt-config_0.8.36-1_all.deb \
    && rm mysql-apt-config_0.8.36-1_all.deb

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        locales \
        default-mysql-client \
    && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG=en_US.utf8

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
ENV BEXHOMA_USER=root
ENV BEXHOMA_PASSWORD=root
ENV BEXHOMA_VOLUME=ssb
ENV MYSQL_CLIENT_OPTIONS=""

# Bexhoma experiment identity
ENV BEXHOMA_CONNECTION=mysql
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
