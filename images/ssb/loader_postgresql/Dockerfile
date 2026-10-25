######################################################################################
# Dockerfile for Bexhoma - Loader SSB PostgreSQL
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma loader for SSB data into PostgreSQL.
#
# Base Image: alpine:3.15
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2026-10-25
# Version: 1.0
# Description: This container loads pre-generated SSB .tbl files into PostgreSQL via
# psql \COPY. The child index is read from /tmp/ssb/BEXHOMA_CHILD written by the
# generator in the same pod. Each pod loads the files of its own folder; the folder of
# child 1 also holds the dimensions. With SSB_SCHEMA_VARIANT=flat it loads
# lineorder_flat. redis and postgresql-client are installed via apk.
######################################################################################
FROM alpine:3.15

######################################################################################
# Install dependencies
######################################################################################
RUN apk update && apk add --no-cache bash grep redis postgresql-client

######################################################################################
# Environment variables — runtime configuration
######################################################################################
# Scaling and parallelism
ENV SF=1
ENV BEXHOMA_NUM_PODS=4
ENV BEXHOMA_CHILD=1

# Target DBMS connection
ENV BEXHOMA_HOST="www.example.com"
ENV BEXHOMA_PORT=5432
ENV BEXHOMA_USER=postgres
ENV BEXHOMA_PASSWORD=postgres
ENV BEXHOMA_DATABASE=postgres
ENV BEXHOMA_SCHEMA=public

# Bexhoma experiment identity
ENV BEXHOMA_CONNECTION=postgresql
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
