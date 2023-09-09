FROM tpcorg/hammerdb:v4.7

COPY ./benchmarker.sh ./benchmarker.sh
RUN ["chmod", "+x", "./benchmarker.sh"]

ENV BEXHOMA_CLIENT 1
ENV SF=1
ENV CHILD=1
ENV PARALLEL=4
ENV RNGSEED=123
ENV CONNECTION=monetdb
ENV EXPERIMENT=12345
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
ENV HAMMERDB_MYSQL_ENGINE innodb
ENV DBMSBENCHMARKER_START 1
ENV DBMSBENCHMARKER_NOW 1

# set async_client $pg_async_client;# Number of asynchronous clients per Vuser
# set async_verbose $pg_async_verbose;# Report activity of asynchronous clients
# set async_delay $pg_async_delay;# Delay in ms between logins of asynchronous clients

RUN mkdir -p /tmp/tpcc

CMD ["/bin/bash", "-c", "./benchmarker.sh"]
