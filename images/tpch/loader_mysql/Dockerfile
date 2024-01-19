FROM debian:stable-20221004-slim

RUN apt-get -y update && apt-get clean all

RUN apt-get install -y build-essential
RUN apt-get install -y wget
RUN wget http://download.redis.io/redis-stable.tar.gz && tar xvzf redis-stable.tar.gz && cd redis-stable && make && cp src/redis-cli /usr/local/bin/ && chmod 755 /usr/local/bin/redis-cli

#&& apt-get install -y mysql-apt-config && apt-get install -y mysql-shell

#RUN apt-get install --fix-missing -y libcurl4
RUN apt-get install -y libssh-4
#RUN wget https://downloads.mysql.com/archives/get/p/43/file/mysql-shell_8.0.31-1debian11_amd64.deb
#RUN dpkg -i mysql-shell_8.0.31-1debian11_amd64.deb
#RUN wget https://cdn.mysql.com//Downloads/MySQL-Shell/mysql-shell_8.0.36-1debian12_amd64.deb
#RUN dpkg -i mysql-shell_8.0.36-1debian12_amd64.deb
RUN apt-get install mysql-shell -y
RUN apt-get update
RUN apt install -y mysql-shell

ENV NUM_PODS=4
ENV CHILD=1
ENV BEXHOMA_HOST="www.example.com"
ENV BEXHOMA_PORT 50000
ENV BEXHOMA_CONNECTION="monetdb"
ENV BEXHOMA_EXPERIMENT="12345"
ENV DATABASE tpch
ENV STORE_RAW_DATA=0
ENV BEXHOMA_SYNCH_LOAD 0
ENV MYSQL_LOADING_THREADS 8
ENV MYSQL_LOADING_PARALLEL 1
ENV MYSQL_LOADING_FROM "LOCAL"

WORKDIR /tmp

RUN mkdir -p /tmp/tpch

#COPY ./*.dat /tmp/

#COPY ./loader-parallel.sh /tmp/loader.sh
COPY ./loader.sh /tmp/loader.sh
RUN ["chmod", "+x", "/tmp/loader.sh"]


CMD ["/bin/bash", "-c", "/tmp/loader.sh"]
#CMD ["/bin/bash", "-c", "while true; do sleep 2; done"]
