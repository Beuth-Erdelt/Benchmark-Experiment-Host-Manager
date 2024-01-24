FROM debian:stable-20240110-slim

RUN apt-get -y update && apt-get dist-upgrade && apt-get clean all

RUN apt-get install -y build-essential
RUN apt-get install -y wget
RUN wget http://download.redis.io/redis-stable.tar.gz && tar xvzf redis-stable.tar.gz && cd redis-stable && make && cp src/redis-cli /usr/local/bin/ && chmod 755 /usr/local/bin/redis-cli

#&& apt-get install -y mysql-apt-config && apt-get install -y mysql-shell

RUN apt --fix-missing --fix-broken -y install
RUN apt-get install --fix-missing -y libcurl4
RUN apt-get install -y libssh-4
#RUN wget https://cdn.mysql.com//Downloads/MySQL-Shell/mysql-shell_8.0.36-1debian12_amd64.deb
#RUN dpkg -i mysql-shell_8.0.36-1debian12_amd64.deb
RUN wget https://dev.mysql.com/get/Downloads/MySQL-Shell/mysql-shell_8.3.0-1debian12_amd64.deb
RUN dpkg -i mysql-shell_8.3.0-1debian12_amd64.deb
RUN apt-get install mysql-shell -y
RUN apt-get update

RUN apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
	&& localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

#RUN apt-get install -y locales
#RUN dpkg-reconfigure locales
#RUN echo "LC_ALL=en_US.UTF-8" >> /etc/environment
#RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
#RUN echo "LANG=en_US.UTF-8" > /etc/locale.conf
#RUN locale-gen
ENV LC_ALL="en_US.UTF-8"
#ENV LANG="en_US.utf8"

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

#COPY ./loader-parallel.sh /tmp/loader.sh
COPY ./loader.sh /tmp/loader.sh
RUN ["chmod", "+x", "/tmp/loader.sh"]


CMD ["/bin/bash", "-c", "/tmp/loader.sh"]
#CMD ["/bin/bash", "-c", "while true; do sleep 2; done"]


