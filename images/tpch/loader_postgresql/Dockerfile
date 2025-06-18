######################################################################################
# Dockerfile for Bexhoma - Benchmarker TPC-H
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma component "loader".
#
# Base Image: alpine:3.15
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2025-05-18
# Version: 1.0
# Description: This container runs a driver for a benchmark. Pre-generated data is loaded.
# The configuration is given by environment variables.
# A redis queue is consulted for further details.
# Redis client is installed.
# PostgreSQL client is installed.
######################################################################################
#FROM debian:stable-20221004-slim
FROM alpine:3.15

RUN apk update

RUN apk add --no-cache bash

RUN apk add --no-cache nano

RUN apk add --no-cache make cmake gcc libc-dev

RUN apk add redis

#RUN apk add libssl3

#COPY --from=redis:7-alpine3.20 /usr/local/bin/redis-cli /usr/local/bin/redis-cli

#RUN wget http://download.redis.io/redis-stable.tar.gz && tar xvzf redis-stable.tar.gz && cd redis-stable && make && cp src/redis-cli /usr/local/bin/ && chmod 755 /usr/local/bin/redis-cli

#RUN cd /tmp; wget http://download.redis.io/redis-stable.tar.gz; tar xvzf redis-stable.tar.gz; cd redis-stable; make; cp src/redis-cli /usr/local/bin/; chmod 755 /usr/local/bin/redis-cli

RUN apk update && apk --update add postgresql-client

ENV SF=1
ENV BEXHOMA_NUM_PODS=4
ENV BEXHOMA_CHILD=1
ENV BEXHOMA_RNGSEED=123
ENV BEXHOMA_URL jdbc:mysql://localhost:3306/ycsb
ENV BEXHOMA_HOST="www.example.com"
ENV BEXHOMA_PORT 3306
ENV BEXHOMA_JAR mysql-connector-j-8.0.31.jar
ENV BEXHOMA_DRIVER com.mysql.cj.jdbc.Driver
ENV BEXHOMA_CONNECTION="mysql"
ENV BEXHOMA_EXPERIMENT="12345"
ENV BEXHOMA_EXPERIMENT_RUN=1
ENV BEXHOMA_USER root
ENV BEXHOMA_PASSWORD root
ENV BEXHOMA_DATABASE demo
ENV STORE_RAW_DATA=0
ENV BEXHOMA_SYNCH_LOAD 0
ENV BEXHOMA_USER postgres

WORKDIR /tmp

RUN mkdir -p /tmp/tpch

COPY ./loader.sh /tmp/loader.sh
RUN ["chmod", "+x", "/tmp/loader.sh"]


CMD ["/bin/bash", "-c", "/tmp/loader.sh"]
