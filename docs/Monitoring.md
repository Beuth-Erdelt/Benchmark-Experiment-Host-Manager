# Monitoring

Monitoring refers to automatical observation of resource consumption of components.

Bexhoma basically offers two variants
* Monitor only the system-under-test (SUT) with `-m`
* Monitor all components with `-mc`

Moreover bexhoma expects the cluster to be prepared, i.e. a daemonset of cAdvisors (exporters) is running and there is a Prometheus server (collector) we can connect to.
However bexhoma can optionally install these components if missing.

## Configuration

Monitoring can be configured.
Probably you won't have to change much.
If there is a Prometheus server running in your cluster, make sure to adjust `service_monitoring`.
If there is no Prometheus server running in your cluster, make sure to leave the template in `service_monitoring` as is.

* `service_monitoring`: a DNS name of the Prometheus server
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

Moreover the is automatical substituion of
* `container_label_io_kubernetes_container_name="dbms"`: 

## Installation

Deployment
* `cadvisor`

Prometheus
* `job="monitor-node"`
* `container_name="dbms"`
