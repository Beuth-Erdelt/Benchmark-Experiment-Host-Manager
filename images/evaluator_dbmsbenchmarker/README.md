# Evaluator for DBMSBenchmarker experiments

The image is based on [DBMSBenchmarker](https://github.com/Beuth-Erdelt/DBMS-Benchmarker).

This folder contains the Dockerfile template for an evaluator that serves the
DBMSBenchmarker results dashboard and a Jupyter Notebook server for post-experiment
analysis.

## Services

* **Dashboard** — DBMSBenchmarker result dashboard at port `8050` (reads from `/results`).
* **Jupyter Notebook** — interactive evaluation environment at port `8888`; password: `admin`.

## Environment variables

This image has no configurable runtime environment variables. The result folder is
hard-coded to `/results`; mount the experiment results volume at that path.

## Notebooks

Evaluation notebooks are copied from `./notebooks/` at build time into
`/usr/src/app/DBMS-Benchmarker/notebooks/` inside the image.

## Notes

* The base image is `python:3.12.8`. `python:3.14.2` is not used because it is
  incompatible with Flask (`pkgutil` has no `get_loader` attribute).
* A Python virtualenv is created at `/opt/venv`; all Python packages (including
  DBMSBenchmarker and Jupyter) are installed inside it.
* The DBMSBenchmarker repository is cloned twice: once as the working tree root, and
  once as a sub-directory (`DBMS-Benchmarker/DBMS-Benchmarker/`) to expose raw source
  files alongside the installed package.

See [DBMSBenchmarker docs](https://github.com/Beuth-Erdelt/DBMS-Benchmarker) for
details on the dashboard and notebook API.
