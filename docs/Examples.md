# Basic examples

## Files

This repository includes some basic examples as files:
* `template-cluster.config`: Demo of cluster configuration file
* `experiments/example/`: Demo of benchmark configuration files
  * `connection.config`: Empty list of (already processed) DBMS
  * `queries.config`: Configuration of queries of the experiment
  * `OmniSci/initschema.sql`: File of DDL commands of experiment
  * `OmniSci/initdata.sql`: File of ingestion commands of experiment
* `k8s/deploymenttemplate-PostgreSQL.yml`: Demo of DBMS deployment for k8s
* `experiment-example-AWS.py`: Demo of experiment workflow in AWS environment
* `experiment-example-k8s.py`: Demo of experiment workflow in k8s environment

We will explain this structure in the following.

## How to address a cluster

* Load cluster config
* Set config for benchmarks
* For k8s: Set config for deployments

On **k8s**:

```
cluster = clusters.testbed(clusterconfig='cluster.config', experiments_configfolder='experiments/tpch', yamlfolder='k8s/')
```

On **AWS**:

```
cluster = masterAWS.testbed(clusterconfig='cluster.config', experiments_configfolder='experiments/tpch')
```

## Example: TPC-H Benchmark for 3 DBMS on 1 Virtual Machine

For running *TPC-H benchmarks of an OmniSci, a MariaDB and a PostgreSQL installation on an AWS instance*, we suggest the following folder structure:
```
./cluster.config
./experiments/tpch/queries.config
./experiments/tpch/MariaDB/initschema.sql
./experiments/tpch/MariaDB/initdata.sql
./experiments/tpch/OmniSci/initschema.sql
./experiments/tpch/OmniSci/initdata.sql
./experiments/tpch/PostgreSQL/initschema.sql
./experiments/tpch/PostgreSQL/initdata.sql
./experiment-tpch.py
```

This means we provide
* a [config file](#clusterconfig) containing cluster information, say `cluster.config`
* a [config folder](https://github.com/Beuth-Erdelt/GEO-GPU-DBMS-Benchmarks#config-folder) for the benchmark tool, say `experiments/tpch/`, containing a config file `queries.config` for TPC-H [queries](https://github.com/Beuth-Erdelt/DBMS-Benchmarker#query-file) and schema and ingestion commands per DBMS
* a python script managing the experiment workflow, say `experiment-tpch.py`

### The Manager

`experiment-tpch.py` may contain
* Set data volume to `tpch`
* Set installation script to `1shard-SF1`
* Set instance to `1xK80`
* Run experiment on 3 different docker images

```
# set config
cluster = masterAWS.testbed(clusterconfig='cluster.config', experiments_configfolder='experiments/tpch')

cluster.setExperiment(volume='tpch', script='1shard-SF1', instance='1xK80')
cluster.runExperiment(docker='OmniSci')
cluster.runExperiment(docker='MariaDB')
cluster.runExperiment(docker='MemSQL')
```

This is an abbreviation of

```
cluster.runExperiment(volume='tpch', docker='OmniSci', script='1shard-SF1', instance='1xK80')
cluster.runExperiment(volume='tpch', docker='MariaDB', script='1shard-SF1', instance='1xK80')
cluster.runExperiment(volume='tpch', docker='MemSQL', script='1shard-SF1', instance='1xK80')
```

If we do not want to restart the instance:

```
cluster = masterAWS.testbed(clusterconfig='cluster.config', experiments_configfolder='experiments/tpch')

cluster.setExperiment(volume='tpch', script='1shard-SF1', instance='1xK80')
cluster.prepareExperiment()
cluster.startExperiment(docker='OmniSci')
cluster.runBenchmarks()
cluster.stopExperiment()
cluster.startExperiment(docker='MariaDB')
cluster.runBenchmarks()
cluster.stopExperiment()
cluster.startExperiment(docker='MemSQL')
cluster.runBenchmarks()
cluster.stopExperiment()
cluster.cleanExperiment()
```

## Example: TPC-H Benchmark for 1 DBMS on 3 Virtual Machines

For running *TPC-H benchmarks of an OmniSci installation on three AWS instances*, we suggest the following folder structure:
```
./cluster.config
./experiments/tpch/queries.config
./experiments/tpch/OmniSci/initschema.sql
./experiments/tpch/OmniSci/initdata.sql
./experiment-tpch.py
```

This means we provide
* a [config file](#clusterconfig) containing cluster information, say `cluster.config`
* a [config folder](https://github.com/Beuth-Erdelt/GEO-GPU-DBMS-Benchmarks#config-folder) for the benchmark tool, say `experiments/tpch/`, containing a config file `queries.config` for TPC-H [queries](https://github.com/Beuth-Erdelt/DBMS-Benchmarker#query-file) and schema and ingestion files for the DBMS
* a python script managing the experiment workflow, say `experiment-tpch.py`

### The Manager

`experiment-tpch.py` may contain
* Set data volume to `tpch`
* Set docker image to `OmniSci`
* Set installation script to `1shard-SF1`
* Run experiment on 3 different instances

```
cluster = masterAWS.testbed(clusterconfig='cluster.config', experiments_configfolder='experiments/tpch')

cluster.setExperiment(volume='tpch', docker='OmniSci', script='1shard-SF1')
cluster.runExperiment(instance='1xK80')
cluster.runExperiment(instance='4xK80')
cluster.runExperiment(instance='8xK80')
```

This is an abbreviation of

```
cluster.runExperiment(volume='tpch', docker='OmniSci', script='1shard-SF1', instance='1xK80')
cluster.runExperiment(volume='tpch', docker='OmniSci', script='1shard-SF1', instance='4xK80')
cluster.runExperiment(volume='tpch', docker='OmniSci', script='1shard-SF1', instance='8xK80')
```


