# Loader for TPC-H data into IBM Db2

Loads pre-generated TPC-H `.tbl` files into IBM Db2 (Community Edition) as remote external tables.
It is the [PostgreSQL loader](../loader_postgresql/README.md) with [`load.py`](load.py) instead of `psql \COPY`; the execution flow, the synchronisation and the multi-tenant remapping are the same.

See [images/tpch/README.md](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/tpch/README.md) for the shared TPC-H pipeline design.

## Loading

```bash
python3 /tmp/load.py <table> <file>
```

* `load.py` sends the file from the loader pod to the server: `INSERT INTO <table> SELECT * FROM EXTERNAL '<chunk>' USING (DELIMITER '|' REMOTESOURCE 'YES' MAXERRORS 1)`, through `ibm_db` and its IBM Data Server Driver for ODBC and CLI
* chunks of `DB2_LOAD_CHUNK_ROWS` lines (default 20000), one transaction each, so the transaction log of the server needs room for one chunk per loader pod
* several loader pods load into the same table at the same time; the primary keys of `initschema-tpch.sql` are maintained row by row
* a chunk holds one row lock per row until its commit: with chunks of 200000 lines, four loaders filled the lock list, Db2 escalated to table locks and the loaders deadlocked (`SQL0911N`, reason code 2); 20000 lines keep them far below it
* `MAXERRORS 1`: a bad row fails its chunk, which is then not loaded at all
* the generator strips the trailing `|` (`TRANSFORM_RAW_DATA=1`); dates are read in the default format `YYYY-MM-DD`
* the tables are in the default schema of `BEXHOMA_USER` (`DB2INST1`) unless `BEXHOMA_SCHEMA` is set
* `load.py` ends with `BEXHOMA_LOADED:<rows>`, the rows Db2 reports as inserted; the loader compares it with the lines of the file and writes one `BEXHOMA_INGEST:<file>:<expected>:<reported>:ok|failed` line per file (#848). A failed file makes the pod exit 1. A chunk is retried, up to `DB2_LOAD_RETRIES` times, only on errors after which nothing of it is in the table: no connection (SQLSTATE class `08`, `57019`, `57011`, `57033`, `SQL30081N`, `SQL1224N`) or rolled back by a deadlock or lock timeout (SQLSTATE `40001`, `SQL0911N`).

## Environment variables

As the [PostgreSQL loader](../loader_postgresql/README.md#environment-variables), with these defaults:

* `BEXHOMA_PORT`: `50000`
* `BEXHOMA_USER`: `db2inst1`
* `BEXHOMA_PASSWORD`: empty, set by bexhoma from the JDBC `auth` of `cluster.config`
* `BEXHOMA_DATABASE`: `bexhoma`, the database of the tables
* `BEXHOMA_SCHEMA`: empty (= default schema of the user)
* `DB2_DELIMITER`: `|`
* `DB2_LOAD_CHUNK_ROWS`: `20000`
* `DB2_LOAD_RETRIES`: `10`

## Image

Base `python:3.12-slim` and `redis-tools` for `redis-cli`; the image contains no IBM software.
[`install-driver.sh`](install-driver.sh), sourced at the start of `loader.sh`, installs `ibm_db` (`IBM_DB_VERSION`, default 3.2.6, with IBM's Data Server Driver for ODBC and CLI) from PyPI into `DB2_DRIVER_CACHE` (default `/data/drivers` on the data volume, once per version; `/tmp/drivers` if that is not writable) and sets `PYTHONPATH`.
Several pods starting at the same time install into their own folders, the first one is kept. A pod that cannot install the driver exits with 1.
IBM allows passing on the driver only together with an end-user license that protects IBM as much as IBM's own, which the public images cannot give.
