# TPC-H Refresh Loader — SQL Server

Applies TPC-H RF1 (INSERT) and RF2 (DELETE) operations to a SQL Server database, with `bcp` and `sqlcmd` of `mssql-tools18`.
Reads pre-generated update files from `/data/tpch-refresh/SF<SF>/` on the PVC.
Runs as the main container (`benchmark_run=2`) of the refresh benchmarker job,
in parallel with the query-stream benchmarker (`benchmark_run=1`).

See [images/tpch_refresh/README.md](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/tpch_refresh/README.md) for the shared refresh-stream pipeline design.

## Environment variables

As the [PostgreSQL refresh loader](../loader_postgresql/README.md#environment-variables), with these defaults:

| Variable | Default | Description |
|---|---|---|
| `BEXHOMA_PORT` | `1433` | SQL Server port |
| `BEXHOMA_USER` | `sa` | SQL Server login |
| `BEXHOMA_PASSWORD` | empty | set by bexhoma from the JDBC `auth` of `cluster.config` |
| `BEXHOMA_DATABASE` | `tpch` | Target database |
| `BEXHOMA_SCHEMA` | empty | Target schema; empty = `dbo` |
| `BEXHOMA_CONNECTION` | `sqlserver` | Connection name (Redis counter key) |
| `MSSQL_TOOLS_VERSION` | `18.7.1.1-1` | Version of `msodbcsql18` and `mssql-tools18` |
| `MSSQL_TOOLS_CACHE` | `/data/drivers` | Cache of the downloaded packages on the data volume (`/tmp/drivers` if not writable) |

The image contains no Microsoft software: the licence terms of `msodbcsql18` and `mssql-tools18` do not allow publishing them in an image.
[`install-tools.sh`](install-tools.sh) (a copy of `images/tpch/loader_sqlserver/install-tools.sh`), sourced at the start of `loader.sh`, downloads both packages from `packages.microsoft.com` into the cache, once per version, and installs them with `ACCEPT_EULA=Y`.

## Execution flow

Steps 1-4 (set range, data folder, job and round counters) are those of the [PostgreSQL refresh loader](../loader_postgresql/README.md#execution-flow).
For each set K:

* **RF1**: `bcp <schema>.orders|lineitem in <file>.tbl.u<K> -u -c -t '|' -r 0x0a -m 1`, one transaction per file; the reported `<n> rows copied` must equal the lines of the file.
* **RF2**: a staging table `<schema>.tpch_refresh_delete_<K>` (`orderkey BIGINT`) is created, filled by `bcp` from `delete.<K>`, both `DELETE ... WHERE ... IN (SELECT orderkey ...)` run in one transaction (`XACT_ABORT ON`), and the table is dropped. A `#temp` table cannot be used: `bcp` and `sqlcmd` are separate connections.

One `BEXHOMA_INGEST` line per unit (#848); a failed unit makes the pod exit 1.
