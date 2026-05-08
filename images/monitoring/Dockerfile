######################################################################################
# Dockerfile for Bexhoma - Monitor
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma monitoring component.
#
# Base Image: prom/prometheus:v3.10.0
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2025-05-18
# Version: 1.0
# Description: Runs a Prometheus instance configured at container startup.
#   The Prometheus scrape configuration is supplied via the BEXHOMA_WORKERS
#   environment variable, written to /etc/prometheus/prometheus-bexhoma.yml
#   before the server starts.
######################################################################################
FROM prom/prometheus:v3.10.0

######################################################################################
# Bundle a default Prometheus configuration for reference
# (overwritten at runtime by the content of BEXHOMA_WORKERS)
######################################################################################
COPY prometheus.yml /etc/prometheus/prometheus.yml

USER       nobody
EXPOSE     9090
VOLUME     [ "/prometheus" ]
WORKDIR    /prometheus

######################################################################################
# Environment variables — runtime configuration
######################################################################################
# Prometheus scrape configuration supplied as a YAML string.
# Written to /etc/prometheus/prometheus-bexhoma.yml at container startup.
ENV BEXHOMA_WORKERS=""

######################################################################################
# Clear the base-image entrypoint so CMD runs as a plain shell string.
######################################################################################
ENTRYPOINT [ "" ]
CMD echo "$BEXHOMA_WORKERS" > /etc/prometheus/prometheus-bexhoma.yml ; \
    while [ ! -f /etc/prometheus/prometheus-bexhoma.yml ] ; do sleep 2 ; echo "Waiting for config" ; done ; \
    /bin/prometheus \
        --config.file=/etc/prometheus/prometheus-bexhoma.yml \
        --storage.tsdb.path=/prometheus \
        --web.console.libraries=/etc/prometheus/console_libraries \
        --web.enable-lifecycle \
        --web.console.templates=/etc/prometheus/consoles
