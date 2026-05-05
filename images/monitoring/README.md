# Image of Monitoring Container

The image is based on [prom/prometheus](https://hub.docker.com/r/prom/prometheus).

This folder contains the Dockerfile for a Prometheus monitoring container used by Bexhoma.
At startup the container writes `$BEXHOMA_WORKERS` to `/etc/prometheus/prometheus-bexhoma.yml`
and launches Prometheus with that configuration.

Prometheus listens on port `9090` (web UI and HTTP API).
The time-series data directory is `/prometheus` (mounted as a volume).
A default `prometheus.yml` is bundled in the image for reference but is not used at
runtime — the live configuration always comes from `BEXHOMA_WORKERS`.

## Environment variables

### Prometheus configuration

* `BEXHOMA_WORKERS`: Full YAML content of the Prometheus scrape configuration.
  Written to `/etc/prometheus/prometheus-bexhoma.yml` at container startup.
  When empty the container starts with an empty configuration and Prometheus will
  report a parse error; always supply a valid YAML string.

## Default prometheus.yml

The bundled `prometheus.yml` defines two scrape jobs as a reference template:

| Job | Target | Interval |
|---|---|---|
| `monitor-node` | `localhost:9300` | 3 s |
| `monitor-gpu` | `localhost:9400` | 3 s |

These targets are **not active** unless `BEXHOMA_WORKERS` contains equivalent
scrape-config blocks.
