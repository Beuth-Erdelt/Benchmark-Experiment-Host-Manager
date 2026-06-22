# bexhoma/ — development notes

---

## clusters.py

### Overview

`clusters.py` is the Kubernetes cluster-management layer for Bexhoma.
It provides two public classes:

| Class | Role |
|---|---|
| `Kubernetes` | K8s cluster manager: API wrappers, component lifecycle, experiment bookkeeping, pod/job log persistence |
| `AWS` | Extends `Kubernetes` with EKS nodegroup scaling via `eksctl` |

Module-level helper: `to_unc(path)` — converts Windows drive paths to UNC
administrative share paths for `kubectl cp` on Windows.

### Class hierarchy

```
Kubernetes
└── AWS
```

`AWS` adds `self.cluster = self.context` (used as the EKS cluster name for `eksctl`).

### Constructor attributes

All instance attributes are declared in `Kubernetes.__init__`.  Key groups:

| Group | Attributes |
|---|---|
| Kubernetes API clients | `v1core`, `v1apps`, `v1batches` (set by `cluster_access()`) |
| Context / network | `context`, `contextdata`, `host`, `port`, `namespace`, `appname` |
| Config | `config` (dict, loaded via `ast.literal_eval()` from the cluster config file) |
| Folder paths | `yamlfolder`, `experiments_configfolder`, `resultfolder` |
| Experiment selection | `change_instance`, `instance_key`, `volume_key`, `volume`, `docker_key`, `docker`, `script_key`, `initscript` |
| Experiment catalog | `instance`, `instances`, `volumes`, `dockers` (set by `set_experiments()`) |
| Workload params | `resources`, `ddl_parameters`, `connectionmanagement`, `querymanagement`, `workload` |
| Monitoring flags | `monitoring_active`, `monitor_app_active`, `monitor_cluster_active`, `monitor_cluster_exists` |
| Experiment bookkeeping | `code`, `experiments`, `benchmark`, `queryfile`, `timeLoading`, `max_sut` |

### Key design decisions

| Decision | Reason |
|---|---|
| `eval()` for cluster config | Config files are Python dicts, not YAML/JSON; this is a legacy format |
| Kubernetes API errors trigger `cluster_access()` retry | Short-lived kubeconfig tokens expire; auto-refresh avoids manual re-auth |
| `kubectl` subprocess fallback | Some operations (create from file, exec, cp) are simpler as CLI calls than raw API |
| `to_unc()` for Windows paths | `kubectl cp` on Windows requires UNC paths when the source is a drive-lettered path |
| `container = ''` override in `store_pod_description` / `pod_description` | `kubectl describe pod` is not container-scoped; the parameter is kept for API symmetry |
| Double-retry pattern on `ApiException` | Reconnects token and retries once; no infinite loop risk because the retry passes the same explicit arguments |

### `OLD_*` methods

Methods prefixed `OLD_` are deprecated legacy helpers kept for reference.
They are **not called** anywhere in the current codebase and should not be
relied upon in new code:

- `OLD_startPortforwarding` / `OLD_stopPortforwarding` — manual port-forward lifecycle
- `OLD_getChildProcesses` — psutil child enumeration (no-op body)
- `OLD__getTimediff` — pod/host clock-skew measurement
- `OLD_continueBenchmarks` / `OLD_runReporting` — legacy benchmarker flow
- `OLD_copyLog` / `OLD_copyInits` / `OLD_downloadLog` — legacy pod log copying

### Public name contract

Do **not** rename any public class, attribute, or method — they are referenced
by name from `configurations/`, experiment notebooks, and external scripts.
`testbed` no longer exists; it was merged into `Kubernetes` in v0.9.6.
Internal (local variable) names may be changed freely.

### Style conventions

- Every class and method carries a Sphinx-style `:param` / `:type` / `:return:` / `:rtype:` docstring.
- Logger calls use `self.logger.debug(...)` — no `print()` for debug output.
- `print()` is reserved for user-visible status lines (component start/stop).
- Label-selector construction follows the pattern `label = 'app=' + app; if len(x): label += ',x=' + x`.
- Retry loops always pass keyword arguments to avoid positional-order bugs on recursion.

---

## configurations/ (subpackage)

### Overview

`configurations/` is a subpackage that defines the DBMS configuration layer for Bexhoma
experiments via **composition**.  `configurations.py` no longer exists; import paths remain
the same (`from bexhoma import configurations`).

The module-level alias `configurations.default = SutConfiguration` is kept for backward
compatibility with all entry scripts.

### Files

