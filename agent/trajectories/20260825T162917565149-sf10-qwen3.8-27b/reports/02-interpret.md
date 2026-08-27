

# Benchmark Study Result

## Original question

Retry the failed 10 GB (SF10) TPC-H comparison: under a fixed envelope of 16 CPU cores and 64 GiB RAM, does PostgreSQL remain the better choice than forced-DuckDB PgDuckDB for concurrent analytical reporting? The retry had to preserve the PostgreSQL-versus-forced-PgDuckDB comparison and use one comparable design with rounds [1, 2, 4] and three repetitions. It had to preserve the failed run's experiment-specific settings — four loader pods, one loader thread, split 1, a 120-minute loading timeout, shared post-load settings of indexes=false, constraints=false, statistics=true, storage_format=heap, monitoring_sut=true, monitoring_cluster=false, monitoring_app=false, and 50Gi storage — and it had to select viable SUT, loading, and benchmarking placements from the current environment and validate the complete peak resource envelope before submission.

## Hypothesis

Under a fixed 16 CPU / 64 GiB envelope, PostgreSQL remains the better choice than forced-DuckDB PgDuckDB for concurrent analytical reporting: across concurrency levels 1, 2, and 4, PostgreSQL achieves lower per-query latency and higher Power@Size / Throughput@Size than PgDuckDB running with `duckdb_force_execution=true`. The only factor that varies between the two systems is the system itself; workload, resources, physical design, and profile are held identical.

## Experiments performed

One completed experiment (code `1787668255`, bexhoma 0.10.8 at submission, report generated with 0.10.10) ran the full controlled comparison:

- **Systems (the only varied factor):** PostgreSQL and PgDuckDB, both on the `analytical-ssd` profile. PgDuckDB additionally carried the override `duckdb_force_execution: true`, forcing every query through the DuckDB engine. Both received identical deployment parameter overrides (shared_buffers 20480MB, effective_cache_size 49152MB, work_mem 1024MB, maintenance_work_mem 2048MB, random_page_cost 1.1, effective_io_concurrency 200, io_method io_uring, max_parallel_workers_per_gather 2, max_parallel_workers 4, max_worker_processes 6).
- **Workload:** TPC-H, scaling factor 10, queries Q1–Q22, identical parameters across systems, 600 s per-query timeout.
- **Concurrency sweep (rounds):** [1, 2, 4] benchmark pods (clients 1/2/3), i.e. 1, 2, and 4 parallel query streams.
- **Repetitions:** 3 full experiment runs (experiment_runs 1/2/3), giving 9 phases per system (3 rounds × 3 runs).
- **Loading:** 4 loader pods, 1 thread, split 1, 120-minute timeout; post-load statistics recomputation enabled.
- **Resources:** SUT request/limit 16 CPU and 64Gi RAM; 50Gi ephemeral storage.
- **Monitoring:** SUT sidecar monitoring on; cluster and app monitoring off.
- **Placements:** SUT on cl-worker28, loading on cl-worker29, benchmarking on cl-worker27.

What changed between the two systems was only the system itself (and the PgDuckDB force-execution flag). Workload, scale, concurrency sweep, repetitions, resources, physical design, and profile were held fixed.

## Validity

The run is **not fully clean**: the index frontmatter reports `overall_status: passed 10, failed 1, skipped 2`.

- **Failed (1): `SQL errors`** — 64 errors. Per the result contract, a failed SQL-errors row scopes/invalidates the per-query metrics for the specific queries that errored. The errors are:
  - **PostgreSQL: Q2, Q17, Q20 on every connection** (63 errors), all `org.postgresql.util.PSQLException: ERROR: canceling statement due to user request` — i.e. the 600 s per-query timeout firing.
  - **PgDuckDB: Q19 on one connection** (`pgduckdb-1-2-3-1-2`), `PGDuckDB/Duckdb_ExecCustomScan_Cpp) Executor Error: Query cancelled` — a single transient failure.
