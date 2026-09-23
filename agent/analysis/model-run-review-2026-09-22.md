# Review of the Glimmer and Gemma benchmark investigations

Reviewed on 2026-09-22. This review uses the local archived results under
`~/benchmarks/agent`. It selects an initial implementation from the
[handbook improvement proposal](handbook-improvement-plan-2026-09-22.md).

## Decision

**Start with compact, query-specific evidence and a procedure that keeps the
verdict within that evidence.** The clearest observed problem is the jump from
an aggregate measurement to a broader scientific conclusion. The existing
structured checks catch some numerical claims, but do not establish that the
free-text conclusion is justified.

The first increment now exposes per-query timings and localized query failures
through the existing assessment tool. Handbook 0.6.0 adds a verdict procedure in
M7 and corrects M2.9's overstatement about resource utilization. This is an
implementation of proposed improvements 1 and 5, with compact context relevant
to interpretation. It is not yet evidence that either model's answers improve.

## Which investigations were reviewed

Both investigations ask: “Is pg_duckdb faster than PostgreSQL for aggregation
under concurrency, and does that depend on how many cores we give it? We have a
10 GB dataset and 64 GB of RAM.”

| Property | Glimmer investigation | Gemma investigation |
|---|---|---|
| Recorded model | `meta-models/Muse-Glimmer-30B` | `google/gemma-4-31b-it` |
| Result code | `1790026202` | `1790080023` |
| CPU allocations | 32 and 64 cores. | 8 and 32 cores. |
| Concurrency | 1, 4 and 8. | 1, 4 and 8. |
| Repetitions | Three per condition. | Three per condition. |
| Planned queries | TPC-H Q1, Q13 and Q18. | TPC-H Q1, Q13 and Q18. |
| Reported mechanical failures | Zero. | Two failed check categories: restarts and SQL errors. |
| Final recorded scientific verdict | Refuted; both user questions marked settled. | Supported; both user questions marked settled. |

The standalone Glimmer design directory and the bare-model answers were not
treated as additional completed benchmark results. For Gemma, both the earlier
interpretation and the final repeated interpretation were inspected.

These investigations do **not** support a controlled ranking of the two models.
They use different CPU ranges, tuning overrides, preparation choices, handbook
fingerprints, harness versions and serving arrangements. Glimmer requested
post-load indexes; Gemma explicitly raised parallel-worker settings. Gemma's
hypothesis also strengthens “does that depend” into “this advantage increases.”
The measured performance differences cannot be attributed to model choice alone.

## What Glimmer got right and where its conclusion goes too far

The archived per-query execution table shows lower mean times for PgDuckDB on
Q1, Q13 and Q18 at every matched CPU/concurrency condition. Its aggregate
comparison is therefore consistent with this component evidence for the tested
workload. The report records complete coverage and no failed checks.

Its stronger CPU conclusion deserves qualification. At concurrency 8, for
example, mean phase Geo Times change from 9.927 to 9.867 seconds for PgDuckDB
and from 19.337 to 19.403 seconds for PostgreSQL when allocation rises from 32
to 64 cores. These are descriptive means over three phase repetitions.
They support describing little movement in this metric under these conditions.
They do not establish general CPU independence, an explanation for the flat
result, or equivalence within a predeclared practically important margin.

The assessor's `flat` label is a descriptive classification, not an equivalence
test. Glimmer used that label to mark the broader core-dependence question
settled. The appropriate improvement is to require a statement of tested scope
and remaining uncertainty. It would be equally wrong to say that the resource
change was never tested solely because monitored utilization was low. That is
why the first increment corrects M2.9 instead of enforcing its old wording.

## What Gemma missed

### The query rankings differ

Gemma's final answer says PgDuckDB consistently outperforms PostgreSQL and uses
the phase Geo Times as its principal evidence. The per-query execution timings
show a more specific result. At **32 cores and concurrency 8**:

| Query | PgDuckDB mean execution time | PostgreSQL mean execution time | Observed faster mean |
|---|---:|---:|---|
| Q1 | 13,153.72 ms | 8,882.32 ms | PostgreSQL. |
| Q13 | 2,417.37 ms | 10,456.08 ms | PgDuckDB. |

For each query, these numbers first average the connection timings within a
phase and then average the three phase means. The Q1 phase-mean ranges are
12,750.35–13,808.41 ms for PgDuckDB and 8,639.25–9,207.65 ms for PostgreSQL.
They are observed ranges, not confidence intervals. Other validity limitations,
including restart effects, remain unresolved.

