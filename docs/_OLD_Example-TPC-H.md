# Example: TPC-H

This example shows how to benchmark 22 reading queries Q1-Q22 derived from TPC-H in MonetDB and PostgreSQL.

> The query file is derived from the TPC-H and as such is not comparable to published TPC-H results, as the query file results do not comply with the TPC-H Specification.

Official TPC-H benchmark - http://www.tpc.org/tpch

## Prerequisites

For basic execution of benchmarking we need  
* a Kubernetes (K8s) cluster
  * a namespace `my_namespace` in the cluster
  * `kubectl` usable, i.e. access token stored in a default vault like `~/.kube`
  * a persistent volume named `vol-benchmarking` containing the raw TPC-H data in `/data/tpch/SF1/`
* JDBC driver `./monetdb-jdbc-2.29.jar` and `./postgresql-42.2.5.jar`

We need configuration files containing the following informations in a predefined format, c.f. [demo file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/k8s-cluster.config).
The demo also includes the necessary settings for some [DBMS](DBMS.html): MariaDB, MonetDB, MySQL, OmniSci and PostgreSQL.

We may adjust the configuration to match the actual environment.
This in particular holds for `imagePullSecrets`, `tolerations` and `nodeSelector` in the [YAML files](Deployments.html).



For also enabling monitoring we need
* a monitoring instance Prometheus / Grafana that scrapes metrics from `localhost:9300`
* an access token and URL for asking Grafana for metrics  
  https://grafana.com/docs/grafana/latest/http_api/auth/#create-api-token


## Perform Benchmark

For performing the experiment we can run the [tpch file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpch.py).

The actual configurations to benchmark are added by
```
config = configurations.default(experiment=experiment, docker='MonetDB', configuration='MonetDB-{}'.format(cluster_name), alias='DBMS 1')
config = configurations.default(experiment=experiment, docker='PostgreSQL', configuration='PostgreSQL-{}'.format(cluster_name), alias='DBMS 2')
```

### Adjust Parameter

You maybe want to adjust some of the parameters that are set in the file: `python tpch.py -h`

```
usage: tpch.py [-h] [-db] [-c CONNECTION] [-cx CONTEXT] [-e EXPERIMENT] [-d] [-m] [-ms MAX_SUT] [-dt]
               [-md MONITORING_DELAY] [-nr NUM_RUN] [-nc NUM_CONFIG] [-ne NUM_QUERY_EXECUTORS] [-sf SCALING_FACTOR]
               [-t TIMEOUT] [-rr REQUEST_RAM] [-rc REQUEST_CPU] [-rct REQUEST_CPU_TYPE] [-rg REQUEST_GPU]
               [-rgt REQUEST_GPU_TYPE] [-rst {None,,local-hdd,shared}] [-rss REQUEST_STORAGE_SIZE]
               [-rnn REQUEST_NODE_NAME]
               {profiling,run,start,load}

Perform TPC-H inspired benchmarks in a Kubernetes cluster. This either profiles the imported data in several DBMS and
compares some statistics, or runs the TPC-H queries. Optionally monitoring is actived. User can choose to detach the
componenten of the benchmarking system, so that as much as possible is run inside a Kubernetes (K8s) cluster. User can
also choose some parameters like number of runs per query and configuration and request some resources.

positional arguments:
  {profiling,run,start,load}
                        profile the import of TPC-H data, or run the TPC-H queries, or start DBMS and load data, or
                        just start the DBMS

optional arguments:
  -h, --help            show this help message and exit
  -db, --debug          dump debug informations
  -c CONNECTION, --connection CONNECTION
                        name of DBMS
  -cx CONTEXT, --context CONTEXT
                        context of Kubernetes (for a multi cluster environment), default is current context
  -e EXPERIMENT, --experiment EXPERIMENT
                        sets experiment code for continuing started experiment
  -d, --detached        puts most of the experiment workflow inside the cluster
  -m, --monitoring      activates monitoring
  -ms MAX_SUT, --max-sut MAX_SUT
                        maximum number of parallel DBMS configurations, default is no limit
  -dt, --datatransfer   activates datatransfer
  -md MONITORING_DELAY, --monitoring-delay MONITORING_DELAY
                        time to wait [s] before execution of the runs of a query
  -nr NUM_RUN, --num-run NUM_RUN
                        number of runs per query
  -nc NUM_CONFIG, --num-config NUM_CONFIG
                        number of runs per configuration
  -ne NUM_QUERY_EXECUTORS, --num-query-executors NUM_QUERY_EXECUTORS
                        comma separated list of number of parallel clients
  -sf SCALING_FACTOR, --scaling-factor SCALING_FACTOR
                        scaling factor (SF)
  -t TIMEOUT, --timeout TIMEOUT
                        timeout for a run of a query
  -rr REQUEST_RAM, --request-ram REQUEST_RAM
                        request ram
  -rc REQUEST_CPU, --request-cpu REQUEST_CPU
                        request cpus
  -rct REQUEST_CPU_TYPE, --request-cpu-type REQUEST_CPU_TYPE
                        request node having node label cpu=
  -rg REQUEST_GPU, --request-gpu REQUEST_GPU
                        request number of gpus
  -rgt REQUEST_GPU_TYPE, --request-gpu-type REQUEST_GPU_TYPE
                        request node having node label gpu=
  -rst {None,,local-hdd,shared}, --request-storage-type {None,,local-hdd,shared}
                        request persistent storage of certain type
  -rss REQUEST_STORAGE_SIZE, --request-storage-size REQUEST_STORAGE_SIZE
                        request persistent storage of certain size
  -rnn REQUEST_NODE_NAME, --request-node-name REQUEST_NODE_NAME
                        request a specific node
```

The hardware requirements are set via
```
# pick hardware
cpu = str(args.request_cpu)
memory = str(args.request_ram)
cpu_type = str(args.request_cpu_type)
```

## Evaluate Results in Dashboard

Evaluation is done using DBMSBenchmarker: https://github.com/Beuth-Erdelt/DBMS-Benchmarker/blob/master/docs/Dashboard.html

