# Loader for TPC-H data into Oracle Database

Loads pre-generated TPC-H `.tbl` files into Oracle Database (Free) using SQL*Loader (`sqlldr` of the Oracle Instant Client tools).
It is the [PostgreSQL loader](../loader_postgresql/README.md) with `sqlldr` instead of `psql \COPY`; the execution flow, the synchronisation and the multi-tenant remapping are the same.

See [images/tpch/README.md](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/tpch/README.md) for the shared TPC-H pipeline design.

## Loading

```bash
sqlldr parfile=/tmp/sqlldr.par control=/tmp/<table>.ctl data=<file> errors=0 rows=50000 bindsize=20000000 readsize=20000000
```

* one control file per table in [`ctl/`](ctl/), `BEXHOMA_TABLE` is replaced by `<schema>.<table>`; dates are read with `DATE "YYYY-MM-DD"`
* conventional path: several loader pods load into the same table at the same time (a direct path load locks the table), and the primary keys of `initschema-tpch.sql` are maintained row by row; one commit per 50000 rows
* `errors=0`: the load stops at the first bad row
* the generator strips the trailing `|` (`TRANSFORM_RAW_DATA=1`)
* the schema is `BEXHOMA_DATABASE` (Oracle: schema = user, `bexhoma`) unless `BEXHOMA_SCHEMA` is set
* the connection `user/"password"@//host:port/ORACLE_SERVICE` is in a parameter file, not on the command line
* the log of `sqlldr` reports `<n> Rows successfully loaded.`; the loader compares it with the lines of the file and writes one `BEXHOMA_INGEST:<file>:<expected>:<reported>:ok|failed` line per file (#848). A failed file makes the pod exit 1. Only connection errors (`ORA-12541`, `ORA-12514`, `ORA-12528`, `ORA-12537`, `ORA-12170`, `ORA-01033`, `ORA-01109`) without loaded rows are retried.

## Environment variables

As the [PostgreSQL loader](../loader_postgresql/README.md#environment-variables), with these defaults:

* `BEXHOMA_PORT`: `1521`
* `BEXHOMA_USER`: `bexhoma`
* `BEXHOMA_PASSWORD`: empty, set by bexhoma from the JDBC `auth` of `cluster.config`
* `BEXHOMA_DATABASE`: `bexhoma`, the schema of the tables
* `BEXHOMA_SCHEMA`: empty (= `BEXHOMA_DATABASE`)
* `ORACLE_SERVICE`: `FREEPDB1`, the service of the pluggable database

## Image

Base `oraclelinux:9-slim`; `oracle-instantclient-basic`, `-sqlplus` and `-tools` (23ai) from the Oracle Linux yum repository, and `redis` for `redis-cli`.
`sqlldr` is in `/usr/lib/oracle/23/client64/bin`, which is on the `PATH`.
