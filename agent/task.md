# Task brief: an experiment design handbook beside the two contracts

Design brief for a future working session. This is not the benchmark question
the Kubernetes lifecycle controller reads — that is still `task.txt` in the
controller's input directory, one question and nothing else.

Written 2026-08-27. The handbook it proposes now exists as
`agent/experiment_design_handbook.md` and is integrated: the design phase and
the follow-up author must read its Navigation chapter before acting, its digest
is recorded in every trajectory, and the four principles it designates as
decidable are enforced by the validator and cited by identifier. What remains
open are the questions at the end of this brief.

## The problem

The prototype has two contracts. The catalog says what an experiment may
express: the workloads, the systems, the parameters, their legal values. The
result contract says what may be claimed once a run finishes, and how the
evidence has to be read. Neither says how to turn a research question into a
sound experiment.

That third thing is method, and today it exists only inside whatever the model
absorbed during training. The agent is therefore only as good at experimental
design as its own priors, which is exactly the assumption the paper should not
be resting on.

The evidence is in this session's trajectories. Asked for a quick YCSB example
on PostgreSQL, Mistral Small produced a specification that is legal, submits,
and runs — the isolated factor is honest and matches what the experiment
actually varies. It also:

- stated a hypothesis no measurement can contradict ("acceptable throughput and
  latency", with no threshold);
- capped each client at a fixed operation rate and then framed the result as a
  throughput claim, so the number it will report is a property of its own
  setting rather than of the database;
- left the CPU and memory request below the limit, so the pod's real share can
  differ between the two concurrency levels it is comparing;
- ran one repetition, leaving no way to separate an effect from noise; and
- throttled the load phase as well, so most of the hour is spent inserting rows
  slowly for no measurement benefit.

None of these are contract violations. All of them are methodology.

## Why more validator rules are not the answer on their own

Two different kinds of defect are hiding in that list.

Some are decidable properties of the specification. Whether a hypothesis states
any criterion at all, and whether a comparison holds its resource envelope
fixed, can be checked mechanically, and probably should be.

The rest are judgments about the relationship between the claim and the design:
whether a throttled run can support a throughput claim, whether a dataset that
fits entirely in memory measures what the question was about, whether the
chosen factor is the one that would actually discriminate. That space is
unbounded. No list of rules closes it.

So the validator is not the wrong tool, it is the wrong primary tool. It can
say "this is illegal". It cannot say "this is a bad experiment".

## The proposal

Add a handbook of experimental method as a third input — guidance rather than
a contract — read by the agent before it designs, versioned, and hashed into the
trajectory beside the catalog and the cluster descriptor.

Content is a distillation of existing literature, not original work. The
sources worth mining: the standard catalogue of database benchmarking pitfalls,
the systems-performance literature on common mistakes in experiment design, the
open- versus closed-loop distinction that decides whether a fixed rate or an
unthrottled run answers a given question, coordinated omission in latency
reporting, and the reproducibility checklists the database conferences already
impose on submissions.

Principles it has to carry, at minimum:

- hold everything constant except the factor named as isolated;
- repeat enough that an effect can be distinguished from noise;
- never claim a quantity that one of your own settings has fixed;
- state the claim so that some outcome would refute it;
- size the dataset against the memory envelope deliberately, and say which
  regime you are measuring;
- keep the client off the machine under test, or say why co-location is
  acceptable for this question;
- separate the cost of preparing the system from the cost of measuring it.

## Two risks to design against

**Prescriptiveness.** A handbook that says "pin request equal to limit and use
two client rounds" stops measuring whether the agent can design an experiment
and starts measuring whether it can follow instructions. It must state
principles and the reasoning behind them and let the agent derive specifics.
Anything workload-specific enough to be copied verbatim into a specification is
too specific.

**Context budget.** The catalog and cluster descriptor already consume most of
the window before the model writes a line — roughly thirty thousand characters
of room were left in this session's runs after those two reads. The handbook has
to be short and dense, or split so that only the workload-relevant part is read.

## How it connects to the validator

The relationship should be the one a style guide has with a linter. The
handbook is the normative text. The validator mechanically enforces the subset
that is decidable, and each rejection cites the principle being violated
instead of inventing its own phrasing. This stops the two from drifting apart,
and it turns a rejection into a lesson rather than an obstacle.

The decidable subset to start from, all of which this session's run would have
failed:

- a hypothesis with no criterion that any result could fail;
- a resource request that differs from its limit in an experiment that compares
  anything;
- a single repetition where a comparison is being claimed.

## Why this matters for the paper

If the handbook is a hashed input like the other contracts, two runs are
comparable only when they saw the same one, and the obvious ablation becomes
available: the same model and the same question, with and without the handbook,
scored on the quality of the designs produced. That measures what the method
document is worth. Without it, any claim that the contracts produce valid
experiments rests on the model's priors.

## Open questions still standing

1. One compact document covering every workload, or that plus a short
   per-workload section for the traps specific to key-value and analytical
   runs? Still open: the first exists; whether the second is needed depends on
   what design runs still get wrong.
2. Settled for now: it lives in the agent's own directory, since the catalog and
   result contract are shared with bexhoma while method is the agent's own
   concern, and the contracts directory is out of bounds for agent work.
3. Settled: it is read through the same file-reading tool as the other
   contracts, which keeps provenance uniform. It exceeds the whole-file read
   limit for Markdown, so it is read chapter by chapter — cheaper than a full
   read and apparently well-suited to how a model consults it.
4. Does the interpretation phase need the handbook as a required read the way
   design does? It is currently readable there but not required, because a
   required read that cannot be satisfied is how the comparison-quality gate
   deadlocked. M8 is about conclusions, so this is worth deciding deliberately.
5. Does the handbook actually change design quality? The ablation is now
   available: same model, same question, with and without the document, scored
   on the designs produced. The archived trajectories from before the
   integration are the without arm.

## State of play as of this brief

- YCSB on PostgreSQL, experiment code 1787839849, designed by
  `mistral-small-2603`, finished and was interpreted. Its investigation is
  `agent/trajectories/20260827T160755275940-sf1-mistral-small-2603`. The local
  lifecycle wrapper drove it to the final verdict in external-endpoint mode,
  without starting or stopping any model server; the model asked for no
  follow-up.
- The verdict is the best available argument for the handbook. Throughput came
  out at 999.86 operations per second with one client and 1999.39 with two,
  which is the thousand-per-client ceiling the design itself set, reproduced to
  four figures. The agent reported those as performance findings and declared
  the hypothesis supported. Its latency observation is real — the ninety-ninth
  percentile for updates rose from 793 microseconds to about 1,130 as offered
  load doubled — but it is not what the experiment claimed to be testing.
- Interpretation initially could not run at all for this workload: the
  comparison-quality gate reads only the analytical benchmarker's per-query
  tables and treated their absence as an unmet precondition. Fixed, and logged
  in `docs/FEATURES.md`. Expect more assumptions of that shape elsewhere in the
  harness.
- Shipped in this session: the validator now knows the parameter type YCSB's
  throughput sweeps use; a rejection that used to be a dead end now names the
  ways out; the wrapper can chain phases for an endpoint it does not host, which
  is what makes Mistral and a local Ollama run unattended; and interpretation is
  reachable for a workload whose benchmarker writes no per-query tables.
- Loose end: the wrapper passes the model API key to each phase as a
  command-line argument, so it is visible in the machine's process list. Both
  keys in the local `.env` were exposed today and should be rotated. Handing the
  key through the child's environment instead would fix it; the agent already
  reads it from there.
