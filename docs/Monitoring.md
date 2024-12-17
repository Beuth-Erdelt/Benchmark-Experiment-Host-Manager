# Monitoring

Monitoring refers to automatical observation of resource consumption of components.

Bexhoma basically offers two variants
* Monitor only the system-under-test (SUT) with `-m`
* Monitor all components with `-mc`

Moreover bexhoma expects the cluster to be prepared, i.e. a daemonset of cAdvisors (exporters) is running and there is a Prometheus server (collector) we can connect to.
However bexhoma can optionally install these components if missing.

## Configuration and Options

Monitoring can be configured.
Probably you won't have to change much.
If there is a Prometheus server running in your cluster, make sure to adjust `service_monitoring`.
If there is no Prometheus server running in your cluster, make sure to leave the template in `service_monitoring` as is.
Bexhoma checks at the beginning of an experiment if the URL provided is reachable;
it uses cURL inside the dashboard pod to test if `query_range?query=sum(node_memory_MemTotal_bytes)&start={start}&end={end}&step=60` has a return status of 200 (where `start`is 5 min ago and `end` is 4 min ago).

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
* `extend`: number of seconds each interval of observations should be extended  
  i.g., an interval [t,t'] will be extended to [t-e, t'+e]
* `shift`: number of seconds each interval of observations should be shifted  
  i.g., an interval [t,t'] will be shifted to [t+s, t'+s]
* `metrics`: a dict of informations about metrics to be collected, see below


Example metrics, c.f. [config file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s-cluster.config):

```
'monitor': {
    'service_monitoring': 'http://{service}.{namespace}.svc.cluster.local:9090/api/v1/',
    'extend': 20,
    'shift': 0,
    'metrics': {
'total_cpu_memory': {
    'query': '(sum(max(container_memory_working_set_bytes{{container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_container_name="dbms"}}) by (instance)))/1024/1024',
    'title': 'CPU Memory [MiB]'
},
'total_cpu_memory_cached': {
    'query': '(sum(max(container_memory_usage_bytes{{container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_container_name="dbms"}}) by (instance)))/1024/1024',
    'title': 'CPU Memory Cached [MiB]'
},
'total_cpu_util': {
    'query': 'sum(irate(container_cpu_usage_seconds_total{{container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_container_name="dbms"}}[1m]))',
    'title': 'CPU Util [%]'
},
'total_cpu_throttled': {
    'query': 'sum(irate(container_cpu_cfs_throttled_seconds_total{{container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_container_name="dbms"}}[1m]))',
    'title': 'CPU Throttle [%]'
},
'total_cpu_util_others': {
    'query': 'sum(irate(container_cpu_usage_seconds_total{{container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_container_name!="dbms",id!="/"}}[1m]))',
    'title': 'CPU Util Others [%]'
},
'total_cpu_util_s': {
    'query': 'sum(container_cpu_usage_seconds_total{{container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_container_name="dbms"}})',
    'title': 'CPU Util [s]'
},
'total_cpu_util_user_s': {
    'query': 'sum(container_cpu_user_seconds_total{{container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_container_name="dbms"}})',
    'title': 'CPU Util User [s]'
},
'total_cpu_util_sys_s': {
    'query': 'sum(container_cpu_system_seconds_total{{container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_container_name="dbms"}})',
    'title': 'CPU Util Sys [s]'
},
'total_cpu_throttled_s': {
    'query': 'sum(container_cpu_cfs_throttled_seconds_total{{container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_container_name="dbms"}})',
    'title': 'CPU Throttle [s]'
},
'total_cpu_util_others_s': {
    'query': 'sum(container_cpu_usage_seconds_total{{container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_container_name!="dbms",id!="/"}})',
    'title': 'CPU Util Others [s]'
},
'total_network_rx': {
    'query': 'sum(container_network_receive_bytes_total{{container_label_app="bexhoma", container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)"}})/1024/1024',
    'title': 'Net Rx [MiB]'
},
'total_network_tx': {
    'query': 'sum(container_network_transmit_bytes_total{{container_label_app="bexhoma", container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)"}})/1024/1024',
    'title': 'Net Tx [MiB]'
},
'total_fs_read': {
    'query': 'sum(container_fs_reads_bytes_total{{container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_container_name="dbms"}})/1024/1024',
    'title': 'FS Read [MiB]'
},
'total_fs_write': {
    'query': 'sum(container_fs_writes_bytes_total{{container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_container_name="dbms"}})/1024/1024',
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
