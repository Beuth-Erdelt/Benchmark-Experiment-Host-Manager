# Monitoring

Monitoring refers to automatical observation of resource consumption of components.

Bexhoma basically offers two variants
* Monitor only the system-under-test (SUT) with `-m`
* Monitor all components with `-mc`

Moreover bexhoma expects the cluster to be prepared, i.e. a daemonset of cAdvisors (exporters) is running and there is a Prometheus server (collector) we can connect to.
However bexhoma can optionally install these components if missing.

There is a third option in alpha status: `-ma` for collection of application metrics, for example, pgexporter

## Configuration and Options

Monitoring can be configured.
Probably you won't have to change much.
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

Configuration takes place in `cluster.config`:
* `service_monitoring`: a DNS name of the Prometheus server  
  the placeholders `service` and `namespace` are replaced by the service of the monitoring component of the experiment and the namespace inside the cluster config resp.
* `service_monitoring_application`: optional setting. This should not be changed. It is a template how to find sidecar containers for collecting application metrics, for example, pgexporter
* `extend`: number of seconds each interval of observations should be extended  
  i.g., an interval [t,t'] will be extended to [t-e, t'+e]
* `shift`: number of seconds each interval of observations should be shifted  
  i.g., an interval [t,t'] will be shifted to [t+s, t'+s]
* `metrics`: a dict of informations about metrics to be collected, see below
  * `type`: is cluster or application
  * `active`: if set to False, the metric will be ignored
  * `metric`: is gauge or counter or ratio; this does not affect bexhoma, it only affects how results will be presented (for counter: max - min, for gauge: mean, for ratio: max)
  * `query`: promql query
  * `title`: for presentation in summary


Example metrics, c.f. [config file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s-cluster.config):

