# images/evaluator_dbmsbenchmarker — development notes

## Overview

The `images/evaluator_dbmsbenchmarker/` directory contains the Docker image template
for the Bexhoma evaluator that serves the DBMSBenchmarker results dashboard and a
Jupyter Notebook server.

## Directory layout

```
images/evaluator_dbmsbenchmarker/
├── Dockerfile_template    — image template; {version} replaced by create_Dockerfiles.py
├── create_Dockerfiles.py  — generates the versioned Dockerfile from Dockerfile_template
├── notebooks/             — evaluation notebooks copied into the image at build time
└── README.md              — image description
```

`Dockerfile_template` is the canonical source. Do not edit generated `Dockerfile` files directly.

---

## Execution flow

The image runs a single command at startup:

```
python ./dashboard.py -r /results
```

This starts the DBMSBenchmarker dashboard server on port `8050`, reading all experiment
results from the `/results` volume mount.  The Jupyter Notebook server must be started
separately (e.g. via `docker exec` or a sidecar pod command).

---

## Key design decisions

| Decision | Reason |
|---|---|
| Base image `python:3.12.8` instead of `3.14.2` | `python:3.14.2` is incompatible with Flask: `pkgutil` has no `get_loader` attribute |
| Python virtualenv at `/opt/venv` | Isolates the DBMSBenchmarker + Jupyter environment from the system Python; avoids conflicts with future system-level packages |
| Repository cloned twice | First clone provides the working directory and installed package; second clone (`DBMS-Benchmarker/DBMS-Benchmarker/`) exposes raw source files at a predictable path that the dashboard and notebooks reference |
| Notebooks copied at build time | Evaluation notebooks are version-controlled alongside the image; they do not require a runtime volume mount |

---

## Double git clone structure

The image clones the DBMSBenchmarker repository twice:

1. `/usr/src/app/DBMS-Benchmarker/` — outer clone; `WORKDIR` is set here; `dashboard.py`
   runs from here.
2. `/usr/src/app/DBMS-Benchmarker/DBMS-Benchmarker/` — inner clone; the `CMD` `ls`
   lines at startup confirm both paths exist.

This is intentional: the dashboard references raw source files from the inner clone.

---

## Dockerfile template

`Dockerfile_template` contains the placeholder `{version}` which `create_Dockerfiles.py`
replaces with the target DBMSBenchmarker Git tag (e.g. `v0.14.6`).  The placeholder
appears in the pip install step and both `git clone` steps.

---

## Style conventions

- **Dockerfile_template**: section headers for every operation; `{version}` placeholder
  clearly commented; base-image choice explained inline.
- **READMEs**: describes the services, port numbers, and any non-obvious structural
  decisions (double clone, virtualenv, base image constraint).
