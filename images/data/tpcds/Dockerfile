FROM python:3

RUN mkdir -p /tmp/tpcds

COPY SF1.zip /tmp/tpcds/SF1.zip

WORKDIR /tmp/tpcds

RUN unzip SF1.zip

RUN rm SF1.zip

CMD mkdir -p /data;cp -r /tmp/tpcds /data
