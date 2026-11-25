# Concept: Run Integrity

A benchmark run has many moving parts: data generators, loader pods, scripts in the SUT, benchmarker pods, monitoring, and the Kubernetes cluster underneath.
Any of them can fail in a way that does not stop the run, but makes its numbers wrong.
This page lists such malfunctions: how each can happen, what it would mean for the result, and how bexhoma checks a run for it.
The last section lists malfunctions that are not noticed.

## How a run reports problems

Every summary ends with a list of tests:

```
### Tests
* TEST passed: Loader pods without errors
* TEST failed: Results of all benchmarker pods - missing: postgresql-1-1-2-1-3
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST warning: Host information incomplete (CPU)
```

* **failed**: something did not work as planned; the numbers of this run are not to be trusted as they are.
* **skipped**: the test does not apply to this run, the reason is given.
* **warning**: worth a look, but not wrong in itself.

After the summary, bexhoma prints `Test successful!` or `Tests failed: N of M`, and exits with code 1 if a test failed.
An experiment with several benchmarks prints one list per benchmark.
`bexhoma summary -e <code>` shows the same tests later, including those found while the experiment ran (they are stored in the result folder).

Most tests judge the result folder only: logs, pod and job descriptions, `connections.config`.
A test without anything to judge (e.g. no loader pod was stored, because a volume was reused) is not recorded at all.

Some things are expected and only reported, never a failed test:

* errors in OLTP workloads (Benchbase, HammerDB), such as aborted transactions: they belong to the workload and are counted;
* differences of query results: there are no reference answers for every scale factor, so results are compared between the DBMS of a run (test `No SQL warnings`).

Failed operations of YCSB are an exception: they fail the test `Execution Phase: contains no FAILED column`.

## Data generation

| Malfunction | How it can happen | Consequence | How it is handled |
|---|---|---|---|
| Raw data generated only partly | The generator fails, runs out of disk, or its pod is evicted | The loaders read incomplete files; later runs that reuse the folder would load too few rows as well | A generator writes a completion marker only after it succeeded. Raw data without the marker is generated again, never reused |

## Loading

| Malfunction | How it can happen | Consequence | How it is handled |
|---|---|---|---|
| Rows not loaded | The DBMS rejects a load statement or reports fewer rows than the file has | Tables are smaller than they should be; queries run faster than they would on complete data | Every loader compares the reply with the file and stops with an error. Test `Loader pods without errors`, which also lists each failed unit (table, file chunk); a failed loading job ends the experiment |
| YCSB rows not inserted | A YCSB thread stops at its first failed insert, while the others and the pod go on | The pod ends without error, but rows are missing | Rows inserted are compared with the scale factor. Test `Loading Phase: all rows inserted` |
| A loading script fails | A schema, index, constraint or statistics statement returns an error | An index or constraint is missing, so query plans and times differ | The error lines of the DBMS client and the script's exit code are checked. Test `Init scripts without errors` |
| A script is cut off | The connection to the SUT pod breaks, or the pod goes away, while a script runs | The script stops halfway, e.g. only some indexes exist | Every script prints an end marker when it is done; a missing marker counts as failed, as does a non-zero exit code. Test `Init scripts without errors` |
| A listed script is not in the folder | A script named in the configuration does not exist | The step is left out | Listed in the summary (`Init Scripts Not in Folder`) |
| A failing command goes unnoticed inside a script | A command whose output is passed on to another command (a pipe) fails, but only the last command's result counts | The script reports success although a step failed | Script authors follow a rule for such commands, and a repository test lists every one of them, so a new one has to be checked first |
| A loader pod cannot start | The cluster has no room for it, or its image cannot be pulled | Loading waits forever, or its measured time includes the wait | The experiment ends when a loader pod stays unschedulable for 15 minutes, when a loading job reaches the Kubernetes state `Failed`, or when loading exceeds its timeout (`-lt`). A wait for an image is a failed test, because it is part of the loading time |
| The SUT restarts during loading | The DBMS container crashes, e.g. out of memory | Data loaded so far may be lost | The load counts as failed (test `Loading completed without failures`), and its volume is never marked as loaded, so it is not reused |
| A reused volume holds an unfinished or failed load | An earlier experiment was aborted or its load failed | The run would measure partial data | The volume is refused: the SUT is not started, the experiment ends with a failed test |
| A reused volume does not fit | It is on another storage class, or was loaded for another number of workers | The run would measure another backend, or incomplete data | The volume is refused, as above |
| A reused volume holds other data | A persistent volume was loaded with other settings than requested | The run measures other data than asked for | The settings the volume was loaded with are compared with the request. Test `Data parameters as requested`; skipped when the volume has no labels for them |
| Loading times are not measured | The volume was reused, or loading was switched off (`-sl`) | The loading times are copies from another experiment, or there are none | Test `Loading measured in this experiment` is skipped with the reason |

