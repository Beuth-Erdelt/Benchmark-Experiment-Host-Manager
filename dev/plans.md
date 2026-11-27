# Plans: overview

State of every `plan-*.md` in `dev/`, checked 2026-11-26 against the plan texts and the branch
`docs-modularity` (on top of #937 and #941). One line per open item; details are in the plan.

| State | Meaning |
|---|---|
| open | implemented in part, items left that are meant to be done |
| planned | written, nothing (or almost nothing) implemented |
| parked | deliberately on hold or deferred by the user |
| done | finished; leftovers are optional or belong elsewhere |

## Summary

| Plan | State | Open |
|---|---|---|
| [ddl-parameters](plan-ddl-parameters.md) | open | M5 keys, 13b, catalog size, small items |
| [software-quality](plan-software-quality.md) | open | S4, S6, S7 blocking |
| [fewer-kubectl-calls](plan-fewer-kubectl-calls.md) | open | M5, M15 |
| [load-failure-and-sizing](plan-load-failure-and-sizing.md) | open | P2 tmpdir (decision c/d), A4 |
| [dbms-generic-verification](plan-dbms-generic-verification.md) | done | 2 side findings, aliases deferred |
| [research-software](plan-research-software.md) | open | Zenodo 2/2a/20, step 18, R3, I1 |
| [ceph-pool-metrics](plan-ceph-pool-metrics.md) | open | lag decision, text summary |
| [observe-per-query-metrics](plan-observe-per-query-metrics.md) | open | refresh, staleness, application metrics |
| [ssb](plan-ssb.md) | open | multi-tenancy |
| [explicit-rounds](plan-explicit-rounds.md) | planned | C1-C4, then #925 |
| [experiment-yaml-source-of-truth](plan-experiment-yaml-source-of-truth.md) | planned | W1-W11, Q1-Q7 |
| [pgduckdb-force-execution](plan-pgduckdb-force-execution.md) | planned | all (P1, "for later") |
| [shorter-phase-gaps](plan-shorter-phase-gaps.md) | planned | G0-G8 |
| [per-config-overrides](plan-per-config-overrides.md) | planned | M1-M5 (`--set-tenant`) |
| [tenancy-sweep](plan-tenancy-sweep.md) | planned | runs A, B, D; C needs per-config-overrides |
| [ycsb-sysbench-noisy-neighbor](plan-ycsb-sysbench-noisy-neighbor.md) | planned | all |
| [pg18-tuning-followup](plan-pg18-tuning-followup.md) | planned | items 1-5 |
| [mariadbcs-bug-reports](plan-mariadbcs-bug-reports.md) | planned | M0-M5, tickets B1-B7 |
| [result-comparison](plan-result-comparison.md) | planned | phases 1-5, contract finding |
| [harness-identity](plan-harness-identity.md) | planned | steps 1-5 |
| [publish-bundle](plan-publish-bundle.md) | planned | all |
| [studies](plan-studies.md) | planned | M0-M9 |
| [session-parameters](plan-session-parameters.md) | parked | S1-S3 |
| [planned-disruptions](plan-planned-disruptions.md) | parked | all, until a benchmark needs it |
| [848-no-silent-load-failures](plan-848-no-silent-load-failures.md) | done | - |
| [docs-dbms-pages](plan-docs-dbms-pages.md) | done | one unreferenced log |
| [keep-sut](plan-keep-sut.md) | done | default of `load` (optional) |
| [metrics-pod-scope](plan-metrics-pod-scope.md) | done | - |
| [mysql-storage-slowness](plan-mysql-storage-slowness.md) | done | template default (in load-failure-and-sizing) |
| [oltp-storage-dbms](plan-oltp-storage-dbms.md) | done | - |
| [reset-scripts](plan-reset-scripts.md) | done | optional: flush time at large SF |
| [silent-malfunctions](plan-silent-malfunctions.md) | done | P9 is an issue, P11 in planned-disruptions |
| [storage-class-sweep](plan-storage-class-sweep.md) | done | risks only |
| [storage-remove-per-repetition](plan-storage-remove-per-repetition.md) | done | - |
| [stream-metrics](plan-stream-metrics.md) | done | rest of #239 elsewhere |

## Open

### [ddl-parameters](plan-ddl-parameters.md)

M1-M4 done, M4 cluster-checked 2026-11-25 and merged in #937. The status header at the top of the plan still
says the cluster checks are open.
- **M5:** keys not started: `covering_indexes`, `projections`, `pk_order`; keys that change results
  (`string_type`, `numeric_type`); script variants (`primary_keys`, `distribution_key`); `hash_partitions`
  (BenchBase creates the PostgreSQL TPC-C schema); `tablespace_index`.
- **13b:** missing post-load scripts are skipped with a notice (done); open: the ClickHouse/ClickHouseCluster
  constraints, indexes and statistics, whether missing `.sql` and `.sh` are reported alike (A/B/C), and the
  missing check scripts (`checkschema-tpch` for DatabaseService and PgDuckDB, `checkschema-ycsb` for
  DatabaseService).
- **Catalog size:** the next PostgreSQL key needs a shorter catalog or a higher limit (decision).
- **Docs rerun:** the TPC-H cluster logs in Example-ClickHouse.md are from the old layout.
- Optional: item 11, an obsolete "No curly braces" comment in many scripts.
- Outside the plan: Python client calls do not wait out a cluster outage (`MaxRetryError`); old-named volumes
  from another machine's older bexhoma.

### [software-quality](plan-software-quality.md)

S1, S2, S3, S5, S7 done (#931, #933).
- **S4:** one argument check (`argument_error()`) used by `main()` and the catalog paths, so a catalog
  experiment with invalid tenancy or a 0-thread split is refused.
- **S6:** split `work_benchmark_list()` into phase handlers and remove the legacy `benchmark_list` path; needs
  cluster runs.
- **S7 blocking:** diff coverage is reported but `continue-on-error`; make it fail.
- S2 left out long lines (E501).

### [fewer-kubectl-calls](plan-fewer-kubectl-calls.md)

M0-M4, M6-M14 done (v0.11.6).
- **M5 (optional):** exec through the Python client instead of kubectl; check the token plugin and token
  lifetime with the admins first.
- **M15:** handle the four repetition-boundary passes (stop SUTs, start SUTs, start loading, loading end)
  of all tenants side by side; about 23 of 79 min of tenancy_8.
- The optional O1-O3 continue in [shorter-phase-gaps](plan-shorter-phase-gaps.md).

### [load-failure-and-sizing](plan-load-failure-and-sizing.md)

P1, P3-P6 done.
- **P2:** MySQL `/mysqltmp` is a memory `emptyDir` (32Gi); decide c (data volume) or d (container `/tmp`).
- **A4:** a start check of buffer pool vs. container limit, a candidate guard.
- Later options for the template's buffer pool default (A1/A2/A4/A5), also asked by
  [mysql-storage-slowness](plan-mysql-storage-slowness.md).

### [dbms-generic-verification](plan-dbms-generic-verification.md)

Done 2026-11-24; left over:
- RF2 row counts: the MySQL refresh loader prints none for RF2, the ClickHouse loader none for RF1 or RF2.
- Db2 loaders write chunk files and `SYSTET*.log` into the shared data folder; fix: `/tmp` and
  `LOGDIR '/tmp'`.
- Deferred ("for the future"): 1.4 aliases, check that anonymized summaries reveal no DBMS.

### [research-software](plan-research-software.md)

Steps 1, 2b, 3-17, 19 done (v0.12.0, v0.12.1).
- **2, 2a, 20 (last):** `.gitattributes` export-ignore, `.zenodo.json`, GitHub integration, DOI badge, DOI in
  `CITATION.cff`/`codemeta.json`, a Zenodo community for experiment specifications. Open question: archive
  every release or only minor ones (recommended: every release).
- **18 (deferred):** contract specs, validator, result format as separate packages with DOIs; decide option
  A/B/C, split of generic spec vs. catalog, one or two DOIs, how the proposal describes the validator.
- **R3:** CI tests only Python 3.10 and 3.12.
- **I1:** result folder formats (pickle, Python literals) come from DBMS-Benchmarker.

### [ceph-pool-metrics](plan-ceph-pool-metrics.md)

M1-M5 done (v0.11.3).
- **Lag decision:** Ceph counters lag 1-2 min behind the phase windows; a per-metric `shift` in
  DBMS-Benchmarker or document the lag. Measure the lag first.
- The text summary (`bexhoma summary`) has no Ceph tables (the agent report has).

### [observe-per-query-metrics](plan-observe-per-query-metrics.md)

Node occupancy, `monitoring:` section and `observe.metrics` for hardware metrics done.
- Refresh `environment.yml` on every agent start.
- Staleness check: `source_sha256` is written but never compared.
- Application metrics in the catalog: wait for the catalog split.
- `cluster.config`: `tikv_store_size_bytes` defined twice; network/filesystem queries active although skipped.

### [ssb](plan-ssb.md)

Done for all DBMS incl. ClickHouseCluster and MariaDB ColumnStore.
- **Multi-tenancy:** `-mtn` is still refused for SSB.

## Planned

### [explicit-rounds](plan-explicit-rounds.md) (draft 2026-11-26, untracked)

Rounds as an explicit list in the experiment dict / YAML (decisions D1-D5).
- **C1-C4:** benchmark lookup by entry name instead of position, no per-round side lists, round 0 template only
  in builders, `-nc` replays the rounds.
- **#925:** TPC-DS data maintenance as explicit DM rounds, all in `bexhoma/benchmarks/tpcds/`.
- Later: explicit rounds in the YAML schema, start conditions (`plan-start-conditions.md` does not exist yet).

### [experiment-yaml-source-of-truth](plan-experiment-yaml-source-of-truth.md) (draft 2026-11-26, untracked)

`experiment.yaml` as the one source of truth; CLI options build it.
- **W1-W11:** option inventory, explicit rounds (= the plan above), settings objects instead of `args`, generic
  loader/validator, a builder per benchmark, equivalence tests, `--print-yaml`, persisted YAML, one entry
  script `bexhoma experiment`, catalog path, docs.
- **Q1-Q7:** schema shape, sweeps in the file, fate of the experiment dict, file names, where the schema lives,
  runtime-only options, provenance of CLI runs (proposals given, not decided).

### [pgduckdb-force-execution](plan-pgduckdb-force-execution.md)

`-xdfe` writes a role setting that survives on a reused volume; results there can be wrong. Ranked P1,
deferred by the user.
- Server setting via a new `option_settings` entry key, `RESET` in the template, catalog knob style, result
  recording, `--set` vs. SUT parameters, tests and a same-volume cluster check.
- Also: the workload note ignores a system's own `sut_parameters`.

### [shorter-phase-gaps](plan-shorter-phase-gaps.md)

Shorter SUT idle time between loading and benchmarking and between rounds.
- **G0-G8:** measure gaps, fetch metrics after the next submission, async scripts wake the loop, parallel
  index scripts of tenants, job end after next submission, wake on job end, background fetches, a pause
  parameter.
- Open: default pause of G8, whether the per-round DB size is needed before the next round, dashboard pod
  placement.

### [per-config-overrides](plan-per-config-overrides.md)

`--set-tenant` for per-tenant placement and workload.
- **M1-M5:** tenant id on the configuration, flag and parser, node, env and manifest targets, use in the
  tenancy sweep; M6 optional.

### [tenancy-sweep](plan-tenancy-sweep.md)

fio tenancy sweep on the `nvme` pool; M0a (`-xfow`) done.
- **Runs A, B, D** with the code as it is (D needs krbd `noshare`, M3).
- **Placement C and noisy neighbor:** wait for [per-config-overrides](plan-per-config-overrides.md).

### [ycsb-sysbench-noisy-neighbor](plan-ycsb-sysbench-noisy-neighbor.md)

sysbench co-located with YCSB as CPU noise; nothing written. Code paths in the plan are outdated (benchmark
folders), and benchmark folders may import only generic code.

### [pg18-tuning-followup](plan-pg18-tuning-followup.md)

Rerun of the PostgreSQL 18 default vs. tuned comparison.
- 1: isolate `io_method` for both TPC-C tools; 2: the same for TPC-DS (now also concerns the docs runs);
  3: fix the TPC-H harness; 4: larger TPC-DS PVC; 5: repetitions.

### [mariadbcs-bug-reports](plan-mariadbcs-bug-reports.md)

Report the ColumnStore bugs of #827 to MariaDB Jira (MCOL), filed by the user.
- **B1-B5:** silent wrong results (CTE window filter, rollup on derived table, left join filter, computed join
  key, CTE self join); **B6:** rollup crash of `PrimProc`; **B7:** cgroup means one core.
- Milestones M0-M5: environment, standalone scripts, runs, versions, ticket texts, filing.
- Open: whether B7 is a ticket, `ERROR 1030` with concurrent loads, `cpimport -m 1` from another container.

### [result-comparison](plan-result-comparison.md)

Comparison of result sets across DBMS with levels and tolerances (DBMS-Benchmarker + bexhoma).
- Phases 1-5: core with canonicalization and tests, merge and report, bexhoma integration, golden results,
  order keys.
- **Contract finding:** `contract_result.yml` says result sets are compared only inside one process, which is
  outdated; correct it with a version bump (independent of the plan).

### [harness-identity](plan-harness-identity.md)

Identify the agent harness without git: version from package metadata, fingerprint over a declared manifest,
build stamp at release, git only as a label. Steps 1-5 (`fingerprint.py`, publish workflow, `.gitignore`,
docs).

### [publish-bundle](plan-publish-bundle.md)

Redacted export of runs (`scripts/publish_bundle.py`, #795). Must refuse runs with internal DBMS (SQLServer,
OracleDB, DB2, CedarDB) and carry the TPC note. Open: configurable redactions, handbook/contract versions in
the bundle.

### [studies](plan-studies.md)

Studies as first-class records (`study.yml`, standing, study answer, citations as context, baseline, later
rerun, withdrawal, planned series).
- **M0:** design read scope; whether design and follow-up authoring may read provenance (user decision).
- M1-M6, later M7-M9.
- Open decision: answer a study from citations alone.

## Parked

### [session-parameters](plan-session-parameters.md)

Session settings swept without reload, nothing blocks it any more. Today: one experiment per value with
`--set` on the same `-rst` volume. Milestones S1-S3; open: round order bias, restore after the last round.

### [planned-disruptions](plan-planned-disruptions.md)

Benchmarks that terminate pods on purpose (e.g. recovery time) must pass when disruptions happen as planned.
Not started until a benchmark needs it. Open: who disrupts, timing reference, what "recovered" means, workers,
interaction with `-nc`/`-rsrp`.

## Done

- [848-no-silent-load-failures](plan-848-no-silent-load-failures.md): v0.11.14 (#868).
- [docs-dbms-pages](plan-docs-dbms-pages.md): left over, delete or keep
  `logs_tests/test_tpcds_testcase_compare_summary.md` (v0.10.0, unreferenced).
- [keep-sut](plan-keep-sut.md): optional, whether `load` should default to not keeping SUTs.
- [metrics-pod-scope](plan-metrics-pod-scope.md)
- [mysql-storage-slowness](plan-mysql-storage-slowness.md): the template default of 8G is a separate decision
  (load-failure-and-sizing).
- [oltp-storage-dbms](plan-oltp-storage-dbms.md)
- [reset-scripts](plan-reset-scripts.md): optional, watch the MySQL/MariaDB flush time at larger SF; YugabyteDB
  persist needs `yb-admin`.
- [silent-malfunctions](plan-silent-malfunctions.md): S1-S19 merged in #937, S20 (P6/P13, expected-metrics
  list, #952) on `feature/expected-metrics`, checked 2026-11-27; docs page
  [docs/Malfunctions.md](../docs/Malfunctions.md). P9 (`-nbp`/`-nbt` ignored by TPC-H, TPC-DS, SSB) is an
  issue; P11 is [planned-disruptions](plan-planned-disruptions.md); mapping `tpcc` to HammerDB (P12) will not
  be done.
- [storage-class-sweep](plan-storage-class-sweep.md): risks only (stale PVCs, placement warning).
- [storage-remove-per-repetition](plan-storage-remove-per-repetition.md)
- [stream-metrics](plan-stream-metrics.md): the rest of #239 is in metrics-pod-scope.

## Other documents in `dev/`

- [Design-Catalog-Contract](Design-Catalog-Contract.md): draft, phase 1 implemented (TPC-H, YCSB); phase 2
  is W10 of experiment-yaml-source-of-truth.
- [Design-Yaml-Experiment-Entry-Script](Design-Yaml-Experiment-Entry-Script.md): today's TPC-H-only YAML path.
- [network-degeneration-findings](network-degeneration-findings.md): findings on the PostgreSQL pod-count
  degradation (`-nbp 1,2`), not a plan.
