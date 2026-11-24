# Publishing Results

This page sets out what may be published from experiments run with Bexhoma, in the repository, in the documentation, in papers and in archives such as Zenodo.

## What may be published

* **Experiment specifications** for every DBMS: configurations in `cluster.config` and `experiments/`, entry scripts and their command lines, Kubernetes manifests, catalog contracts and schema files.
  They describe how to run an experiment and contain no results.
* **Results** only for DBMS whose licence allows disclosing benchmark results, and only after the checks below.
  Results are logs and their summaries, result folders, evaluations, reports, plots and numbers in texts.

Results obtained with Bexhoma are not TPC benchmark results, see the [note on TPC](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/THIRD_PARTY.md#note-on-tpc).

## DBMS whose results are kept internal

For these DBMS the repository describes how to deploy and run them, but holds no results.

| DBMS | Configuration key | Reason | Details |
|---|---|---|---|
| Microsoft SQL Server Developer | `SQLServer` | The licence requires Microsoft's prior written approval to disclose results of benchmark tests (#834). | [SQL Server](DBMS.md#sql-server) |
| Oracle Database Free | `OracleDB` | The terms of the database have no benchmark clause; the results are kept internal by decision of the maintainer (#828). | [Oracle Database Free](DBMS.md#oracle-database-free) |
| IBM Db2 Community Edition | `DB2` | Information about the Technology Preview Code in the image, including benchmarks, is IBM confidential (#829). | [IBM Db2](DBMS.md#ibm-db2-community-edition) |
| CedarDB Community Edition | `CedarDB` | Kept internal by decision of the maintainer. | [CedarDB](DBMS.md#cedardb) |

### How this is enforced

* The test scripts of these DBMS write their logs to `logs_tests/local`, which is git-ignored. So such a script must not run published DBMS as well: their logs would end up there too.
* `tests/test_unpublished_results.py` runs in CI on every pull request. It fails if a committed log names one of these DBMS, if a page under `docs/` or a top-level Markdown file contains one of their result markers (configuration or pod names, links to logs, `Experiment is limited to DBMS [...]`), or if a test script runs one of them without writing to `logs_tests/local`.
* Images do not contain software whose terms forbid passing it on: the Db2 driver and Microsoft's SQL Server tools are installed when a container starts, and no derived CedarDB image is built (see [THIRD_PARTY.md](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/THIRD_PARTY.md)).

## Adding a DBMS

Before the first result of a new DBMS is committed or published:

1. Read its licence terms, including those of the edition and image used, for clauses on benchmarks, on disclosing performance results, and on preview or evaluation features that must not be discussed.
2. If there is such a clause, or the terms are unclear, keep the results internal: add the DBMS to `UNPUBLISHED` in `tests/test_unpublished_results.py`, let its test script write to `logs_tests/local`, and note the reason in its section of [DBMS](DBMS.md) and in the table above.
3. Otherwise note the licence and the absence of a benchmark clause in its section of [DBMS](DBMS.md).

## Before publishing a result folder

Result folders and logs contain more than results. Before a result folder or a log leaves the cluster (in a paper's artifact, on Zenodo, in an issue):

* Check that the DBMS is not in the table above.
* Remove or replace credentials: `connections.config` and the logs contain JDBC URLs, user names and passwords.
* Remove or replace names of the infrastructure where needed: host and node names, IP addresses, storage classes, names from `cluster.config`.
* Keep the experiment specification with the results, so that they can be repeated, and name the versions of Bexhoma and DBMS-Benchmarker (both are recorded in the result folder).
