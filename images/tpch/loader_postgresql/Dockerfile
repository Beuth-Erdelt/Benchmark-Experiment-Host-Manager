#FROM debian:stable-20221004-slim
FROM alpine:3.15

RUN apk update

RUN apk add --no-cache bash

RUN apk add --no-cache nano

RUN apk add --no-cache make cmake gcc libc-dev

RUN cd /tmp; wget http://download.redis.io/redis-stable.tar.gz; tar xvzf redis-stable.tar.gz; cd redis-stable; make; cp src/redis-cli /usr/local/bin/; chmod 755 /usr/local/bin/redis-cli

RUN apk update && apk --update add postgresql-client

ENV NUM_PODS=4
ENV CHILD=1
ENV BEXHOMA_HOST="www.example.com"
ENV BEXHOMA_PORT 50000
ENV BEXHOMA_CONNECTION="monetdb"
ENV BEXHOMA_EXPERIMENT="12345"
ENV DATABASE postgres
ENV STORE_RAW_DATA=0
ENV BEXHOMA_SYNCH_LOAD 0
ENV BEXHOMA_USER postgres

WORKDIR /tmp

RUN mkdir -p /tmp/tpch

COPY ./loader.sh /tmp/loader.sh
RUN ["chmod", "+x", "/tmp/loader.sh"]


CMD ["/bin/bash", "-c", "/tmp/loader.sh"]
