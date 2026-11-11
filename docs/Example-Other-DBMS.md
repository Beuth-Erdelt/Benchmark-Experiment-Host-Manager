# Example: Other DBMS

This page introduces DBMS that bexhoma can run, but that have no worked example with results.
Each section says what the DBMS is, which workloads run on it, which test script covers them, and shows one example call.

See [DBMS](DBMS.html) for the configuration of each DBMS.

## CedarDB

CedarDB is an HTAP DBMS with a PostgreSQL wire protocol, the commercial successor of TUM's Umbra [1].
Bexhoma runs the Community Edition image `cedardb/cedardb` with the template [deploymenttemplate-CedarDB.yml](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-CedarDB.yml).
The Community Edition turns read-only above 64 GiB of data.

| Workload | Runs | Note |
|---|---|---|
| TPC-H | yes | no SF 100, because of the 64 GiB limit |
| SSB | yes | normal and flat schema |
| YCSB | yes | workloads with concurrent updates lose some of them, see below |
| Benchbase `tpcc`, `ycsb` | yes | |
| Benchbase `chbenchmark` | yes | Q22 and sometimes Q15 fail, so `num_errors` is not 0 |
| Benchbase `twitter` | no | the benchmark needs `SERIALIZABLE`, which CedarDB refuses |

CedarDB does not wait on a write conflict, the transaction fails.
With YCSB workload A this fails the test `Execution Phase: contains FAILED column`.
See [DBMS](DBMS.html#cedardb) for the reasons of these limits.

The test scripts [`scripts/test-docs-cedardb.sh`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-cedardb.sh) and [`scripts/test-docs-cedardb.ps1`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-cedardb.ps1) run all these workloads except `twitter`, one after the other.
They write their logs to `logs_tests/local`, which is not part of the repository.

An example call, TPC-H at SF 1 on a persistent volume:

```bash
bexhoma tpch \
  -dbms CedarDB \
  -sf 1 \
  -nlp 8 \
  -xii -xic -xis \
  -rst $BEXHOMA_STORAGE_CLASS -rss 50Gi \
  -nc 2 \
  -ar \
  -ks no \
  -tr \
  run
```

`$BEXHOMA_STORAGE_CLASS` is the storage class of your cluster, set in `scripts/testfunctions.sh` for the test scripts.
The second run (`-nc 2`) restarts the SUT on the same data, `-ar` runs the reset scripts before each round.

## SQL Server

Microsoft SQL Server is a relational DBMS [2].
Bexhoma runs SQL Server 2022, Developer edition, from the image `mcr.microsoft.com/mssql/server` with the template [deploymenttemplate-SQLServer.yml](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-SQLServer.yml).

The license terms of the Developer edition do not allow disclosing the results of a benchmark test to a third party without Microsoft's prior written approval.
Bexhoma therefore runs SQL Server for internal tests only: there are no results of it on this page, in the documentation or in the repository.

| Workload | Runs | Note |
|---|---|---|
| TPC-H | yes | dialect `TSQL` of the query file; also with a refresh stream (`-xrs`) |
| YCSB | yes | JDBC binding |
| Benchbase `tpcc` | yes | the only Benchbase benchmark with a SQL Server config |
| HammerDB TPC-C | yes | ODBC Driver 18 for SQL Server |
| TPC-DS, SSB | no | the query files have no `TSQL` variants |

See [DBMS](DBMS.html#sql-server) for the deployment, the loaders and the scripts.

The test scripts [`scripts/test-docs-sqlserver.sh`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-sqlserver.sh) and [`scripts/test-docs-sqlserver.ps1`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-sqlserver.ps1) run all these workloads, one after the other.
They write their logs to `logs_tests/local`, which is not part of the repository; the logs must not be passed on.

An example call, TPC-H at SF 1 on a persistent volume:

```bash
bexhoma tpch \
  -dbms SQLServer \
  -sf 1 \
  -nlp 8 \
  -xii -xic -xis \
  -rst $BEXHOMA_STORAGE_CLASS -rss 50Gi \
  -nc 2 \
  -ar \
  -ks no \
  -tr \
  run
```

`-xii`, `-xic` and `-xis` create the indexes, add the foreign keys and update the statistics after loading.

[1] https://cedardb.com

[2] https://www.microsoft.com/sql-server
