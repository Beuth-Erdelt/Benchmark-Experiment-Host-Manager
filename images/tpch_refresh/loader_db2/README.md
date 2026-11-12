# TPC-H Refresh Loader for IBM Db2

Applies the TPC-H refresh functions RF1 (insert) and RF2 (delete) to IBM Db2, as the refresh stream (`-xrs`) next to the query streams.
The execution flow, the synchronisation and the result lines are those of the [Oracle refresh loader](../loader_oracle/README.md).

See [images/tpch_refresh/README.md](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/tpch_refresh/README.md) for the shared pipeline design.

## Refresh functions

* RF1: [`load.py`](load.py) inserts `orders.tbl.u<K>` and `lineitem.tbl.u<K>` as remote external tables, one transaction per chunk of `DB2_LOAD_CHUNK_ROWS` lines; it is a copy of [`images/tpch/loader_db2/load.py`](../../tpch/loader_db2/load.py) (each image is built from its own folder), keep both the same
* RF2: [`rf2.py`](rf2.py) deletes the lineitems and orders whose keys are in `delete.<K>` in one transaction; the delete file is read as a remote external table, so there is no staging table
* one `BEXHOMA_INGEST:<unit>:<expected>:<reported>:ok|failed` line per unit (#848); RF2 has no expected count (a set applied again deletes nothing). A failed unit makes the pod exit 1.

## Environment variables

As the [Oracle refresh loader](../loader_oracle/README.md), with these defaults:

* `BEXHOMA_PORT`: `50000`
* `BEXHOMA_USER`: `db2inst1`
* `BEXHOMA_DATABASE`: `bexhoma`, the database of the tables
* `BEXHOMA_SCHEMA`: empty (= default schema of the user)
* `DB2_DELIMITER`, `DB2_LOAD_CHUNK_ROWS`, `DB2_LOAD_RETRIES`: as the [TPC-H loader](../../tpch/loader_db2/README.md)

## Image

Base `python:3.12-slim` and `redis-tools` for `redis-cli`; the image contains no IBM software.
[`install-driver.sh`](install-driver.sh) (a copy of [`images/tpch/loader_db2/install-driver.sh`](../../tpch/loader_db2/install-driver.sh), keep both the same), sourced at the start of `loader.sh`, installs `ibm_db` (`IBM_DB_VERSION`, default 3.2.6, with IBM's Data Server Driver for ODBC and CLI) from PyPI into `DB2_DRIVER_CACHE` (default `/data/drivers` on the data volume, once per version; `/tmp/drivers` if that is not writable) and sets `PYTHONPATH`.
Several pods starting at the same time install into their own folders, the first one is kept. A pod that cannot install the driver exits with 1.
IBM allows passing on the driver only together with an end-user license that protects IBM as much as IBM's own, which the public images cannot give.