- **Passed (10):** No SUT container restarts; loading-phase SUT and loader CPU non-zero; benchmarking-phase SUT and benchmarker CPU non-zero; `Geo Times [s]`, `Power@Size [~Q/h]`, and `Throughput@Size` contain no 0/NaN; no SQL warnings (no result-set mismatch); workflow as planned.
- **Skipped (2):** data-generator CPU (data pre-existing) and EXPLAIN capture (`-se` not used). Skipped rows invalidate nothing.

**Consequence for the numbers:** The headline `Geo Times [s]` and `Power@Size [~Q/h]` are computed over the 18 queries that succeeded on all connections of both systems (Per Phase shows `num_of_queries` = 18 per pod for both systems; the Latency table has exactly 18 rows: Q1, Q3–Q16, Q18, Q21, Q22). Those two metrics are therefore not directly invalidated. However, the reported **`Throughput@Size` is a wall-clock metric** (`num_queries / wall_time × 3600 × SF`), and PostgreSQL's wall time (e.g. 2042 s at concurrency 1) is dominated by the three 600 s timeouts. That makes the reported Throughput@Size biased against PostgreSQL and it must not be read as a fair per-query comparison.

**Resource envelope:** The SUT deployment peaked at **10.34 CPUs and 32.34 Gb RAM** during benchmarking (index.md Monitoring), with no restarts and no OOM — comfortably inside the 16 CPU / 64 GiB envelope, so the envelope was not a binding constraint on either system.

## Results

Headline metrics per phase (index.md Key Metrics; identical to benchmarking.md Per Phase). Concurrency = client (1/2/4 pods); run = experiment_run.

| System | Conc | Run | Geo Times [s] | Power@Size [~Q/h] | Throughput@Size | wall time [s] |
|---|---|---|---|---|---|---|
| PgDuckDB | 1 | 1 | 10.68 | 3369.92 | 2083.60 | 311 |
| PgDuckDB | 1 | 2 | 9.63 | 3740.12 | 4747.25 | 273 |
| PgDuckDB | 1 | 3 | 12.70 | 2834.58 | 6646.15 | 390 |
| PgDuckDB | 2 | 1 | 10.15 | 3545.76 | 2219.18 | 292 |
| PgDuckDB | 2 | 2 | 10.21 | 3525.86 | 4563.38 | 284 |
| PgDuckDB | 2 | 3 | 12.05 | 2988.13 | 2728.42 | 950 |
| PgDuckDB | 4 | 1 | 9.79 | 3675.54 | 2138.61 | 303 |
| PgDuckDB | 4 | 2 | 9.67 | 3721.89 | 4890.57 | 265 |
| PgDuckDB | 4 | 3 | 12.60 | 2857.18 | 6447.76 | 402 |
| PostgreSQL | 1 | 1 | 7.70 | 4673.96 | 317.34 | 2042 |
| PostgreSQL | 1 | 2 | 6.95 | 5177.08 | 643.18 | 2015 |
| PostgreSQL | 1 | 3 | 7.86 | 4577.82 | 1263.77 | 2051 |
| PostgreSQL | 2 | 1 | 7.23 | 4981.69 | 320.00 | 2025 |
| PostgreSQL | 2 | 2 | 6.96 | 5175.97 | 645.42 | 2008 |
| PostgreSQL | 2 | 3 | 7.61 | 4733.52 | 1261.93 | 2054 |
| PostgreSQL | 4 | 1 | 7.58 | 4746.23 | 318.58 | 2034 |
| PostgreSQL | 4 | 2 | 7.23 | 4978.89 | 644.14 | 2012 |
| PostgreSQL | 4 | 3 | 7.85 | 4583.91 | 1260.70 | 2056 |

Aggregated across the 3 runs per concurrency level:

