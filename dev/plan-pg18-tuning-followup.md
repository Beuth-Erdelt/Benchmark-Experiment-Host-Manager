# Plan: PostgreSQL 18 tuning follow-up (default vs. recommended, round 1 results)

Status: **not implemented, held as a plan**. No script changes have been made yet.

## Background

`dev/test-postgres18-tuning.ps1` ran once (5 workloads x Default/Tuned, `-nc 1`
throughout). Results (full detail in the published artifact from that run):

- **YCSB**: tuned wins cleanly (+10.9% throughput, -29.5% update p99 latency,
  read latency unchanged). No follow-up needed.
- **Benchbase TPC-C**: tuned *lost* by -28.8% throughput, +41% avg latency.
- **HammerDB TPC-C**: tuned *lost* by -9.2% NOPM/TPM — same direction as
  Benchbase, on an independent driver running the identical workload.
- **TPC-H**: comparison is not usable. Default completed 0/22 queries, tuned
  completed 2/22 — both hit the base parser's `-t` per-query timeout (default
  600s, never overridden in the script) on nearly the whole query set at
  `-sf 100`, and default also exhausted the 200Gi PVC ("No space left on
  device").
- **TPC-DS**: completed (95/99 queries both variants, a real comparison), but
  tuned lost the single-stream power test by ~19% on Power@Size; the 4-stream
  throughput test was close to a wash. Both variants also hit a handful of
  "No space left on device" errors on the 150Gi PVC.

The TPC-C regression has a specific clue, not just a "worse number": during
the Benchbase run, tuned's SUT peaked at **1.23 CPUs** vs. default's **1.78
CPUs** — lower CPU utilization *and* lower throughput together, which is the
signature of a process blocked on I/O completion rather than one that's
simply doing less work per transaction. `io_method=io_uring` is the one
setting in the tuned `--set` block that changes how Postgres submits/waits on
I/O; every other changed setting (bigger `shared_buffers`, bigger `work_mem`,
higher `effective_io_concurrency`) has no obvious mechanism to hurt TPC-C.
This is a hypothesis, not a proven cause — the tuned block changes 8+
settings at once in the current script.

## Goal

Turn round 1's mostly-negative, partly-broken results into trustworthy
answers: is the regression really `io_method`, and do the OLAP workloads
actually benefit from tuning once the harness itself isn't the bottleneck.

## Action items, in priority order

### 1. Isolate `io_method` for both TPC-C tools (highest priority)

Add a third variant per TPC-C tool in `dev/test-postgres18-tuning.ps1`:
`Test-BenchbaseTpccTunedNoAio` / `Test-HammerdbTpccTunedNoAio` (naming TBD) —
identical to the existing `*Tuned` functions but with the
`io_method=io_uring` `--set` line removed (falls back to PostgreSQL 18's
default `io_method`, currently `worker` per upstream defaults — confirm
against the actual image). Everything else in the tuned block stays.

Driver loop becomes Default -> Tuned -> Tuned-minus-io_uring per TPC-C tool,
still interleaved (not grouped by variant), same reasoning as the existing
driver loop comment.

If Tuned-minus-io_uring recovers most of the throughput lost between Default
and Tuned, that confirms `io_method` as the cause and the fix is just "don't
set io_method=io_uring for TPC-C" (or try `io_method=sync` explicitly as a
fourth variant, matching what `dev/pg-storage.ps1` already uses). If it
doesn't recover, the regression is coming from somewhere else in the block
and `shared_buffers`/`work_mem`/`effective_io_concurrency` need the same
isolation treatment.

### 2. Apply the same isolation to TPC-DS

TPC-DS changed the identical `io_method=io_uring` setting and also regressed
(power test). Add `Test-TpcdsTunedNoAio` alongside the TPC-C variants once
(1) confirms or rules out the hypothesis there — TPC-DS's read-heavy
analytical I/O pattern is different enough from TPC-C's that the same cause
isn't guaranteed, so it needs its own check rather than assuming the TPC-C
result transfers.

### 3. Fix the TPC-H harness before re-running it

Two independent problems, both need fixing together:

- **`-t` (per-query timeout)**: add `-t 1800` (or higher) to both
  `Test-TpchDefault` and `Test-TpchTuned` — the script currently omits `-t`
  entirely, so it runs at the base parser's default of 600s, which round 1
  showed is nowhere near enough for `-sf 100` TPC-H on this hardware, tuned
  or not.
- **PVC size**: raise `-rss` past 200Gi, or first check actual peak disk
  usage from a completed run to size it properly instead of guessing again.
- Given round 1 got 0-2/22 queries through even with more time budget than a
  simple `-t` bump might buy, consider dropping to a smaller scale factor
  (e.g. `-sf 30`) for a first re-run that actually completes, then step back
  up to `-sf 100` once a full run is confirmed feasible in a reasonable
  timeout. Don't jump straight back to `-sf 100` with just a timeout fix and
  assume it'll finish.

### 4. Raise TPC-DS's PVC size too

Both TPC-DS variants hit "No space left on device" a handful of times even
though the run mostly completed (95/99 queries). Raise `-rss` past 150Gi so
those queries stop failing and the comparison isn't losing a few data points
to disk exhaustion.

### 5. Add repetitions once the above are fixed

Every number from round 1 is `-nc 1`. Before trusting any magnitude from a
re-run — especially the TPC-DS throughput-test near-wash, which could easily
flip with a second sample — add `-nc 3` the same way
`dev/test-storage-oltp-olap.ps1` did for its noisiest profiles. Do this last,
after the isolation and harness fixes above, since repeating a broken
comparison (TPC-H at the current timeout/PVC size) just burns time producing
three broken samples instead of one.

## Explicitly out of scope for this plan

- Re-deriving the YCSB settings — round 1 already confirmed them; no changes
  proposed here.
- Changing the OLTP/OLAP storage-class choices (`shared` / `cephcsi`) — those
  came from the separate `dev/test-storage-oltp-olap.ps1` round-3 findings
  and aren't implicated by this round's results.
