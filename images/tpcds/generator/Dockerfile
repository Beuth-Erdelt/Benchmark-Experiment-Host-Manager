FROM eclipse-temurin:11

# FROM alpine:3.16.2
#RUN apk add --no-cache bash
#RUN apk add --no-cache redis
#COPY ./tpc-ds-tool.zip /tmp/
#RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
RUN apt-get update
RUN apt-get install -y make
RUN apt-get install -y gcc
#RUN apt-get install -y build-essential

RUN cd /tmp; wget http://download.redis.io/redis-stable.tar.gz; tar xvzf redis-stable.tar.gz; cd redis-stable; make; cp src/redis-cli /usr/local/bin/; chmod 755 /usr/local/bin/redis-cli

COPY ./tpc_eula.txt ./tpc_eula.txt
COPY ./tpcds.idx /tmp/tpcds.idx
COPY ./dsdgen /tmp/dsdgen
RUN ["chmod", "+x", "/tmp/dsdgen"]

COPY ./generator.sh /tmp/generator.sh
RUN ["chmod", "+x", "/tmp/generator.sh"]

ENV SF=1
ENV NUM_PODS=4
ENV CHILD=1
ENV RNGSEED=123
ENV CONNECTION=monetdb
ENV EXPERIMENT=12345
ENV STORE_RAW_DATA=0
ENV STORE_RAW_DATA_RECREATE=0
ENV TRANSFORM_RAW_DATA=1
ENV BEXHOMA_SYNCH_GENERATE 0

WORKDIR /tmp
RUN mkdir -p /tmp/tpcds

CMD ["/bin/bash", "-c", "/tmp/generator.sh"]

#CMD ["/bin/bash", "-c", "/tmp/dsdgen -dir /tmp/ -scale $SF -parallel $NUM_PODS -child $CHILD -verbose -RNGSEED $RNGSEED; while true; do sleep 2; done"]
#CMD ["/bin/bash", "-c", "while true; do sleep 2; done"]
