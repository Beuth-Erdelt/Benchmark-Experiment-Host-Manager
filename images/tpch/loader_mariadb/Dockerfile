FROM debian:stable-20221004-slim

RUN apt-get -y update && apt-get clean all

RUN apt-get install -y build-essential
RUN apt-get install -y wget
RUN wget http://download.redis.io/redis-stable.tar.gz && tar xvzf redis-stable.tar.gz && cd redis-stable && make && cp src/redis-cli /usr/local/bin/ && chmod 755 /usr/local/bin/redis-cli

RUN apt-get update && apt install -y mariadb-client

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
ENV MYSQL_LOADING_FROM "LOCAL"

WORKDIR /tmp

RUN mkdir -p /tmp/tpch

#COPY ./*.dat /tmp/

COPY ./loader.sh /tmp/loader.sh
RUN ["chmod", "+x", "/tmp/loader.sh"]


CMD ["/bin/bash", "-c", "/tmp/loader.sh"]
#CMD ["/bin/bash", "-c", "while true; do sleep 2; done"]