PostgreSQL also has the lower Q1 mean at 32 cores with concurrency 1 and 4,
and at 8 cores with concurrency 1. An overall metric can favor PgDuckDB while
a particular query favors PostgreSQL. The final answer omits this distinction.
These query execution timings are not interchangeable with phase Geo Times;
they must be reported with their own metric definition.

### Failure scope was exaggerated

The SQL error table records 48 Q18 errors: eight connections in each of six
PostgreSQL phases, covering both CPU allocations and three repetitions, all at
**concurrency 8**. It does not report Q18 errors at concurrency 1 or 4.
Gemma's final claim that Q18 failed “across all configurations” obscures this
load-specific scope and is misleading if read as every tested condition.

The compact latency table contains Q1 and Q13, while the phase table counts
two queries per stream for both database systems. This does not mean Q18
failed everywhere, nor does the aggregate's name prove which query observations
it includes. Gemma's claim that PostgreSQL's Geo Times underestimate its time
because PostgreSQL omitted Q18 while PgDuckDB's figure includes all three is
not established by these tables. Establish metric membership from provenance or
use the explicitly identified per-query evidence.

Completion failures are relevant operational evidence. They are not successful
execution times and do not by themselves prove a speed advantage. Likewise,
successful Q1 and Q13 timings do not establish that the recorded PostgreSQL
restarts had no influence on those measurements.

### The correction loop repaired the record without repairing its meaning

In the Gemma trajectory, the earlier interpretation recorded an inconclusive
verdict and proposed a targeted Q18 follow-up. That follow-up validated but
submission was refused three times because the runtime considered another
experiment active. The subsequent interpretation of the same result switched
to a supported verdict and a decision to finish.

During the final interpretation, the assessor withheld automated factor claims
because of incomplete query coverage. Gemma nevertheless proposed such claims.
After rejection, it removed the checked claims while retaining the substantive
conclusions in the verdict and question answers. The final record passed.
This is direct evidence of a gap between structural acceptance and scientific
support, not proof that a grammar constraint or more mandatory reads would
solve it.

The final interpretation also exhausted its file-reading budget after 110,000
returned characters. Compact evidence is therefore a concrete way to make
relevant facts easier to find, although a model improvement from that change
has not yet been measured. The new breakdown is approximately 4.4 KB for this
archived report. That size is not an observed token saving from a rerun.

## Reprioritized improvements

| Priority | Work | Reason from these runs |
|---|---|---|
| First, implemented | Add per-query evidence, localized failures, and a source-linked verdict procedure. | The missing facts are present in the archive but do not reach the final conclusion reliably. |
| Next, evaluate | Replay interpretation with the same archived evidence, separately varying the new tool feedback and handbook procedure. | We need to know whether either change alters conclusions rather than only tool use. |
| Next, investigate | Make conclusions explicitly traceable to the particular comparison they use. | Exact copying of checked fields did not prevent unsupported prose. A future gate needs a clear scope model, not a blanket ban on conclusions from partial runs. |
| Later | Add selected worked examples and improve context selection. | Both may help, but current evidence favors fixing the visibility and interpretation of existing measurements first. |
| Later | Consider constrained generation and training. | Gemma produced accepted structure; these interventions have not been shown to fix its scientific inference here. |

The follow-up submission refusal remains part of the interpretation's history.
It is not attributed solely to the model or silently counted as a completed
follow-up experiment. Investigating that operational issue is separate from
this initial evidence improvement.

## What was implemented and what the checks establish

The existing `assess_comparison_quality` tool now includes `query_evidence`.
It retains configuration identity, maps concurrency from the phase table rather
than the client ordinal, and reports query timings with repetition counts and
ranges. It preserves errors by query and phase instead of only by configuration.
It does not emit replacement full-workload claims from a successful subset.

Only complete, positive, finite query timing rows with no recorded query error
are summarized. Missing phase mappings or connection counts leave the compact
timing breakdown unavailable. This is a conservative implementation boundary;
it does not prove that every omitted measurement is scientifically unusable.
The current parser recognizes the existing TPC-H query labels. Other workload
formats retain the prior assessment without an invented query breakdown.

M7's procedure is in an already required handbook chapter. M2.9 now preserves a
narrow flat-result finding and distinguishes a joint tuning/allocation change
from an isolated allocation effect. The prompt describes the new tool fields
and clarifies that deleting a rejected structured claim does not justify it in
prose. Scientific guidance stays in the handbook, preserving the existing
ability to compare behavior with and without handbook access.

