# Third-party material

Bexhoma is licensed under the GNU Affero General Public License v3.0 or later (see [LICENSE](LICENSE)).
This file lists material from others that is included in the repository, built into the Docker images in `images/`, or needed to run experiments, with its licence.
Licences were checked on 2026-11-19 from the projects' repositories and package metadata.

## Included in the repository

| Material | Location | Source | Licence |
|---|---|---|---|
| TPC-H and TPC-DS query texts | `experiments/tpch/`, `experiments/tpcds/` | Derived from the [TPC-H](https://www.tpc.org/tpch/) and [TPC-DS](https://www.tpc.org/tpcds/) specifications, adapted to several SQL dialects | See the note on TPC below |
| TPC End User License Agreement | `images/tpch/generator/`, `images/tpch_refresh/generator/`, `images/ssb/generator/` | TPC | TPC EULA |
| SSB query texts | `experiments/ssb/` | Star Schema Benchmark by O'Neil et al., derived from TPC-H | See the note on TPC below |
| YCSB workload files | `images/ycsb/*/workloads/` | [YCSB](https://github.com/brianfrankcooper/YCSB) | Apache-2.0 (`LICENSE.txt` next to them) |
| Logo and icons | `docs/logo/` | Original work by Patrick K. Erdelt | CC BY 4.0, see [docs/logo/README.md](docs/logo/README.md) |

The TPC data generators themselves (`dbgen`, `dsdgen` and their data files) are not in the repository.
They are built from the kits downloaded from the TPC and copied into the build context of the generator images (see the READMEs in `images/tpch/generator/` and `images/tpcds/generator/`).

## Built into the Docker images

The images are not part of the Python package; they are built from `images/`, published on [Docker Hub](https://hub.docker.com/u/bexhoma) as `bexhoma/*` and pulled by the Kubernetes manifests.
Publishing them redistributes the components below, under the licences listed.
Each image that adds components of others contains a folder `/licenses/` with a `NOTICE` (components, versions, licences, sources; kept as `NOTICE` next to the Dockerfile) and the licence texts of the versions used.
The generator images of TPC-H, TPC-DS and SSB carry the complete TPC EULA and the legend required by its clause 9 ("THE TPC SOFTWARE IS AVAILABLE WITHOUT CHARGE FROM TPC.") in `/licenses/` and in an image label.
Packages installed with the package manager of a base image (apt, apk, dnf) bring their own copyright files; the base images carry their own licences.

| Image | Component | Source | Licence |
|---|---|---|---|
| `benchmarker_dbmsbenchmarker`, `evaluator_dbmsbenchmarker` | DBMS-Benchmarker | [Beuth-Erdelt/DBMS-Benchmarker](https://github.com/Beuth-Erdelt/DBMS-Benchmarker) | AGPL-3.0-or-later |
| `benchbase` | Benchbase (base image `benchbase.azurecr.io/benchbase`) | [cmu-db/benchbase](https://github.com/cmu-db/benchbase) | Apache-2.0 |
| `hammerdb` | HammerDB (base image `tpcorg/hammerdb`) | [TPC-Council/HammerDB](https://github.com/TPC-Council/HammerDB) | GPL-3.0 |
| `ycsb` | YCSB | [brianfrankcooper/YCSB](https://github.com/brianfrankcooper/YCSB) | Apache-2.0 |
| `ycsb` | jemalloc | [jemalloc/jemalloc](https://github.com/jemalloc/jemalloc) | BSD-2-Clause |
| `ycsb`, `benchmarker_dbmsbenchmarker`, `tpch`, `tpch_refresh`, `tpcds` | `redis-cli` from `redis-stable` (synchronisation of pods) | [redis/redis](https://github.com/redis/redis) | Redis 8: RSALv2, SSPLv1 or AGPL-3.0, at the user's choice |
| `tpch`, `tpch_refresh` | TPC-H `dbgen` | [TPC](https://www.tpc.org/tpch/), supplied by the user | TPC EULA |
| `tpcds` | TPC-DS `dsdgen` | [TPC](https://www.tpc.org/tpcds/), supplied by the user | TPC EULA |
| `ssb` | SSB `dbgen` | [eyalroz/ssb-dbgen](https://github.com/eyalroz/ssb-dbgen), derived from TPC-H `dbgen` | No licence stated; TPC EULA included |
| loaders in `tpch`, `tpcds`, `ssb` | Client tools of the DBMS (e.g. `psql`, `mysql`, MySQL Shell, `clickhouse-client`, `mclient`, `sqlcmd`, `sqlplus`, `db2`, DuckDB CLI) | Base images and packages of the vendors | Licence of each vendor |
| `hardware` | fio | [axboe/fio](https://github.com/axboe/fio) | GPL-2.0 |
| `hardware` | sysbench | [akopytov/sysbench](https://github.com/akopytov/sysbench) | GPL-2.0 |
| `hardware` | netperf | [HewlettPackard/netperf](https://github.com/HewlettPackard/netperf) | MIT |
| `hardware` | sockperf | [Mellanox/sockperf](https://github.com/Mellanox/sockperf) | BSD-3-Clause |
| `monitoring` | Prometheus | [prometheus/prometheus](https://github.com/prometheus/prometheus) | Apache-2.0 |
| (manifest `k8s/daemonsettemplate-monitoring.yml`) | cAdvisor | [google/cadvisor](https://github.com/google/cadvisor) | Apache-2.0 |

### JDBC drivers in the images

| Driver | Source | Licence |
|---|---|---|
| PostgreSQL JDBC | [pgjdbc/pgjdbc](https://github.com/pgjdbc/pgjdbc) | BSD-2-Clause |
| YugabyteDB JDBC | [yugabyte/pgjdbc](https://github.com/yugabyte/pgjdbc) | BSD-2-Clause |
| MySQL Connector/J | [mysql/mysql-connector-j](https://github.com/mysql/mysql-connector-j) | GPL-2.0 with the Universal FOSS Exception |
| MariaDB Connector/J | [mariadb-corporation/mariadb-connector-j](https://github.com/mariadb-corporation/mariadb-connector-j) | LGPL-2.1 |
| MonetDB JDBC | [MonetDB/monetdb-java](https://github.com/MonetDB/monetdb-java) | MPL-2.0 |
| SingleStore JDBC | [memsql/S2-JDBC-Connector](https://github.com/memsql/S2-JDBC-Connector) | LGPL-2.1 |
| Kinetica JDBC | [kineticadb/kinetica-client-jdbc](https://github.com/kineticadb/kinetica-client-jdbc) | MIT |
| Microsoft JDBC Driver for SQL Server | [microsoft/mssql-jdbc](https://github.com/microsoft/mssql-jdbc) | MIT |
| ClickHouse JDBC | [ClickHouse/clickhouse-java](https://github.com/ClickHouse/clickhouse-java) | Apache-2.0 |
| Oracle JDBC (`ojdbc8`) | Maven Central | [Oracle Free Use Terms and Conditions](https://www.oracle.com/downloads/licenses/oracle-free-license.html): redistribution of the unmodified jar without charge, with a copy of the terms |

Drivers of IBM Db2 are not built into the images; they are downloaded when a container starts.

The loader images for SQL Server and Oracle install the vendors' client tools from their package repositories: `msodbcsql18` and `mssql-tools18` (Microsoft licence terms, accepted with `ACCEPT_EULA=Y`) and Oracle Instant Client.
Whether these terms allow publishing the images has not been checked yet.

## Not included: the DBMS under test

Bexhoma deploys DBMS from the images of their vendors (see the manifests in `k8s/`); none of them is part of Bexhoma.
Each DBMS is subject to the licence of its vendor.
Some licences restrict the publication of benchmark results: the Developer edition of SQL Server requires Microsoft's prior written approval.
Bexhoma keeps the results of SQL Server, Oracle Database Free, IBM Db2 Community Edition and CedarDB internal; the repository describes how to run them but contains no results (checked by `tests/test_unpublished_results.py`).

## Note on TPC

TPC-H, TPC-DS and TPC-C are trademarks of the Transaction Processing Performance Council (TPC).
The query texts and data generators used by Bexhoma are derived from the TPC specifications and kits; HammerDB and Benchbase implement workloads derived from TPC-C.
Results obtained with Bexhoma are not TPC benchmark results: they have not been audited, do not follow all rules of the specifications, and must not be compared with published TPC results.

## Python dependencies

The dependencies in [requirements.txt](requirements.txt) are installed by pip and not distributed with Bexhoma.
Their licences, as stated in the metadata of the installed versions:

| Package | Licence |
|---|---|
| dbmsbenchmarker | AGPL-3.0-or-later |
| HiYaPyCo | GPL-3.0-or-later |
| kubernetes, requests, pyarrow | Apache-2.0 |
| cryptography | Apache-2.0 or BSD-3-Clause |
| psutil, mistune, numpy, Werkzeug, prettytable, idna, ipython, seaborn | BSD-3-Clause (numpy, seaborn: BSD) |
| pyasn1 | BSD-2-Clause |
| urllib3, setuptools, fonttools, dash, zipp, myst_parser | MIT |
| pillow | MIT-CMU |
