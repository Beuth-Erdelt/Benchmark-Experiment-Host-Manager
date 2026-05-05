# images/monitoring — development notes

## Overview

The `images/monitoring/` directory contains a single Docker image that runs a
Prometheus instance for Bexhoma experiment monitoring.

## Directory layout

```
images/monitoring/
├── Dockerfile         — image definition
├── prometheus.yml     — bundled reference config (NOT used at runtime)
└── README.md          — environment variable reference
```

There are no shell scripts and no subdirectories.

---

## Execution flow

The container has a single entry point defined inline in `CMD`:

1. Write `$BEXHOMA_WORKERS` to `/etc/prometheus/prometheus-bexhoma.yml`.
2. Start `/bin/prometheus` with `--config.file=/etc/prometheus/prometheus-bexhoma.yml`.

`ENTRYPOINT [""]` clears the default entrypoint of the `prom/prometheus` base
image (which would otherwise exec the binary directly and ignore `CMD`).

The bundled `prometheus.yml` is **never read at runtime**; it exists only as a
reference template showing two scrape jobs (`monitor-node` on port 9300,
`monitor-gpu` on port 9400).  The live configuration always comes from
`BEXHOMA_WORKERS`.

---

## Key design decisions

| Decision | Reason |
|---|---|
| Config supplied as an env-var string | Kubernetes can inject the full YAML via a ConfigMap without mounting a volume |
| `ENTRYPOINT [""]` clears base entrypoint | The `prom/prometheus` image sets its own `ENTRYPOINT`; clearing it lets `CMD` run as a plain shell string |
| Bundled `prometheus.yml` kept as reference | Provides a working example of the expected YAML structure without affecting runtime behaviour |

---

## Ports and volumes

| Resource | Value | Purpose |
|---|---|---|
| Port | `9090` | Prometheus web UI and HTTP API |
| Volume | `/prometheus` | Time-series data storage |

---

## Style conventions

- **Dockerfile**: Single `ENV BEXHOMA_WORKERS=""` with a comment explaining the purpose; `ENTRYPOINT` has an inline comment explaining why it clears the base entrypoint.
- **README**: Documents every ENV and explains the relationship between `BEXHOMA_WORKERS`, the bundled config, and the runtime config file.
