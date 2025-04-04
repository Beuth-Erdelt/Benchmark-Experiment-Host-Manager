# Cluster-Config

The configuration of the cluster, that is the possible host and experiment settings, is set in a file `cluster.config` and consists of these parts (see also [example](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s-cluster.config) config file):


## Basic settings

```
'benchmarker': {
    'resultfolder': './',                               # Local path to results folder of benchmark tool
    'jarfolder': './jars/'                              # Optional: Local path to JDBC drivers
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
                'port': 9091, # K8s: Local port for connecting via JDBC after port forwarding
            },
```
* `my_context`: Context (name) of the cluster. Repeat this section for every K8s cluster you want to use. This also allows to use and compare several clouds.
* `my_namespace`: Namespace in the cluster. Make sure you have access to that namespace.
* `clustername`: Customize the cluster name for your convenience.


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

Example: For TPC-H the script `tpch.py` may run (depending on the CLI parameters)
* `Schema` before ingestion - this runs the script `initschema-tpch.sql`
* `Index_and_Constraints` after ingestion - this runs the script `initindexes-tpch.sql` and `initconstraints-tpch.sql`

The data itself is expected to be stored in a shared disk, that will be mounted into the DBMS container as `/data/`.
The examples scripts above (like `initdata-tpch-SF1.sql` for example) refer to `/data/tpch/SF1/` for example.

## DBMS

Database systems are described in the `docker` section.
Please see [DBMS section](https://bexhoma.readthedocs.io/en/latest/DBMS.html) for more informations.


