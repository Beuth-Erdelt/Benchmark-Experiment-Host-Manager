# Benchmark Experiment Host Manager

In this folder is a collection of useful manifests for the components of the benchmarking experiments.

## Orchestration of Benchmarking Experiments

<p align="center">
    <img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/v0.5.6/docs/experiment-with-orchestrator.png" width="800">
</p>

For full power, use this tool as an orchestrator as in [2]. It also starts a monitoring container using [Prometheus](https://prometheus.io/) and a metrics collector container using [cAdvisor](https://github.com/google/cadvisor). For analytical use cases, the Python package [dbmsbenchmarker](https://github.com/Beuth-Erdelt/DBMS-Benchmarker), [3], is used as query executor and evaluator as in [1,2].
For transactional use cases, HammerDB's TPC-C, Benchbase's TPC-C and YCSB are used as drivers for generating and loading data and for running the workload as in [4].


## Template files

### File naming rules

Every file in this folder follows one of these naming patterns:

| Pattern | Role | How Python selects it |
|---|---|---|
| `deploymenttemplate-{DBMS}.yml` | SUT deployment for a named DBMS | `sut_template = "deploymenttemplate-" + docker + ".yml"` in `configurations/base.py` |
| `deploymenttemplate-{DBMS}-{variant}.yml` | Alternative SUT variant (e.g. `-args`) | Referenced directly from experiment scripts |
| `deploymenttemplate-bexhoma-{service}.yml` | Bexhoma infrastructure (dashboard, messagequeue, prometheus) | Applied once at cluster setup; not per-experiment |
| `daemonsettemplate-{service}.yml` | Node-level DaemonSet (monitoring/cAdvisor) | Applied once at cluster setup |
| `jobtemplate-loading-{benchmark}.yml` | Generic loading job — benchmark-level default | `experiment.jobtemplate_loading` |
| `jobtemplate-loading-{benchmark}-{DBMS}.yml` | DBMS-specific loading job (when the loader image differs per DBMS) | `experiment_dict_template["loader"][0]["template"]` |
| `jobtemplate-benchmarking-{tool}.yml` | Benchmarking job | `experiment.jobtemplate_benchmarking` |
| `jobtemplate-benchmarking-{tool}-{DBMS}.yml` | DBMS-specific benchmarking job | `experiment_dict_template["benchmarker"][*][*]["template"]` |
| `pvc-bexhoma-{name}.yml` | Global shared PVC (data, results) — static, not per-experiment | Applied once at cluster setup |
| `job-data-{benchmark}-{N}.yml` | One-time static data generation job | Applied once at cluster setup |

### Document structure

SUT deployment templates are multi-document YAML files (documents separated by `---`).
`start_sut()` in `configurations/lifecycle.py` iterates through all documents.
Each document may be one of these Kubernetes kinds:

| Kind | Required? | Notes |
|---|---|---|
| `PersistentVolumeClaim` | Optional | Removed when `use_storage=False` or `use_ramdisk=True` |
| `Service` | Optional | Removed when no matching component exists or `num_worker=0` for a StatefulSet component |
| `Deployment` | At least one required | The primary SUT container |
| `StatefulSet` | Optional | Used for distributed DBMS workers; one document per worker role |

### Label conventions

Every Bexhoma-managed resource must carry these labels on its `metadata.labels`:

| Label | Template placeholder | Runtime value | Notes |
|---|---|---|---|
| `app` | `bexhoma` | `bexhoma` | Always `cfg.appname` |
| `component` | role-dependent (see below) | **never overwritten** | `start_sut()` reads this to route each document |
| `configuration` | `default` | DBMS configuration name (e.g. `PostgreSQL`) | |
| `experiment` | `default` | unique experiment code (timestamp-based string) | |
| `client` | `default` | client-round index | Job manifests only |

The `component` label value is fixed per resource and controls how `start_sut()` names and wires each document:

| `component` value | Applied to | Effect |
|---|---|---|
| `sut` | Deployment, Service, PVC | Primary DBMS; its generated name becomes `cfg.service` |
| `storage` | PVC | DBMS-persistent storage; labels and name are computed and applied |
| `worker` | StatefulSet, Service | Worker pods; generates `BEXHOMA_WORKER_*` env vars in all containers |
| `store` | StatefulSet, Service | Store pods; generates `BEXHOMA_STORE_*` env vars |
| `pd` | StatefulSet, Service | Placement-driver pods (TiDB); generates `BEXHOMA_PD_*` env vars |
| `pool` | Deployment, Service | Connection pool (e.g. PGBouncer) |
| `loading` | Job | Loading pods |
| `benchmarker` | Job | Benchmarking pods |
| `monitoring` | DaemonSet, Service | cAdvisor per-node collection |

For every StatefulSet with `component: X`, `start_sut()` automatically injects these env vars into all containers:

| Env var | Content |
|---|---|
| `BEXHOMA_{X}_NAME` | StatefulSet name |
| `BEXHOMA_{X}_SERVICE` | Headless service name |
| `BEXHOMA_{X}_LIST` | Comma-separated DNS addresses of all pods (`{name}-{i}.{service}`) |
| `BEXHOMA_{X}_LIST_SPACE` | Same, space-separated |

(`X` is the component value uppercased, e.g. `worker` → `BEXHOMA_WORKER_NAME`.)

### Component name generation

`generate_component_name()` in `configurations/base.py` produces all runtime resource names:

```
{app}-{component}-{configuration}-{experiment}[-{experimentRun}][-{client}[-{benchmarkRun}]]
```

All lowercase. Examples:

| Use case | Example result |
|---|---|
| SUT pod and service | `bexhoma-sut-postgresql-1717000000` |
| SUT storage PVC | `bexhoma-storage-postgresql-1717000000` |
| Benchmarker job, client round 2, parallel job 3 | `bexhoma-benchmarker-postgresql-1717000000-2-3` |

Worker pods use `get_worker_name()`, which applies the same formula but draws the experiment segment from `storage_label` (or the experiment code when `worker_name_app`/`worker_name_component` overrides are set).
Worker PVCs from StatefulSet `volumeClaimTemplates` follow the fixed prefix `bxw-{worker_name}-{i}`.

The `name:` fields in templates are placeholders that `start_sut()` always overwrites — their values do not matter to the code, only their `component` label does.

### Reserved container names

Container names inside pods are fixed; `start_sut()` and the evaluator pipeline locate containers by name:

| Container name | Found in | Role |
|---|---|---|
| `dbms` | SUT Deployment/StatefulSet templates | Primary DBMS; `start_sut()` reads its `args` and manages volume mounts |
| `monitor-application` | SUT Deployment templates | Application metrics exporter (e.g. postgres-exporter); removed when app monitoring is disabled |
| `cadvisor` | SUT/worker templates (sidecar) | Node metrics; removed when cluster-level monitoring already exists |
| `dcgm-exporter` | SUT/worker templates (sidecar) | GPU metrics; removed when cluster-level monitoring already exists |
| `datagenerator` | Loading Job templates (initContainer) | Data generation before loading; logs saved as `.datagenerator.log` |
| `sensor` | Loading Job templates (main container) | Loader; logs saved as `.sensor.log` |
| `dbmsbenchmarker` | Benchmarking Job templates | Benchmarker; logs saved as `.dbmsbenchmarker.log`; **must be named `dbmsbenchmarker`** for timing extraction |
| `pool` | Connection-pool Deployment templates | PGBouncer or equivalent |

### Reserved volume names

Volume names in pod specs are matched by name in `start_sut()`:

| Volume name | Purpose | Removed when |
|---|---|---|
| `benchmark-storage-volume` | Mounts the DBMS storage PVC | `use_storage=False` |
| `benchmark-data-volume` | Mounts the shared dataset PVC | `use_distributed_datasource=False` |
| `bxw` | Worker-node storage (StatefulSet) | `use_storage=False` |
| `dshm` | Shared-memory `emptyDir` | Never removed |
| `bexhoma-results` | Results PVC (job templates) | Never removed |
| `datadir` | Ephemeral in-memory volume for generated data (loading jobs) | Never removed |

### Service port names

`start_sut()` strips Service ports by name when monitoring is inactive.

| Port name | Always kept | Notes |
|---|---|---|
| `port-dbms` | Yes | DBMS connection port |
| `port-bus` | Yes | Cluster bus port for distributed DBMSs |
| `port-web` | Yes | Web UI |
| `port-monitoring` | Stripped when monitoring inactive | cAdvisor metrics |
| `port-monitoring-application` | Stripped when monitoring inactive | Application metrics exporter |

### Global PVCs (not per-experiment)

The `claimName` values in `volumes[].persistentVolumeClaim` inside pod specs are **not overwritten** by `start_sut()`.
They must match the actual PVC names deployed once at cluster setup:

| Claim name | Content |
|---|---|
| `bexhoma-data` | Shared read-only dataset store (TPC-H/TPC-DS tables, etc.) |
| `bexhoma-results` | Writable results store; mounted by benchmarker pods |

## References

If you use Bexhoma in work contributing to a scientific publication, we kindly ask that you cite our application note [2] or [1]:

[1] [A Framework for Supporting Repetition and Evaluation in the Process of Cloud-Based DBMS Performance Benchmarking](https://doi.org/10.1007/978-3-030-84924-5_6)
> Erdelt P.K. (2021)
> A Framework for Supporting Repetition and Evaluation in the Process of Cloud-Based DBMS Performance Benchmarking.
> In: Nambiar R., Poess M. (eds) Performance Evaluation and Benchmarking. TPCTC 2020.
> Lecture Notes in Computer Science, vol 12752. Springer, Cham.
> https://doi.org/10.1007/978-3-030-84924-5_6

[2] [Orchestrating DBMS Benchmarking in the Cloud with Kubernetes](https://doi.org/10.1007/978-3-030-94437-7_6)
> Erdelt P.K. (2022)
> Orchestrating DBMS Benchmarking in the Cloud with Kubernetes.
> In: Nambiar R., Poess M. (eds) Performance Evaluation and Benchmarking. TPCTC 2021.
> Lecture Notes in Computer Science, vol 13169. Springer, Cham.
> https://doi.org/10.1007/978-3-030-94437-7_6

[3] [DBMS-Benchmarker: Benchmark and Evaluate DBMS in Python](https://doi.org/10.21105/joss.04628)
> Erdelt P.K., Jestel J. (2022).
> DBMS-Benchmarker: Benchmark and Evaluate DBMS in Python.
> Journal of Open Source Software, 7(79), 4628
> https://doi.org/10.21105/joss.04628

[4] [A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools](http://dx.doi.org/10.13140/RG.2.2.29866.18880)
> Erdelt P.K. (2023)
> http://dx.doi.org/10.13140/RG.2.2.29866.18880
