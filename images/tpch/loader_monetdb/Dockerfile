######################################################################################
# Dockerfile for Bexhoma - Loader TPC-H MonetDB
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma loader for TPC-H data into MonetDB.
#
# Base Image: monetdb/monetdb:Dec2025
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2025-05-18
# Version: 1.0
# Description: This container loads pre-generated TPC-H .tbl files into MonetDB using
# mclient COPY ... FROM STDIN. Writes a .monetdb credentials file before loading.
# Retries on worker/producer thread errors. redis and gcc/wget are installed via yum.
######################################################################################
FROM monetdb/monetdb:Dec2025

######################################################################################
# Update system and install dependencies
######################################################################################
RUN yum -y update \
    && yum install -y \
        redis \
        gcc \
        wget \
    && yum clean all \
    && rm -rf /var/cache/yum

######################################################################################
# Environment variables — runtime configuration
######################################################################################
# Scaling and parallelism
ENV SF=1 \
    BEXHOMA_NUM_PODS=4 \
    BEXHOMA_CHILD=1 \
    BEXHOMA_RNGSEED=123

# Target DBMS connection
ENV BEXHOMA_URL=jdbc:mysql://localhost:3306/ycsb \
    BEXHOMA_HOST=www.example.com \
    BEXHOMA_PORT=3306 \
    BEXHOMA_JAR=mysql-connector-j-8.0.31.jar \
    BEXHOMA_DRIVER=com.mysql.cj.jdbc.Driver \
    BEXHOMA_USER=root \
    BEXHOMA_PASSWORD=root \
    BEXHOMA_DATABASE=demo

# Bexhoma experiment identity
ENV BEXHOMA_CONNECTION=mysql \
    BEXHOMA_EXPERIMENT=12345 \
    BEXHOMA_EXPERIMENT_RUN=1 \
    BEXHOMA_CONFIGURATION="" \
    BEXHOMA_CLIENT=1

# Data storage and loading control
ENV STORE_RAW_DATA=0 \
    BEXHOMA_SYNCH_LOAD=0 \
    TPCH_TABLE=""

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
