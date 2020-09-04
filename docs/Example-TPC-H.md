# Example: TPC-H

This example shows how to benchmark 22 reading queries Q1-Q22 derived from TPC-H in MonetDB and PostgreSQL.

> The query file is derived from the TPC-H and as such is not comparable to published TPC-H results, as the query file results do not comply with the TPC-H Specification.

Official TPC-H benchmark - http://www.tpc.org/tpch

**Content**:
* [Prerequisites](#prerequisites)
* [Perform Benchmark](#perform-benchmark)
* [Evaluate Results in Dashboard](#evaluate-results-in-dashboard)

## Prerequisites

We need configuration file containing the following informations in a predefined format, c.f. [demo file](../k8s-cluster.config).
We may adjust the configuration to match the actual environment.
This in particular holds for `imagePullSecrets`, `tolerations` and `nodeSelector` in the YAML files.

The demo also includes the necessary settings for some DBMS: MariaDB, MonetDB, MySQL, OmniSci and PostgreSQL.

For basic execution of benchmarking we need
* a Kubernetes (K8s) cluster
  * a namespace `mynamespace`
  * `kubectl` usable, i.e. access token stored in a default vault like `~/.kube`
  * a persistent volume named `vol-benchmarking` containing the raw TPC-H data in `/data/tpch/SF1/`
* JDBC driver `./monetdb-jdbc-2.29.jar` and `./postgresql-42.2.5.jar`
* a folder `/benchmarks` for the results


For also enabling monitoring we need
* a monitoring instance Prometheus / Grafana that scrapes metrics from `localhost:9300`
* an access token and URL for asking Grafana for metrics  
  https://grafana.com/docs/grafana/latest/http_api/auth/#create-api-token


## Perform Benchmark

For performing the experiment we can run the [demo file](../demo-tpch-k8s.py).

The actual benchmarking is done by
```
# run experiments
run_experiments(docker='MonetDB', alias='DBMS-A')
run_experiments(docker='PostgreSQL', alias='DBMS-B')
```

### Adjust Parameter

You maybe want to adjust some of the parameters that are set in the file.

The hardware requirements are set via
```
# pick hardware
cpu = "4000m"
memory = '16Gi'
cpu_type = 'epyc-7542'
```

The number of executions of each query can be adjusted here
```
# set query parameters - this overwrites infos given in the query file
cluster.set_querymanagement(numRun = 1)
```

### Evaluate Results in Dashboard

Evaluation is done using DBMSBenchmarker: https://github.com/Beuth-Erdelt/DBMS-Benchmarker/blob/master/docs/Dashboard.md