## The SUT during the run

| Malfunction | How it can happen | Consequence | How it is handled |
|---|---|---|---|
| A container of the SUT restarts | The DBMS crashes or is killed, e.g. out of memory | Caches are cold again; without a data volume, the database is empty after the restart | Restarts are counted per repetition, with the reason. Tests `No SUT container restarts` and `SUT data survived container restarts` |
| The SUT pod is replaced | The pod is evicted, rescheduled or deleted, and Kubernetes starts a new one | The benchmark continues against a different pod: empty, or with an interrupted load | bexhoma notes the pod's UID when loading starts, at the start of every round and at the end of every repetition, for the SUT pod and every worker pod. A replaced pod is not loaded again; the experiment ends. Test `SUT pods not replaced` |
| A pod terminated on purpose | A benchmark that measures recovery terminates a pod or container | Same as above | Treated like any other replacement or restart: the tests fail |

## Benchmarking

| Malfunction | How it can happen | Consequence | How it is handled |
|---|---|---|---|
| A benchmarker pod fails | The pod crashes or is evicted; Kubernetes may start a replacement | Without care, the replacement would run as a second copy of another client, and one client would never run | Each benchmarker pod takes its client number from a queue; a replacement finds the queue empty and stops with an error. Tests `Benchmarker pods without errors` (also counts failed pods whose description is gone) and `Results of all benchmarker pods`, which names the missing clients, or a client that has two results |
| A benchmarker job fails | The job reaches the Kubernetes state `Failed` | Its pods do not all run | The job is ended like a finished one, the run goes on, with a failed test |
| A benchmarker pod starts too late | It is scheduled after the common start time of its round | It ends without running, with exit code 0 | It leaves no result. Test `Results of all benchmarker pods` |
| A benchmarker pod leaves no result | Its log is lost or cut, or it ended before it printed a result | Throughput is summed over fewer pods than planned, and the total looks plausible | Every planned pod must have a result. Test `Results of all benchmarker pods` |
| A pod ran shorter than configured | The benchmark tool ended early | Throughput over a shorter time is not comparable | Compared with the configured duration (Benchbase, HammerDB) or number of operations (YCSB). Tests `Every pod ran for the configured time`, `Execution Phase: every pod ran its configured operations` |
| HammerDB virtual users fail | A virtual user cannot connect or ends with an error | The workload runs with fewer users than planned | Test `No virtual user FINISHED FAILED`. Transaction errors are counted only |
| Queries fail | A query of TPC-H, TPC-DS or SSB returns an error | The query is missing from the totals of every DBMS of the run | Tests `No SQL errors` and `All active queries counted in the totals` |
| Results differ between DBMS | A DBMS returns another result set for the same query | One of them computes something else | Test `No SQL warnings` (result mismatch) |
| Query plans are missing | EXPLAIN was requested (`-se`), but not stored for every query | Plans cannot be compared | Test `EXPLAIN captured for every active query`; skipped without `-se` |
| No or zero throughput | The benchmark ran, but measured nothing | Results are empty | Tests on the main metrics: `... contains no 0 or NaN` (e.g. throughput, NOPM, Power@Size); for hardware benchmarks a test per tool that no round measured 0 |
| Efficiency is zero | Benchbase or HammerDB TPC-C ran without key-and-think time, or with other threads than 10 x SF | Efficiency is not defined | The efficiency test is skipped with the reason; it is tested only where it is computed |
| The workflow differs from the plan | A round was skipped, ran twice, ran another benchmark, or a repetition is missing | The result describes another experiment | Test `Workflow as planned`: configurations, repetitions, rounds, and the benchmark and planned number of pods of each job. The pods that really ran are counted by `Results of all benchmarker pods` |
| A round cannot start | Benchmarker pods cannot be scheduled in time | The round would wait forever | The round is skipped after 15 minutes, with a failed test; the other rounds go on |
| A reset before a round fails | A reset script (`-ar`) returns an error | The round starts from another state than the others | Test `Reset scripts ran without errors` |

