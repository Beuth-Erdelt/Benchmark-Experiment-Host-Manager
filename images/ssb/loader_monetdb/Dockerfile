######################################################################################
# Dockerfile for Bexhoma - Loader SSB MonetDB
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma loader for SSB data into MonetDB.
#
# Base Image: monetdb/monetdb:Dec2025
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2026-10-25
# Version: 1.0
# Description: This container loads pre-generated SSB .tbl files into MonetDB using
# mclient COPY ... FROM STDIN. Writes a .monetdb credentials file before loading.
# Retries on worker/producer thread errors. Each pod loads the files of its own folder;
# the folder of child 1 also holds the dimensions. With SSB_SCHEMA_VARIANT=flat it
# loads lineorder_flat. redis is installed via yum.
######################################################################################
FROM monetdb/monetdb:Dec2025

######################################################################################
# Update system and install dependencies
######################################################################################
RUN yum -y update \
    && yum install -y \
        redis \
    && yum clean all \
    && rm -rf /var/cache/yum

######################################################################################
# Environment variables — runtime configuration
######################################################################################
# Scaling and parallelism
ENV SF=1 \
    BEXHOMA_NUM_PODS=4 \
    BEXHOMA_CHILD=1

# Target DBMS connection
ENV BEXHOMA_HOST=www.example.com \
    BEXHOMA_PORT=50000 \
    BEXHOMA_USER=monetdb \
    BEXHOMA_PASSWORD=monetdb \
    BEXHOMA_DATABASE=monetdb

# Bexhoma experiment identity
ENV BEXHOMA_CONNECTION=monetdb \
    BEXHOMA_EXPERIMENT=12345 \
    BEXHOMA_EXPERIMENT_RUN=1 \
    BEXHOMA_CONFIGURATION="" \
    BEXHOMA_CLIENT=1

# Data storage and loading control
ENV STORE_RAW_DATA=0 \
    BEXHOMA_SYNCH_LOAD=0 \
    SSB_SCHEMA_VARIANT=normal \
    SSB_TABLE=""

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
