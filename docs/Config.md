# How to configure an experiment setup

We need
* a [config file](#clusterconfig) containing cluster information , say `cluster.config`
* a [config folder](https://github.com/Beuth-Erdelt/GEO-GPU-DBMS-Benchmarks#config-folder) for the benchmark tool, say `experiments/tpch/`, containing a config file `queries.config` for the [queries](https://github.com/Beuth-Erdelt/DBMS-Benchmarker#query-file)
* some additional data depending on if it is an [AWS](#on-aws) or a [k8s](#on-k8s) cluster
* a python script managing the experimental workflow, say `experiment-tpch.py`

## Clusterconfig

The configuration of the cluster, that is the possible host settings, consists of these parts (see also [example](template-cluster.config) config file):

**Result folder** for the benchmark tool:
```
'benchmarker': {
    'resultfolder': '/benchmarks' # Local path to results folder of benchmark tool
},
```

Information about the **volumes** containing the raw data for the DBMS to import. We also set a named list of **import scripts** per data set:
```
'volumes': {
    'tpch': { # Volume: Name
        'initscripts': { 
            '1shard-SF1': [ # Init Script: Name
                'initschema-tpch.sql',
                'initdata-tpch-SF1.sql'
            ],
            '4shard-SF1': [ # Init Script: Name
                'initschema-tpch-4shards.sql',
                'initdata-tpch-SF1.sql'
            ],
        }
    },
    'gdelt': { # Volume: Name
        'initscripts': {
            '1shard': [ # Init Script: Name
                'initschema-gdelt.sql',
                'initdata-gdelt.sql'
            ],
            '4shard-time': [ # Init Script: Name
                'initschema-gdelt-4shards.sql',
                'initdata-gdelt.sql'
            ],
        }
    }
},
```

Information about the **DBMS** to use:
```
'dockers': {
    'OmniSci': {
        'loadData': 'bin/omnisql -u admin -pHyperInteractive < {scriptname}', # DBMS: Command to Login and Run Scripts
        'template': { # Template for Benchmark Tool
            'version': 'CE v4.7',
            'alias': '',
            'JDBC': {
                'driver': 'com.omnisci.jdbc.OmniSciDriver',
                'url': 'jdbc:omnisci:{serverip}:9091:omnisci',
                'auth': {'user': 'admin', 'password': 'HyperInteractive'},
                'jar': 'omnisci-jdbc-4.7.1.jar' # DBMS: Local Path to JDBC Jar
            }
        },
        'logfile': '/omnisci-storage/data/mapd_log/omnisci_server.INFO', # DBMS: Path to Log File on Server
        'datadir': '/omnisci-storage/data/mapd_data/', # DBMS: Path to directory containing data storage
        'priceperhourdollar': 0.0, # DBMS: Price per hour in USD if DBMS is rented
    }
}
```
This requires
* a base name for the DBMS
* a prepared docker image of the DBMS
  * with an open port for a JDBC connection
* a placeholder `template` for the benchmark tool
* the JDBC driver jar locally available
* a command running the init scripts with `{scriptname}` as a placeholder for the script name inside the container
* `{serverip}` as a placeholder for the host address (localhost for k8s, an Elastic IP for AWS)
* an optional `priceperhourdollar`

### On k8s

We need to add to the config file
```
'credentials': {
    'k8s': {
        'namespace': 'mynamespace', # K8s: Namespace of User
        'clustername': 'My_k8s_cluster', # K8s: Name of Cluster (just for annotation)
        'appname': 'dbmsbenchmarker', # K8s: To find corresponding deployments etc labels: app:
        'port': 9091 # K8s: Local port for connecting via JDBC after port forwarding
    }
}
```
This will tell the tool how to adress the cluster. An access token has to be installed at `~/.kube/config` with the corresponding `namespace` and all deployments, services, pods and pvcs of this tool will be recognized by
```
metadata:
  labels:
    app: dbmsbenchmarker
```

We also need to add for each DBMS which port we have to forward
```
'dockers': {
    'OmniSci': {
        'port': 3306, # k8s: remote port of the DBMC for connecting via JDBC
    }
}
```

For the deployments we either need yaml files containing all necessary information, i.e.
* Deployment with container information
* Service for networking
* PVC for local storage

or we need a template yaml file, c.f. [how to generate deployments](#prepare-experiment) and an [example](https://github.com/perdelt/kubecluster/blob/master/benchmarker/k8s/deploymenttemplate-OmniSci.yml).

### On AWS


We additionally need
```
'credentials': {
    'AWS': {
        'AWS_Access_Key_ID': '', # AWS Access: Key ID
        'AWS_Secret_Access_Key': '', # AWS Access: Secret Access Key
        'Default_region': 'eu-central-1', # AWS Access: Default region
        'monitor': {
            'grafanatoken': 'Bearer 46363756756756476754756745', # Grafana: Access Token
            'grafanaurl': 'http://127.0.0.1:3000/api/datasources/proxy/1/api/v1/', # Grafana: API URL
            'exporter': {
                'dcgm': docker run --runtime=nvidia --name gpu_monitor_dcgm --rm -d --publish 8000:8000 1234.dkr.ecr.eu-central-1.amazonaws.com/name/dcgm:latest',
                'nvlink': 'docker run --runtime=nvidia --name gpu_monitor_nvlink --rm -d --publish 8001:8001 1234.dkr.ecr.eu-central-1.amazonaws.com/name/nvlink:latest',
                'node': 'docker run --name cpu_monitor_prom --rm -d --publish 9100:9100 prom/node-exporter:latest'
            } 
        },
        'worker': {
            'ip': '127.1.2.3', # Elastic IP: IP Address
            'allocid': 'eipalloc-1234512345', # Elastic IP: Allocation ID
            'ppk': 'cluster.pem', # SSH: Local path to private key for acccessing instances in AWS cluster
            'username': 'ubuntu', # SSH: User name 
        },
    }
}
```
and for each volume an AWS Volume ID
```
'volumes': {
    'tpch': { # Volume: Name
        'id': 'vol-1234512345', # AWS Volume ID
    },
    'gdelt': { # Volume: Name
        'id': 'vol-9876987655', # AWS Volume ID
    }
},
```
and for each instance some basic information
```
'instances': {
    '1xK80': { # Instance: Name
        'id': 'i-918273764645', # Instance: Id
        'type': 'p2.xlarge', # Instance: Type
        'priceperhourdollar': 1.326, # Instance: Price per hour (on demand)
        'device': 'sdf', # Instance: Device name ec2volume.attach_to_instance(/dev/$device)
        'deviceMount': 'xvdf', # Instance: Device mount name - 'sudo mount /dev/$deviceMount /data'
        'RAM': '64G', # Instance: RAM
        'GPU': '1xK80' # Instance: GPUs
    },
    '8xK80': { # Instance: Name
        'id': 'i-192838475655', # Instance: Id
        'type': 'p2.8xlarge', # Instance: Type
        'priceperhourdollar': 10.608, # Instance: Price per hour (on demand)
        'device': 'sdf', # Instance: Device name ec2volume.attach_to_instance(/dev/$device)
        'deviceMount': 'xvdf', # Instance: Device mount name - 'sudo mount /dev/$deviceMount /data'
        'RAM': '480G', # Instance: RAM
        'GPU': '8xK80' # Instance: GPUs
    },
},
```
and for each DBMS the image source and docker command
```
'dockers': {
    'OmniSci': {
        'image': 'eu-central-1.amazonaws.com/myrepository/dbms:omnisci', # ECR: Path to DBMS Docker Image
        'start': 'docker run -d --runtime=nvidia --name benchmark -p 6273:6273 -p 6275-6280:6275-6280 -p 9091:6274 -v /data:/data/ ', # Docker: Part of Command to Start Container
    }
}
```

This requires
* A managing host having access to AWS
  * typically this means an `~/.aws` directory with config and credentials files
* EC2 instances as experiment hosts having
  * aws cli installed
  * docker installed
  * required ports open
* EIP for attaching to the current experiment host
* EBS volumes containing raw data
* Optionally: ECR for simple docker registry

### Monitoring

Monitoring requires
* A server having Prometheus installed
  * With Prometheus scraping the fixed EIP for a fixed list of ports
* A server (the same) having Grafana installed
  * With Grafana importing metrics from Prometheus
  * `grafanatoken` and `grafanaurl` to access this from DBMSBenchmarker
* A dict of exporters given as docker commands
  * Will be installed and activated automatically at each instance when `cluster.prepareExperiment()` is invoked.
