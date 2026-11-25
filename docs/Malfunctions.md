# Malfunctions and How They Are Noticed

A benchmark run has many moving parts: data generators, loader pods, scripts in the SUT, benchmarker pods, monitoring, and the Kubernetes cluster underneath.
Any of them can fail in a way that does not stop the run, but makes its numbers wrong.
This page lists such malfunctions: how each can happen, what it would mean for the result, and how bexhoma handles it.

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
`bexhoma summary -e <code>` shows the same tests later, including those found while the experiment ran (they are stored in the result folder).

Some things are expected and only reported, never a failed test:

* errors in OLTP and key-value workloads (Benchbase, HammerDB, YCSB), such as aborted transactions or failed operations: they belong to the workload and are counted;
* differences of query results: there are no reference answers for every scale factor, so results are compared between the DBMS of a run (test `No SQL warnings`).

## Data generation

| Malfunction | How it can happen | Consequence | How it is handled |
|---|---|---|---|
| Raw data generated only partly | The generator fails, runs out of disk, or its pod is evicted | The loaders read incomplete files; later runs that reuse the folder would load too few rows as well | A generator writes a completion marker only after it succeeded. Raw data without the marker is generated again, never reused |

## Loading

| Malfunction | How it can happen | Consequence | How it is handled |
|---|---|---|---|
| Rows not loaded | The DBMS rejects a load statement or reports fewer rows than the file has | Tables are smaller than they should be; queries run faster than they would on complete data | Every loader compares the reply with the file and stops with an error. Test `Loader pods without errors`; a failed loading job ends the experiment |
| A loading script fails | A schema, index, constraint or statistics statement returns an error | An index or constraint is missing, so query plans and times differ | The error lines of the DBMS client and the script's exit code are checked. Test `Init scripts without errors` |
| A script is cut off | The connection to the SUT pod breaks, or the pod goes away, while a script runs | The script stops halfway, e.g. only some indexes exist | Every script prints an end marker when it is done; a missing marker counts as failed, as does a non-zero exit code. Test `Init scripts without errors` |
| A failing command goes unnoticed inside a script | A command whose output is passed on to another command (a pipe) fails, but only the last command's result counts | The script reports success although a step failed | Script authors follow a rule for such commands, and a repository test lists every one of them, so a new one has to be checked first |
| A loader pod cannot start | The cluster has no room for it, or its image cannot be pulled | Loading waits forever, or its measured time includes the wait | The experiment ends when a loader pod cannot be scheduled or loading exceeds its timeout (`-lt`). A wait for an image is reported as a failed test, because it is part of the loading time |
| The SUT restarts during loading | The DBMS container crashes, e.g. out of memory | Data loaded so far may be lost | The load counts as failed (test `Loading completed without failures`), and its volume is never marked as loaded, so it is not reused |
| A reused volume holds other data | A persistent volume was loaded with other settings than requested | The run measures other data than asked for | The settings the volume was loaded with are compared with the request. Test `Data parameters as requested` |

## The SUT during the run

| Malfunction | How it can happen | Consequence | How it is handled |
|---|---|---|---|
| A container of the SUT restarts | The DBMS crashes or is killed, e.g. out of memory | Caches are cold again; without a data volume, the database is empty after the restart | Restarts are counted per repetition, with the reason. Tests `No SUT container restarts` and `SUT data survived container restarts` |
| The SUT pod is replaced | The pod is evicted, rescheduled or deleted, and Kubernetes starts a new one | The benchmark continues against a different pod: empty, or with an interrupted load | bexhoma notes which pod it loaded and checks it at the start of every round and at the end of every repetition. A replaced pod is not loaded again; the experiment ends. Test `SUT pods not replaced` |
| A pod terminated on purpose | A benchmark that measures recovery terminates a pod or container | Same as above | Treated like any other replacement or restart: the tests fail |

## Benchmarking

| Malfunction | How it can happen | Consequence | How it is handled |
|---|---|---|---|
| A benchmarker pod fails | The pod crashes or is evicted; Kubernetes may start a replacement | Without care, the replacement would run as a second copy of another client, and one client would never run | Each benchmarker pod takes its client number from a queue; a replacement finds the queue empty and stops. Tests `Benchmarker pods without errors` and `Results of all benchmarker pods`, which names the missing clients |
| A benchmarker pod leaves no result | Its log is lost or cut, or it ended before it printed a result | Throughput is summed over fewer pods than planned, and the total looks plausible | Every planned pod must have a result. Test `Results of all benchmarker pods` |
| A pod ran shorter than configured | The benchmark tool ended early | Throughput over a shorter time is not comparable | Compared with the configured duration (Benchbase, HammerDB) or number of operations (YCSB). Tests `Every pod ran for the configured time`, `Execution Phase: every pod ran its configured operations` |
| HammerDB virtual users fail | A virtual user cannot connect or ends with an error | The workload runs with fewer users than planned | Test `No virtual user FINISHED FAILED`. Transaction errors are counted only |
| Queries fail | A query of TPC-H, TPC-DS or SSB returns an error | The query is missing from the totals | Tests `No SQL errors` and the check that every active query is in the totals |
| Results differ between DBMS | A DBMS returns another result set for the same query | One of them computes something else | Test `No SQL warnings` (result mismatch) |
| No or zero throughput | The benchmark ran, but measured nothing | Results are empty | Tests on the main metrics: `... contains no 0 or NaN` |
| The workflow differs from the plan | A round was skipped, or more or fewer pods ran | The result describes another experiment | Test `Workflow as planned` |
| A round cannot start | Benchmarker pods cannot be scheduled in time | The round would wait forever | The round is skipped after a timeout, with a failed test |
| A reset before a round fails | A reset script (`-ar`) returns an error | The round starts from another state than the others | Test `Reset scripts ran without errors` |

## Monitoring

| Malfunction | How it can happen | Consequence | How it is handled |
|---|---|---|---|
| A metric is missing | Prometheus returns no data for a query | The metric is filled with zeros and looks like an idle component | The fetch reports each missing metric. Test `No monitoring metrics missing`; gaps with a known reason (e.g. a phase shorter than the scrape interval) are skipped or a warning |
| No monitoring data at all | Monitoring did not work in this run | No resource numbers for the run | Test `Monitoring returned data` |
| CPU of a component is zero | The component was not measured, or idle | Resource numbers per component are wrong | Test `... contains no 0 or NaN in CPU [CPUs]`, skipped for phases too short to be measured |

Not noticed: one component without any data while others have data, and a fetch of metrics that failed before it queried anything.

## Results and the experiment

| Malfunction | How it can happen | Consequence | How it is handled |
|---|---|---|---|
| A pod log cannot be stored | The log could not be read from the cluster after several attempts | Results or diagnostics of that pod are missing | Failed test `Pod log stored: <file>` |
| A pod log has no start or end time | The pod ended before it printed them | Timings of that job are missing | Failed test `Start and end time in pod log <file>` |
| The experiment hits its time limit | `--experiment-timeout` ends a run that takes too long | Parts of the plan did not run | Failed test `Experiment ended by --experiment-timeout ...` |
| Host information is incomplete | A probe in the SUT pod finds no value, e.g. a missing tool in the image | Results lack the hardware they ran on | Warning `Host information incomplete (...)` |
| A result folder has no summary | Its workload type belongs to no benchmark | Nothing is evaluated | Failed test `No summary: workload type ... belongs to no benchmark` |
| An experiment ends before its first result | Loading failed before any benchmark ran | Nothing to evaluate | A short summary with the tests that explain why: scripts, loader pods, the reason the experiment ended |
