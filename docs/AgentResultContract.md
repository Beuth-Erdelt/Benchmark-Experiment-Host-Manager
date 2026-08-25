# Result Folder Output Contract

A pre-run reference for an agent (or human) that needs to know, **before
submitting an experiment**, exactly what will exist in the result folder
afterwards, what it will be named, and which files are safe to treat as
ground truth versus which are only a rendered convenience.

This is the contract version of [`AgentReport.md`](AgentReport.md) (which
explains the tiered-report *design*) and of the naming/validity/interpretation
blocks embedded verbatim in every `report/index.md`
(`bexhoma/report_writer.py`) — read this file to plan; read the generated
`report/index.md` to interpret an actual run.

```yaml
result_contract_version: "1.4.0"   # == bexhoma.report_writer.SCHEMA_VERSION;
                                    # bump tracks report_writer.py's own frontmatter/tier/layout changes

entry_point:
  with_report:    report/index.md  # only exists if the run passed -rp/--report
  without_report: connections.config, queries.config   # always exist once benchmarking started; read these directly

structure:
  result_dir: "{resultfolder}/{code}/"
  experiment_code: unix-timestamp        # `code`: seconds, generated at experiment start;
                                          # unique + monotonically increasing, but NOT evidence
                                          # two codes ran under comparable conditions
  configuration:  "<system>-<n>"                                       # e.g. postgresql-1 (lowercased when
                                                                        # embedded in phase/job/connection below;
                                                                        # original case, e.g. "PostgreSQL-1", when
                                                                        # shown standalone, e.g. connections.config)
  phase:          "<configuration>-<experiment_run>-<client>"          # drops benchmark_run, pod
  job:            "<configuration>-<experiment_run>-<client>-<benchmark_run>"  # drops pod
  connection:     "<configuration>-<experiment_run>-<client>-<benchmark_run>-<pod>"
  # decode any identifier by counting dash-separated segments from the right

tiers:                                  # only "with_report" tiers 1-2 are new files; tier 3 is always the raw folder
  1_answers:   {glob: "report/index.md"}
  2_evidence:  {glob: "report/{workflow,loading,benchmarking,monitoring,connections}.md"}
                                          # each written only if that phase was active
  3_diagnosis: {result_dir: "*"}         # see provenance: below; linked from every tier-2 "### Provenance" footer

provenance:                              # pre-existing files, never written or modified by the report
  connections:  {"connections.config": "repr() list of every connection dict (identity, params, timings)",
                 "{connection}.config": "durable single-connection backup, survives dashboard rewrites",
                 "queries.config":      "SF/type/duration/defaultParameters/benchmark_sequence/workflow_planned"}
  workflow:     {"*.yml / *.yaml (minus the input-provenance filenames below)":
                                         "rendered K8s Job/Deployment/Service manifests actually submitted;
                                          every image: field is a concrete tag, BEXHOMA_PACKAGE_VERSION
                                          already substituted — the authoritative source for image versions",
                 "experiment.yml / experiment.yaml, contract_catalog.yml, contract_result.yml,
                  catalog.yaml, environment.yml (whichever exist)":
                                         "the input(s) this run was actually built from, not a K8s manifest —
                                          a YAML-driven run (experiment.py) copies the experiment.yml/.yaml it
                                          was given, plus (catalog-driven only) the contract_catalog.yml/
                                          contract_result.yml pair that governed it, or (self-specified only)
                                          any catalog:/environment: pointer files the spec named; a hand-typed
                                          python tpch.py ... invocation writes none of these",
                 "{pod-name}.describe.log": "kubectl describe pod: scheduling/image-pull/restart/OOMKill events
                                              for that specific Pod object",
                 "{job-name}.describe.job.log": "kubectl describe job (loading/generator jobs only; .job.log,
                                              not .describe.log, so it globs apart from per-pod describes):
                                              the Job's own Events list every Pod it ever spawned over
                                              its full lifetime, including a failed one replaced under
                                              backoffLimit — evidence that survives even after the failed Pod
                                              object itself has been garbage-collected and dropped out of the
                                              per-pod *.describe.log set above"}
  loading:      {"*-loading-*.sql.log / *-loading-*.sh.log": "rendered script SOURCE despite the .log suffix",
                 "*-loading-*.stdout.log": "stdout of that script",
                 "*-loading-*.stderr.log": "stderr — check first on a silent loading failure"}
  benchmarking: {"bexhoma-benchmarker-*.log":            "raw per-pod benchmarker/driver stdout",
                 "bexhoma-benchmarker.*.all.df.pickle":  "cached parsed+aggregated DataFrame",
                 "queries.config":                        "literal SQL text — DBMSBenchmarker-family (TPC-H/TPC-DS) only"}
  monitoring:   {"query_{component}_metric_{key}.csv":   "wide format: one column per connection, one row per Prometheus scrape;
                                                            {component} (e.g. loading/benchmarking/loader/benchmarker/datagenerator)
                                                            is a fixed vocabulary owned by the vendored dbmsbenchmarker dependency,
                                                            not bexhoma's to rename freely — see monitoring.md's component_title
                                                            column for the human-readable pairing"}
  restarts:     {"bexhoma-sut-{configuration}-{experiment_run}-restarts.json": "per-pod SUT container restart counts, one snapshot per experiment_run; aggregate by max per pod (restartCount is cumulative across runs, same pod, not recreated), not by summing every file"}
  sut_logs:     {"bexhoma-sut-{configuration}-{code}-{experiment_run}.yml":                    "SUT Deployment manifest — one archived copy per experiment_run, even when identical to the previous run's, since the live Deployment itself is restarted in place rather than recreated",
                 "bexhoma-sut-{configuration}-{code}-{experiment_run}-{pod-hash}-{pod-suffix}.{container}.log":  "SUT container stdout, one capture per experiment_run",
                 "bexhoma-sut-{configuration}-{code}-{experiment_run}-{pod-hash}-{pod-suffix}.describe.log":     "kubectl describe pod, one capture per experiment_run"}
                 # see "Result-folder filenames vs. report identifiers" below for the one remaining
                 # asymmetry: the live k8s object's own name has no experiment_run segment, even
                 # though every filename on disk (including its own archived manifest) does

versions:                                # see Known gaps below for what's genuinely still missing
  images: recorded_as_tag_not_digest     # every submitted manifest's image: field is a concrete tag
                                          # (provenance.workflow *.yml); connections.config's own
                                          # `dockerimage` field mirrors the SUT's resolved tag too;
                                          # no sha256 digest either way, so a re-pushed tag is invisible
  bexhoma: recorded_directly_and_via_image_tag
                                          # report/index.md frontmatter's bexhoma_version field records
                                          # the installed bexhoma.__version__ at report-generation time
                                          # (can differ from the version that actually ran the experiment
                                          # if -rp/--report is applied later, e.g. `bexhoma summary -e
                                          # <code> -rp`, after an upgrade); for the submission-time version,
                                          # BEXHOMA_PACKAGE_VERSION in every bexhoma/* image tag is
                                          # substituted with the real installed version before the
                                          # manifest is written to the result folder
                                          # (clusters.py::create_object_from_file()) and can't drift later
  dbmsbenchmarker: not_recorded          # baked into the bexhoma/benchmarker_dbmsbenchmarker image,
                                          # whose tag tracks bexhoma's own version, not
                                          # dbmsbenchmarker's — genuinely not recoverable

