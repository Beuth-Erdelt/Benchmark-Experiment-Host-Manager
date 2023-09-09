FROM tpcorg/hammerdb:v4.7

COPY ./generator.sh ./generator.sh
RUN ["chmod", "+x", "./generator.sh"]

ENV SF=1
ENV CHILD=1
ENV PARALLEL=1
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
ENV HAMMERDB_MYSQL_ENGINE innodb

# set async_client $pg_async_client;# Number of asynchronous clients per Vuser
# set async_verbose $pg_async_verbose;# Report activity of asynchronous clients
# set async_delay $pg_async_delay;# Delay in ms between logins of asynchronous clients

RUN mkdir -p /tmp/tpcc

CMD ["/bin/bash", "-c", "./generator.sh"]
