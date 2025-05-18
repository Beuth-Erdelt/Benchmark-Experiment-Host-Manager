#FROM eclipse-temurin:11
FROM debian:stable-20221004-slim

RUN apt-get -y update && apt-get clean all

RUN apt-get install -y build-essential
RUN apt-get install -y wget
RUN wget http://download.redis.io/redis-stable.tar.gz && tar xvzf redis-stable.tar.gz && cd redis-stable && make && cp src/redis-cli /usr/local/bin/ && chmod 755 /usr/local/bin/redis-cli

#RUN apt-get update
#RUN apt-get install -y make
#RUN apt-get install -y gcc
#RUN cd /tmp; wget http://download.redis.io/redis-stable.tar.gz; tar xvzf redis-stable.tar.gz; cd redis-stable; make; cp src/redis-cli /usr/local/bin/; chmod 755 /usr/local/bin/redis-cli

COPY ./tpc_eula.txt ./tpc_eula.txt
COPY ./dists.dss /tmp/dists.dss
COPY ./dbgen /tmp/dbgen
RUN ["chmod", "+x", "/tmp/dbgen"]

COPY ./generator.sh /tmp/generator.sh
RUN ["chmod", "+x", "/tmp/generator.sh"]

ENV SF=1
ENV BEXHOMA_NUM_PODS=4
ENV BEXHOMA_CHILD=1
ENV RNGSEED=123
ENV CONNECTION=monetdb
ENV EXPERIMENT=12345
ENV STORE_RAW_DATA=0
ENV STORE_RAW_DATA_RECREATE=0
ENV TRANSFORM_RAW_DATA=1
ENV BEXHOMA_SYNCH_GENERATE 0

WORKDIR /tmp
RUN mkdir -p /tmp/tpch

CMD ["/bin/bash", "-c", "/tmp/generator.sh"]