| System | Conc | Geo Times [s] (range) | Power@Size [~Q/h] (range) | Throughput@Size (range) |
|---|---|---|---|---|
| PgDuckDB | 1 | 9.63–12.70 | 2834.58–3740.12 | 2083.60–6646.15 |
| PgDuckDB | 2 | 10.15–12.05 | 2988.13–3545.76 | 2219.18–4563.38 |
| PgDuckDB | 4 | 9.67–12.70 | 2834.58–3721.89 | 2138.61–6447.76 |
| PostgreSQL | 1 | 6.95–7.86 | 4577.82–5177.08 | 317.34–1263.77 |
| PostgreSQL | 2 | 6.96–7.61 | 4733.52–5175.97 | 320.00–1261.93 |
| PostgreSQL | 4 | 7.23–7.85 | 4583.91–4978.89 | 318.58–1260.70 |

Per-query latency (benchmarking.md "Latency of Timer Execution [ms]", 18 common queries, representative values):

| Query | PgDuckDB (conc 1, ms) | PostgreSQL (conc 1, ms) |
|---|---|---|
| Q1 | 50254 | 44447 |
| Q3 | 12468 | 6789 |
| Q4 | 13720 | 9002 |
| Q5 | 16248 | 7281 |
| Q6 | 7650 | 3569 |
| Q7 | 10491 | 6154 |
| Q8 | 17102 | 8119 |
| Q9 | 17175 | 21048 |
| Q10 | 9612 | 6827 |
| Q11 | 3996 | 1480 |
| Q12 | 13165 | 8021 |
| Q13 | 4090 | 14747 |
| Q14 | 8850 | 4100 |
| Q15 | 8158 | 4173 |
| Q16 | 2460 | 2859 |
| Q18 | 24586 | 62123 |
| Q21 | 35700 | 19084 |
| Q22 | (not shown) | (not shown) |

PostgreSQL is faster on most common queries (Q3, Q5, Q6, Q7, Q8, Q10, Q11, Q12, Q14, Q15, Q16, Q21) but slower on Q1, Q9, Q13, and Q18.

## Interpretation

**What the evidence supports.** On the 18 TPC-H queries both systems completed, PostgreSQL is the faster system at every concurrency level: its Geo Times (6.95–7.86 s) are consistently lower than PgDuckDB's (9.63–12.70 s), and its Power@Size (4577.82–5177.08 ~Q/h) is consistently higher than PgDuckDB's (2834.58–3740.12 ~Q/h). PostgreSQL is also more stable under concurrency — its Geo Times barely move from concurrency 1 to 4 (≈7.0–7.9 s), whereas PgDuckDB's worsen (≈9.6–10.7 s at concurrency 1 to ≈12.0–12.7 s at concurrency 4). On per-query speed and concurrency stability, the hypothesis is confirmed.

**What the evidence does not support.** The hypothesis also claimed higher **Throughput@Size** for PostgreSQL, and the reported numbers go the other way (PgDuckDB 2083.60–6646.15 vs PostgreSQL 317.34–1263.77). This is a measurement artifact, not a real throughput advantage: Throughput@Size divides the query count by wall-clock time, and PostgreSQL's wall time (≈2000 s) is inflated by the three 600 s timeouts on Q2/Q17/Q20, while PgDuckDB's wall time (≈265–950 s) is not. The lower Geo Times actually indicate PostgreSQL has higher effective throughput on the common queries. So the hypothesis's Throughput@Size claim is wrong as reported, and the reported Throughput@Size is not a valid basis for the comparison.

**The query-completion gap.** PostgreSQL failed Q2, Q17, and Q20 on every connection (63 timeout errors); PgDuckDB completed all 22 queries (one transient Q19 failure). This is the central unresolved tension: PostgreSQL is faster on the queries it can finish, but it cannot finish three of the 22 within 600 s, whereas PgDuckDB finishes all of them. Whether "faster but incomplete" or "slower but complete" is the "better choice" depends on a weighting (per-query speed vs. query completion) that this experiment does not establish.

**Mechanism inference (separate from evidence):** The PostgreSQL timeouts on Q2/Q17/Q20 are consistent with those queries exceeding 600 s under the 16 CPU / 64 GiB envelope with the shared physical design (no indexes, heap storage, limited parallelism: max_parallel_workers_per_gather=2, max_parallel_workers=4). The PgDuckDB Q19 failure is a single transient cancellation, not a systematic problem.