## Monitoring

| Malfunction | How it can happen | Consequence | How it is handled |
|---|---|---|---|
| A metric is missing | Prometheus returns no data for a query | The metric is filled with zeros and looks like an idle component | The fetch reports each missing metric. Test `No monitoring metrics missing`; gaps with a known reason are skipped (a phase shorter than the scrape interval, pre-existing data, a series that exists only while non-zero) |
| Disk I/O of a component is missing | The container did no disk I/O, so there is no series | Plausible for an in-memory DBMS, suspicious for one on disk | A warning, when CPU of the same component has data (its pods were scraped); otherwise a failed test |
| No monitoring data at all | Monitoring did not work in this run | No resource numbers for the run | Test `Monitoring returned data` |
| CPU of a component is zero | The component was not measured, or idle | Resource numbers per component are wrong | Test `... contains no 0 or NaN in CPU [CPUs]`, skipped for phases too short to be measured |
| A required metric is switched off | `-mm` switches off CPU or memory metrics | Core resource numbers are missing | `-mm` refuses to switch off the required metrics (CPU utilization and time, memory with and without cache) |
| A job's metrics include other pods | A loader or benchmarker query selects pods of other jobs | Resource numbers of one job include another's | Each job's queries select only its own pods, by the pod names Kubernetes gives them (see below for the limits) |

## Results and the experiment

| Malfunction | How it can happen | Consequence | How it is handled |
|---|---|---|---|
| A pod log cannot be stored | The log could not be read from the cluster after several attempts | Results or diagnostics of that pod are missing | Failed test `Pod log stored: <file>` |
| A pod log has no start or end time | The pod ended before it printed them | The pod is left out of the job's timing, so the phase may look shorter | Failed test `Start and end time in pod log <file>` |
| The experiment hits its time limit | `--experiment-timeout` ends a run that takes too long | Parts of the plan did not run | Failed test `Experiment ended by --experiment-timeout ...` |
| Host information is incomplete | A probe in the SUT pod finds no value, e.g. a missing tool in the image | Results lack the hardware they ran on | Warning `Host information incomplete (...)` |
| A result folder has no summary | Its workload type belongs to no benchmark | Nothing is evaluated | Failed test `No summary: workload type ... belongs to no benchmark` |
| An experiment ends before its first result | Loading failed before any benchmark ran | Nothing to evaluate | A short summary with the tests that explain why: scripts, loader pods, the reason the experiment ended |

## Not noticed

Pods of similar names:

* **Long job names.** Kubernetes names the pods of a job `<job>-<5 characters>`, but cuts `<job>-` to 58 characters first. Jobs whose names agree in the first 58 characters (a long configuration name, differing only in repetition, round or benchmark number) get the same monitoring query, so each job's loader or benchmarker metrics include the pods of the others. The start and end times of a job are found by its full name in the log file names, so for a cut name none are found: for a benchmarker job, bexhoma prints `no timing data found for job` and fetches no monitoring for that round. No test fails.
* **Numbers 1 and 10.** Start and end times of a job are collected from the logs whose names start with the job name. Job `...-1` also takes the logs of `...-10` to `...-19`, when they are stored before it ends: ten or more loading jobs, or benchmarks of one round, running in parallel.
* **Configuration names.** The SUT's queries select pods whose name contains `<configuration>-<code>`. If one configuration name ends with another one of the same experiment (e.g. `PG-1` and `XPG-1`), the SUT metrics of the shorter one include the DBMS container of the other.
* **DBMS not managed by bexhoma.** For a system whose components bexhoma did not deploy (e.g. YugabyteDB via Helm), workers are selected by component name only and without a container filter: any other pod of the namespace with that name part counts too.

Monitoring:

* one component without any data, while others have data;
* a fetch of metrics that failed before it queried anything;
* a required metric switched off in the cluster configuration itself (`active: False`): it is not fetched, so it is not reported as missing; only `-mm` is checked;
* zeros in other columns than CPU (memory, network, disk) are not tested; only a missing series is.
