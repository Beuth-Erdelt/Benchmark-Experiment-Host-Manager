FROM tpcorg/hammerdb:v4.12

COPY ./benchmarker.sh ./benchmarker.sh
RUN ["chmod", "+x", "./benchmarker.sh"]

ENV SF=1
ENV BEXHOMA_CLIENT 1
ENV BEXHOMA_CHILD=1
ENV BEXHOMA_RNGSEED=123
ENV BEXHOMA_HOST="www.example.com"
ENV BEXHOMA_PORT 3307
ENV BEXHOMA_CONNECTION="monetdb"
ENV BEXHOMA_EXPERIMENT="12345"
ENV DATABASE demo
ENV USER tpc
ENV PASSWORD tpc
ENV HAMMERDB_TYPE postgresql
# Rampup time in minutes before first Transaction Count is taken
ENV HAMMERDB_RAMPUP 2
# Duration in minutes before second Transaction Count is taken
ENV HAMMERDB_DURATION 5
# Number of transactions before logging off
ENV HAMMERDB_ITERATIONS 10000000
ENV HAMMERDB_VUSERS 1 2 4 8
ENV HAMMERDB_NUM_VU=4
ENV HAMMERDB_MYSQL_ENGINE innodb
ENV DBMSBENCHMARKER_START 1
ENV DBMSBENCHMARKER_NOW 1
ENV HAMMERDB_TIMEPROFILE true
ENV HAMMERDB_ALLWAREHOUSES false
ENV HAMMERDB_KEYANDTHINK false

# set async_client $pg_async_client;# Number of asynchronous clients per Vuser
# set async_verbose $pg_async_verbose;# Report activity of asynchronous clients
# set async_delay $pg_async_delay;# Delay in ms between logins of asynchronous clients

#RUN cd /tmp; wget http://download.redis.io/redis-stable.tar.gz; tar xvzf redis-stable.tar.gz; cd redis-stable; make; cp src/redis-cli /usr/local/bin/; chmod 755 /usr/local/bin/redis-cli

RUN apt update && apt install -y redis-tools

RUN mkdir -p /tmp/tpcc

CMD ["/bin/bash", "-c", "./benchmarker.sh"]
