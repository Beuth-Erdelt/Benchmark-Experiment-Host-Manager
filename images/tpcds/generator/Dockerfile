######################################################################################
# Dockerfile for Bexhoma - Generator TPC-DS
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma generator for TPC-DS data.
#
# Base Image: eclipse-temurin:11
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2025-05-18
# Version: 1.0
# Description: This container generates TPC-DS .dat files (pipe-delimited) using the
# pre-compiled dsdgen binary. In multi-pod mode each pod generates its share
# (dsdgen -parallel <N> -child <i>). customer.dat is converted from ISO-8859-1 to
# UTF-8 when TRANSFORM_RAW_DATA=1. The child index is obtained from a Redis queue.
# redis-cli is built from source.
######################################################################################
FROM eclipse-temurin:11

######################################################################################
# Install build dependencies
######################################################################################
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        make \
        gcc \
        wget \
    && rm -rf /var/lib/apt/lists/*

######################################################################################
# Build Redis CLI from source
######################################################################################
RUN wget -q http://download.redis.io/redis-stable.tar.gz \
    && tar xvzf redis-stable.tar.gz \
    && cd redis-stable \
    && make redis-cli \
    && cp src/redis-cli /usr/local/bin/ \
    && chmod 755 /usr/local/bin/redis-cli \
    && cd / \
    && rm -rf redis-stable redis-stable.tar.gz

######################################################################################
# Copy TPC-DS generator files
######################################################################################
COPY ./tpc_eula.txt ./tpc_eula.txt
COPY ./tpcds.idx /tmp/tpcds.idx
COPY ./dsdgen /tmp/dsdgen
RUN chmod +x /tmp/dsdgen

COPY ./generator.sh /tmp/generator.sh
RUN chmod +x /tmp/generator.sh

######################################################################################
# Environment variables — runtime configuration
######################################################################################
# Scaling and parallelism
ENV SF=1
ENV BEXHOMA_NUM_PODS=4
ENV BEXHOMA_CHILD=1
ENV BEXHOMA_RNGSEED=123

# Data storage
ENV STORE_RAW_DATA=0
ENV STORE_RAW_DATA_RECREATE=0
ENV TRANSFORM_RAW_DATA=1

# Target DBMS connection (declared for compatibility; not used during generation)
ENV BEXHOMA_URL=jdbc:mysql://localhost:3306/ycsb
ENV BEXHOMA_HOST=www.example.com
ENV BEXHOMA_PORT=3306
ENV BEXHOMA_JAR=mysql-connector-j-8.0.31.jar
ENV BEXHOMA_DRIVER=com.mysql.cj.jdbc.Driver
ENV BEXHOMA_USER=root
ENV BEXHOMA_PASSWORD=root
ENV BEXHOMA_DATABASE=demo

# Bexhoma experiment identity
ENV BEXHOMA_CONNECTION=mysql
ENV BEXHOMA_EXPERIMENT=12345
ENV BEXHOMA_EXPERIMENT_RUN=1
ENV BEXHOMA_CONFIGURATION=""
ENV BEXHOMA_CLIENT=1

# Pod synchronisation
ENV BEXHOMA_SYNCH_GENERATE=0

######################################################################################
# Working directory and data folder
######################################################################################
WORKDIR /tmp
RUN mkdir -p /tmp/tpcds

######################################################################################
# Entrypoint
######################################################################################
CMD ["/bin/bash", "-c", "/tmp/generator.sh"]
