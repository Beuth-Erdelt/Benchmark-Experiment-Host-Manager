

## Interpretation

**Trustworthy? Yes — both sides of the comparison are sound.** The follow-up run (`1787179264`, `duckdb_force_execution=false`) passed all 7 validity checks (`report/index.md`: `overall_status: passed 7 / failed 0 / skipped 0`): no SUT container restarts, no SQL errors, no SQL warnings, no 0/NaN in the headline metrics, and the workflow ran as planned. The forced-side run (`1787175665`) passed the same 7/7. Since the contract says cross-code comparability is the agent's responsibility, I verified it directly: both `index.md` Workload sections are identical (TPC-H SF1, Q1–Q22, 2 repeats, 3 repetitions, rounds [1, 8], 16 CPU / 64 GiB on `cl-worker36`, bexhoma 0.10.8, byte-identical deployment parameter overrides) — the only difference is the force flag. The two runs are directly comparable.

**Overall recommendation: leave cost-based routing at default (`duckdb_force_execution=false`).** It wins at both concurrency levels, across all three repetitions:

| Streams | Geo Times forced (s) | Geo Times default (s) | Throughput@Size forced | Throughput@Size default |
|---|---|---|---|---|
| 1 | 0.51 / 0.56 / 0.58 | 0.23 / 0.26 / 0.26 | 2933 / 2400 / 2329 | 4659 / 3960 / 3600 |
| 8 | 0.83 / 0.82 / 0.83 | 0.29 / 0.32 / 0.33 | 12931 / 13200 / 12672 | 24369 / 17600 / 18635 |

(From the Key Metrics tables in `1787175665/report/index.md` and `1787179264/report/index.md`.) Default routing is ~2.1× faster on Geo Times at 1 stream (median 0.26 s vs 0.56 s) and ~2.6× at 8 streams (0.32 s vs 0.83 s); Throughput@Size is ~1.65× higher at 1 stream (3960 vs 2400 Q/h) and ~1.4× at 8 streams (18635 vs 13200 Q/h). Forcing every query through DuckDB is a clear net loss on this workload.

**Consistency across query shapes: consistent across concurrency, but not uniform across queries — 5 of 22 favor the opposite mode.** The per-query comparison (both `execution.md` files, 3/3 matched runs for every query) shows the *same* split at 1 and 8 streams: default wins 17/22, forced wins 5/22, no ties.

- **Favor forced execution (the exceptions):** Q1 (+14.3% at 1 stream, +58.4% at 8), Q13 (+133.1% / +55.3%), Q14 (+169.4% / +286.0%, with high variance in default mode — range up to ~2.96 s at 8 streams), Q16 (+7.6% / +29.1%), Q18 (+327.1% at 1 stream, +72.1% at 8).
- **Favor default routing (the 17):** the biggest wins are Q19 (−92.6% / −96.6%), Q20 (−85.7% / −91.0%), Q8 (−89.8% / −89.9%), Q4 (−80.1% / −82.3%), Q21 (−78.4% / −79.6%), Q5 (−79.8% / −74.4%), Q11 (−74.3% / −78.7%) — i.e., the simple filter/aggregate and join-heavy shapes where the PostgreSQL side of the router clearly does the better job.

**What the hypothesis got right:** the design premise — that the two sides must be measured with identical setups and compared overall and per query shape — was exactly what produced a decisive answer. The hypothesis's implicit expectation that cost-based routing might be competitive with forced execution is confirmed in one direction: routing is not just adequate, it is substantially better overall, and the per-query data shows *why* — the router correctly keeps a majority of TPC-H shapes off the DuckDB executor, while a handful of shapes (Q1, Q13, Q14, Q16, Q18) are the ones where forcing would have helped.