validity:                                # from experiment._test_results -> report/index.md "### Tests" table
  - id: workflow_as_planned              # planned (queries.config's workflow_planned) == actual submitted jobs/pods
    kind: absolute
  - id: no_sut_container_restarts        # bexhoma-sut-*-restarts.json sums to 0
    kind: absolute
  - id: key_metric_present               # benchmark-type headline column(s) contain no 0/NaN — see table below
    kind: absolute
  - id: no_sql_errors                    # DBMSBenchmarker-family (TPC-H/TPC-DS) only
    kind: absolute
  - id: no_sql_warnings                  # = no result-set mismatch across systems; DBMSBenchmarker-family only
    kind: absolute
  - id: monitoring_component_cpu_nonzero # per monitored component; SKIPPED (not failed) when phase < 1 scrape interval
    kind: absolute
  - id: cross_experiment_comparison      # NOT IMPLEMENTED — see Known gaps
    kind: comparative
  verdict: {passed: int, failed: int, skipped: int}   # index.md frontmatter overall_status;
                                                        # only a FAILED row scopes/invalidates metrics below it — skipped never does

answer_contract:                         # how to structure the final written answer, once the above has been read
  hypothesis:
    source_file: experiment.yml          # <result_dir>/experiment.yml; fields: title, hypothesis, discriminates, follow_up_of
    present_when: catalog-driven run     # `python experiment.py run <file>.yml` copies it in at run start
    absent_when: direct entry-script run # e.g. `python tpch.py run -dbms ...` never had a catalog file to copy —
                                          # state "no hypothesis recorded", don't reconstruct one from workload params
    also_copied: [contract_catalog.yml, contract_result.yml]  # frozen at run time, may differ from the repo's current copies
  steps:
    - {id: hypothesis, instruction: "restate the question, quoting experiment.yml's hypothesis verbatim when present"}
    - {id: verdict,     instruction: "pass/fail/skip counts; note any FAILED row scoping a metric below it", source: verdict_shape}
    - {id: evidence,    instruction: "cite the specific tier-1/tier-2 file and value behind every claim", source: tiers}
    - {id: follow_up,   instruction: "if unresolved, propose a new experiment.yml with follow_up_of set to this run's experiment_code", source: "experiment.yml discriminates/follow_up_of, else known_gaps.cross_experiment_comparison"}
