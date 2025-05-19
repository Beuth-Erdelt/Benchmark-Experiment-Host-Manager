######################################################################################
# Dockerfile for Bexhoma - Benchmarker HammerDB
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma component "loader".
#
# Base Image: tpcorg/hammerdb:v4.12
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2025-05-18
# Version: 1.0
# Description: This container runs a driver for a benchmark. Data is generated and loaded.
# The configuration is given by environment variables.
######################################################################################
FROM tpcorg/hammerdb:v4.12

COPY ./generator.sh ./generator.sh
RUN ["chmod", "+x", "./generator.sh"]

ENV SF=1
ENV BEXHOMA_CLIENT 1
ENV BEXHOMA_CHILD=1
ENV BEXHOMA_RNGSEED=123
ENV BEXHOMA_HOST="www.example.com"
ENV BEXHOMA_PORT 3307
ENV BEXHOMA_CONNECTION="monetdb"
ENV BEXHOMA_EXPERIMENT="12345"
ENV BEXHOMA_EXPERIMENT_RUN=1
ENV HAMMERDB_TYPE postgresql
# Rampup time in minutes before first Transaction Count is taken
ENV HAMMERDB_RAMPUP 2
# Duration in minutes before second Transaction Count is taken
ENV HAMMERDB_DURATION 5
# Number of transactions before logging off
ENV HAMMERDB_ITERATIONS 10000000
ENV HAMMERDB_MYSQL_ENGINE innodb
ENV HAMMERDB_NUM_VU=4
ENV HAMMERDB_VUSERS 1

# set async_client $pg_async_client;# Number of asynchronous clients per Vuser
# set async_verbose $pg_async_verbose;# Report activity of asynchronous clients
# set async_delay $pg_async_delay;# Delay in ms between logins of asynchronous clients

RUN mkdir -p /tmp/tpcc

CMD ["/bin/bash", "-c", "./generator.sh"]
