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

Base `python:3.12-slim`; `ibm_db` 3.2.6 from PyPI, which downloads IBM's redistributable `clidriver`, and `redis-tools` for `redis-cli`.
