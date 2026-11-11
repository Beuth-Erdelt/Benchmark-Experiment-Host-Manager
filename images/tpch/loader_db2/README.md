# Loader for TPC-H data into IBM Db2

Loads pre-generated TPC-H `.tbl` files into IBM Db2 (Community Edition) as remote external tables.
It is the [PostgreSQL loader](../loader_postgresql/README.md) with [`load.py`](load.py) instead of `psql \COPY`; the execution flow, the synchronisation and the multi-tenant remapping are the same.

See [images/tpch/README.md](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/tpch/README.md) for the shared TPC-H pipeline design.

## Loading

```bash
python3 /tmp/load.py <table> <file>
```

* `load.py` sends the file from the loader pod to the server: `INSERT INTO <table> SELECT * FROM EXTERNAL '<chunk>' USING (DELIMITER '|' REMOTESOURCE 'YES' MAXERRORS 1)`, through `ibm_db` and its IBM Data Server Driver for ODBC and CLI
* chunks of `DB2_LOAD_CHUNK_ROWS` lines (default 200000), one transaction each, so the transaction log of the server needs room for one chunk per loader pod
* several loader pods load into the same table at the same time; the primary keys of `initschema-tpch.sql` are maintained row by row
* `MAXERRORS 1`: a bad row fails its chunk, which is then not loaded at all
* the generator strips the trailing `|` (`TRANSFORM_RAW_DATA=1`); dates are read in the default format `YYYY-MM-DD`
* the tables are in the default schema of `BEXHOMA_USER` (`DB2INST1`) unless `BEXHOMA_SCHEMA` is set
* `load.py` ends with `BEXHOMA_LOADED:<rows>`, the rows Db2 reports as inserted; the loader compares it with the lines of the file and writes one `BEXHOMA_INGEST:<file>:<expected>:<reported>:ok|failed` line per file (#848). A failed file makes the pod exit 1. Only connection errors (SQLSTATE class `08`, `57019`, `57011`, `57033`, `SQL30081N`, `SQL1224N`) are retried, per chunk, up to `DB2_LOAD_RETRIES` times.

## Environment variables

As the [PostgreSQL loader](../loader_postgresql/README.md#environment-variables), with these defaults:

* `BEXHOMA_PORT`: `50000`
* `BEXHOMA_USER`: `db2inst1`
* `BEXHOMA_PASSWORD`: empty, set by bexhoma from the JDBC `auth` of `cluster.config`
* `BEXHOMA_DATABASE`: `bexhoma`, the database of the tables
* `BEXHOMA_SCHEMA`: empty (= default schema of the user)
* `DB2_DELIMITER`: `|`
* `DB2_LOAD_CHUNK_ROWS`: `200000`
* `DB2_LOAD_RETRIES`: `10`

## Image

Base `python:3.12-slim`; `ibm_db` 3.2.6 from PyPI, which downloads IBM's redistributable `clidriver`, and `redis-tools` for `redis-cli`.