| File | Contents |
|---|---|
| `__init__.py` | Re-exports all public symbols; defines `default = SutConfiguration` alias |
| `base.py` | `SutConfiguration` — the primary class; all `__init__` attributes, `set_*`/`patch_*`/`add_*` helpers, worker-naming methods, direct pod helpers |
| `status.py` | `ComponentStatus` — SUT/monitoring/loading/maintaining readiness predicates |
| `host.py` | `HostProbe` — `get_host_*` and `check_volumes()` methods |
| `manifest.py` | `ManifestBuilder` — YAML template creation for loading/benchmarking jobs; module-level helpers `find_workloads`, `ensure_arg_pairs`, `patch_container` |
| `metrics.py` | `MetricsCollector` — Prometheus metric fetching |
| `loading.py` | `LoadingCoordinator` — loading pod lifecycle; module-level `load_data_asynch` thread function |
| `benchmarking.py` | `BenchmarkRunner` — benchmarker pod lifecycle (`run_pod()`) |
| `lifecycle.py` | `LifecycleManager` — SUT start/stop, monitoring, port-forward; contains `start_sut()` |

### Composition pattern

Each helper class is instantiated in `SutConfiguration.__init__` and holds a
`self._config` back-reference to the owning `SutConfiguration`:

```python
self.status  = ComponentStatus(self)
self.host    = HostProbe(self)
self.lifecycle = LifecycleManager(self)
self.loader  = LoadingCoordinator(self)
self.runner  = BenchmarkRunner(self)
self.metrics = MetricsCollector(self)
self.manifest = ManifestBuilder(self)
```

Call sites in `experiments/base.py` use the helper attributes:
`config.lifecycle.start_sut()`, `config.loader.start_pod(...)`, `config.runner.run_pod(...)`, etc.

### Branching attributes for DBMS-specific behaviour

Rather than monkey-patching methods in entry scripts, `SutConfiguration` provides three
instance attributes that change the behaviour of existing methods:

| Attribute | Default | Effect when set |
|---|---|---|
| `worker_name_app` | `''` | `get_worker_name()` uses this instead of `self.appname` and also substitutes `experiment_name` for `storage_label` |
| `worker_name_component` | `''` | `get_worker_name()` uses this as the component label |
| `worker_metric_strip_container` | `False` | `set_metric_of_config()` strips the `container="dbms"` PromQL filter (YugabyteDB) |

`statefulset_name` (declared in `__init__`, not new) causes `get_worker_pods()` to call
`cluster.get_stateful_set_pods()` and `get_worker_endpoints()` to return bare pod names.

Entry scripts set these attributes instead of defining `types.MethodType` monkey patches.

### Constructor attributes

All instance attributes of `SutConfiguration` are declared in `SutConfiguration.__init__`.
`reset_sut()` is called from `__init__` and resets a subset of attributes —
this is intentional; the attributes are still declared in `__init__` first.

Key attribute groups:

| Group | Attributes |
|---|---|
| Identity | `experiment`, `docker`, `configuration`, `code`, `appname`, `path`, `alias` |
| Templates | `dockertemplate`, `sut_template`, `jobtemplate_loading`, `jobtemplate_maintaining` |
| Scripts | `script`, `initscript`, `indexing`, `indexscript` |
| Component parameters | `resources`, `ddl_parameters`, `eval_parameters`, `storage`, `nodes`, `connectionmanagement`, `loading_parameters`, `maintaining_parameters`, `sut_parameters`, `benchmarking_parameters` |
| Patch dicts | `loading_patch`, `benchmarking_patch` |
| Scaling | `num_worker`, `num_loading`, `num_maintaining`, `num_loading_pods`, `num_maintaining_pods`, `num_tenants`, `tenant_per` |
| Monitoring flags | `monitoring_active`, `monitor_app_active`, `maintaining_active`, `loading_active`, `loading_deactivated`, `monitor_loading`, `monitoring_sut` |
| Timing | `timeLoading`, `timeGenerating`, `timeIngesting`, `timeSchema`, `timeIndex`, `timeLoadingStart`, `timeLoadingEnd`, `loading_timespans`, `benchmarking_timespans` |
| State | `is_sut_ready`, `are_worker_ready`, `loading_started`, `loading_finished`, `experiment_done` |
| Deployment bookkeeping | `deployment_infos`, `statefulset_name`, `sut_service_name`, `sut_pod_name`, `volumeid`, `service` |
| Benchmark sequencing | `benchmark_list`, `benchmark_list_template`, `benchmarking_parameters_list`, `benchmarking_parameters_list_template`, `client`, `connection`, `current_benchmark_start`, `current_benchmark_connection` |
| DBMS branching | `worker_name_app`, `worker_name_component`, `worker_metric_strip_container` |
| SUT throttling | `max_sut_dbms` — max concurrent SUT pods with the same `dbms` label allowed in the cluster; `None` means no limit |

### Key design decisions

| Decision | Reason |
|---|---|
| `reset_sut()` called from `__init__` | Centralises the "no load yet" state so that the same method can be called to restart cleanly mid-experiment |
| `add_benchmark_list()` populates `benchmark_list` | The list is consumed as a queue during the benchmark sequence; the template copy allows future reconstruction |
| `storageConfiguration` local variable in several methods | Dict key `self.storage['storageConfiguration']` is a string; the local variable of the same camelCase name is intentional to match the dict key — do **not** rename the local variable without also renaming the dict key everywhere |
| YAML patching via `hiyapyco` | Deep-merges experiment-level patches onto the base job template without rewriting the template |
| `load_data_asynch` is a module-level function | It is executed in threads; making it a standalone function avoids holding a reference to `self` across thread boundaries |

