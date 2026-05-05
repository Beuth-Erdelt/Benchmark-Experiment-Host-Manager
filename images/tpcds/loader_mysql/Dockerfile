######################################################################################
# Dockerfile for Bexhoma - Loader TPC-DS MySQL
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma loader for TPC-DS data into MySQL.
#
# Base Image: debian:stable-20240110-slim
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2025-05-18
# Version: 1.0
# Description: This container loads pre-generated TPC-DS .dat files into MySQL using
# mysql LOAD DATA LOCAL INFILE with per-table NULLIF column mappings. The child index
# is read from /tmp/tpcds/BEXHOMA_CHILD. Both mysql (default-mysql-client) and
# mysqlsh (MySQL Shell 8.4.3) are installed. redis-cli is built from source.
######################################################################################
FROM debian:stable-20240110-slim

######################################################################################
# Install build dependencies and build Redis CLI
######################################################################################
RUN apt-get clean \
    && apt-get -y update \
    && apt-get clean all

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
# Install MySQL Shell (mysqlsh 8.4.3)
######################################################################################
# Set noninteractive frontend to avoid prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install prerequisites
RUN apt-get update --allow-releaseinfo-change \
    && apt-get install -y --no-install-recommends wget gnupg lsb-release ca-certificates

# Download current MySQL APT config package
RUN wget https://dev.mysql.com/get/mysql-apt-config_0.8.36-1_all.deb

# Install non-interactive
RUN DEBIAN_FRONTEND=noninteractive dpkg -i mysql-apt-config_0.8.36-1_all.deb

### install mysqlsh
RUN wget https://dev.mysql.com/get/Downloads/MySQL-Shell/mysql-shell_8.4.3-1debian12_amd64.deb
# Install + auto-fix dependencies
RUN apt-get update && \
    dpkg -i mysql-shell_8.4.3-1debian12_amd64.deb || apt-get -f install -y && \
    rm -rf /var/lib/apt/lists/*

######################################################################################
# Set locale
######################################################################################
# Set locale properly
RUN apt-get update && \
    apt-get install -y --no-install-recommends locales && \
    rm -rf /var/lib/apt/lists/* && \
    localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

RUN apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG=en_US.utf8

######################################################################################
# Install MySQL client
######################################################################################
# Add MySQL GPG key to trusted keyring
RUN wget https://repo.mysql.com/RPM-GPG-KEY-mysql-2022 -O /usr/share/keyrings/mysql-archive-keyring.gpg

### install mysql
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        locales \
        default-mysql-client \
    && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

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
ENV TPCDS_TABLE=""
ENV MYSQL_LOADING_FROM=LOCAL
ENV MYSQL_LOADING_THREADS=8
ENV MYSQL_LOADING_PARALLEL=0

######################################################################################
# Working directory and data folder
######################################################################################
WORKDIR /tmp
RUN mkdir -p /tmp/tpcds

######################################################################################
# Loader script
######################################################################################
COPY ./loader.sh /tmp/loader.sh
RUN chmod +x /tmp/loader.sh

######################################################################################
# Entrypoint
######################################################################################
CMD ["/bin/bash", "-c", "/tmp/loader.sh"]
