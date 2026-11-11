# Loader for TPC-DS data into IBM Db2

Loads pre-generated TPC-DS `.dat` files into IBM Db2 (Community Edition) as remote external tables.
It is the [PostgreSQL loader](../loader_postgresql/README.md) with [`load.py`](load.py) instead of `psql \COPY`; the execution flow and the synchronisation are the same.

See [images/tpcds/README.md](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/tpcds/README.md) for the shared TPC-DS pipeline design.

## Loading

```bash
python3 /tmp/load.py <table> <file>
```

* [`load.py`](load.py) is a copy of [`images/tpch/loader_db2/load.py`](../../tpch/loader_db2/load.py) (each image is built from its own folder), keep both the same; see the [TPC-H loader](../../tpch/loader_db2/README.md#loading) for how it loads
* `DB2_EMPTY_AS_NULL=1`: an empty field is `NULL` (`NULLVALUE ''`), as `null ''` of PostgreSQL
* one `BEXHOMA_INGEST:<file>:<expected>:<reported>:ok|failed` line per file (#848); a failed file makes the pod exit 1

## Environment variables

As the [PostgreSQL loader](../loader_postgresql/README.md#environment-variables), with these defaults:

* `BEXHOMA_PORT`: `50000`
* `BEXHOMA_USER`: `db2inst1`
* `BEXHOMA_PASSWORD`: empty, set by bexhoma from the JDBC `auth` of `cluster.config`
* `BEXHOMA_DATABASE`: `bexhoma`, the database of the tables
* `BEXHOMA_SCHEMA`: empty (= default schema of the user)
* `DB2_DELIMITER`: `|`
* `DB2_EMPTY_AS_NULL`: `1`
* `DB2_LOAD_CHUNK_ROWS`: `200000`
* `DB2_LOAD_RETRIES`: `10`

## Image

Base `python:3.12-slim`; `ibm_db` 3.2.6 from PyPI, which downloads IBM's redistributable `clidriver`, and `redis-tools` for `redis-cli`.
