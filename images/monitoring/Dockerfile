FROM prom/prometheus:v2.24.1

COPY prometheus.yml /etc/prometheus/prometheus.yml

USER       nobody
EXPOSE     9090
VOLUME     [ "/prometheus" ]
WORKDIR    /prometheus

ENTRYPOINT [ "" ]
CMD echo "$BEXHOMA_WORKERS" > /etc/prometheus/prometheus-bexhoma.yml ; echo "Test config" ; while [ ! -f /etc/prometheus/prometheus-bexhoma.yml ] ; do sleep 2 ; echo "Waiting for config" ; done ; /bin/prometheus \
	--config.file=/etc/prometheus/prometheus-bexhoma.yml \
    --storage.tsdb.path=/prometheus \
    --web.console.libraries=/etc/prometheus/console_libraries \
    --web.enable-lifecycle \
    --web.console.templates=/etc/prometheus/consoles
