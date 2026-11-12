# TPC-H Refresh Loader — Oracle Database

Applies TPC-H RF1 (INSERT) and RF2 (DELETE) operations to an Oracle database (Free), with `sqlldr` and `sqlplus` of the Oracle Instant Client.
Reads pre-generated update files from `/data/tpch-refresh/SF<SF>/` on the PVC.
Runs as the main container (`benchmark_run=2`) of the refresh benchmarker job,
in parallel with the query-stream benchmarker (`benchmark_run=1`).

See [images/tpch_refresh/README.md](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/tpch_refresh/README.md) for the shared refresh-stream pipeline design.

## Environment variables

As the [PostgreSQL refresh loader](../loader_postgresql/README.md#environment-variables), with these defaults:

| Variable | Default | Description |
|---|---|---|
| `BEXHOMA_PORT` | `1521` | Oracle listener port |
| `BEXHOMA_USER` | `bexhoma` | Oracle user |
| `BEXHOMA_PASSWORD` | empty | set by bexhoma from the JDBC `auth` of `cluster.config` |
| `BEXHOMA_DATABASE` | `bexhoma` | Schema (= user) of the tables |
| `BEXHOMA_SCHEMA` | empty | Target schema; empty = `BEXHOMA_DATABASE` |
| `ORACLE_SERVICE` | `FREEPDB1` | Service of the pluggable database |
| `BEXHOMA_CONNECTION` | `oracle` | Connection name (Redis counter key) |

## Execution flow

Steps 1-4 (set range, data folder, job and round counters) are those of the [PostgreSQL refresh loader](../loader_postgresql/README.md#execution-flow).
For each set K:

* **RF1**: `sqlldr` with the control files `ctl/orders.ctl` and `ctl/lineitem.ctl` into `<schema>.orders|lineitem` from `<file>.tbl.u<K>`, conventional path (the query streams run at the same time), `errors=0`; the reported `<n> Rows successfully loaded.` must equal the lines of the file.
* **RF2**: a staging table `<schema>.tpch_refresh_delete_<K>` (`orderkey NUMBER(12)`) is created, filled by `sqlldr` from `delete.<K>` (`ctl/delete.ctl`), both `DELETE ... WHERE ... IN (SELECT orderkey ...)` run in one transaction (`sqlplus`, `WHENEVER SQLERROR EXIT FAILURE`), and the table is dropped (`PURGE`).

The connection is in a parameter file (`sqlldr`) and a login script (`sqlplus /nolog`), not on the command line.
One `BEXHOMA_INGEST` line per unit (#848); a failed unit makes the pod exit 1.