```
'monitor': {
    'service_monitoring': 'https://prometheus.mycluster.com/api/v1/',                                      # preinstalled external address
    'service_monitoring_application': 'http://{service}.{namespace}.svc.cluster.local:9090/api/v1/',       # self installed
    'extend': 20,
    'shift': 0,
    'metrics': {
        'total_cpu_memory': {
            'type': 'cluster',
            'active': True,
            'metric': 'gauge',
            'query': '(sum(max(container_memory_working_set_bytes{{pod=~"(.*){configuration}-{experiment}(.*)", pod=~"(.*){configuration}-{experiment}(.*)", container="dbms"}}) by (instance)))/1024/1024',
            'title': 'CPU Memory [MiB]'
        },
        'total_cpu_memory_cached': {
            'type': 'cluster',
            'active': True,
            'metric': 'gauge',
            'query': '(sum(max(container_memory_usage_bytes{{pod=~"(.*){configuration}-{experiment}(.*)", pod=~"(.*){configuration}-{experiment}(.*)", container="dbms"}}) by (instance)))/1024/1024',
            'title': 'CPU Memory Cached [MiB]'
        },
        'total_cpu_util': {
            'type': 'cluster',
            'active': True,
            'metric': 'gauge',
            'query': 'sum(irate(container_cpu_usage_seconds_total{{pod=~"(.*){configuration}-{experiment}(.*)", pod=~"(.*){configuration}-{experiment}(.*)", container="dbms"}}[1m]))',
            'title': 'CPU Util [%]'
        },
        'total_cpu_throttled': {
            'type': 'cluster',
            'active': True,
            'metric': 'gauge',
            'query': 'sum(irate(container_cpu_cfs_throttled_seconds_total{{pod=~"(.*){configuration}-{experiment}(.*)", pod=~"(.*){configuration}-{experiment}(.*)", container="dbms"}}[1m]))',
            'title': 'CPU Throttle [%]'
        },
        'total_cpu_util_others': {
            'type': 'cluster',
            'active': True,
            'metric': 'gauge',
            'query': 'sum(irate(container_cpu_usage_seconds_total{{pod=~"(.*){configuration}-{experiment}(.*)", pod=~"(.*){configuration}-{experiment}(.*)", container!="dbms",id!="/"}}[1m]))',
            'title': 'CPU Util Others [%]'
        },
        'total_cpu_util_s': {
            'type': 'cluster',
            'active': True,
            'metric': 'counter',
            'query': 'sum(container_cpu_usage_seconds_total{{pod=~"(.*){configuration}-{experiment}(.*)", pod=~"(.*){configuration}-{experiment}(.*)", container="dbms"}})',
            'title': 'CPU Util [s]'
        },
        'total_cpu_util_user_s': {
            'type': 'cluster',
            'active': True,
            'metric': 'counter',
            'query': 'sum(container_cpu_user_seconds_total{{pod=~"(.*){configuration}-{experiment}(.*)", pod=~"(.*){configuration}-{experiment}(.*)", container="dbms"}})',
            'title': 'CPU Util User [s]'
        },
        'total_cpu_util_sys_s': {
            'type': 'cluster',
            'active': True,
            'metric': 'counter',
            'query': 'sum(container_cpu_system_seconds_total{{pod=~"(.*){configuration}-{experiment}(.*)", pod=~"(.*){configuration}-{experiment}(.*)", container="dbms"}})',
            'title': 'CPU Util Sys [s]'
        },
        'total_cpu_throttled_s': {
            'type': 'cluster',
            'active': True,
            'metric': 'counter',
            'query': 'sum(container_cpu_cfs_throttled_seconds_total{{pod=~"(.*){configuration}-{experiment}(.*)", pod=~"(.*){configuration}-{experiment}(.*)", container="dbms"}})',
            'title': 'CPU Throttle [s]'
        },
        'total_cpu_util_others_s': {
            'type': 'cluster',
            'active': True,
            'metric': 'counter',
            'query': 'sum(container_cpu_usage_seconds_total{{pod=~"(.*){configuration}-{experiment}(.*)", pod=~"(.*){configuration}-{experiment}(.*)", container!="dbms",id!="/"}})',
            'title': 'CPU Util Others [s]'
        },
        'total_network_rx': {
            'type': 'cluster',
            'active': False,
            'metric': 'counter',
            'query': 'sum(container_network_receive_bytes_total{{container_label_app="bexhoma", container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)"}})/1024/1024',
            'title': 'Net Rx [MiB]'
        },
        'total_network_tx': {
            'type': 'cluster',
            'active': False,
            'metric': 'counter',
            'query': 'sum(container_network_transmit_bytes_total{{container_label_app="bexhoma", container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)"}})/1024/1024',
            'title': 'Net Tx [MiB]'
        },
        'total_fs_read': {
            'type': 'cluster',
            'active': False,
            'metric': 'counter',
            'query': 'sum(container_fs_reads_bytes_total{{container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_container_name="dbms"}})/1024/1024',
            'title': 'FS Read [MiB]'
        },
        'total_fs_write': {
            'type': 'cluster',
            'active': False,
            'metric': 'counter',
            'query': 'sum(container_fs_writes_bytes_total{{container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_container_name="dbms"}})/1024/1024',
            'title': 'FS Write [MiB]'
        },
        'total_gpu_util': {
            'type': 'cluster',
            'active': False,
            'metric': 'gauge',
            'query': 'sum(DCGM_FI_DEV_GPU_UTIL{{UUID=~"{gpuid}"}})',
            'title': 'GPU Util [%]'
        },
        'total_gpu_power': {
            'type': 'cluster',
            'active': False,
            'metric': 'gauge',
            'query': 'sum(DCGM_FI_DEV_POWER_USAGE{{UUID=~"{gpuid}"}})',
            'title': 'GPU Power Usage [W]'
        },
        'total_gpu_memory': {
            'type': 'cluster',
            'active': False,
            'metric': 'gauge',
            'query': 'sum(DCGM_FI_DEV_FB_USED{{UUID=~"{gpuid}"}})',
            'title': 'GPU Memory [MiB]'
        },
    }
},
```

