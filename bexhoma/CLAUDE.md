# bexhoma/clusters.py — development notes

## Overview

`clusters.py` is the Kubernetes cluster-management layer for Bexhoma.
It provides two public classes:

| Class | Role |
|---|---|
| `Kubernetes` | K8s cluster manager: API wrappers, component lifecycle, experiment bookkeeping, pod/job log persistence |
| `AWS` | Extends `Kubernetes` with EKS nodegroup scaling via `eksctl` |

Module-level helper: `to_unc(path)` — converts Windows drive paths to UNC
administrative share paths for `kubectl cp` on Windows.

---

## Class hierarchy

```
Kubernetes
└── AWS
```

`AWS` adds `self.cluster = self.context` (used as the EKS cluster name for `eksctl`).

---

## Constructor attributes

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

---

## Key design decisions

| Decision | Reason |
|---|---|
| `eval()` for cluster config | Config files are Python dicts, not YAML/JSON; this is a legacy format |
| Kubernetes API errors trigger `cluster_access()` retry | Short-lived kubeconfig tokens expire; auto-refresh avoids manual re-auth |
| `kubectl` subprocess fallback | Some operations (create from file, exec, cp) are simpler as CLI calls than raw API |
| `to_unc()` for Windows paths | `kubectl cp` on Windows requires UNC paths when the source is a drive-lettered path |
| `container = ''` override in `store_pod_description` / `pod_description` | `kubectl describe pod` is not container-scoped; the parameter is kept for API symmetry |
| Double-retry pattern on `ApiException` | Reconnects token and retries once; no infinite loop risk because the retry passes the same explicit arguments |

---

## `OLD_*` methods

Methods prefixed `OLD_` are deprecated legacy helpers kept for reference.
They are **not called** anywhere in the current codebase and should not be
relied upon in new code:

- `OLD_startPortforwarding` / `OLD_stopPortforwarding` — manual port-forward lifecycle
- `OLD_getChildProcesses` — psutil child enumeration (no-op body)
- `OLD__getTimediff` — pod/host clock-skew measurement
- `OLD_continueBenchmarks` / `OLD_runReporting` — legacy benchmarker flow
- `OLD_copyLog` / `OLD_copyInits` / `OLD_downloadLog` — legacy pod log copying

---

## Public name contract

Do **not** rename any public class, attribute, or method — they are referenced
by name from `configurations.py`, experiment notebooks, and external scripts.
`testbed` no longer exists; it was merged into `Kubernetes` in v0.9.6.
Internal (local variable) names may be changed freely.

---

## Style conventions

- Every class and method carries a Sphinx-style `:param` / `:type` / `:return:` / `:rtype:` docstring.
- Logger calls use `self.logger.debug(...)` — no `print()` for debug output.
- `print()` is reserved for user-visible status lines (component start/stop).
- Label-selector construction follows the pattern `label = 'app=' + app; if len(x): label += ',x=' + x`.
- Retry loops always pass keyword arguments to avoid positional-order bugs on recursion.