```

---

## Naming legend, as a decoding rule

Every identifier is a positional dash-concatenation — decode by counting
segments from the right, no lookup table needed:

| Term | Meaning | Example |
|---|---|---|
| `configuration` | SUT instance name (original case when shown standalone, e.g. `PostgreSQL-1`) | `PostgreSQL-1` |
| `experiment_run` | Repeat counter for the whole experiment (`-nc`) | `2` |
| `client` | 1-based index of the benchmark phase/round within a run (`-ne`) | `3` |
| `phase` | `<configuration>-<experiment_run>-<client>`, lowercased | `postgresql-1-2-3` |
| `benchmark_run` | 1-based index of a parallel benchmark job within a round (query stream vs. refresh stream, etc.) | `1` |
| `job` | `<phase>-<benchmark_run>`, lowercased | `postgresql-1-2-3-1` |
| `pod` | 1-based index of a driver pod within a job | `1` |
| `connection` | `<job>-<pod>`, lowercased | `postgresql-1-2-3-1-1` |

`code` (the result folder's own directory name) is a Unix epoch timestamp
in seconds, assigned once at experiment start — unique and monotonically
increasing, but comparing two different `code`s as "the same conditions"
requires independently verifying that (see Interpretation Rules in every
`index.md`).

## Result-folder filenames vs. report identifiers

The table above decodes identifiers *inside* the report (table indexes,
`connections.md` anchors). Filenames actually on disk — manifests, logs,
`.describe.log` — follow a related but distinct convention:
`<app>-<component>-<configuration>-<code>[-<experiment_run>[-<client>[-<benchmark_run>]]]`,
optionally followed by Kubernetes' own pod-hash/random suffix on files tied
to one specific pod, e.g.
`bexhoma-benchmarker-postgresql-1-1784910886-1-1-1-qp9nt.dbmsbenchmarker.log`.
Decode these the same way — count from `code`, not from the right — since a
trailing Kubernetes pod suffix (a hash plus 5 random characters) isn't part
of the schema and can't be told apart from it by position alone.

**The SUT Deployment's own k8s identity is the one asymmetric case — but its
filenames are not.** The live Deployment object is restarted in place across
every `-nc` repeat rather than recreated, so its `metadata.name` (and the
service/pod names derived from it) stay identical run after run, with no
`experiment_run` segment. Every *filename* related to it, however, is
experiment_run-scoped like everything else: its manifest is archived as
`bexhoma-sut-{configuration}-{code}-{experiment_run}.yml` — a fresh copy
written every run (even when byte-identical to the previous run's, since the
Deployment spec didn't change), not just its `.log`/`.describe.log` captures
(`bexhoma-sut-postgresql-1-1784910886-3-7bd45c7b95-pwzkz.dbms.log`). So an
agent decoding filenames never needs a special case for the SUT — only code
that resolves a filename back to *which live k8s object* it came from needs
to know that several manifest files can point at the same, still-running
Deployment.

## Whether `report/` exists at all

`report/*.md` is **not** written by default. It only exists when the run
passed `-rp`/`--report` (any entry script, or `bexhoma summary -e <code> -rp`
run later against the same result folder — no live cluster connection
needed either way). An agent that has not confirmed `-rp` was used must plan
to read the raw files listed under `provenance:` above directly — start from
`connections.config` (what ran) and `queries.config` (workload identity +
`workflow_planned`), rather than assuming `report/index.md` exists.

## Key metric per benchmark type

The `key_metric_present` validity check and `report/index.md`'s Key Metrics
block both test the same column(s), one set per benchmark type — this is the
column an agent should treat as "the" headline number:

| Benchmark type | Entry script | Key metric column(s) |
|---|---|---|
| DBMSBenchmarker (TPC-H/TPC-DS) | `tpch.py`, `tpcds.py` | `Geo Times [s]`, `Power@Size [~Q/h]`, `Throughput@Size` |
| YCSB | `ycsb.py` | `[OVERALL].Throughput(ops/sec)` (loading and benchmarking phase, tested separately) |
| HammerDB TPC-C | `hammerdb.py` | `NOPM` |
| Benchbase | `benchbase.py` | `Throughput (requests/second)` |
| Hardware (fio/sysbench/sockperf/netperf) | `hardware.py` | IOPS / CPU events-per-sec / message rate / transaction rate, per active probe |

## Known gaps versus an idealized contract

- **Image tags are recorded; digests are not, and `dbmsbenchmarker`'s own
  version isn't either.** Every manifest actually submitted to the cluster
  — SUT deployment, loader/generator/benchmarker jobs, monitoring sidecars —
  is written into the result folder by `clusters.py::create_object_from_file()`
  *after* its `BEXHOMA_PACKAGE_VERSION` placeholder is substituted with the
  real installed bexhoma version, so every `image:` field in
  `provenance.workflow`'s `*.yml` files is a concrete tag (e.g.
  `postgres:18.3`, `bexhoma/benchmarker_dbmsbenchmarker:0.9.8`,
  `gcr.io/cadvisor/cadvisor:v0.47.0`) — this is the source an agent should
  read for versions, not `connections.config`'s `dockerimage` field alone
  (which does carry the SUT's own resolved tag once the SUT has started,
  via `configurations/benchmarking.py:127`, but is a narrower single-image
  view). What's still genuinely missing: a **sha256 digest** (a tag can be
  re-pushed to point at different bytes) and the **`dbmsbenchmarker`
  package version** specifically — it's baked inside the
  `bexhoma/benchmarker_dbmsbenchmarker` image, whose own tag tracks
  bexhoma's version, not dbmsbenchmarker's.
- **No comparative/historical validity check.** Every validity test is
  *absolute* (pass/fail/skip against this run's own data); there is no
  archived-corridor or cross-run regression check. "Compare only within this
  experiment code" (see every `index.md`'s Interpretation Rules) is a rule an
  agent must apply itself — nothing in the result folder does it automatically.
  `contract_catalog.yml`'s `experiment_schema.fields.follow_up_of` lets an
  experiment.yml record which prior experiment_code it follows up on, but
  that's bookkeeping only — nothing reads or validates it yet.
- **Per-system post_load selection isn't a queryable field.** A catalog-driven
  experiment can choose, per named system, whether indexes/constraints/
  statistics were applied after loading (`contract_catalog.yml`'s `systems[].post_load`
  — see [Design-Catalog-Contract.md](Design-Catalog-Contract.md)'s "Validation
  ordering"). `connections.config`/`queries.config` record *which* SUT ran,
  not *which post-load steps* it received — an agent has to fall back to
  tier-3's `*-loading-*.sql.log` (the rendered DDL source, per
  `provenance.loading` above) and check for `CREATE INDEX`/constraint/`ANALYZE`
  statements itself.

## See also

- [`AgentWorkflow.md`](AgentWorkflow.md) — the end-to-end loop this contract
  is one half of: question → contracts → `experiment.yml` → validate → run →
  answer.
- [`AgentCatalogContract.md`](AgentCatalogContract.md) — the input-side
  counterpart: what a valid `experiment.yml` may contain.
- [`AgentReport.md`](AgentReport.md) — design rationale for the tiered report,
  `index.md`'s eleven sections, the Full Metric Catalog.
- `bexhoma/report_writer.py` module docstring — the same output contract,
  embedded next to the code that implements it.
- `bexhoma/experiments/README.md` §9 — full `show_summary()` call graph,
  per-benchmark-type evaluator/column details, result-folder file naming for
  every benchmarker type (§7).