This is handed over to the [DBMS configuration](https://dbmsbenchmarker.readthedocs.io/en/docs/Options.html#connection-file) of [DBMSBenchmarker](https://dbmsbenchmarker.readthedocs.io/en/docs/Concept.html#monitoring-hardware-metrics) for the collection of the metrics.


### Explanation

There is a placeholder `{gpuid}` that is substituted automatically by a list of GPUs present in the pod.
There is a placeholder `{configuration}` that is substituted automatically by the name of the current configuration of the SUT.
There is a placeholder `{experiment}` that is substituted automatically by the name (identifier) of the current experiment. 

Moreover the is an automatical substituion of `container_label_io_kubernetes_container_name="dbms"`; the `dbms` refers to the sut. For other containers it is replaced by `datagenerator`, `sensor` and `dbmsbenchmarker`.

Note that the metrics make a summation over all matching components (containers, CPU cores etc).

### Installation Templates

cAdvisor runs as a container `cadvisor` and a service with `port-monitoring` 9300
* example per SUT (sidecar container): `k8s/deploymenttemplate-PostgreSQL.yml`
* example per node (daemonset): `k8s/daemonsettemplate-monitoring.yml`

Prometheus runs as a container with a service with `port-prometheus` 9090
* `k8s/deploymenttemplate-bexhoma-prometheus.yml`

## Application Metrics

Metrics collectors for DBMS can be run as sidecar containers.
A list of metrics is defined in the DBMS part of the configuration file.
Bexhoma has two methods implemented: Balackbox and non-blackbox.


## Blackbox: PostgreSQL

A blackbox method in metric exporters means "collect metrics by probing the system from the outside, without relying on internal statistics.
Here, we collect metrics from an instance of an exporter.
We send requests to a /probe API and give a list of targets, one for each database.

* Example per SUT (sidecar container): `k8s/deploymenttemplate-PostgreSQL.yml`
* Example metrics, c.f. [config file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s-cluster.config):

```
'monitor': {
    'blackbox': True,
    'metrics': {
        'pg_stat_database_blks_read': {
            'type': 'application',
            'active': True,
            'metric': 'counter',
            'query': 'sum(pg_stat_database_blks_read{{datname!~"template.*"}})',
            'query2': 'sum(pg_stat_database_blks_read{{schemaname="{schema}", datname="{database}"}})',
            'query3': 'sum(sum by(datname) (pg_stat_database_blks_read{{datname!~"template.*"}})) / count(sum by(datname) (pg_stat_database_blks_read{{datname!~"template.*"}}))',
            'title': 'Disk Blocks Read Count'
        },
        'pg_stat_database_blks_hit': {
            'type': 'application',
            'active': True,
            'metric': 'counter',
            'query': 'sum(pg_stat_database_blks_hit{{datname!~"template.*"}})',
            'query2': 'sum(pg_stat_database_blks_hit{{schemaname="{schema}", datname="{database}"}})',
            'query3': 'sum(sum by(datname) (pg_stat_database_blks_hit{{datname!~"template.*"}})) / count(sum by(datname) (pg_stat_database_blks_hit{{datname!~"template.*"}}))',
            'title': 'Buffer Cache Hit Count'
        },
    },
},
```

## No Blackbox: MySQL

Here, we collect metrics from an instance of an exporter.
It automatically contains data about all databases in the system.

* Example per SUT (sidecar container): `k8s/deploymenttemplate-MySQL.yml`
* Example metrics, c.f. [config file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s-cluster.config):

```
'monitor': {
    'blackbox': False,
    'metrics': {
        'mysql_buffer_pool_hit_ratio': {
            'type': 'application',
            'active': True,
            'metric': 'gauge',
            'query': '(rate(mysql_global_status_innodb_buffer_pool_reads[5m]) == 0) or (1 - (rate(mysql_global_status_innodb_buffer_pool_reads[5m]) / rate(mysql_global_status_innodb_buffer_pool_read_requests[5m])))',
            'title': 'InnoDB Buffer Pool Hit Ratio'
        },
        'mysql_queries_per_second': {
            'type': 'application',
            'active': True,
            'metric': 'gauge',
            'query': 'rate(mysql_global_status_queries[5m])',
            'title': 'Queries Per Second (QPS)'
        },
    },
},
```
