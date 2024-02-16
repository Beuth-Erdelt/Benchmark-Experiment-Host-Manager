# Configurations

We need
* a [config file](#clusterconfig) containing cluster information , say `cluster.config`
* a [config folder](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch), say `experiments/tpch/`, containing
  * a [config file](https://dbmsbenchmarker.readthedocs.io/en/latest/Options.html) `queries.config` for the workload
  * folders for DDL scripts (per DBMS)
* a python script managing the experimental workflow, say `tpch.py`, see [example](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpch.py)

To use the predefined examples you will only have to change the context and namespace of the Kubernetes cluster - see below.

## Cluster-Config

The configuration of the cluster, that is the possible host and experiment settings, consists of these parts (see also [example](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s-cluster.config) config file):


### Config of the Benchmark tool

You probably can leave this as is.

```
'benchmarker': {
    'resultfolder': './',                               # Local path to results folder of benchmark tool
    'jarfolder': './jars/'                              # Optional: Local path to JDBC drivers
},
```

* `resultfolder`: Where the benchmarker puts it's result folders
* `jarfolder`: Where the benchmarker expects the JDBC jar files

Both folders are used to correspond with the Docker containers of the benchmarker and must match the settings inside of the image.


### Credentials of the Cluster

You will have to adjust the name of the namespace `my_namespace`.
The rest probably can stay as is.

```
'credentials': {
    'k8s': {
        'appname': 'bexhoma',
        'context': {
            'my_context': {
                'namespace': 'my_namespace',
                'clustername': 'BHT',
                'service_sut': '{service}.{namespace}.svc.cluster.local',
                'port': 9091, # K8s: Local port for connecting via JDBC after port forwarding
            },
```
* `my_context`: Context (name) of the cluster. Repeat this section for every K8s cluster you want to use. This also allows to useand compare several Clouds.
* `my_namespace`: Namespace in the cluster.


## (Hardware) Monitoring

It follows a dict of hardware metrics that should be collected per DBMS.
This probably can stay as is.
The attributes are set by bexhoms automatically so that corresponding pods can be identified.
The host is found using the service of the DBMS.
See [monitoring section](https://bexhoma.readthedocs.io/en/latest/Monitoring.html) for more details.

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

The data itself is expected to be stored in a shared disk, that will be mounted into the DBMS container as `/data/`.
The examples scripts above (like `initdata-tpch-SF1.sql` for example) refer to `/data/tpch/SF1/` for example.
