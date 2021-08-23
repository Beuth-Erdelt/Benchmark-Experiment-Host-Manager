FROM python:3

RUN mkdir -p /tmp/tpch

COPY SF1.zip /tmp/tpch/SF1.zip

WORKDIR /tmp/tpch

RUN unzip SF1.zip

RUN rm SF1.zip

CMD mkdir -p /data;cp -r /tmp/tpch /data
