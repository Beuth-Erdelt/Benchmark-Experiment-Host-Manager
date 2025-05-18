######################################################################################
# Dockerfile for Bexhoma - Monitor
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma component "monitoring".
#
# Base Image: prom/prometheus:v2.24.1
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2025-05-18
# Version: 1.0
# Description: This container runs a 
# It expects the content of the config file (normally `/etc/prometheus/prometheus.yml`) as a string in `$BEXHOMA_WORKERS`.
######################################################################################
FROM prom/prometheus:v2.24.1

COPY prometheus.yml /etc/prometheus/prometheus.yml

USER       nobody
EXPOSE     9090
VOLUME     [ "/prometheus" ]
WORKDIR    /prometheus

ENV BEXHOMA_WORKERS

ENTRYPOINT [ "" ]
CMD echo "$BEXHOMA_WORKERS" > /etc/prometheus/prometheus-bexhoma.yml ; echo "Test config" ; while [ ! -f /etc/prometheus/prometheus-bexhoma.yml ] ; do sleep 2 ; echo "Waiting for config" ; done ; /bin/prometheus \
	--config.file=/etc/prometheus/prometheus-bexhoma.yml \
    --storage.tsdb.path=/prometheus \
    --web.console.libraries=/etc/prometheus/console_libraries \
    --web.enable-lifecycle \
    --web.console.templates=/etc/prometheus/consoles