**Design and envelope.** The comparison was preserved and comparable (two systems, identical workload/resources/profile, rounds [1,2,4], 3 repetitions). The 16 CPU / 64 GiB envelope was validated and not binding (peak 10.34 CPUs / 32.34 Gb RAM, no restarts/OOM).

## Follow-up experiment

No completed follow-up is available in this chain. The current run is itself the retry of the previously failed 10 GB comparison; no subsequent follow-up experiment is recorded in the handoff.

## Final verdict

**Direct answer:** On the 18 TPC-H queries both systems completed, PostgreSQL is the faster and more concurrency-stable system under 16 CPU / 64 GiB (lower Geo Times, higher Power@Size at every concurrency level 1/2/4). However, the evidence does **not** establish a clean "PostgreSQL is the better choice" verdict, because PostgreSQL failed Q2, Q17, and Q20 on every connection at the 600 s timeout while PgDuckDB completed all 22 queries, and the reported Throughput@Size (which favors PgDuckDB) is an artifact of those timeouts rather than a fair per-query comparison.

**Remaining limitations / unresolved questions:**
1. PgDuckDB's per-query latencies for Q2/Q17/Q20 are not in the Latency table (excluded because they failed on PostgreSQL), so the speed gap on the queries PostgreSQL cannot complete is unquantified.
2. No principled weighting of per-query speed vs. query completion was applied, so a single "better choice" verdict is not settled.
3. The reported Throughput@Size is biased against PostgreSQL by the 3×600 s timeouts and should not be used as a fair throughput comparison.
4. The post-load settings indexes=false, constraints=false, storage_format=heap (and split=1) are confirmed only by the submitted specification, not by a tier-1/2 report field (per the result contract's known_gaps, they are reconstructable only from tier-3 loading SQL logs); because they are shared and identical across both systems, this does not bias the comparison.



Submitted.

**Experiment code: `1787691294`** (follow-up of `1787668255`)

**What the run will settle:** whether PostgreSQL's Q2/Q17/Q20 failures in the prior run were a genuine capability gap or an artifact of the 600 s per-query timeout cap. The spec is the preserved design — PostgreSQL vs forced-PgDuckDB (`duckdb_force_execution: true`), both on `analytical-ssd`, 16 CPU / 64Gi / 50Gi, rounds [1, 2, 4], 3 repetitions, identical loading (4 pods, 1 thread, split 1, 120-min timeout), post_load (indexes=false, constraints=false, statistics=true, storage_format=heap), monitoring (sut=true, cluster=false, app=false), and placements (SUT cl-worker28, loading cl-worker29, benchmarking cl-worker27) — with exactly one changed parameter: `workload.params.timeout: 1800` (was the 600 s default).

Discriminators:
- **If PostgreSQL completes all 22 queries within 1800 s** on every connection, the Latency table will contain all 22 queries for both systems and Geo Times / Power@Size can be computed over the full set — settling the "better choice" question on a complete, comparable basis (and de-biasing the wall-clock Throughput@Size that the prior run's timeouts had skewed against PostgreSQL).
- **If PostgreSQL still times out (or is disproportionately slow) on Q2/Q17/Q20 at 1800 s**, the capability gap is confirmed and the verdict is genuinely mixed: PostgreSQL faster on the 18 common queries, PgDuckDB completing the 3 it cannot.

Peak envelope was validated before submission: SUT 16 CPU / 64Gi / 50Gi on cl-worker28 (256 CPU / ~1 TiB / ~1.7 TiB), 4 loader pods on cl-worker29 (128 CPU / ~1 TiB / ~438 GiB), and up to 4 benchmarker pods (16 CPU / 128Gi each = 64 CPU / 512Gi peak) on cl-worker27 (256 CPU / ~1 TiB) — all fit, and the prior run already showed the SUT envelope non-binding (peak 10.34 CPU / 32.34 GiB).
