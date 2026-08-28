

## Interpretation: TPC-H SF10 — PostgreSQL vs forced-PgDuckDB at 16 CPU / 64 GiB, 1800 s timeout

### What was tested

This run (code 1787691294) retried the failed 10 GB TPC-H comparison with the per-query timeout raised from 600 s to 1800 s. Both systems (PostgreSQL and PgDuckDB with `duckdb_force_execution=true`) ran the full 22-query TPC-H workload at SF10 under a fixed 16 CPU / 64 GiB envelope, with concurrency rounds [1, 2, 4] and 3 repetitions. All other settings (4 loader pods, 1 thread, split 1, 120-min load timeout, indexes=false, constraints=false, statistics=true, heap storage, 50 GiB storage) were preserved from the prior run.

### Validity

**One check failed: SQL errors (50 errors).** This scopes per-query metrics for the specific queries that errored. All other checks passed (no SUT restarts, monitoring present, workflow as planned, no SQL warnings, key metric columns free of 0/NaN). Whole-workload throughput is **not comparable** because the two systems did not complete the same set of queries.

### What the numbers show

**PostgreSQL still fails Q2, Q17, and Q20 at 1800 s.** Every error for these three queries is `canceling statement due to user request` (i.e., the 1800 s timeout fired). This occurs across all three experiment runs and all concurrency levels. The hypothesis that the prior 600 s cap was the sole cause of PostgreSQL's Q2/Q17/Q20 failures is **disproven**.

**PgDuckDB fails only Q1**, and only once (connection `pgduckdb-1-1-3-1-4`, error: `Query cancelled`). All other 21 queries complete.

**On the 18 queries both systems completed, PostgreSQL is faster at every concurrency level** (from `report/indexagent/trajectories/20260825T162917565149-sf10-qwen3.8-27b/phases/04-interpret.md` Key Metrics):

| Concurrency | PostgreSQL Geo Times [s] | PgDuckDB Geo Times [s] | PostgreSQL Power@Size | PgDuckDB Power@Size |
|---|---|---|---|---|
| 1 | 6.54 – 7.23 | 9.12 – 11.06 | 4977 – 5508 | 3254 – 3949 |
| 2 | 6.25 – 7.30 | 8.99 – 11.95 | 4930 – 5761 | 3013 – 4005 |
| 4 | 1.09 – 1.19 ⚠️ | 9.40 – 11.99 | 30292 – 32882 ⚠️ | 3003 – 3828 |

⚠️ **Suspect repetitions:** All three PostgreSQL run-3 phases (clients 1, 2, 3) show Geo Times of ~1.1 s, a 5.4–6.7× deviation from the peer median (~6.4–7.3 s). The deterministic assessment flags these as `suspect_not_invalid`. The direction (PostgreSQL faster) is consistent with runs 1 and 2, but the magnitude at concurrency 4 is not trustworthy.

### Verdict on the question

The question "does PostgreSQL remain the better choice than forced-PgDuckDB for concurrent analytical reporting?" is **partially answered**:

- **Speed on common queries:** Yes — PostgreSQL is consistently faster (roughly 1.4–1.7× lower Geo Times) on the 18 queries both systems complete, at all three concurrency levels.
- **Workload completion:** No clean answer. PostgreSQL fails 3 of 22 queries (Q2, Q17, Q20) even at 1800 s; PgDuckDB fails 1 of 22 (Q1). If the reporting workload requires all 22 queries to complete, neither system is a clean "better choice," but PgDuckDB is closer. If the 3 failing PostgreSQL queries are acceptable to exclude or handle separately, PostgreSQL's speed advantage is clear.
- **The timeout hypothesis is dead:** Extending the timeout from 600 s to 1800 s did not fix PostgreSQL's Q2/Q17/Q20. These queries genuinely exceed 1800 s under this resource envelope.

### Recommended follow-up

Run **only Q2, Q17, and Q20** on PostgreSQL with a **3600 s per-query timeout** under the same 16 CPU / 64 GiB envelope and identical physical design. This is the smallest controlled intervention that discriminates between "timeout-cap artifact" (queries complete given more time) and "genuine capability gap" (queries cannot complete within any reasonable time at this resource level). The full 22-query workload is not needed for this question.
