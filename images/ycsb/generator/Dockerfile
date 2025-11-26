######################################################################################
# Dockerfile for Bexhoma - Benchmarker YCSB
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
# Description: This container runs a driver for a benchmark. Data is generated and loaded.
# The configuration is given by environment variables.
# A redis queue is consulted for further details.
# Java is installed.
# Python2 is installed.
# Redis client is installed.
# Some JDBC driver are installed.
######################################################################################
#FROM alpine:latest
FROM alpine:3.15

ENV YCSB_VERSION=0.17.0
ENV YCSB=/opt/ycsb
ENV PATH=${PATH}:/usr/bin

ENV SF=1
ENV BEXHOMA_NUM_PODS=4
ENV BEXHOMA_CHILD=1
ENV BEXHOMA_RNGSEED=123
ENV BEXHOMA_DBMS_TYPE=jdbc
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
ENV BEXHOMA_SYNCH_LOAD 1
ENV DATABASE demo
ENV BEXHOMA_TIME_START 0
ENV BEXHOMA_TIME_NOW 0
ENV YCSB_THREADCOUNT 1
ENV YCSB_TARGET 10000
ENV YCSB_STATUS_INTERVAL 10
ENV YCSB_STATUS 0
ENV YCSB_WORKLOAD a
ENV YCSB_BATCHSIZE=""
ENV YCSB_MEASUREMENT_TYPE=hdrhistogram
ENV YCSB_INSERTORDER=hashed

RUN apk update && apk add --update curl openjdk8-jre && \
    mkdir -p /opt && cd /opt && \
    curl -O --location  https://github.com/brianfrankcooper/YCSB/releases/download/${YCSB_VERSION}/ycsb-${YCSB_VERSION}.tar.gz && \
    tar xfz *.tar.gz && \
    rm -rf *.tar.gz

RUN mv "${YCSB}-${YCSB_VERSION}" "${YCSB}"

WORKDIR "${YCSB}"

RUN cd "${YCSB}"

RUN apk add --no-cache bash

RUN apk add --no-cache nano

RUN apk add --no-cache make cmake gcc libc-dev

# Install build dependencies
RUN apk add --no-cache \
    build-base \
    git \
    autoconf \
    automake \
    libtool

# Build and install jemalloc
RUN git clone https://github.com/jemalloc/jemalloc.git /tmp/jemalloc && \
    cd /tmp/jemalloc && \
    ./autogen.sh && \
    ./configure --prefix=/usr/local && \
    make -j$(nproc) && \
    make install && \
    rm -rf /tmp/jemalloc

RUN cd /tmp; wget http://download.redis.io/redis-stable.tar.gz; tar xvzf redis-stable.tar.gz; cd redis-stable; make; cp src/redis-cli /usr/local/bin/; chmod 755 /usr/local/bin/redis-cli

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python2 && ln -sf python3 /usr/bin/python
RUN python2 -m ensurepip
RUN pip install --no-cache --upgrade pip setuptools

RUN ln -sf /usr/bin/python2.7 /usr/bin/python

RUN mkdir -p jars

######### Specific version of PostgreSQL JDBC #########
RUN wget https://jdbc.postgresql.org/download/postgresql-42.5.0.jar --no-check-certificate
RUN cp postgresql-42.5.0.jar jars/postgresql-42.5.0.jar

######### Specific version of MySQL JDBC #########
RUN wget https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-j-8.0.31.tar.gz
RUN tar -zxvf mysql-connector-j-8.0.31.tar.gz
RUN cp mysql-connector-j-8.0.31/mysql-connector-j-8.0.31.jar jars/mysql-connector-j-8.0.31.jar

######### Specific version of MariaDB JDBC #########
RUN wget https://dlm.mariadb.com/2678616/Connectors/java/connector-java-3.1.0/mariadb-java-client-3.1.0.jar
RUN cp mariadb-java-client-3.1.0.jar jars/mariadb-java-client-3.1.0.jar

######### Specific version of MonetDB JDBC #########
RUN wget https://www.monetdb.org/downloads/Java/archive/monetdb-jdbc-3.2.jre8.jar --no-check-certificate
RUN cp monetdb-jdbc-3.2.jre8.jar jars/monetdb-jdbc-3.2.jre8.jar

######### Specific version of MonetDB JDBC #########
#RUN wget https://www.monetdb.org/downloads/Java/monetdb-jdbc-3.3.jre8.jar --no-check-certificate
#RUN cp monetdb-jdbc-3.3.jre8.jar jars/monetdb-jdbc-3.3.jre8.jar

######### Specific version of SingleStore JDBC #########
RUN wget https://github.com/memsql/S2-JDBC-Connector/releases/download/v1.1.4/singlestore-jdbc-client-1.1.4.jar
RUN cp singlestore-jdbc-client-1.1.4.jar jars/singlestore-jdbc-client-1.1.4.jar

######### Specific version of Kinetica JDBC #########
RUN wget https://github.com/kineticadb/kinetica-client-jdbc/archive/refs/tags/v7.1.8.7.tar.gz
RUN tar -zxvf v7.1.8.7.tar.gz
RUN cp kinetica-client-jdbc-7.1.8.7/kinetica-jdbc-7.1.8.7-jar-with-dependencies.jar jars/kinetica-jdbc-7.1.8.7-jar-with-dependencies.jar

######### Specific version of YugabyteDB JDBC #########
RUN wget https://github.com/yugabyte/pgjdbc/releases/download/v42.3.5-yb-2/jdbc-yugabytedb-42.3.5-yb-2.jar
RUN cp jdbc-yugabytedb-42.3.5-yb-2.jar jars/jdbc-yugabytedb-42.3.5-yb-2.jar
RUN wget https://github.com/yugabyte/pgjdbc/releases/download/v42.7.3-yb-3/jdbc-yugabytedb-42.7.3-yb-3.jar
RUN cp jdbc-yugabytedb-42.7.3-yb-3.jar jars/jdbc-yugabytedb-42.7.3-yb-3.jar

COPY ./workloads ./workloads

COPY ./generator.sh /tmp/generator.sh
RUN ["chmod", "+x", "/tmp/generator.sh"]
CMD ["/bin/bash", "-c", "/tmp/generator.sh"]


#CMD ["/bin/bash", "-c", "while true; do sleep 2; done"]