The new tests reproduce a query ranking reversal, localized failures, repetition
accounting, invalid timing values, missing connections and unavailable timing
tables. All five tests and five parameterized subtests pass. Replaying the
assessor against the actual archives yields 12 contexts and three queries for
Glimmer, and 12 contexts, two queries and the six affected failure phases for
Gemma.

Before editing, the existing harness test file had 157 passing tests and eight
failures. The final combined run of that file and the new tests had 163 passing
tests, 23 passing subtests and seven failures, all present in the baseline.
The baseline's directory-rename failure did not recur in the final run; it was
not fixed by this change. The remaining failures concern node resource limits,
summary persistence, submission-code uniqueness and phase/CLI behavior.
A final focused run covering query evidence, comparison assessment, result
characterization and interpretation prompts passed all 16 selected tests and
five subtests. The M7 procedure was also checked to be included in the existing
required chapter read.
These checks verify evidence extraction and integration. They do not show that
Glimmer or Gemma will use the evidence correctly. No live model or cluster
experiment was launched for this increment, and the archived runs were not edited.

## Next controlled model evaluation

Hold the model revision, serving settings, archived result, question and budgets
fixed. Compare the corrected handbook baseline with the procedure alone, the
compact feedback alone, and both together. Keep the resource-rule correction
common to all compared conditions. Run several interpretations if the endpoint
is nondeterministic and retain failures rather than selecting the best answer.

Score whether the answer preserves the Q1/Q13 reversal, locates Q18 failures at
concurrency 8, avoids inventing aggregate membership, distinguishes a successful
subset from the full workload, and limits Glimmer's CPU conclusion to the tested
conditions. Also score unnecessary refusal and follow-up cost. Add unseen cases
with complete coverage and different rankings so that blanket inconclusiveness
cannot pass the evaluation. The two reviewed runs are development evidence and
must not be described as an untouched final test set.

## Literature behind the choice

- Gernot Heiser's *Systems Benchmarking Crimes*, sections on benchmark
  subsetting and missing sub-benchmark results, supports examining component
  results and restricting claims from incomplete suites.
  [Primary source](https://gernot-heiser.org/benchmarking-crimes.html).
- Jie Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet*,
  ICLR 2024, finds unreliable intrinsic correction without external feedback in
  the studied reasoning tasks. It motivates testing precise external evidence
  here, but does not demonstrate this implementation's effectiveness.
  [Paper](https://arxiv.org/pdf/2310.01798).
- Tushar Khot et al., *Decomposed Prompting*, ICLR 2023, studies explicit task
  decomposition. The handbook procedure is our adaptation to benchmark
  interpretation, not a result reported in that study.
  [Paper](https://arxiv.org/pdf/2210.02406).

The earlier [literature audit](handbook-literature-audit-2026-09-22.md) remains
the source for the other unresolved handbook corrections. This increment does
not certify the rest of the handbook as fully supported.

## Local evidence and reproducibility

Glimmer's [trajectory](</Users/scydal/benchmarks/agent/incluster-glimmer-20260921/state/investigations/glimmer-20260921/trajectories/20260921T212715597002/trajectory.jsonl>)
records the final verdict at line 160. Its submitted design is beside that
trajectory under `phases/01-design/submitted-experiment.yml`.
The [benchmark tables](</Users/scydal/benchmarks/agent/incluster-glimmer-20260921/state/results/1790026202/report/benchmarking.md>)
provide the underlying measurements.

Gemma's [trajectory](</Users/scydal/benchmarks/agent/incluster-gemma4-openrouter-20260922/out/investigations/gemma4-openrouter-20260922c/trajectories/20260922T122525911463-sf10-google-gemma-4-31b-it/trajectory.jsonl>)
records the earlier accepted interpretation at line 75, refused submissions at
94, 96 and 98, final assessment at 126, claim rejection at 138, and final accepted
record at 142. Its submitted design is beside that trajectory under
`phases/01-design/submitted-experiment.yml`.
Its [benchmark tables](</Users/scydal/benchmarks/agent/incluster-gemma4-openrouter-20260922/out/results/1790080023/report/benchmarking.md>)
contain the query timings and failure locations discussed above.

The reviewed benchmarking file fingerprints are:

| Result | SHA-256 of `report/benchmarking.md` |
|---|---|
| Glimmer `1790026202` | `fa4e538875ec53ef7eaac2e369a29f6753d8cfa9035776890bcb64db18f1f28c` |
| Gemma `1790080023` | `1813e370bb273a9d6cb4b385e7bd7f7a701898c0af9d53b9ac72abfc85a4d08a` |

Hashes identify the reviewed bytes. Local paths require access to the archived
benchmark folder; no credentials or cluster configuration are copied here.
