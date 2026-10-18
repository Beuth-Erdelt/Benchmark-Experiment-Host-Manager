# Plan: fewer kubectl calls when a benchmark round starts

Status: plan only (2026-10-18). Follows the parallel metric fetching
(commit 12e5546f), which cut tenancy_8 from 176 to 146 minutes.

## Goal

Starting a benchmarker job (`BenchmarkRunner.run_pod()`) takes 44-80 s per
configuration, one configuration after another. With 8 tenants each phase
starts about 6 minutes late, about 35 minutes per tenancy_8 run. Bring
`run_pod()` to about 15-20 s without changing what the pods see.

## How it works today

Every kubectl call is a new process. From the Windows host it costs about
1.5 s (measured 2026-10-18: `get` 1.3 s, `exec` into dashboard 1.5-1.7 s, into
Redis 1.4-1.6 s; client start alone 0.19 s). The kubeconfig gets its token
through an exec plugin (`users[0].user.exec.command = kubectl`), so each call
starts a second kubectl process and opens a new TLS connection to
`cl-master:6444`. Calls through the Python client (`get_pods()`) are not
affected.

Calls per `run_pod()`, counted from the code
([configurations/benchmarking.py](../bexhoma/configurations/benchmarking.py)):

| Step | Where | kubectl calls |
|---|---|---|
| volume size: `df` in the SUT pod + label on the PVC | `cfg.host.check_volumes()`, benchmarking.py:141 | 2 |
| `mkdir -p /results/{code}` in the dashboard | benchmarking.py:214 | 1 |
| upload 4 files (queries, connection, connections, protocol) | benchmarking.py:216-219 | 4 x 4 = 16 |
| Redis: `del` + one `rpush` per pod | `fill_messagequeue()`, [clusters.py:2797](../bexhoma/clusters.py#L2797) | 1 + parallelism |
| Redis: one `set` per pod config | `_push_pod_configs()` -> `set_pod_config()`, [clusters.py:2871](../bexhoma/clusters.py#L2871) | parallelism |
| Redis: job counter | `set_pod_counter()`, benchmarking.py:238 | 1 |
| create the job | `create_object_from_file()`, benchmarking.py:246 | 1 |
| **total, parallelism 1** | | **about 23-25** |

Each upload ([clusters.py:1732 `upload_file()`](../bexhoma/clusters.py#L1732))
runs `mkdir -p` (exec), `kubectl cp` to `<file>.uploadtmp`, `mv` (exec) and
`test -s` (exec): four calls, for atomicity and verification.

The end of a phase calls `config.host.check_volumes()` again
([experiments/base.py:2471](../bexhoma/experiments/base.py#L2471)), so the
volume is measured twice per phase.

The first `run_pod()` of a repetition takes 72-80 s instead of about 44 s; the
cause is not known yet (M0 finds it).

## Design

Keep every guarantee (atomic replace, verified upload, exact queue length)
and only merge calls. One milestone per mechanism, so each can be measured on
its own.

### M0 - measure

1. Count and time subprocess calls in `Kubernetes.kubectl()` and
   `execute_command_in_pod()`: a per-thread counter (call count, seconds) that
   `run_pod()` reads at its start and end. Print one line per call of
   `run_pod()`, e.g. `submitted benchmarker job in 44.1s (23 kubectl calls, 38.2s)`.
   Same line for a `MetricFetchBatch`.
2. Find what makes the first `run_pod()` of a repetition 30 s slower (candidates:
   reset script, `ensure_copy_metrics_script()` upload, loading-metric queueing,
   first `check_volumes()` on a fresh volume).

### M1 - uploads: 4 calls per file -> 2 for all files

1. `upload_files(pairs, pod, container)` in `clusters.py`: stage the files in
   a local temp folder, `kubectl cp` the folder to
   `/results/{code}/.upload-<uuid>/` (one call; `kubectl cp` creates the
   target folder), then one exec:
   `mv .upload-<uuid>/a a && mv ... && rmdir .upload-<uuid> && test -s a && ... && echo UPLOAD_OK`.
   Each `mv` is a rename on the same volume, so readers see old or new files
   only, as today. Retry the whole thing as `upload_file()` does.
2. `run_pod()` uploads its 4 files with one `upload_files()` call; the
   separate `mkdir -p /results/{code}` exec is dropped (the folder cp creates it).
3. `upload_file()` for single files: skip the `mkdir -p` when this pod and
   folder were already created in this process (cache), and merge `mv` and
   `test -s` into one exec: 4 -> 2 calls. Used by `MetricFetchBatch`,
   `end_benchmarking()` and the loader.

Saves about 15 calls per `run_pod()`.

### M2 - Redis: one exec per job

1. `fill_messagequeue()`: one exec
   `redis-cli del Q && redis-cli rpush Q 1 2 ... n`, check the returned length
   as today (retry from a cleared queue on a wrong length). n numbers in one
   `rpush` is atomic in Redis.
2. `set_pod_counter()` for the job counter and the per-pod `set_pod_config()`
   calls of one job: one exec with `redis-cli mset k1 v1 k2 v2 ...`, values
   quoted as `set_pod_config()` quotes them today. Check quoting through
   `execute_command_in_pod()` (it escapes `"` for the local shell; JSON has `"`).
   Simplest safe form: write the commands to a local file, upload it with the
   M1 path and run `redis-cli < file` in the Redis pod; or pipe through
   `sh -c` with single-quoted values, as today.

Saves `2 x parallelism` calls per `run_pod()` (2 with parallelism 1, more for
parallel loaders/benchmarkers).

### M3 - measure the volume once per phase

`run_pod()` measures the volume right before the job, `end_benchmarking()`
right after. Keep the measurement after the phase and the one before the first
phase of a repetition (needed for `volume_used` before benchmarking), skip the
`run_pod()` one for later phases. Check first which value ends up in the
connection (`volume_used` in the summary) and that the report does not change.
Saves 2 calls for every phase but the first.

### M4 - more fetches at once

`DEFAULT_MAX_PARALLEL_FETCHES` 4 -> 8
([metric_fetching.py:24](../bexhoma/metric_fetching.py#L24)). A fetch is about
4.7 s of overhead and 0.4 s of Prometheus work (dashboard metrics.py >= 0.15.2),
so 16 fetches go from about 19 s to about 10 s. Check dashboard pod CPU/RAM with
8 metrics.py processes (pandas import each).

### M5 (optional) - exec through the Python client

`execute_command_in_pod()` via `kubernetes.stream.stream(connect_get_namespaced_pod_exec, ...)`
instead of a kubectl subprocess: no second process for the token, one TLS
setup per call instead of two processes. Would make every exec about 0.2-0.5 s
instead of 1.5 s, for everything (loading, metrics, Redis). Larger change: the
outage retry (`is_cluster_connection_error`, `wait_for_cluster`), stdout/stderr
split, exit status and timeouts must keep their behaviour. Decide after M0-M2.

### M6 (optional) - submit configurations in parallel

Run the `run_pod()` calls of one loop pass in a thread pool. Needs the local
writes in `run_pod()` serialised (`connections.config`, `queries.config`,
`protocol.json` in the shared result folder; `cfg.benchmark` per configuration
is fine) and the round/experiment counters set before any job starts. Only if
M1-M3 leave too much.

## Tests

- `upload_files()`: with a stub cluster, one `cp` and one exec for n files;
  the exec moves every file and checks every file; retry on missing `UPLOAD_OK`.
- `upload_file()`: `mkdir` only on first use per pod and folder; `mv` and
  `test` in one exec.
- `fill_messagequeue()`: one exec with `del` and `rpush 1..n`; wrong length ->
  retried; `RuntimeError` after the last attempt (existing tests keep passing).
- Pod configs and counter in one exec; values with `'` and `"` survive the
  quoting (round-trip through a real `sh -c` if available, as
  `tests/test_metric_fetching.py` does for the copy script).
- M0 line printed with call count and seconds.

## Cluster check

Rerun tenancy_2 and tenancy_8 (same parameters as 2026-10-18):
- `submitted benchmarker job in` drops from about 44 s to about 15-20 s, with
  the kubectl count from M0;
- tenancy_8 total time below 146 minutes, about 120 expected;
- same set of result files, same benchmark results, no failed upload or
  queue retries in the log.

## Open questions

- **Token plugin.** Part of the 1.5 s is the exec credential plugin of this
  kubeconfig. A kubeconfig with a cached bearer token (e.g. a service account
  token for the bexhoma namespace) would make every kubectl call cheaper
  without code changes. Worth checking with the cluster admin before M5.
- **Upload staging folder name** must not clash with result files and must be
  removed even if the `mv` fails halfway (cleanup on the next attempt).
- **Order of M5 and M6.** If M5 brings exec to about 0.3 s, M6 is likely not
  needed.