### `OLD_*` methods

Methods prefixed `OLD_` are deprecated legacy helpers kept for reference.
They are **not called** anywhere in the current codebase:

- `OLD_prepare` — legacy per-config SUT startup
- `OLD_start` — legacy per-config data load

### Public name contract

Do **not** rename any public class, attribute, or method — they are referenced
by name from `experiments.py`, experiment notebooks, and external scripts.
Internal (local variable) names may be changed freely, **except** the camelCase
local variable `storageConfiguration` (see design decisions above).

### Style conventions

- Every class and public method carries a Sphinx-style docstring.
- `self.logger.debug(...)` for internal tracing; `print(...)` for user-visible status.
- All instance attributes are declared in `__init__` before first use, even those
  later overwritten by `reset_sut()` or `set_*` / `patch_*` helpers.
- Attribute comments use `#:` (Sphinx autodoc) so they appear in generated docs.

---

## Pod synchronization counters

All Kubernetes pods (generators, loaders, benchmarkers) synchronize their start using
Redis count-down counters before executing their workload.  The mechanism was redesigned
in issue #720 to eliminate race conditions between multi-configuration experiments.

### Semantics

Python initializes each counter to its target `N`.  Each pod decrements the counter by 1
on startup, then polls until the value is `<= 0`.  Using `<= 0` instead of `== 0` makes
the mechanism restart-safe: a restarted pod that decrements again drives the counter
further negative, but the wait condition is still satisfied immediately.

### Three counter levels

| Level | Scope | Key format |
|---|---|---|
| **Job** | All pods within one Kubernetes Job | `bexhoma-{type}-podcount-job-{CONNECTION}-{EXPERIMENT}` |
| **Round** | All benchmarker pods within one configuration's client round (e.g. query stream + refresh stream) | `bexhoma-benchmarker-podcount-round-{EXPERIMENT_RUN}-{CLIENT}-{CONFIGURATION}-{EXPERIMENT}` |
| **Experiment** | All pods of all configurations in the same phase; container tenancy only | `bexhoma-{type}-podcount-exp-{EXPERIMENT}` |

`{type}` is `benchmarker`, `loader`, or `generator`.  `{CONNECTION}` maps to
`self.configuration` / `$BEXHOMA_CONNECTION`.  `{EXPERIMENT}` maps to `self.code` /
`$BEXHOMA_EXPERIMENT`.

The round counter key is unique per `(EXPERIMENT_RUN, CLIENT, CONFIGURATION, EXPERIMENT)` quad.
The `CONFIGURATION` segment scopes the counter to a single SUT so that benchmarkers of
different parallel configurations never share a round counter. The remaining fields prevent
stale values from one round affecting the next (the core fix for #720).

### Rules per pod type

**Benchmarker pods** always wait for all three counters, in order:

1. Job counter — unconditional.
2. Round counter — unconditional.
3. Experiment counter — only when `BEXHOMA_TENANT_BY=container`.

**Loader pods** wait conditionally on `BEXHOMA_SYNCH_LOAD > 0`:

1. Job counter.
2. Experiment counter — only when `BEXHOMA_TENANT_BY=container`.

**Generator pods** wait conditionally on `BEXHOMA_SYNCH_GENERATE > 0`
(TPC-H/TPC-DS) or `BEXHOMA_SYNCH_LOAD != 0` (YCSB, Benchbase):

1. Job counter.
2. Experiment counter — only when `BEXHOMA_TENANT_BY=container`.

The experiment counter for generators uses the `generator-podcount-exp` key;
for loaders (including the YCSB generator which does `ycsb load`) it uses the
`loader-podcount-exp` key.

### Python initialization points

| Counter | Method | Value |
|---|---|---|
| Loader job counter | `configurations/loading.py::LoadingCoordinator.start_pod()` | `num_pods` |
| Generator job counter | `configurations/loading.py::LoadingCoordinator.start_pod()` | `num_pods` |
| Benchmarker job counter | `configurations/benchmarking.py::BenchmarkRunner.run_pod()` | `parallelism` |
| Round counter | `experiments/base.py::work_benchmark_list()` at `config.client > self.client` | Sum of `parallelism` across all configs for this round |
| Loader/generator experiment counter | `experiments/base.py::work_benchmark_list()` when all container-tenancy configs are ready to load | Sum of `num_loading_pods` across all active configs |
| Benchmarker experiment counter | `experiments/base.py::work_benchmark_list()` at `config.client > self.client`, when `self.tenant_per == 'container'` | Same as round counter value |

The loader and generator experiment counters are both initialized to `total_loading_pods`
so that each key can be independently decremented by its own pod type without one type's
counter interfering with the other's.
