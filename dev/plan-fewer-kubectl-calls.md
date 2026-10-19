# Plan: fewer kubectl calls when a benchmark round starts

Status: M0-M4 and M7-M14 implemented and committed 2026-10-18 (`9152423e`,
`7ebfc8dd`), unit tests in `tests/test_fewer_calls.py`; cluster check done
(see "Cluster check"). M6 implemented and committed 2026-10-19 (`f3d8f6bb`,
then the exec client pool and the init pod fix), cluster check done: tenancy_8 88.8 ->
78.7 min, SUT idle between rounds 212 -> 114 s (see "M6: result"). M15
(repetition boundaries side by side) planned 2026-10-19, not implemented. M5
and the optional section not done. Note
2026-10-18: `extend` never took effect (`configurations/metrics.py` read
`grafanaextend`); it is now read and defaults to 0, so O1's `time_end +
extend` is `time_end` unless a cluster sets it. Deviations from the text below:
- M7: no awk at all for `disk`/`datadisk` (`df -m /`, `du -Ls` parsed in
  Python like awk's `NR == 2{print $3}` / `END{print $1}`), instead of the
  `$` variant on the API path. Found on the way: from the Windows host the
  old `\$` variant made awk fail (`unexpected character '\'`); `disk` then
  fell back to the `$` variant, but `datadisk` returned 0 without fallback,
  so **`datadisk` was 0 in every run from Windows**. It now has its value.
- M8 reuses the static values only if the first measurement found RAM, CPU,
  cores, kernel and node.
- M12: `reset_sut()` and the other resets run right after `stop_sut()` (as
  the plan's step 1 for the rest), only the start waits; `_waits_for_slot()`
  counts a configuration whose SUT is being removed as waiting, so a kept
  SUT under `-ms` cannot block its restart.
- M11: the row "after `_prepare_next_repetition()`" became "SUT removal
  noticed as done" (M12 no longer blocks).
- M2: Redis `set`/`mset`/refill/`get` also go through the API exec (each is
  safe to repeat), not only merged.
- M14 throttles the client's own hook (passed on at most every 60 s or 30 s
  before the JWT `exp`) instead of running `ExecProvider` itself; the hook
  re-registers itself on reload, the wrapper puts itself back in front.
- M3: `check_volumes()` reuses the SUT pod's `df` from the host info and
  skips a PVC label write with unchanged values; the labels are only read by
  `bexperiments` (status), not by the results.

Measured after M14 from the Windows host (read-only, dashboard pod): API
request 0.08 s (was 0.6 s), exec through the API 0.27 s (kubectl 1.6-2.1 s),
10 x `get_pods()` 0.9 s (was 5.6 s); pod reads and probe outputs equal to
the kubectl versions.

Cluster check 2026-10-18 (same parameters as the reruns of that morning; other
experiments ran on cl-worker36 and nvme at the same time; logs in
`dev/logs_fewer_calls/`):

| | before | after |
|---|---|---|
| tenancy_2 total | 76.5 min | 59.3 min |
| tenancy_8 total | 145.6 min | 88.8 min |
| submit a benchmarker job (median) | 44 s | 12 s |
| SUT idle between rounds, tenancy_2 / tenancy_8 (median) | 202 s / 663 s | 94 s / 212 s |
| result files tenancy_2 / tenancy_8 | 1689 / 6393 | 1689 / 6393 |

Every job ended once, no upload/queue/token retries, same test outcome
(only "Monitoring metrics missing", as before), host info identical except
`datadisk` (now set). Loading times unchanged; the loading metric window is
shorter (it ended with bexhoma's detection of the loader's end). Unthrottled
TPC-C throughput about 10% lower in both (tenancy_8 mean 3426 vs 3810
requests/s), light rounds identical: other experiments on the same node, or
the shorter idle time between rounds; needs a run on a quiet cluster. YCSB
Citus (3 workers, nvme, `-nc 2`): worker host info per pod, volumes reused,
non-blocking removal; found and fixed a duplicate `env` key in the Citus
worker template, OOM of workers at 16Gi (docs runs now `-lr/-rr 64Gi`), and
`pg_isready` without `-U` logging `role "root" does not exist`.

Plan written 2026-10-18. Follows the parallel metric fetching
(commit 12e5546f), which cut tenancy_8 from 176 to 146 minutes. Extended
2026-10-18 with host info probes, idle time of the main loop and the cost of
one loop pass (M7-M13, see "Order" at the end). Revised the same day: M14
(token cache for the Python client, measured), M7 through the Python client
exec, M11 as short waits after own steps instead of a watcher.

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
`cl-master:6444`.

The Python client (`get_pods()` etc.) is affected too (measured 2026-10-18,
kubernetes client 22.6.0, from the Windows host): every request takes
0.55-0.8 s (`read_namespaced_pod` 0.55 s, `list_namespaced_pod` 0.6-0.8 s,
exec through `kubernetes.stream` 0.75 s), because the client runs the token
plugin (`kubectl oidc-login get-token`, one subprocess) before **every**
request. Reason: the client treats a token as expired 5 minutes before its
`expirationTimestamp` (`EXPIRY_SKEW_PREVENTION_DELAY`), and the OIDC tokens
seem to live about 5 minutes (one had 2.5 minutes left when fetched), so
every token is "expired" as soon as it is issued. With the refresh hook
disabled, the same calls take 0.08 s (`read_namespaced_pod`) and 0.26 s
(exec). See M14.

| Call (from the Windows host) | today | with token cache (M14) |
|---|---|---|
| kubectl exec / get | 1.6-1.8 s | 1.6-1.8 s (kubectl runs the plugin per process) |
| Python client request | 0.55-0.8 s | 0.08 s |
| Python client exec (`kubernetes.stream`) | 0.75 s | 0.26 s |

Calls per `run_pod()`, counted from the code
([configurations/benchmarking.py](../bexhoma/configurations/benchmarking.py)):

