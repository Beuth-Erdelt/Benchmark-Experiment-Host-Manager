# Deployments in Kubernetes

The deployment is expected to be given as a file named `'deployment-'+docker+'-'+instance+'.yml'`
Such files are generated from a template.

Content of this document:
* How do [templates](#templates) work
  * What templates are [included](#included)
  * Adjust the templates to [your cluster](#your-cluster)
* How to [parametrize](#parametrize-templates) templates at runtime

## Templates

Template files are named `'deploymenttemplate-"+docker+".yml'`.

To generate a file `'deployment-'+docker+'-'+instance+'.yml'` from this
  * the instance name is understood as `cpu-mem-gpu-gputype`
  * the yaml file is changed as
  ```  
  dep['spec']['template']['spec']['containers'][0]['resources']['requests']['cpu'] = cpu  
  dep['spec']['template']['spec']['containers'][0]['resources']['limits']['cpu'] = cpu  
  dep['spec']['template']['spec']['containers'][0]['resources']['requests']['memory'] = mem  
  dep['spec']['template']['spec']['containers'][0]['resources']['limits']['memory'] = mem  
  dep['spec']['template']['spec']['nodeSelector']['gpu'] = gputype  
  dep['spec']['template']['spec']['containers'][0]['resources']['limits']['nvidia.com/gpu'] = int(gpu)
   ```

### Included

This repository includes some templates at https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/k8s

[DBMS](DBMS.md) included are:
* MariaDB (10.4.6)
* MonetDB (11.31.7)
* OmniSci (v5.4.0)
* PostgreSQL (11.4)

To be added in near future:
* Exasol (7.0.0)  
  You will need a Docker image including EXAplus
* MemSQL (centos-7.1.8-43a12901be-2.0.0-1.7.0)  
  You will have to add a licence key
* MySQL (8.0.21)  
  You will need a Docker image including tar
* Oracle DB (18.4.0-xe)  
  You will need to build the Docker image
* MS SQL Server (2019-CU5-ubuntu-18.04)

### Your Cluster

To make these work, you may have to add the name of your Docker pull secret and the name of your persistant volume. 

The default name of the secret is `private-registry-auth`:
```
      imagePullSecrets:
      - {name: private-registry-auth}
```

The default name of the PV is `volume-benchmarking`:
```
      - name: benchmark-data-volume
        persistentVolumeClaim: {claimName: volume-benchmarking}
```

## Parametrize Templates

The resources (requests, limits and nodeSelector) can also be set explicitly using
```
cluster.set_resources(
  requests = {
    'cpu': cpu,
    'memory': mem
  },
  limits = {
    'cpu': 0,     # unlimited
    'memory': 0   # unlimited
  },
  nodeSelector = {
    'cpu': cpu_type,
    'gpu': gpu_type,
  })
```

For further information and option see the [documentation](API.md#set-resources).
