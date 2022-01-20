# Example: TPC-H

This example shows how to benchmark 22 reading queries Q1-Q22 derived from TPC-H in MonetDB and PostgreSQL.

> The query file is derived from the TPC-H and as such is not comparable to published TPC-H results, as the query file results do not comply with the TPC-H Specification.

Official TPC-H benchmark - http://www.tpc.org/tpch

## Prerequisites

We need configuration file containing the following informations in a predefined format, c.f. [demo file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/k8s-cluster.config).
The demo also includes the necessary settings for some [DBMS](DBMS.html): MariaDB, MonetDB, MySQL, OmniSci and PostgreSQL.

We may adjust the configuration to match the actual environment.
This in particular holds for `imagePullSecrets`, `tolerations` and `nodeSelector` in the [YAML files](Deployments.html).

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

For performing the experiment we can run the [demo file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpch.py).

The actual configurations to benchmark are added by
```
config = configurations.default(experiment=experiment, docker='MonetDB', configuration='MonetDB-{}'.format(cluster_name), alias='DBMS A')
config = configurations.default(experiment=experiment, docker='PostgreSQL', configuration='PostgreSQL-{}'.format(cluster_name), alias='DBMS D')
```

### Adjust Parameter

You maybe want to adjust some of the parameters that are set in the file.

The hardware requirements are set via
```
# pick hardware
cpu = str(args.request_cpu)
memory = str(args.request_ram)
cpu_type = str(args.request_cpu_type)
```

## Evaluate Results in Dashboard

Evaluation is done using DBMSBenchmarker: https://github.com/Beuth-Erdelt/DBMS-Benchmarker/blob/master/docs/Dashboard.html

