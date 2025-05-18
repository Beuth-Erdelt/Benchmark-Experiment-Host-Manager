FROM monetdb/monetdb:Sep2022
#FROM centos:centos7

RUN yum -y update && yum clean all
#RUN yum install -y https://dev.monetdb.org/downloads/epel/MonetDB-release-epel.noarch.rpm
#RUN yum install -y MonetDB-client

RUN yum install -y gcc
RUN yum install -y wget
RUN wget http://download.redis.io/redis-stable.tar.gz && tar xvzf redis-stable.tar.gz && cd redis-stable && make && sudo cp src/redis-cli /usr/local/bin/ && sudo chmod 755 /usr/local/bin/redis-cli

ENV BEXHOMA_NUM_PODS=4
ENV BEXHOMA_CHILD=1
ENV BEXHOMA_HOST="www.example.com"
ENV BEXHOMA_PORT 50000
ENV BEXHOMA_CONNECTION="monetdb"
ENV BEXHOMA_EXPERIMENT="12345"
ENV DATABASE demo
ENV STORE_RAW_DATA=0
ENV BEXHOMA_SYNCH_LOAD 0

WORKDIR /tmp

RUN mkdir -p /tmp/tpch

#COPY ./*.dat /tmp/

COPY ./loader.sh /tmp/loader.sh
RUN ["chmod", "+x", "/tmp/loader.sh"]


CMD ["/bin/bash", "-c", "/tmp/loader.sh"]
