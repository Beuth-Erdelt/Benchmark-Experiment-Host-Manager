# Collectors

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

## Introductory Remarks

### Naming
* There is an experiment having a code, say `1775855486`.
* The experiment inspects a SUT. This is called a `configuration`.  
    Example: `PostgreSQL-A`
* The experiment is run several times, say twice. The indicator of the run is called `experiment_run`.
* Each run can have several phases as a sequence. The number of the phase is called `client`.
* Each client can have several `pods`, that are run in parallel. A pod represents a driver.
* The state of the configuration in a phase as seen by a pod is called a `connection`.  
    The naming of an instance of a `connection` is `<sut>-<experiment_run>-<client>-<pod>`. It is unique (only) per experiment.
    The naming  `<code>-<configuration>-<experiment_run>-<client>-<pod>` is a unique identifier.  
    Example: `1775855486-PostgreSQL-A-1-2-3` - first execution run of experiment, second client in sequence of clients, third pod of parallel running pods
* Performance metrics are collected per `connection` (driver pod).
* Monitoring metrics are collected per phase. They are automatically aggregated across parallel pods by Prometheus.  
    The naming of an instance is `<configuration>-<experiment_run>-<client>`. It is unique (only) per experiment.
    The naming  `<code>-<configuration>-<experiment_run>-<client>` is a unique identifier.  
    Example: `1775855486-PostgreSQL-A-1-2` - first execution run of experiment, second client in sequence of clients

### Aggregation
* Aggregation is complicated. Some metrics are aggregated via count, sum, max or average. Others cannot be aggregated sensibly, like experiment code or latency percentiles.
* There are helper functions to aggregated pods that are certainly run in parallel.  
  So `<configuration>-<experiment_run>-<client>-<pod>` are aggregated to `<configuration>-<experiment_run>-<client>`.
* An exception is multi-tenancy. Here, a single service provider can be represented by several configurations (container instances) [1]. To assess the performance a service provider can offer, we have to aggregate across different configurations.

## Class `collector`

* Constructor matching the experiment type, for example `collectors.benchbase(path, codes)`  
  `codes` is a list of codes of experiments, that will be combined.
* Evaluator object `evaluate = collect.get_evaluator()`
* Add connection infos to monitoring or performance dataframes with `collect.add_metadata(df)`
* Dataframe of connection infos `collect.get_connections()`
    * Index is name of connection

## Monitoring Metrics

* Dataframe of available metrics `collect.get_metrics_metadata()`
    * Index is key of metric
* Dataframe of monitored components `collect.get_monitored_components()`
    * Index is key of component
* Dataframe of aggregated metrics per phase `collect.get_monitoring_aggregated_per_phase(component)`
    * Index is name of phase
    * Metrics aggregated per code, experiment_run, client, type_tenants, num_tenants
    * Aggregation is given by type of metric (count: max-min, others: mean)
* Dataframe of time series for a metric in the phase an experiment `collect.get_monitoring_timeseries_per_phase(code, metric, component)`
    * Index is name of connection
    * Unstacked (wide format)
* Dataframe of time series for a metric in all experiments `collect.get_monitoring_timeseries_all(metric)`
    * Index just enumerates
    * Stacked (long format)
* **Open**: Dataframe of aggregated metrics per connection and across tenants `collect.get_monitoring_all()`
    * Index just enumerates
    * Metrics aggregated per code, experiment_run and client and across tenants

## Performance Metrics - Benchmarking Phases

* Dataframe of performance for one experiment `collect.get_performance_per_connection()`
    * Index is name of connection
    * Performance of each single pod (driver)
* Dataframe of performance aggregated per parallel client `collect.get_performance_aggregated_per_phase()`
    * Index is name of phase
    * Performance aggregated per code, experiment_run and client

### DBMSBenchmarker

* Dataframe of latencies (in ms) per query and connection `get_query_latencies()`
    * Index is name of connection
    * Query number can optionally be translated into the title of the query
* Dataframe of errors per query and connection `get_total_errors()`
    * Index is name of connection
    * Query number can optionally be translated into the title of the query
* Dataframe of warnings per query and connection `get_total_warnings()`
    * Index is name of connection
    * Query number can optionally be translated into the title of the query

## Performance Metrics - Loading Phases

* Dataframe of loading metrics `collect.get_loading_time_max_all()`
    * Index is name of connection


[1] [Benchmarking Multi-Tenant Architectures in PostgreSQL](https://doi.org/10.48786/edbt.2026.46)
> Erdelt, P.K., and Rabl T. (2026)
> In: Proceedings 29th International Conference on Extending Database Technology, EDBT 2026
> OpenProceedings.org
> https://doi.org/10.48786/edbt.2026.46
