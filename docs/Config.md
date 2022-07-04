# How to configure an experiment setup

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
        'appname': 'bexhoma',                           # K8s: To find corresponding deployments etc
        'context': {
            'my_context': {                             # K8s: Name of context of cluster
                'namespace': 'my_namespace',            # K8s: Namespace of User
                'clustername': 'my_cluster',            # K8s: Name of Cluster (just for annotation)
                'service_sut': '{service}.{namespace}.svc.cluster.local',
                'port': 9091,                           # K8s: Local port for connecting via JDBC after port forwarding
            },
        },
```
* `my_context`: Context (name) of the cluster. Repeat this section for every K8s cluster you want to use. This also allows to useand compare several Clouds.
* `namespace`: Namespace in the cluster.
* `port`: Arbitrary (free) local port that is used to ping running DBMS.


### (Hardware) Monitoring

This defines where to scrape the Prometheus metrics and is defined per context (cluster).
The services and the monitoring pods can be installed automatically by bexhoma.

```
        'monitor': {
            'service_monitoring': 'http://{service}.{namespace}.svc.cluster.local:9090/api/v1/',
            'extend': 20,
            'shift': 0,
```

* `extend`: Number of seconds the scraping interval should be extended (at both ends).
* `shift`: Number of seconds the scraping interval should be shifted (into future).


#### (Hardware) Metrics

It follows a dict of hardware metrics that should be collected per DBMS.
The attributes are set by bexhoms automatically so that corresponding pods can be identified.
The host is found using the service of the DBMS.

```
    'metrics': {
        'total_cpu_memory': {
            'query': 'container_memory_working_set_bytes{{job="monitor-node", container_label_io_kubernetes_container_name="dbms"}}/1024/1024',
            'title': 'CPU Memory [MiB]'
        },
        'total_cpu_memory_cached': {
            'query': 'container_memory_usage_bytes{{job="monitor-node", container_label_io_kubernetes_container_name="dbms"}}/1024/1024',
            'title': 'CPU Memory Cached [MiB]'
        },
        'total_cpu_util': {
            'query': 'sum(irate(container_cpu_usage_seconds_total{{job="monitor-node", container_label_io_kubernetes_container_name="dbms"}}[1m]))',
            'title': 'CPU Util [%]'
        },
        'total_cpu_throttled': {
            'query': 'sum(irate(container_cpu_cfs_throttled_seconds_total{{job="monitor-node", container_label_io_kubernetes_container_name="dbms"}}[1m]))',
            'title': 'CPU Throttle [%]'
        },
        'total_cpu_util_others': {
            'query': 'sum(irate(container_cpu_usage_seconds_total{{job="monitor-node", container_label_io_kubernetes_container_name!="dbms",id!="/"}}[1m]))',
            'title': 'CPU Util Others [%]'
        },
        'total_cpu_util_s': {
            'query': 'sum(container_cpu_usage_seconds_total{{job="monitor-node", container_label_io_kubernetes_container_name="dbms"}})',
            'title': 'CPU Util [s]'
        },
        'total_cpu_util_user_s': {
            'query': 'sum(container_cpu_user_seconds_total{{job="monitor-node", container_label_io_kubernetes_container_name="dbms"}})',
            'title': 'CPU Util User [s]'
        },
        'total_cpu_util_sys_s': {
            'query': 'sum(container_cpu_system_seconds_total{{job="monitor-node", container_label_io_kubernetes_container_name="dbms"}})',
            'title': 'CPU Util Sys [s]'
        },
        'total_cpu_throttled_s': {
            'query': 'sum(container_cpu_cfs_throttled_seconds_total{{job="monitor-node", container_label_io_kubernetes_container_name="dbms"}})',
            'title': 'CPU Throttle [s]'
        },
        'total_cpu_util_others_s': {
            'query': 'sum(container_cpu_usage_seconds_total{{job="monitor-node", container_label_io_kubernetes_container_name!="dbms",id!="/"}})',
            'title': 'CPU Util Others [s]'
        },
        'total_network_rx': {
            'query': 'sum(container_network_receive_bytes_total{{container_label_app="bexhoma", job="monitor-node"}})/1024/1024',
            'title': 'Net Rx [MiB]'
        },
        'total_network_tx': {
            'query': 'sum(container_network_transmit_bytes_total{{container_label_app="bexhoma", job="monitor-node"}})/1024/1024',
            'title': 'Net Tx [MiB]'
        },
        'total_fs_read': {
            'query': 'sum(container_fs_reads_bytes_total{{job="monitor-node", container_label_io_kubernetes_container_name="dbms"}})/1024/1024',
            'title': 'FS Read [MiB]'
        },
        'total_fs_write': {
            'query': 'sum(container_fs_writes_bytes_total{{job="monitor-node", container_label_io_kubernetes_container_name="dbms"}})/1024/1024',
            'title': 'FS Write [MiB]'
        },
        'total_gpu_util': {
            'query': 'sum(DCGM_FI_DEV_GPU_UTIL{{UUID=~"{gpuid}"}})',
            'title': 'GPU Util [%]'
        },
        'total_gpu_power': {
            'query': 'sum(DCGM_FI_DEV_POWER_USAGE{{UUID=~"{gpuid}"}})',
            'title': 'GPU Power Usage [W]'
        },
        'total_gpu_memory': {
            'query': 'sum(DCGM_FI_DEV_FB_USED{{UUID=~"{gpuid}"}})',
            'title': 'GPU Memory [MiB]'
        },
    }
        },
    }
},
```

### Data Sources

Data sources and imports can be adressed using a key.
This is organized as follows:

```
'volumes': {
    'tpch': {
        'initscripts': {
            'SF1': [
                'initschema-tpch.sql',
                'initdata-tpch-SF1.sql',
                'initdata-tpch-SF1.sh'
            ],
            'SF1-index': [
                'initschema-tpch.sql',
                'initdata-tpch-SF1.sql',
                'initdata-tpch-SF1.sh',
                'initindexes-tpch.sql',
            ],
            'SF10': [
                'initschema-tpch.sql',
                'initdata-tpch-SF10.sql',
                'initdata-tpch-SF10.sh'
            ],
            'SF10-index': [
                'initschema-tpch.sql',
                'initdata-tpch-SF10.sql',
                'initdata-tpch-SF10.sh',
                'initindexes-tpch.sql',
            ],
        }
    }
},
```

* `tpch`: Name of the data source.
* `initscripts`: Dict of scripts to load the data source into a database.
It consists of  
  * a name, for example `SF1-index`,
  * a list of script names.  
  The scripts `.sql` are sent to the command line tool of the DBMS (`loadData` - see below) and the files `.sh` are executed as shell scripts.
The scripts must be present in a [config folder](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch), say `experiments/tpch/`.

The data itself must reside on a persistent volume within the cluster, that will be mounted into the DBMS container.
The examples above refer to `/data/tpch/SF1/` for example.


### DBMS

DBMS can be adressed using a key.
We have to define some data per key, for example for the key `MonetDB` we use:

```
'dockers': {
   'MonetDB': {
        'loadData': 'cd /home/monetdb;mclient demo < {scriptname}',
        'template': {
            'version': '11.37.11',
            'alias': 'Columnwise',
            'docker_alias': 'Columnwise',
             'JDBC': {
                'auth': ['monetdb', 'monetdb'],
                'driver': 'nl.cwi.monetdb.jdbc.MonetDriver',
                'jar': 'monetdb-jdbc-2.29.jar',
                'url': 'jdbc:monetdb://{serverip}:9091/demo?so_timeout=0'
            }
        },
        'logfile': '/tmp/monetdb5/dbfarm/merovingian.log',
        'datadir': '/var/monetdb5/',
        'priceperhourdollar': 0.0,
    },
}
```

This includes
* `loadData`: A command to run a script inside of the DBMS. This will run inside of the container of the DBMS and is used to load data. `{scriptname}` is a placeholder for the script name inside the container.
* `template`: [DBMS](https://dbmsbenchmarker.readthedocs.io/en/latest/DBMS.html) JDBC connection info that will be handed over to the benchmarker, c.f. [example](https://dbmsbenchmarker.readthedocs.io/en/latest/Options.html#connection-file).  
Some of the data in the reference, like `hostsystem`, will be added by bexhoma automatically.  
The JDBC driver jar must be locally available inside the container.  
Some placeholders in the URL are: `serverip` (set automatically to match the corresponding pod), `dbname`, `DBNAME`, `timout_s`, `timeout_ms` (name of the database in lower and upper case, timeout in seconds and miliseconds)
* `logfile` and `datadir` that contain information about where the DBMS stores logs and databases resp.
* an optional `priceperhourdollar` that is currently ignored.

