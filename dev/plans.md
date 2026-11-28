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
| [research-software](plan-research-software.md) | open | Zenodo 2/2a/20, step 18, R3, I1 |
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
| [ceph-pool-metrics](plan-ceph-pool-metrics.md) | done | risks only |
| [dbms-generic-verification](plan-dbms-generic-verification.md) | done | - |
| [docs-dbms-pages](plan-docs-dbms-pages.md) | done | one unreferenced log |
| [fewer-kubectl-calls](plan-fewer-kubectl-calls.md) | done | M15 is issue #963 |
| [keep-sut](plan-keep-sut.md) | done | default of `load` (optional) |
| [load-failure-and-sizing](plan-load-failure-and-sizing.md) | done | P2 (and A4) is issue #971 |
| [metrics-pod-scope](plan-metrics-pod-scope.md) | done | - |
| [observe-per-query-metrics](plan-observe-per-query-metrics.md) | done | rest is issues #964-#970 |
| [mysql-storage-slowness](plan-mysql-storage-slowness.md) | done | template default (in load-failure-and-sizing) |
| [oltp-storage-dbms](plan-oltp-storage-dbms.md) | done | - |
| [reset-scripts](plan-reset-scripts.md) | done | optional: flush time at large SF |
| [silent-malfunctions](plan-silent-malfunctions.md) | done | P9 is an issue, P11 in planned-disruptions |
| [software-quality](plan-software-quality.md) | done | rest is issues #957-#960 |
| [ssb](plan-ssb.md) | done | multi-tenancy is issue #961 |
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

### [research-software](plan-research-software.md)

Steps 1, 2b, 3-17, 19 done (v0.12.0, v0.12.1).
- **2, 2a, 20 (last):** `.gitattributes` export-ignore, `.zenodo.json`, GitHub integration, DOI badge, DOI in
  `CITATION.cff`/`codemeta.json`, a Zenodo community for experiment specifications. Open question: archive
  every release or only minor ones (recommended: every release).
- **18 (deferred):** contract specs, validator, result format as separate packages with DOIs; decide option
  A/B/C, split of generic spec vs. catalog, one or two DOIs, how the proposal describes the validator.
- **R3:** CI tests only Python 3.10 and 3.12.
- **I1:** result folder formats (pickle, Python literals) come from DBMS-Benchmarker.

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
- [ceph-pool-metrics](plan-ceph-pool-metrics.md): v0.11.3; the 1-2 min counter lag is documented only
  (decided 2026-11-28). Risks only: short phases on a fresh volume, CephFS pool level, no OSD scope.
- [dbms-generic-verification](plan-dbms-generic-verification.md): done 2026-11-24. The side findings (RF2 row
  counts for MySQL/MariaDB, Db2 load logs off the data volume) are fixed in b275ad8c (#937); ClickHouse prints
  file counts only (no extra query in the stream); no cluster run with rebuilt images recorded. 1.4 aliases
  and the check that anonymized summaries reveal no DBMS were dropped 2026-11-28 (not pursued for a long time).
- [docs-dbms-pages](plan-docs-dbms-pages.md): left over, delete or keep
  `logs_tests/test_tpcds_testcase_compare_summary.md` (v0.10.0, unreferenced).
- [fewer-kubectl-calls](plan-fewer-kubectl-calls.md): M0-M4, M6-M14 (v0.11.6). M15 (repetition boundaries of
  all tenants side by side) is issue #963; M5 will not be done, kubectl stays (decided 2026-11-28); the
  optional O1-O3 continue in [shorter-phase-gaps](plan-shorter-phase-gaps.md).
- [keep-sut](plan-keep-sut.md): optional, whether `load` should default to not keeping SUTs.
- [load-failure-and-sizing](plan-load-failure-and-sizing.md): P1 (8G buffer pool), P3-P6 and the loader
  barrier timeout done (P3/P4 via #848, P5 and the timeout via #929). P2 (MySQL `/mysqltmp` out of the memory
  budget, decide c or d) and the optional A4 guard (buffer pool vs. limit) are issue #971 (2026-11-28). Later
  options for the buffer pool default (A1/A2/A5) stay in the plan.
- [metrics-pod-scope](plan-metrics-pod-scope.md)
- [mysql-storage-slowness](plan-mysql-storage-slowness.md): the template default of 8G is a separate decision
  (load-failure-and-sizing).
- [observe-per-query-metrics](plan-observe-per-query-metrics.md): node occupancy, `monitoring:` section and
  `observe.metrics` for hardware metrics done. The rest is tracked as issues (2026-11-28): #964 staleness check,
  #965 refresh selected sections of `environment.yml` (no auto refresh by the agent), #966 own cAdvisor
  disk/network metrics, #967 `current_load`, #968 application metrics in the catalog, #969 summary order,
  #970 result contract. The `tikv_store_size_bytes` duplicate is fixed in `k8s-cluster.config`.
- [oltp-storage-dbms](plan-oltp-storage-dbms.md)
- [reset-scripts](plan-reset-scripts.md): optional, watch the MySQL/MariaDB flush time at larger SF; YugabyteDB
  persist needs `yb-admin`.
- [silent-malfunctions](plan-silent-malfunctions.md): S1-S19 merged in #937, S20 (P6/P13, expected-metrics
  list, #952) on `feature/expected-metrics`, checked 2026-11-27; docs page
  [docs/Malfunctions.md](../docs/Malfunctions.md). P9 (`-nbp`/`-nbt` ignored by TPC-H, TPC-DS, SSB) is an
  issue; P11 is [planned-disruptions](plan-planned-disruptions.md); mapping `tpcc` to HammerDB (P12) will not
  be done.
- [software-quality](plan-software-quality.md): S1, S2, S3, S5, S7 merged (#931, #933). The rest is tracked
  as issues: #957 (S7 blocking), #958 (S4 argument check), #959 (S6 split `work_benchmark_list()`), #960
  (long lines, star imports, E402, shadowed built-ins, type checks).
- [ssb](plan-ssb.md): done for all DBMS incl. ClickHouseCluster and MariaDB ColumnStore (v0.11.9).
  Multi-tenancy (`-mtn`, refused today) is issue #961: container tenancy first, then schema/database.
- [storage-class-sweep](plan-storage-class-sweep.md): risks only (stale PVCs, placement warning).
- [storage-remove-per-repetition](plan-storage-remove-per-repetition.md)
- [stream-metrics](plan-stream-metrics.md): the rest of #239 is in metrics-pod-scope.

## Other documents in `dev/`

- [Design-Catalog-Contract](Design-Catalog-Contract.md): draft, phase 1 implemented (TPC-H, YCSB); phase 2
  is W10 of experiment-yaml-source-of-truth.
- [Design-Yaml-Experiment-Entry-Script](Design-Yaml-Experiment-Entry-Script.md): today's TPC-H-only YAML path.
- [network-degeneration-findings](network-degeneration-findings.md): findings on the PostgreSQL pod-count
  degradation (`-nbp 1,2`), not a plan.
