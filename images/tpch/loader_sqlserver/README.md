# Loader for TPC-H data into SQL Server

Loads pre-generated TPC-H `.tbl` files into Microsoft SQL Server using `bcp` of `mssql-tools18`.
It is the [PostgreSQL loader](../loader_postgresql/README.md) with `bcp` instead of `psql \COPY`; the execution flow, the synchronisation and the multi-tenant remapping are the same.

See [images/tpch/README.md](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/tpch/README.md) for the shared TPC-H pipeline design.

## Loading

```bash
bcp <schema>.<table> in <file> -S <host>,<port> -U <user> -P <password> -d <database> -u -c -t '|' -r 0x0a -h TABLOCK -m 1
```

* one transaction per file (no `-b`), so a failed file leaves nothing behind and can be retried
* `-h TABLOCK`: table lock, minimally logged bulk load
* `-r 0x0a`: the generator strips the trailing `|` (`TRANSFORM_RAW_DATA=1`), rows end with LF
* `-u`: trusts the self-signed certificate of the server (ODBC Driver 18 encrypts by default)
* the schema is `dbo` unless `BEXHOMA_SCHEMA` is set
* `bcp` answers `<n> rows copied.`; the loader compares it with the lines of the file and writes one `BEXHOMA_INGEST:<file>:<expected>:<reported>:ok|failed` line per file (#848). A failed file makes the pod exit 1. Only connection errors (login timeout, TCP provider) are retried.

## Environment variables

As the [PostgreSQL loader](../loader_postgresql/README.md#environment-variables), with these defaults:

* `BEXHOMA_PORT`: `1433`
* `BEXHOMA_USER`: `sa`
* `BEXHOMA_PASSWORD`: empty, set by bexhoma from the JDBC `auth` of `cluster.config`
* `BEXHOMA_DATABASE`: `tpch`
* `BEXHOMA_SCHEMA`: empty (= `dbo`)

## Image

Base `ubuntu:22.04`; `msodbcsql18`, `mssql-tools18` (with `ACCEPT_EULA=Y`) from `packages.microsoft.com`, and `redis-tools`.
