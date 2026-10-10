# Result Contract

[`contracts/contract_result.yml`](../contracts/contract_result.yml) says what a
finished experiment's result folder contains, how its names decode, which
checks decide whether a number can be trusted, and how an answer is shaped. Its
version equals the report's `schema_version`. Its rationale is in
`contracts/contract_result_comments.md`.

## Result folder

```
<resultfolder>/<code>/
  report/index.md            tier 1: start here (only with -rp; always for experiment.py)
  report/{workflow,loading,benchmarking,monitoring,connections}.md
                             tier 2: evidence, each only if that phase ran
  report/files.md            tier 3: links every raw file below, once
  experiment.yml, contract_catalog.yml, contract_result.yml, environment.yml
                             inputs of a catalog-driven run, copied at start
  connections.config, queries.config, <job>.config
                             what ran; read these when there is no report
  *.yml                      Kubernetes manifests as submitted (concrete image tags)
  *-loading-*.{sql,sh,stdout,stderr,sensor,datagenerator}.log
  bexhoma-benchmarker-*.log, query_<component>_metric_<key>.csv
  bexhoma-sut-*.{<container>,describe}.log, *.<container>.previous.log, *-restarts.json
  agent_summary.yml          written by the agent harness only
```

`<code>` is the start time in Unix seconds: unique and increasing, but not
evidence that two codes ran under comparable conditions.

## Identifiers

Decode by counting dash-separated segments from the right.

| Identifier | Shape | Example |
|---|---|---|
| configuration | `<system>-<n>` | `pgduckdb-1` |
| phase | `<configuration>-<experiment_run>-<client>` | `pgduckdb-1-3-2` |
| job | `<phase>-<benchmark_run>` | `pgduckdb-1-3-2-1` |
| connection | `<job>-<pod>` | `pgduckdb-1-3-2-1-4` |

`experiment_run` counts repetitions, `client` the phases (rounds) within one,
`benchmark_run` parallel jobs in a phase, `pod` driver pods in a job. File
names follow `<app>-<component>-<configuration>-<code>[-<run>[-<client>[-<benchmark_run>]]]`,
plus a Kubernetes pod suffix where the file belongs to one pod; decode them from
`<code>`.

## Validity checks

`index.md`'s Tests table. Only a failed row restricts what can be claimed; a
skipped row never does.

| Check | Fails when | Restricts |
|---|---|---|
| workflow as planned | submitted jobs or pods differ from the plan | comparisons across phases |
| no SUT container restarts | a SUT container restarted | its configuration from the restart on |
| SUT data survived restarts | a restarted SUT had no data volume | every later query of it ran on an empty database |
| key metric present | a headline metric is 0 or NaN | that metric |
| no SQL errors (TPC-H) | a query failed | that query; the pooled totals |
| all active queries in the totals (TPC-H) | a query failed in some connection and left the pooled totals | the pooled per-phase metrics |
| no SQL warnings (TPC-H) | result sets differ inside one driver process | correctness of those queries |
| component CPU non-zero | monitoring read 0 or NaN (skipped for phases shorter than a scrape) | monitoring data only |
| no monitoring metrics missing | Prometheus returned no data, filled with zeros (skipped when every gap is expected) | those metrics |
| EXPLAIN captured (TPC-H) | an active query has no plan (skipped without `store_explain`) | evidence of which engine ran |

Headline metrics: TPC-H `Geo Times [s]`, `Power@Size [~Q/h]`,
`Throughput@Size`; YCSB `[OVERALL].Throughput(ops/sec)`; HammerDB `NOPM`;
Benchbase `Throughput (requests/second)`.

## Answer contract

1. **Hypothesis**: quote `experiment.yml`'s hypothesis; without that file, say
   no hypothesis was recorded.
2. **Verdict**: supported, refuted, inconclusive or invalid, then the
   pass/fail/skip counts. Start from the first failure in the report's Failure
   Timeline; the order is evidence, not a diagnosis.
3. **Evidence**: cite the file and value behind every claim.
4. **Follow-up**: if unresolved, propose an `experiment.yml` with
   `follow_up_of` set to this code.

`agent_summary.yml` holds the agent's compact verdict for lineage: code,
`follow_up_of`, hypothesis, verdict with evidence paths, failed-check count
and scope, unresolved question. A later follow-up reads only these summaries
of its ancestors, never their reports.

## Known gaps

- Image tags are recorded, digests are not; dbmsbenchmarker's own version is not.
- No check compares experiments; compare only within one code.
- Nothing verifies that data loaded completely. A table that failed to load
  shows only in tier 3: each loader pod's `*.sensor.log` and the statistics
  script's row counts.
- `no_sql_warnings` compares result sets only within one driver process; a
  pass says nothing about agreement between systems or runs.
- Which `post_load` steps a system received is visible only in
  `*-loading-*.sql.log`.

## The contract

```{literalinclude} ../contracts/contract_result.yml
:language: yaml
```
