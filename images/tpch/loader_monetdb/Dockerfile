######################################################################################
# Dockerfile for Bexhoma - Benchmarker TPC-DS
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma component "loader".
#
# Base Image: monetdb/monetdb:Dec2025
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2025-05-18
# Version: 1.0
# Description: This container runs a driver for a benchmark. Pre-generated data is loaded.
# The configuration is given by environment variables.
# A redis queue is consulted for further details.
# Redis client is installed.
# MonetDB client is installed.
######################################################################################
FROM monetdb/monetdb:Dec2025

# Update system and install Redis CLI + runtime dependencies in a single layer
RUN yum -y update \
    && yum install -y \
        redis \
        gcc \
        wget \
    && yum clean all \
    && rm -rf /var/cache/yum

# Environment variables
ENV SF=1 \
    BEXHOMA_NUM_PODS=4 \
    BEXHOMA_CHILD=1 \
    BEXHOMA_RNGSEED=123 \
    BEXHOMA_URL=jdbc:mysql://localhost:3306/ycsb \
    BEXHOMA_HOST=www.example.com \
    BEXHOMA_PORT=3306 \
    BEXHOMA_JAR=mysql-connector-j-8.0.31.jar \
    BEXHOMA_DRIVER=com.mysql.cj.jdbc.Driver \
    BEXHOMA_CONNECTION=mysql \
    BEXHOMA_EXPERIMENT=12345 \
    BEXHOMA_EXPERIMENT_RUN=1 \
    BEXHOMA_USER=root \
    BEXHOMA_PASSWORD=root \
    BEXHOMA_DATABASE=demo \
    STORE_RAW_DATA=0 \
    BEXHOMA_SYNCH_LOAD=0

# Working directory
WORKDIR /tmp
RUN mkdir -p /tmp/tpch

# Loader script
COPY ./loader.sh /tmp/loader.sh
RUN chmod +x /tmp/loader.sh

CMD ["/bin/bash", "-c", "/tmp/loader.sh"]
