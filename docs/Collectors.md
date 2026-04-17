# Collectors

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

## Introductory Remarks

### Missing
* connection and configuration also in monitoring and connection df

### Naming
* There is an experiment having a code, say `1775855486`.
* The experiment inspects a SUT, say `PostgreSQL-A`. This is called a `configuration`.
* The experiment is run several times, say twice. The indicator of the run is called `experiment_run`.
* Each run can have several phases as a sequence. The number of the phase is called `client`. The state of the configuration in a phase is called a `connection`.
* Each client can have several `pods`, that are run in parallel. A pod represents a driver.
* Performance metrics are collected per driver pod.  
    The naming of an instance is `<sut>-<experiment_run>-<client>-<pod>`. It is unique (only) per experiment.
    The naming  `<code>-<sut>-<experiment_run>-<client>-<pod>` is a unique identifier.
* Monitoring metrics are collected per phase. They are automatically aggregated across parallel pods.  
    The naming of an instance is `<sut>-<experiment_run>-<client>`. It is unique (only) per experiment.
    The naming  `<code>-<sut>-<experiment_run>-<client>` is a unique identifier.

### Aggregation
* Aggregation is complicated. Some metrics are aggregated via count, sum, max or average. Others cannot be aggregated sensibly, like experiment code or latency percentiles.
* There are helper functions to aggregated pods that are certainly run in parallel.  
  So `<sut>-<experiment_run>-<client>-<pod>` are aggregated to `<sut>-<experiment_run>-<client>`.
* An exception is multi-tenancy.

## Class `collector`

* Constructor matching the experiment type, for example `collectors.benchbase(path, codes)`  
  `codes` is a list of codes of experiments, that will be combined.
* Evaluator object `evaluate = collect.get_evaluator()`
* Add connection infos to monitoring or performance dataframes with `collect.add_metadata(df)`
* Dataframe of connection infos `collect.get_connections()`
    * Index is name of connection

### Monitoring Metrics

* Dataframe of available metrics `collect.df_metrics`
    * Index is key of metric
* Dataframe of monitored components `collect.get_monitored_phases()`
    * Index is key of component
* Dataframe of aggregated metrics per connection `collect.get_monitoring_aggregated_per_connection(component)`
    * Index is name of connection
    * Metrics aggregated per code, experiment_run and client
* Dataframe of time series for a metric of a connection in an experiment `collect.get_monitoring_timeseries_per_connection(code, metric, component)`
    * Index is name of connection
    * Unstacked (wide format)
* Dataframe of time series for a metric in all experiments `collect.get_monitoring_timeseries_all(metric)`
    * Index just enumerates
    * Stacked (long format)
* **Open**: Dataframe of aggregated metrics per connection and across tenants `collect.get_monitoring_all()`
    * Index just enumerates
    * Metrics aggregated per code, experiment_run and client and across tenants

### Performance Metrics
* Dataframe of loading metrics `collect.get_loading_time_max_all()`
    * Index is name of connection
* Dataframe of performance aggregated per parallel client `collect.get_performance_aggregated_per_connection()`
    * Index is name of connection
    * Performance aggregated per code, experiment_run and client
* Dataframe of performance for one experiment `collect.get_performance_per_pod()`
    * Performance of each single pod (driver)
    * Index is name of client pod
* Dataframe of performance for all experiments `collect.get_performance_all_single()`
    * Performance of each single client (driver)
    * Index is name of client pod


[1] [Benchmarking Multi-Tenant Architectures in PostgreSQL](https://doi.org/10.48786/edbt.2026.46)
> Erdelt, P.K., and Rabl T. (2026)
> In: Proceedings 29th International Conference on Extending Database Technology, EDBT 2026
> OpenProceedings.org
> https://doi.org/10.48786/edbt.2026.46
