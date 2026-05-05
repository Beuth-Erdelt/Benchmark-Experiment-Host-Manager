######################################################################################
# Dockerfile for Bexhoma - Loader TPC-H MariaDB
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma loader for TPC-H data into MariaDB.
#
# Base Image: debian:stable-20251103-slim
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2025-05-18
# Version: 1.0
# Description: This container loads pre-generated TPC-H .tbl files into MariaDB using
# mysql LOAD DATA LOCAL INFILE. The child index is read from /tmp/tpch/BEXHOMA_CHILD.
# Sets BEXHOMA_DATABASE=$BEXHOMA_VOLUME at runtime. redis-cli is built from source;
# mariadb-client is installed via apt.
######################################################################################
FROM debian:stable-20251103-slim

######################################################################################
# Install build dependencies and build Redis CLI
######################################################################################
RUN apt-get update -y && apt-get clean all

RUN apt-get install -y --no-install-recommends build-essential wget \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q http://download.redis.io/redis-stable.tar.gz \
    && tar xvzf redis-stable.tar.gz \
    && cd redis-stable \
    && make redis-cli \
    && cp src/redis-cli /usr/local/bin/ \
    && chmod 755 /usr/local/bin/redis-cli \
    && cd / \
    && rm -rf redis-stable redis-stable.tar.gz

######################################################################################
# Install MariaDB client
######################################################################################
RUN apt-get update && apt-get install -y --no-install-recommends mariadb-client \
    && rm -rf /var/lib/apt/lists/*

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
ENV BEXHOMA_PORT=3306
ENV BEXHOMA_USER=root
ENV BEXHOMA_PASSWORD=root
ENV BEXHOMA_DATABASE=demo
ENV BEXHOMA_VOLUME=""
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

# Data storage and loading control
ENV STORE_RAW_DATA=0
ENV BEXHOMA_SYNCH_LOAD=0
ENV TPCH_TABLE=""
ENV MYSQL_LOADING_FROM=LOCAL

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
