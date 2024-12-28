---
title: 'Bexhoma: Cloud-native Benchmarking of DBMS at Kubernetes'
tags:
  - Python
  - DBMS
  - Kubernetes
  - Docker
  - Cloud-native
  - Microservices
authors:
  - name: Patrick K. Erdelt
    orcid: 0000-0002-3359-2386
    corresponding: true
    affiliation: 1
affiliations:
 - name: Berliner Hochschule für Technik (BHT)
   index: 1
date: 05 November 2022
bibliography: paper.bib

---

# Summary

Bexhoma (Benchmark Experiment Host Manager) is a Python tool that helps with managing benchmark experiments of Database Management Systems (DBMS) in a Kubernetes-based High-Performance-Computing (HPC) cluster environment. It enables users to configure hardware / software setups for easily repeating tests over varying configurations.

The basic workflow is [@10.1007/978-3-030-84924-5_6;@10.1007/978-3-030-94437-7_6]: start a containerized version of the DBMS, install monitoring software, import data, run benchmarks and shut down everything with a single command. A more advanced workflow is: Plan a sequence of such experiments, run plan as a batch and join results for comparison. It is possible to scale-out drivers for generating and loading data and for benchmarking to simulate cloud-native environments. Benchmarks included are YCSB, TPC-H, TPC-DS and TPC-C (HammerDB and Benchbase version).

![workflow in bexhoma.\label{fig:workflow}](docs/workflow-sketch-simple.png){ width=1440}

Bexhoma serves as the orchestrator [@10.1007/978-3-030-94437-7_6] for distributed parallel benchmarking experiments in a Kubernetes Cloud. It starts a monitoring container of Prometheus and metrics collector containers of cAdvisor.
For analytical use cases, the Python package dbmsbenchmarker, [@Erdelt2022DBMSBenchmarker], is used as query executor and evaluator as in [@10.1007/978-3-030-84924-5_6;@10.1007/978-3-030-94437-7_6]. For transactional use cases, HammerDB's TPC-C, Benchbase's TPC-C and YCSB are used as drivers for generating and loading data and for running the workload as in [@10.1007/978-3-031-68031-1_9].

Bexhoma has been tested at Amazon Web Services, Google Cloud, Microsoft Azure, IBM Cloud, Oracle Cloud, and at Minikube installations, running with Clickhouse, Exasol, Citus Data (Hyperscale), IBM DB2, MariaDB, MariaDB Columnstore, MemSQL (SingleStore), MonetDB, MySQL, OmniSci (HEAVY.AI), Oracle DB, PostgreSQL, SQL Server, SAP HANA, TimescaleDB, and Vertica.

