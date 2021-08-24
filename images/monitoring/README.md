# Image of Monitoring Container

This image contains an instance of [Prometheus](https://prometheus.io/).

It expects the config file (normally `/etc/prometheus/prometheus.yml`) in `$BEXHOMA_WORKERS`.

## Build Commands

```
docker build -t perdelt/bexhoma:monitoring --no-cache .
docker push perdelt/bexhoma:monitoring
```
