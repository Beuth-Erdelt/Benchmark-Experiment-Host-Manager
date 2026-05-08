######################################################################################
# Dockerfile for Bexhoma - Benchmarker YCSB
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma benchmarker running YCSB workloads
# against an already-loaded DBMS.
#
# Base Image: alpine:3.15
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2025-05-18
# Version: 1.0
# Description: Runs the YCSB 'run' phase against a target DBMS.
#   Configuration is supplied via environment variables.
#   A Redis message queue is consulted for pod-assignment details.
#   Java 8 JRE, Python 2, redis-cli, jemalloc, and JDBC drivers are installed.
######################################################################################
FROM alpine:3.15

######################################################################################
# Environment variables — runtime configuration
######################################################################################
# YCSB installation paths
ENV YCSB_VERSION=0.17.0
ENV YCSB=/opt/ycsb
ENV PATH=${PATH}:/usr/bin

# Scaling and parallelism
ENV SF=1
ENV BEXHOMA_NUM_PODS=4
ENV BEXHOMA_CHILD=1
ENV BEXHOMA_RNGSEED=123

# Target DBMS connection (JDBC defaults; override for Redis)
ENV BEXHOMA_DBMS_TYPE=jdbc
ENV BEXHOMA_URL=jdbc:mysql://localhost:3306/ycsb
ENV BEXHOMA_HOST=www.example.com
ENV BEXHOMA_PORT=3306
ENV BEXHOMA_JAR=mysql-connector-j-8.0.31.jar
ENV BEXHOMA_DRIVER=com.mysql.cj.jdbc.Driver
ENV BEXHOMA_USER=root
ENV BEXHOMA_PASSWORD=root
ENV DATABASE=demo

# Bexhoma experiment identity
ENV BEXHOMA_CONNECTION=mysql
ENV BEXHOMA_EXPERIMENT=12345
ENV BEXHOMA_EXPERIMENT_RUN=1

# Pod synchronisation
ENV BEXHOMA_SYNCH_LOAD=1
ENV BEXHOMA_TIME_START=0
ENV BEXHOMA_TIME_NOW=0

# YCSB workload parameters
ENV YCSB_THREADCOUNT=1
ENV YCSB_TARGET=10000
ENV YCSB_STATUS_INTERVAL=10
ENV YCSB_STATUS=0
ENV YCSB_WORKLOAD=a
ENV YCSB_BATCHSIZE=""
ENV YCSB_MEASUREMENT_TYPE=hdrhistogram
ENV YCSB_USE_HOSTLIST=0
ENV YCSB_INSERTORDER=hashed

######################################################################################
# Install Java 8 JRE and download YCSB
######################################################################################
RUN apk update && apk add --update curl openjdk8-jre && \
    mkdir -p /opt && cd /opt && \
    curl -O --location https://github.com/brianfrankcooper/YCSB/releases/download/${YCSB_VERSION}/ycsb-${YCSB_VERSION}.tar.gz && \
    tar xfz *.tar.gz && \
    rm -rf *.tar.gz

RUN mv "${YCSB}-${YCSB_VERSION}" "${YCSB}"

WORKDIR "${YCSB}"

######################################################################################
# Install shell utilities and C build toolchain
######################################################################################
RUN apk add --no-cache \
    bash \
    nano \
    make \
    cmake \
    gcc \
    libc-dev \
    build-base \
    git \
    autoconf \
    automake \
    libtool

######################################################################################
# Build and install jemalloc from source
######################################################################################
RUN git clone https://github.com/jemalloc/jemalloc.git /tmp/jemalloc && \
    cd /tmp/jemalloc && \
    ./autogen.sh && \
    ./configure --prefix=/usr/local && \
    make -j$(nproc) && \
    make install && \
    rm -rf /tmp/jemalloc

######################################################################################
# Build and install redis-cli from source
######################################################################################
RUN cd /tmp && \
    wget http://download.redis.io/redis-stable.tar.gz && \
    tar xvzf redis-stable.tar.gz && \
    cd redis-stable && \
    make && \
    cp src/redis-cli /usr/local/bin/ && \
    chmod 755 /usr/local/bin/redis-cli && \
    rm -rf /tmp/redis-stable /tmp/redis-stable.tar.gz

######################################################################################
# Install Python 2
######################################################################################
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python2 && \
    ln -sf /usr/bin/python2.7 /usr/bin/python && \
    python2 -m ensurepip && \
    pip install --no-cache --upgrade pip setuptools

######################################################################################
# Install JDBC drivers into jars/
######################################################################################
RUN mkdir -p jars

# PostgreSQL 42.5.0
RUN wget https://jdbc.postgresql.org/download/postgresql-42.5.0.jar --no-check-certificate && \
    cp postgresql-42.5.0.jar jars/

# MySQL 8.0.31
RUN wget https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-j-8.0.31.tar.gz && \
    tar -zxvf mysql-connector-j-8.0.31.tar.gz && \
    cp mysql-connector-j-8.0.31/mysql-connector-j-8.0.31.jar jars/

# MariaDB 3.1.0
RUN wget https://dlm.mariadb.com/2678616/Connectors/java/connector-java-3.1.0/mariadb-java-client-3.1.0.jar && \
    cp mariadb-java-client-3.1.0.jar jars/

# MonetDB 3.2 (jre8)
RUN wget https://www.monetdb.org/downloads/Java/archive/monetdb-jdbc-3.2.jre8.jar --no-check-certificate && \
    cp monetdb-jdbc-3.2.jre8.jar jars/

# SingleStore 1.1.4
RUN wget https://github.com/memsql/S2-JDBC-Connector/releases/download/v1.1.4/singlestore-jdbc-client-1.1.4.jar && \
    cp singlestore-jdbc-client-1.1.4.jar jars/

# Kinetica 7.1.8.7
RUN wget https://github.com/kineticadb/kinetica-client-jdbc/archive/refs/tags/v7.1.8.7.tar.gz && \
    tar -zxvf v7.1.8.7.tar.gz && \
    cp kinetica-client-jdbc-7.1.8.7/kinetica-jdbc-7.1.8.7-jar-with-dependencies.jar jars/

# YugabyteDB 42.3.5-yb-2
RUN wget https://github.com/yugabyte/pgjdbc/releases/download/v42.3.5-yb-2/jdbc-yugabytedb-42.3.5-yb-2.jar && \
    cp jdbc-yugabytedb-42.3.5-yb-2.jar jars/

######################################################################################
# Copy workload templates and entrypoint script
######################################################################################
COPY ./workloads ./workloads

COPY ./benchmarker.sh /tmp/benchmarker.sh
RUN ["chmod", "+x", "/tmp/benchmarker.sh"]
CMD ["/bin/bash", "-c", "/tmp/benchmarker.sh"]
