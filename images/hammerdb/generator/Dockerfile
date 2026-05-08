######################################################################################
# Dockerfile for Bexhoma - Generator HammerDB
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma generator that loads TPC-C data
# into a DBMS using HammerDB's buildschema command.
#
# Base Image: tpcorg/hammerdb:v5.0
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2025-05-18
# Version: 1.0
# Description: Runs the HammerDB schema builder to populate TPC-C data.
#   Configuration is supplied via environment variables.
######################################################################################
FROM tpcorg/hammerdb:v5.0

######################################################################################
# Environment variables — runtime configuration
######################################################################################
# Scaling and parallelism
ENV SF=1
ENV BEXHOMA_NUM_PODS=1
ENV BEXHOMA_CHILD=1
ENV BEXHOMA_RNGSEED=123

# Target DBMS connection
ENV BEXHOMA_HOST=www.example.com
ENV BEXHOMA_PORT=5432
ENV BEXHOMA_USER=postgres
ENV BEXHOMA_PASSWORD=postgres
ENV BEXHOMA_DATABASE=tpcc

# Bexhoma experiment identity
ENV BEXHOMA_DBMS=postgresql
ENV BEXHOMA_CONFIGURATION=postgresql
ENV BEXHOMA_CONNECTION=postgresql
ENV BEXHOMA_EXPERIMENT=12345
ENV BEXHOMA_EXPERIMENT_RUN=1
ENV BEXHOMA_CLIENT=1

# HammerDB workload parameters
ENV HAMMERDB_TYPE=postgresql
ENV HAMMERDB_RAMPUP=2
ENV HAMMERDB_DURATION=5
ENV HAMMERDB_ITERATIONS=10000000
ENV HAMMERDB_MYSQL_ENGINE=innodb
ENV HAMMERDB_NUM_VU=4
ENV HAMMERDB_VUSERS=1

######################################################################################
# Create temp TPC-C directory and copy entrypoint script
######################################################################################
RUN mkdir -p /tmp/tpcc

COPY ./generator.sh ./generator.sh
RUN ["chmod", "+x", "./generator.sh"]

CMD ["/bin/bash", "-c", "./generator.sh"]
