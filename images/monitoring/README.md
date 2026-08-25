# Image of Monitoring Container

The image is based on [prom/prometheus](https://hub.docker.com/r/prom/prometheus).

This folder contains the Dockerfile for a Prometheus monitoring container used by Bexhoma.
At startup the container writes `$BEXHOMA_WORKERS` to `/etc/prometheus/prometheus-bexhoma.yml`
and launches Prometheus with that configuration.

Prometheus listens on port `9090` (web UI and HTTP API).
The time-series data directory is `/prometheus` (mounted as a volume).
A default `prometheus.yml` is bundled in the image for reference but is not used at
runtime — the live configuration always comes from `BEXHOMA_WORKERS`.

## Directory layout

```
images/monitoring/
├── Dockerfile         — image definition
├── prometheus.yml     — bundled reference config (NOT used at runtime)
└── README.md          — this file
```

There are no shell scripts and no subdirectories.

## Execution flow

The container has a single entry point defined inline in `CMD`:

1. Write `$BEXHOMA_WORKERS` to `/etc/prometheus/prometheus-bexhoma.yml`.
2. Start `/bin/prometheus` with `--config.file=/etc/prometheus/prometheus-bexhoma.yml`.

`ENTRYPOINT [""]` clears the default entrypoint of the `prom/prometheus` base
image (which would otherwise exec the binary directly and ignore `CMD`).

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

## Key design decisions

| Decision | Reason |
|---|---|
| Config supplied as an env-var string | Kubernetes can inject the full YAML via a ConfigMap without mounting a volume |
| `ENTRYPOINT [""]` clears base entrypoint | The `prom/prometheus` image sets its own `ENTRYPOINT`; clearing it lets `CMD` run as a plain shell string |
| Bundled `prometheus.yml` kept as reference | Provides a working example of the expected YAML structure without affecting runtime behaviour |

## Ports and volumes

| Resource | Value | Purpose |
|---|---|---|
| Port | `9090` | Prometheus web UI and HTTP API |
| Volume | `/prometheus` | Time-series data storage |

## Style conventions

- **Dockerfile**: Single `ENV BEXHOMA_WORKERS=""` with a comment explaining the purpose; `ENTRYPOINT` has an inline comment explaining why it clears the base entrypoint.
- **This README**: Documents every ENV and explains the relationship between `BEXHOMA_WORKERS`, the bundled config, and the runtime config file.
