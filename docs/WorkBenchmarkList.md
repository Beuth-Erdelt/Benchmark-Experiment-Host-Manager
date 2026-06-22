# `work_benchmark_list()` — Main Workflow Loop

`work_benchmark_list()` is the central orchestration method of a Bexhoma experiment.
It drives the full lifecycle of one or more DBMS configurations from startup through
benchmarking to teardown. The method is a single `while` loop that polls Kubernetes
state every `intervals` seconds and advances each configuration through a pipeline
of phases.

**Source:** [`bexhoma/experiments/base.py:1368`](../bexhoma/experiments/base.py#L1368)

---

## Signature

```python
def work_benchmark_list(
    self,
    intervals: int = 30,
    stop_after_starting: bool = False,
    stop_after_loading: bool = False,
    stop_after_benchmarking: bool = False,
) -> None:
```

| Parameter | Default | Effect |
|---|---|---|
| `intervals` | `30` | Seconds to sleep between loop ticks |
| `stop_after_starting` | `False` | Exit after SUT is up and monitoring is ready (phase 2) |
| `stop_after_loading` | `False` | Exit after data is loaded (phase 3) |
| `stop_after_benchmarking` | `False` | Leave SUT running after all benchmarks finish; do not tear down |

---

## High-level phase overview

```
┌─────────────────────────────────────────────────────────────────┐
│  Pre-loop                                                        │
│    • Check cluster monitoring health                             │
│    • Write experiment_dict JSON files for each config            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  MAIN LOOP  (repeat every `intervals` seconds)                   │
│                                                                  │
│  Part A — for each configuration:                                │
│    Phase 1  Start SUT                                            │
│    Phase 2  Start monitoring (if needed)                         │
│    Phase 3  Wait for SUT health; start loading                   │
│    Phase 4  Start maintaining pods (if needed)                   │
│    Phase 5  Submit benchmarker job(s)                            │
│    Phase 6  Collect SUT logs; stop / restart / mark done         │
│                                                                  │
│  Part B — for each configuration:                                │
│    Harvest completed benchmarker job pods (store logs, describe) │
│    On job success: call end_benchmarking(), delete job           │
│                                                                  │
│  Loop termination check                                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Pseudocode

```
FUNCTION work_benchmark_list(intervals, stop_after_starting,
                              stop_after_loading, stop_after_benchmarking):

    # ── Pre-loop ──────────────────────────────────────────────────────────

    IF cluster monitoring is healthy:
        mark monitor_cluster_exists = True

    FOR each config IN self.configurations:
        IF config has loader or benchmarker entries:
            write experiment_dict to a JSON file in the result folder

    intervals_wait = 0          # first tick is immediate
    do = True

    # ── Main loop ─────────────────────────────────────────────────────────

    WHILE do:
        wait(intervals_wait)
        intervals_wait = intervals   # subsequent ticks use the full interval

        _benchmark_just_submitted = False

        # Count how many SUT pods are already running / pending,
        # both within this experiment and across the whole cluster.
        num_pods_running_experiment = ...
        num_pods_pending_experiment = ...
        num_pods_running_cluster    = ...
        num_pods_pending_cluster    = ...

        # ── Part A: advance each configuration through its lifecycle ───────

        FOR each config IN self.configurations:

            # ── Phase 1: Start SUT ────────────────────────────────────────

            IF SUT is NOT running:
                IF config.experiment_done:
                    CONTINUE to next config

                IF SUT is NOT pending:
                    # Respect per-experiment and per-cluster SUT limits.
                    IF max_sut limit exists (experiment or cluster):
                        we_can_start = True
                        IF running+pending >= self.max_sut:   # experiment limit
                            we_can_start = False
                            print "has to wait"
                        IF running+pending >= cluster.max_sut: # cluster limit
                            we_can_start = False
                            print "has to wait"
                        IF we_can_start:
                            config.start_sut()
                            increment pod counters
                    ELSE:
                        config.start_sut()
                        increment pod counters
                ELSE:
                    print "is pending"

                CONTINUE to next config   # SUT not ready yet; skip further phases

            # SUT is running from here on.

            # ── Phase 2 / 3: Wait for monitoring, health, then load ───────

            config.check_load_data()    # refreshes loading_started / loading_finished

            IF NOT config.loading_started:

                IF config has benchmarks AND monitoring_active AND monitoring NOT running:
                    IF monitoring NOT pending:
                        config.start_monitoring()
                    CONTINUE   # wait for monitoring

                IF SUT is running but NOT healthy:
                    print "waits for health check"
                    CONTINUE

                IF SUT workers are NOT healthy:
                    print "waits for worker health check"
                    CONTINUE

                # Respect the optional loading delay (e.g., 60 s after SUT start).
                IF config.loading_after_time is None:
                    # First time here: compute when loading may begin.
                    delay = config.dockertemplate.get('delay_prepare', 60)
                    IF delay > 0:
                        config.loading_after_time = now + delay
                        CONTINUE   # come back later
                    ELSE:
                        proceed to start loading immediately

                IF now < config.loading_after_time:
                    print "will start loading but not before <time>"
                    CONTINUE

                # Start the actual loading process.
                IF tenant_per == 'container':
                    mark config as ready-to-load
                    # Real start is deferred until ALL containers are ready (see below)
                ELSE:
                    IF config.loading_active:
                        config.start_loading()
                        config.start_loading_pod(parallelism, num_pods)
                    ELSE:
                        config.start_loading()   # schema / DDL only

            # ── Phase 4: Start maintaining pods ──────────────────────────

            IF config.loading_finished AND config has benchmarks:
                IF monitoring needed but not running:
                    start monitoring or wait
                    CONTINUE
                IF config.maintaining_active AND maintaining NOT running:
                    IF maintaining NOT pending:
                        config.start_maintaining(parallelism, num_pods)
                    ELSE:
                        print "has pending maintaining"

            # Store logs of any completed 'init' job pods.
            FOR each succeeded init pod:
                store pod log
                store pod description (if not already stored)

            # ── Tenant-per-container synchronisation ─────────────────────

            IF tenant_per == 'container' AND NOT config.loading_finished:
                IF NOT config.tenant_started_to_load:
                    IF all containers are ready-to-load:
                        FOR each container config:
                            start loading (and loading pod)
                ELIF NOT config.tenant_started_to_index:
                    IF all containers are ready-to-index:
                        FOR each container config:
                            run indexing script

            # ── Phase 5: Submit benchmarker job(s) ───────────────────────

            IF config.loading_finished:

                IF SUT not healthy (or workers not healthy):
                    CONTINUE   # wait

                # Enforce the post-load warm-up window.
                IF config.loading_after_time is None:
                    # Loaded from PVC; set delay as if loading just finished.
                    ...set loading_after_time; CONTINUE
                IF now < config.loading_after_time:
                    print "will start benchmarking but not before <time>"
                    CONTINUE

                # Do not submit a new job while any benchmarker jobs
                # (running OR succeeded-but-not-yet-cleaned-up) still exist.
                # The cleanup happens in Part B; submitting here too early
                # would corrupt the client counter sequence.
                _active_jobs = get_jobs(benchmarker)
                IF _active_jobs:
                    IF any job is still running:
                        print "has running benchmarks"
                    CONTINUE   # wait for Part B to clean up

                # --- Path A: experiment_dict-driven benchmarks ---
                IF experiment_dict has benchmarker entries AND client round exists:
                    client_round = experiment_dict["benchmarker"][config.client - 1]
                    config.client += 1
                    IF config.client > self.client:
                        reset global client counter and Redis pod-count queue

                    FOR each (benchmark_index, bench_entry) IN client_round:
                        connection_name = "<config>-<run>-<client>-<benchmark_index>"
                        IF bench_entry has parameters:
                            config.benchmarking_parameters = bench_entry["parameters"]
                        config.run_benchmarker_pod(
                            connection  = connection_name,
                            parallelism = bench_entry["parallelism"],
                            benchmark_run = benchmark_index,
                            template_override = bench_entry.get("template"),
                        )
                    _benchmark_just_submitted = True

                # --- Path B: legacy benchmark_list ---
                ELIF NOT experiment_dict path AND config.benchmark_list not empty:
                    parallelism = config.benchmark_list.pop(0)
                    client = config.client; config.client += 1
                    IF config.client > self.client:
                        reset global client counter and Redis pod-count queue
                    IF config.benchmarking_parameters_list not empty:
                        benchmarking_parameters = config.benchmarking_parameters_list.pop(0)
                        config.set_benchmarking_parameters(**benchmarking_parameters)
                    connection_name = "<config>-<run>-<client>"
                    config.run_benchmarker_pod(connection, parallelism)
                    _benchmark_just_submitted = True

                # ── Phase 6: All benchmarks done — stop or repeat ─────────

                ELSE:  # no more benchmark entries remain
                    IF NOT stop_after_benchmarking:
                        print "can be stopped"
                        # Collect SUT pod logs and descriptions.
                        FOR each deployment pod:
                            store pod log (for each container)
                            store pod description
                            log restart count
                        FOR each statefulset pod:
                            store pod log, description, restart count

                        config.stop_sut()
                        config.num_experiment_to_apply_done += 1

                        IF more repetitions remain (num_experiment_to_apply_done < num_experiment_to_apply):
                            WAIT until SUT is fully removed
                            # Reset and restart for next repetition.
                            IF NOT experiment_dict driven:
                                restore benchmark_list from template
                                restore benchmarking_parameters_list from template
                            self.client = 0
                            config.reset_sut()
                            config.start_sut()
                        ELSE:
                            config.experiment_done = True

                    ELSE:  # stop_after_benchmarking=True: leave SUT up
                        print "can be stopped, but we leave it running"
                        generate and print port-forward command
                        IF this was the first client and more repetitions remain:
                            run a prepare-only benchmarker pod
                            mark repetition as done

            ELSE:  # loading_finished is False
                print "is loading"

        # ── Part B: Harvest completed benchmarker jobs ────────────────────

        _we_have_running_benchmarks = False
        _we_have_incomplete_jobs    = False

        FOR each config IN self.configurations:
            jobs = get_jobs(benchmarker, config)
            pods = get_job_pods(benchmarker, config)

            FOR each job IN jobs:
                _we_have_running_benchmarks = True

                FOR each pod IN pods:
                    IF pod log not yet stored:
                        status = get_pod_status(pod)
                        IF status == Succeeded OR Failed:
                            store pod logs (all containers)
                            store pod description

                job_success = get_job_status(job)
                IF NOT job_success:
                    _we_have_incomplete_jobs = True

                IF job_success:
                    FOR each pod IN pods:
                        IF status == Succeeded OR Failed:
                            store pod logs and description
                            delete pod
                    end_benchmarking(job, config)   # record timing, result metadata
                    delete job
                    config.check_volumes()

        # ── Loop termination check ─────────────────────────────────────────

        IF _we_have_running_benchmarks:
            do = False   # start from "stop" assumption

            IF _benchmark_just_submitted:
                # New job may not appear in get_jobs() yet; force another pass.
                do = True

            FOR each config:
                IF SUT is pending:                        do = True
                IF not yet loaded:                        do = True
                IF still has benchmark entries to submit: do = True
                IF more repetitions pending (and not stop_after_benchmarking):
                                                          do = True
                IF stop_after_starting AND repetitions remain:
                                                          do = True

            IF _we_have_incomplete_jobs:
                do = True

        ELSE:
            # No benchmarker jobs at all in the cluster.
            # Stop only when every config has finished all repetitions.
            IF all(config.experiment_done for config in self.configurations):
                do = False
```

---

## Key design decisions

### Single polling loop over a configuration list

All configurations (`self.configurations`) are advanced in the same loop tick.
Because each phase check uses `continue`, a configuration that is blocked in an
early phase simply skips all later phases without disturbing the others.

### Separation of Part A (submit) and Part B (harvest)

The loop deliberately separates submission from harvesting within the same tick.
Part A never touches completed job objects; Part B never submits new jobs.
This avoids a race condition where a just-submitted job might be mistakenly
collected before its first pod is scheduled.

### `_benchmark_just_submitted` guard

After submitting a job, the Kubernetes API may not yet return it from
`get_jobs()`. The `_benchmark_just_submitted` flag forces at least one more
loop iteration before the termination check can set `do = False`.

### SUT pod-count gating

When `max_sut` limits are configured (per-experiment and/or per-cluster), the
loop counts running and pending SUT pods each tick and defers `start_sut()` for
any configuration that would exceed the limit.

### Loading delay (`delay_prepare`)

Before loading begins, the loop enforces a configurable warm-up window (default
60 s after SUT start). The same window is re-applied before benchmarking when a
system was loaded from a pre-existing PVC and no explicit `loading_after_time`
was recorded.

### Tenant-per-container synchronisation

When `tenant_per == 'container'`, multiple database schemas live inside a single
SUT container. Each configuration independently sets its `tenant_ready_to_load`
flag. Loading (and later indexing) only begins when **all** container
configurations report ready, ensuring a consistent data-load start point.

### experiment_dict vs. benchmark_list

Two parallel submission paths exist:

| Path | Trigger | Format |
|---|---|---|
| **experiment_dict** | `config.experiment_dict["benchmarker"]` is non-empty | Nested list of client rounds; each round is a list of `{parallelism, parameters?, template?}` dicts |
| **benchmark_list** (legacy) | `experiment_dict["benchmarker"]` is empty; `benchmark_list` is populated via `add_benchmark_list()` | Flat list of parallelism integers |

Only one path is active per configuration per run.

### Repetition (`num_experiment_to_apply`)

After all benchmarks of a single repetition are done, the SUT is stopped,
removed, reset, and restarted. The `benchmark_list` (and optionally
`benchmarking_parameters_list`) is restored from its template copy. The loop
continues until `num_experiment_to_apply_done == num_experiment_to_apply`.

---

## State flags per configuration

| Attribute | Set when |
|---|---|
| `loading_started` | `start_loading()` is called |
| `loading_finished` | `check_load_data()` confirms the load job completed |
| `experiment_done` | All repetitions of this configuration are complete |
| `client` | Incremented each time a benchmark job is submitted |
| `num_experiment_to_apply_done` | Incremented each time `stop_sut()` is called after a full benchmark sequence |

---

## Termination conditions

The loop exits (`do = False`) when one of the following is true:

1. No benchmarker jobs exist anywhere in the cluster **and** every configuration
   has `experiment_done = True`.
2. `_we_have_running_benchmarks` is `True` (jobs were seen this tick) but after
   all continuation conditions are evaluated, none of them is still `True`.