| Step | Where | kubectl calls |
|---|---|---|
| host info of the SUT pod: `get_host_all()` (15-17 execs + `kubectl get pod -o json`) | `get_connection_config()`, [metrics.py:137](../bexhoma/configurations/metrics.py#L137) | 15-17 per pod, again for every worker and pool pod (see M7) |
| volume size: `df` in the SUT pod + label on the PVC | `cfg.host.check_volumes()`, benchmarking.py:141 | 2 |
| `mkdir -p /results/{code}` in the dashboard | benchmarking.py:214 | 1 |
| upload 4 files (queries, connection, connections, protocol) | benchmarking.py:216-219 | 4 x 4 = 16 |
| Redis: `del` + one `rpush` per pod | `fill_messagequeue()`, [clusters.py:2797](../bexhoma/clusters.py#L2797) | 1 + parallelism |
| Redis: one `set` per pod config | `_push_pod_configs()` -> `set_pod_config()`, [clusters.py:2871](../bexhoma/clusters.py#L2871) | parallelism |
| Redis: job counter | `set_pod_counter()`, benchmarking.py:238 | 1 |
| create the job | `create_object_from_file()`, benchmarking.py:246 | 1 |
| **total, parallelism 1, single-pod SUT** | | **about 38-42** (the first count, 23-25, missed the host info) |

Each upload ([clusters.py:1732 `upload_file()`](../bexhoma/clusters.py#L1732))
runs `mkdir -p` (exec), `kubectl cp` to `<file>.uploadtmp`, `mv` (exec) and
`test -s` (exec): four calls, for atomicity and verification.

The end of a phase calls `config.host.check_volumes()` again
([experiments/base.py:2471](../bexhoma/experiments/base.py#L2471)), so the
volume is measured twice per phase.

The first `run_pod()` of a repetition takes 72-80 s instead of about 44 s; the
cause is not known yet (M0 finds it).

Outside `run_pod()` the main loop `work_benchmark_list()`
([experiments/base.py:1931](../bexhoma/experiments/base.py#L1931)) loses time
in three ways (details in M9-M12):

- **Waiting.** Every pass starts with `wait(30)`. Each step bexhoma itself
  causes is seen one pass later: a job ends, is noticed 0-30 s later, is
  ended and deleted, the next round is submitted one pass later (or two, if
  the deleted job is still listed). A round transition costs 30-60 s plus
  pass time.
- **Blocking.** `_prepare_next_repetition()` waits in 30 s steps until a
  stopped SUT is gone, inside the pass. No other configuration is served
  meanwhile, and with N tenants the removals run one after another.
- **Pass cost.** A pass makes roughly 15 Python client requests per
  configuration (status checks of SUT, monitoring, loader, jobs), each
  0.55-0.8 s today: about 10 s per configuration and pass, over a minute with
  8 tenants (estimate, M0 measures). Status checks also call kubectl in places
  (2 per `get_pod_containers()`, `get_pod_restart_counts()`,
  `get_pod_waiting_reasons()`), `get_pod_status()` lists all bexhoma pods of
  the namespace to find one, and finished pods of a running job are inspected
  again in every pass.

## Safety rules (all milestones)

The point is less overhead, not different measurements. Each milestone must
keep:

1. **Same values.** A merged or cached call returns what the separate calls
   returned (same parser, same fallbacks, same value on a missing pod). Tests
   compare old and new code on recorded outputs.
2. **Same outage handling.** kubectl calls go through `kubectl()` /
   `execute_command_in_pod()` (outage budget); Python client calls through
   the clients of `_new_api_client()` (urllib3 retries, timeout) with the
   usual `ApiException` handling. No new call path without one of them.
3. **Same order where it matters.** Files read by a later step (connection
   config before the metric fetch, results before deletion of a job) are in
   place before that step, as today.
4. **Pauses with a purpose stay.** The 30 s loop wait stays the default.
   Shorter waits are only allowed after bexhoma's own steps whose next step
   needs no outside change (M11), so the time between a job's end and its
   metric fetch does not change, nor `delay_prepare` and the readiness
   checks.
5. **Fallback instead of gaps.** If a merged call fails as a whole (e.g. no
   markers in the output), fall back to the old per-call path; never store
   empty host info or skip a file.

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
   first `check_volumes()` on a fresh volume, first `du` of the data
   directory in `get_host_all()`).
3. Count Python client requests too: the `request_with_timeout()` wrapper in
   `_new_api_client()` ([clusters.py:403](../bexhoma/clusters.py#L403)) is the
   hook (count, seconds).
4. Per loop pass, one debug line: pass duration, kubectl calls, API requests,
   seconds in `wait()`.
5. Idle time per transition, from timestamps in the log: job end
   (`BEXHOMA_END` of the last pod) -> `end_benchmarking()` -> next
   `run_pod()` of that configuration; `stop_sut()` -> SUT gone; time spent in
   `_prepare_next_repetition()`.

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

With M7 `get_host_all()` measures the same `df` a moment before
`check_volumes()` in `run_pod()`. For the SUT deployment, label the PVC with
those values instead of a second `df` (statefulset pods: same, per pod).
Only if both use the same mount path (`get_data_paths()`); else keep the call.

### M4 - more fetches at once

`DEFAULT_MAX_PARALLEL_FETCHES` 4 -> 8
([metric_fetching.py:24](../bexhoma/metric_fetching.py#L24)). A fetch is about
4.7 s of overhead and 0.4 s of Prometheus work (dashboard metrics.py >= 0.15.2),
so 16 fetches go from about 19 s to about 10 s. Check dashboard pod CPU/RAM with
8 metrics.py processes (pandas import each).

### M5 (optional) - exec through the Python client

`execute_command_in_pod()` via `kubernetes.stream.stream(connect_get_namespaced_pod_exec, ...)`
instead of a kubectl subprocess. Measured: 0.26 s per exec with M14, 0.75 s
without, against 1.6-1.8 s for kubectl. M7 builds the transport
(`execute_command_in_pod_api()`) for the read-only host probes first; M5 then
moves the other execs (metrics, uploads, logs) to it. Not the scripts of
`load_data_asynch()` and reset scripts (decided 2026-10-18): they are not safe
to repeat, can run for hours, and run in parallel threads already; a
websocket that drops mid-script would lose the exit status. Larger change for
those: the outage retry (`is_cluster_connection_error`, `wait_for_cluster`),
stdout/stderr split, exit status, timeouts and `retry_interrupted` (commands
not safe to repeat) must keep their behaviour. Decide after M7 has run on the
cluster for a while.

### M6 (optional) - submit configurations in parallel

Run the `run_pod()` calls of one loop pass in a thread pool. Needs the local
writes in `run_pod()` serialised (`connections.config`, `queries.config`,
`protocol.json` in the shared result folder; `cfg.benchmark` per configuration
is fine) and the round/experiment counters set before any job starts. Only if
M1-M3 and M7 leave too much.

**Why it was done (2026-10-19).** After M0-M14, tenancy_8 still spent about
3.5 minutes per round transition (`dev/logs_fewer_calls/tenancy_8.log`):
the pass ending 8 jobs took 96 s (about 77 s of it the 8 `end_benchmarking()`
calls one after another, 19 s fetches), the pass submitting the next round
122 s (8 `run_pod()` of 8-17 s each, 20 s follow-up actions). Passes without
transitions take about 10 s. The SUT idle time between rounds (median 212 s)
is mostly these two passes.

**M6: result.** Module `bexhoma/parallel_steps.py`:
- `run_steps(steps, max_workers)`: one step per configuration in a thread
  pool; `ExperimentBase.max_parallel_steps` (default 8, no CLI flag, as
  `max_parallel_fetches`); 1 runs them one by one in the loop thread, as
  before. Every step runs to its end; the first error (in configuration
  order) is raised afterwards.
- First loop: the counters (round, experiment) are set in the loop as before;
  the submission itself (reset script, parameters, `run_pod()` per entry,
  start timer of the round) becomes `_submit_round()` /
  `_submit_legacy_round()`, collected and run after the loop, before
  `submit_batch.run()`.
- Second loop: the body per configuration became `_end_finished_jobs()`
  (store pods, `end_benchmarking()`, delete job, `check_volumes()`), run
  side by side; the follow-up waits (M11) and the flags are combined in the
  loop thread.
- Shared result files: `result_files_lock()` (RLock) around the
  read-change-write of `connections.config`, `protocol.json`,
  `experiments.config` and `queries.config` in `run_pod()`, around the
  `connections.config` update in `end_benchmarking()` and around the
  evaluator (it keeps counters).
- Upload order: `run_pod()` uploads through `upload_result_files()`
  (`OrderedUpload`): one upload at a time, requests that arrive meanwhile are
  merged into the next one, and a request returns only after an upload that
  started after its write. The pod never gets an older `connections.config`
  after a newer one, and 8 submissions need about 2 uploads instead of 8.
- `MetricFetchBatch.add_fetch()` / `add_after()` under a lock;
  `CALL_STATS.snapshot/since(own_thread=True)` so each "submitted
  benchmarker job" line counts its own calls. A line `submitted N benchmark
  rounds in Xs` / `ended N benchmarker jobs in Xs` follows when more than one
  ran.
- Not parallel: the "can be stopped" branch (`-m load` / keep-SUT
  `run_pod(only_prepare=True)`, `stop_sut()`), loading, starts.
- Changes for the results: the order of connections in `connections.config`
  follows the order the submissions reach the lock (was configuration
  order). Log lines of several configurations interleave.
- Tests: `ParallelStepsTest` in `tests/test_fewer_calls.py`.
- Found in the first cluster run (2026-10-19, 1792401429): submitting 8
  rounds took 47.8 s instead of about 15 s, "224 API requests 218 s".
  Plain API requests scale with threads (48 x `read_namespaced_pod`: 3.76 s
  one by one, 0.67 s from 8 threads, 0.076 s each either way), API execs did
  not: one exec client per cluster object behind `_exec_lock` (needed,
  `stream()` swaps the request method of its client), so the ~15 host info
  execs per tenant queued (8 threads: 1.3x, 3.15 s per exec incl. waiting).
  Fix: `_take_exec_client()` / `_return_exec_client()`, a free list of exec
  clients (the first is `self.v1exec`, more only for execs at the same time,
  reused across passes, dropped after `cluster_access()`); the lock only
  guards the list. Measured with bexhoma's path: 8 threads 2.1x, 0.28 s per
  exec, same outputs. The rest is the exec itself (kubelet, websocket).
  Tests in `ExecApiTest`. Cluster check: see below.
- Also fixed: the first loop looked up init job pods with `configuration`,
  which only the old job-end loop set (to the last configuration of the
  previous pass); since M6 it was undefined (NameError at the first loading
  pass, run 1792401119). Now `config.configuration`. (Init pod logs of all
  tenants were stored before too, see the cluster check.)

Expected: tenancy_8 round transition from about 220 s to about 60 s (fetch
and follow-up batches stay); no change with one configuration.

Cluster check 2026-10-19 (tenancy_8 as on 2026-10-18, run 1792410057 with
M6 and the exec client pool, log `dev/logs_fewer_calls/tenancy_8_m6.log`):

| | 2026-10-18 (1792337757) | M6 (1792410057) |
|---|---|---|
| total | 88.8 min | 78.7 min |
| SUT idle between rounds (median, min-max) | 212 s (190-221) | 114 s (96-121) |
| submit 8 rounds, first / second round of a repetition | ~100 s | 28-35 s / 15-35 s |
| end 8 jobs | ~77 s | 20-29 s |
| result files | 6393 | 6393 |
| connections in `connections.config` | 48, all with timespans | 48, all with timespans |

Every job ended once (48), tests as before (only "Monitoring metrics
missing", the CPU throttling metrics), `datadisk` set everywhere. One joint
upload (repetition 2, round 2) could not be verified on its first attempt and
succeeded on the second; the 10 s retry held up the other 7 submissions of
that pass (34.9 s instead of about 15 s). First round of a repetition: about
13 more host info execs per tenant (fresh SUT pods, static values measured
once per pod UID) plus the first PVC label write. Init pod logs: stored for
all 8 tenants in both runs, so the old `configuration` name did not lose
them in practice. Still sequential: the pass that stops the 8 SUTs between
repetitions (101-113 s, 40 kubectl calls; "can be stopped" branch), and
three more passes per repetition (start SUTs, start loading, loading end):
see M15.

### M7 - host info through the Python client exec, getters stay modular

`get_host_all()` ([host.py:414](../bexhoma/configurations/host.py#L414))
runs one exec per value: RAM, CPU, GPU, GPU ids, cores, kernel, disk,
datadisk (`du`), volume (`df`), cuda (twice, host.py:441 and 445), hugepages
total and free, cpu list, plus `kubectl get pod -o json` for the node. `disk`
and `datadisk` first try `awk '{print \$3}'` and fall back to `$3` on an
exception, so they can take 2 execs each. That is 15-17 calls, about 25 s,
per pod. `get_connection_config()` calls it for the SUT pod and for every
worker and pool pod, so a SUT with 3 workers (Citus, YugabyteDB) spends about
60 calls, 100 s, in every `run_pod()`.

Approach: keep one getter per value, as today, and make each call cheap by
changing only the transport. Every getter goes through
`self._config.execute_command_in_pod_sut()`, so this is one switch point.
bexhoma already runs exec through the Python client in
[environment.py:579](../bexhoma/environment.py#L579) (`kubernetes.stream`,
command as an argument list, no shell).

1. **Transport** `Kubernetes.execute_command_in_pod_api(command, pod, container)`
   in `clusters.py`, returning `("", stdout, stderr)` like
   `execute_command_in_pod()`:
   - `stream(connect_get_namespaced_pod_exec, ..., command=['sh', '-c', command],
     stdout=True, stderr=True, _preload_content=False)`, then
     `run_forever(timeout=...)`, `read_stdout()` / `read_stderr()`
     separately (as environment.py does; preloaded content would parse JSON
     output).
   - Its own `CoreV1Api` / `ApiClient` (`self.v1exec`): `stream()` swaps
     `api_client.request` for the duration of the call, so it must not share
     the client of normal requests.
   - The websocket does not use urllib3's `Retry`. Own retry loop: on a
     connection error before the command ran (handshake failed,
     `ApiException` with status 0 / 5xx) wait with `wait_for_cluster()`
     within `CLUSTER_OUTAGE_BUDGET_SECONDS`; on 401 `cluster_access()` once
     and retry. The probes are read-only, so a retry after a broken
     connection is safe too.
   - If it still fails, or the client cannot exec at all: fall back to
     `execute_command_in_pod()` (kubectl) for this call. Worst case is the
     speed of today.
2. **Probes use it.** `HostProbe` gets `_exec(command)` that calls the API
   transport and falls back to kubectl. Only `HostProbe` uses it at first;
   all other execs stay on kubectl until M5.
3. **Quoting.** There is no local shell on this path, so the `\$` variants in
   `get_host_diskspace_used()` and `get_host_diskspace_used_data()` would
   reach awk as `\$3`, fail and fall back to the `$` variant (2 calls). On
   the API path use the `$` variant directly; keep the `\$` variant for the
   kubectl fallback. Commands containing `"` no longer need escaping.
4. **Node** from `read_namespaced_pod()` (`spec.node_name`) instead of
   `kubectl get pods/<pod> -o=json`; `get_host_cuda()` once (the second call
   at host.py:445 writes the same key).
5. **Same values.** Same commands, same parsers, same stdout. Check once on
   the cluster: kubectl and API transport give the same `get_host_all()` dict
   for a SUT pod (disk, datadisk and volume may drift a little).

Cost: with M14 about 15 x 0.26 s = 4 s per pod instead of about 25 s; a SUT
with 3 workers about 16 s instead of 100 s. Without M14 about 12 s per pod.

Optional, only if M0 still shows host info as large after this (e.g. many
workers): run all probes in **one** exec (measured: 0.8-1.0 s for all probes
in one call without M14). Keeps modularity with a probe registry: each value
is a `(command, parser)` entry, the getter runs its one entry, `probe_all()`
runs all entries in one exec with a marker line (`echo @@BXH:<key>@@`) before
each block and gives each block to its parser. A failing command (no
`nvidia-smi`) gives an empty block, mapped to today's value; output without
markers -> getters one by one.

### M8 - host info: static values once per pod

RAM, CPU, cores, kernel, node, GPU, GPU ids, cuda, hugepages total and cpu
list do not change while a pod lives. Cache them per pod **UID** (from
`read_namespaced_pod()`), not per name: a StatefulSet pod keeps its name when
it is recreated, possibly on another node. Measure in every round only disk,
datadisk, volume size/used and hugepages free. `cpu list`
is the cpuset of the container; bexhoma does no in-place resize, so it is
static too (drop it from the cache if that ever changes).

Saves 10 of 15 probe calls per pod in later rounds (about 2.5 s per pod with
M14), so only after M7 if M0 still shows host info as large.

### M9 - status calls without kubectl and without listing all pods

1. `get_pod_status()` ([clusters.py:740](../bexhoma/clusters.py#L740)) lists
   every pod with `app=bexhoma` in the namespace (all running experiments)
   and searches the name. Use `read_namespaced_pod(pod)`; return '' on 404
   and when the pod's `app` label is not `app` (as today, where such a pod is
   not in the list). It is called many times per pass and per configuration.
2. One `read_namespaced_pod()` instead of kubectl jsonpath calls in
   `get_pod_containers()` (2 calls), `get_pod_restart_counts()` (2),
   `get_pod_waiting_reasons()` (2) and `HostProbe.get_host_restarts()` (1).
   Same return values: containers in spec order then init containers;
   restart counts as `{name: int}`; `get_host_restarts()` as the
   space-separated string kubectl jsonpath gives, through
   `clean_restart_counts()`; a missing pod -> [] / {} / '' as today.
   Where it matters:
   - `_note_image_pull_waits()` runs `get_pod_waiting_reasons()` for every
     loading pod in every pass while loading: 3 s per pod and pass, 24 s per
     pass with 8 tenants or 8 parallel loader pods.
   - "can be stopped" calls `store_previous_pod_logs()` (restart counts, 2),
     `get_host_restarts()` (1) and `get_pod_restart_counts()` (2) per SUT and
     worker pod, all reading the same counts: read the pod once, pass the
     counts on.
3. `kubectl logs` and `kubectl describe` stay (describe has no client
   equivalent with the same text; the logs are the results).

With M14 a `read_namespaced_pod()` costs 0.08 s instead of 1.6-1.8 s per
kubectl call it replaces.

### M10 - remember stored job pods

In the second loop of `work_benchmark_list()`
([experiments/base.py:2413](../bexhoma/experiments/base.py#L2413))
`pod_log_exists(p)` is asked without a container, so it looks for
`{pod}.log`; logs are stored as `{pod}.{container}.log`, so the check is
always false. In every pass and for every pod of a running job this calls
`get_pod_status()`, and for every finished pod `get_pod_containers()`
(2 kubectl calls) again; `store_pod_log()` then skips the existing files.
`loader.check()` ([loading.py:619](../bexhoma/configurations/loading.py#L619))
does the same for finished pods of a running loading job.

Keep a set of pods (per process) whose logs of all containers and whose
description were stored, and skip those pods in later passes. A finished pod
does not change any more (a failed pod is replaced by a new pod with a new
name), so nothing is missed. The final pass when the job succeeded stays as
it is (stores all, deletes the pods).

### M11 - main loop: short wait after own steps, 30 s otherwise

The loop keeps waiting 30 s per pass. A branch may shorten **only the next**
wait, when the step it just did needs no outside change before the next step
(no pod has to start, become ready or finish). The pass logic stays.

Mechanism, using the existing variable at
[experiments/base.py:1963-1969](../bexhoma/experiments/base.py#L1963):
`intervals_wait = intervals` is set right after the wait, so a branch later
in the pass can lower it for the next wait only:

```python
self.wait(intervals_wait)
intervals_wait = intervals
...
# in a branch that is safe to follow up quickly
intervals_wait = self._follow_up_wait(intervals_wait, SHORT_WAIT_SECONDS, "job ended")
```

Goal: the idle time of the SUT between two benchmark rounds as short as
possible, without wake on change (decided 2026-10-18).

`_follow_up_wait(current, seconds, reason)` returns `min(current, seconds)`,
logs the reason (debug), and counts short waits in a row: after
`MAX_SHORT_WAITS_IN_A_ROW` (3) it returns `intervals`, so a state that does not
resolve never turns into a tight loop. All follow-up waits are 0 s.

**Ended jobs are remembered.** A deleted job vanishes from `get_jobs()`
asynchronously. Today the 30 s wait hides that; with 0 s the next pass can
still list it, and then (a) the first loop sees "jobs present" and does not
submit, (b) the second loop would end it a second time (pods, logs,
`end_benchmarking()`, metric fetch, upload). So: `self._jobs_ended` (set of
job names), filled right after `delete_job()` and after a skipped round;
both loops ignore listed jobs in this set. Job names are unique per
experiment (they contain run, client and benchmark index), so the set never
needs clearing. This makes the 0 s wait safe and also removes a latent
double end today (a job still listed 30 s after deletion).

Branches that may shorten (all others keep 30 s):

| Site | Step just done | Next step | Next wait |
|---|---|---|---|
| second loop, after `end_benchmarking()` + `delete_job()` ([base.py:2469](../bexhoma/experiments/base.py#L2469)) | job ended, results stored, job deleted, name in `_jobs_ended` | submit the next round, or "can be stopped" | 0 s |
| `_skip_benchmark_round_if_not_started()` returned True ([base.py:2206](../bexhoma/experiments/base.py#L2206)) | stuck round deleted, names in `_jobs_ended` | next round | 0 s |
| after `stop_sut()` + `_prepare_next_repetition()` ([base.py:2353](../bexhoma/experiments/base.py#L2353)) | SUT gone (waited for), configuration reset | start the next SUT, with the `-ms` checks | 0 s |
| with M12: SUT removal noticed as done, `reset_sut()` | same | same | 0 s |

The first-loop branch "`_active_jobs` all complete"
([base.py:2209](../bexhoma/experiments/base.py#L2209)) needs no own rule: such
a job is ended by the second loop of the same pass, which sets 0 s.

**What remains of the idle time** between the end of round k and the start of
round k+1 of one configuration, and what reduces it:

| Part | Today | After | Reduced by |
|---|---|---|---|
| job end -> noticed | 0-30 s | 0-30 s | nothing (needs wake on change, not wanted) |
| rest of the pass up to `end_benchmarking()`, then that | pass time | about 1/8 with M14 | M14, M9, M10, M13 |
| wait to the next pass | 30 s | 0 s | M11 |
| next pass up to this configuration, reset script, `run_pod()` | pass + 44 s | pass + about 10 s | M14, M7, M1, M2 |
| job pods start, benchmarker waits for all pods | external | external | - |

So from about 90-120 s today to about 15-45 s, still random through the
detection delay.

Keep 30 s for: `start_sut()`, "is pending", monitoring start/wait, health
check waits, "not before" (`delay_prepare`), loading running, a job just
submitted (its pods have to start), benchmarks running, SUT still being
removed. The loop's own extra pass after a submission
(`_benchmark_just_submitted`) also keeps 30 s.

What changes for results:
- **Not affected:** the time from a job's end to its detection (still 0-30 s
  plus pass time, as today), so the metric fetch in `end_benchmarking()` sees
  Prometheus as today (no scrape-lag risk); `delay_prepare`; readiness checks;
  the `-ms` checks before a start.
- **Shorter, on purpose:** the idle time of the SUT between two benchmark
  rounds (table above). It was never controlled and stays random through the
  detection delay. Results of runs before and after are therefore not
  exactly comparable for DBMS that do background work between rounds
  (checkpoints, compaction, vacuum); note it in the release notes.

Timeouts are all wall clock (`-xt`, `BENCHMARK_START_TIMEOUT_MINUTES`,
loading abort), none counts passes; check this again when implementing.

Expected: about 30 s less per round transition and configuration from M11
alone, about 30 s less per repetition transition.

### M12 - SUT removal between repetitions without blocking the loop

`_prepare_next_repetition()`
([experiments/base.py:1878](../bexhoma/experiments/base.py#L1878)) waits in
30 s steps until the stopped SUT is gone, inside the pass. Meanwhile no job
end is processed, no other SUT starts, and with 8 tenants the stops run one
after another: tenant 2's `stop_sut()` starts when tenant 1's pods are gone.

1. After `stop_sut()`, do the immediate part as today (`benchmark_list`
   copies, `self.client = 0`), set `config.sut_removing = True` and go on.
2. At the top of the per-configuration loop: while `sut_removing` and
   `status.sut_exists()`, print "still being removed" and `continue`; once
   gone, `reset_sut()`, `sut_removing = False`, `continue`. The next pass
   starts the SUT through the normal path.
3. `sut_removing` keeps `do` true (already true: repetitions pending).

Safety: the `-mse` / `-ms` / `max_sut_dbms` checks still run before the next
start (see the `-ms` repetition gap fix, 4a04da2a). Terminating pods are still
phase `Running`, so they count against the caps while they go - conservative,
as today. The skip at the top must come before `sut_running()`: a terminating
SUT looks running and healthy (`is_sut_ready` is only reset by `reset_sut()`).
Check container tenancy (`tenant_per == 'container'`) separately.
Fallback if this is too much: keep blocking, poll every 5 s.

### M13 - one upload per pass at the end of jobs

`end_benchmarking()` uploads `<connection>.config` and `connections.config`
(2 x 4 kubectl calls) per job, one job after another in the second loop.
`connections.config` is shared and rewritten for each job that ends in this
pass. Collect the files of all jobs ended in the pass and upload them with
one `upload_files()` (M1) after the last `end_benchmarking()` and before
`end_batch.run()` (the fetches read `<connection>.config` in the pod). Same
files in the pod before the same step as today. 8 jobs ending together: 64 ->
2 calls.

### M14 - token cache for the Python client

Every Python client request runs the token plugin (see "How it works
today"): 0.55-0.8 s per request instead of 0.08 s. This affects every
`get_pods()`, `get_jobs()`, `get_pod_status()`, ... in every pass, and the
exec transport of M7.

The client's hook (`kube_config.py`, `_set_config()` -> `_refresh_api_key`)
reloads the token when `expiry - 5 min <= now`. With tokens that live about
5 minutes this is always true.

1. In `_new_api_client()` ([clusters.py:381](../bexhoma/clusters.py#L381)),
   replace `configuration.refresh_api_key_hook` with an own hook. It runs the
   plugin itself (`kubernetes.config.exec_provider.ExecProvider`, as the
   client does), sets `configuration.api_key['authorization']`, and keeps the
   token until the first of:
   - `expirationTimestamp - TOKEN_EXPIRY_MARGIN_SECONDS` (30 s), when the
     plugin reports an expiry (it does: measured 2026-10-18);
   - `TOKEN_REFRESH_SECONDS` (60 s) after it was fetched.
   The plugin (`kubectl oidc-login`) keeps its own token cache and refresh
   token, so it hands out the cached token until that is about to expire. At
   most one plugin run per minute and client instead of one per request.
   Only for kubeconfigs with an `exec` user; other users keep the client's
   hook.
2. A lock around the reload: the hook may be called from several threads
   (today the metric fetch threads use kubectl, but M5/M7 must not race).
3. On 401 Unauthorized: reload and retry once. The `ApiException` handlers
   already call `cluster_access()`, which builds new clients with a fresh
   token; check that the exec transport of M7 does the same (a 401 on the
   websocket handshake).
4. The `exec` section of the kubeconfig user is read with the public loader
   API where possible; pin the behaviour with a test, since `ExecProvider`
   and the hook are client internals that may change with the client version.

Safety: a token is never used closer than 30 s to its expiry, and never
longer than 60 s after it was fetched. A request that still gets 401 (e.g.
token revoked) is refreshed and retried as today. kubectl is not affected
(each process runs the plugin itself); only the Python client gets faster.

Expected (estimate from the per-call times): a loop pass with 8 tenants from
about a minute to about 10 s; every Python client call in `run_pod()` 7x
faster; the M7 exec 0.26 s instead of 0.75 s.

### M15 - repetition boundaries side by side (planned 2026-10-19)

**Why.** After M6 a round transition with 8 tenants takes about 1 minute, but
every repetition still has four passes that handle the tenants one after
another (`tenancy_8_m6.log`, per repetition, 8 tenants):

| Pass | Time | kubectl | Where |
|---|---|---|---|
| A stop SUTs ("can be stopped") | 101-113 s | 40 | first loop, `else` branch: pod logs, previous logs, describe, restart counts, `stop_sut()`, `_prepare_next_repetition()` |
| B start SUTs | 106-113 s | 8 | `config.lifecycle.start_sut()`; with `-rsrp` each waits >= 10 s for its PVC to go ([lifecycle.py:633-643](../bexhoma/configurations/lifecycle.py#L633)) |
| C start loading (container tenancy, "is not loaded yet") | 106-133 s | 40 | "#### Starting to load": `start_exec()` + `start_pod()` per tenant |
| D loading ended + index start | 138-151 s | 64 | `config.loader.check()` per tenant, then "#### Starting to index" |

About 8 minutes per repetition, 23 of the 79 minutes of tenancy_8. D's index
start is G3 of [plan-shorter-phase-gaps.md](plan-shorter-phase-gaps.md); not
repeated here.

**How.** As in M6: the **decisions** stay in the loop thread, in
configuration order (caps, who keeps its SUT, who waits for whom); only the
**work** per configuration is collected and run with `_run_parallel_steps()`
at the end of the first loop, before the submissions.

- **M15a - stop (A).** `_leaves_sut_running()` / `_waits_for_slot()` decide in
  the loop (they look at other configurations). The rest of the branch
  becomes `_stop_repetition(config)`: store logs (current, previous),
  descriptions, restart snapshot file, `stop_sut()`, count the repetition,
  `_prepare_next_repetition()` or `experiment_done`. Writes per configuration
  only (own files, own counters); `self.workload['sut_stopped'/'sut_service']`
  are dict assignments of distinct keys. `-m load` (`run_pod(only_prepare=True)`)
  already uses the M6 lock and ordered upload. Expected: about 100 s -> 15-20 s.
- **M15b - start (B).** The cap checks (`-ms`, `-mse`, `max_sut_dbms`) and
  their optimistic pending counters stay in the loop, exactly as today; the
  `start_sut()` call itself is deferred. The 8 PVC removals then wait their
  10 s at the same time. Check before: `start_sut()` writes its manifest per
  configuration (file names), `delete_pvc`/`get_pvc` per PVC, the shared
  `storage_label` of PVC names (one per tenant: `postgresql-<i>-8-...`).
  Expected: about 110 s -> 20-25 s.
- **M15c - start loading (C).** The "all tenants ready" decision stays; the
  inner `for config_tmp in self.configurations: start_exec(); start_pod()`
  runs side by side. `load_data()` already starts its scripts in a thread;
  check `start_pod()` (loader manifest per job, Redis queue per job; the
  experiment-wide loader counters are set before, in the loop) and the init
  script uploads (`upload_file` per SUT pod). Only container tenancy has more
  than one configuration here; single configurations are unchanged.
  Expected: about 115 s -> 20-30 s.
- **M15d - loading end (D without the index start).** `config.loader.check()`
  per configuration at the top of the first loop (end the loader job, timing,
  PVC labels, `end_loading()`): run the checks of all configurations whose
  loading is running side by side at the start of the pass, then the loop
  reads their results. Coordinate with G3 (same pass). Expected: together
  with G3 about 145 s -> 30 s.

**Not changed:** what the pods and the SUT see; the order of decisions; the
caps. Each step is a single configuration's own work.

**Risks.**
- Several SUTs start at the same moment on the same node (they did within
  about 90 s before). Image pulls, PVC provisioning and scheduling run in
  parallel; under `-ms` nothing changes (caps decided before).
- More concurrent kubectl processes (up to 8): each gets slower (seen in
  M6: ~3 s instead of 1.6 s), but the pass gets shorter.
- Interleaved log lines of several tenants (as in M6).
- Results: loading of tenants starts closer together (container tenancy
  already waits for all tenants; the spread of loader starts was ~90 s,
  it gets smaller). Loading times per tenant may change slightly with more
  overlap; they are in the results.

**Tests.** Stub configurations: decisions in configuration order, work in
steps; a cap reached by the first start still blocks the second (counters
set in the loop); `_stop_repetition` keeps the repetition counters and
`experiment_done` as today; `max_parallel_steps = 1` gives today's order.

**Cluster check.** tenancy_8 as before: the four passes of the table above
per repetition; total time (expected about 15 minutes less, ~63 min); same
result files (6393), tests, `connections.config`; no SUT started beyond `-ms`
in a run with `-ms 4`.

**Order.** M15a and M15b first (largest, simplest: no shared files), then
M15c, then M15d together with G3.

### Not worth it (checked)

- `get_pods()` for the SUT 3 times and for the dashboard twice per
  `run_pod()`, `monitoring_running()` up to 3 times per configuration and
  pass: Python client, cheap after M14.
- `stop_sut()` deletes deployments, services and statefulsets through kubectl
  (about 1.5 s each), once per repetition. Goes with M5 if at all.
- Start/stop waits on PVC removal (`lifecycle.py:637`, `:1131`, 10 s polls):
  needed, once per repetition.

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
- M7: `execute_command_in_pod_api()` with a stub stream: stdout and stderr
  separate; connection error -> retried within the budget; 401 ->
  `cluster_access()` and one retry; still failing -> kubectl fallback.
  `HostProbe` on the API path uses the `$` awk variant (one call per value),
  on the kubectl fallback the old variants. `get_host_all()` gives the same
  dict on both transports for recorded outputs; `get_host_cuda()` once.
  Optional registry: `probe_all()` = getters on the same outputs; no markers
  -> getters one by one.
- M8: cache hit for the same UID, miss for the same name with a new UID;
  volatile values measured every time.
- M9: `get_pod_status()` on a pod of another app -> ''; 404 -> ''. Each
  converted getter returns the same value as the kubectl version on one
  recorded pod JSON (multi-container, init containers, restarts, waiting).
- M10: a finished pod of a running job is inspected once over several
  passes; logs of all containers and the description are stored.
- M11: stub loop: after `end_benchmarking()` + `delete_job()`, a skipped
  round and a finished `_prepare_next_repetition()` the next wait is 0 s, in
  every other branch 30 s; after 3 short waits in a row 30 s again. A job
  that is still listed after deletion is neither ended twice nor blocks the
  next submission (`_jobs_ended`); the next round is submitted in the pass
  right after the end.
- M14: hook runs the plugin once for many requests; again after 60 s or
  30 s before the reported expiry, whichever comes first; 401 -> refresh and
  retry once; non-exec kubeconfig keeps the client's hook; concurrent calls
  run the plugin once (lock).
- M12: stub cluster with a SUT that takes 3 passes to vanish: other
  configurations are served meanwhile, the SUT is not restarted while it
  exists, the `-ms` check runs before the restart.
- M13: two jobs ending in one pass -> one upload with both connection files
  and `connections.config`, before the batch fetch.

## Cluster check

Rerun tenancy_2 and tenancy_8 (same parameters as 2026-10-18):
- `submitted benchmarker job in` drops from about 44 s to about 15-20 s, with
  the kubectl count from M0;
- tenancy_8 total time below 146 minutes, about 120 expected;
- same set of result files, same benchmark results, no failed upload or
  queue retries in the log.
- `hostsystem` in `connections.config` equal to a run before the change for
  the same SUT (RAM, CPU, cores, node, GPU, cuda, hugepages, cpu list; disk,
  datadisk and volume within normal drift); also for a SUT with workers
  (Citus).
- Log shows no wait after job ends and repetition ends, `30s` otherwise
  (M11); idle time between rounds (last `BEXHOMA_END` of round k to first
  `BEXHOMA_START` of round k+1) about 15-45 s; each job ended once (one
  "showing benchmarker times" per job); metric curves of a phase reach its
  end, as before.
- No 401 / "Create new access token" in a run of several hours (M14); a pass
  with 8 tenants takes about 10 s (M0 line).
- tenancy_8 with `-nc 2`: the 8 SUTs of repetition 1 are removed in parallel
  (M12), no SUT starts beyond `-ms`.
- Pass duration from M0 before/after M9 and M10.

## Open questions

- **Token plugin.** Part of the 1.6 s per kubectl call is the exec
  credential plugin of this kubeconfig (M14 only helps the Python client). A
  kubeconfig with a cached bearer token (e.g. a service account token for
  the bexhoma namespace) would make every kubectl call cheaper without code
  changes. Worth checking with the cluster admin before M5.
- **Token lifetime.** Check the OIDC access token lifetime with the admin
  (looks like 5 minutes); M14's rules assume more than 90 s.
- **Upload staging folder name** must not clash with result files and must be
  removed even if the `mv` fails halfway (cleanup on the next attempt).
- **Order of M5 and M6.** If M5 brings exec to about 0.3 s, M6 is likely not
  needed.

## Order

By gain per risk:

1. M0 (measure) and M14 (token cache: small change, speeds up every Python
   client call and the pass).
2. M7 (host info, largest part of `run_pod()`), M9 and M10 (pass cost; same
   values, low risk).
3. M11 (short waits after own steps), M12 (repetitions of many tenants).
4. M1, M2, M13 (uploads, Redis).
5. M3, M8, M4.
6. M5, M6 only if still needed.
7. Optional section below only on request.

## Optional (not planned): wake on change, and the metric tail

Decided 2026-10-18: not part of this plan; the loop keeps its 30 s wait
(M11 shortens it only after own steps). Kept here for later.

### O1 - check the metric tail of today (worth doing on its own)

The metric window of a phase ends at `time_end + extend`
(DBMS-Benchmarker
[monitor.py:312-319](../../DBMS-Benchmarker/dbmsbenchmarker/monitor.py#L312);
`extend` is 20 s in the shipped `k8s-cluster.config`, check the cluster's
config). Prometheus has a sample about one scrape interval (15 s on the
cluster) after it happened. So the data of a window is complete about
`extend + 2 x scrape interval` (35-50 s) after the job's end. Today the
fetch in `end_benchmarking()` runs 0-30 s plus pass time after the end, so
a job noticed early may already miss part of the tail: Prometheus returns
fewer points, means barely change, max or last values can. M11/M14 make
passes faster but do not change the detection delay, so they do not make
this worse.

Check: for some finished runs, compare the last timestamp in the metric CSVs
of a phase with `time_end + extend`, against the time the fetch ran (log).
If the tail is cut: queue a fetch until `now >= time_end + extend + 2 x scrape
interval` (deferred to a later pass; before the experiment ends, wait for
deferred fetches). The job's end, deletion and the next round do not wait
for it.

### O2 - wake on change

**When it applies.** After M11 every remaining 30 s wait is a wait for an
outside change, noticed 0-30 s late (15 s on average):

| Waiting for | How often | Seen late today | With wake on change |
|---|---|---|---|
| benchmark job ends | every round | 0-30 s | 0-5 s |
| SUT pod pending -> running -> ready (workers, pool, monitoring) | every repetition, 2-3 steps | 0-30 s each | 0-5 s each |
| loading job ends | every repetition | 0-30 s | 0-5 s |
| stopped SUT gone (with M12) | every repetition | 0-30 s | 0-5 s |
| `delay_prepare` (60 s) over | every repetition | effectively 60-90 s | 60 s (only with 4. below) |

**How.**
1. `self.wait(intervals_wait)` becomes
   `self._wait_for_change(intervals_wait, snapshot, deadline)`: sleeps in 5 s
   steps; each step one `list_namespaced_job` and one `list_namespaced_pod`
   for this experiment (about 0.16 s with M14, 1.4 s without).
2. Snapshot at the end of a pass: per job succeeded/failed/conditions; per
   relevant pod phase, Ready, `deletionTimestamp`, existence. Relevant pods:
   SUT, workers, pool, monitoring, loader (not benchmarker pods starting,
   to avoid extra passes).
3. Returns early on a difference, at the earliest pending deadline, else
   after the full wait. If a check fails, sleep the rest of the wait.
4. Optional: also wake at `loading_after_time`. Not recommended: the
   effective `delay_prepare` becomes shorter than today (60 s instead of
   60-90 s), and a DBMS whose value was chosen with the 30 s rhythm may then
   be checked earlier than its authors assumed.

**Labels: not all pods carry `experiment=<code>`.**
- bexhoma's own Deployments, StatefulSets (workers,
  [lifecycle.py:969-976](../bexhoma/configurations/lifecycle.py#L969),
  labels copied to the pod template), jobs and monitoring do.
- External StatefulSets do not: YugabyteDB installed by Helm
  (`config.statefulset_name = 'yb-tserver'`, benchbase.py:621, ycsb.py:482)
  has the chart's labels (`app=yb-tserver`); bexhoma finds them through
  `get_stateful_set_pods()`
  ([clusters.py:1429](../bexhoma/clusters.py#L1429)), not through its labels.
  yb-master likewise.
- PVCs carry `experiment=<storage_label>`, not the code (not relevant for
  pods).
So the watcher must select per configuration what the status checks
select: the bexhoma labels, plus the pods of `statefulset_name` where set
(one more list call per such configuration), or watch only the bexhoma SUT
pod and accept 30 s for external workers.

Side note: `get_stateful_set_pods()` selects
`statefulset.kubernetes.io/pod-name=<stateful_set>`. That label carries the
**pod** name (`yb-tserver-0`), not the StatefulSet name, so selecting
`yb-tserver` seems to find nothing. Check on the cluster (YugabyteDB worker
info and readiness) independently of this plan.

**Safety.**
- Pass logic unchanged; only when passes run.
- Needs O1's deferred fetch: with wake on change the fetch would run about
  2.5 s after a job's end and miss the tail.
- Idle time between rounds shorter again (wanted).
- During a cluster outage one check can take longer than the wait (client
  retries up to 300 s); a pass blocks the same way today.
- API load: 2-3 list calls per 5 s per experiment.

**Expected timings** (on top of M14, M7, M11):

| | without | with wake on change |
|---|---|---|
| idle between rounds, 1 tenant | about 12-40 s | about 12-17 s |
| idle between rounds, 8 tenants ending together | about 20-50 s | about 20-25 s (rest is `run_pod()` of the others, M6) |
| per repetition (readiness, loading end, SUT removal) | about 60-75 s late | about 10-15 s |

About 12 s per round and 1 minute per repetition; with 5 rounds and `-nc 2`
about 4 minutes per experiment. Small against M14 and M7.

Tests: wait returns early on a job condition change, a relevant pod change
and a deadline; benchmarker pods starting do not wake; a failing check
sleeps the rest; external StatefulSet pods are watched where configured.

### O3 - metric fetches in the background (or at the end)

**Today.** The fetches of a pass run in a `MetricFetchBatch`
(`submit_batch.run()`, `end_batch.run()` in `work_benchmark_list()`), in
threads, but the pass waits for them: about 19 s for 16 fetches (10 s with
M4). Meanwhile no other tenant is served and the next round is not
submitted. The metric CSVs are only read at the end (`evaluate_results()`,
evaluators, report), nothing in the run uses them.

**Constraint: the per-configuration Prometheus.** Without a cluster
Prometheus, or with application metrics (`monitor_app_active`), bexhoma
starts its own Prometheus pod per configuration
([lifecycle.py:152](../bexhoma/configurations/lifecycle.py#L152)), without a
volume, and `stop_sut()` deletes it after every repetition
([lifecycle.py:1578](../bexhoma/configurations/lifecycle.py#L1578)). Its data
must be fetched before that. This component is going to be deprecated
(2026-10-18); then all metrics come from the cluster Prometheus, and a query
over a past range returns the same data whenever it runs (within retention;
vanilla Prometheus does not downsample).

**Option a: background fetches** (recommended).
1. A fetch queue with a thread pool (`max_parallel_fetches`), filled where
   `submit_batch` / `end_batch` are filled today; the pass does not wait.
2. A fetch starts only when its data is complete: `now >= time_end + extend +
   2 x scrape interval` (fixes O1).
3. Barriers: before `evaluate_results()` and in `remove_experiment()` /
   abort paths (`-xt`, loading abort, exceptions via `finally`) wait for all
   queued fetches, so finished rounds keep their metrics when a run stops
   early. While the per-configuration Prometheus still exists: also wait for
   a configuration's fetches before its `stop_sut()` (or keep today's
   blocking fetch for configurations that use it); after deprecation this
   barrier goes.
4. Order as today: `<connection>.config` is in the dashboard pod (M13
   upload) before its fetch is queued.

Gain: fetch time leaves the critical path; fetches overlap with running
benchmarks. Idle time between rounds minus the fetch time of that pass.

**Option b: all fetches at the end.** Possible only after the deprecation.
Same work, moved after the last round: for a single configuration total time
is about the same as today (only the idle time between rounds gets
shorter); with several tenants it saves the passes blocked by fetching. A
run that stops early must still fetch in `remove_experiment()` /
`finally`, and a long experiment depends on the cluster Prometheus
retention. Simpler than a, but a gets the overlap too.

**Checks.**
- Fetches now run while benchmarks run (partly already today with several
  tenants): Prometheus and the dashboard pod (metrics.py, pandas) do the
  work; check that the dashboard pod does not share a node with a SUT.
- Thread safety of the queue; fetches use kubectl only (as `MetricFetchBatch`
  today).
- Cluster Prometheus retention against the longest experiment (option b).
- Same CSVs as a run with today's blocking fetches (number of files,
  timestamps up to `time_end + extend`).

Makes M4 (8 parallel fetches) less important; replaces O1's "defer to a
later pass".
