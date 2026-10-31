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

## MariaDB ColumnStore

MariaDB ColumnStore is the columnar storage engine of MariaDB [2], under the name `MariaDBCS` in bexhoma.
Bexhoma runs the official image `mariadb` with the template [deploymenttemplate-MariaDBCS.yml](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-MariaDBCS.yml), which installs the plugin at every start, so the pods need access to the package repositories.
It runs on a single node.

| Workload | Runs | Note |
|---|---|---|
| TPC-H | yes | no refresh stream |
| SSB | yes | normal and flat schema |
| TPC-DS | partly | 80 of 99 queries, with 11 rewritten, see below |

MariaDBCS loads with one pod, `-nlp` is ignored.
See [DBMS](DBMS.html#mariadb-columnstore) for the reasons of these limits and the list of queries.

The test scripts [`scripts/test-docs-mariadbcs.sh`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-mariadbcs.sh) and [`scripts/test-docs-mariadbcs.ps1`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-mariadbcs.ps1) run these workloads, one after the other.
They write their logs to `logs_tests/local`, which is not part of the repository.

An example call, TPC-DS at SF 1 on a persistent volume:

```bash
bexhoma tpcds \
  -dbms MariaDBCS \
  -sf 1 \
  -xis \
  -rst $BEXHOMA_STORAGE_CLASS -rss 30Gi \
  -nc 2 \
  -ar \
  -ks no \
  -tr \
  run
```

19 queries are refused by ColumnStore, so the test `No SQL errors` fails in this run. 11 queries run with a variant, see [TPC-DS queries](Queries-TPC-DS.html).

[1] https://cedardb.com

[2] https://mariadb.com/docs/analytics/mariadb-columnstore