See the [homepage](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager) and the [documentation](https://bexhoma.readthedocs.io/en/latest/) for more details.

# Statement of Need

The first purpose of Bexhoma responds to the need for a framework to support all aspects of a benchmarking experiment.
In [@10.1007/978-3-319-67162-8_12] the authors present a cloud-centric analysis of eight evaluation frameworks.
In [@10.1007/978-3-030-12079-5_4] the authors inspect several frameworks and collect requirements for a DBMS benchmarking framework in an interview based method and per interest group.
In [@10.1007/978-3-319-15350-6_6] the authors list important components for benchmarking, like Benchmark Coordinator, Measurement Manager, Workload Executor. They plead for a benchmarking middleware to support the process, to "*take care of the hassle of distributed benchmarking and managing the measurement infrastructure*". This is supposed to help the benchmark designer to concentrate on the core competences: specifying workload profiles and analyzing obtained measurements. In [@10.1007/978-3-030-84924-5_6] we introduce the package based on the following extracted requirements:

* Help with time-consuming initial setup and configuration
* Metadata collection / Track everything
* Generality / Versatility
* Extensibility / Abstraction
* Usability / Configurability
* Repeatability / Reproducibility

The second purpose of Bexhoma targets the specific situation of cloud-native benchmarking.

## Similar approaches

Theodolite [@HENNING2021100209] for benchmarking stream processing engines.
Mowgli [@10.1145/3297663.3310303] aims at establishing Benchmarking-as-a-service.
Frisbee [@nikolaidis2021frisbeeautomatedtestingcloudnative] for declarative end-to-end system testing of containerized application.
KOBE [@10.1007/978-3-030-77385-4_40] for benchmarking federated query processors.


## Summary of Solution

Key concepts are

* Virtualization with Docker containers
* Orchestration with Kubernetes
* Monitoring with cAdvisor / Prometheus

This is implemented as [@10.1007/978-3-030-84924-5_6;@10.1007/978-3-030-94437-7_6;@10.1007/978-3-031-68031-1_9]

* **SUT (DBMS)**: *deployment*, container `dbms`, container for cAdvisor for sidecar monitoring, *pvc* for persistent storage, *service* for connection, port 9091
* **Multi-host DBMS**: *statefulset* for worker, *job* for initialization
* **Monitoring**: *deployment* of Prometheus
* **Metrics collectors**: either sidecar of single-host DBMS or *daemonset* for all nodes of cluster.
* **Loader (schema and index creation)**: fire-and-forget thread in the orchestrator
* **Ingestion**: *job* of pods for data generation and for ingestion of data into the DBMS, synchronized using a Redis queue
* **Benchmarking**: *job* of pods for running the driver, synchronized using a Redis queue


![components of bexhoma.\label{fig:components}](docs/Experiment-Setup-Microservices.png){ width=1440}


# Installation

1. Download the repository: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager
1. Install the package `pip install bexhoma`
1. Make sure you have a working `kubectl` installed.
    * (Also make sure to have access to a running Kubernetes cluster - for example [Minikube](https://minikube.sigs.k8s.io/docs/start/))
    * (Also make sure, you can create PV via PVC and dynamic provisioning)
1. Adjust [configuration](https://bexhoma.readthedocs.io/en/latest/Config.html)
    1. Copy `k8s-cluster.config` to `cluster.config`
    1. Set name of context, namespace and name of cluster in that file
    2. Make sure the `resultfolder` is set to a folder that exists on your local filesystem
1. Other components like the shared data and result directories, the message queue and the evaluator are installed automatically when you start an experiment. Before that, you might want to adjust  
    * Result directory: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/pvc-bexhoma-results.yml  
      * `storageClassName`: must be an available storage class of type `ReadWriteMany` in your cluster
      * `storage`: size of the directory
    * Data directory: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/pvc-bexhoma-data.yml  
      * `storageClassName`: must be an available storage class of type `ReadWriteMany` in your cluster
      * `storage`: size of the directory

Bexhoma is now ready to use.


# A Basic Example

The [documentation](https://bexhoma.readthedocs.io/en/latest/) contains a lot of examples.
We here show some basic examples for basic use cases.

## HammerDB's TPC-C at PostgreSQL

```
python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms PostgreSQL \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 16 \
  run
```

This

* starts a clean instance of PostgreSQL (`-dbms`)
  * data directory inside a Docker container
* starts 1 loader pod (per DBMS) that
  * creates TPC-C schema in the database
  * imports data for 16 (`-sf`) warehouses into the DBMS
  * using 16 (`-nlt`) threads
* runs streams of TPC-C queries (per DBMS)
    * running for 5 (`-sd`) minutes
    * each stream having 16 threads to simulate 16 users (`-nbt`)
    * `-nbp`: first stream 1 pods, second stream 2 pods (8 threads each)
* with a maximum of 1 DBMS per time (`-ms`)
* tests if results match workflow (`-tr`)
* shows a summary

### Experiment Status

You can watch the status while benchmark is running via `bexperiments status`

```
Dashboard: Running
Cluster Prometheus: Running
Message Queue: Running
Data directory: Running
Result directory: Running
+---------------------+--------------+------------+---------------+-------------+
| 1726578005          | sut          | loaded [s] | use case      | loading     |
+=====================+==============+============+===============+=============+
| PostgreSQL-BHT-16-1 | (1. Running) |          1 | hammerdb_tpcc | (1 Running) |
+---------------------+--------------+------------+---------------+-------------+
```

The code `1726578005` is the unique identifier of the experiment.
You can find the number also in the output of `hammerdb.py`.

### Experiment Results

At the end of a benchmark you will see a summary like

```
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 1205s 
    Code: 1726578005
    This includes no queries. HammerDB runs the benchmark
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes.
    Benchmark is limited to DBMS PostgreSQL.
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [16] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-BHT-16-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:252347764
    datadisk:3377044
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-16-1-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:253279924
    datadisk:4309204
    requests_cpu:4
    requests_memory:16Gi

### Execution
                       experiment_run  vusers  client  pod_count     NOPM      TPM  duration  errors
PostgreSQL-BHT-16-1-1               1      16       1          1  12247.0  37509.0         5       0
PostgreSQL-BHT-16-1-2               1      16       2          2  10391.0  31969.5         5       0

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-BHT-16-1 - Pods [[1, 2]]

#### Planned
DBMS PostgreSQL-BHT-16-1 - Pods [[1, 2]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-16-1-1       84.0        1.0   1.0                 685.714286
PostgreSQL-BHT-16-1-2       84.0        1.0   2.0                 685.714286

### Tests
TEST passed: NOPM contains no 0 or NaN
TEST passed: Workflow as planned
```

We can see that scaled-out drivers (2 pods with 8 threads each) have similar results as a monolithic driver (1 pod with 16 threads) - but are a bit weaker.

To see the summary again you can simply call `bexperiments summary -e 1726578005` with the experiment code.


# Configuration

Here we provide more background information on the configuration and files included in bexhoma. In most cases the default settings will be sufficient.

## Cluster-Config

The configuration of the cluster, that is the possible host and experiment settings, is set in a file `cluster.config` and consists of these parts (see also [example](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s-cluster.config) config file):


## Basic settings

```
'benchmarker': {
    'resultfolder': './',
    'jarfolder': './jars/'
},
```

* `resultfolder`: Where the benchmarker puts it's result folders. Make sure this is an existing folder bexhoma can write to.
* `jarfolder`: Where the benchmarker expects the JDBC jar files. You probably should leave this as is.

## Credentials of the Cluster

You will have to adjust the name of the namespace `my_namespace`.
The rest probably can stay as is.

```
'credentials': {
    'k8s': {
        'appname': 'bexhoma',
        'context': {
            'my_context': {
                'namespace': 'my_namespace',
                'clustername': 'My Cluster',
                'service_sut': '{service}.{namespace}.svc.cluster.local',
                'port': 9091,
            },
```

* `my_context`: Context (name) of the cluster. Repeat this section for every K8s cluster you want to use. This also allows to use and compare several clouds.
* `my_namespace`: Namespace in the cluster. Make sure you have access to that namespace.
* `clustername`: Customize the cluster name for your convenience.


## (Hardware) Monitoring

Monitoring refers to automatical observation of resource consumption of components.

It follows a dict of hardware metrics that should be collected per DBMS.
This probably can stay as is.
The attributes are set by bexhoms automatically so that corresponding pods can be identified.
The host is found using the service of the DBMS.
Bexhoma basically offers two variants

* Monitor only the system-under-test (SUT) with `-m`
* Monitor all components with `-mc`

Moreover bexhoma expects the cluster to be prepared, i.e. a daemonset of cAdvisors (exporters) is running and there is a Prometheus server (collector) we can connect to.
However bexhoma can optionally install these components if missing.

If there is a Prometheus server running in your cluster, make sure to adjust `service_monitoring`.
If there is no Prometheus server running in your cluster, make sure to leave the template in `service_monitoring` as is.
Bexhoma checks at the beginning of an experiment if the URL provided is reachable;
it uses cURL inside the dashboard pod to test if `query_range?query=sum(node_memory_MemTotal_bytes)&start={start}&end={end}&step=60` has a return status of 200 (where `start` is 5 min ago and `end` is 4 min ago).

If there is no preinstalled Prometheus in the cluster, bexhoma will in case of

* Monitor only the system-under-test (SUT) with `-m`
  * install a cAdvisor sidecar container per SUT
  * install a Prometheus server per experiment
* Monitor all components with `-mc`
  * install a cAdvisor per node as a daemonset
  * install a Prometheus server per experiment

Bexhoma will also make sure all components know of eachother.

For example metrics, c.f. [config file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s-cluster.config).

Note that the metrics make a summation over all matching components (containers, CPU cores etc).

### Installation Templates

cAdvisor runs as a container `cadvisor` and a service with `port-monitoring` 9300

* example per SUT (sidecar container): `k8s/deploymenttemplate-PostgreSQL.yml`
* example per node (daemonset): `k8s/daemonsettemplate-monitoring.yml`

Prometheus runs as a container with a service with `port-prometheus` 9090

* `k8s/deploymenttemplate-bexhoma-prometheus.yml`

## Data Sources

Data sources and imports can be adressed using a key.
This probably can stay as is.
It is organized as follows:

```
'volumes': {
    'tpch': {
        'initscripts': {
            'Schema': [
                'initschema-tpch.sql',
            ],
            'Schema_dummy': [
                'initschemadummy-tpch.sql',
            ],
            'Index': [
                'initindexes-tpch.sql',
            ],
            'Index_and_Constraints': [
                'initindexes-tpch.sql',
                'initconstraints-tpch.sql',
            ],
            'Index_and_Constraints_and_Statistics': [
                'initindexes-tpch.sql',
                'initconstraints-tpch.sql',
                'initstatistics-tpch.sql',
            ],
            'SF1': [
                'initschema-tpch.sql',
                'initdata-tpch-SF1.sql',
                'initdata-tpch-SF1.sh'
            ],
        }
    }
},
```

* `tpch`: Name of the data source (addressed by the corresponding experiments)
* `initscripts`: Dict of scripts to prepare the database, ingest data, create indexes etc.  
  It consists of  
  * a name, for example `Index_and_Constraints`,
  * a list of script names.  
  The scripts `.sql` are sent to the command line tool of the DBMS (`loadData` parameter in the DBMS configuration) and the files `.sh` are executed as shell scripts.
The scripts must be present in a [config folder](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch), say `experiments/tpch/`.

Example: For TPC-H the script `tpch.py` may run (depending on the CLI parameters)

* `Schema` before ingestion - this runs the script `initschema-tpch.sql`
* `Index_and_Constraints` after ingestion - this runs the script `initindexes-tpch.sql` and `initconstraints-tpch.sql`

The data itself is expected to be stored in a shared disk, that will be mounted into the DBMS container as `/data/`.
The examples scripts above (like `initdata-tpch-SF1.sql` for example) refer to `/data/tpch/SF1/` for example.

## DBMS

Database systems are described in the `docker` section.
Please see [DBMS section](https://bexhoma.readthedocs.io/en/latest/DBMS.html) for more informations.

To include a DBMS in a Kubernetes-based experiment you will need

* a Docker Image
* a JDBC Driver
* a Kubernetes Deployment Template
* some configuration
  * How to load data (DDL command)
  * DDL scripts
  * How to connect via JDBC

DBMS can be adressed using a key.
We have to define some data per key, for example for the key `PostgreSQL` we use:

```
'PostgreSQL': {
    'loadData': 'psql -U postgres < {scriptname}',
    'delay_prepare': 60,
    'template': {
        'version': 'v11.4',
        'alias': 'General-B',
        'docker_alias': 'GP-B',
         'JDBC': {
            'driver': "org.postgresql.Driver",
            'auth': ["postgres", ""],
            'url': 'jdbc:postgresql://{serverip}:9091/postgres?reWriteBatchedInserts=true',
            'jar': 'postgresql-42.5.0.jar'
        }
    },
    'logfile': '/usr/local/data/logfile',
    'datadir': '/var/lib/postgresql/data/',
    'priceperhourdollar': 0.0,
},
```
This has

* a base name for the DBMS
* a `delay_prepare` in seconds to wait before system is considered ready
* a placeholder `template` for the [benchmark tool DBMSBenchmarker](https://dbmsbenchmarker.readthedocs.io/en/latest/Options.html#connection-file)  
  Some of the data in the reference, like `hostsystem`, will be added by bexhoma automatically.
* assumed to have the JDBC driver jar locally available inside the benchmarking tool
* a command `loadData` for running the init scripts  
  Some placeholders in the URL are: `serverip` (set automatically to match the corresponding pod), `dbname`, `DBNAME`, `timout_s`, `timeout_ms` (name of the database in lower and upper case, timeout in seconds and miliseconds)
* `{serverip}` as a placeholder for the host address
* `{dbname}` as a placeholder for the db name
* an optional `priceperhourdollar` (currently ignored)
* an optional name of a `logfile` that is downloaded after the benchmark
* name of the `datadir` of the DBMS. It's size is measured using `du` after data loading has been finished.

### Deployment Manifests

Every DBMS that is deployed by bexhoma needs a YAML manifest.
See for example the [PostgreSQL manifest](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-PostgreSQL.yml).

You may want to pay attention to name of the secret:
```
      imagePullSecrets:
      - {name: dockerhub}
```
Another section that might be interesting is
```
      tolerations:
```


# Acknowledgements


# References
