FROM monetdb/monetdb:Sep2022
#FROM centos:centos7

RUN yum -y update && yum clean all
#RUN yum install -y https://dev.monetdb.org/downloads/epel/MonetDB-release-epel.noarch.rpm
#RUN yum install -y MonetDB-client

RUN yum install -y gcc
RUN yum install -y wget
RUN wget http://download.redis.io/redis-stable.tar.gz && tar xvzf redis-stable.tar.gz && cd redis-stable && make && sudo cp src/redis-cli /usr/local/bin/ && sudo chmod 755 /usr/local/bin/redis-cli

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
ENV BEXHOMA_USER root
ENV BEXHOMA_PASSWORD root
ENV BEXHOMA_DATABASE demo
ENV STORE_RAW_DATA=0
ENV BEXHOMA_SYNCH_LOAD 0

WORKDIR /tmp

RUN mkdir -p /tmp/tpch

#COPY ./*.dat /tmp/

COPY ./loader.sh /tmp/loader.sh
RUN ["chmod", "+x", "/tmp/loader.sh"]


CMD ["/bin/bash", "-c", "/tmp/loader.sh"]
